import asyncio
import logging
import os
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_ID    = 7114761739
VIP_LINK    = "https://t.me/Rebatrix"
FREE_LINK   = "https://t.me/Rebatrix"
TIKTOK_LINK = "https://www.tiktok.com/@iahsansardar"
INSTAGRAM   = "https://www.instagram.com/iahsansardar"
YOUTUBE     = "https://www.youtube.com/@iahsansardar"
FACEBOOK    = "https://www.facebook.com/iahsansardar"
WHATSAPP    = "https://wa.me/923437620668"
VIDEO_FILE_ID = "BAACAgQAAxkBAAEDjVtpws_paY7tuUQgAf7kKerBomBIZQACHiEAAtyEGFJsit78Ft4YhjoE"

SHEET_NAME = "AK Forex Bot Users"

BROKERS = {
    "exness":    {"name": "Exness",     "link": "https://one.exnessonelink.com/a/rebatrix", "code": "rebatrix"},
    "xm":        {"name": "XM",         "link": "https://clicks.pipaffiliates.com/c?c=1116352&l=en&p=1", "code": "VG4RX"},
    "icmarkets": {"name": "IC Markets", "link": None, "code": None},
    "vantage":   {"name": "Vantage",    "link": None, "code": None},
}

logging.basicConfig(level=logging.INFO)
USER = {}
PENDING = {}
USER_LANG = {}  # Store user language preference

