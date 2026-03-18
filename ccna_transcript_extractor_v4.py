#!/usr/bin/env python3
"""
CCNA 200-301 YouTube Transcript Extractor v4
==============================================
3-layer fallback:
  1. youtube-transcript-api (fastest)
  2. yt-dlp auto-subtitle extraction (catches more)
  3. yt-dlp audio download + OpenAI Whisper (catches all)

SETUP:
    pip install pytubefix youtube-transcript-api yt-dlp openai-whisper

    Note: openai-whisper is optional. Only needed if methods 1 & 2 fail.
    Whisper requires ~1-2GB download on first run (model weights).
    If you have a CUDA GPU, also install: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

USAGE:
    python ccna_transcript_extractor_v4.py              # Methods 1 & 2 only
    python ccna_transcript_extractor_v4.py --whisper     # Enable Whisper for remaining
    python ccna_transcript_extractor_v4.py --whisper-only # Only Whisper failed videos from previous run
"""

import os
import re
import sys
import time
import json
import subprocess
import argparse
from pathlib import Path

# ============================================================
# Config
# ============================================================
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ"
OUTPUT_DIR = Path("ccna_transcripts")
BATCH_DIR = OUTPUT_DIR / "batches_for_claude"
AUDIO_DIR = OUTPUT_DIR / "_audio_temp"
BATCH_SIZE = 5

# ============================================================
# Transcript Method 1: youtube-transcript-api
# ============================================================
def get_transcript_api(video_id: str) -> str | None:
    """Try youtube-transcript-api (v1.2+)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()

        # Direct fetch
        try:
            transcript = api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
            text = '\n'.join(s.text for s in transcript)
            if text.strip():
                return text
        except Exception:
            pass

        # List and find
        try:
            tlist = api.list(video_id)
            for method in ['find_manually_created_transcript', 'find_generated_transcript', 'find_transcript']:
                try:
                    t = getattr(tlist, method)(['en', 'en-US', 'en-GB'])
                    fetched = t.fetch()
                    text = '\n'.join(s.text for s in fetched)
                    if text.strip():
                        return text
                except Exception:
                    continue

            # Translate from any language
            for t in tlist:
                if t.is_translatable:
                    try:
                        translated = t.translate('en')
                        fetched = translated.fetch()
                        text = '\n'.join(s.text for s in fetched)
                        if text.strip():
                            return text
                    except Exception:
                        continue
        except Exception:
            pass
    except Exception:
        pass

    return None


# ============================================================
# Transcript Method 2: yt-dlp subtitle extraction
# ============================================================
def get_transcript_ytdlp_subs(video_id: str) -> str | None:
    """Use yt-dlp to extract auto-generated subtitles."""
    import tempfile

    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        out_template = os.path.join(tmpdir, "subs")
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--convert-subs", "srt",
            "-o", out_template,
            "--no-warnings",
            url,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

        # Look for downloaded subtitle file
        for ext in ['.en.srt', '.en.vtt', '.srt', '.vtt']:
            sub_file = Path(tmpdir) / f"subs{ext}"
            if sub_file.exists():
                raw = sub_file.read_text(encoding='utf-8', errors='replace')
                # Parse SRT/VTT to plain text
                lines = []
                for line in raw.split('\n'):
                    line = line.strip()
                    # Skip timestamps, sequence numbers, VTT headers
                    if not line:
                        continue
                    if re.match(r'^\d+$', line):
                        continue
                    if re.match(r'[\d:,.\-\s>]+$', line):
                        continue
                    if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                        continue
                    if line.startswith('NOTE'):
                        continue
                    # Remove HTML tags
                    clean = re.sub(r'<[^>]+>', '', line)
                    # Remove VTT positioning
                    clean = re.sub(r'align:start position:\d+%', '', clean)
                    clean = clean.strip()
                    if clean and clean not in lines[-1:]:  # deduplicate consecutive
                        lines.append(clean)

                text = '\n'.join(lines)
                if len(text.strip()) > 50:  # meaningful content
                    return text

    return None


# ============================================================
# Transcript Method 3: Whisper (local AI transcription)
# ============================================================
def download_audio(video_id: str, output_dir: Path) -> Path | None:
    """Download audio using yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = output_dir / f"{video_id}.mp3"

    if output_path.exists():
        return output_path

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "5",  # lower quality = smaller file, faster transcription
        "-o", str(output_dir / f"{video_id}.%(ext)s"),
        "--no-warnings",
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if output_path.exists():
            return output_path
        # yt-dlp might save with different extension before converting
        for f in output_dir.glob(f"{video_id}.*"):
            if f.suffix in ['.mp3', '.m4a', '.wav', '.opus', '.webm']:
                return f
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return None


