#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
أوامر التسلية لبوت واتساب الكساندر
"""

import random
import json
from datetime import datetime

class EntertainmentManager:
    def __init__(self):
        self.marriage_responses = [
            "💍 *ألف مبروك على الجواز!* 🎉",
            "🎊 *عقبال الفرح الحقيقي!* 💒",
            "💕 *دامت بينكم المحبة والسعادة!* 😂🎀",
            "🥳 *مبروك للعروسين!* 👰🤵",
            "🎉 *الف الف مبروك!* 💖"
        ]
        
        self.beauty_comments = [
            "✨ *جمال طبيعي!*",
            "💄 *حلو قوي!*", 
            "🌟 *جميل جداً!*",
            "💎 *جمال نادر!*",
            "🔥 *جمال خرافي!*",
            "😍 *جمال ساحر!*",
            "🌹 *جميل كالوردة!*",
            "⭐ *جمال النجوم!*"
        ]
        
        self.love_comments = [
            "❤️ *حب من أول نظرة!*",
            "💕 *حب حقيقي!*",
            "💖 *قلوب متصلة!*",
            "💘 *حب أبدي!*",
            "💝 *حب صادق!*",
            "💞 *توأم الروح!*",
            "💓 *نبضات الحب!*",
            "💗 *حب كبير!*"
        ]
        
        self.anime_couples = [
            ("🧑‍🦱 *كيريتو*", "👩‍🦱 *أسونا*"),
            ("🧑‍🦰 *ناتسو*", "👱‍♀️ *لوسي*"),
            ("🧑‍🦳 *إيتشيغو*", "🧑‍🦰 *أوريهيمي*"),
            ("🧑‍🦱 *ناروتو*", "👩‍🦱 *هيناتا*"),
            ("🧑‍🦰 *إدوارد*", "👱‍♀️ *وينري*"),
            ("🧑‍🦱 *تانجيرو*", "👩‍🦱 *كانو*"),
            ("🧑‍🦰 *ميليوداس*", "👸 *إليزابيث*"),
            ("🧑‍🦱 *سينكو*", "👩‍🦱 *هولو*")
        ]
    
    def get_marriage_partner(self, user_id, group_members=None):
        """اختيار شريك عشوائي للزواج"""
        if group_members and len(group_members) > 1:
            # اختيار من أعضاء المجموعة
            available_members = [m for m in group_members if m != user_id]
            partner = random.choice(available_members)
        else:
            # اختيار عشوائي
            partner = f"@عضو{random.randint(1, 100)}"
        
        response = random.choice(self.marriage_responses)
        
        marriage_text = f"{response}\n\n"
        marriage_text += f"👰 *العروسة:* @{user_id}\n"
        marriage_text += f"🤵 *العريس:* {partner}\n\n"
        marriage_text += f"{random.choice(self.love_comments)}"
        
        return marriage_text
    
    def calculate_beauty_percentage(self, user_id):
        """حساب نسبة الجمال"""
        # استخدام hash للحصول على نتيجة ثابتة لنفس المستخدم
        random.seed(hash(user_id) % 1000)
        percentage = random.randint(60, 100)  # نسبة إيجابية دائماً
        random.seed()  # إعادة تعيين البذرة
        
        comment = random.choice(self.beauty_comments)
        
        loading_text = "💄 *جاري حساب نسبة الجمال...* ⏳\n"
        loading_text += "▓▓▓▓▓▓▓▓▓▓ 100%\n\n"
        loading_text += f"✨ *نسبة جمالك:* {percentage}%\n"
        loading_text += f"{comment}"
        
        return loading_text
    
    def calculate_love_percentage(self, user1, user2):
        """حساب نسبة الحب بين شخصين"""
        # استخدام hash للحصول على نتيجة ثابتة لنفس الثنائي
        combined = f"{min(user1, user2)}{max(user1, user2)}"
        random.seed(hash(combined) % 1000)
        percentage = random.randint(30, 100)
        random.seed()
        
        comment = random.choice(self.love_comments)
        
        loading_text = "❤️ *جاري حساب نسبة الحب...* ⏳\n"
        loading_text += "💕💕💕💕💕💕💕💕💕💕 100%\n\n"
        loading_text += f"💖 *نسبة الحب بينكم:* {percentage}%\n"
        loading_text += f"👫 *{user1} ❤️ {user2}*\n\n"
        loading_text += f"{comment}"
        
        return loading_text
    
    def get_anime_couple_pics(self):
        """الحصول على صور تطقيم انمي"""
        couple = random.choice(self.anime_couples)
        boy_pic = couple[0]
        girl_pic = couple[1]
        
        result = "🎭 *صور التطقيم الانمي:* 🎭\n\n"
        result += f"👦 *صورة الولد:* {boy_pic}\n"
        result += f"👧 *صورة البنت:* {girl_pic}\n\n"
        result += "💕 *تطقيم جميل! استمتعوا!* ✨"
        
        return result
    
    def bot_love_response(self, user_name="الكساندر"):
        """رد البوت على كلمة الحب"""
        responses = [
            f"🎵 *وأنا كمان بحبك يا {user_name}* 🎵",
            f"❤️ *حبيبي {user_name}، وأنا أحبك أكثر* ❤️",
            f"💖 *{user_name} عزيز على قلبي* 💖",
            f"🥰 *وأنا بحبك أكتر يا {user_name}* 🥰",
            f"💕 *حبك يملأ قلبي يا {user_name}* 💕"
        ]
        
        response = random.choice(responses)
        return f"{response}\n\n🎤 *[مقطع صوتي من البوت]* 🎵"
    
    def get_random_joke(self):
        """نكتة عشوائية"""
        jokes = [
            "😂 *ليش الدجاجة عبرت الشارع؟*\n*عشان توصل للجهة التانية!* 🐔",
            "🤣 *إيه الفرق بين السمك والفراخ؟*\n*السمك بيعوم والفراخ بتطير!* 🐟🐔",
            "😄 *ليش القطة بتنام كتير؟*\n*عشان عندها 9 أرواح تتعب فيهم!* 🐱",
            "😆 *إيه أسرع حاجة في العالم؟*\n*الشائعات!* 📢",
            "🤪 *ليش الموز أصفر؟*\n*عشان مش أخضر!* 🍌"
        ]
        
        return random.choice(jokes)
    
    def process_entertainment_command(self, command, sender, group_id=None):
        """معالجة أوامر التسلية"""
        command_parts = command.split()
        main_command = command_parts[0].lower()
        
        if main_command == "جوزني":
            return self.get_marriage_partner(sender)
        
        elif main_command == "نسبة" and len(command_parts) > 1:
            if command_parts[1] == "جمال":
                return self.calculate_beauty_percentage(sender)
            elif command_parts[1] == "حب" and len(command_parts) > 2:
                target = command_parts[2].replace("@", "")
                return self.calculate_love_percentage(sender, target)
        
        elif main_command == "حب":
            if len(command_parts) < 2:
                return "❌ *يرجى منشن الشخص*\nمثال: .حب @أحمد"
            target = command_parts[1].replace("@", "")
            return self.calculate_love_percentage(sender, target)
        
        elif main_command == "تطقيم":
            return self.get_anime_couple_pics()
        
        elif main_command == "نكتة":
            return self.get_random_joke()
        
        else:
            return f"❌ *أمر غير معروف في التسلية: {main_command}*"

