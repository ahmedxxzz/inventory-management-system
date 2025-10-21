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
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (0,-1), 'LEFT'), ('ALIGN', (1,0), (1,-1), 'CENTER'),
            ('ALIGN', (2,0), (2,-1), 'RIGHT'), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.5*cm))

        # 3. Add Items Table
        items_header = [self._reshape(h) for h in ["الإجمالي قبل الخصم", "السعر", "الكمية", "الصنف", "م"]]
        table_data = [items_header]
        
        total_quantity = 0
        grand_total_before_discount = 0.0
        total_discount_amount = 0.0

        for i, item in enumerate(self.bill_data['items'], 1):
            item_total_before_discount = item['price'] * item['quantity']
            item_discount = item['discount'] * item['quantity']
            
            total_quantity += item['quantity']
            grand_total_before_discount += item_total_before_discount
            total_discount_amount += item_discount
            
            row = [
                f"{item_total_before_discount:,.2f}",
                f"{item['price']:,.2f}",
                str(item['quantity']),
                self._reshape(item['product_name']),
                str(i)
            ]
            table_data.append(row)
            
        net_total = grand_total_before_discount - total_discount_amount
        
        summary_row_1 = [f"{grand_total_before_discount:,.2f}", "", str(total_quantity), self._reshape("الإجمالي"), ""]
        table_data.append(summary_row_1)
        
        final_summary_row = [f"{net_total:,.2f}", self._reshape("صافي الفاتورة:"), f"{total_discount_amount:,.2f}", self._reshape("مجموع الخصم:"), ""]
        table_data.append(final_summary_row)
        
        items_table_col_widths = [3.5*cm, 3*cm, 2*cm, 8*cm, 1.5*cm]
        items_table = Table(table_data, colWidths=items_table_col_widths)
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-3), 0.25, colors.grey),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0,0), (-1,-0), colors.white),
            ('FONTNAME', (0,0), (-1,0), self.bold_arabic_font_name),
            ('BACKGROUND', (0,-2), (-1,-2), colors.lightgrey),
            ('FONTNAME', (0,-2), (-1,-2), self.bold_arabic_font_name),
            ('SPAN', (3, -2), (4, -2)),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.white),
            ('FONTNAME', (0,-1), (-1,-1), self.bold_arabic_font_name),
            ('ALIGN', (1, -1), (1, -1), 'RIGHT'),
            ('ALIGN', (3, -1), (3, -1), 'RIGHT'),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.2*cm))

        # --- START OF MODIFICATION ---
        # 4. Add Footer with account details
        status = self._reshape("آجل") if self.bill_data['is_paid'] == 0 else self._reshape("نقدي (مدفوعة)")
        currency = self._reshape("ج.م")
        
        footer_data = [
            [f"{grand_total_before_discount:,.2f} {currency}", self._reshape("الفاتورة قبل الخصم")],
            [f"{total_discount_amount:,.2f} {currency}", self._reshape("الخصم")],
            [f"{net_total:,.2f} {currency}", self._reshape("صافى الفاتورة بعد الخصم")],
            [f"{self.bill_data['balance_after']:,.2f} {currency}", self._reshape("الحساب عليكم بعد الفاتورة")],
        ]
        
        footer_table = Table(footer_data, colWidths=[5*cm, 7*cm])
        
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.bold_arabic_font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            # Apply inner grid to all, which draws the line between columns and rows
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
            # Apply the outer BOX only to the first column (index 0)
            ('BOX', (0, 0), (0, -1), 1, colors.black),
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ]))
        
        items_table_total_width = sum(items_table_col_widths)
        
        footer_wrapper = Table([[footer_table]], colWidths=[items_table_total_width], hAlign='CENTER')
        
        # Add a line above the wrapper and padding to create space
        footer_wrapper.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            # Add a black line above the entire wrapper cell
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            # Add some padding on top to push the footer table down from the line
            ('TOPPADDING', (0,0), (-1,-1), 8),
        ]))

        elements.append(footer_wrapper)
        # --- END OF MODIFICATION ---

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