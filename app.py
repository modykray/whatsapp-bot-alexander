from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import string
import requests
import os
from datetime import datetime
from group_manager import GroupManager
from entertainment import EntertainmentManager
from tools_manager import ToolsManager
from verification_system import VerificationSystem
from qr_manager import QRManager

app = Flask(__name__)
CORS(app)

# قاعدة بيانات بسيطة في الذاكرة
bot_users = {}
verification_codes = {}
admin_users = set()

# إنشاء مديرين للمجموعات والتسلية والأدوات ونظام التحقق
group_manager = GroupManager()
entertainment_manager = EntertainmentManager()
tools_manager = ToolsManager()
verification_system = VerificationSystem()
qr_manager = QRManager()

# رقم المطور
DEVELOPER_NUMBER = "01227812859"
DEVELOPER_NAME = "Alexander Mody"

# إيموجيات عشوائية للقوائم
RANDOM_EMOJIS = ["💘", "🇵🇸", "🎀", "🦧", "💎", "🌟", "🔥", "⚡", "🎯", "🎪"]

def get_random_emoji():
    return random.choice(RANDOM_EMOJIS)

def generate_verification_code():
    """توليد كود تحقق عشوائي"""
    return ".join(random.choices(string.ascii_lowercase + string.digits, k=8))"

def is_admin(phone_number, group_id=None):
    """التحقق من صلاحيات الادمن"""
    return phone_number in admin_users or phone_number == DEVELOPER_NUMBER

def get_main_menu():
    """إنشاء القائمة الرئيسية"""
    emoji1 = get_random_emoji()
    emoji2 = get_random_emoji()
    emoji3 = get_random_emoji()
    emoji4 = get_random_emoji()
    emoji5 = get_random_emoji()
    emoji6 = get_random_emoji()
    emoji7 = get_random_emoji()
    
    menu = f"""🤖 *مرحباً بك في بوت الكساندر* 🤖

📋 *القوائم المتاحة:*

{emoji1} *المجموعات* - اكتب: م1
{emoji2} *التسلية* - اكتب: م2  
{emoji3} *المطور* - اكتب: م3
{emoji4} *الأعضاء* - اكتب: م4
{emoji5} *الأدوات* - اكتب: م5
{emoji6} *التنزيلات* - اكتب: م6
{emoji7} *الألعاب* - اكتب: م7

💡 *لاستخدام أي أمر، اكتب نقطة (.) قبل الأمر*
مثال: .رفع أو .جوزني

🔗 *للحصول على بوت خاص بك، اكتب: A7A*"""
    
    return menu

def get_groups_menu():
    """قائمة أوامر المجموعات"""
    emoji = get_random_emoji()
    return f"""{emoji} *أوامر المجموعات (م1)*

• *.رفع* - رفع عضو كادمن
• *.خفط* - إزالة عضو من الادمن  
• *.انطر* - طرد عضو من المجموعة
• *.اضافة [الرقم]* - إضافة رقم للمجموعة
• *.تغير نيم [الاسم]* - تغيير اسم المجموعة
• *.منع سب* - تفعيل منع الشتائم

⚠️ *هذه الأوامر للمشرفين فقط*"""

def get_entertainment_menu():
    """قائمة أوامر التسلية"""
    emoji = get_random_emoji()
    return f"""{emoji} *أوامر التسلية (م2)*

• *.جوزني* - اختيار شريك عشوائي للزواج 💍
• *.نسبة جمال* - قياس نسبة الجمال 💄
• *.حب [@منشن]* - قياس نسبة الحب ❤️
• *الكساندر بحبك* - رد صوتي من البوت 🎵

😄 *استمتع بالأوامر الترفيهية!*"""

def get_developer_menu():
    """قائمة معلومات المطور"""
    emoji = get_random_emoji()
    return f"""{emoji} *معلومات المطور (م3)*

👨‍💻 *المطور:* {DEVELOPER_NAME}
📱 *رقم التواصل:* {DEVELOPER_NUMBER}

⚠️ *تحذير: لا تقم بمنشن المطور بدون سبب!*"""

