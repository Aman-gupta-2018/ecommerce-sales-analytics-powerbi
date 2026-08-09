"""
Generate PDF Executive Analytics Report for Portfolio
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "outputs", "reports", "Executive_Analytics_Report.pdf")
os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)

doc = SimpleDocTemplate(PDF_PATH, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22, textColor=colors.HexColor('#1E293B'), alignment=0, spaceAfter=8)
subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor=colors.HexColor('#64748B'), spaceAfter=15)
h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#2563EB'), spaceBefore=12, spaceAfter=8)
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#334155'), spaceAfter=8)
bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')

story = []

# Title & Header
story.append(Paragraph("E-Commerce Sales & Profitability Executive Report", title_style))
story.append(Paragraph("Data Analysis Period: 2014 – 2017 | Superstore Dataset (US Regional Retail)", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

# Executive Summary
story.append(Paragraph("Executive Summary", h1_style))
story.append(Paragraph(
    "This report summarizes key business findings from analyzing 9,994 transaction records spanning 2014 through 2017. "
    "While cumulative revenue reached <b>$2.30M</b> with <b>$286.4K</b> in profit (12.5% overall margin), deep-dive analysis reveals "
    "critical margin erosion caused by unmonitored discount policies, regional underperformance, and high-volume loss-making SKUs.",
    body_style
))

# Key Metrics Table
story.append(Paragraph("Yearly Financial Summary", h1_style))
table_data = [
    ["Year", "Revenue", "YoY Growth", "Total Profit", "Profit Margin", "Total Orders"],
    ["2014", "$484,247", "-", "$49,544", "10.2%", "969"],
    ["2015", "$470,533", "-2.8%", "$61,619", "13.1%", "1,038"],
    ["2016", "$609,206", "+29.5%", "$81,795", "13.4%", "1,315"],
    ["2017", "$733,215", "+20.4%", "$93,439", "12.7%", "1,687"],
    ["Total", "$2,297,201", "-", "$286,397", "12.5%", "5,009"]
]
t = Table(table_data, colWidths=[60, 90, 80, 90, 90, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 10),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
]))
story.append(t)
story.append(Spacer(1, 15))

# Strategic Insights & Recommendations
story.append(Paragraph("Key Findings & Strategic Recommendations", h1_style))

insights = [
    "<b>1. Uncontrolled Discounts Destroy Profitability:</b> Orders with 0% discount yield an average profit margin of <b>34.0%</b>, whereas orders with discounts average a negative margin of <b>-8.3%</b>. Discounts greater than 20% consistently lead to financial losses. <i>Recommendation: Cap maximum promotional discounts at 20% to recover an estimated $138,515 in profit.</i>",
    "<b>2. Product Portfolio Rationalization:</b> Technology products generate the highest profitability ($145.5K profit, 15.6% margin). Conversely, Sub-Categories such as Tables, Bookcases, and Supplies operate at net losses totaling <b>-$22,387</b>. <i>Recommendation: Re-negotiate vendor terms or raise prices for negative-margin SKUs.</i>",
    "<b>3. Regional Performance Disparities:</b> The West region delivers the highest profit ($108.4K, 21.9% margin), whereas 10 states operate at a net loss (led by Texas at -$25.7K and Ohio at -$17.0K). <i>Recommendation: Re-evaluate shipping rates and promotional incentives in Central and Southern loss-making states.</i>",
    "<b>4. RFM Customer Value Concentration:</b> Customer segmentation identifies 124 'Champion' accounts driving high lifetime value, alongside 261 'At Risk' or 'Lost' accounts. <i>Recommendation: Establish automated retention triggers for accounts with declining order frequency.</i>"
]

for ins in insights:
    story.append(Paragraph(ins, body_style))
    story.append(Spacer(1, 4))

# Visual chart inclusion
chart_img = os.path.join(BASE_DIR, "outputs", "charts", "05_discount_impact.png")
if os.path.exists(chart_img):
    story.append(Spacer(1, 10))
    story.append(Paragraph("Discount Impact Visualization", h1_style))
    story.append(Image(chart_img, width=500, height=230))

doc.build(story)
print(f"Executive Report PDF generated successfully at: {PDF_PATH}")
