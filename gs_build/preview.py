#!/usr/bin/env python3
"""Render a built document to PDF with LibreOffice and make contact sheets for a visual check.

    python3 gs_build/preview.py MA         -> gs_build/.cache/preview/MA_01.png ...
Needs: apt-get install -y --no-install-recommends libreoffice-writer ; pip install pymupdf pillow
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import registry          # noqa: E402
from engine import style as S       # noqa: E402


def main(code, per=4, dpi=55):
    import pymupdf
    from PIL import Image
    spec = registry()[code]
    src = S.SUBJECT_DIR / spec["folder"] / spec["file"]
    out = S.CACHE / "preview"
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / f"{code}.docx"
    shutil.copy(src, tmp)
    subprocess.run(["soffice", "--headless", "--norestore", "--convert-to", "pdf", "--outdir", str(out), str(tmp)],
                   check=True, capture_output=True, timeout=600)
    doc = pymupdf.open(out / f"{code}.pdf")
    imgs = []
    for p in doc:
        pm = p.get_pixmap(dpi=dpi)
        imgs.append(Image.frombytes("RGB", [pm.width, pm.height], pm.samples))
    for old in out.glob(f"{code}_*.png"):
        old.unlink()
    for k in range(0, len(imgs), per):
        grp = imgs[k:k + per]
        sheet = Image.new("RGB", (sum(i.width for i in grp) + 12 * (len(grp) - 1), max(i.height for i in grp)), "#777")
        x = 0
        for im in grp:
            sheet.paste(im, (x, 0))
            x += im.width + 12
        sheet.save(out / f"{code}_{k // per + 1:02d}.png")
    print(f"{code}: {doc.page_count} pages -> {out}/{code}_NN.png")


if __name__ == "__main__":
    for c in sys.argv[1:]:
        main(c)
