#!/usr/bin/env python3
"""Regenere les pages index.html du site et le fichier URLS.txt.

Usage :  python tools/make_index.py

Le script parcourt les dossiers de cours a la racine du depot, liste les
medias qu'ils contiennent et ecrit :
  - index.html            a la racine (page d'accueil)
  - <cours>/index.html    une page par cours
  - URLS.txt              la liste des URLs publiques (pour generer les QR)

Aucune dependance externe. Relancer apres chaque ajout de fichier.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

BASE_URL = "https://ferrucci-franco.github.io/courses-media"

ROOT = Path(__file__).resolve().parent.parent

# Dossiers ignores lors du scan des cours.
SKIP_DIRS = {"tools", ".git", ".github"}

MEDIA_EXT = {
    ".gif", ".png", ".jpg", ".jpeg", ".webp", ".svg",
    ".mp4", ".webm", ".mp3", ".wav", ".pdf",
}
IMAGE_EXT = {".gif", ".png", ".jpg", ".jpeg", ".webp", ".svg"}
VIDEO_EXT = {".mp4", ".webm"}

CSS = """
:root {
  --bg: #fbfaf8; --fg: #1c1b19; --muted: #6b6862;
  --line: #e3e0da; --card: #ffffff; --accent: #8a5a2b;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161513; --fg: #e9e6e0; --muted: #98948c;
    --line: #2e2c28; --card: #1e1d1a; --accent: #d3a06a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 2.5rem 1.25rem 5rem;
  background: var(--bg); color: var(--fg);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
.wrap { max-width: 60rem; margin: 0 auto; }
h1 { font-size: 1.65rem; margin: 0 0 .4rem; letter-spacing: -.01em; }
h2 {
  font-size: 1.05rem; margin: 2.5rem 0 .85rem; padding-bottom: .4rem;
  border-bottom: 1px solid var(--line); font-weight: 600;
}
h2 .count { color: var(--muted); font-weight: 400; font-size: .85rem; }
.lede { color: var(--muted); margin: 0 0 .5rem; max-width: 44rem; }
a { color: var(--accent); }
.back { display: inline-block; margin-bottom: 1.5rem; font-size: .9rem; }
.grid {
  display: grid; gap: 1rem; list-style: none; padding: 0; margin: 0;
  grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
}
.card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 10px; overflow: hidden;
}
.card a.thumb {
  display: block; background: var(--bg); border-bottom: 1px solid var(--line);
  aspect-ratio: 16 / 10; overflow: hidden;
}
.card a.thumb img, .card a.thumb video {
  width: 100%; height: 100%; object-fit: contain; display: block;
}
.card .meta { padding: .7rem .85rem .8rem; }
.card .name {
  font-weight: 600; font-size: .92rem; word-break: break-word;
  text-decoration: none; color: var(--fg);
}
.card .name:hover { color: var(--accent); }
.card .sub { color: var(--muted); font-size: .78rem; margin-top: .2rem; }
.rows { list-style: none; padding: 0; margin: 0; }
.rows li { border-bottom: 1px solid var(--line); }
.rows a { display: flex; justify-content: space-between; gap: 1rem;
          padding: .6rem .2rem; text-decoration: none; }
.rows a:hover { color: var(--accent); }
.rows .sub { color: var(--muted); font-size: .8rem; white-space: nowrap; }
.empty { color: var(--muted); font-style: italic; }
footer { margin-top: 4rem; color: var(--muted); font-size: .8rem; }
"""


def human_size(n: int) -> str:
    if n < 1024:
        return f"{n} o"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} ko"
    return f"{n / 1024 / 1024:.1f} Mo"


def course_title(d: Path) -> str:
    """Nom affiche : contenu de .title s'il existe, sinon le nom du dossier."""
    title_file = d / ".title"
    if title_file.is_file():
        text = title_file.read_text(encoding="utf-8").strip()
        if text:
            return text
    return d.name.replace("-", " ").replace("_", " ").title()


def media_files(d: Path) -> list[Path]:
    return sorted(
        (p for p in d.iterdir()
         if p.is_file() and p.suffix.lower() in MEDIA_EXT),
        key=lambda p: p.name.lower(),
    )


