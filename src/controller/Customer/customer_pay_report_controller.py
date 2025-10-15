import os
import sys
import subprocess
import time
import traceback
from tkinter import messagebox
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph

import arabic_reshaper
from bidi.algorithm import get_display

class CustomerPayReportController:
    def __init__(self, pay_data):
        self.pay_data = pay_data
        self.arabic_font_name = 'Arial'
        self.bold_arabic_font_name = "Arial-Bold"
        self.pagesize = letter
        self._register_fonts()
    
    def _register_fonts(self):
        try:
            regular_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arial.ttf")
            pdfmetrics.registerFont(TTFont(self.arabic_font_name, regular_path))
            bold_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arialbd.ttf")
            pdfmetrics.registerFont(TTFont(self.bold_arabic_font_name, bold_path))
        except Exception:
            self.arabic_font_name = 'Helvetica'; self.bold_arabic_font_name = 'Helvetica-Bold'
            
    def _reshape(self, text):
        return get_display(arabic_reshaper.reshape(str(text)))

    def generate_pdf(self):
        elements = []
        
        # 1. Logo
        logo_path = self.pay_data.get('logo_path', "Z_Files/images/Golden_Rose.png")
        if os.path.exists(logo_path):
            elements.append(Image(logo_path, width=4*cm, height=4*cm, hAlign='CENTER'))
            elements.append(Spacer(1, 0.5*cm))

        # 2. Header Table (Three-column layout using Paragraphs inside cells for alignment)
        style_right = ParagraphStyle(name='Right', fontName=self.bold_arabic_font_name, fontSize=11, alignment=TA_RIGHT, leading=14)
        style_center = ParagraphStyle(name='Center', fontName=self.arabic_font_name, fontSize=11, alignment=TA_CENTER, leading=14)
        style_left = ParagraphStyle(name='Left', fontName=self.bold_arabic_font_name, fontSize=11, alignment=TA_LEFT, leading=14)

        right_col_text = f"{self._reshape('عميل: ' + self.pay_data['customer_name'])}<br/>{self._reshape('العملية رقم: ' + str(self.pay_data['pay_id']))}"
        center_col_text = f"<b>{self._reshape('موزع ' + self.pay_data['distributor_name'])}</b><br/>{self._reshape('تاريخ العملية: ' + self.pay_data['date'])}"
        left_col_text = f"{self._reshape('دفعة رقم: ' + str(self.pay_data['pay_id']))}<br/>{self._reshape('القاهرة')}"

        header_data = [[
            Paragraph(right_col_text, style_right),
            Paragraph(center_col_text, style_center),
            Paragraph(left_col_text, style_left)
        ]]
        header_table = Table(header_data, colWidths=[6.5*cm, 6*cm, 6*cm])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.5*cm))

        # 3. Payment Details Table
        payment_header = [self._reshape(h) for h in ["المبلغ المدفوع", "التاريخ", "اسم المكتب", "م"]]
        payment_row = [
            f"{self.pay_data['amount_paid']:,.2f} {self._reshape('ج.م')}",
            self.pay_data['date'],
            self._reshape(self.pay_data['customer_name']),
            "1"
        ]
        payment_table_data = [payment_header, payment_row]
        
        payment_table = Table(payment_table_data, colWidths=[4.5*cm, 4.5*cm, 8*cm, 1.5*cm])
        payment_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), ('FONTSIZE', (0,0), (-1,-1), 11),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey), ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D9E1F2")),
            ('FONTNAME', (0,0), (-1,0), self.bold_arabic_font_name),
        ]))
        elements.append(payment_table)
        elements.append(Spacer(1, 1*cm))

        # 4. Summary Details (using Paragraphs for centered text as in the image)
        summary_style = ParagraphStyle(name='Summary', fontName=self.bold_arabic_font_name, fontSize=12, alignment=TA_CENTER, leading=18)
        
        summary_lines = [
            f"{self._reshape('الحساب قبل الدفع:')} {self.pay_data['balance_before']:,.2f} {self._reshape('ج.م')}",
            f"{self._reshape('المبلغ المدفوع:')} {self.pay_data['amount_paid']:,.2f} {self._reshape('ج.م')}",
            f"{self._reshape('الحساب المتبقي عليكم:')} {self.pay_data['balance_after']:,.2f} {self._reshape('ج.م')}",
        ]
        
        for line in summary_lines:
            elements.append(Paragraph(line, summary_style))

        self._create_and_open_pdf(elements)

    def _create_and_open_pdf(self, elements):
        os.makedirs("Z_Files/reports/customer_payments", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_customer_name = "".join(c for c in self.pay_data['customer_name'] if c.isalnum())
        file_path = os.path.join("Z_Files/reports/customer_payments", f"Payment_{self.pay_data['pay_id']}_{safe_customer_name}_{timestamp}.pdf")
        
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter, topMargin=1*cm, bottomMargin=1*cm, leftMargin=1*cm, rightMargin=1*cm)
            doc.build(elements)
            self._open_pdf(file_path)
        except Exception as e:
            messagebox.showerror("خطأ في إنشاء PDF", f"فشل إنشاء ملف PDF: {e}")
            traceback.print_exc()

    def _open_pdf(self, filename):
        time.sleep(0.5)
        try:
            if sys.platform == "win32": os.startfile(filename)
            elif sys.platform == "darwin": subprocess.run(['open', filename], check=True)
            else: subprocess.run(['xdg-open', filename], check=True)
        except Exception as e:
            messagebox.showerror("خطأ في فتح الملف", f"لا يمكن فتح ملف PDF:\n{e}")