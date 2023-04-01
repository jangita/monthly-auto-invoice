import os
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import schedule
import time

def create_invoice():
    # Setting the current date, month, and year
    now = datetime.now()
    current_month = now.strftime('%B')
    current_year = now.year

    # PDF file name and path
    file_name = f"Invoice_{current_month}_{current_year}.pdf"
    pdf_path = Path.cwd() / file_name

    # Create PDF
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    elements = []

    # Add logo
    logo_path = "path/to/your/logo.png"
    logo = Image(logo_path, width=2 * inch, height=inch)
    elements.append(logo)

    # Add invoice number
    invoice_number = f"Invoice Number: {now.strftime('%Y%m')}-001"
    invoice_number_paragraph = Paragraph(invoice_number, styles["Heading2"])
    elements.append(invoice_number_paragraph)
    elements.append(Paragraph("<br/>", styles["Normal"]))  # Add some space

    # Add invoice header
    invoice_header = f"Invoice - {current_month} {current_year}"
    header = Paragraph(invoice_header, styles["Heading1"])
    elements.append(header)

    # Add biller and customer details
    biller = "Biller Name\nBiller Address\nBiller City, State, ZIP\nBiller Phone\nBiller Email"
    customer = "Customer Name\nCustomer Address\nCustomer City, State, ZIP\nCustomer Phone\nCustomer Email"

    data = [
        ["Biller:", biller, "Customer:", customer]
    ]
    biller_customer_table = Table(data, colWidths=[inch, 3 * inch, inch, 3 * inch])
    elements.append(biller_customer_table)
    elements.append(Paragraph("<br/>", styles["Normal"]))  # Add some space

    # Create invoice table with data
    data = [
        ['Item', 'Quantity', 'Price', 'Total'],
        ['Item 1', 1, 50, 50],
        ['Item 2', 3, 30, 90],
        ['Item 3', 2, 20, 40],
    ]
    table = Table(data)

    # Add table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]
      
      ()))

  elements.append(table)
  elements.append(Paragraph("<br/>", styles["Normal"]))  # Add some space

  # Add terms, notes, and payment details
  terms = "Payment Terms: Due upon receipt"
  notes = "Notes: Thank you for your business!"
  payment_details = "Payment Details: Please make payment via Bank Transfer to Account Number 12345678, Sort Code 01-23-45, Bank Name."

  terms_paragraph = Paragraph(terms, styles["Normal"])
  notes_paragraph = Paragraph(notes, styles["Normal"])
  payment_details_paragraph = Paragraph(payment_details, styles["Normal"])

  # Add a spacer for pushing notes and payment details to the bottom
  spacer = Paragraph("<br/>" * 5, styles["Normal"])  # Adjust the number of lines as needed
  elements.append(spacer)

  # Add notes and payment details
  elements.append(notes_paragraph)
  elements.append(Paragraph("<br/>", styles["Normal"]))  # Add some space
  elements.append(payment_details_paragraph)

  # Generate the PDF
  doc.build(elements)

  return file_name

def send_email(file_name):
  email = os.environ.get("YOUR_EMAIL")
  password = os.environ.get("YOUR_PASSWORD")
  recipient = "recipient@example.com"

  msg = EmailMessage()
  msg["Subject"] = f"Monthly Invoice - {file_name}"
  msg["From"] = email
  msg["To"] = recipient
  msg.set_content("Please find the attached invoice for this month.")

  with open(file_name, "rb") as pdf_file:
      pdf_data = MIMEApplication(pdf_file.read(), _subtype="pdf")
      pdf_data.add_header("Content-Disposition", "attachment", filename=file_name)
      msg.attach(pdf_data)

  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(email, password)
      server.send_message(msg)

  print(f"Invoice {file_name} sent to {recipient}")

  def run_monthly_task():
    file_name = create_invoice()
    send_email(file_name)

def main():
# Schedule the script to run on the 1st of every month
  schedule.every().month.at("00:00").do(run_monthly_task)

  while True:
      schedule.run_pending()
      time.sleep(60)  # Wait for 60 seconds before checking again

if name == "main":
  main()
