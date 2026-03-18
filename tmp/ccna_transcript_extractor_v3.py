#!/usr/bin/env python3
"""
CCNA 200-301 YouTube Playlist Transcript Extractor v3
======================================================
Fixed for youtube-transcript-api v1.2.4 (new API)

SETUP:
    pip install pytubefix youtube-transcript-api yt-dlp

USAGE:
    python ccna_transcript_extractor_v3.py
"""

import os
import re
import sys
import time
import json
import subprocess
from pathlib import Path

# ============================================================
# Config
# ============================================================
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ"
OUTPUT_DIR = Path("ccna_transcripts")
BATCH_DIR = OUTPUT_DIR / "batches_for_claude"
BATCH_SIZE = 5

# ============================================================
# Transcript extraction - FIXED for youtube-transcript-api v1.2+
# ============================================================
def get_transcript(video_id: str) -> str:
    """Fetch transcript using the NEW API (v1.0+)."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()

    # Method 1: Direct fetch with language preference
    try:
        transcript = api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
        return '\n'.join(snippet.text for snippet in transcript)
    except Exception:
        pass

    # Method 2: List available transcripts, pick best one
    try:
        transcript_list = api.list(video_id)

        # Try manually created English transcript
        try:
            t = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
            fetched = t.fetch()
            return '\n'.join(snippet.text for snippet in fetched)
        except Exception:
            pass

        # Try auto-generated English transcript
        try:
            t = transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB'])
            fetched = t.fetch()
            return '\n'.join(snippet.text for snippet in fetched)
        except Exception:
            pass

        # Try any transcript and translate to English
        try:
            for t in transcript_list:
                if t.is_translatable:
                    translated = t.translate('en')
                    fetched = translated.fetch()
                    return '\n'.join(snippet.text for snippet in fetched)
        except Exception:
            pass

        # Try find_transcript (finds any matching language)
        try:
            t = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            fetched = t.fetch()
            return '\n'.join(snippet.text for snippet in fetched)
        except Exception:
            pass

    except Exception as e:
        return f"[TRANSCRIPT UNAVAILABLE: {e}]"

    return "[TRANSCRIPT UNAVAILABLE: No English transcript found]"


# ============================================================
# Playlist fetching (same as v2 - multiple fallback methods)
# ============================================================
def extract_video_id(url: str) -> str:
    for pattern in [r'(?:v=|/v/)([a-zA-Z0-9_-]{11})', r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})']:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


def get_playlist_videos_ytdlp():
    print("  Running yt-dlp to fetch playlist metadata...")
    cmd = ["yt-dlp", "--flat-playlist", "--dump-json", "--no-warnings", PLAYLIST_URL]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"yt-dlp error: {result.stderr[:300]}")

    videos = []
    for line in result.stdout.strip().split('\n'):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            vid_id = data.get('id', '')
            title = data.get('title', f'Video_{len(videos)+1}')
            duration = data.get('duration') or 0
            videos.append({
                'url': f'https://www.youtube.com/watch?v={vid_id}',
                'video_id': vid_id,
                'title': title,
                'duration': int(duration),
            })
            print(f"  Found: {len(videos):3d}. {title[:60]}")
        except json.JSONDecodeError:
            continue
    return videos


def get_playlist_videos_pytubefix():
    from pytubefix import Playlist
    p = Playlist(PLAYLIST_URL)
    videos = []
    for i, video in enumerate(p.videos):
        try:
            videos.append({
                'url': video.watch_url,
                'video_id': video.video_id,
                'title': video.title,
                'duration': video.length or 0,
            })
            print(f"  Found: {i+1:3d}. {video.title[:60]}")
        except Exception as e:
            try:
                vid_url = p.video_urls[i]
                vid_id = extract_video_id(vid_url)
                videos.append({'url': vid_url, 'video_id': vid_id, 'title': f'Video_{i+1}', 'duration': 0})
            except:
                pass
    return videos


def get_playlist_videos_manual():
    manual_file = Path("video_urls.txt")
    if not manual_file.exists():
        return None
    videos = []
    with open(manual_file, 'r') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            vid_id = extract_video_id(line)
            if vid_id:
                # Check if line has a title after the URL (tab or | separated)
                parts = re.split(r'\t|\|', line, maxsplit=1)
                title = parts[1].strip() if len(parts) > 1 else f'Video_{i}'
                videos.append({'url': parts[0].strip(), 'video_id': vid_id, 'title': title, 'duration': 0})
    return videos if videos else None


# ============================================================
# Topic classification
# ============================================================
CCNA_DOMAINS = {
    "1-Network_Fundamentals": [
        "osi", "tcp/ip", "ipv4", "ipv6", "subnet", "subnetting", "cidr",
        "cable", "topology", "ethernet", "arp", "icmp", "binary", "hex",
        "broadcast", "unicast", "multicast", "encapsulation", "header",
        "tcp", "udp", "port number", "three-way handshake", "layer",
        "fiber", "utp", "rj-45", "speed", "duplex",
    ],
    "2-Network_Access": [
        "vlan", "trunk", "stp", "spanning tree", "etherchannel",
        "switch", "switching", "wireless", "wlan", "802.1q", "dtp",
        "port channel", "lacp", "pagp", "access port", "native vlan",
        "wifi", "802.11", "wlc", "ap ", "ssid", "rstp", "pvst",
    ],
    "3-IP_Connectivity": [
        "routing", "ospf", "static route", "default route", "router",
        "gateway", "routing table", "administrative distance", "metric",
        "dynamic routing", "next hop", "floating static",
        "loopback", "ospf area", "dr ", "bdr", "lsa", "spf",
        "first hop redundancy", "hsrp", "vrrp",
    ],
    "4-IP_Services": [
        "nat", "pat", "dhcp", "ntp", "snmp", "syslog", "qos",
        "ftp", "tftp", "ssh", "telnet", "cdp", "lldp",
        "inside local", "inside global",
    ],
    "5-Security": [
        "acl", "access list", "access-list", "firewall", "vpn",
        "port security", "aaa", "radius", "tacacs", "ipsec",
        "permit", "deny", "standard acl", "extended acl",
        "dhcp snooping", "arp inspection", "802.1x", "password",
    ],
    "6-Automation": [
        "api", "rest", "json", "sdn", "ansible", "puppet",
        "automation", "programmability", "controller", "dna center",
        "yang", "netconf", "restconf", "python", "script",
    ],
}

def classify_topic(title: str, transcript_text: str) -> str:
    combined = (title + " " + transcript_text[:1500]).lower()
    scores = {}
    for domain, keywords in CCNA_DOMAINS.items():
        score = sum(combined.count(kw.lower()) for kw in keywords)
        if score > 0:
            scores[domain] = score
    return max(scores, key=scores.get) if scores else "0-General"


def sanitize_filename(name: str, max_length: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '_', name.strip())
    name = re.sub(r'[^\w\-.]', '', name)
    return name[:max_length]


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 70)
    print("CCNA 200-301 - YouTube Transcript Extractor v3")
    print("(Fixed for youtube-transcript-api v1.2+)")
    print("=" * 70)

    # Check deps
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        print(f"[OK] youtube-transcript-api loaded (new API)")
    except ImportError:
        print("ERROR: pip install youtube-transcript-api")
        sys.exit(1)

    has_ytdlp = False
    has_pytubefix = False
    try:
        r = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        if r.returncode == 0:
            has_ytdlp = True
            print(f"[OK] yt-dlp v{r.stdout.strip()}")
    except FileNotFoundError:
        pass
    try:
        import pytubefix
        has_pytubefix = True
        print(f"[OK] pytubefix loaded")
    except ImportError:
        pass

    if not has_ytdlp and not has_pytubefix:
        print("ERROR: Need at least one: pip install pytubefix  OR  pip install yt-dlp")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)
    BATCH_DIR.mkdir(exist_ok=True)

    # ---- Step 1: Get video list ----
    print(f"\nPlaylist: {PLAYLIST_URL}")
    print(f"Output:   {OUTPUT_DIR.absolute()}\n")

    videos = get_playlist_videos_manual()
    if videos:
        print(f"Loaded {len(videos)} videos from video_urls.txt\n")

    if not videos and has_ytdlp:
        print("Fetching playlist with yt-dlp...")
        try:
            videos = get_playlist_videos_ytdlp()
            print(f"  Got {len(videos)} videos.\n")
        except Exception as e:
            print(f"  Failed: {e}\n")

    if not videos and has_pytubefix:
        print("Fetching playlist with pytubefix...")
        try:
            videos = get_playlist_videos_pytubefix()
            print(f"  Got {len(videos)} videos.\n")
        except Exception as e:
            print(f"  Failed: {e}\n")

    if not videos:
        print("ERROR: Could not fetch playlist.")
        print(f"\nManual fallback: run this command and retry:")
        print(f'  yt-dlp --flat-playlist --print url "{PLAYLIST_URL}" > video_urls.txt')
        sys.exit(1)

    # ---- Step 2: Extract transcripts ----
    print(f"Extracting transcripts for {len(videos)} videos...\n")

    all_transcripts = []
    failed_videos = []

    for i, video in enumerate(videos, 1):
        vid_id = video['video_id']
        title = video['title']
        duration = video['duration']
        
        print(f"[{i:3d}/{len(videos)}] {title[:55]}...", end=" ", flush=True)

        transcript = get_transcript(vid_id)

        if "[TRANSCRIPT UNAVAILABLE" in transcript:
            print("SKIP (no transcript)")
            failed_videos.append((i, title, video['url']))
        else:
            domain = classify_topic(title, transcript)
            word_count = len(transcript.split())
            print(f"OK ({word_count} words)")

            safe_name = sanitize_filename(title)
            filename = f"{i:03d}_{safe_name}.txt"

            with open(OUTPUT_DIR / filename, 'w', encoding='utf-8') as f:
                f.write(f"VIDEO {i}: {title}\n")
                f.write(f"URL: {video['url']}\n")
                f.write(f"CCNA Domain: {domain}\n")
                f.write(f"Duration: {duration // 60}m {duration % 60}s\n")
                f.write("=" * 70 + "\n\n")
                f.write(transcript)

            all_transcripts.append({
                'index': i, 'title': title, 'url': video['url'],
                'domain': domain, 'duration': duration,
                'transcript': transcript, 'filename': filename,
            })

        time.sleep(0.3)

    # ---- Step 3: Generate output files ----
    print(f"\nGenerating study materials...")

    # Video Index
    with open(OUTPUT_DIR / "VIDEO_INDEX.txt", 'w', encoding='utf-8') as f:
        f.write("CCNA 200-301 - Complete Course Video Index\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total: {len(videos)} | Extracted: {len(all_transcripts)} | Failed: {len(failed_videos)}\n\n")

        domains_sorted = sorted(set(v['domain'] for v in all_transcripts))
        for domain in domains_sorted:
            dvids = [v for v in all_transcripts if v['domain'] == domain]
            total_min = sum(v['duration'] for v in dvids) // 60
            f.write(f"\n{domain} ({len(dvids)} videos, ~{total_min} min):\n")
            for v in dvids:
                dur = f"{v['duration']//60}m" if v['duration'] else "?"
                f.write(f"  {v['index']:3d}. ({dur}) {v['title']}\n")

        if failed_videos:
            f.write(f"\n\nFAILED ({len(failed_videos)} videos - watch manually):\n")
            for idx, title, url in failed_videos:
                f.write(f"  {idx:3d}. {title}\n       {url}\n")

    # Combined transcript
    with open(OUTPUT_DIR / "ALL_TRANSCRIPTS.txt", 'w', encoding='utf-8') as f:
        for v in all_transcripts:
            f.write(f"\n{'#' * 70}\n")
            f.write(f"# VIDEO {v['index']}: {v['title']}\n")
            f.write(f"# Domain: {v['domain']}\n")
            f.write(f"{'#' * 70}\n\n")
            f.write(v['transcript'])
            f.write("\n")

    # Batches for Claude
    batch_count = 0
    for start in range(0, len(all_transcripts), BATCH_SIZE):
        batch = all_transcripts[start:start + BATCH_SIZE]
        batch_count += 1
        with open(BATCH_DIR / f"batch_{batch_count:02d}.txt", 'w', encoding='utf-8') as f:
            f.write(f"CCNA 200-301 - Batch {batch_count} (Videos {batch[0]['index']}-{batch[-1]['index']})\n")
            f.write("=" * 70 + "\n")
            for v in batch:
                f.write(f"\n--- VIDEO {v['index']}: {v['title']} ---\n")
                f.write(f"Domain: {v['domain']}\n\n")
                f.write(v['transcript'])
                f.write("\n")

    # Domain-grouped files
    domain_dir = OUTPUT_DIR / "by_domain"
    domain_dir.mkdir(exist_ok=True)
    for domain in domains_sorted:
        dvids = [v for v in all_transcripts if v['domain'] == domain]
        with open(domain_dir / f"{domain}.txt", 'w', encoding='utf-8') as f:
            f.write(f"CCNA Domain: {domain} ({len(dvids)} videos)\n")
            f.write("=" * 70 + "\n")
            for v in dvids:
                f.write(f"\n--- VIDEO {v['index']}: {v['title']} ---\n\n")
                f.write(v['transcript'])
                f.write("\n")

    # Summary
    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)
    print(f"""
  Extracted: {len(all_transcripts)}/{len(videos)} videos
  Failed:    {len(failed_videos)} videos
  Batches:   {batch_count} files in {BATCH_DIR}/
  Domains:   {len(domains_sorted)} groups in {OUTPUT_DIR}/by_domain/

  NEXT: Copy batches_for_claude/batch_01.txt into claude.ai
  See CCNA_STUDY_GUIDE_WITH_CLAUDE.txt for prompt templates.
""")


if __name__ == "__main__":
    main()
