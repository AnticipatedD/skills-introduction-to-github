import os
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Polygon

# -------------------------------------------------
# Output
# -------------------------------------------------
os.makedirs("generated", exist_ok=True)
pdf_path = "generated/Microsoft_Learn_Badge_Profile_v4.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=(380, 260),
    rightMargin=10,
    leftMargin=10,
    topMargin=10,
    bottomMargin=10
)

# -------------------------------------------------
# Microsoft Brand Colors
# -------------------------------------------------
PRIMARY     = colors.HexColor("#0078D4")   # Microsoft Blue
DARK_TEXT   = colors.HexColor("#242424")
MUTED_TEXT  = colors.HexColor("#605E5C")
LIGHT_BG    = colors.HexColor("#F3F2F1")
CARD_BG     = colors.white
BORDER      = colors.HexColor("#E1DFDD")
XP_GREEN    = colors.HexColor("#107C41")
XP_TRACK    = colors.HexColor("#E0E0E0")

# Microsoft logo colors
MS_RED    = colors.HexColor("#F25022")
MS_GREEN  = colors.HexColor("#7FBA00")
MS_BLUE   = colors.HexColor("#00A4EF")
MS_YELLOW = colors.HexColor("#FFB900")

styles = getSampleStyleSheet()

# -------------------------------------------------
# Typography
# -------------------------------------------------
name_style = ParagraphStyle(
    "Name", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=13,
    textColor=DARK_TEXT, leading=16
)

email_style = ParagraphStyle(
    "Email", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9,
    textColor=MUTED_TEXT, leading=12
)

val_style = ParagraphStyle(
    "Val", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=18,
    textColor=PRIMARY, alignment=1, leading=20
)

lbl_style = ParagraphStyle(
    "Lbl", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8,
    textColor=MUTED_TEXT, alignment=1, leading=10
)

xp_lbl_style = ParagraphStyle(
    "XPLbl", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=8,
    textColor=DARK_TEXT
)

xp_val_style = ParagraphStyle(
    "XPVal", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8,
    textColor=MUTED_TEXT, alignment=2
)

btn_style = ParagraphStyle(
    "Btn", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9,
    textColor=colors.white, alignment=1
)

story = []

# -------------------------------------------------
# 1. Profile Header (Logo + Name + Email)
# -------------------------------------------------
def make_ms_logo(size=28):
    d = Drawing(size, size)
    s = size / 2 - 1
    d.add(Rect(0, s + 1, s, s, fillColor=MS_RED, strokeColor=None))
    d.add(Rect(s + 1, s + 1, s, s, fillColor=MS_GREEN, strokeColor=None))
    d.add(Rect(0, 0, s, s, fillColor=MS_BLUE, strokeColor=None))
    d.add(Rect(s + 1, 0, s, s, fillColor=MS_YELLOW, strokeColor=None))
    return d

logo = make_ms_logo(28)

meta = Table([
    [Paragraph("MD ABUL HOSSAIN", name_style)],
    [Paragraph("mdabulhossain1008@gmail.com", email_style)]
], colWidths=[280])
meta.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
]))

header = Table([[logo, meta]], colWidths=[36, 300])
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
]))

header_wrapper = Table([[header]], colWidths=[360])
header_wrapper.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(header_wrapper)
story.append(Spacer(1, 12))

# -------------------------------------------------
# 2. Metrics Grid
# -------------------------------------------------
metrics_data = [
    [Paragraph("159", val_style), Paragraph("34", val_style), Paragraph("12", val_style)],
    [Paragraph("Badges", lbl_style), Paragraph("Trophies", lbl_style), Paragraph("Level", lbl_style)]
]
metrics = Table(metrics_data, colWidths=[110, 110, 110])
metrics.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
    ("TOPPADDING", (0, 1), (-1, 1), 1),
]))

metrics_box = Table([[metrics]], colWidths=[340])
metrics_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
    ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(metrics_box)
story.append(Spacer(1, 12))

# -------------------------------------------------
# 3. XP Progress Section
# -------------------------------------------------
xp_labels = Table([
    [Paragraph("LEVEL 12", xp_lbl_style),
     Paragraph("234,750 / 331,999 XP", xp_val_style)]
], colWidths=[170, 170])
xp_labels.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(xp_labels)

# Progress bar
bar_width = 340
ratio = 234750 / 331999
fill_w = bar_width * ratio

xp_bar = Drawing(bar_width, 14)
# Track
xp_bar.add(Rect(0, 3, bar_width, 8, fillColor=XP_TRACK, strokeColor=None, rx=4, ry=4))
# Fill
xp_bar.add(Rect(0, 3, fill_w, 8, fillColor=PRIMARY, strokeColor=None, rx=4, ry=4))
# Green diamond indicator
xp_bar.add(Polygon(
    [fill_w - 5, 7, fill_w, 12, fill_w + 5, 7, fill_w, 2],
    fillColor=XP_GREEN,
    strokeColor=None
))
story.append(xp_bar)
story.append(Spacer(1, 16))

# -------------------------------------------------
# 4. CTA Button
# -------------------------------------------------
btn_text = '<link href="https://learn.microsoft.com"><font color="white">View Public Profile</font></link>'
btn = Table([[Paragraph(btn_text, btn_style)]], colWidths=[160])
btn.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))

btn_wrap = Table([[btn]], colWidths=[340])
btn_wrap.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
]))
story.append(btn_wrap)

# -------------------------------------------------
# Build
# -------------------------------------------------
doc.build(story)
print(f"✓ Professional Microsoft Learn profile card saved to:\n  {pdf_path}")
