import os
import subprocess
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import sys

class FactoryReturnReportController:
    """
    A class to generate a PDF report for a factory return receipt.
    It dynamically finds and uses the system's Arial font for robust Arabic support.
    """
    def __init__(self, return_data):
        """
        Initializes the report generator.
        Args:
            return_data (dict): A dictionary containing all necessary data for the report.
                                Expected keys: 'return_id', 'factory_name', 'date', 'items',
                                'balance_before', 'balance_after'.
                                The 'items' key should be a list of dicts, each with:
                                'product_name', 'quantity', 'price_at_return'.
        """
        self.return_data = return_data
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR)) 
        
        self.logo_path = os.path.join(self.BASE_DIR, 'Z_Files', 'images', 'Golden_Rose.png')
        self.unicode_font_loaded = False
        
    def _handle_arabic(self, text):
        """Prepares Arabic text for display in FPDF."""
        reshaped_text = arabic_reshaper.reshape(str(text))
        return get_display(reshaped_text)

    def _set_font(self, pdf, style="", size=12):
        """Sets the font to our loaded Unicode font, otherwise falls back to built-in Arial."""
        font_family = "ArialUnicode" if self.unicode_font_loaded else "Arial"
        pdf.set_font(font_family, style, size)

    def generate_pdf(self):
        """Main method to create, format, save, and open the PDF."""
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        
        try:
            if sys.platform == "win32":
                font_directory = os.path.join(os.environ.get("WINDIR"), "Fonts")
                arial_path = os.path.join(font_directory, "Arial.ttf")
                if os.path.exists(arial_path):
                    pdf.add_font("ArialUnicode", "", arial_path, uni=True)
                    pdf.add_font("ArialUnicode", "B", arial_path, uni=True)
                    self.unicode_font_loaded = True
                    print("Successfully loaded system Arial font for Arabic support.")
                else:
                    raise RuntimeError("Arial.ttf not found in system Fonts directory.")
            # Add paths for other OS if needed
        except Exception as e:
            print(f"WARNING: Could not load system font for Arabic. Error: {e}")
            self.unicode_font_loaded = False
        
        self._draw_header(pdf)
        grand_total, total_quantity = self._draw_table(pdf)
        self._draw_footer(pdf, grand_total, total_quantity)
        
        file_path = self._save_pdf(pdf)
        if file_path:
            self._open_pdf(file_path, 'print') # Open directly in print dialog

    def _draw_header(self, pdf):
        """Draws the receipt's header section with logo and info."""
        try:
            logo_width = 60
            x_pos = (pdf.w - logo_width) / 2
            pdf.image(self.logo_path, x=x_pos, w=logo_width)
            pdf.ln(10)
        except Exception:
            self._set_font(pdf, style="B", size=12)
            pdf.cell(0, 10, self._handle_arabic("لم يتم العثور على اللوجو"), ln=1, align="C")
            pdf.ln(10)
        
        page_width = pdf.w - 2 * pdf.l_margin
        cell_width = page_width / 3
        
        self._set_font(pdf, style="B", size=14)
        pdf.cell(cell_width, 10, txt=self._handle_arabic(f"مصنع: {self.return_data['factory_name']}"), align="L")
        pdf.cell(cell_width, 10, txt=self._handle_arabic("إيصال مرتجع"), align="C") # <-- CHANGED
        pdf.cell(cell_width, 10, txt=self._handle_arabic("مكتب: Golden Rose"), align="R", ln=1)

        self._set_font(pdf, style="", size=12)
        pdf.cell(cell_width, 10, txt=self._handle_arabic("القاهرة"), align="L")
        pdf.cell(cell_width, 10, txt=self._handle_arabic(f"تاريخ: {self.return_data['date']}"), align="C")
        pdf.cell(cell_width, 10, txt=self._handle_arabic(f"مرتجع رقم: {self.return_data['return_id']}"), align="R", ln=1) # <-- CHANGED

        pdf.ln(5)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + page_width, pdf.get_y())
        pdf.ln(5)

    def _draw_table(self, pdf):
        """Draws the returned items table and returns the calculated totals."""
        self._set_font(pdf, style="B", size=11)
        pdf.set_fill_color(200, 220, 255)
        # <-- MODIFIED: Columns redefined, "discount" removed
        col_widths = {"m": 15, "item": 90, "qty": 25, "price": 30, "total": 30}

        pdf.cell(col_widths["total"], 10, self._handle_arabic("الإجمالي"), border=1, align="C", fill=True)
        pdf.cell(col_widths["price"], 10, self._handle_arabic("السعر"), border=1, align="C", fill=True)
        pdf.cell(col_widths["qty"], 10, self._handle_arabic("الكمية"), border=1, align="C", fill=True)
        pdf.cell(col_widths["item"], 10, self._handle_arabic("الصنف"), border=1, align="C", fill=True)
        pdf.cell(col_widths["m"], 10, self._handle_arabic("م"), border=1, align="C", fill=True, ln=1)
        
        self._set_font(pdf, style="", size=10)
        total_quantity = 0
        grand_total_price = 0.0
        
        for i, item in enumerate(self.return_data['items'], 1):
            # <-- MODIFIED: Simpler calculation without discount
            item_total = item['price_at_return'] * item['quantity']
            total_quantity += item['quantity']
            grand_total_price += item_total
            
            pdf.cell(col_widths["total"], 10, f"{item_total:,.2f}", border=1, align="C")
            pdf.cell(col_widths["price"], 10, f"{item['price_at_return']:,.2f}", border=1, align="C") # <-- MODIFIED
            pdf.cell(col_widths["qty"], 10, str(item['quantity']), border=1, align="C")
            pdf.cell(col_widths["item"], 10, self._handle_arabic(item['product_name']), border=1, align="R")
            pdf.cell(col_widths["m"], 10, str(i), border=1, align="C", ln=1)
            
        return grand_total_price, total_quantity

    def _draw_footer(self, pdf, grand_total, total_quantity):
        """Draws the summary/footer section of the receipt."""
        self._set_font(pdf, style="B", size=12)
        pdf.set_fill_color(230, 230, 230)
        # <-- MODIFIED: Adjusted for new columns
        col_widths = {"m": 15, "item": 90, "qty": 25, "price": 30, "total": 30}
        merged_width =  col_widths["item"] + col_widths["m"]
        
        pdf.cell(col_widths["total"], 10, f"{grand_total:,.2f}", border=1, align="C", fill=True)
        pdf.cell(col_widths["price"], 10, "", border=1, align="C", fill=True)
        pdf.cell(col_widths["qty"], 10, str(total_quantity), border=1, align="C", fill=True)
        pdf.cell(merged_width, 10, self._handle_arabic("الإجمالي النهائي"), border=1, align="C", fill=True, ln=1)
        pdf.ln(10)
        
        # <-- MODIFIED: Footer text updated for returns
        pdf.cell(0, 10, self._handle_arabic(f"حساب المصنع قبل المرتجع: {self.return_data['balance_before']:,.2f} ج.م"), ln=1, align="C")
        pdf.cell(0, 10, self._handle_arabic(f"قيمة المرتجع : {grand_total:,.2f} ج.م"), ln=1, align="C")
        pdf.cell(0, 10, self._handle_arabic(f"حساب المصنع بعد المرتجع: {self.return_data['balance_after']:,.2f} ج.م"), ln=1, align="C")

    def _save_pdf(self, pdf):
        """Saves the PDF to a structured directory and returns the full path."""
        original_cwd = os.getcwd()
        try:
            # Change directory to the base project folder to ensure relative paths work
            os.chdir(self.BASE_DIR)

            # <-- MODIFIED: Folder name for returns
            folder_name = os.path.join('Z_Files', 'reports', 'factory_returns')
            os.makedirs(folder_name, exist_ok=True)
            
            return_id = self.return_data['return_id']
            factory_name = self.return_data['factory_name'].replace(" ", "_")
            # <-- MODIFIED: File name for returns
            file_name = f"ReturnReceipt_{return_id}_{factory_name}.pdf"
            
            full_path = os.path.join(folder_name, file_name)
            pdf.output(full_path)
            return os.path.abspath(full_path)
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return None
        finally:
            os.chdir(original_cwd) # Always change back to the original directory

    def _open_pdf(self, file_path, operation='open'):
        """Opens the PDF file with the default system application, optionally for printing."""
        try:
            if sys.platform == "win32":
                os.startfile(file_path, operation)
            elif sys.platform == "darwin": # macOS
                subprocess.Popen(['open', file_path])
            else: # Linux
                subprocess.Popen(['xdg-open', file_path])
        except Exception as e:
            print(f"Error opening PDF automatically: {e}")