"""
Create a test PDF document for testing purposes.
"""
import os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Get the directory of this script
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "documents"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create a PDF document
pdf_path = OUTPUT_DIR / 'test_document.pdf'

# Create the PDF document
doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
styles = getSampleStyleSheet()

# Create content
story = []

# Add title
story.append(Paragraph("TEST INVOICE", styles['Title']))
story.append(Spacer(1, 12))

# Add company information
story.append(Paragraph("ABC Consulting Services", styles['Heading2']))
story.append(Paragraph("123 Business Avenue", styles['Normal']))
story.append(Paragraph("New York, NY 10001", styles['Normal']))
story.append(Paragraph("Phone: (555) 123-4567", styles['Normal']))
story.append(Paragraph("Email: billing@abcconsulting.example", styles['Normal']))
story.append(Spacer(1, 12))

# Add client information
story.append(Paragraph("BILL TO:", styles['Heading3']))
story.append(Paragraph("DEF Corporation", styles['Normal']))
story.append(Paragraph("456 Corporate Plaza", styles['Normal']))
story.append(Paragraph("Chicago, IL 60601", styles['Normal']))
story.append(Paragraph("Contact: Robert Brown", styles['Normal']))
story.append(Spacer(1, 12))

# Add invoice details
story.append(Paragraph("Invoice #: INV-2023-1045", styles['Heading3']))
story.append(Paragraph("Date: October 15, 2023", styles['Normal']))
story.append(Paragraph("Due Date: November 15, 2023", styles['Normal']))
story.append(Spacer(1, 12))

# Add service details
story.append(Paragraph("SERVICES:", styles['Heading3']))
story.append(Paragraph("1. Business Strategy Consulting - $5,000", styles['Normal']))
story.append(Paragraph("2. Market Research Analysis - $3,500", styles['Normal']))
story.append(Paragraph("3. Financial Projections Development - $2,800", styles['Normal']))
story.append(Paragraph("4. Presentation Development - $1,500", styles['Normal']))
story.append(Spacer(1, 12))

# Add totals
story.append(Paragraph("Subtotal: $12,800", styles['Normal']))
story.append(Paragraph("Tax (8%): $1,024", styles['Normal']))
story.append(Paragraph("Total Due: $13,824", styles['Heading3']))
story.append(Spacer(1, 12))

# Add payment information
story.append(Paragraph("PAYMENT INFORMATION:", styles['Heading3']))
story.append(Paragraph("Please make checks payable to 'ABC Consulting Services'", styles['Normal']))
story.append(Paragraph("For wire transfers, please contact our accounting department.", styles['Normal']))
story.append(Paragraph("Payment Terms: Net 30", styles['Normal']))
story.append(Spacer(1, 12))

# Add notes
story.append(Paragraph("NOTES:", styles['Heading3']))
story.append(Paragraph("Thank you for your business! Please contact us with any questions regarding this invoice.", styles['Normal']))
story.append(Paragraph("Late payments are subject to a 1.5% monthly fee.", styles['Normal']))

# Build the PDF
doc.build(story)

print(f"Test PDF document created at: {pdf_path}") 