# COMPLETE TRANSLATIONS - ALL 6 LANGUAGES
LANGUAGES = {
    "en": {
        "welcome": "Welcome to AK Forex ❤️‍🔥💸\n\nChoose any option from below to start 👇",
        "btn_join_vip": "🚀 I want to join VIP group for free",
        "btn_new_user": "📊 I am new, can I know your trading style?",
        "btn_how_works": "❓ How does it work?",
        "btn_already_member": "✅ Already a member",
        "btn_socials": "🌐 Our Socials",
        "btn_support": "💬 Contact Support",
        "btn_language": "🌍 Change Language",
        "btn_main_menu": "🏠 Main menu",
        "msg_new_user": "👋 Welcome! Great that you are here.\n\nHere are two ways to get started:",
        "btn_tiktok": "🎵 See our TikTok / Trading Style",
        "btn_free_channel": "📢 Join our Free Signals Channel",
        "msg_how_works": "❓ How it works:\n\n1️⃣ Open a trading account with one of our partner brokers using our referral link\n\n2️⃣ Send us your Account ID and Email\n\n3️⃣ We verify your account\n\n4️⃣ You get instant access to the VIP signals group\n\nIt is completely FREE — no subscription, no fees.",
        "btn_join_vip_free": "🚀 Join VIP Free",
        "msg_already_member": "Welcome back!\n\nIf you are having trouble accessing the VIP group or need any help, tap Contact Support below and we will sort it out for you.",
        "btn_contact_support": "💬 Contact Support",
        "msg_socials": "🌐 Follow us on social media!\n\nStay updated with our latest signals, results and trading content",
        "msg_support": "💬 Contact Support\n\nNeed help? Our support team is available on WhatsApp.\n\nTap below to start a chat",
        "btn_whatsapp": "💬 Chat on WhatsApp",
        "msg_setup_step1": "Let's get you set up!\n\nStep 1 — Which broker do you currently trade with?",
        "btn_other_broker": "Other broker",
        "msg_step2_size": "Step 2 — What is your account size?",
        "btn_size_1": "Under $500",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "Step 3 — Which country are you from?",
        "btn_type_country": "🌐 Type my country",
        "msg_type_country": "Type your country name below:",
        "msg_step4_source": "Step 4 — Where did you find us?",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 Friend / Referral",
        "msg_account_format": "Great!\n\nPlease send your Account ID and Email in this format:\n\nAccount ID: 12345678\nEmail: yourname@email.com",
        "msg_change_ib": "🔄 **Change IB to Join VIP**\n\nWhich broker do you currently use?",
        "msg_ib_exness": "🔄 **Keep your Exness Account but Change IB Code**\n\n🔷 **Step 1:** Log in and open Live Chat with Exness Support.\n\n🔷 **Step 2:** Type \"Change partner\" and click the Link they provide.\n❗ Note: Exness may ask you to log in again.\n\n🔷 **Step 3:** Fill in the form with Partner code **1043796384435708709**. Usually got approved in 24 hours or You have to wait up to 3 business days.\n\n🔷 **Step 4:** After Exness confirms the IB code change, **send your MT4/MT5 ID to bot or whatsapp support**.\n\n⚠️ **Important:** Only create your ID after Exness confirms your IB has been changed\n\n**Exness Live Chat:**\nhttps://www.exness.com/support/live-chat/\n\nAfter completing, click below to submit your account details:",
        "btn_ib_changed": "✅ IB Changed - Submit Account Details",
        "btn_need_help": "💬 Need Help?",
        "msg_other_broker": "To get free VIP access you need to trade with one of our partner brokers.\n\nOur partners are:\nExness\nXM\nIC Markets (coming soon)\nVantage (coming soon)\n\nWould you like to open an account with one of them?",
        "btn_open_exness": "Open Exness Account",
        "btn_open_xm": "Open XM Account",
        "msg_coming_soon": " referral link is coming soon!\n\nFor now please sign up with Exness or XM to get instant VIP access.",
        "msg_almost_there": "Almost there!\n\nTo get FREE VIP access, open your {broker} account using our referral link below.\n\nReferral Link: {link}\nPartner Code: {code}\n\nChoose your option:",
        "btn_created_account": "✅ Yes, I have created account using referral link",
        "btn_need_create": "🆕 I need to create new account",
        "btn_change_ib": "🔄 I have account already, Change IB",
        "btn_open_account": "Open {broker} Account",
        "msg_vip_welcome": "🎉 **Perfect! Welcome to VIP!**\n\n📱 **Join Our VIP Signals Group:**\n👇 Click here to join:\n\n{link}\n\n🚀 **You're all set!**\n\nOur signals will be posted in the group.\nFollow them carefully and stick to the rules.\n\n💬 Questions? Reply here anytime!\n📊 Happy trading! Let's make profits together! 💰",
        "msg_app_received": "Application received!\n\nWe will verify your account and send you the VIP group link within 24 hours.\n\nIf you need help in the meantime tap the button below.",
        "msg_type_start": "Type /start to begin",
        "msg_status_waiting": "⏳ **Status:** Waiting for your confirmation\n\nReply YES to get your VIP link!",
        "msg_status_pending": "⏳ **Status:** Application pending\n\nWe're reviewing your application. You'll hear from us within 24 hours!",
        "msg_status_none": "❓ **Status:** No active application\n\nType /start to begin your VIP signup!",
        "msg_help": "🆘 **Help Menu**\n\n**Commands:**\n/start - Start the bot\n/status - Check your application status\n/help - Show this help menu\n\n**Need Support?**\nContact us on WhatsApp for instant help!",
        "msg_approved": "🎉 **Congratulations! You've been approved for VIP access.**\n\nBefore you start trading, there are a few important steps to follow...",
        "msg_tutorial": "📺 **STEP 1: Watch This Tutorial First**\n\n⚠️ **THIS IS REQUIRED** - Do NOT skip!\n\nThis 5-minute video explains:\n✅ How to read our signals\n✅ Entry and exit strategies\n✅ Risk management rules\n✅ How to maximize profits\n✅ Common mistakes to avoid\n\n👇 **Watch now:**",
        "msg_video_caption": "📺 **Watch this tutorial carefully!**",
        "msg_guidelines": "📋 **STEP 2: Read These Guidelines Carefully**\n\n**Risk Management Rules:**\n✅ Never risk more than 2% per trade\n✅ Always set stop loss on every trade\n✅ Take profit at our specified targets\n✅ Don't overtrade - quality over quantity\n\n**Signal Execution:**\n✅ Enter at the price we specify\n✅ Follow our stop loss levels\n✅ Close positions at our targets\n✅ Never average down losing positions\n\n**Important Reminders:**\n⚠️ Only trade during active market hours\n⚠️ Don't use full leverage\n⚠️ Keep emotions out of trading\n⚠️ Never trade if you don't understand the signal",
        "msg_confirm": "✅ **STEP 3: Confirm You're Ready**\n\nBefore I send you the VIP group link, please confirm:\n\n❓ Have you watched the tutorial video?\n❓ Have you read the trading guidelines?\n❓ Do you understand the risk management rules?\n\n**Reply with: YES** (when you're ready)\n\n⚠️ I will only send the VIP link after your confirmation.",
        "msg_rejected": "We could not verify your account.\n\nPlease make sure you signed up using our referral link and try again.\n\nType /start to reapply or tap Contact Support for help.",
    },
    
    "ar": {
        "welcome": "مرحباً بك في AK Forex ❤️‍🔥💸\n\nاختر أي خيار من الأسفل للبدء 👇",
        "btn_join_vip": "🚀 أريد الانضمام إلى مجموعة VIP مجاناً",
        "btn_new_user": "📊 أنا جديد، هل يمكنني معرفة أسلوب التداول الخاص بك؟",
        "btn_how_works": "❓ كيف يعمل؟",
        "btn_already_member": "✅ عضو بالفعل",
        "btn_socials": "🌐 وسائل التواصل الاجتماعي",
        "btn_support": "💬 اتصل بالدعم",
        "btn_language": "🌍 تغيير اللغة",
        "btn_main_menu": "🏠 القائمة الرئيسية",
        "msg_new_user": "👋 مرحباً! سعداء بوجودك هنا.\n\nإليك طريقتان للبدء:",
        "btn_tiktok": "🎵 شاهد TikTok / أسلوب التداول",
        "btn_free_channel": "📢 انضم إلى قناة الإشارات المجانية",
        "msg_how_works": "❓ كيف يعمل:\n\n1️⃣ افتح حساب تداول مع أحد وسطائنا الشركاء باستخدام رابط الإحالة الخاص بنا\n\n2️⃣ أرسل لنا معرف حسابك والبريد الإلكتروني\n\n3️⃣ نتحقق من حسابك\n\n4️⃣ تحصل على وصول فوري إلى مجموعة إشارات VIP\n\nإنه مجاني تماماً — بدون اشتراك، بدون رسوم.",
        "btn_join_vip_free": "🚀 انضم إلى VIP مجاناً",
        "msg_already_member": "مرحباً بعودتك!\n\nإذا كنت تواجه مشكلة في الوصول إلى مجموعة VIP أو تحتاج إلى أي مساعدة، انقر على اتصل بالدعم أدناه وسنحل المشكلة لك.",
        "btn_contact_support": "💬 اتصل بالدعم",
        "msg_socials": "🌐 تابعنا على وسائل التواصل الاجتماعي!\n\nابق على اطلاع بأحدث إشاراتنا ونتائجنا ومحتوى التداول",
        "msg_support": "💬 اتصل بالدعم\n\nتحتاج مساعدة؟ فريق الدعم لدينا متاح على WhatsApp.\n\nانقر أدناه لبدء المحادثة",
        "btn_whatsapp": "💬 دردشة على WhatsApp",
        "msg_setup_step1": "لنبدأ في إعدادك!\n\nالخطوة 1 — أي وسيط تتداول معه حالياً؟",
        "btn_other_broker": "وسيط آخر",
        "msg_step2_size": "الخطوة 2 — ما هو حجم حسابك؟",
        "btn_size_1": "أقل من $500",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "الخطوة 3 — من أي بلد أنت؟",
        "btn_type_country": "🌐 اكتب بلدي",
        "msg_type_country": "اكتب اسم بلدك أدناه:",
        "msg_step4_source": "الخطوة 4 — من أين وجدتنا؟",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 صديق / إحالة",
        "msg_account_format": "عظيم!\n\nيرجى إرسال معرف حسابك والبريد الإلكتروني بهذا التنسيق:\n\nمعرف الحساب: 12345678\nالبريد الإلكتروني: yourname@email.com",
        "msg_change_ib": "🔄 **تغيير IB للانضمام إلى VIP**\n\nأي وسيط تستخدم حالياً؟",
        "msg_ib_exness": "🔄 **احتفظ بحساب Exness الخاص بك ولكن غير رمز IB**\n\n🔷 **الخطوة 1:** قم بتسجيل الدخول وافتح الدردشة المباشرة مع دعم Exness.\n\n🔷 **الخطوة 2:** اكتب \"Change partner\" وانقر على الرابط الذي يقدمونه.\n❗ ملاحظة: قد يطلب منك Exness تسجيل الدخول مرة أخرى.\n\n🔷 **الخطوة 3:** املأ النموذج برمز الشريك **1043796384435708709**. عادة ما تتم الموافقة في 24 ساعة أو عليك الانتظار حتى 3 أيام عمل.\n\n🔷 **الخطوة 4:** بعد أن يؤكد Exness تغيير رمز IB، **أرسل معرف MT4/MT5 الخاص بك إلى البوت أو دعم WhatsApp**.\n\n⚠️ **مهم:** قم بإنشاء معرفك فقط بعد أن يؤكد Exness تغيير IB الخاص بك\n\n**دردشة Exness المباشرة:**\nhttps://www.exness.com/support/live-chat/\n\nبعد الانتهاء، انقر أدناه لإرسال تفاصيل حسابك:",
        "btn_ib_changed": "✅ تم تغيير IB - إرسال تفاصيل الحساب",
        "btn_need_help": "💬 تحتاج مساعدة؟",
        "msg_other_broker": "للحصول على وصول VIP مجاني، تحتاج إلى التداول مع أحد وسطائنا الشركاء.\n\nشركاؤنا هم:\nExness\nXM\nIC Markets (قريباً)\nVantage (قريباً)\n\nهل ترغب في فتح حساب مع أحدهم؟",
        "btn_open_exness": "فتح حساب Exness",
        "btn_open_xm": "فتح حساب XM",
        "msg_coming_soon": " رابط الإحالة قريباً!\n\nفي الوقت الحالي، يرجى التسجيل مع Exness أو XM للحصول على وصول VIP فوري.",
        "msg_almost_there": "تقريباً هناك!\n\nللحصول على وصول VIP مجاني، افتح حساب {broker} الخاص بك باستخدام رابط الإحالة أدناه.\n\nرابط الإحالة: {link}\nرمز الشريك: {code}\n\nاختر خيارك:",
        "btn_created_account": "✅ نعم، لقد أنشأت حساباً باستخدام رابط الإحالة",
        "btn_need_create": "🆕 أحتاج إلى إنشاء حساب جديد",
        "btn_change_ib": "🔄 لدي حساب بالفعل، تغيير IB",
        "btn_open_account": "فتح حساب {broker}",
        "msg_vip_welcome": "🎉 **مثالي! مرحباً بك في VIP!**\n\n📱 **انضم إلى مجموعة إشارات VIP:**\n👇 انقر هنا للانضمام:\n\n{link}\n\n🚀 **كل شيء جاهز!**\n\nسيتم نشر إشاراتنا في المجموعة.\nاتبعها بعناية والتزم بالقواعد.\n\n💬 أسئلة؟ رد هنا في أي وقت!\n📊 تداول سعيد! لنحقق الأرباح معاً! 💰",
        "msg_app_received": "تم استلام الطلب!\n\nسنتحقق من حسابك ونرسل لك رابط مجموعة VIP في غضون 24 ساعة.\n\nإذا كنت بحاجة إلى مساعدة في هذه الأثناء، انقر على الزر أدناه.",
        "msg_type_start": "اكتب /start للبدء",
        "msg_status_waiting": "⏳ **الحالة:** في انتظار تأكيدك\n\nرد بـ YES للحصول على رابط VIP الخاص بك!",
        "msg_status_pending": "⏳ **الحالة:** الطلب قيد الانتظار\n\nنحن نراجع طلبك. ستسمع منا في غضون 24 ساعة!",
        "msg_status_none": "❓ **الحالة:** لا يوجد طلب نشط\n\nاكتب /start لبدء تسجيل VIP الخاص بك!",
        "msg_help": "🆘 **قائمة المساعدة**\n\n**الأوامر:**\n/start - بدء البوت\n/status - تحقق من حالة طلبك\n/help - إظهار قائمة المساعدة\n\n**تحتاج دعم؟**\nاتصل بنا على WhatsApp للحصول على مساعدة فورية!",
        "msg_approved": "🎉 **تهانينا! تمت الموافقة على وصول VIP الخاص بك.**\n\nقبل أن تبدأ التداول، هناك بعض الخطوات المهمة التي يجب اتباعها...",
        "msg_tutorial": "📺 **الخطوة 1: شاهد هذا البرنامج التعليمي أولاً**\n\n⚠️ **هذا مطلوب** - لا تتخطى!\n\nيشرح هذا الفيديو لمدة 5 دقائق:\n✅ كيفية قراءة إشاراتنا\n✅ استراتيجيات الدخول والخروج\n✅ قواعد إدارة المخاطر\n✅ كيفية تعظيم الأرباح\n✅ الأخطاء الشائعة التي يجب تجنبها\n\n👇 **شاهد الآن:**",
        "msg_video_caption": "📺 **شاهد هذا البرنامج التعليمي بعناية!**",
        "msg_guidelines": "📋 **الخطوة 2: اقرأ هذه الإرشادات بعناية**\n\n**قواعد إدارة المخاطر:**\n✅ لا تخاطر أبداً بأكثر من 2٪ لكل صفقة\n✅ قم دائماً بتعيين إيقاف الخسارة في كل صفقة\n✅ خذ الربح عند أهدافنا المحددة\n✅ لا تفرط في التداول - الجودة أكثر من الكمية\n\n**تنفيذ الإشارة:**\n✅ ادخل بالسعر الذي نحدده\n✅ اتبع مستويات وقف الخسارة لدينا\n✅ أغلق المراكز عند أهدافنا\n✅ لا تتوسط أبداً في المراكز الخاسرة\n\n**تذكيرات مهمة:**\n⚠️ تداول فقط خلال ساعات السوق النشطة\n⚠️ لا تستخدم الرافعة المالية الكاملة\n⚠️ أبق العواطف بعيداً عن التداول\n⚠️ لا تتداول أبداً إذا كنت لا تفهم الإشارة",
        "msg_confirm": "✅ **الخطوة 3: أكد أنك مستعد**\n\nقبل أن أرسل لك رابط مجموعة VIP، يرجى التأكيد:\n\n❓ هل شاهدت الفيديو التعليمي؟\n❓ هل قرأت إرشادات التداول؟\n❓ هل تفهم قواعد إدارة المخاطر؟\n\n**رد بـ: YES** (عندما تكون مستعداً)\n\n⚠️ سأرسل رابط VIP فقط بعد تأكيدك.",
        "msg_rejected": "لم نتمكن من التحقق من حسابك.\n\nيرجى التأكد من أنك قمت بالتسجيل باستخدام رابط الإحالة الخاص بنا والمحاولة مرة أخرى.\n\nاكتب /start لإعادة التقديم أو انقر على اتصل بالدعم للحصول على المساعدة.",
    },
    
    "ur": {
        "welcome": "AK Forex میں خوش آمدید ❤️‍🔥💸\n\nشروع کرنے کے لیے نیچے سے کوئی آپشن منتخب کریں 👇",
        "btn_join_vip": "🚀 میں مفت VIP گروپ میں شامل ہونا چاہتا ہوں",
        "btn_new_user": "📊 میں نیا ہوں، کیا میں آپ کا ٹریڈنگ انداز جان سکتا ہوں؟",
        "btn_how_works": "❓ یہ کیسے کام کرتا ہے؟",
        "btn_already_member": "✅ پہلے سے ممبر ہوں",
        "btn_socials": "🌐 ہمارے سوشل میڈیا",
        "btn_support": "💬 سپورٹ سے رابطہ کریں",
        "btn_language": "🌍 زبان تبدیل کریں",
        "btn_main_menu": "🏠 مین مینو",
        "msg_new_user": "👋 خوش آمدید! خوشی ہے کہ آپ یہاں ہیں۔\n\nشروع کرنے کے دو طریقے ہیں:",
        "btn_tiktok": "🎵 ہماری TikTok دیکھیں / ٹریڈنگ اسٹائل",
        "btn_free_channel": "📢 ہمارے مفت سگنل چینل میں شامل ہوں",
        "msg_how_works": "❓ یہ کیسے کام کرتا ہے:\n\n1️⃣ ہمارے پارٹنر بروکرز میں سے کسی ایک کے ساتھ ہمارے ریفرل لنک کا استعمال کرتے ہوئے ٹریڈنگ اکاؤنٹ کھولیں\n\n2️⃣ ہمیں اپنی اکاؤنٹ ID اور ای میل بھیجیں\n\n3️⃣ ہم آپ کے اکاؤنٹ کی تصدیق کریں گے\n\n4️⃣ آپ کو VIP سگنل گروپ تک فوری رسائی ملے گی\n\nیہ بالکل مفت ہے — کوئی سبسکرپشن نہیں، کوئی فیس نہیں۔",
        "btn_join_vip_free": "🚀 مفت VIP میں شامل ہوں",
        "msg_already_member": "واپسی پر خوش آمدید!\n\nاگر آپ کو VIP گروپ تک رسائی میں دشواری ہو رہی ہے یا کسی مدد کی ضرورت ہے، نیچے سپورٹ سے رابطہ کریں پر ٹیپ کریں اور ہم آپ کے لیے مسئلہ حل کریں گے۔",
        "btn_contact_support": "💬 سپورٹ سے رابطہ کریں",
        "msg_socials": "🌐 ہمیں سوشل میڈیا پر فالو کریں!\n\nہمارے تازہ ترین سگنلز، نتائج اور ٹریڈنگ مواد سے اپ ڈیٹ رہیں",
        "msg_support": "💬 سپورٹ سے رابطہ کریں\n\nمدد چاہیے؟ ہماری سپورٹ ٹیم WhatsApp پر دستیاب ہے۔\n\nچیٹ شروع کرنے کے لیے نیچے ٹیپ کریں",
        "btn_whatsapp": "💬 WhatsApp پر چیٹ کریں",
        "msg_setup_step1": "آئیں آپ کو سیٹ اپ کریں!\n\nقدم 1 — آپ فی الحال کس بروکر کے ساتھ تجارت کرتے ہیں؟",
        "btn_other_broker": "دوسرا بروکر",
        "msg_step2_size": "قدم 2 — آپ کے اکاؤنٹ کا سائز کیا ہے؟",
        "btn_size_1": "$500 سے کم",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "قدم 3 — آپ کس ملک سے ہیں؟",
        "btn_type_country": "🌐 اپنا ملک ٹائپ کریں",
        "msg_type_country": "اپنے ملک کا نام نیچے ٹائپ کریں:",
        "msg_step4_source": "قدم 4 — آپ نے ہمیں کہاں سے پایا؟",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 دوست / ریفرل",
        "msg_account_format": "بہترین!\n\nبرائے مہربانی اپنی اکاؤنٹ ID اور ای میل اس فارمیٹ میں بھیجیں:\n\nاکاؤنٹ ID: 12345678\nای میل: yourname@email.com",
        "msg_change_ib": "🔄 **VIP میں شامل ہونے کے لیے IB تبدیل کریں**\n\nآپ فی الحال کس بروکر کا استعمال کرتے ہیں؟",
        "msg_ib_exness": "🔄 **اپنا Exness اکاؤنٹ رکھیں لیکن IB کوڈ تبدیل کریں**\n\n🔷 **قدم 1:** لاگ ان کریں اور Exness سپورٹ کے ساتھ لائیو چیٹ کھولیں۔\n\n🔷 **قدم 2:** \"Change partner\" ٹائپ کریں اور وہ لنک کلک کریں جو وہ فراہم کرتے ہیں۔\n❗ نوٹ: Exness آپ سے دوبارہ لاگ ان کرنے کو کہہ سکتا ہے۔\n\n🔷 **قدم 3:** پارٹنر کوڈ **1043796384435708709** کے ساتھ فارم بھریں۔ عام طور پر 24 گھنٹے میں منظور ہو جاتا ہے یا آپ کو 3 کاروباری دنوں تک انتظار کرنا پڑ سکتا ہے۔\n\n🔷 **قدم 4:** Exness کی IB کوڈ تبدیلی کی تصدیق کے بعد، **اپنی MT4/MT5 ID بوٹ یا WhatsApp سپورٹ کو بھیجیں**۔\n\n⚠️ **اہم:** صرف اس وقت اپنی ID بنائیں جب Exness آپ کے IB کی تبدیلی کی تصدیق کر دے\n\n**Exness لائیو چیٹ:**\nhttps://www.exness.com/support/live-chat/\n\nمکمل کرنے کے بعد، اپنے اکاؤنٹ کی تفصیلات جمع کرانے کے لیے نیچے کلک کریں:",
        "btn_ib_changed": "✅ IB تبدیل ہو گیا - اکاؤنٹ کی تفصیلات جمع کرائیں",
        "btn_need_help": "💬 مدد چاہیے؟",
        "msg_other_broker": "مفت VIP رسائی حاصل کرنے کے لیے آپ کو ہمارے پارٹنر بروکرز میں سے کسی ایک کے ساتھ تجارت کرنے کی ضرورت ہے۔\n\nہمارے پارٹنرز ہیں:\nExness\nXM\nIC Markets (جلد آ رہا ہے)\nVantage (جلد آ رہا ہے)\n\nکیا آپ ان میں سے کسی ایک کے ساتھ اکاؤنٹ کھولنا چاہیں گے؟",
        "btn_open_exness": "Exness اکاؤنٹ کھولیں",
        "btn_open_xm": "XM اکاؤنٹ کھولیں",
        "msg_coming_soon": " ریفرل لنک جلد آ رہا ہے!\n\nفی الحال براہ کرم فوری VIP رسائی کے لیے Exness یا XM کے ساتھ سائن اپ کریں۔",
        "msg_almost_there": "تقریباً ہو گیا!\n\nمفت VIP رسائی حاصل کرنے کے لیے، نیچے ہمارے ریفرل لنک کا استعمال کرتے ہوئے اپنا {broker} اکاؤنٹ کھولیں۔\n\nریفرل لنک: {link}\nپارٹنر کوڈ: {code}\n\nاپنا آپشن منتخب کریں:",
        "btn_created_account": "✅ ہاں، میں نے ریفرل لنک استعمال کرکے اکاؤنٹ بنایا ہے",
        "btn_need_create": "🆕 مجھے نیا اکاؤنٹ بنانے کی ضرورت ہے",
        "btn_change_ib": "🔄 میرے پاس پہلے سے اکاؤنٹ ہے، IB تبدیل کریں",
        "btn_open_account": "{broker} اکاؤنٹ کھولیں",
        "msg_vip_welcome": "🎉 **بہترین! VIP میں خوش آمدید!**\n\n📱 **ہمارے VIP سگنلز گروپ میں شامل ہوں:**\n👇 شامل ہونے کے لیے یہاں کلک کریں:\n\n{link}\n\n🚀 **آپ تیار ہیں!**\n\nہمارے سگنلز گروپ میں پوسٹ کیے جائیں گے۔\nانہیں احتیاط سے فالو کریں اور قواعد پر عمل کریں۔\n\n💬 سوالات؟ کسی بھی وقت یہاں جواب دیں!\n📊 خوش تجارت! آئیں مل کر منافع حاصل کریں! 💰",
        "msg_app_received": "درخواست موصول ہوئی!\n\nہم آپ کے اکاؤنٹ کی تصدیق کریں گے اور 24 گھنٹے کے اندر آپ کو VIP گروپ لنک بھیجیں گے۔\n\nاگر آپ کو اس دوران مدد کی ضرورت ہو تو نیچے بٹن پر ٹیپ کریں۔",
        "msg_type_start": "شروع کرنے کے لیے /start ٹائپ کریں",
        "msg_status_waiting": "⏳ **حیثیت:** آپ کی تصدیق کا انتظار ہے\n\nاپنا VIP لنک حاصل کرنے کے لیے YES کے ساتھ جواب دیں!",
        "msg_status_pending": "⏳ **حیثیت:** درخواست زیر التواء\n\nہم آپ کی درخواست کا جائزہ لے رہے ہیں۔ آپ کو 24 گھنٹے کے اندر ہم سے خبر ملے گی!",
        "msg_status_none": "❓ **حیثیت:** کوئی فعال درخواست نہیں\n\nاپنی VIP سائن اپ شروع کرنے کے لیے /start ٹائپ کریں!",
        "msg_help": "🆘 **مدد کا مینو**\n\n**کمانڈز:**\n/start - بوٹ شروع کریں\n/status - اپنی درخواست کی حیثیت چیک کریں\n/help - یہ مدد کا مینو دکھائیں\n\n**سپورٹ چاہیے؟**\nفوری مدد کے لیے WhatsApp پر ہم سے رابطہ کریں!",
        "msg_approved": "🎉 **مبارک ہو! آپ کی VIP رسائی منظور ہو گئی ہے۔**\n\nتجارت شروع کرنے سے پہلے، کچھ اہم اقدامات ہیں جن پر عمل کرنا ضروری ہے...",
        "msg_tutorial": "📺 **قدم 1: پہلے یہ ٹیوٹوریل دیکھیں**\n\n⚠️ **یہ ضروری ہے** - چھوڑیں نہیں!\n\nیہ 5 منٹ کی ویڈیو بتاتی ہے:\n✅ ہمارے سگنلز کیسے پڑھیں\n✅ داخلے اور خارجے کی حکمت عملی\n✅ خطرے کے انتظام کے قوانین\n✅ منافع کو کیسے زیادہ سے زیادہ کریں\n✅ عام غلطیوں سے بچیں\n\n👇 **ابھی دیکھیں:**",
        "msg_video_caption": "📺 **اس ٹیوٹوریل کو احتیاط سے دیکھیں!**",
        "msg_guidelines": "📋 **قدم 2: ان رہنما خطوط کو احتیاط سے پڑھیں**\n\n**خطرے کے انتظام کے قوانین:**\n✅ ہر تجارت میں 2٪ سے زیادہ خطرہ کبھی نہ لیں\n✅ ہر تجارت پر ہمیشہ اسٹاپ لاس سیٹ کریں\n✅ ہمارے مخصوص اہداف پر منافع لیں\n✅ زیادہ تجارت نہ کریں - مقدار سے زیادہ معیار\n\n**سگنل کا نفاذ:**\n✅ ہماری بتائی ہوئی قیمت پر داخل ہوں\n✅ ہمارے اسٹاپ لاس کی سطح کی پیروی کریں\n✅ ہمارے اہداف پر پوزیشن بند کریں\n✅ کبھی بھی نقصان دہ پوزیشن میں اوسط نہ لیں\n\n**اہم یاد دہانیاں:**\n⚠️ صرف فعال بازار کے اوقات میں تجارت کریں\n⚠️ مکمل لیوریج استعمال نہ کریں\n⚠️ جذبات کو تجارت سے دور رکھیں\n⚠️ اگر آپ سگنل نہیں سمجھتے تو کبھی تجارت نہ کریں",
        "msg_confirm": "✅ **قدم 3: تصدیق کریں کہ آپ تیار ہیں**\n\nمیں آپ کو VIP گروپ لنک بھیجنے سے پہلے، برائے مہربانی تصدیق کریں:\n\n❓ کیا آپ نے ٹیوٹوریل ویڈیو دیکھی ہے؟\n❓ کیا آپ نے تجارتی رہنما خطوط پڑھے ہیں؟\n❓ کیا آپ خطرے کے انتظام کے قوانین سمجھتے ہیں؟\n\n**جواب دیں: YES** (جب آپ تیار ہوں)\n\n⚠️ میں صرف آپ کی تصدیق کے بعد VIP لنک بھیجوں گا۔",
        "msg_rejected": "ہم آپ کے اکاؤنٹ کی تصدیق نہیں کر سکے۔\n\nبرائے مہربانی یقینی بنائیں کہ آپ نے ہمارے ریفرل لنک کا استعمال کرکے سائن اپ کیا ہے اور دوبارہ کوشش کریں۔\n\nدوبارہ درخواست دینے کے لیے /start ٹائپ کریں یا مدد کے لیے سپورٹ سے رابطہ کریں پر ٹیپ کریں۔",
    },

    "fr": {
        "welcome": "Bienvenue chez AK Forex ❤️‍🔥💸\n\nChoisissez une option ci-dessous pour commencer 👇",
        "btn_join_vip": "🚀 Je veux rejoindre le groupe VIP gratuitement",
        "btn_new_user": "📊 Je suis nouveau, puis-je connaître votre style de trading?",
        "btn_how_works": "❓ Comment ça marche?",
        "btn_already_member": "✅ Déjà membre",
        "btn_socials": "🌐 Nos réseaux sociaux",
        "btn_support": "💬 Contacter le support",
        "btn_language": "🌍 Changer de langue",
        "btn_main_menu": "🏠 Menu principal",
        "msg_new_user": "👋 Bienvenue! Ravi que vous soyez ici.\n\nVoici deux façons de commencer:",
        "btn_tiktok": "🎵 Voir notre TikTok / Style de trading",
        "btn_free_channel": "📢 Rejoindre notre chaîne de signaux gratuits",
        "msg_how_works": "❓ Comment ça marche:\n\n1️⃣ Ouvrez un compte de trading avec l'un de nos courtiers partenaires en utilisant notre lien de parrainage\n\n2️⃣ Envoyez-nous votre ID de compte et votre email\n\n3️⃣ Nous vérifions votre compte\n\n4️⃣ Vous obtenez un accès instantané au groupe de signaux VIP\n\nC'est complètement GRATUIT — pas d'abonnement, pas de frais.",
        "btn_join_vip_free": "🚀 Rejoindre VIP gratuitement",
        "msg_already_member": "Bon retour!\n\nSi vous avez des difficultés à accéder au groupe VIP ou si vous avez besoin d'aide, appuyez sur Contacter le support ci-dessous et nous réglerons le problème pour vous.",
        "btn_contact_support": "💬 Contacter le support",
        "msg_socials": "🌐 Suivez-nous sur les réseaux sociaux!\n\nRestez informé de nos derniers signaux, résultats et contenu de trading",
        "msg_support": "💬 Contacter le support\n\nBesoin d'aide? Notre équipe de support est disponible sur WhatsApp.\n\nAppuyez ci-dessous pour démarrer une discussion",
        "btn_whatsapp": "💬 Discuter sur WhatsApp",
        "msg_setup_step1": "Configurons votre compte!\n\nÉtape 1 — Avec quel courtier tradez-vous actuellement?",
        "btn_other_broker": "Autre courtier",
        "msg_step2_size": "Étape 2 — Quelle est la taille de votre compte?",
        "btn_size_1": "Moins de $500",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "Étape 3 — De quel pays êtes-vous?",
        "btn_type_country": "🌐 Tapez mon pays",
        "msg_type_country": "Tapez le nom de votre pays ci-dessous:",
        "msg_step4_source": "Étape 4 — Où nous avez-vous trouvé?",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 Ami / Parrainage",
        "msg_account_format": "Super!\n\nVeuillez envoyer votre ID de compte et votre email dans ce format:\n\nID de compte: 12345678\nEmail: votremail@email.com",
        "msg_change_ib": "🔄 **Changer IB pour rejoindre VIP**\n\nQuel courtier utilisez-vous actuellement?",
        "msg_ib_exness": "🔄 **Gardez votre compte Exness mais changez le code IB**\n\n🔷 **Étape 1:** Connectez-vous et ouvrez le chat en direct avec le support Exness.\n\n🔷 **Étape 2:** Tapez \"Change partner\" et cliquez sur le lien qu'ils fournissent.\n❗ Note: Exness peut vous demander de vous reconnecter.\n\n🔷 **Étape 3:** Remplissez le formulaire avec le code partenaire **1043796384435708709**. Généralement approuvé en 24 heures ou vous devrez attendre jusqu'à 3 jours ouvrables.\n\n🔷 **Étape 4:** Après qu'Exness confirme le changement de code IB, **envoyez votre ID MT4/MT5 au bot ou au support WhatsApp**.\n\n⚠️ **Important:** Créez votre ID uniquement après qu'Exness confirme le changement de votre IB\n\n**Chat en direct Exness:**\nhttps://www.exness.com/support/live-chat/\n\nAprès avoir terminé, cliquez ci-dessous pour soumettre vos détails de compte:",
        "btn_ib_changed": "✅ IB modifié - Soumettre les détails du compte",
        "btn_need_help": "💬 Besoin d'aide?",
        "msg_other_broker": "Pour obtenir un accès VIP gratuit, vous devez trader avec l'un de nos courtiers partenaires.\n\nNos partenaires sont:\nExness\nXM\nIC Markets (bientôt disponible)\nVantage (bientôt disponible)\n\nVoulez-vous ouvrir un compte avec l'un d'eux?",
        "btn_open_exness": "Ouvrir un compte Exness",
        "btn_open_xm": "Ouvrir un compte XM",
        "msg_coming_soon": " lien de parrainage bientôt disponible!\n\nPour l'instant, veuillez vous inscrire avec Exness ou XM pour obtenir un accès VIP instantané.",
        "msg_almost_there": "Presque là!\n\nPour obtenir un accès VIP GRATUIT, ouvrez votre compte {broker} en utilisant notre lien de parrainage ci-dessous.\n\nLien de parrainage: {link}\nCode partenaire: {code}\n\nChoisissez votre option:",
        "btn_created_account": "✅ Oui, j'ai créé un compte en utilisant le lien de parrainage",
        "btn_need_create": "🆕 J'ai besoin de créer un nouveau compte",
        "btn_change_ib": "🔄 J'ai déjà un compte, Changer IB",
        "btn_open_account": "Ouvrir un compte {broker}",
        "msg_vip_welcome": "🎉 **Parfait! Bienvenue dans VIP!**\n\n📱 **Rejoignez notre groupe de signaux VIP:**\n👇 Cliquez ici pour rejoindre:\n\n{link}\n\n🚀 **Vous êtes prêt!**\n\nNos signaux seront publiés dans le groupe.\nSuivez-les attentivement et respectez les règles.\n\n💬 Des questions? Répondez ici à tout moment!\n📊 Bon trading! Faisons des profits ensemble! 💰",
        "msg_app_received": "Demande reçue!\n\nNous vérifierons votre compte et vous enverrons le lien du groupe VIP dans les 24 heures.\n\nSi vous avez besoin d'aide entre-temps, appuyez sur le bouton ci-dessous.",
        "msg_type_start": "Tapez /start pour commencer",
        "msg_status_waiting": "⏳ **Statut:** En attente de votre confirmation\n\nRépondez YES pour obtenir votre lien VIP!",
        "msg_status_pending": "⏳ **Statut:** Demande en attente\n\nNous examinons votre demande. Vous aurez de nos nouvelles dans les 24 heures!",
        "msg_status_none": "❓ **Statut:** Aucune demande active\n\nTapez /start pour commencer votre inscription VIP!",
        "msg_help": "🆘 **Menu d'aide**\n\n**Commandes:**\n/start - Démarrer le bot\n/status - Vérifier le statut de votre demande\n/help - Afficher ce menu d'aide\n\n**Besoin de support?**\nContactez-nous sur WhatsApp pour une aide instantanée!",
        "msg_approved": "🎉 **Félicitations! Vous avez été approuvé pour l'accès VIP.**\n\nAvant de commencer à trader, il y a quelques étapes importantes à suivre...",
        "msg_tutorial": "📺 **ÉTAPE 1: Regardez d'abord ce tutoriel**\n\n⚠️ **CECI EST REQUIS** - Ne sautez pas!\n\nCette vidéo de 5 minutes explique:\n✅ Comment lire nos signaux\n✅ Stratégies d'entrée et de sortie\n✅ Règles de gestion des risques\n✅ Comment maximiser les profits\n✅ Erreurs courantes à éviter\n\n👇 **Regardez maintenant:**",
        "msg_video_caption": "📺 **Regardez ce tutoriel attentivement!**",
        "msg_guidelines": "📋 **ÉTAPE 2: Lisez attentivement ces directives**\n\n**Règles de gestion des risques:**\n✅ Ne risquez jamais plus de 2% par trade\n✅ Définissez toujours un stop loss sur chaque trade\n✅ Prenez vos profits à nos objectifs spécifiés\n✅ Ne sur-tradez pas - qualité plutôt que quantité\n\n**Exécution des signaux:**\n✅ Entrez au prix que nous spécifions\n✅ Suivez nos niveaux de stop loss\n✅ Fermez les positions à nos objectifs\n✅ Ne moyennez jamais les positions perdantes\n\n**Rappels importants:**\n⚠️ Tradez uniquement pendant les heures de marché actives\n⚠️ N'utilisez pas l'effet de levier complet\n⚠️ Gardez les émotions hors du trading\n⚠️ Ne tradez jamais si vous ne comprenez pas le signal",
        "msg_confirm": "✅ **ÉTAPE 3: Confirmez que vous êtes prêt**\n\nAvant de vous envoyer le lien du groupe VIP, veuillez confirmer:\n\n❓ Avez-vous regardé la vidéo tutorielle?\n❓ Avez-vous lu les directives de trading?\n❓ Comprenez-vous les règles de gestion des risques?\n\n**Répondez par: YES** (quand vous êtes prêt)\n\n⚠️ Je n'enverrai le lien VIP qu'après votre confirmation.",
        "msg_rejected": "Nous n'avons pas pu vérifier votre compte.\n\nVeuillez vous assurer que vous vous êtes inscrit en utilisant notre lien de parrainage et réessayez.\n\nTapez /start pour postuler à nouveau ou appuyez sur Contacter le support pour obtenir de l'aide.",
    },

    "es": {
        "welcome": "Bienvenido a AK Forex ❤️‍🔥💸\n\nElige cualquier opción de abajo para comenzar 👇",
        "btn_join_vip": "🚀 Quiero unirme al grupo VIP gratis",
        "btn_new_user": "📊 Soy nuevo, ¿puedo conocer tu estilo de trading?",
        "btn_how_works": "❓ ¿Cómo funciona?",
        "btn_already_member": "✅ Ya soy miembro",
        "btn_socials": "🌐 Nuestras redes sociales",
        "btn_support": "💬 Contactar soporte",
        "btn_language": "🌍 Cambiar idioma",
        "btn_main_menu": "🏠 Menú principal",
        "msg_new_user": "👋 ¡Bienvenido! Me alegra que estés aquí.\n\nAquí hay dos formas de comenzar:",
        "btn_tiktok": "🎵 Ver nuestro TikTok / Estilo de trading",
        "btn_free_channel": "📢 Unirse a nuestro canal de señales gratis",
        "msg_how_works": "❓ Cómo funciona:\n\n1️⃣ Abre una cuenta de trading con uno de nuestros brokers asociados usando nuestro enlace de referido\n\n2️⃣ Envíanos tu ID de cuenta y correo electrónico\n\n3️⃣ Verificamos tu cuenta\n\n4️⃣ Obtienes acceso instantáneo al grupo de señales VIP\n\nEs completamente GRATIS — sin suscripción, sin tarifas.",
        "btn_join_vip_free": "🚀 Unirse a VIP gratis",
        "msg_already_member": "¡Bienvenido de nuevo!\n\nSi tienes problemas para acceder al grupo VIP o necesitas ayuda, toca Contactar soporte abajo y lo resolveremos por ti.",
        "btn_contact_support": "💬 Contactar soporte",
        "msg_socials": "🌐 ¡Síguenos en redes sociales!\n\nMantente actualizado con nuestras últimas señales, resultados y contenido de trading",
        "msg_support": "💬 Contactar soporte\n\n¿Necesitas ayuda? Nuestro equipo de soporte está disponible en WhatsApp.\n\nToca abajo para iniciar un chat",
        "btn_whatsapp": "💬 Chatear en WhatsApp",
        "msg_setup_step1": "¡Configuremos tu cuenta!\n\nPaso 1 — ¿Con qué broker operas actualmente?",
        "btn_other_broker": "Otro broker",
        "msg_step2_size": "Paso 2 — ¿Cuál es el tamaño de tu cuenta?",
        "btn_size_1": "Menos de $500",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "Paso 3 — ¿De qué país eres?",
        "btn_type_country": "🌐 Escribir mi país",
        "msg_type_country": "Escribe el nombre de tu país abajo:",
        "msg_step4_source": "Paso 4 — ¿Dónde nos encontraste?",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 Amigo / Referido",
        "msg_account_format": "¡Genial!\n\nPor favor envía tu ID de cuenta y correo electrónico en este formato:\n\nID de cuenta: 12345678\nCorreo: tunombre@email.com",
        "msg_change_ib": "🔄 **Cambiar IB para unirse a VIP**\n\n¿Qué broker usas actualmente?",
        "msg_ib_exness": "🔄 **Mantén tu cuenta de Exness pero cambia el código IB**\n\n🔷 **Paso 1:** Inicia sesión y abre el chat en vivo con el soporte de Exness.\n\n🔷 **Paso 2:** Escribe \"Change partner\" y haz clic en el enlace que proporcionen.\n❗ Nota: Exness puede pedirte que inicies sesión nuevamente.\n\n🔷 **Paso 3:** Completa el formulario con el código de socio **1043796384435708709**. Usualmente se aprueba en 24 horas o tendrás que esperar hasta 3 días hábiles.\n\n🔷 **Paso 4:** Después de que Exness confirme el cambio de código IB, **envía tu ID MT4/MT5 al bot o al soporte de WhatsApp**.\n\n⚠️ **Importante:** Crea tu ID solo después de que Exness confirme el cambio de tu IB\n\n**Chat en vivo de Exness:**\nhttps://www.exness.com/support/live-chat/\n\nDespués de completar, haz clic abajo para enviar los detalles de tu cuenta:",
        "btn_ib_changed": "✅ IB cambiado - Enviar detalles de cuenta",
        "btn_need_help": "💬 ¿Necesitas ayuda?",
        "msg_other_broker": "Para obtener acceso VIP gratuito, necesitas operar con uno de nuestros brokers asociados.\n\nNuestros socios son:\nExness\nXM\nIC Markets (próximamente)\nVantage (próximamente)\n\n¿Te gustaría abrir una cuenta con uno de ellos?",
        "btn_open_exness": "Abrir cuenta Exness",
        "btn_open_xm": "Abrir cuenta XM",
        "msg_coming_soon": " enlace de referido próximamente!\n\nPor ahora, regístrate con Exness o XM para obtener acceso VIP instantáneo.",
        "msg_almost_there": "¡Casi listo!\n\nPara obtener acceso VIP GRATIS, abre tu cuenta de {broker} usando nuestro enlace de referido abajo.\n\nEnlace de referido: {link}\nCódigo de socio: {code}\n\nElige tu opción:",
        "btn_created_account": "✅ Sí, he creado una cuenta usando el enlace de referido",
        "btn_need_create": "🆕 Necesito crear una cuenta nueva",
        "btn_change_ib": "🔄 Ya tengo una cuenta, Cambiar IB",
        "btn_open_account": "Abrir cuenta {broker}",
        "msg_vip_welcome": "🎉 **¡Perfecto! ¡Bienvenido a VIP!**\n\n📱 **Únete a nuestro grupo de señales VIP:**\n👇 Haz clic aquí para unirte:\n\n{link}\n\n🚀 **¡Todo listo!**\n\nNuestras señales se publicarán en el grupo.\nSíguelas cuidadosamente y cumple con las reglas.\n\n💬 ¿Preguntas? ¡Responde aquí en cualquier momento!\n📊 ¡Feliz trading! ¡Hagamos ganancias juntos! 💰",
        "msg_app_received": "¡Solicitud recibida!\n\nVerificaremos tu cuenta y te enviaremos el enlace del grupo VIP en 24 horas.\n\nSi necesitas ayuda mientras tanto, toca el botón abajo.",
        "msg_type_start": "Escribe /start para comenzar",
        "msg_status_waiting": "⏳ **Estado:** Esperando tu confirmación\n\n¡Responde YES para obtener tu enlace VIP!",
        "msg_status_pending": "⏳ **Estado:** Solicitud pendiente\n\n¡Estamos revisando tu solicitud. Tendrás noticias nuestras en 24 horas!",
        "msg_status_none": "❓ **Estado:** Sin solicitud activa\n\n¡Escribe /start para comenzar tu registro VIP!",
        "msg_help": "🆘 **Menú de ayuda**\n\n**Comandos:**\n/start - Iniciar el bot\n/status - Verificar estado de tu solicitud\n/help - Mostrar este menú de ayuda\n\n**¿Necesitas soporte?**\n¡Contáctanos en WhatsApp para ayuda instantánea!",
        "msg_approved": "🎉 **¡Felicidades! Has sido aprobado para acceso VIP.**\n\nAntes de comenzar a operar, hay algunos pasos importantes a seguir...",
        "msg_tutorial": "📺 **PASO 1: Mira este tutorial primero**\n\n⚠️ **ESTO ES REQUERIDO** - ¡No lo omitas!\n\nEste video de 5 minutos explica:\n✅ Cómo leer nuestras señales\n✅ Estrategias de entrada y salida\n✅ Reglas de gestión de riesgos\n✅ Cómo maximizar ganancias\n✅ Errores comunes a evitar\n\n👇 **Mira ahora:**",
        "msg_video_caption": "📺 **¡Mira este tutorial cuidadosamente!**",
        "msg_guidelines": "📋 **PASO 2: Lee estas directrices cuidadosamente**\n\n**Reglas de gestión de riesgos:**\n✅ Nunca arriesgues más del 2% por operación\n✅ Siempre establece stop loss en cada operación\n✅ Toma ganancias en nuestros objetivos especificados\n✅ No operes en exceso - calidad sobre cantidad\n\n**Ejecución de señales:**\n✅ Entra al precio que especificamos\n✅ Sigue nuestros niveles de stop loss\n✅ Cierra posiciones en nuestros objetivos\n✅ Nunca promedies posiciones perdedoras\n\n**Recordatorios importantes:**\n⚠️ Opera solo durante horas activas del mercado\n⚠️ No uses apalancamiento completo\n⚠️ Mantén las emociones fuera del trading\n⚠️ Nunca operes si no entiendes la señal",
        "msg_confirm": "✅ **PASO 3: Confirma que estás listo**\n\nAntes de enviarte el enlace del grupo VIP, por favor confirma:\n\n❓ ¿Has visto el video tutorial?\n❓ ¿Has leído las directrices de trading?\n❓ ¿Entiendes las reglas de gestión de riesgos?\n\n**Responde con: YES** (cuando estés listo)\n\n⚠️ Solo enviaré el enlace VIP después de tu confirmación.",
        "msg_rejected": "No pudimos verificar tu cuenta.\n\nPor favor asegúrate de que te registraste usando nuestro enlace de referido e inténtalo de nuevo.\n\nEscribe /start para volver a solicitar o toca Contactar soporte para obtener ayuda.",
    },

    "id": {
        "welcome": "Selamat datang di AK Forex ❤️‍🔥💸\n\nPilih opsi di bawah untuk memulai 👇",
        "btn_join_vip": "🚀 Saya ingin bergabung dengan grup VIP gratis",
        "btn_new_user": "📊 Saya baru, bisakah saya mengetahui gaya trading Anda?",
        "btn_how_works": "❓ Bagaimana cara kerjanya?",
        "btn_already_member": "✅ Sudah menjadi anggota",
        "btn_socials": "🌐 Media Sosial Kami",
        "btn_support": "💬 Hubungi Dukungan",
        "btn_language": "🌍 Ubah Bahasa",
        "btn_main_menu": "🏠 Menu utama",
        "msg_new_user": "👋 Selamat datang! Senang Anda di sini.\n\nBerikut dua cara untuk memulai:",
        "btn_tiktok": "🎵 Lihat TikTok kami / Gaya Trading",
        "btn_free_channel": "📢 Bergabung dengan Saluran Sinyal Gratis",
        "msg_how_works": "❓ Cara kerjanya:\n\n1️⃣ Buka akun trading dengan salah satu broker mitra kami menggunakan tautan referral kami\n\n2️⃣ Kirimkan ID akun dan email Anda kepada kami\n\n3️⃣ Kami verifikasi akun Anda\n\n4️⃣ Anda mendapatkan akses instan ke grup sinyal VIP\n\nSepenuhnya GRATIS — tanpa berlangganan, tanpa biaya.",
        "btn_join_vip_free": "🚀 Bergabung VIP Gratis",
        "msg_already_member": "Selamat datang kembali!\n\nJika Anda mengalami masalah mengakses grup VIP atau memerlukan bantuan, ketuk Hubungi Dukungan di bawah dan kami akan menyelesaikannya untuk Anda.",
        "btn_contact_support": "💬 Hubungi Dukungan",
        "msg_socials": "🌐 Ikuti kami di media sosial!\n\nTetap update dengan sinyal terbaru, hasil, dan konten trading kami",
        "msg_support": "💬 Hubungi Dukungan\n\nButuh bantuan? Tim dukungan kami tersedia di WhatsApp.\n\nKetuk di bawah untuk memulai obrolan",
        "btn_whatsapp": "💬 Obrolan di WhatsApp",
        "msg_setup_step1": "Mari siapkan akun Anda!\n\nLangkah 1 — Dengan broker mana Anda saat ini trading?",
        "btn_other_broker": "Broker lain",
        "msg_step2_size": "Langkah 2 — Berapa ukuran akun Anda?",
        "btn_size_1": "Di bawah $500",
        "btn_size_2": "$500 - $2,500",
        "btn_size_3": "$2,500 - $10,000",
        "btn_size_4": "$10,000 - $50,000",
        "btn_size_5": "$50,000+",
        "msg_step3_country": "Langkah 3 — Dari negara mana Anda?",
        "btn_type_country": "🌐 Ketik negara saya",
        "msg_type_country": "Ketik nama negara Anda di bawah:",
        "msg_step4_source": "Langkah 4 — Dari mana Anda menemukan kami?",
        "btn_instagram": "📸 Instagram",
        "btn_telegram": "Telegram",
        "btn_tiktok_short": "🎵 TikTok",
        "btn_youtube": "▶️ YouTube",
        "btn_friend": "👥 Teman / Referral",
        "msg_account_format": "Bagus!\n\nSilakan kirim ID Akun dan Email Anda dalam format ini:\n\nID Akun: 12345678\nEmail: namaemail@email.com",
        "msg_change_ib": "🔄 **Ubah IB untuk Bergabung VIP**\n\nBroker mana yang Anda gunakan saat ini?",
        "msg_ib_exness": "🔄 **Pertahankan Akun Exness Anda tapi Ubah Kode IB**\n\n🔷 **Langkah 1:** Masuk dan buka Live Chat dengan Dukungan Exness.\n\n🔷 **Langkah 2:** Ketik \"Change partner\" dan klik Tautan yang mereka berikan.\n❗ Catatan: Exness mungkin meminta Anda masuk lagi.\n\n🔷 **Langkah 3:** Isi formulir dengan kode mitra **1043796384435708709**. Biasanya disetujui dalam 24 jam atau Anda harus menunggu hingga 3 hari kerja.\n\n🔷 **Langkah 4:** Setelah Exness mengonfirmasi perubahan kode IB, **kirim ID MT4/MT5 Anda ke bot atau dukungan WhatsApp**.\n\n⚠️ **Penting:** Buat ID Anda hanya setelah Exness mengonfirmasi IB Anda telah diubah\n\n**Live Chat Exness:**\nhttps://www.exness.com/support/live-chat/\n\nSetelah selesai, klik di bawah untuk mengirimkan detail akun Anda:",
        "btn_ib_changed": "✅ IB Diubah - Kirim Detail Akun",
        "btn_need_help": "💬 Butuh Bantuan?",
        "msg_other_broker": "Untuk mendapatkan akses VIP gratis, Anda perlu trading dengan salah satu broker mitra kami.\n\nMitra kami adalah:\nExness\nXM\nIC Markets (segera hadir)\nVantage (segera hadir)\n\nApakah Anda ingin membuka akun dengan salah satu dari mereka?",
        "btn_open_exness": "Buka Akun Exness",
        "btn_open_xm": "Buka Akun XM",
        "msg_coming_soon": " tautan referral segera hadir!\n\nUntuk saat ini, silakan daftar dengan Exness atau XM untuk mendapatkan akses VIP instan.",
        "msg_almost_there": "Hampir selesai!\n\nUntuk mendapatkan akses VIP GRATIS, buka akun {broker} Anda menggunakan tautan referral kami di bawah.\n\nTautan Referral: {link}\nKode Mitra: {code}\n\nPilih opsi Anda:",
        "btn_created_account": "✅ Ya, saya telah membuat akun menggunakan tautan referral",
        "btn_need_create": "🆕 Saya perlu membuat akun baru",
        "btn_change_ib": "🔄 Saya sudah punya akun, Ubah IB",
        "btn_open_account": "Buka Akun {broker}",
        "msg_vip_welcome": "🎉 **Sempurna! Selamat datang di VIP!**\n\n📱 **Bergabunglah dengan Grup Sinyal VIP Kami:**\n👇 Klik di sini untuk bergabung:\n\n{link}\n\n🚀 **Semua sudah siap!**\n\nSinyal kami akan diposting di grup.\nIkuti dengan hati-hati dan patuhi aturannya.\n\n💬 Pertanyaan? Balas di sini kapan saja!\n📊 Selamat trading! Mari kita hasilkan profit bersama! 💰",
        "msg_app_received": "Aplikasi diterima!\n\nKami akan memverifikasi akun Anda dan mengirimkan tautan grup VIP dalam 24 jam.\n\nJika Anda memerlukan bantuan sementara itu, ketuk tombol di bawah.",
        "msg_type_start": "Ketik /start untuk memulai",
        "msg_status_waiting": "⏳ **Status:** Menunggu konfirmasi Anda\n\nBalas YES untuk mendapatkan tautan VIP Anda!",
        "msg_status_pending": "⏳ **Status:** Aplikasi tertunda\n\nKami sedang meninjau aplikasi Anda. Anda akan mendengar dari kami dalam 24 jam!",
        "msg_status_none": "❓ **Status:** Tidak ada aplikasi aktif\n\nKetik /start untuk memulai pendaftaran VIP Anda!",
        "msg_help": "🆘 **Menu Bantuan**\n\n**Perintah:**\n/start - Mulai bot\n/status - Periksa status aplikasi Anda\n/help - Tampilkan menu bantuan ini\n\n**Butuh Dukungan?**\nHubungi kami di WhatsApp untuk bantuan instan!",
        "msg_approved": "🎉 **Selamat! Anda telah disetujui untuk akses VIP.**\n\nSebelum Anda mulai trading, ada beberapa langkah penting yang harus diikuti...",
        "msg_tutorial": "📺 **LANGKAH 1: Tonton Tutorial Ini Terlebih Dahulu**\n\n⚠️ **INI WAJIB** - Jangan lewati!\n\nVideo 5 menit ini menjelaskan:\n✅ Cara membaca sinyal kami\n✅ Strategi masuk dan keluar\n✅ Aturan manajemen risiko\n✅ Cara memaksimalkan profit\n✅ Kesalahan umum yang harus dihindari\n\n👇 **Tonton sekarang:**",
        "msg_video_caption": "📺 **Tonton tutorial ini dengan saksama!**",
        "msg_guidelines": "📋 **LANGKAH 2: Baca Panduan Ini Dengan Saksama**\n\n**Aturan Manajemen Risiko:**\n✅ Jangan pernah mengambil risiko lebih dari 2% per perdagangan\n✅ Selalu atur stop loss pada setiap perdagangan\n✅ Ambil profit pada target yang kami tentukan\n✅ Jangan over-trading - kualitas lebih penting daripada kuantitas\n\n**Eksekusi Sinyal:**\n✅ Masuk pada harga yang kami tentukan\n✅ Ikuti level stop loss kami\n✅ Tutup posisi pada target kami\n✅ Jangan pernah rata-rata posisi yang merugi\n\n**Pengingat Penting:**\n⚠️ Hanya trading selama jam pasar aktif\n⚠️ Jangan gunakan leverage penuh\n⚠️ Jauhkan emosi dari trading\n⚠️ Jangan pernah trading jika Anda tidak memahami sinyalnya",
        "msg_confirm": "✅ **LANGKAH 3: Konfirmasi Anda Siap**\n\nSebelum saya mengirimkan tautan grup VIP, harap konfirmasi:\n\n❓ Apakah Anda sudah menonton video tutorial?\n❓ Apakah Anda sudah membaca panduan trading?\n❓ Apakah Anda memahami aturan manajemen risiko?\n\n**Balas dengan: YES** (ketika Anda siap)\n\n⚠️ Saya hanya akan mengirim tautan VIP setelah konfirmasi Anda.",
        "msg_rejected": "Kami tidak dapat memverifikasi akun Anda.\n\nHarap pastikan Anda mendaftar menggunakan tautan referral kami dan coba lagi.\n\nKetik /start untuk mendaftar ulang atau ketuk Hubungi Dukungan untuk bantuan.",
    },
}


