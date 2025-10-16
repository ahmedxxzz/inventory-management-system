from fpdf import FPDF
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
import os, sys
import subprocess

class FactoryPayReportController:
    def __init__( self,data):
        # تهيئة البيانات ومجهز النصوص العربية
        self.data = data # factory_name, amount, date
        self.reshape = ArabicReshaper(configuration={'delete_harakat': True})
        # إنشاء الـ PDF
        self.add_data()
        self.create_pdf()


    def add_data(self):
        self.data["customer_name"] = "golden rose"


    def handle_arabic(self, text):
        reshaped_text = self.reshape.reshape(str(text))
        bidi_text = get_display(reshaped_text)
        return bidi_text

    def create_pdf(self):
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        
        # إضافة الخطوط اللازمة (العادي والـ Bold)
        try:
            pdf.add_font("SegoeUI", "", "Z_Files/required files/SegoeUI/Segoe.UI_.Bold.ttf", uni=True)
            pdf.add_font("SegoeUI", "B", "Z_Files/required files/SegoeUI/Segoe.UI_.Bold.ttf", uni=True)
            pdf.set_font("SegoeUI", size=12)
        except RuntimeError:
            print("خطأ: لم يتم العثور على ملف الخط. تأكد من أن المسار صحيح.")
            pdf.set_font("Arial", size=12)


        # 1. وضع الصورة في المنتصف في بداية الصفحة
        try:
            # عرض الصورة 60mm، ويتم حساب موقعها لتكون في المنتصف
            image_width = 60
            x_position = (pdf.w - image_width) / 2
            
            # <<< التعديل الرئيسي هنا >>>
            # تم حذف y=10 لوضع الصورة في مكان المؤشر الحالي
            # سيتم تحريك المؤشر تلقائياً لأسفل الصورة بعد وضعها
            pdf.image('Z_Files/images/Golden_Rose.png', x=x_position, w=image_width)           
            # ترك مسافة بسيطة بعد الصورة وقبل النص
            pdf.ln(10) 
            
        except FileNotFoundError:
            pdf.set_font("SegoeUI", "B", 12)
            pdf.cell(0, 10, self.handle_arabic("لم يتم العثور على الصورة. تأكد من المسار: 'Z_Files/images/golden 2 .jpeg'"), ln=1, align="C")
            pdf.ln(10)


        # 2. السطر الثاني (عميل، دفعة، مصنع)
        pdf.set_font("SegoeUI", "B", 14)
        page_width = pdf.w - 2 * pdf.l_margin 

        # تحديد عرض الخلايا
        cell_width = 50
        # تحديد عرض المسافات الفاصلة
        spacer_width = (page_width - (cell_width * 3)) / 2
        #
        # لو عايز تضبط المسافات يدويًا:
        # spacer_width = 20

        # الخلية الأولى (الدفعة)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(f"اسم المصنع:{self.data['factory_name']}"), align="L")
        # مسافة فاصلة
        pdf.cell(spacer_width, 10, txt="", border=0)
        # الخلية الثانية (اسم المصنع)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(f"وصل دفع"), align="L")
        # مسافة فاصلة أخرى
        pdf.cell(spacer_width, 10, txt="", border=0)
        # الخلية الثالثة (اسم العميل)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(f"مكتب: {self.data['customer_name']}"), align="R", ln=1)



        # 3. السطر الثالث (رقم العملية، التاريخ، المدينة)
        pdf.set_font("SegoeUI", "", 12)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(self.data['wallet_name']), align="L")
        pdf.cell(spacer_width, 10, txt="", border=0)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(f"تاريخ العملية: {self.data['payment_date']}"), align="C")
        pdf.cell(spacer_width, 10, txt="", border=0)
        pdf.cell(cell_width, 10, txt=self.handle_arabic(f"العملية رقم: {self.data['pay_id']}"), align="R",  ln=1)
        # 4. رسم خط فاصل
        pdf.ln(5) # ترك مسافة قبل الخط
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + page_width, pdf.get_y())
        pdf.ln(5) # ترك مسافة بعد الخط

        # 5. إنشاء الجدول (كما هو بدون تغيير)
        pdf.set_font("SegoeUI", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(45, 10, self.handle_arabic("المبلغ المدفوع"), border=1, align="C", fill=True, )
        pdf.cell(45, 10, self.handle_arabic("التاريخ"), border=1, align="C", fill=True)
        pdf.cell(80, 10, self.handle_arabic("اسم المصنع"), border=1, align="C", fill=True)
        pdf.cell(20, 10, self.handle_arabic("م"), border=1, align="C", fill=True, ln=1)

        pdf.set_font("SegoeUI", "", 11)
        pdf.cell(45, 10, f"ج.م {self.data['amount_paid']:,}", border=1, align="C",)
        pdf.cell(45, 10, str(self.data['payment_date']), border=1, align="C")
        pdf.cell(80, 10, self.handle_arabic(self.data['factory_name']), border=1, align="C")
        pdf.cell(20, 10, str(self.data['pay_id']), border=1, align="C", ln=1)

        # 6. رسم خط فاصل (كما هو بدون تغيير)
        pdf.ln(5)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + page_width, pdf.get_y())
        pdf.ln(5)

        # 7. الحسابات النهائية (تم تعديل المحاذاة لليمين لتبدو أفضل)
        pdf.set_font("SegoeUI", "B", 12)
        pdf.cell(0, 10, self.handle_arabic(f"الحساب قبل الدفع: {self.data['balance_before']:,} ج.م"), ln=1, align="C")
        pdf.cell(0, 10, self.handle_arabic(f"المبلغ المدفوع: {self.data['amount_paid']:,} ج.م"), ln=1, align="C")
        pdf.set_font("SegoeUI", "B", 14)
        pdf.cell(0, 12, self.handle_arabic(f"الحساب المتبقي عليكم: {self.data['balance_after']:,} ج.م"), ln=1, align="C")

        # حفظ الملف
        folder_name = "Z_Files/reports/factory_pays"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        file_name = f"receipt_{self.data['pay_id']}_{self.data['factory_name']}.pdf"
        full_path = os.path.join(folder_name, file_name)

        pdf.output(full_path)
        self.print_the_pdf(full_path)



    def print_the_pdf(self, file_path):
        try:
            # هذا السطر يعمل فقط على ويندوز
            if sys.platform == "win32":
                # <<< --- هذا هو التعديل الوحيد والمطلوب --- >>>
                # إضافة 'print' كفعل افتراضي لتنفيذه على الملف
                os.startfile(file_path, 'print')
                print(f"تم إرسال الملف '{file_path}' إلى قائمة الطباعة.")
            else:
                # الأنظمة الأخرى لا تدعم هذا الأمر مباشرة، سنكتفي بفتحه
                # (يمكن استخدام أوامر أكثر تعقيداً مثل 'lp' أو 'lpr' في لينكس/ماك)
                if sys.platform == "darwin": # macOS
                    subprocess.Popen(["open", file_path])
                else: # Linux
                    subprocess.Popen(["xdg-open", file_path])
                print(f"تم فتح الملف '{file_path}' (الطباعة المباشرة غير مدعومة تلقائياً على هذا النظام).")

        except FileNotFoundError:
            print(f"خطأ: لم يتم العثور على الملف '{file_path}'.")
        except Exception as e:
            print(f"حدث خطأ أثناء محاولة طباعة الملف: {e}")