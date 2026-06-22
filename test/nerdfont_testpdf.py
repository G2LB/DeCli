#!/usr/bin/env python3
"""
test/nerdfont_testpdf.py — genereert een test-PDF (classic-stijl) met alle
NERD_GLYPH_* glyphs uit DeCli.py + een tabel. Glyphs worden getekend met de
JetBrains Mono Nerd Font (NERD_FONT_PATH); de tekst in Times-Roman (classic).

Gebruik:  py test/nerdfont_testpdf.py [uitvoer.pdf]
"""
import os
import sys

# DeCli.py staat één map omhoog
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fitz  # noqa: E402
import DeCli  # noqa: E402  -> NERD_GLYPH_* + NERD_FONT_PATH

# (constante-naam, label, class, codepoint)
ROWS = [
    ("NERD_GLYPH_OCR",     "OCR",             "nf-md-ocr",                0xF113A),
    ("NERD_GLYPH_EUR",     "EUR",             "nf-md-currency_eur",       0xF01AD),
    ("NERD_GLYPH_JSON",    "JSON",            "nf-md-code_json",          0xF0626),
    ("NERD_GLYPH_GITHUB",  "GitHub-logo",     "nf-fa-github",             0xF09B),
    ("NERD_GLYPH_IMAGE",   "Afbeelding",      "nf-fa-image",              0xF03E),
    ("NERD_GLYPH_ZIP",     "ZIP / map",       "nf-md-folder_zip_outline", 0xF07B9),
    ("NERD_GLYPH_TERM",    "Terminal",        "nf-fa-terminal",           0xF120),
    ("NERD_GLYPH_MATCH",   "Locatie / match", "nf-md-map_marker_check",   0xF0C95),
    ("NERD_GLYPH_RECEIPT", "Bonnetje",        "nf-md-receipt",            0xF0449),
    ("NERD_GLYPH_CAMERA",  "Foto / EXIF",     "nf-md-camera",             0xF0100),
    ("NERD_GLYPH_CASH",    "Bedrag (cash)",   "nf-md-cash_multiple",      0xF0116),
    ("NERD_GLYPH_GITHUB2", "GitHub (alt)",    "nf-md-github",             0xF02A4),
    ("NERD_GLYPH_IMGMARK", "Afbeeld. marker", "nf-md-image_marker",       0xF177B),
    ("NERD_GLYPH_IMGSYNC", "Afbeeld. sync",   "nf-md-image_sync",         0xF1A00),
    ("NERD_GLYPH_TERM2",   "Terminal (alt)",  "nf-cod-terminal",          0xEA85),
    # basis-set (al langer in gebruik)
    ("NERD_GLYPH_FOLDER",  "Map",             "nf-fa-folder",             0xF07C),
    ("NERD_GLYPH_CALENDAR","Datum",           "nf-fa-calendar",           0xF073),
    ("NERD_GLYPH_EURO",    "Euro",            "nf-fa-euro",               0xF155),
    ("NERD_GLYPH_MONEY",   "Geld",            "nf-fa-money",              0xF0D6),
    ("NERD_GLYPH_FILE",    "Bestand",         "nf-fa-file_o",             0xF016),
    ("NERD_GLYPH_BANK",    "Bank",            "nf-fa-credit_card",        0xF09C),
    ("NERD_GLYPH_TAG",     "Categorie",       "nf-fa-tag",                0xF02B),
    ("NERD_GLYPH_LOCATION","GPS / locatie",   "nf-fa-map_marker",         0xF041),
    ("NERD_GLYPH_LINK_IMG","Foto-koppeling",  "nf-fa-paperclip",          0xF0C6),
    ("NERD_GLYPH_CHECK",   "Geverifieerd",    "nf-fa-check",              0xF00C),
]


def esc(cp):
    return ("\\u%04x" % cp) if cp <= 0xFFFF else ("\\U%08x" % cp)


def main(out_path):
    nerd_file = DeCli.NERD_FONT_PATH
    if not os.path.exists(nerd_file):
        print("WAARSCHUWING: Nerd Font niet gevonden:", nerd_file)
    SERIF, SERIF_B, SERIF_I = "Times-Roman", "Times-Bold", "Times-Italic"
    INK = (0.12, 0.12, 0.12)
    MUT = (0.45, 0.45, 0.45)
    ACC = (0.10, 0.30, 0.55)

    # fitz.Font + TextWriter rendert Nerd-glyphs correct; insert_text(fontfile=)
    # geeft .notdef-blokjes voor deze PUA/MDI codepoints.
    nerd_font = fitz.Font(fontfile=nerd_file) if os.path.exists(nerd_file) else None

    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4
    M = 40
    tw = fitz.TextWriter(page.rect) if nerd_font else None

    # kop
    page.insert_text((M, 60), "DeCli", fontsize=24, fontname=SERIF_B, color=ACC)
    page.insert_text((M + 78, 60), "Nerd Font glyph-overzicht", fontsize=20,
                     fontname=SERIF, color=INK)
    page.insert_text((M, 80), "classic-stijl (Times-Roman) — glyphs: JetBrains Mono Nerd Font — issue #4",
                     fontsize=9, fontname=SERIF_I, color=MUT)
    page.draw_line((M, 90), (595 - M, 90), color=ACC, width=1.2)

    # kolomposities
    x_const, x_sym, x_class, x_code, x_esc = M, 196, 226, 392, 470
    # kolomkoppen
    yh = 108
    for x, h in ((x_const, "Constante"), (x_sym, "Sym"), (x_class, "Class"),
                 (x_code, "Codepoint"), (x_esc, "Python-escape")):
        page.insert_text((x, yh), h, fontsize=8, fontname=SERIF_B, color=MUT)
    page.draw_line((M, yh + 5), (595 - M, yh + 5), color=MUT, width=0.6)

    y = yh + 25
    rh = 27.2
    for i, (name, label, cls, cp) in enumerate(ROWS):
        glyph = getattr(DeCli, name, "")
        if i % 2 == 1:  # zebra
            page.draw_rect(fitz.Rect(M - 4, y - 13, 595 - M + 4, y + rh - 14),
                           color=None, fill=(0.96, 0.96, 0.97))
        page.insert_text((x_const, y), name, fontsize=8.5, fontname=SERIF, color=INK)
        page.insert_text((x_const, y + 10), label, fontsize=7, fontname=SERIF_I, color=MUT)
        # glyph in nerd font (via TextWriter — insert_text geeft .notdef)
        if glyph and tw is not None and nerd_font.has_glyph(ord(glyph)):
            tw.append((x_sym, y + 4), glyph, font=nerd_font, fontsize=15)
        else:
            page.insert_text((x_sym, y), "?", fontsize=12, fontname=SERIF, color=(0.8, 0, 0))
        page.insert_text((x_class, y), cls, fontsize=8.5, fontname=SERIF, color=INK)
        page.insert_text((x_code, y), "U+%X" % cp, fontsize=8.5, fontname=SERIF, color=INK)
        page.insert_text((x_esc, y), '"%s"' % esc(cp), fontsize=8.5, fontname=SERIF, color=(0.0, 0.35, 0.2))
        y += rh

    if tw is not None:
        tw.write_text(page, color=ACC)

    page.draw_line((M, y - 12), (595 - M, y - 12), color=MUT, width=0.6)
    page.insert_text((M, y + 4), "%d glyphs — gegenereerd door test/nerdfont_testpdf.py" % len(ROWS),
                     fontsize=7.5, fontname=SERIF_I, color=MUT)

    doc.save(out_path)
    doc.close()
    print("PDF geschreven:", out_path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "nerdfont_test_classic.pdf")
    main(out)
