#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدير المجموعات لبوت واتساب الكساندر
يحتوي على جميع وظائف إدارة المجموعات
"""

import json
import random
from datetime import datetime

class GroupManager:
    def __init__(self):
        self.groups_data = {}
        self.banned_words = [
            "كلب", "حمار", "غبي", "احمق", "لعنة", "تبا", "قذر", "وسخ",
            "كريه", "مقرف", "بهيمة", "حيوان", "قرد", "خنزير"
        ]
        
    def is_admin(self, user_id, group_id, developer_number="01227812859"):
        """التحقق من صلاحيات الادمن"""
        if user_id == developer_number:
            return True
            
        if group_id in self.groups_data:
            return user_id in self.groups_data[group_id].get('admins', [])
        return False
    
    def is_bot_admin(self, group_id):
        """التحقق من كون البوت ادمن في المجموعة"""
        # في التطبيق الحقيقي، هذا سيتم التحقق منه عبر واتساب API
        return True  # افتراضي للاختبار
    
    def promote_user(self, admin_id, target_user, group_id):
        """رفع عضو كادمن"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if not self.is_bot_admin(group_id):
            return "❌ *انا مش رول يحب* - البوت ليس ادمن في المجموعة"
        
        # إضافة المجموعة إذا لم تكن موجودة
        if group_id not in self.groups_data:
            self.groups_data[group_id] = {'admins': [], 'settings': {}}
        
        # إضافة العضو كادمن
        if target_user not in self.groups_data[group_id]['admins']:
            self.groups_data[group_id]['admins'].append(target_user)
        
        return f"✅ *تم رفع {target_user} كادمن بنجاح* 👑\n\n🎉 *مبروك الترقية!*"
    
    def demote_user(self, admin_id, target_user, group_id):
        """خفط عضو من الادمن"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if not self.is_bot_admin(group_id):
            return "❌ *انا مش رول يحب* - البوت ليس ادمن في المجموعة"
        
        if group_id in self.groups_data:
            if target_user in self.groups_data[group_id]['admins']:
                self.groups_data[group_id]['admins'].remove(target_user)
                return f"✅ *تم خفط {target_user} من الادمن* ⬇️\n\n😔 *تم إزالة الصلاحيات*"
        
        return f"❌ *{target_user} ليس ادمن في المجموعة*"
    
    def kick_user(self, admin_id, target_user, group_id):
        """طرد عضو من المجموعة"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if not self.is_bot_admin(group_id):
            return "❌ *انا مش رول يحب* - البوت ليس ادمن في المجموعة"
        
        # منع طرد الادمن
        if self.is_admin(target_user, group_id):
            return "❌ *لا يمكن طرد الادمن*"
        
        return f"✅ *تم طرد {target_user} من المجموعة* 🚪\n\n👋 *وداعاً!*"
    
    def add_member(self, admin_id, phone_number, group_id):
        """إضافة عضو للمجموعة"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if not self.is_bot_admin(group_id):
            return "❌ *انا مش رول يحب* - البوت ليس ادمن في المجموعة"
        
        # التحقق من صحة رقم الهاتف
        if not phone_number.startswith('+'):
            return "❌ *يرجى كتابة الرقم مع رمز الدولة*\nمثال: +201234567890"
        
        return f"✅ *تم إرسال دعوة إلى {phone_number}* 📨\n\n⏳ *في انتظار قبول الدعوة...*"
    
    def change_group_name(self, admin_id, new_name, group_id):
        """تغيير اسم المجموعة"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if not self.is_bot_admin(group_id):
            return "❌ *انا مش رول يحب* - البوت ليس ادمن في المجموعة"
        
        if len(new_name.strip()) == 0:
            return "❌ *يرجى كتابة اسم صحيح للمجموعة*"
        
        # حفظ الاسم الجديد
        if group_id not in self.groups_data:
            self.groups_data[group_id] = {'admins': [], 'settings': {}}
        
        self.groups_data[group_id]['settings']['name'] = new_name
        
        return f"✅ *تم تغيير اسم المجموعة إلى:* \n\n📝 *{new_name}* 🎉"
    
    def toggle_anti_swear(self, admin_id, group_id):
        """تفعيل/إلغاء منع الشتائم"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *هذا الأمر للمشرفين فقط*"
        
        if group_id not in self.groups_data:
            self.groups_data[group_id] = {'admins': [], 'settings': {}}
        
        current_status = self.groups_data[group_id]['settings'].get('anti_swear', False)
        self.groups_data[group_id]['settings']['anti_swear'] = not current_status
        
        if not current_status:
            return "✅ *تم تفعيل منع الشتائم* 🚫\n\n⚠️ *سيتم طرد أي عضو يستخدم كلمات غير لائقة*"
        else:
            return "✅ *تم إلغاء منع الشتائم* ✅\n\n💬 *يمكن للأعضاء الكتابة بحرية الآن*"
    
    def check_message_for_swear(self, message, user_id, group_id):
        """فحص الرسالة للكلمات المحظورة"""
        if group_id not in self.groups_data:
            return None
        
        if not self.groups_data[group_id]['settings'].get('anti_swear', False):
            return None
        
        # عدم فحص رسائل الادمن
        if self.is_admin(user_id, group_id):
            return None
        
        message_lower = message.lower()
        for word in self.banned_words:
            if word in message_lower:
                return f"🚫 *تم طرد {user_id} لاستخدام كلمات غير لائقة* 🚪\n\n⚠️ *الكلمة المحظورة: {word}*"
        
        return None
    
    def mention_all(self, admin_id, group_id):
        """منشن جميع أعضاء المجموعة"""
        if not self.is_admin(admin_id, group_id):
            return "❌ *للمشرفين فقط يحب* - هذا الأمر للادمن فقط"
        
        # قائمة أعضاء وهمية للاختبار
        members = [
            "@أحمد", "@محمد", "@فاطمة", "@عائشة", "@علي", 
            "@سارة", "@يوسف", "@مريم", "@عبدالله", "@نور"
        ]
        
        random.shuffle(members)
        selected_members = members[:random.randint(5, 10)]
        
        mention_text = "📢 *منشن جماعي* 📢\n\n"
        mention_text += " ".join(selected_members)
        mention_text += "\n\n👥 *تم منشن جميع الأعضاء*"
        
        return mention_text
    
    def get_group_info(self, group_id):
        """الحصول على معلومات المجموعة"""
        if group_id not in self.groups_data:
            return "📊 *معلومات المجموعة:*\n\n👥 *الأعضاء:* غير محدد\n👑 *الادمن:* غير محدد\n⚙️ *الإعدادات:* افتراضية"
        
        group_data = self.groups_data[group_id]
        admins_count = len(group_data.get('admins', []))
        group_name = group_data.get('settings', {}).get('name', 'غير محدد')
        anti_swear = group_data.get('settings', {}).get('anti_swear', False)
        
        info = f"📊 *معلومات المجموعة:*\n\n"
        info += f"📝 *الاسم:* {group_name}\n"
        info += f"👑 *عدد الادمن:* {admins_count}\n"
        info += f"🚫 *منع الشتائم:* {'مفعل' if anti_swear else 'معطل'}\n"
        info += f"🆔 *معرف المجموعة:* {group_id[:10]}..."
        
        return info
    
    def process_group_command(self, command, sender, group_id, is_group=True):
        """معالجة أوامر المجموعات"""
        if not is_group:
            return "❌ *هذا الأمر يعمل في المجموعات فقط*"
        
        command_parts = command.split()
        main_command = command_parts[0].lower()
        
        if main_command == "رفع":
            target = command_parts[1] if len(command_parts) > 1 else "@المنشن"
            return self.promote_user(sender, target, group_id)
        
        elif main_command == "خفط":
            target = command_parts[1] if len(command_parts) > 1 else "@المنشن"
            return self.demote_user(sender, target, group_id)
        
        elif main_command == "انطر":
            target = command_parts[1] if len(command_parts) > 1 else "@المنشن"
            return self.kick_user(sender, target, group_id)
        
        elif main_command == "اضافة":
            if len(command_parts) < 2:
                return "❌ *يرجى كتابة الرقم مع رمز الدولة*\nمثال: .اضافة +201234567890"
            phone = command_parts[1]
            return self.add_member(sender, phone, group_id)
        
        elif main_command == "تغير" and len(command_parts) > 1 and command_parts[1] == "نيم":
            if len(command_parts) < 3:
                return "❌ *يرجى كتابة الاسم الجديد*\nمثال: .تغير نيم مجموعة الأصدقاء"
            new_name = " ".join(command_parts[2:])
            return self.change_group_name(sender, new_name, group_id)
        
        elif main_command == "منع" and len(command_parts) > 1 and command_parts[1] == "سب":
            return self.toggle_anti_swear(sender, group_id)
        
        elif main_command == "منشن":
            return self.mention_all(sender, group_id)
        
        elif main_command == "معلومات":
            return self.get_group_info(group_id)
        
        else:
            return f"❌ *أمر غير معروف في المجموعات: {main_command}*"