def transcribe_whisper(audio_path: Path, model_name: str = "base") -> str | None:
    """Transcribe audio using OpenAI Whisper."""
    try:
        import whisper
    except ImportError:
        return None

    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(str(audio_path), language="en")
        text = result.get("text", "")
        return text if text.strip() else None
    except Exception as e:
        print(f"\n    Whisper error: {e}")
        return None


# ============================================================
# Playlist fetching
# ============================================================
def extract_video_id(url: str) -> str:
    for p in [r'(?:v=|/v/)([a-zA-Z0-9_-]{11})', r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})']:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return ""


def get_playlist_videos():
    """Try multiple methods to get video list."""
    # Manual file
    manual = Path("video_urls.txt")
    if manual.exists():
        videos = []
        with open(manual, 'r') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                vid_id = extract_video_id(line)
                if vid_id:
                    parts = re.split(r'\t|\|', line, maxsplit=1)
                    title = parts[1].strip() if len(parts) > 1 else f'Video_{i}'
                    videos.append({'url': parts[0].strip(), 'video_id': vid_id, 'title': title, 'duration': 0})
        if videos:
            print(f"Loaded {len(videos)} videos from video_urls.txt")
            return videos

    # yt-dlp
    try:
        print("Fetching playlist with yt-dlp...")
        cmd = ["yt-dlp", "--flat-playlist", "--dump-json", "--no-warnings", PLAYLIST_URL]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            videos = []
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    vid_id = data.get('id', '')
                    videos.append({
                        'url': f'https://www.youtube.com/watch?v={vid_id}',
                        'video_id': vid_id,
                        'title': data.get('title', f'Video_{len(videos)+1}'),
                        'duration': int(data.get('duration') or 0),
                    })
                except json.JSONDecodeError:
                    continue
            if videos:
                print(f"  Found {len(videos)} videos")
                return videos
    except Exception as e:
        print(f"  yt-dlp failed: {e}")

    # pytubefix
    try:
        from pytubefix import Playlist
        print("Fetching playlist with pytubefix...")
        p = Playlist(PLAYLIST_URL)
        videos = []
        for i, v in enumerate(p.videos):
            try:
                videos.append({'url': v.watch_url, 'video_id': v.video_id, 'title': v.title, 'duration': v.length or 0})
            except:
                pass
        if videos:
            print(f"  Found {len(videos)} videos")
            return videos
    except Exception as e:
        print(f"  pytubefix failed: {e}")

    return None


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
    ],
    "5-Security": [
        "acl", "access list", "access-list", "firewall", "vpn",
        "port security", "aaa", "radius", "tacacs", "ipsec",
        "permit", "deny", "dhcp snooping", "arp inspection", "802.1x",
    ],
    "6-Automation": [
        "api", "rest", "json", "sdn", "ansible", "puppet",
        "automation", "programmability", "dna center",
        "yang", "netconf", "restconf",
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
    parser = argparse.ArgumentParser(description="CCNA 200-301 Transcript Extractor v4")
    parser.add_argument('--whisper', action='store_true', help='Enable Whisper for videos without subtitles')
    parser.add_argument('--whisper-only', action='store_true', help='Only process previously failed videos with Whisper')
    parser.add_argument('--whisper-model', default='base', choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size (default: base). Larger = more accurate but slower.')
    parser.add_argument('--start', type=int, default=1, help='Start from video number N (skip earlier videos)')
    parser.add_argument('--end', type=int, default=None, help='End at video number N')
    args = parser.parse_args()

    print("=" * 70)
    print("CCNA 200-301 - YouTube Transcript Extractor v4")
    print("3-layer: transcript-api → yt-dlp subs → Whisper")
    print("=" * 70)

    OUTPUT_DIR.mkdir(exist_ok=True)
    BATCH_DIR.mkdir(exist_ok=True)

    # Check Whisper availability
    has_whisper = False
    if args.whisper or args.whisper_only:
        try:
            import whisper
            has_whisper = True
            print(f"[OK] Whisper available (model: {args.whisper_model})")
            AUDIO_DIR.mkdir(exist_ok=True)
        except ImportError:
            print("[!!] Whisper not installed. Install: pip install openai-whisper")
            if args.whisper_only:
                sys.exit(1)

    # Get video list
    videos = get_playlist_videos()
    if not videos:
        print("ERROR: Could not fetch playlist.")
        print(f'Try: yt-dlp --flat-playlist --print url "{PLAYLIST_URL}" > video_urls.txt')
        sys.exit(1)

    # Load previous results if whisper-only mode
    failed_file = OUTPUT_DIR / "_failed_videos.json"
    if args.whisper_only:
        if not failed_file.exists():
            print("No _failed_videos.json found. Run without --whisper-only first.")
            sys.exit(1)
        with open(failed_file, 'r') as f:
            failed_indices = set(json.load(f))
        videos = [v for i, v in enumerate(videos, 1) if i in failed_indices]
        print(f"\nProcessing {len(videos)} previously failed videos with Whisper...\n")

    # ---- Extract transcripts ----
    # Apply --start and --end filters
    total_in_playlist = len(videos)
    if not args.whisper_only:
        end_idx = args.end if args.end else len(videos)
        videos = videos[args.start - 1:end_idx]
        if args.start > 1 or args.end:
            print(f"Processing videos {args.start} to {end_idx} ({len(videos)} videos)\n")
        else:
            print(f"\nProcessing {len(videos)} videos...\n")
    else:
        print(f"\nProcessing {len(videos)} videos...\n")

    all_transcripts = []
    failed_videos = []

    # Load existing transcripts (to avoid re-processing)
    existing = {}
    if args.whisper_only:
        for f in OUTPUT_DIR.glob("*.txt"):
            m = re.match(r'^(\d+)_', f.name)
            if m:
                existing[int(m.group(1))] = f

    for i_raw, video in enumerate(videos):
        # Determine actual index
        if args.whisper_only:
            # video_urls are already filtered, find original index
            all_vids = get_playlist_videos()
            idx = next((j for j, v in enumerate(all_vids, 1) if v['video_id'] == video['video_id']), i_raw + 1)
        else:
            idx = i_raw + args.start  # offset by start

        vid_id = video['video_id']
        title = video['title']
        duration = video['duration']

        print(f"[{idx:3d}/{total_in_playlist}] {title[:50]}...", end=" ", flush=True)

        transcript = None
        method_used = ""

        # Method 1: transcript API
        if not args.whisper_only:
            transcript = get_transcript_api(vid_id)
            if transcript:
                method_used = "API"

        # Method 2: yt-dlp subtitles
        if not transcript and not args.whisper_only:
            transcript = get_transcript_ytdlp_subs(vid_id)
            if transcript:
                method_used = "yt-dlp-subs"

        # Method 3: Whisper
        if not transcript and (args.whisper or args.whisper_only) and has_whisper:
            print("downloading audio...", end=" ", flush=True)
            audio_path = download_audio(vid_id, AUDIO_DIR)
            if audio_path:
                print("transcribing...", end=" ", flush=True)
                transcript = transcribe_whisper(audio_path, args.whisper_model)
                if transcript:
                    method_used = "Whisper"
                # Clean up audio to save space
                try:
                    audio_path.unlink()
                except:
                    pass

        if transcript:
            domain = classify_topic(title, transcript)
            word_count = len(transcript.split())
            print(f"OK ({word_count} words, {method_used})")

            safe_name = sanitize_filename(title)
            filename = f"{idx:03d}_{safe_name}.txt"

            with open(OUTPUT_DIR / filename, 'w', encoding='utf-8') as f:
                f.write(f"VIDEO {idx}: {title}\n")
                f.write(f"URL: {video['url']}\n")
                f.write(f"CCNA Domain: {domain}\n")
                f.write(f"Duration: {duration // 60}m {duration % 60}s\n")
                f.write(f"Transcript method: {method_used}\n")
                f.write("=" * 70 + "\n\n")
                f.write(transcript)

            all_transcripts.append({
                'index': idx, 'title': title, 'url': video['url'],
                'domain': domain, 'duration': duration,
                'transcript': transcript, 'filename': filename,
                'method': method_used,
            })
        else:
            print("SKIP (all methods failed)")
            failed_videos.append((idx, title, video['url']))

        time.sleep(0.3)

    # Save failed list for --whisper-only later
    if failed_videos and not args.whisper_only:
        with open(failed_file, 'w') as f:
            json.dump([idx for idx, _, _ in failed_videos], f)

    # ---- Generate output files ----
    # Collect ALL transcripts (including from previous runs)
    if args.whisper_only:
        # Merge with existing
        for f in sorted(OUTPUT_DIR.glob("[0-9][0-9][0-9]_*.txt")):
            m = re.match(r'^(\d+)_', f.name)
            if m:
                idx = int(m.group(1))
                if not any(t['index'] == idx for t in all_transcripts):
                    content = f.read_text(encoding='utf-8')
                    # Parse header
                    lines = content.split('\n')
                    title = lines[0].replace(f'VIDEO {idx}: ', '') if lines else f'Video_{idx}'
                    url_line = lines[1] if len(lines) > 1 else ''
                    url = url_line.replace('URL: ', '') if url_line.startswith('URL:') else ''
                    domain_line = lines[2] if len(lines) > 2 else ''
                    domain = domain_line.replace('CCNA Domain: ', '') if domain_line.startswith('CCNA') else '0-General'
                    # Get transcript body (after === line)
                    body_start = content.find('=' * 70)
                    body = content[body_start + 71:].strip() if body_start >= 0 else content
                    all_transcripts.append({
                        'index': idx, 'title': title, 'url': url,
                        'domain': domain, 'duration': 0,
                        'transcript': body, 'filename': f.name,
                        'method': 'previous',
                    })

    all_transcripts.sort(key=lambda x: x['index'])

    print(f"\nGenerating study materials for {len(all_transcripts)} videos...")

    # Video Index
    with open(OUTPUT_DIR / "VIDEO_INDEX.txt", 'w', encoding='utf-8') as f:
        f.write("CCNA 200-301 - Complete Course Video Index\n")
        f.write("=" * 70 + "\n\n")
        total_all = 126
        f.write(f"Total in playlist: {total_all}\n")
        f.write(f"Transcripts ready: {len(all_transcripts)}\n")
        f.write(f"Still missing:     {len(failed_videos)}\n\n")

        # Stats by method
        methods = {}
        for t in all_transcripts:
            m = t.get('method', 'unknown')
            methods[m] = methods.get(m, 0) + 1
        f.write("By extraction method:\n")
        for m, count in sorted(methods.items()):
            f.write(f"  {m}: {count} videos\n")

        f.write("\n\nBY CCNA EXAM DOMAIN:\n")
        f.write("-" * 50 + "\n")
        domains_sorted = sorted(set(v['domain'] for v in all_transcripts))
        for domain in domains_sorted:
            dvids = [v for v in all_transcripts if v['domain'] == domain]
            f.write(f"\n{domain} ({len(dvids)} videos):\n")
            for v in dvids:
                dur = f"{v['duration']//60}m" if v['duration'] else "?"
                f.write(f"  {v['index']:3d}. ({dur}) {v['title']}\n")

        if failed_videos:
            f.write(f"\n\nSTILL MISSING ({len(failed_videos)} videos):\n")
            f.write("-" * 50 + "\n")
            for idx, title, url in failed_videos:
                f.write(f"  {idx:3d}. {title}\n       {url}\n")
            f.write(f"\nTo transcribe these, run:\n")
            f.write(f"  pip install openai-whisper\n")
            f.write(f"  python ccna_transcript_extractor_v4.py --whisper-only\n")

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
  Transcripts ready: {len(all_transcripts)}/126
  Still missing:     {len(failed_videos)}
  Batches:           {batch_count} files in {BATCH_DIR}/

  Output: {OUTPUT_DIR.absolute()}""")

    if failed_videos:
        print(f"""
  {len(failed_videos)} videos still need transcripts.
  To fix, run:
    pip install openai-whisper
    python ccna_transcript_extractor_v4.py --whisper-only
    (or --whisper-only --whisper-model small  for better accuracy)
""")
    else:
        print(f"\n  All 126 videos extracted! Ready to study with Claude.")

    print(f"  See CCNA_STUDY_GUIDE_WITH_CLAUDE.txt for prompt templates.\n")


if __name__ == "__main__":
    main()
