# app/utils/pdf.py
from fpdf import FPDF

def generate_order_pdf(order_data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Наряд DentShare", ln=1, align="C")
    for key, value in order_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=1)
    pdf.output(filename)
    return filename