def get_sheet():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        return sheet
    except Exception as e:
        logging.error(f"Error connecting to Google Sheets: {e}")
        return None


def save_to_sheet(user_data):
    try:
        sheet = get_sheet()
        if sheet:
            row = [
                user_data.get("date", ""),
                user_data.get("name", ""),
                user_data.get("username", ""),
                user_data.get("user_id", ""),
                user_data.get("broker", ""),
                user_data.get("size", ""),
                user_data.get("country", ""),
                user_data.get("source", ""),
                user_data.get("account_details", ""),
                user_data.get("status", "Pending")
            ]
            sheet.append_row(row)
            logging.info(f"Saved user {user_data.get('user_id')} to Google Sheets")
    except Exception as e:
        logging.error(f"Error saving to sheet: {e}")


def update_sheet_status(user_id, status):
    try:
        sheet = get_sheet()
        if sheet:
            cell = sheet.find(str(user_id))
            if cell:
                sheet.update_cell(cell.row, 10, status)
                logging.info(f"Updated status for user {user_id} to {status}")
    except Exception as e:
        logging.error(f"Error updating sheet: {e}")


def get_text(uid, key):
    lang = USER_LANG.get(uid, "en")
    return LANGUAGES[lang].get(key, LANGUAGES["en"][key])


