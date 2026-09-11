#!/usr/bin/env python3
"""Genere un QR code par media, pret a inserer dans le polycopie.

Usage :
    python tools/make_qr.py                  # tout, PDF vectoriel de 18 mm
    python tools/make_qr.py electronics      # un seul cours
    python tools/make_qr.py --size 25        # 25 mm de cote
    python tools/make_qr.py --png            # ajoute des PNG a 600 dpi

Les fichiers sont ecrits dans qr/<cours>/<nom>.pdf, en miroir de la structure
du depot. Le PDF est vectoriel et fait exactement la taille demandee : dans le
polycopie, \\includegraphics sans option donne la bonne dimension.

Dependance : segno (pur Python).
    <interpreteur> -m pip install segno
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_index as mi  # noqa: E402  (meme dossier, structure partagee)

try:
    import segno
except ModuleNotFoundError:
    sys.exit(
        "Le module 'segno' est introuvable pour cet interpreteur :\n"
        f"  {sys.executable}\n\n"
        "Installez-le, ou utilisez l'interpreteur qui l'a deja :\n"
        f"  {sys.executable} -m pip install segno"
    )

MM_PER_INCH = 25.4
PT_PER_INCH = 72.0

# Marge blanche autour du symbole, en modules. La norme QR en impose 4 :
# en dessous, les lecteurs decrochent sur fond imprime.
DEFAULT_BORDER = 4
DEFAULT_SIZE_MM = 18.0
DEFAULT_PNG_DPI = 600


def qr_outputs(out_root: Path, course: str, files: list[Path]) -> dict[Path, str]:
    """Associe chaque media au nom de base de son QR.

    On utilise le nom sans extension ; si deux medias du meme cours ne
    different que par l'extension, on garde l'extension pour lever
    l'ambiguite.
    """
    stems: dict[str, int] = {}
    for f in files:
        stems[f.stem] = stems.get(f.stem, 0) + 1
    return {
        f: (f.stem if stems[f.stem] == 1 else f.name.replace(".", "-"))
        for f in files
    }


def pdf_scale(qr: "segno.QRCode", size_mm: float, border: int) -> float:
    """Echelle (points par module) pour obtenir un cote de `size_mm`."""
    modules = qr.symbol_size(scale=1, border=border)[0]
    return (size_mm / MM_PER_INCH * PT_PER_INCH) / modules


def png_geometry(qr: "segno.QRCode", size_mm: float, border: int,
                 dpi: int) -> tuple[int, float]:
    """Echelle entiere (pixels par module) et resolution a inscrire dans le PNG.

    L'echelle doit etre entiere, sinon un pixel tombe a cheval sur deux modules
    et le symbole devient flou. On arrondit donc l'echelle, puis on recalcule la
    resolution reelle pour que la taille *physique* reste exactement `size_mm` :
    c'est cette resolution que graphicx lit pour dimensionner l'image.
    """
    modules = qr.symbol_size(scale=1, border=border)[0]
    scale = max(1, round((size_mm / MM_PER_INCH * dpi) / modules))
    actual_dpi = scale * modules / (size_mm / MM_PER_INCH)
    return scale, actual_dpi


def main() -> int:
    p = argparse.ArgumentParser(
        description="Genere les QR codes des medias du depot.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("courses", nargs="*",
                   help="Dossiers de cours a traiter (defaut : tous).")
    p.add_argument("--size", type=float, default=DEFAULT_SIZE_MM, metavar="MM",
                   help=f"Cote du QR en mm (defaut : {DEFAULT_SIZE_MM:g}).")
    p.add_argument("--error", default="m", choices=["l", "m", "q", "h"],
                   help="Niveau de correction d'erreur minimal (defaut : m).")
    p.add_argument("--no-boost", action="store_true",
                   help="Ne pas remonter le niveau de correction, meme quand "
                        "c'est gratuit en taille.")
    p.add_argument("--border", type=int, default=DEFAULT_BORDER, metavar="N",
                   help=f"Marge blanche en modules (defaut : {DEFAULT_BORDER}).")
    p.add_argument("--png", action="store_true",
                   help=f"Ecrire aussi des PNG a {DEFAULT_PNG_DPI} dpi.")
    p.add_argument("--dpi", type=int, default=DEFAULT_PNG_DPI, metavar="N",
                   help=f"Resolution des PNG (defaut : {DEFAULT_PNG_DPI}).")
    p.add_argument("--out", default="qr", metavar="DIR",
                   help="Dossier de sortie (defaut : qr).")
    args = p.parse_args()

    all_courses = mi.courses()
    if args.courses:
        wanted = set(args.courses)
        selected = [d for d in all_courses if d.name in wanted]
        unknown = wanted - {d.name for d in all_courses}
        if unknown:
            print(f"Cours inconnu(s) : {', '.join(sorted(unknown))}", file=sys.stderr)
            print(f"Disponibles : {', '.join(d.name for d in all_courses)}",
                  file=sys.stderr)
            return 1
    else:
        selected = all_courses

    out_root = mi.ROOT / args.out
    manifest: list[str] = [
        "# QR codes generes par tools/make_qr.py",
        f"# Taille : {args.size:g} mm  -  correction : {args.error.upper()}"
        f"{'' if args.no_boost else ' minimum'}  -  marge : {args.border} modules",
        "",
    ]
    total = 0
    smallest_module_mm = None

    for d in selected:
        files = mi.media_files(d)
        if not files:
            continue
        names = qr_outputs(out_root, d.name, files)
        dest = out_root / d.name
        dest.mkdir(parents=True, exist_ok=True)
        manifest.append(f"## {mi.course_title(d)}")

        for f in files:
            url = f"{mi.BASE_URL}/{d.name}/{f.name}"
            qr = segno.make(url, error=args.error, boost_error=not args.no_boost)
            base = names[f]

            scale = pdf_scale(qr, args.size, args.border)
            qr.save(dest / f"{base}.pdf", scale=scale, border=args.border)

            module_mm = args.size / qr.symbol_size(scale=1, border=args.border)[0]
            if smallest_module_mm is None or module_mm < smallest_module_mm:
                smallest_module_mm = module_mm

            line = f"{f.name}  ->  {args.out}/{d.name}/{base}.pdf"
            if args.png:
                s, real_dpi = png_geometry(qr, args.size, args.border, args.dpi)
                qr.save(dest / f"{base}.png", scale=s, border=args.border,
                        dpi=real_dpi)
                line += " + .png"

            manifest.append(f"{line}")
            manifest.append(f"    {url}")
            manifest.append(
                f"    \\includegraphics{{{args.out}/{d.name}/{base}.pdf}}"
                f"   % version {qr.version}, correction {qr.error}"
            )
            total += 1

        manifest.append("")
        print(f"  {d.name:<22} {len(files):>3} QR")

    if total == 0:
        print("\nAucun media a encoder : ajoutez des fichiers dans les dossiers "
              "de cours, puis relancez.")
        return 0

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "MANIFEST.txt").write_text("\n".join(manifest), encoding="utf-8")

    print(f"\n{total} QR code(s) dans {args.out}/ ({args.size:g} mm de cote).")
    print(f"Plus petit module : {smallest_module_mm:.2f} mm "
          f"(seuil pratique a l'impression : 0,40 mm).")
    print(f"Recapitulatif et lignes \\includegraphics : {args.out}/MANIFEST.txt")

    # Sous ~0,4 mm par module, l'impression bave et les lecteurs decrochent.
    if smallest_module_mm < 0.4:
        needed = args.size * 0.4 / smallest_module_mm
        print(
            f"\nAttention : modules trop fins pour une impression fiable.\n"
            f"Passez a --size {needed:.0f} ou raccourcissez les noms de fichiers "
            f"(une URL plus courte = moins de modules).",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
