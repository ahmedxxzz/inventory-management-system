import os
import sys
import subprocess
import time
import traceback
from tkinter import messagebox
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle

import arabic_reshaper
from bidi.algorithm import get_display

class SalesReportController:
    """
    Generates a PDF sales bill for a customer.
    This class is now simplified to accept a single dictionary of bill data.
    """
    def __init__(self, bill_data):
        self.bill_data = bill_data
        self.arabic_font_name = 'Arial'
        self.bold_arabic_font_name = "Arial-Bold" # Using a more standard name
        self.pagesize = letter
        self._register_fonts()
    
    def _register_fonts(self):
        """Registers system Arial fonts for ReportLab."""
        try:
            # Register Regular Arial
            regular_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arial.ttf")
            pdfmetrics.registerFont(TTFont(self.arabic_font_name, regular_path))
            
            # Register Bold Arial
            bold_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arialbd.ttf")
            pdfmetrics.registerFont(TTFont(self.bold_arabic_font_name, bold_path))
            print("Successfully registered Arial regular and bold fonts.")
        except Exception as e:
            print(f"Warning: Could not register system Arial fonts. Fallback to Helvetica. Error: {e}")
            self.arabic_font_name = 'Helvetica'
            self.bold_arabic_font_name = 'Helvetica-Bold'
            
    def _reshape(self, text):
        """Helper method to reshape and apply bidi algorithm for display."""
        return get_display(arabic_reshaper.reshape(str(text)))

    def generate_pdf(self):
        """The main method to build and open the PDF report."""
        elements = []
        
        # 1. Add Logo
        logo_path = self.bill_data.get('logo_path', "Z_Files/images/Golden_Rose.png")
        if os.path.exists(logo_path):
            img = Image(logo_path, width=3*cm, height=3*cm, hAlign='CENTER')
            elements.append(img)
            elements.append(Spacer(1, 0.2*cm))

        # 2. Add Header Table
        header_data = [
            [
                self._reshape(f"موزع: {self.bill_data['distributor_name']}"),
                self._reshape("فاتورة مبيعات"),
                self._reshape(f"عميل: {self.bill_data['customer_name']}"),
            ],
            [
                self._reshape("القاهرة"),
                self._reshape(f"تاريخ: {self.bill_data['date']}"),
                self._reshape(f"فاتورة رقم: {self.bill_data['sales_bill_id']}"),
            ]
        ]
        header_table = Table(header_data, colWidths=[2.5*cm, 12*cm, 4*cm], rowHeights=25)
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('ALIGN', (1,0), (1,-1), 'CENTER'),
            ('ALIGN', (2,0), (2,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.5*cm))

        # 3. Add Items Table
        items_header = [self._reshape(h) for h in ["الإجمالي", "الخصم", "السعر", "الكمية", "الصنف", "م"]]
        table_data = [items_header]
        
        total_quantity = 0
        grand_total = 0

        for i, item in enumerate(self.bill_data['items'], 1):
            item_total = (item['price'] - item['discount']) * item['quantity']
            total_quantity += item['quantity']
            grand_total += item_total
            
            row = [
                f"{item_total:,.2f}",
                f"{item['discount']:,.2f}",
                f"{item['price']:,.2f}",
                str(item['quantity']),
                self._reshape(item['product_name']),
                str(i)
            ]
            table_data.append(row)
            
        # Add summary row to the table
        summary_row = [f"{grand_total:,.2f}", "", "", str(total_quantity), self._reshape("الإجمالي النهائي"), ""]
        table_data.append(summary_row)
        
        items_table = Table(table_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2*cm, 7*cm, 1.5*cm])
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-2), 0.25, colors.grey),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            # Header Style
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), self.bold_arabic_font_name),
            # Summary Row Style
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
            ('FONTNAME', (0,-1), (-1,-1), self.bold_arabic_font_name),
            ('SPAN', (1, -1), (3, -1)), # Span cells in summary row
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 1*cm))

        # 4. Add Footer with account details
        status = "آجل" if self.bill_data['is_paid'] == 0 else "نقدي (مدفوعة)"
        footer_text = f"""
        <b>حالة الفاتورة:</b> {self._reshape(status)}<br/>
        <b>الحساب قبل الفاتورة:</b> {self.bill_data['balance_before']:,.2f} {self._reshape("ج.م")}<br/>
        <b>الحساب بعد الفاتورة:</b> {self.bill_data['balance_after']:,.2f} {self._reshape("ج.م")}
        """
        style = ParagraphStyle(name='Footer', fontName=self.arabic_font_name, fontSize=12, alignment=TA_CENTER, leading=18)
        elements.append(Paragraph(self._reshape(footer_text), style))

        # 5. Build the PDF
        self._create_and_open_pdf(elements)

    def _create_and_open_pdf(self, elements):
        """Builds, saves, and opens the PDF document."""
        os.makedirs("Z_Files/reports/customer_sales", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_customer_name = "".join(c for c in self.bill_data['customer_name'] if c.isalnum())
        file_path = os.path.join("Z_Files/reports/customer_sales", f"Sale_{self.bill_data['sales_bill_id']}_{safe_customer_name}_{timestamp}.pdf")
        
        try:
            doc = SimpleDocTemplate(file_path, pagesize=self.pagesize, topMargin=1*cm, bottomMargin=1*cm, leftMargin=1*cm, rightMargin=1*cm)
            doc.build(elements)
            print(f"PDF generated successfully at: {file_path}")
            self._open_pdf(file_path)
        except Exception as e:
            messagebox.showerror("خطأ في إنشاء PDF", f"فشل إنشاء ملف PDF: {e}")
            traceback.print_exc()

    def _open_pdf(self, filename):
        """Opens the specified file using the default system application."""
        time.sleep(0.5) # Give a moment for the file to be written
        try:
            if sys.platform == "win32":
                os.startfile(filename)
            elif sys.platform == "darwin":
                subprocess.run(['open', filename], check=True)
            else:
                subprocess.run(['xdg-open', filename], check=True)
        except Exception as e:
            messagebox.showerror("خطأ في فتح الملف", f"لا يمكن فتح ملف PDF:\n{e}")