def get_members_menu():
    """قائمة أوامر الأعضاء"""
    emoji = get_random_emoji()
    return f"""{emoji} *أوامر الأعضاء (م4)*

• *.منشن* - منشن جميع أعضاء المجموعة (للادمن فقط)
• *.تطقيم* - صور انمي عشوائية للتطقيم 🎭
• *.بروفايل [@منشن]* - عرض بروفايل العضو 👤

👥 *أوامر خاصة بإدارة الأعضاء*"""

def get_tools_menu():
    """قائمة الأدوات"""
    emoji = get_random_emoji()
    return f"""{emoji} *الأدوات (م5)*

• *.تنزيل [رابط]* - تنزيل من تيك توك/فيسبوك/انستجرام 📥
• *.شغل [اسم الأغنية]* - تشغيل الأغاني 🎵
• *.apk [اسم التطبيق]* - تنزيل التطبيقات 📱
• *.صورة [كلمة البحث]* - البحث عن الصور 🖼️

🛠️ *أدوات مفيدة لجميع الاستخدامات*"""

def get_downloads_menu():
    """قائمة التنزيلات"""
    emoji = get_random_emoji()
    return f"""{emoji} *التنزيلات (م6)*

• *.تنزيل [رابط تيك توك]* - تنزيل فيديو تيك توك
• *.تنزيل [رابط فيسبوك]* - تنزيل فيديو فيسبوك  
• *.تنزيل [رابط انستجرام]* - تنزيل فيديو انستجرام
• *.apk [اسم التطبيق]* - تنزيل ملف APK

📥 *جميع خدمات التنزيل في مكان واحد*"""

def get_games_menu():
    """قائمة الألعاب"""
    emoji = get_random_emoji()
    return f"""{emoji} *الألعاب (م7)*

🚧 *قيد التطوير...*

⏳ *سيتم إضافة ألعاب مثيرة قريباً!*"""

