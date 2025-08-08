#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام التحقق والربط لبوت واتساب الكساندر
يحتوي على نظام A7A للحصول على أكواد التحقق
"""

import random
import string
import json
from datetime import datetime, timedelta

class VerificationSystem:
    def __init__(self):
        self.verification_codes = {}
        self.verified_users = {}
        self.pending_verifications = {}
        
    def generate_verification_code(self):
        """توليد كود تحقق عشوائي"""
        # توليد كود من 8 أحرف وأرقام
        characters = string.ascii_lowercase + string.digits
        code = ''.join(random.choices(characters, k=8))
        return code
    
    def create_verification_request(self, user_id):
        """إنشاء طلب تحقق جديد"""
        code = self.generate_verification_code()
        timestamp = datetime.now()
        
        # حفظ الكود مع معلومات الطلب
        self.verification_codes[user_id] = {
            "code": code,
            "timestamp": timestamp,
            "attempts": 0,
            "verified": False
        }
        
        response = f"🔐 *كود التحقق الخاص بك:* `{code}`\n\n"
        response += f"📱 *استخدم هذا الكود لربط رقمك بالبوت*\n"
        response += f"⏰ *صالح لمدة 24 ساعة*\n"
        response += f"🔢 *الكود مكون من 8 أحرف وأرقام*\n\n"
        response += f"⚠️ *لا تشارك هذا الكود مع أحد*\n"
        response += f"🛡️ *احتفظ به في مكان آمن*"
        
        return response
    
    def verify_code(self, user_id, provided_code):
        """التحقق من صحة الكود"""
        if user_id not in self.verification_codes:
            return "❌ *لم يتم العثور على كود تحقق لهذا الرقم*\n\n💡 *اكتب A7A للحصول على كود جديد*"
        
        user_data = self.verification_codes[user_id]
        
        # التحقق من انتهاء صلاحية الكود (24 ساعة)
        if datetime.now() - user_data["timestamp"] > timedelta(hours=24):
            del self.verification_codes[user_id]
            return "⏰ *انتهت صلاحية الكود*\n\n💡 *اكتب A7A للحصول على كود جديد*"
        
        # التحقق من عدد المحاولات
        if user_data["attempts"] >= 3:
            return "🚫 *تم تجاوز عدد المحاولات المسموحة*\n\n💡 *اكتب A7A للحصول على كود جديد*"
        
        # التحقق من صحة الكود
        if provided_code.lower() == user_data["code"].lower():
            # تم التحقق بنجاح
            user_data["verified"] = True
            self.verified_users[user_id] = {
                "verification_date": datetime.now(),
                "code_used": user_data["code"],
                "status": "verified"
            }
            
            response = f"✅ *تم التحقق بنجاح!* 🎉\n\n"
            response += f"🤖 *تم ربط رقمك بالبوت*\n"
            response += f"📱 *الرقم:* {user_id}\n"
            response += f"🔐 *الكود:* {provided_code}\n"
            response += f"📅 *تاريخ التحقق:* {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            response += f"🎯 *يمكنك الآن استخدام جميع ميزات البوت*"
            
            return response
        else:
            # كود خاطئ
            user_data["attempts"] += 1
            remaining_attempts = 3 - user_data["attempts"]
            
            response = f"❌ *كود خاطئ*\n\n"
            response += f"🔢 *الكود المدخل:* {provided_code}\n"
            response += f"⚠️ *المحاولات المتبقية:* {remaining_attempts}\n\n"
            
            if remaining_attempts > 0:
                response += f"💡 *تأكد من إدخال الكود بشكل صحيح*"
            else:
                response += f"🚫 *تم استنفاد جميع المحاولات*\n💡 *اكتب A7A للحصول على كود جديد*"
            
            return response
    
    def is_verified(self, user_id):
        """التحقق من حالة التحقق للمستخدم"""
        return user_id in self.verified_users
    
    def get_verification_status(self, user_id):
        """الحصول على حالة التحقق"""
        if user_id in self.verified_users:
            user_data = self.verified_users[user_id]
            response = f"✅ *حالة التحقق: مُحقق* ✅\n\n"
            response += f"📱 *الرقم:* {user_id}\n"
            response += f"📅 *تاريخ التحقق:* {user_data['verification_date'].strftime('%Y-%m-%d %H:%M')}\n"
            response += f"🔐 *الكود المستخدم:* {user_data['code_used']}\n\n"
            response += f"🎯 *جميع الميزات متاحة*"
            return response
        
        elif user_id in self.verification_codes:
            user_data = self.verification_codes[user_id]
            time_left = timedelta(hours=24) - (datetime.now() - user_data["timestamp"])
            hours_left = int(time_left.total_seconds() // 3600)
            
            response = f"⏳ *حالة التحقق: في الانتظار* ⏳\n\n"
            response += f"📱 *الرقم:* {user_id}\n"
            response += f"🔐 *الكود:* {user_data['code']}\n"
            response += f"⏰ *الوقت المتبقي:* {hours_left} ساعة\n"
            response += f"🔢 *المحاولات المتبقية:* {3 - user_data['attempts']}\n\n"
            response += f"💡 *أدخل الكود للتحقق*"
            return response
        
        else:
            response = f"❌ *حالة التحقق: غير مُحقق* ❌\n\n"
            response += f"📱 *الرقم:* {user_id}\n"
            response += f"🔐 *لا يوجد كود تحقق*\n\n"
            response += f"💡 *اكتب A7A للحصول على كود التحقق*"
            return response
    
    def get_all_verified_users(self):
        """الحصول على قائمة جميع المستخدمين المحققين"""
        if not self.verified_users:
            return "📊 *لا يوجد مستخدمين محققين حالياً*"
        
        response = f"📊 *قائمة المستخدمين المحققين:* 📊\n\n"
        
        for i, (user_id, data) in enumerate(self.verified_users.items(), 1):
            response += f"{i}. 📱 *{user_id}*\n"
            response += f"   📅 {data['verification_date'].strftime('%Y-%m-%d')}\n\n"
        
        response += f"👥 *إجمالي المستخدمين المحققين:* {len(self.verified_users)}"
        
        return response
    
    def reset_verification(self, user_id):
        """إعادة تعيين التحقق للمستخدم"""
        removed_from_codes = user_id in self.verification_codes
        removed_from_verified = user_id in self.verified_users
        
        if removed_from_codes:
            del self.verification_codes[user_id]
        
        if removed_from_verified:
            del self.verified_users[user_id]
        
        if removed_from_codes or removed_from_verified:
            return f"🔄 *تم إعادة تعيين التحقق للرقم {user_id}*\n\n💡 *يمكن الآن طلب كود تحقق جديد*"
        else:
            return f"❌ *لم يتم العثور على بيانات تحقق للرقم {user_id}*"

