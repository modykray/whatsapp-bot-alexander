import os
import time
import base64
from io import BytesIO
from alright import WhatsApp
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import threading
import logging

class WhatsAppClient:
    def __init__(self):
        self.messenger = None
        self.qr_code_base64 = None
        self.session_status = "disconnected"
        self.is_authenticated = False
        self.qr_thread = None
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_chrome_options(self):
        """إعداد خيارات Chrome للتشغيل في البيئة السحابية"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
        return chrome_options
        
    def start_session(self):
        """بدء جلسة واتساب وتوليد رمز QR"""
        try:
            self.logger.info("بدء جلسة واتساب...")
            self.session_status = "starting"
            
            # إنشاء عميل واتساب مع خيارات Chrome المخصصة
            chrome_options = self.get_chrome_options()
            self.messenger = WhatsApp(web_driver_options=chrome_options)
            
            # بدء thread منفصل لمراقبة رمز QR
            self.qr_thread = threading.Thread(target=self._monitor_qr_code)
            self.qr_thread.daemon = True
            self.qr_thread.start()
            
            self.session_status = "waiting_for_scan"
            self.logger.info("تم بدء الجلسة، في انتظار مسح رمز QR...")
            
        except Exception as e:
            self.logger.error(f"خطأ في بدء الجلسة: {str(e)}")
            self.session_status = "error"
            
    def _monitor_qr_code(self):
        """مراقبة رمز QR وحالة الاتصال"""
        max_attempts = 30  # 30 محاولة (حوالي 5 دقائق)
        attempt = 0
        
        while attempt < max_attempts and not self.is_authenticated:
            try:
                # البحث عن رمز QR في الصفحة
                qr_element = self.messenger.driver.find_element(By.CSS_SELECTOR, "canvas[aria-label='Scan me!']")
                
                if qr_element:
                    # التقاط رمز QR وتحويله إلى base64
                    qr_screenshot = qr_element.screenshot_as_png
                    self.qr_code_base64 = base64.b64encode(qr_screenshot).decode('utf-8')
                    self.session_status = "waiting_for_scan"
                    self.logger.info("تم تحديث رمز QR")
                    
                # فحص حالة الاتصال
                if self._check_authentication():
                    self.is_authenticated = True
                    self.session_status = "authenticated"
                    self.logger.info("تم الربط بنجاح!")
                    break
                    
            except NoSuchElementException:
                # إذا لم يتم العثور على رمز QR، قد يكون المستخدم قد سجل الدخول
                if self._check_authentication():
                    self.is_authenticated = True
                    self.session_status = "authenticated"
                    self.logger.info("تم الربط بنجاح!")
                    break
                    
            except Exception as e:
                self.logger.error(f"خطأ في مراقبة رمز QR: {str(e)}")
                
            time.sleep(10)  # انتظار 10 ثوانٍ قبل المحاولة التالية
            attempt += 1
            
        if not self.is_authenticated:
            self.session_status = "timeout"
            self.logger.warning("انتهت مهلة انتظار مسح رمز QR")
            
    def _check_authentication(self):
        """فحص ما إذا كان المستخدم قد سجل الدخول"""
        try:
            # البحث عن عناصر تدل على نجاح تسجيل الدخول
            chat_elements = self.messenger.driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']")
            search_elements = self.messenger.driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list-search']")
            
            return len(chat_elements) > 0 or len(search_elements) > 0
            
        except Exception as e:
            self.logger.error(f"خطأ في فحص حالة المصادقة: {str(e)}")
            return False
            
    def get_qr_code_base64(self):
        """إرجاع رمز QR كـ base64"""
        if self.qr_code_base64:
            return self.qr_code_base64
        else:
            # إرجاع رمز QR افتراضي إذا لم يكن متوفراً
            return self._generate_placeholder_qr()
            
    def _generate_placeholder_qr(self):
        """توليد رمز QR افتراضي للعرض"""
        try:
            import qrcode
            from PIL import Image
            
            # إنشاء رمز QR افتراضي
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data("https://web.whatsapp.com - في انتظار الاتصال...")
            qr.make(fit=True)
            
            # تحويل إلى صورة
            img = qr.make_image(fill_color="black", back_color="white")
            
            # تحويل إلى base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            self.logger.error(f"خطأ في توليد رمز QR افتراضي: {str(e)}")
            return ""
            
    def get_session_status(self):
        """إرجاع حالة الجلسة الحالية"""
        return self.session_status
        
    def send_message(self, phone_number, message):
        """إرسال رسالة إلى رقم معين"""
        if not self.is_authenticated:
            return {"status": "error", "message": "البوت غير متصل"}
            
        try:
            self.messenger.send_direct_message(phone_number, message)
            return {"status": "success", "message": "تم إرسال الرسالة بنجاح"}
            
        except Exception as e:
            self.logger.error(f"خطأ في إرسال الرسالة: {str(e)}")
            return {"status": "error", "message": f"فشل في إرسال الرسالة: {str(e)}"}
            
    def close_session(self):
        """إغلاق الجلسة"""
        try:
            if self.messenger and self.messenger.driver:
                self.messenger.driver.quit()
            self.session_status = "disconnected"
            self.is_authenticated = False
            self.logger.info("تم إغلاق الجلسة")
            
        except Exception as e:
            self.logger.error(f"خطأ في إغلاق الجلسة: {str(e)}")

# إنشاء مثيل عالمي للعميل
whatsapp_client = WhatsAppClient()

