########################### Imports #########################################
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.platypus.tables import Table, TableStyle, colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys
from datetime import datetime
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
import traceback
from tkinter import messagebox
import time
import subprocess # Added for open_pdf on macOS/Linux
#############################################################################
from model.Customer_compnents_model.buy_report_model import BuyReportModel


class BuyReportController:
    def __init__(self, supplier, buys_operations):
        # data = [{
        #                 'cusname': self.view.cus_name.get(),
        #                 'productcode': self.view.product_code.get(),
        #                 'quantity': self.view.quantity.get(),
        #                 'discount': self.view.discount.get(),
        #                 'paid': self.view.checkbox_var.get()و
        #                 'date': 
        #     }, ]
        self.buys_operations = buys_operations
        self.supplier = supplier
        self.model = BuyReportModel()
        
        self.arabic_font_name = 'Arial'
        self.Bold_arabic_font_name = "SegoeUIBoldCustom"
        self.pagesize = letter
        self._register_fonts() 
        all_processed_data = self.preprocess_data(data=self.buys_operations)
        # for row in self.buys_operations:
        #     self.run(cus_name= self.buys_operations["cus_name"], purchase_id= purchase_id, purchase_date = purchase_date,  total_discount = total_discount, old_account= old_account,data = preprocessed_data)
        # preprocessed data = [ total price = quantity * price_per_piece , price_per_piece, quantity, product_type ]
        print(f"self.buys_operations = {self.buys_operations}")
        for index, all_data in enumerate(all_processed_data):
            self.run(cus_name= self.buys_operations[index][0]["cusname"],  purchase_date = self.buys_operations[index][0]["date"],  total_discount = all_data[0], old_account= self.buys_operations[index][0]["cus_money_before"],data = all_data[1])


    def _handle_bold_font_fallback(self, original_bold_name):
        """Handles fallback for the bold font if custom registration fails."""
        print(f"Warning: Custom bold font '{original_bold_name}' could not be registered or its file was not found.")

        # Fallback 2: Try Helvetica-Bold (standard PDF font, good for non-Arabic bold text, might not render Arabic)
        try:
            pdfmetrics.getFont('Helvetica-Bold') # Check if it's known to ReportLab
            self.Bold_arabic_font_name = 'Helvetica-Bold'
            print(f"Fallback: Using 'Helvetica-Bold' for text styled as '{original_bold_name}'. Arabic characters may not render correctly with this fallback.")
            return
        except KeyError:
            pass # Helvetica-Bold not found or not suitable

        # Fallback 3: Use the regular Arabic font. Text won't be bold, but should render Arabic correctly.
        print(f"Fallback: Using '{self.arabic_font_name}' (regular) for text styled as '{original_bold_name}'. Text will not be bold.")
        self.Bold_arabic_font_name = self.arabic_font_name


    def _register_fonts(self):
        """Registers the Arabic fonts for ReportLab if not already registered."""
        # --- Registration for self.arabic_font_name (Regular Arial/DejaVu) ---
        try:
            pdfmetrics.getFont(self.arabic_font_name)
            print(f"Font '{self.arabic_font_name}' already registered.")
        except KeyError: # Font not yet registered
            font_path = None
            potential_regular_font_name = 'Arial' # Keep track of the intended name

            if sys.platform == "win32":
                font_path = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "arial.ttf")
            elif sys.platform == "darwin": # macOS
                font_path = "/Library/Fonts/Arial.ttf"
                if not os.path.exists(font_path):
                    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
            else: # Linux
                linux_paths = [
                    ("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", "Arial"),
                    ("/usr/share/fonts/TTF/arial.ttf", "Arial"),
                    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans")
                ]
                for p, name in linux_paths:
                    if os.path.exists(p):
                        font_path = p
                        potential_regular_font_name = name # Update if using DejaVu
                        break
            
            if font_path and os.path.exists(font_path):
                try:
                    self.arabic_font_name = potential_regular_font_name # Set the actual font name being used
                    pdfmetrics.registerFont(TTFont(self.arabic_font_name, font_path))
                    print(f"Successfully registered font: {self.arabic_font_name} from {font_path}")
                except Exception as e:
                    print(f"Warning: Could not register font {potential_regular_font_name} from {font_path}. Error: {e}")
                    traceback.print_exc()
                    self.arabic_font_name = 'Helvetica' 
                    print(f"Fell back to using 'Helvetica' for regular Arabic text.")
            else:
                print(f"Warning: Font file for {potential_regular_font_name} not found at expected paths.")
                self.arabic_font_name = 'Helvetica'
                print(f"Fell back to using 'Helvetica' for regular Arabic text.")
                
                
        # --- Registration for self.Bold_arabic_font_name (SegoeUIBoldCustom) ---
        # Store the original desired name for fallback messages
        original_bold_font_name_request = self.Bold_arabic_font_name
        try:
            pdfmetrics.getFont(self.Bold_arabic_font_name)
            print(f"Font '{self.Bold_arabic_font_name}' already registered.")
        except KeyError: # Font 'SegoeUIBoldCustom' not yet registered
            # Path for the custom bold font. This should be relative to the script or an absolute path.
            # Ensure "required files" directory is in the same location as your script,
            # or provide an absolute path.
            bold_font_path = os.path.join("required files", "alfont_com_AlFont_com_Segoe.UI_.Bold_DownloadSoftware.iR_.ttf")

            if os.path.exists(bold_font_path):
                try:
                    # Register the font with its correct name: self.Bold_arabic_font_name
                    pdfmetrics.registerFont(TTFont(self.Bold_arabic_font_name, bold_font_path))
                    print(f"Successfully registered font: {self.Bold_arabic_font_name} from {bold_font_path}")
                except Exception as e:
                    print(f"Warning: Could not register font {self.Bold_arabic_font_name} from {bold_font_path}. Error: {e}")
                    traceback.print_exc()
                    self._handle_bold_font_fallback(original_bold_font_name_request)
            else:
                print(f"Warning: Font file for {self.Bold_arabic_font_name} not found at '{bold_font_path}'.")
                self._handle_bold_font_fallback(original_bold_font_name_request)


    def _get_rtl_style(self, alignment=TA_RIGHT, fontSize=10, leading=14, spaceBefore=6, spaceAfter=6, font_name=None):
        """Creates a customized ParagraphStyle for RTL text."""
        # Use specified font_name or default to self.arabic_font_name
        actual_font_name = font_name if font_name else self.arabic_font_name
        
        # Style name includes parameters to ensure uniqueness if multiple styles are needed
        style_name = f'RTL_Style_{actual_font_name}_{alignment}_{fontSize}_{leading}_{spaceBefore}_{spaceAfter}'
        styles = getSampleStyleSheet()
        
        # Check if style already exists to avoid re-adding
        if ParagraphStyle(name=style_name, fontName=actual_font_name) in styles:
             return styles[style_name]

        new_style = ParagraphStyle(
            name=style_name,
            parent=styles['Normal'],
            fontName=actual_font_name,
            alignment=alignment,
            fontSize=fontSize,
            leading=leading,
            wordWrap='RTL', 
            spaceBefore=spaceBefore,
            spaceAfter=spaceAfter,
        )
        styles.add(new_style) # Add the new style to the stylesheet
        return new_style


    def _reshape_and_bidi(self, text):
        """Helper method to reshape and apply bidi algorithm for display in PDF."""
        text_str = str(text) if text is not None else ""
        if not text_str:
            return ""

        common_labels = ["الوقت", "المبلغ", "المشتريات", "المدفوعات", "المرتجعات", "الإجمالي",
                            "كشف حساب مصنع:", "شركة البهجي للبرمجيات", "تاريخ التقرير:",
                            "الرصيد النهائي المستحق عليكم", "الرصيد النهائي المستحق لكم",
                            "الرصيد النهائي صفر", "ج.م", "الصنف", "الكمية", "السعر", "الاجمالى", "الid"]
        
        needs_processing = any('\u0600' <= char <= '\u06FF' for char in text_str) or \
                            any(label in text_str for label in common_labels)

        if needs_processing:
            try:
                reshaped_text = arabic_reshaper.reshape(text_str)
                return get_display(reshaped_text)
            except Exception: # Simplified exception handling
                return text_str 
        return text_str

