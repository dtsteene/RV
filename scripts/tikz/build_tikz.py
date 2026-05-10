"""Compile standalone TikZ figures to PDF and PNG.

Each .tex file in this directory (other than the leading-underscore style
inputs) is compiled with pdflatex and the resulting PDF is rasterised to
PNG via pdftocairo. Both files are written to ../../figures/, where the
MyST chapters reference them.

Usage:
    python build_tikz.py                # build everything
    python build_tikz.py fig_2_8_*      # build a subset
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT.parent.parent / "figures"
DPI = 220


def discover(patterns: list[str]) -> list[Path]:
    if not patterns:
        return sorted(p for p in ROOT.glob("*.tex") if not p.name.startswith("_"))
    selected: list[Path] = []
    for pattern in patterns:
        if not pattern.endswith(".tex"):
            pattern = f"{pattern}.tex" if "*" not in pattern else pattern
        selected.extend(ROOT.glob(pattern))
    return sorted({p for p in selected if not p.name.startswith("_")})


def build_one(tex: Path) -> None:
    name = tex.stem
    print(f"[tikz] {name}")
    subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={ROOT}",
            tex.name,
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    pdf_src = ROOT / f"{name}.pdf"
    pdf_dst = FIGURES / f"{name}.pdf"
    shutil.copy(pdf_src, pdf_dst)
    subprocess.run(
        ["pdftocairo", "-png", "-singlefile", "-r", str(DPI), str(pdf_src), str(FIGURES / name)],
        check=True,
    )
    # Clean intermediate files in scripts/tikz, keep .tex sources.
    for ext in (".aux", ".log", ".pdf"):
        f = ROOT / f"{name}{ext}"
        if f.exists():
            f.unlink()


def main() -> None:
    patterns = sys.argv[1:]
    targets = discover(patterns)
    if not targets:
        print("No .tex targets found.")
        sys.exit(1)
    for tex in targets:
        build_one(tex)


if __name__ == "__main__":
    main()
