#!/usr/bin/env python3
"""Generate WebVTT subtitle files for RFD clips from transcript JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "data" / "transcripts"
OUT = ROOT / "public" / "clips"

CLIP_SPECS = [
    {
        "id": "what-a-hasid-is",
        "transcriptId": "hachesed-video",
        "startSec": 64,
        "durationSec": 44,
        "translations": {
            "es": [
                (0.0, 10.0, "El jasid es un carácter humano único. Los animales no tienen jesed."),
                (10.0, 20.0, "Jesed es salir de tu propio pellejo y dar de lo tuyo a gente que nunca conociste."),
                (20.0, 32.0, "Eso es lo que se supone que hagas. Eso es para lo que fuiste creado. Es nuestra identidad como judíos."),
                (32.0, 44.0, "Hay vecinos, en un barrio muy lindo, que simplemente no tienen comida para Shabat."),
            ],
            "fr": [
                (0.0, 10.0, "Le hassid est un caractère humain unique. Les animaux n'ont pas de 'hessed."),
                (10.0, 20.0, "Le 'hessed, c'est sortir de sa peau et donner de soi à des gens qu'on n'a jamais connus."),
                (20.0, 32.0, "C'est ce que tu es censé faire. C'est pour cela que tu as été créé. C'est notre identité de Juifs."),
                (32.0, 44.0, "Il y a des voisins, dans un très beau quartier, qui n'ont tout simplement pas de nourriture pour Chabbat."),
            ],
        },
    },
    {
        "id": "money-goes-direct",
        "transcriptId": "hachesed-video",
        "startSec": 204,
        "durationSec": 45,
        "translations": {
            "es": [
                (0.0, 10.0, "No sé qué haría sin él. Esta ayuda es como un envío de Hashem."),
                (10.0, 22.0, "Siempre es otra cara. Ayuda a viudas y huérfanos. Busca a estas personas."),
                (22.0, 35.0, "El dinero va directo a gente muy necesitada — aquí o en Israel."),
                (35.0, 45.0, "Va a Israel con diez mil dólares en la mano y los reparte. Es extraordinario."),
            ],
            "fr": [
                (0.0, 10.0, "Je ne sais pas ce que je ferais sans lui. Cette aide, c'est comme un envoi d'Hachem."),
                (10.0, 22.0, "Toujours un autre visage. Il aide les veuves et les orphelins. Il va les chercher."),
                (22.0, 35.0, "L'argent va directement à des gens très dans le besoin — ici ou en Israël."),
                (35.0, 45.0, "Il part en Israël avec dix mille dollars en main et les donne. C'est extraordinaire."),
            ],
        },
    },
]


def parse_time(ts: str) -> float:
    parts = ts.split(":")
    h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
    return h * 3600 + m * 60 + s


def format_vtt_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".rstrip("0").rstrip(".")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def segments_from_transcript(transcript_id: str, start_sec: float, duration_sec: float):
    data = json.loads((TRANSCRIPTS / f"{transcript_id}.json").read_text(encoding="utf-8"))
    end_sec = start_sec + duration_sec
    lines = data.get("lines", [])
    parsed = [(parse_time(l["time"]), clean_text(l["text"])) for l in lines]
    in_range = [(t, txt) for t, txt in parsed if start_sec <= t < end_sec]
    if not in_range:
        return []
    segments = []
    for i, (t, txt) in enumerate(in_range):
        rel_start = t - start_sec
        if i + 1 < len(in_range):
            rel_end = in_range[i + 1][0] - start_sec
        else:
            rel_end = min(duration_sec, rel_start + 4.0)
        rel_end = max(rel_end, rel_start + 0.5)
        segments.append((rel_start, rel_end, txt))
    return segments


def write_vtt(path: Path, segments, lang_label: str):
    lines = ["WEBVTT", f"NOTE Language: {lang_label}", ""]
    for i, (start, end, text) in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{format_vtt_time(start)} --> {format_vtt_time(end)}")
        lines.append(text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in CLIP_SPECS:
        en_segments = segments_from_transcript(
            spec["transcriptId"], spec["startSec"], spec["durationSec"]
        )
        write_vtt(OUT / f"{spec['id']}.en.vtt", en_segments, "en")
        for lang in ("es", "fr"):
            write_vtt(OUT / f"{spec['id']}.{lang}.vtt", spec["translations"][lang], lang)
        print(f"{spec['id']}: {len(en_segments)} EN cues, ES/FR translated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
