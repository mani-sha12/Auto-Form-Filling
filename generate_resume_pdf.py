"""Generate PDF Resume"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create PDF
pdf_file = "sample-resume.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold',
    borderColor=colors.HexColor('#1f4788'),
    borderWidth=1,
    borderPadding=4,
    borderBottomWidth=2
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=4,
    alignment=TA_JUSTIFY
)

# Title
story.append(Paragraph("JOHN DOE", title_style))
story.append(Spacer(1, 0.1*inch))

# Contact info
contact_text = "📧 john.doe@example.com | 📱 +1 (555) 123-4567 | 📍 New York, NY 10001 | 🌍 American"
story.append(Paragraph(contact_text, ParagraphStyle('contact', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER)))
story.append(Spacer(1, 0.15*inch))

# Professional Summary
story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
summary = """Experienced Software Engineer with 8 years of professional experience in developing scalable web applications, 
cloud infrastructure, and data processing solutions. Proven track record of delivering high-impact projects for Fortune 500 companies."""
story.append(Paragraph(summary, normal_style))
story.append(Spacer(1, 0.1*inch))

# Professional Experience
story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))

exp_data = [
    ("Senior Software Engineer | TechCorp Inc., New York, NY", "2019 - Present (5 years)"),
    ("Led development of microservices architecture handling 1 million+ daily transactions. Designed real-time data pipeline using Apache Kafka and Spark. Mentored 5 junior developers. Optimized database queries by 40%. Tech: Python, JavaScript, React, Node.js, Docker, Kubernetes, AWS", ""),
    ("Software Engineer | DataFlow Systems, New York, NY", "2017 - 2019 (2 years)"),
    ("Developed full-stack web applications using Python/Django and React. Implemented RESTful APIs and GraphQL endpoints. Contributed to open-source with 500+ stars. Tech: Python, Django, React, PostgreSQL, Redis, Docker", ""),
    ("Junior Developer | StartupXYZ, New York, NY", "2015 - 2017 (2 years)"),
    ("Built responsive web interfaces using HTML, CSS, and JavaScript. Maintained legacy PHP code. Developed automated testing suite reducing bugs by 60%.", ""),
]

for item in exp_data:
    title = item[0]
    dates = item[1]
    if dates and "Present" in dates:
        story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('exp', parent=styles['Normal'], fontSize=10, spaceAfter=2)))
        story.append(Paragraph(dates, ParagraphStyle('dates', parent=styles['Normal'], fontSize=9, textColor=colors.grey, spaceAfter=4)))
    elif dates:
        story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('exp', parent=styles['Normal'], fontSize=10, spaceAfter=2)))
        story.append(Paragraph(dates, ParagraphStyle('dates', parent=styles['Normal'], fontSize=9, textColor=colors.grey, spaceAfter=4)))
    else:
        story.append(Paragraph(title, normal_style))

story.append(Spacer(1, 0.1*inch))

# Education
story.append(Paragraph("EDUCATION", heading_style))
story.append(Paragraph("<b>Bachelor of Science in Computer Science</b><br/>New York University, New York, NY | Graduated: 2015 | GPA: 3.8/4.0", normal_style))
story.append(Spacer(1, 0.1*inch))

# Skills
story.append(Paragraph("TECHNICAL SKILLS", heading_style))
skills_text = """<b>Programming Languages:</b> Python, JavaScript, Java, SQL, Go, TypeScript<br/>
<b>Web Development:</b> React, Node.js, Django, FastAPI, Express.js, HTML5, CSS3<br/>
<b>Databases:</b> PostgreSQL, MongoDB, Redis, Elasticsearch, MySQL<br/>
<b>Cloud Platforms:</b> AWS, Google Cloud Platform, Azure<br/>
<b>DevOps & Tools:</b> Docker, Kubernetes, Git, Jenkins, GitHub Actions, Terraform<br/>
<b>Other Skills:</b> REST APIs, GraphQL, Microservices, System Design, Agile/Scrum"""
story.append(Paragraph(skills_text, ParagraphStyle('skills', parent=styles['Normal'], fontSize=9, spaceAfter=8)))
story.append(Spacer(1, 0.1*inch))

# Certifications
story.append(Paragraph("CERTIFICATIONS", heading_style))
certs = """AWS Certified Solutions Architect - Professional (2022)<br/>
Google Cloud Professional Cloud Architect (2021)<br/>
Kubernetes Application Developer (CKAD) (2021)<br/>
"Developer of the Year" Award - TechCorp Inc. (2023)"""
story.append(Paragraph(certs, normal_style))
story.append(Spacer(1, 0.1*inch))

# Why Interested
story.append(Paragraph("ABOUT THIS POSITION", heading_style))
about = """I'm excited about this opportunity because it aligns with my career goals and skills. With 8 years of experience 
in software development and proven track record of delivering high-impact projects, I'm confident I can make significant 
contributions to your team. I'm particularly interested in challenging problems and growing both technically and professionally."""
story.append(Paragraph(about, normal_style))
story.append(Spacer(1, 0.1*inch))

# Additional Info
story.append(Paragraph("ADDITIONAL INFORMATION", heading_style))
additional = """<b>Employment Type:</b> Full-time<br/>
<b>Expected Salary:</b> $120,000 - $150,000 annually<br/>
<b>Earliest Start Date:</b> July 1, 2024<br/>
<b>Date of Birth:</b> January 15, 1990<br/>
<b>Address:</b> 123 Main Street, New York, NY 10001, United States"""
story.append(Paragraph(additional, ParagraphStyle('additional', parent=styles['Normal'], fontSize=9, spaceAfter=8)))

# Build PDF
doc.build(story)
print(f"✅ PDF Created Successfully: {pdf_file}")
print(f"📁 Location: c:\\Users\\Manisha\\OneDrive\\Documents\\Desktop\\New folder (3)\\sample-resume.pdf")
