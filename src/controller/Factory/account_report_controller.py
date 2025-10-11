from model.Factory.account_report_model import AccountReportModel
import sys
import os
from datetime import datetime
import subprocess
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
from tkinter import messagebox
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4, letter, landscape 
from reportlab.lib.units import cm # For margins/spacing if needed
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT # For alignment constants
from reportlab.lib import colors # Import colors for styling








class AccountReportController:
    def __init__(self, factory_id=None, db_conn = None):
        self.db_conn = db_conn
        self.factory_data = {}
        self.factory_data['factory_id'] = factory_id
        self.pagesize = A4
        self.arabic_font_name = 'Helvetica' 
        self.model = AccountReportModel(self.factory_data['factory_id'], self.db_conn)
        self.factory_data['fac_name'], self.factory_data['fac_amount_money'], self.factory_data['fac_quantity'] = self.model.get_factory_data()
        self.define_data()
        self._register_arabic_font()
        self.structure_pdf()

    def _register_arabic_font(self):
        """Registers an Arabic-supporting font."""
        font_name = 'Arabic_Arial' # Give it a specific name
        registered = False
        paths_to_try = [
            'C:/Windows/Fonts/arial.ttf',
            '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/Library/Fonts/Arial.ttf',
            'Arial.ttf'
        ]
        for path in paths_to_try:
            try:
                if os.path.exists(path):
                    pdfmetrics.registerFont(TTFont(font_name, path))
                    print(f"Registered font '{font_name}' from {path}.")
                    self.arabic_font_name = font_name
                    registered = True
                    break
            except Exception:
                 continue

        if not registered:
            print(f"Warning: Could not find Arial or suitable font. Using default '{self.arabic_font_name}'.")
            messagebox.showwarning("خطأ في الخط", f"لم يتم العثور على خط Arial أو خط مناسب. قد لا يتم عرض النص العربي بشكل صحيح.\n سيتم استخدام الخط الافتراضي: {self.arabic_font_name}")


    def _get_rtl_style(self, alignment=TA_RIGHT, fontSize=10, leading=14, spaceBefore=6, spaceAfter=6):
        """Creates a customized ParagraphStyle for RTL text."""
        style_name = f'RTL_Style_{alignment}_{fontSize}_{leading}_{spaceBefore}_{spaceAfter}'
        styles = getSampleStyleSheet()
        if style_name in styles:
            return styles[style_name]
        new_style = ParagraphStyle(
            name=style_name, parent=styles['Normal'], fontName=self.arabic_font_name,
            alignment=alignment, fontSize=fontSize, leading=leading,
            wordWrap='RTL', spaceBefore=spaceBefore, spaceAfter=spaceAfter,
        )
        styles.add(new_style)
        return new_style


    def _reshape_and_bidi(self, text):
        """Helper method to reshape and apply bidi algorithm for display."""
        text_str = str(text) if text is not None else ""
        common_labels = ["الوقت", "المبلغ", "المشتريات", "المدفوعات", "المرتجعات", "الإجمالي",
                         "كشف حساب مصنع:", "شركة البهجي للبرمجيات", "تاريخ التقرير:",
                         "الرصيد النهائي المستحق عليكم", "الرصيد النهائي المستحق لكم",
                         "الرصيد النهائي صفر", "ج.م"]
        needs_processing = any('\u0600' <= char <= '\u06FF' for char in text_str) or \
                           any(label in text_str for label in common_labels)

        if needs_processing and text_str and not text_str.isnumeric():
            try:
                reshaped_text = arabic_reshaper.reshape(text_str)
                return get_display(reshaped_text)
            except Exception as e:
                print(f"Error reshaping/bidi text '{text_str}': {e}")
                return text_str
        return text_str




    def open_pdf(self, filename):
        """Opens the PDF file using the default system viewer."""
        if not os.path.exists(filename):
             messagebox.showerror("خطأ", f"لم يتم العثور على ملف PDF: {filename}")
             print(f"Error: PDF File not found at {filename}")
             return
        try:
            if sys.platform == "win32":
                os.startfile(filename, "print")
                
            elif sys.platform == "darwin": # macOS
                subprocess.run(['open', filename], check=True)
            else: # Linux variants
                subprocess.run(['xdg-open', filename], check=True)
        except Exception as e:
            messagebox.showerror("خطأ في فتح الملف", f"لا يمكن فتح ملف PDF:\n{e}")
            print(f"Error opening PDF: {e}")
            

    def print_pdf(self, filename):
        """Attempts to print a PDF file using system commands."""
        print(f"Attempting to print: {filename}")
        if not os.path.exists(filename):
             messagebox.showerror("خطأ", f"لم يتم العثور على ملف PDF للطباعة: {filename}")
             return False
        if sys.platform == 'win32':
            try:
                print("Direct printing unreliable on Windows. Opening PDF for manual printing.")
                messagebox.showinfo("طباعة", "سيتم فتح ملف ال PDF للعرض والطباعة اليدوية.")
                self.open_pdf(filename)
                 
            except Exception as e:
                messagebox.showerror("خطأ طباعة ويندوز", f"فشل إرسال الملف للطابعة أو فتحه: {e}")
                
        else:
            command = 'lp' if sys.platform == 'darwin' else 'lpr'
            try:
                subprocess.run([command, filename], check=True)
                print(f"Sent {filename} to the default printer via '{command}'.")
                messagebox.showinfo("تمت الطباعة", f"تم إرسال '{os.path.basename(filename)}' إلى الطابعة الافتراضية.")
            except subprocess.CalledProcessError as e:
                 messagebox.showerror("خطأ في الطباعة", f"فشلت عملية الطباعة.\nرمز الخطأ: {e.returncode}")
                 
            except FileNotFoundError:
                 messagebox.showerror("خطأ في الطباعة", f"أمر الطباعة '{command}' غير موجود.")
            except Exception as e:
                 messagebox.showerror("خطأ في الطباعة", f"حدث خطأ غير متوقع أثناء الطباعة: {e}")
                 

    def delete_pdf(self, file_path):
        """Deletes the specified PDF file, with error handling."""
        print(f"Attempting to delete: {file_path}")
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Successfully deleted: {file_path}")
            else:
                print(f"Deletion skipped: File not found at {file_path}")
        except PermissionError:
            messagebox.showerror("Error Deleting File", f"Permission denied to delete file:\n{file_path}")
        except OSError as e:
            messagebox.showerror("Error Deleting File", f"Could not delete file:\n{file_path}\nError: {e}")


    def define_data(self):
        self.factory_data["purchases_data"] = self.model.get_purchases_data() # returned data = [ (50010, '2022-01-01', 'buy'), (6014, '2022-01-02', 'buy') ]
        self.factory_data["paid_purchases_data"] = self.model.get_paid_purchases_data() # returned data = 150 
        self.factory_data["payments_data"] = self.model.get_payments_data() # returned data = [ (50010, '2022-01-01', 'pay'), (6014, '2022-01-02', 'pay') ]
        self.factory_data["returns_data"] = self.model.get_returned_data() # returned data = [ (50010, '2022-01-01', 'return'), (6014, '2022-01-02', 'return') ]
        
        
        self.factory_data["total_purchases"]= sum(float(p[0]) if p[0] is not None else 0 for p in self.factory_data["purchases_data"])
        self.factory_data["total_payments"]  = sum(float(p[0]) if p[0] is not None else 0 for p in self.factory_data["payments_data"])
        self.factory_data["total_returns"]  = sum(float(r[0]) if r[0] is not None else 0 for r in self.factory_data["returns_data"])
        self.factory_data["total_balance"] = self.factory_data["total_purchases"] - (self.factory_data["total_payments"] + self.factory_data["total_returns"] + self.factory_data["paid_purchases_data"])


    def structure_pdf(self):
        try:
            # --- Build the Whole PDF Content (Story) ---
            story = []
            header_style = self._get_rtl_style(alignment=TA_CENTER, fontSize=14, spaceAfter=10)
            subheader_style = self._get_rtl_style(alignment=TA_CENTER, fontSize=10, spaceBefore=2, spaceAfter=10)
            final_total_style = self._get_rtl_style(alignment=TA_CENTER, fontSize=12, spaceBefore=10, spaceAfter=10)
            story.append(Paragraph(self._reshape_and_bidi(f"كشف حساب مصنع: {self.factory_data['fac_name']}"), header_style))
            story.append(Paragraph(self._reshape_and_bidi(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), subheader_style))
            story.append(Spacer(1, 0.8*cm))

            # --- Prepare Table Data ---
            table_data = []
            # رؤوس الأعمدة الصحيحة: التاريخ، الفاتورة، الدفعة، المرتجع
            main_header = [self._reshape_and_bidi("التاريخ"), self._reshape_and_bidi("فاتورة"), self._reshape_and_bidi("دفعة"), self._reshape_and_bidi("مرتجع")]
            table_data.append(main_header)

            All_Data = []
            All_Data.extend([item for item in self.factory_data["purchases_data"]]) # (amount, date, type)
            All_Data.extend([item for item in self.factory_data["payments_data"]])
            All_Data.extend([item for item in self.factory_data["returns_data"]])

            All_Data.sort(key=lambda item: item[1]) # Sort by date

            print(f'All_Data sorted: {All_Data}')

            # Loop through sorted data and populate table rows correctly
            for process in All_Data:
                amount = f"{float(process[0]):,.2f}" if process[0] is not None else "0.00"
                date = process[1] if process[1] is not None else "" # Make sure date is not None

                row = [date, "-", "-", "-"] # Initialize row with date and empty values
                if process[2] == "buy":
                    row[1] = amount # Purchase amount in 'فاتورة' column
                elif process[2] == "pay":
                    row[2] = amount # Payment amount in 'دفعة' column
                elif process[2] == "return":
                    row[3] = amount # Return amount in 'مرتجع' column
                table_data.append(row)

            # Add total row
            total_label = self._reshape_and_bidi("الإجمالي")
            # الترتيب هنا لازم يطابق رؤوس الأعمدة: التاريخ، الفاتورة، الدفعة، المرتجع
            total_row = [total_label,
                         f"{self.factory_data['total_purchases']:,.2f}",
                         f"{self.factory_data['total_payments']:,.2f}",
                         f"{self.factory_data['total_returns']:,.2f}"]
            table_data.append(total_row)


            # --- Define Column Widths (4 columns) ---
            page_width, _ = self.pagesize
            margin_size = 1.0 * cm
            usable_width = page_width - (2 * margin_size)

            # Distribute usable width among 4 columns
            col_widths = [usable_width * 0.25, # التاريخ
                          usable_width * 0.25, # فاتورة
                          usable_width * 0.25, # دفعة
                          usable_width * 0.25] # مرتجع
            
            actual_total_width = sum(col_widths)
            print(f"Calculated Column Widths (cm): {[w/cm for w in col_widths]}. Total Table Width: {actual_total_width/cm:.2f} cm")

            # --- Define Table Style ---
            table_style = TableStyle([
                ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), self.arabic_font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),

                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=0.1, green=0.2, blue=0.4)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('TOPPADDING', (0, 0), (-1, 0), 4),

                # Data Rows Alignment (from row 1 up to row before total, i.e., (col, 1) to (col, -2))
                ('ALIGN', (0, 1), (0, -2), 'CENTER'), # التاريخ في المنتصف
                ('ALIGN', (1, 1), (1, -2), 'RIGHT'),  # فاتورة (المبلغ) لليمين
                ('ALIGN', (2, 1), (2, -2), 'RIGHT'),  # دفعة (المبلغ) لليمين
                ('ALIGN', (3, 1), (3, -2), 'RIGHT'),  # مرتجع (المبلغ) لليمين

                # Total Row (Row -1)
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
                ('FONTSIZE', (0, -1), (-1, -1), 10),
                ('TOPPADDING', (0, -1), (-1, -1), 5),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 5),
                ('GRID', (0, -1), (-1, -1), 0.5, colors.black),
                ('ALIGN', (0, -1), (0, -1), 'CENTER'), # "الإجمالي" Label في المنتصف
                ('ALIGN', (1, -1), (1, -1), 'RIGHT'), # Total Purchases لليمين
                ('ALIGN', (2, -1), (2, -1), 'RIGHT'), # Total Payments لليمين
                ('ALIGN', (3, -1), (3, -1), 'RIGHT'), # Total Returns لليمين
            ])

            # --- Create Table Object ---
            statement_table = Table(table_data, colWidths=col_widths, style=table_style)

            # --- Add Table to Story ---
            story.append(statement_table)
            story.append(Spacer(1, 0.8*cm))

            # --- Final Balance ---
            balance_desc = self._reshape_and_bidi("الرصيد النهائي المستحق عليكم")

            final_balance_text1 = f"{self._reshape_and_bidi('ج.م')} {abs(self.factory_data['paid_purchases_data']):,.2f} : {self._reshape_and_bidi("اجمالى المدفوع مسبقا اثناء الشراء")}"
            final_balance_text2 = f"{self._reshape_and_bidi('ج.م')} {abs(self.factory_data['total_balance']):,.2f} : {balance_desc}"
            story.append(Paragraph(final_balance_text1, final_total_style))
            story.append(Paragraph(final_balance_text2, final_total_style))

            # --- Generate and Print PDF ---
            self.create_and_print_pdf(story, f"factory_{self.factory_data['factory_id']}_statement_sidebyside", margin=margin_size)

        except Exception as e:
            messagebox.showerror("خطأ عام", f"حدث خطأ غير متوقع أثناء إنشاء الكشف: {e}")
            print(f"An unexpected error occurred: {e}")

    def create_and_print_pdf(self, story, base_filename, margin=1.5*cm):
        """Creates, saves, and optionally prints the PDF using specified margins."""
        save_dir = "Z_Files/reports/factory_statements"
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as e:
                 messagebox.showerror("Error Creating Directory", f"Could not create directory '{save_dir}': {e}")
                 print(f"Error creating directory {save_dir}: {e}")
                 return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_filename = os.path.join(save_dir, f"{base_filename}_{timestamp}.pdf")
        

        try:
            pdf_title = f"Account Statement - {self.factory_data['factory_id']}"
            factory_name = "Unknown Factory"
            pdf_title = self._reshape_and_bidi(f"كشف حساب مصنع: {self.factory_data['fac_name']}")
      
            doc = SimpleDocTemplate(
                self.pdf_filename,
                pagesize=self.pagesize,
                # *** Use the passed margin size ***
                rightMargin=margin,
                leftMargin=margin,
                topMargin=margin,      # Apply same margin to top/bottom for consistency
                bottomMargin=margin,
                title=pdf_title,
            )
            doc.build(story)
            print(f"تم إنشاء كشف الحساب بنجاح: {self.pdf_filename} with {margin/cm:.1f}cm margins")
            self.open_pdf(self.pdf_filename)

        except Exception as e:
            messagebox.showerror("خطأ في إنشاء PDF", f"فشل إنشاء ملف PDF: {e}\nFile: {self.pdf_filename}")
            print(f"Error building PDF '{self.pdf_filename}': {e}")
            