def language_selector():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
         InlineKeyboardButton("🇸🇦 العربية Arabic", callback_data="lang_ar")],
        [InlineKeyboardButton("🇵🇰 اردو Urdu", callback_data="lang_ur"),
         InlineKeyboardButton("🇫🇷 Français French", callback_data="lang_fr")],
        [InlineKeyboardButton("🇪🇸 Español Spanish", callback_data="lang_es"),
         InlineKeyboardButton("🇮🇩 Indonesia", callback_data="lang_id")],
    ])


def home_markup(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_text(uid, "btn_join_vip"), callback_data="join")],
        [InlineKeyboardButton(get_text(uid, "btn_new_user"), callback_data="new_user")],
        [InlineKeyboardButton(get_text(uid, "btn_how_works"), callback_data="howitworks")],
        [InlineKeyboardButton(get_text(uid, "btn_already_member"), callback_data="already_member")],
        [InlineKeyboardButton(get_text(uid, "btn_socials"), callback_data="socials")],
        [InlineKeyboardButton(get_text(uid, "btn_support"), callback_data="support")],
        [InlineKeyboardButton(get_text(uid, "btn_language"), callback_data="language")],
    ])


async def start(update, context):
    uid = update.effective_user.id
    USER[uid] = {}
    
    # If user hasn't selected language yet, show language selector
    if uid not in USER_LANG:
        await update.message.reply_text(
            "🌍 **Choose your language / اختر لغتك / اپنی زبان منتخب کریں / Choisissez votre langue / Elige tu idioma / Pilih bahasa Anda**",
            reply_markup=language_selector(),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            get_text(uid, "welcome"),
            reply_markup=home_markup(uid)
        )


