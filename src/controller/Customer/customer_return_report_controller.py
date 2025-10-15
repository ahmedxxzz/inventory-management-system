import os
import sys
import subprocess
import time
import traceback
from tkinter import messagebox
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph

import arabic_reshaper
from bidi.algorithm import get_display

class CustomerReturnReportController:
    """
    Generates a PDF return receipt for a customer.
    Accepts a single dictionary of return data.
    """
    def __init__(self, return_data):
        self.return_data = return_data
        self.arabic_font_name = 'Arial'
        self.bold_arabic_font_name = "Arial-Bold"
        self.pagesize = letter
        self._register_fonts()
    
    def _register_fonts(self):
        """Registers system Arial fonts for ReportLab."""
        try:
            regular_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arial.ttf")
            pdfmetrics.registerFont(TTFont(self.arabic_font_name, regular_path))
            bold_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arialbd.ttf")
            pdfmetrics.registerFont(TTFont(self.bold_arabic_font_name, bold_path))
            print("Successfully registered Arial fonts for return report.")
        except Exception as e:
            print(f"Warning: Could not register system Arial fonts. Fallback to Helvetica. Error: {e}")
            self.arabic_font_name = 'Helvetica'
            self.bold_arabic_font_name = 'Helvetica-Bold'
            
    def _reshape(self, text):
        """Helper method to reshape and apply bidi algorithm."""
        return get_display(arabic_reshaper.reshape(str(text)))

    def generate_pdf(self):
        """The main method to build and open the PDF report."""
        elements = []
        
        logo_path = self.return_data.get('logo_path', "Z_Files/images/Golden_Rose.png")
        if os.path.exists(logo_path):
            elements.append(Image(logo_path, width=3*cm, height=3*cm, hAlign='CENTER'))
            elements.append(Spacer(1, 0.2*cm))

        header_data = [
            [
                self._reshape(f"موزع: {self.return_data['distributor_name']}"),
                self._reshape("إيصال مرتجع"), # <-- CHANGED
                self._reshape(f"عميل: {self.return_data['customer_name']}"),
            ],
            [
                self._reshape("القاهرة"),
                self._reshape(f"تاريخ: {self.return_data['date']}"),
                self._reshape(f"مرتجع رقم: {self.return_data['return_id']}"), # <-- CHANGED
            ]
        ]
        header_table = Table(header_data, colWidths=[4*cm, 10*cm, 4.5*cm], rowHeights=25)
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (0,-1), 'LEFT'), ('ALIGN', (1,0), (1,-1), 'CENTER'), ('ALIGN', (2,0), (2,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.5*cm))

        # <-- MODIFIED: Columns redefined for return (no discount)
        items_header = [self._reshape(h) for h in ["الإجمالي", "السعر", "الكمية", "الصنف", "م"]]
        table_data = [items_header]
        
        total_quantity = 0
        grand_total = 0

        for i, item in enumerate(self.return_data['items'], 1):
            item_total = item['price_at_return'] * item['quantity']
            total_quantity += item['quantity']
            grand_total += item_total
            
            row = [
                f"{item_total:,.2f}",
                f"{item['price_at_return']:,.2f}", # <-- CHANGED
                str(item['quantity']),
                self._reshape(item['product_name']),
                str(i)
            ]
            table_data.append(row)
            
        summary_row = [f"{grand_total:,.2f}", "", str(total_quantity), self._reshape("الإجمالي النهائي"), ""]
        table_data.append(summary_row)
        
        # <-- MODIFIED: Column widths adjusted
        items_table = Table(table_data, colWidths=[3*cm, 3*cm, 2*cm, 9*cm, 1.5*cm])
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-2), 0.25, colors.grey), ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4F81BD")), ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), self.bold_arabic_font_name),
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey), ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
            ('FONTNAME', (0,-1), (-1,-1), self.bold_arabic_font_name),
            ('SPAN', (1, -1), (2, -1)),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 1*cm))

        # <-- MODIFIED: Footer text updated for returns
        footer_text = f"""
        <b>الحساب قبل المرتجع:</b> {self.return_data['balance_before']:,.2f} {self._reshape("ج.م")}<br/>
        <b>قيمة المرتجع :</b> {grand_total:,.2f} {self._reshape("ج.م")}<br/>
        <b>الحساب بعد المرتجع:</b> {self.return_data['balance_after']:,.2f} {self._reshape("ج.م")}
        """
        style = ParagraphStyle(name='Footer', fontName=self.arabic_font_name, fontSize=12, alignment=TA_CENTER, leading=18)
        elements.append(Paragraph(self._reshape(footer_text), style))

        self._create_and_open_pdf(elements)

    def _create_and_open_pdf(self, elements):
        """Builds, saves, and opens the PDF document."""
        # <-- MODIFIED: Save path and filename
        os.makedirs("Z_Files/reports/customer_returns", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_customer_name = "".join(c for c in self.return_data['customer_name'] if c.isalnum())
        file_path = os.path.join("Z_Files/reports/customer_returns", f"Return_{self.return_data['return_id']}_{safe_customer_name}_{timestamp}.pdf")
        
        try:
            doc = SimpleDocTemplate(file_path, pagesize=self.pagesize, topMargin=1*cm, bottomMargin=1*cm, leftMargin=1*cm, rightMargin=1*cm)
            doc.build(elements)
            self._open_pdf(file_path)
        except Exception as e:
            messagebox.showerror("خطأ في إنشاء PDF", f"فشل إنشاء ملف PDF: {e}")
            traceback.print_exc()

    def _open_pdf(self, filename):
        """Opens the specified file using the default system application."""
        time.sleep(0.5)
        try:
            if sys.platform == "win32":
                os.startfile(filename)
            elif sys.platform == "darwin":
                subprocess.run(['open', filename], check=True)
            else:
                subprocess.run(['xdg-open', filename], check=True)
        except Exception as e:
            messagebox.showerror("خطأ في فتح الملف", f"لا يمكن فتح ملف PDF:\n{e}")

