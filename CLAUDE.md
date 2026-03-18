# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal CCNA 200-301 study notes repository based on [Jeremy's IT Lab Complete CCNA course](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ). It contains:

- **`Course_Notes/`** — 60+ Markdown files, one per course "Day", covering every CCNA exam topic
- **`ccna_transcripts/`** — Raw YouTube transcripts extracted from the course playlist
- **`extract_transcripts.py`** / **`ccna_transcript_extractor_v3.py`** — Python scripts to pull transcripts from YouTube
- **`ccna_study_guide.md`** — Aggregated study guide built from course content
- **`CCNA_STUDY_GUIDE_WITH_CLAUDE.txt`** — Prompt templates (in Vietnamese) for studying batches of transcripts with Claude

## Transcript Extraction Scripts

To download transcripts from the Jeremy's IT Lab YouTube playlist:

```bash
# Install dependencies
pip install pytubefix youtube-transcript-api yt-dlp

# Run the extractor (v3 is the current version, fixed for youtube-transcript-api v1.2+)
python ccna_transcript_extractor_v3.py
```

The v3 script outputs to `ccna_transcripts/`:
- Individual transcript files: `001_<title>.txt` … `NNN_<title>.txt`
- `VIDEO_INDEX.txt` — full playlist index grouped by CCNA domain
- `ALL_TRANSCRIPTS.txt` — all transcripts concatenated
- `batches_for_claude/batch_NN.txt` — 5-video batches sized for Claude context windows
- `by_domain/` — transcripts grouped by CCNA exam domain

If yt-dlp fails to fetch the playlist, use the manual fallback:
```bash
yt-dlp --flat-playlist --print url "<playlist_url>" > video_urls.txt
python ccna_transcript_extractor_v3.py
```

## Note Format

Each `Course_Notes/*.md` file follows this pattern:
- Title heading with the Day number and topic
- Embedded images hosted on `github.com/psaumur/CCNA/assets/…`
- Plain-text descriptions, tables, and Cisco IOS command blocks

When adding or editing notes, keep the same structure: heading → images (where applicable) → concept descriptions → command examples.

## CCNA Exam Domains (for classification)

The extractor script maps content to these six domains, which reflect the real exam blueprint:

| Domain | Weight | Key Topics |
|---|---|---|
| Network Fundamentals | 20% | OSI, TCP/IP, IPv4/IPv6, subnetting, ARP |
| Network Access | 20% | VLANs, STP, EtherChannel, wireless |
| IP Connectivity | 25% | Routing, OSPF, static routes, HSRP |
| IP Services | 10% | NAT, DHCP, NTP, SNMP, QoS |
| Security Fundamentals | 15% | ACLs, port security, DHCP snooping, DAI |
| Automation & Programmability | 10% | REST APIs, SDN, Ansible, JSON/YAML |

## Converting Notes to PDF

- **Browser-based:** [Dillinger.io](https://dillinger.io/) — paste Markdown, export PDF
- **Local/bulk:** [Calibre](https://calibre-ebook.com/) — supports batch conversion, good for iPad/mobile