async def button(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data
    
    if uid not in USER:
        USER[uid] = {}
    u = USER[uid]

    # Language selection
    if data.startswith("lang_"):
        lang = data.replace("lang_", "")
        USER_LANG[uid] = lang
        await q.edit_message_text(
            get_text(uid, "welcome"),
            reply_markup=home_markup(uid)
        )
        return

    if data == "language":
        await q.edit_message_text(
            "🌍 **Choose your language / اختر لغتك / اپنی زبان منتخب کریں / Choisissez votre langue / Elige tu idioma / Pilih bahasa Anda**",
            reply_markup=language_selector(),
            parse_mode='Markdown'
        )
        return

    if data == "home":
        USER[uid] = {}
        await q.edit_message_text(
            get_text(uid, "welcome"),
            reply_markup=home_markup(uid)
        )

    elif data == "new_user":
        await q.edit_message_text(
            get_text(uid, "msg_new_user"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_tiktok"), url=TIKTOK_LINK)],
                [InlineKeyboardButton(get_text(uid, "btn_free_channel"), url=FREE_LINK)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data == "howitworks":
        await q.edit_message_text(
            get_text(uid, "msg_how_works"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_join_vip_free"), callback_data="join")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data == "already_member":
        await q.edit_message_text(
            get_text(uid, "msg_already_member"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_contact_support"), url=WHATSAPP)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data == "socials":
        await q.edit_message_text(
            get_text(uid, "msg_socials"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_tiktok_short"), url=TIKTOK_LINK)],
                [InlineKeyboardButton(get_text(uid, "btn_instagram"), url=INSTAGRAM)],
                [InlineKeyboardButton(get_text(uid, "btn_youtube"), url=YOUTUBE)],
                [InlineKeyboardButton("📘 Facebook", url=FACEBOOK)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data == "support":
        await q.edit_message_text(
            get_text(uid, "msg_support"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_whatsapp"), url=WHATSAPP)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data == "join":
        u["step"] = "broker"
        await q.edit_message_text(
            get_text(uid, "msg_setup_step1"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness", callback_data="br_exness"),
                 InlineKeyboardButton("IC Markets", callback_data="br_icmarkets")],
                [InlineKeyboardButton("XM", callback_data="br_xm"),
                 InlineKeyboardButton("Vantage", callback_data="br_vantage")],
                [InlineKeyboardButton(get_text(uid, "btn_other_broker"), callback_data="br_other")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data.startswith("br_"):
        broker = data.replace("br_", "")
        u["broker"] = broker
        await q.edit_message_text(
            get_text(uid, "msg_step2_size"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_size_1"), callback_data="sz_1")],
                [InlineKeyboardButton(get_text(uid, "btn_size_2"), callback_data="sz_2")],
                [InlineKeyboardButton(get_text(uid, "btn_size_3"), callback_data="sz_3")],
                [InlineKeyboardButton(get_text(uid, "btn_size_4"), callback_data="sz_4")],
                [InlineKeyboardButton(get_text(uid, "btn_size_5"), callback_data="sz_5")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data.startswith("sz_"):
        u["size"] = data.replace("sz_", "")
        await q.edit_message_text(
            get_text(uid, "msg_step3_country"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇦🇪 UAE", callback_data="ct_uae"),
                 InlineKeyboardButton("🇮🇳 India", callback_data="ct_india")],
                [InlineKeyboardButton("🇵🇰 Pakistan", callback_data="ct_pak"),
                 InlineKeyboardButton("🇺🇸 USA", callback_data="ct_usa")],
                [InlineKeyboardButton(get_text(uid, "btn_type_country"), callback_data="ct_type")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data.startswith("ct_"):
        if data == "ct_type":
            u["waiting"] = "country"
            await q.edit_message_text(get_text(uid, "msg_type_country"))
        else:
            cm = {"ct_uae": "UAE", "ct_india": "India", "ct_pak": "Pakistan", "ct_usa": "USA"}
            u["country"] = cm.get(data, "Other")
            await q.edit_message_text(
                get_text(uid, "msg_step4_source"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text(uid, "btn_instagram"), callback_data="src_instagram"),
                     InlineKeyboardButton(get_text(uid, "btn_telegram"), callback_data="src_telegram")],
                    [InlineKeyboardButton(get_text(uid, "btn_tiktok_short"), callback_data="src_tiktok"),
                     InlineKeyboardButton(get_text(uid, "btn_youtube"), callback_data="src_youtube")],
                    [InlineKeyboardButton(get_text(uid, "btn_friend"), callback_data="src_friend")],
                    [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
                ])
            )

    elif data.startswith("src_"):
        source_map = {
            "src_instagram": "Instagram", "src_telegram": "Telegram",
            "src_tiktok": "TikTok", "src_youtube": "YouTube",
            "src_friend": "Friend / Referral",
        }
        u["source"] = source_map.get(data, "Other")
        await _show_broker_step(q.edit_message_text, u, u.get("broker", "exness"), uid)

    elif data == "already_have_account":
        u["waiting"] = "account_details"
        await q.edit_message_text(get_text(uid, "msg_account_format"))

    elif data == "change_ib":
        await q.edit_message_text(
                        get_text(uid, "msg_change_ib"),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness", callback_data="ib_exness")],
                [InlineKeyboardButton("XM", callback_data="ib_xm")],
                [InlineKeyboardButton("IC Markets", callback_data="ib_icmarkets")],
                [InlineKeyboardButton("Vantage", callback_data="ib_vantage")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data.startswith("ib_"):
        broker_ib = data.replace("ib_", "")
        u["broker"] = broker_ib
        
        await q.edit_message_text(
            get_text(uid, "msg_ib_exness"),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_ib_changed"), callback_data="already_have_account")],
                [InlineKeyboardButton(get_text(uid, "btn_need_help"), url=WHATSAPP)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif data.startswith("switch_"):
        broker = data.replace("switch_", "")
        u["broker"] = broker
        await _show_broker_step(q.edit_message_text, u, broker, uid)


async def _show_broker_step(send_fn, u, broker, uid):
    b = BROKERS.get(broker, {})
    broker_name = b.get("name", broker.title())

    if broker == "other":
        await send_fn(
            get_text(uid, "msg_other_broker"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_open_exness"), callback_data="switch_exness")],
                [InlineKeyboardButton(get_text(uid, "btn_open_xm"), callback_data="switch_xm")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )
        return

    if broker in ["icmarkets", "vantage"]:
        await send_fn(
            broker_name + get_text(uid, "msg_coming_soon"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_open_exness"), callback_data="switch_exness")],
                [InlineKeyboardButton(get_text(uid, "btn_open_xm"), callback_data="switch_xm")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )
        return

    link = b.get("link")
    code = b.get("code")
    u["selected_broker"] = broker

    msg = get_text(uid, "msg_almost_there").format(broker=broker_name, link=link, code=code)
    
    await send_fn(
        msg,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(get_text(uid, "btn_created_account"), callback_data="already_have_account")],
            [InlineKeyboardButton(get_text(uid, "btn_need_create"), url=link)],
            [InlineKeyboardButton(get_text(uid, "btn_change_ib"), callback_data="change_ib")],
            [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
        ])
    )


async def message(update, context):
    uid = update.effective_user.id
    text = update.message.text.strip()
    
    if uid not in USER:
        USER[uid] = {}
    u = USER[uid]

    if text.upper() == "YES" and PENDING.get(uid) == "waiting_vip_confirmation":
        vip_msg = get_text(uid, "msg_vip_welcome").format(link=VIP_LINK)
        await context.bot.send_message(
            chat_id=uid,
            text=vip_msg,
            parse_mode='Markdown'
        )
        update_sheet_status(uid, "Approved - VIP Link Sent")
        del PENDING[uid]
        return

    if u.get("waiting") == "country":
        u["country"] = text
        u["waiting"] = None
        await update.message.reply_text(
            get_text(uid, "msg_step4_source"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_instagram"), callback_data="src_instagram"),
                 InlineKeyboardButton(get_text(uid, "btn_telegram"), callback_data="src_telegram")],
                [InlineKeyboardButton(get_text(uid, "btn_tiktok_short"), callback_data="src_tiktok"),
                 InlineKeyboardButton(get_text(uid, "btn_youtube"), callback_data="src_youtube")],
                [InlineKeyboardButton(get_text(uid, "btn_friend"), callback_data="src_friend")],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )

    elif u.get("waiting") == "account_details":
        u["account_details"] = text
        u["waiting"] = None
        user = update.effective_user
        name = user.full_name
        username = "@" + user.username if user.username else "No username"
        broker = u.get("broker", "unknown")
        size_map = {
            "1": "Under $500", "2": "$500 - $2,500",
            "3": "$2,500 - $10,000", "4": "$10,000 - $50,000", "5": "$50,000+",
        }
        size = size_map.get(u.get("size", ""), "Unknown")
        country = u.get("country", "Unknown")
        source = u.get("source", "Unknown")
        broker_name = BROKERS.get(broker, {}).get("name", broker.title())
        PENDING[uid] = u

        # Save to Google Sheets
        user_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "username": username,
            "user_id": uid,
            "broker": broker_name,
            "size": size,
            "country": country,
            "source": source,
            "account_details": text,
            "status": "Pending"
        }
        save_to_sheet(user_data)

        # Admin notification (stays in English)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "NEW VIP APPLICATION\n\n"
                "Name: " + name + "\n"
                "Username: " + username + "\n"
                "User ID: " + str(uid) + "\n"
                "Broker: " + broker_name + "\n"
                "Account size: " + size + "\n"
                "Country: " + country + "\n"
                "Found us via: " + source + "\n\n"
                "Account details:\n" + text + "\n\n"
                "To approve: /approve " + str(uid) + "\n"
                "To reject:  /reject "  + str(uid)
            )
        )

        await update.message.reply_text(
            get_text(uid, "msg_app_received"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(uid, "btn_contact_support"), url=WHATSAPP)],
                [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
            ])
        )
    else:
        await update.message.reply_text(get_text(uid, "msg_type_start"))


async def stats_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    
    total_users = len(USER)
    pending = len([p for p in PENDING.values() if isinstance(p, dict)])
    
    stats_text = (
        f"📊 **Bot Statistics**\n\n"
        f"👥 Total Users: {total_users}\n"
        f"⏳ Pending Applications: {pending}\n"
        f"✅ Approved: {total_users - pending}\n"
    )
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')


async def users_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    
    pending_dict = {k: v for k, v in PENDING.items() if isinstance(v, dict)}
    
    if not pending_dict:
        await update.message.reply_text("No pending applications.")
        return
    
    pending_list = "⏳ **Pending Applications:**\n\n"
    for uid, data in pending_dict.items():
        broker = data.get("broker", "Unknown")
        pending_list += f"• User ID: {uid} - Broker: {broker}\n"
    
    await update.message.reply_text(pending_list, parse_mode='Markdown')


async def broadcast_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: /broadcast Your message here\n\n"
            "This will send the message to all users who started the bot."
        )
        return
    
    message_text = " ".join(context.args)
    sent = 0
    failed = 0
    
    for uid in USER.keys():
        try:
            await context.bot.send_message(chat_id=uid, text=message_text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1
    
    await update.message.reply_text(
        f"✅ Broadcast complete!\n\n"
        f"Sent: {sent}\n"
        f"Failed: {failed}"
    )


async def status_command(update, context):
    uid = update.effective_user.id
    
    if uid in PENDING:
        if PENDING[uid] == "waiting_vip_confirmation":
            status_msg = get_text(uid, "msg_status_waiting")
        else:
            status_msg = get_text(uid, "msg_status_pending")
    else:
        status_msg = get_text(uid, "msg_status_none")
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')


async def help_command(update, context):
    uid = update.effective_user.id
    
    await update.message.reply_text(
        get_text(uid, "msg_help"),
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(get_text(uid, "btn_whatsapp") + " Support", url=WHATSAPP)],
            [InlineKeyboardButton(get_text(uid, "btn_main_menu"), callback_data="home")],
        ])
    )


async def approve(update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /approve [user_id]")
        return
    try:
        target_uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    
    # VIP onboarding in user's language
    await context.bot.send_message(
        chat_id=target_uid,
        text=get_text(target_uid, "msg_approved"),
        parse_mode='Markdown'
    )
    await asyncio.sleep(2)

    await context.bot.send_message(
        chat_id=target_uid,
        text=get_text(target_uid, "msg_tutorial"),
        parse_mode='Markdown'
    )
    await asyncio.sleep(1)

    await context.bot.send_video(
        chat_id=target_uid,
        video=VIDEO_FILE_ID,
        caption=get_text(target_uid, "msg_video_caption"),
        parse_mode='Markdown'
    )
    await asyncio.sleep(3)

    await context.bot.send_message(
        chat_id=target_uid,
        text=get_text(target_uid, "msg_guidelines"),
        parse_mode='Markdown'
    )
    await asyncio.sleep(3)

    await context.bot.send_message(
        chat_id=target_uid,
        text=get_text(target_uid, "msg_confirm"),
        parse_mode='Markdown'
    )

    PENDING[target_uid] = "waiting_vip_confirmation"
    update_sheet_status(target_uid, "Approved - Waiting Confirmation")
    
    await update.message.reply_text("User " + str(target_uid) + " sent VIP onboarding sequence. Waiting for confirmation.")


async def reject(update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /reject [user_id]")
        return
    try:
        target_uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    
    await context.bot.send_message(
        chat_id=target_uid,
        text=get_text(target_uid, "msg_rejected")
    )
    
    update_sheet_status(target_uid, "Rejected")
    
    await update.message.reply_text("User " + str(target_uid) + " rejected.")
    if target_uid in PENDING:
        del PENDING[target_uid]


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("help", help_command))
    
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    
    print("AK Forex bot running with 6 languages...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