#####################################
    def sort_customers(self, buys):
        for buy in buys :
            buy['cus_id'] = self.model.get_cus_id_from_name(buy['cusname'])
            buy['product_id'] = self.model.get_product_id_from_code(buy['productcode'])
            buy['price_befor_discount'] = self.model.get_product_price_from_id(buy['product_id']) # price befor the discount
        buys.sort(key=lambda x: x['cus_id'])
        
        def group_by_customer(buys):
            cus_grouped_lists = []
            current_group = [buys[0]] 
            for i in range(1, len(buys)):
                if buys[i]['cus_id'] == current_group[0]['cus_id']:
                    current_group.append(buys[i])
                else:
                    cus_grouped_lists.append(current_group)
                    current_group = [buys[i]]
            cus_grouped_lists.append(current_group) 
            return cus_grouped_lists
        
        buys = group_by_customer(buys)
        '''
        now buys = [
            # [ list of buys of the same customer ]
             [
            {'cusname' : cusname, 
             'cus_id' : cus_id, 
             'product_id' : product_id, 
             'price_befor_discount' : price_befor_discount,  
             'productcode' : productcode id, 
             'quantity' : quantity, 
             'discount' : discount, 
             'paid' : yes(1) or not(0),
             'cus_money_before': cus_money_before,
             }, 
             
            {'cusname' : cus id, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},],
             [{'cusname' : cusname, 'cus_id' : cus_id, 'product_id' : product_id, 'price_befor_discount' : price_befor_discount,  'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)}, {'cusname' : cus id, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},],
             ]
        '''
        return buys

    def preprocess_data(self, data):
        # data = [{
        #                 'cusname': self.view.cus_name.get(),
        #                 'productcode': self.view.product_code.get(),
        #                 'quantity': self.view.quantity.get(),
        #                 'discount': self.view.discount.get(),
        #                 'paid': self.view.checkbox_var.get(),
        #                 'cus_money_before': cus_money_before,
        
        #     }, ]
        data = self.sort_customers(data)
        print("data:", data)
        self.buys_operations = data
        print("self.buys_operations:", self.buys_operations)
        '''
        data now =[
            [{'cusname' : cusname, 
             'cus_id' : cus_id, 
             'product_id' : product_id, 
             'price_befor_discount' : price_befor_discount,  
             'productcode' : productcode id, 
             'quantity' : quantity, 
             'discount' : discount, 
             'paid' : yes(1) or not(0)},
             'cus_money_before': cus_money_before,],
             
            [],
        ]
        '''
        all_processed_data = []
        for customer in data:
            
            processed_data = []
            totlal_discount = 0
            
            for buy in customer:
                total_price = int(buy['quantity']) * float(buy['price_befor_discount'])
                price_per_piece = buy['price_befor_discount']
                quantity = buy['quantity']
                product_type = buy['productcode']
                totlal_discount += float(buy['discount'])
                processed_data.append([total_price, price_per_piece, quantity, product_type])
            
            all_processed_data.append([totlal_discount , processed_data])
            
            
        # preprocessed data = [ total price = quantity * price_per_piece , price_per_piece, quantity, product_type ]
            
        return all_processed_data


    def run(self,cus_name, purchase_date, data, total_discount, old_account):
        elements = []
        #################################
        
        if self.supplier == 'snow white':
            image_path = "images/Snow White 2  .jpeg"  
        elif self.supplier == 'golden rose':
            image_path = "images/golden 2 .jpeg"
        else: # Default or error case
            image_path = None
            print(f"Warning: Unknown resource '{self.supplier}', no image will be added.")

        if image_path and os.path.exists(image_path):
            try:
                img = Image(image_path, width=3*cm, height=3*cm, hAlign='CENTER')
                elements.append(img)
            except Exception as e:
                print(f"Warning: Could not load or add image '{image_path}'. Error: {e}")
        elif image_path:
            print(f"Warning: Image path specified but file not found: '{image_path}'")
        #################################
        
        intro_table_data = [
            [self._reshape_and_bidi("snow white مصنع") if self.supplier == 'snow white' else self._reshape_and_bidi("golden rose مصنع"),self._reshape_and_bidi("فاتورة مبيعات نقدا"),self._reshape_and_bidi("عميل: " + cus_name),],[self._reshape_and_bidi("القاهرة"),self._reshape_and_bidi(purchase_date),],["","",""]
        ]

        intro_table = Table(intro_table_data, rowHeights=25 ,colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        intro_table.setStyle(TableStyle([
                ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), # Use regular Arabic font
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (1,0), (1,0), 'CENTER'),
                ('ALIGN', (2,0), (2,0), 'RIGHT'),
                ('ALIGN', (0,1), (0,1), 'LEFT'),
                ('ALIGN', (1,1), (1,1), 'CENTER'),
                ('ALIGN', (2,1), (2,1), 'RIGHT'),
                ('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),
            ]))

        elements.append(intro_table)
        elements.append(Spacer(1, 0.5*cm))
        #################################
        
        My_Table_Data = [    
                [self._reshape_and_bidi("الاجمالى"),self._reshape_and_bidi("السعر"),self._reshape_and_bidi("الكمية"),self._reshape_and_bidi("الصنف"),self._reshape_and_bidi("م")],
                ##### Example row #####
                # [ 50, 10      ,5  , '1001', '1'],
                ]
        total_quantity = 0
        totalprice = 0
        for i, row in enumerate(data) :
            row.append(i+1)
            My_Table_Data.append(row)
            total_quantity += int(row[2])
            totalprice += float(row[0])
        
        My_Table_Data.append([
            totalprice,"", total_quantity,self._reshape_and_bidi('الاجمالى: '),"" 
            ])

        Main_Data_Table = Table(My_Table_Data,rowHeights=25,
                    colWidths=[5.5*cm, 3.5*cm, 1.5*cm, 7.5*cm, 2*cm],
                    hAlign = 'LEFT'
                    )

        Main_Data_Table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.arabic_font_name), # Use regular Arabic font
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -2), 1, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN',(0, 0), (-1, -1), 'CENTER'), 
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('GRID', (0, 0), (-1, 0), 1, colors.black), 
            ('TEXTCOLOR', (0,0), (-1,0), colors.white), 
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN',(3, 1), (3, -1), 'RIGHT'), 
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white), 
            ('BACKGROUND', (0,-1), (-1,-1), colors.gray), 
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('GRID', (0, -1), (-1, -1), 1.5, colors.black),
            ('SPAN', (-2, -1), (-1, -1)),
        ]))
        
        elements.append(Main_Data_Table)
        elements.append(Spacer(1, 0.5*cm))
        ###########################################
        
        Summer_Table_Data = [
            [totalprice,self._reshape_and_bidi("الاجمالى"),"","",""],
            [total_discount,self._reshape_and_bidi("الخصم"),"","",""],
            [totalprice - total_discount,self._reshape_and_bidi("الباقى بعد الخصم"),"","",""]   if self.supplier == 'Snow White' else [totalprice - total_discount,self._reshape_and_bidi("الاجمالى بعد الخصم"),"","",""],
            [old_account,self._reshape_and_bidi("الحساب السابق"),"","",""],
            [old_account + (totalprice - total_discount),self._reshape_and_bidi("الحساب الحالى"),"","",""],
        ]
        
        Summer_Table = Table(Summer_Table_Data,rowHeights=25,
                            colWidths=[5.5*cm, 7.5*cm, 1.5*cm, 7.5*cm, 2*cm],
                            hAlign = 'LEFT'
                            )
        Summer_Table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.Bold_arabic_font_name), 
            ('FONTSIZE', (0,0), (-1,-1), 10), # Adjusted font size for bold, can be same as regular if preferred
            ('LINEABOVE',(0,0),(-1,0),1,colors.black),
            ('LINEAFTER', (0,0), (0,-1), 0.30, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('ALIGN', (1,0), (1,-1), 'RIGHT')

        ]))
        elements.append(Summer_Table)
        ###########################################
        
        self.create_and_print_pdf(elements)

    def create_and_print_pdf(self, elements,  margin=1.5*cm):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("cus_buy_reports", exist_ok=True)
        my_path = os.path.join("cus_buy_reports", f"table_{timestamp}.pdf")
        
        try:
            doc = SimpleDocTemplate(
                my_path,
                pagesize=self.pagesize,
                rightMargin=1*cm,
                leftMargin=1*cm, # Adjusted for symmetry, was 0
                topMargin=0.5*cm,
                bottomMargin=margin,
            )
            doc.build(elements)
            self.open_pdf(my_path)

        except Exception as e:
            messagebox.showerror("خطأ في إنشاء PDF", f"فشل إنشاء ملف PDF: {e}\nFile: {my_path}")
            traceback.print_exc()

    def open_pdf(self, filename):
        time.sleep(1)
        if not os.path.exists(filename):
                messagebox.showerror("خطأ", f"لم يتم العثور على ملف PDF: {filename}")
                return
        try:
            if sys.platform == "win32":
                os.startfile(filename) 
            elif sys.platform == "darwin": 
                subprocess.run(['open', filename], check=True)
            else: 
                subprocess.run(['xdg-open', filename], check=True)
        except Exception as e:
            messagebox.showerror("خطأ في فتح الملف", f"لا يمكن فتح ملف PDF:\n{e}")
            traceback.print_exc()


