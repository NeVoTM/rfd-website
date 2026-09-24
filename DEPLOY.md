# RFD.com — Live URLs

- **Render (live now):** https://rfd-website-x19x.onrender.com
- **GitHub:** https://github.com/NeVoTM/rfd-website
- **Google Drive:** [17274/RFD](https://drive.google.com/drive/folders/1Q0rMoUb7ho-rt-m1uwCDSin3FHDJkeir) on elichalfinny@gmail.com

## Custom domain RFD.com

In Render → **rfd-website** → Settings → Custom Domains → Add `rfd.com` and `www.rfd.com`

Point DNS at your registrar:

| Host | Type | Value |
|------|------|-------|
| `www` | CNAME | `rfd-website.onrender.com` |
| `@` | ANAME/ALIAS or redirect | Render root target, or redirect apex → `www.rfd.com` |

Render will issue SSL automatically once DNS propagates.

## Storage

| Layer | Location |
|-------|----------|
| Originals | Google Drive `RFD/01-Originals/` |
| Portraits | `RFD/02-Photos/` + site `public/images/portraits/` |
| Edited clips | Drive `RFD/04-Edited-Backup/` + `public/clips/` + Render |
| Transcripts | Drive `RFD/05-Transcripts/<title>/transcript.txt` (from `scripts/vtt_to_transcript.py`) |
| Code | GitHub NeVoTM/rfd-website |

## Deploy

Push to `main` on GitHub — Render auto-deploys from `NeVoTM/rfd-website`.
