#!/usr/bin/env python3
"""
CCNA YouTube Transcript Extractor
==================================
Script de lay transcript tu toan bo playlist Jeremy's IT Lab CCNA 200-301.
Chay tren may tinh ca nhan (khong chay tren Claude).

CACH SU DUNG:
1. Cai dat: pip install youtube-transcript-api pytubefix
2. Chay:    python extract_transcripts.py
3. Ket qua: Thu muc "ccna_transcripts/" chua toan bo transcript

Sau do paste tung file transcript vao Claude de hoc.
"""

import os
import json
import time
import sys

try:
    from pytubefix import Playlist, YouTube
except ImportError:
    print("Chua cai pytubefix. Chay: pip install pytubefix")
    sys.exit(1)

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Chua cai youtube-transcript-api. Chay: pip install youtube-transcript-api")
    sys.exit(1)


PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ"
OUTPUT_DIR = "ccna_transcripts"
SUMMARY_FILE = "ccna_all_titles.txt"


def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None


def get_transcript(video_id, languages=["en", "vi", "en-US"]):
    """Get transcript for a video, trying multiple languages."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get manual transcript first
        for lang in languages:
            try:
                transcript = transcript_list.find_transcript([lang])
                entries = transcript.fetch()
                text = "\n".join([entry.text for entry in entries])
                return text, lang
            except:
                continue
        
        # Try auto-generated
        for lang in languages:
            try:
                transcript = transcript_list.find_generated_transcript([lang])
                entries = transcript.fetch()
                text = "\n".join([entry.text for entry in entries])
                return text, f"{lang} (auto)"
            except:
                continue
                
        return None, None
    except Exception as e:
        return None, str(e)


def main():
    print("=" * 60)
    print("CCNA 200-301 - Jeremy's IT Lab - Transcript Extractor")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get playlist
    print(f"\nDang lay danh sach video tu playlist...")
    try:
        playlist = Playlist(PLAYLIST_URL)
        videos = list(playlist.videos)
        print(f"Tim thay {len(videos)} videos.\n")
    except Exception as e:
        print(f"Loi khi lay playlist: {e}")
        print("Thu lai hoac kiem tra ket noi mang.")
        sys.exit(1)
    
    # Save titles list
    titles = []
    success_count = 0
    fail_count = 0
    
    for i, video in enumerate(videos):
        idx = str(i + 1).zfill(3)
        title = video.title
        video_id = video.video_id
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:80]
        filename = f"{idx}_{safe_title}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        print(f"[{idx}/{len(videos)}] {title}")
        titles.append(f"{idx}. {title} (https://youtu.be/{video_id})")
        
        # Skip if already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
            print(f"  -> Da co, bo qua.")
            success_count += 1
            continue
        
        # Get transcript
        transcript, lang = get_transcript(video_id)
        
        if transcript:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"# Video: https://youtu.be/{video_id}\n")
                f.write(f"# Language: {lang}\n")
                f.write(f"# Index: {i+1}/{len(videos)}\n")
                f.write("=" * 60 + "\n\n")
                f.write(transcript)
            
            print(f"  -> OK ({lang}, {len(transcript)} chars)")
            success_count += 1
        else:
            print(f"  -> KHONG CO transcript: {lang}")
            fail_count += 1
        
        # Rate limiting
        time.sleep(0.5)
    
    # Save titles list
    with open(os.path.join(OUTPUT_DIR, SUMMARY_FILE), "w", encoding="utf-8") as f:
        f.write("JEREMY'S IT LAB - CCNA 200-301 - DANH SACH VIDEO\n")
        f.write("=" * 60 + "\n\n")
        for t in titles:
            f.write(t + "\n")
    
    # Summary
    print("\n" + "=" * 60)
    print("HOAN THANH!")
    print(f"  Thanh cong: {success_count}/{len(videos)}")
    print(f"  That bai:   {fail_count}/{len(videos)}")
    print(f"  Thu muc:    {os.path.abspath(OUTPUT_DIR)}/")
    print(f"  Danh sach:  {OUTPUT_DIR}/{SUMMARY_FILE}")
    print("=" * 60)
    print("\nBUOC TIEP THEO:")
    print("  Mo Claude.ai, paste noi dung transcript va dung prompt template")
    print("  de hoc nhanh. Xem file 'ccna_study_guide.md' de biet cach dung.")


if __name__ == "__main__":
    main()