def courses() -> list[Path]:
    return sorted(
        (p for p in ROOT.iterdir()
         if p.is_dir() and not p.name.startswith(".") and p.name not in SKIP_DIRS),
        key=lambda p: p.name.lower(),
    )


def page(title: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n"
        f'<div class="wrap">\n{body}\n'
        "<footer>Page générée automatiquement par "
        "<code>tools/make_index.py</code>.</footer>\n"
        "</div>\n</body>\n</html>\n"
    )


def card(f: Path) -> str:
    href = html.escape(f.name)
    name = html.escape(f.name)
    sub = f"{f.suffix.lstrip('.').upper()} &middot; {human_size(f.stat().st_size)}"
    ext = f.suffix.lower()
    if ext in IMAGE_EXT:
        thumb = f'<a class="thumb" href="{href}"><img src="{href}" alt="" loading="lazy"></a>'
    elif ext in VIDEO_EXT:
        thumb = (f'<a class="thumb" href="{href}">'
                 f'<video src="{href}" muted preload="metadata"></video></a>')
    else:
        thumb = ""
    return (
        f'<li class="card">{thumb}'
        f'<div class="meta"><a class="name" href="{href}">{name}</a>'
        f'<div class="sub">{sub}</div></div></li>'
    )


def write_course_page(d: Path) -> int:
    files = media_files(d)
    title = course_title(d)
    body = [
        '<a class="back" href="../">&larr; Tous les cours</a>',
        f"<h1>{html.escape(title)}</h1>",
        '<p class="lede">Ouvrez un fichier pour le voir en plein écran. '
        "Les liens sont stables : ils ne changeront pas.</p>",
    ]
    if files:
        body.append('<ul class="grid">')
        body.extend(card(f) for f in files)
        body.append("</ul>")
    else:
        body.append('<p class="empty">Aucun fichier pour l&rsquo;instant.</p>')
    (d / "index.html").write_text(page(title, "\n".join(body)), encoding="utf-8")
    return len(files)


def write_home(counts: dict[Path, int]) -> None:
    body = [
        "<h1>Ressources de cours</h1>",
        '<p class="lede">Animations, schémas et documents complémentaires aux '
        "polycopiés. Chaque fichier a une adresse permanente : celle du QR code "
        "imprimé reste valable.</p>",
    ]
    for d, n in counts.items():
        plural = "s" if n != 1 else ""
        body.append(
            f'<h2>{html.escape(course_title(d))} '
            f'<span class="count">&mdash; {n} fichier{plural}</span></h2>'
        )
        files = media_files(d)
        if not files:
            body.append('<p class="empty">Aucun fichier pour l&rsquo;instant.</p>')
            continue
        body.append('<ul class="rows">')
        for f in files:
            body.append(
                f'<li><a href="{html.escape(d.name)}/{html.escape(f.name)}">'
                f"<span>{html.escape(f.name)}</span>"
                f'<span class="sub">{human_size(f.stat().st_size)}</span></a></li>'
            )
        body.append("</ul>")
        body.append(f'<p><a href="{html.escape(d.name)}/">Voir en galerie &rarr;</a></p>')
    (ROOT / "index.html").write_text(
        page("Ressources de cours", "\n".join(body)), encoding="utf-8"
    )


def write_urls(counts: dict[Path, int]) -> int:
    lines = [
        "# URLs publiques - a encoder dans les QR codes.",
        "# Genere par tools/make_index.py : ne pas editer a la main.",
        "",
    ]
    total = 0
    for d in counts:
        files = media_files(d)
        if not files:
            continue
        lines.append(f"## {course_title(d)}")
        for f in files:
            lines.append(f"{BASE_URL}/{d.name}/{f.name}")
            total += 1
        lines.append("")
    (ROOT / "URLS.txt").write_text("\n".join(lines), encoding="utf-8")
    return total


def main() -> int:
    dirs = courses()
    if not dirs:
        print("Aucun dossier de cours trouve.", file=sys.stderr)
        return 1
    counts = {d: write_course_page(d) for d in dirs}
    write_home(counts)
    total = write_urls(counts)
    for d, n in counts.items():
        print(f"  {d.name:<22} {n:>3} fichier(s)")
    print(f"\n{total} fichier(s) au total, {len(dirs)} cours.")
    print("Ecrit : index.html, <cours>/index.html, URLS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