@app.route("/")
def home():
    return jsonify({
        "status": "active",
        "bot_name": "Alexander WhatsApp Bot",
        "developer": DEVELOPER_NAME,
        "contact": DEVELOPER_NUMBER
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    """معالجة الرسائل الواردة من واتساب"""
    try:
        data = request.get_json()
        
        # استخراج معلومات الرسالة
        message = data.get("message", "").strip()
        sender = data.get("sender", "")
        group_id = data.get("group_id", "")
        is_group = data.get("is_group", False)
        
        # معالجة الرسالة
        response = process_message(message, sender, group_id, is_group)
        
        return jsonify({
            "status": "success",
            "response": response
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def process_message(message, sender, group_id, is_group):
    """معالجة الرسائل وإرجاع الرد المناسب"""
    message_lower = message.lower().strip()
    
    # التحقق من كلمة A7A للحصول على كود التحقق
    if message_lower == "a7a":
        return verification_system.create_verification_request(sender)
    
    # عرض القوائم الرئيسية
    if message_lower in ["م1", "المجموعات"]:
        return get_groups_menu()
    elif message_lower in ["م2", "التسلية"]:
        return get_entertainment_menu()
    elif message_lower in ["م3", "المطور"]:
        return get_developer_menu()
    elif message_lower in ["م4", "الأعضاء"]:
        return get_members_menu()
    elif message_lower in ["م5", "الأدوات"]:
        return get_tools_menu()
    elif message_lower in ["م6", "التنزيلات"]:
        return get_downloads_menu()
    elif message_lower in ["م7", "الألعاب"]:
        return get_games_menu()
    
    # معالجة الأوامر التي تبدأ بنقطة
    if message.startswith("."):
        return process_dot_command(message[1:], sender, group_id, is_group)
    
    # رد على منشن المطور
    if DEVELOPER_NUMBER in message:
        return "ليش تمنشن مطوري؟ 🦧🎀"
    
    # رد على اسم البوت
    if "الكساندر بحبك" in message_lower:
        return entertainment_manager.bot_love_response(sender)
    
    # القائمة الرئيسية للرسائل العادية
    if message_lower in ["اوامر", "الاوامر", "القائمة", "مساعدة", "help"]:
        return get_main_menu()
    
    return get_main_menu()

def process_dot_command(command, sender, group_id, is_group):
    """معالجة الأوامر التي تبدأ بنقطة"""
    command_parts = command.split()
    main_command = command_parts[0].lower()
    
    # فحص الرسائل للكلمات المحظورة في المجموعات
    if is_group:
        swear_check = group_manager.check_message_for_swear(command, sender, group_id)
        if swear_check:
            return swear_check
    
    # أوامر المجموعات (م1)
    if main_command in ["رفع", "خفط", "انطر", "اضافة", "تغير", "منع", "منشن", "معلومات"]:
        return group_manager.process_group_command(command, sender, group_id, is_group)
    
    # أوامر التسلية (م2)
    elif main_command in ["جوزني", "نسبة", "حب", "تطقيم", "نكتة"]:
        return entertainment_manager.process_entertainment_command(command, sender, group_id)
    
    # أوامر الأعضاء والأدوات (م4 و م5)
    elif main_command in ["بروفايل", "صورة", "تنزيل", "شغل", "apk"]:
        return tools_manager.process_tools_command(command, sender, group_id)
    
    # أوامر نظام التحقق
    elif main_command == "تحقق":
        if len(command_parts) < 2:
            return "❌ *يرجى إدخال كود التحقق*\nمثال: .تحقق abc123de"
        code = command_parts[1]
        return verification_system.verify_code(sender, code)
    
    elif main_command == "حالة":
        return verification_system.get_verification_status(sender)
    
    elif main_command == "المحققين" and sender == DEVELOPER_NUMBER:
        return verification_system.get_all_verified_users()
    
    else:
        return f"❌ *أمر غير معروف: {main_command}*\n\n💡 *اكتب \'اوامر\' لعرض القائمة الرئيسية*"

@app.route("/qr_code")
def get_qr_code():
    """إرجاع رمز QR كصورة Base64"""
    qr_base64 = qr_manager.get_qr_code_base64()
    return jsonify({"qr_code": qr_base64, "status": qr_manager.get_session_status()})

@app.route("/qr_page")
def qr_page():
    """عرض صفحة الويب لرمز QR"""
    return """<!DOCTYPE html>\n<html lang=\"ar\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>ربط بوت واتساب</title>\n    <style>\n        body {\n            font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif;\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n            justify-content: center;\n            min-height: 100vh;\n            background-color: #f0f2f5;\n            color: #333;\n            margin: 0;\n            padding: 20px;\n            text-align: center;\n        }\n        .container {\n            background-color: #fff;\n            padding: 30px;\n            border-radius: 12px;\n            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);\n            max-width: 500px;\n            width: 100%;\n        }\n        h1 {\n            color: #1a1a1a;\n            margin-bottom: 20px;\n            font-size: 2em;\n        }\n        p {\n            font-size: 1.1em;\n            line-height: 1.6;\n            margin-bottom: 25px;\n        }\n        #qrCodeContainer {\n            margin-top: 20px;\n            margin-bottom: 30px;\n            border: 2px solid #e0e0e0;\n            border-radius: 8px;\n            padding: 10px;\n            background-color: #f9f9f9;\n            display: inline-block;\n        }\n        #qrCodeImage {\n            width: 250px;\n            height: 250px;\n            display: block;\n            margin: 0 auto;\n        }\n        #statusMessage {\n            font-weight: bold;\n            margin-top: 20px;\n            font-size: 1.2em;\n            color: #007bff;\n        }\n        .instructions {\n            text-align: right;\n            margin-top: 30px;\n            padding-top: 20px;\n            border-top: 1px solid #eee;\n        }\n        .instructions ol {\n            list-style-position: inside;\n            padding-right: 0;\n        }\n        .instructions li {\n            margin-bottom: 10px;\n            font-size: 1em;\n        }\n        .footer {\n            margin-top: 40px;\n            font-size: 0.9em;\n            color: #777;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"container\">\n        <h1>ربط بوت واتساب</h1>\n        <p>لمتابعة استخدام بوت واتساب، يرجى مسح رمز QR أدناه باستخدام تطبيق واتساب على هاتفك.</p>\n        \n        <div id=\"qrCodeContainer\">\n            <img id=\"qrCodeImage\" src=\"\" alt=\"رمز QR\">\n        </div>\n        \n        <p id=\"statusMessage\">جاري تحميل رمز QR...</p>\n\n        <div class=\"instructions\">\n            <h2>كيفية الربط:</h2>\n            <ol>\n                <li>افتح تطبيق واتساب على هاتفك.</li>\n                <li>اذهب إلى <strong>الإعدادات</strong> (Settings).</li>\n                <li>اختر <strong>الأجهزة المرتبطة</strong> (Linked Devices).</li>\n                <li>اضغط على <strong>ربط جهاز</strong> (Link a Device).</li>\n                <li>استخدم كاميرا هاتفك لمسح رمز QR الظاهر على هذه الصفحة.</li>\n            </ol>\n        </div>\n    </div>\n    <div class=\"footer\">\n        <p>&copy; 2025 بوت الكساندر. جميع الحقوق محفوظة.</p>\n    </div>\n\n    <script>\n        const qrCodeImage = document.getElementById(\'qrCodeImage\');\n        const statusMessage = document.getElementById(\'statusMessage\');\n
        async function fetchQrCode() {\n            try {\n                const response = await fetch(\'/qr_code\');\n                const data = await response.json();\n                if (data.qr_code) {\n                    qrCodeImage.src = `data:image/png;base64,${data.qr_code}`;\n                    updateStatus(data.status);\n                } else {\n                    statusMessage.textContent = \'خطأ في تحميل رمز QR.\';\n                }\n            } catch (error) {\n                console.error(\'Error fetching QR code:\', error);\n                statusMessage.textContent = \'خطأ في الاتصال بالخادم. يرجى المحاولة لاحقًا.\';\n            }\n        }\n
        function updateStatus(status) {\n            switch (status) {\n                case \'waiting_for_scan\':\n                    statusMessage.textContent = \'الرجاء مسح رمز QR لربط البوت.\';\n                    statusMessage.style.color = \'#007bff\';\n                    break;\n                case \'authenticated\':\n                    statusMessage.textContent = \'تم الربط بنجاح! يمكنك الآن استخدام البوت.\';\n                    statusMessage.style.color = \'#28a745\';\n                    break;\n                case \'disconnected\':\n                    statusMessage.textContent = \'البوت غير متصل. يرجى تحديث الصفحة.\';\n                    statusMessage.style.color = \'#dc3545\';\n                    break;\n                default:\n                    statusMessage.textContent = `الحالة: ${status}`;\n                    statusMessage.style.color = \'#6c757d\';\n            }\n        }\n
        // تحديث رمز QR كل 5 ثوانٍ (يمكن تعديل المدة حسب الحاجة)\n        setInterval(fetchQrCode, 5000);\n        fetchQrCode(); // جلب رمز QR عند تحميل الصفحة لأول مرة\n    </script>\n</body>\n</html>"""

if __name__ == '__main__':
    print("🤖 بوت واتساب الكساندر يعمل الآن...")
    print(f"👨‍💻 المطور: {DEVELOPER_NAME}")
    print(f"📱 رقم المطور: {DEVELOPER_NUMBER}")
    app.run(host=\'0.0.0.0\', port=5000, debug=True)


