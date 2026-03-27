import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

BOT_TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN")
SIGNUP_LINK = "https://rebatrix.club"
WHATSAPP    = "https://wa.me/PLACEHOLDER"
TELEGRAM_GROUP = "https://t.me/PLACEHOLDER"
TIKTOK      = "https://www.tiktok.com/@PLACEHOLDER"
INSTAGRAM   = "https://www.instagram.com/PLACEHOLDER"
YOUTUBE     = "https://www.youtube.com/@PLACEHOLDER"
VIDEO_URL   = "https://rebatrix.club"

logging.basicConfig(level=logging.INFO)

RATES = {
"exness":    {"std": 6.00, "raw": 3.00},
"icmarkets": {"std": 5.50, "raw": 2.75},
"xm":        {"std": 8.50, "raw": 4.25},
}
BROKERS = [("Exness","exness"),("IC Markets","icmarkets"),("XM","xm")]
BD = {k:n for n,k in BROKERS}
USER = {}

SIZE_MAP = {
"en": {"1":"Under $500","2":"$500 - $2,500","3":"$2,500 - $10,000","4":"$10,000 - $50,000","5":"$50,000 - $1M+"},
"ar": {"1":"أقل من 500$","2":"500$ - 2,500$","3":"2,500$ - 10,000$","4":"10,000$ - 50,000$","5":"50,000$ - 1M$+"},
"id": {"1":"Dibawah $500","2":"$500 - $2,500","3":"$2,500 - $10,000","4":"$10,000 - $50,000","5":"$50,000 - $1 Juta+"},
"ur": {"1":"500$ سے کم","2":"500$ - 2,500$","3":"2,500$ - 10,000$","4":"10,000$ - 50,000$","5":"50,000$ - 1M$+"},
"fr": {"1":"Moins de 500$","2":"500$ - 2 500$","3":"2 500$ - 10 000$","4":"10 000$ - 50 000$","5":"50 000$ - 1M$+"},
}

EST_MAP = {
"en": {"1":"$5-$20","2":"$30-$100","3":"$100-$400","4":"$400-$2,000","5":"$2,000+"},
"ar": {"1":"5$-20$","2":"30$-100$","3":"100$-400$","4":"400$-2,000$","5":"2,000$+"},
"id": {"1":"$5-$20","2":"$30-$100","3":"$100-$400","4":"$400-$2.000","5":"$2.000+"},
"ur": {"1":"$5-$20","2":"$30-$100","3":"$100-$400","4":"$400-$2,000","5":"$2,000+"},
"fr": {"1":"5$-20$","2":"30$-100$","3":"100$-400$","4":"400$-2 000$","5":"2 000$+"},
}

# ── TRANSLATIONS ──────────────────────────────────────────

T = {
"en": {
"welcome": "👋 Welcome to Rebatrix!\n\nEarn cashback on every forex trade — win or lose.\n\nWhat would you like to do?",
"btn_rebates": "💰 What are rebates?",
"btn_start": "✅ I know — lets get started",
"btn_calc": "🧮 Calculate my rebates",
"btn_socials": "🌐 Our Socials",
"btn_support": "💬 Contact Support 24/7",
"btn_home": "🏠 Main menu",
"explain_title": "What are forex rebates?",
"explain_body": "Every time you open a trade, your broker charges you a spread or commission.\n\nRebatrix shares a portion (upto 92%) back with you automatically.\n\nYou trade as normal\nCashback on every trade\nWorks on winning AND losing trades\n\nFree to join. No catch.",
"btn_watch": "▶️ Watch Video",
"btn_got_it": "✅ Got it — lets go",
"socials_title": "Follow us and stay updated!\n\nJoin our Telegram group for giveaways and announcements.",
"btn_telegram": "Telegram Group",
"btn_website": "🌐 Website",
"support_title": "💬 Contact Support 24/7\n\nOur team is available around the clock.",
"btn_whatsapp": "💬 Chat on WhatsApp",
"step1": "Step 1 — Which broker do you trade with?",
"step2": "Step 2 — What is your account size?",
"step3": "Step 3 — How long have you been trading?",
"step3_op1": "Less than 6 months",
"step3_op2": "6 months - 2 years",
"step3_op3": "2+ years",
"step4": "Step 4 — Which country are you from?",
"btn_type_country": "🌐 Type my country",
"type_country": "Type your country name below:",
"step5": "Step 5 — Where did you find us?",
"src1": "Instagram", "src2": "Telegram", "src3": "TikTok", "src4": "YouTube", "src5": "Friend / Referral",
"broker_step_title": "Almost there!\n\nTo get FREE access, open your {broker} account using our referral link.\n\nReferral Link: {link}\nPartner Code: {code}\n\nAlready have an account with {broker} through our referral?",
"btn_already_have": "Yes I already have an account",
"btn_open_broker": "Open {broker} Account",
"other_broker_msg": "Which broker do you use?\n\nJust type the name below:",
"not_partner": "We don’t have a referral partnership with {broker} yet.\n\nOur partners are Exness and XM.\n\nWould you like to open an account with one of them?",
"coming_soon": "{broker} referral link is coming soon!\n\nFor now please sign up with Exness or XM.",
"btn_open_exness": "Open Exness Account",
"btn_open_xm": "Open XM Account",
"account_details_prompt": "Great!\n\nPlease send your Account ID and Email in this format:\n\nAccount ID: 12345678\nEmail: yourname@email.com",
"eligible_title": "You are eligible for Rebatrix!\n\nBroker: {broker}\nAccount size: {size}\nCountry: {country}\nEst. monthly cashback: {est}\n\nWant the exact number? Use the calculator.",
"btn_claim": "🚀 Claim My Rebates — Free",
"btn_calc_exact": "🧮 Calculate exact amount",
"calc_step1": "Rebate Calculator\n\nStep 1 — Which broker do you use for XAUUSD?",
"calc_step2": "Broker: {broker}\n\nStep 2 — Account type?\n\nStandard — wider spread, no commission\nRaw/ECN — tight spread, commission per trade",
"btn_standard": "Standard Account",
"btn_raw": "Raw / ECN Account",
"calc_step3": "{broker} | {label} | ${rate}/lot\n\nStep 3 — How many lots of XAUUSD per day?\n\nCasual: 1 lot\nRegular: 3+ lots\nActive: 7+ lots\n\nType your number below:",
"calc_result": "Here is what you are leaving on the table…\n\nBroker: {broker}\nAccount: {label}\nDaily lots: {d}\nRate: ${rate}/lot\n\nMonthly: ${m} uncollected\nYearly: ${y} uncollected\n\nThat is ${y} every year going to your broker.\n\nSign up free and start collecting it",
"btn_stop_losing": "🚀 Stop leaving money — Join Free",
"btn_calc_again": "🔄 Calculate again",
"app_received": "Application received!\n\nWe will verify your account and send you the link within 24 hours.\n\nIf you need help tap the button below.",
"invalid_lots": "Please enter a valid number like 2 or 0.5",
"fallback": "Type /start to begin",
},

"ar": {
    "welcome": "👋 مرحباً بك في Rebatrix!\n\nاكسب استرداد نقدي على كل صفقة فوركس — ربحت أم خسرت.\n\nماذا تريد أن تفعل؟",
    "btn_rebates": "💰 ما هي الريبيتس؟",
    "btn_start": "✅ أعرف — لنبدأ",
    "btn_calc": "🧮 احسب ريبيتسي",
    "btn_socials": "🌐 تواصل معنا",
    "btn_support": "💬 الدعم 24/7",
    "btn_home": "🏠 القائمة الرئيسية",
    "explain_title": "ما هي ريبيتس الفوركس؟",
    "explain_body": "في كل مرة تفتح فيها صفقة، يكسب وسيطك فارق سعر أو عمولة.\n\nتشارك Rebatrix جزءاً (حتى 92%) معك تلقائياً.\n\nتتداول كالمعتاد\nاسترداد نقدي على كل صفقة\nيعمل على الصفقات الرابحة والخاسرة\n\nمجاني للانضمام. بدون أي خدعة.",
    "btn_watch": "▶️ شاهد الفيديو",
    "btn_got_it": "✅ فهمت — لنبدأ",
    "socials_title": "تابعنا وابق على اطلاع!\n\nانضم لمجموعتنا على تيليجرام للهدايا والإعلانات.",
    "btn_telegram": "مجموعة تيليجرام",
    "btn_website": "🌐 الموقع الإلكتروني",
    "support_title": "💬 الدعم الفني 24/7\n\nفريقنا متاح على مدار الساعة.",
    "btn_whatsapp": "💬 تواصل عبر واتساب",
    "step1": "الخطوة 1 — مع أي وسيط تتداول؟",
    "step2": "الخطوة 2 — ما هو حجم حسابك؟",
    "step3": "الخطوة 3 — منذ متى تتداول؟",
    "step3_op1": "أقل من 6 أشهر",
    "step3_op2": "6 أشهر - سنتان",
    "step3_op3": "أكثر من سنتين",
    "step4": "الخطوة 4 — من أي دولة أنت؟",
    "btn_type_country": "🌐 اكتب بلدك",
    "type_country": "اكتب اسم بلدك أدناه:",
    "step5": "الخطوة 5 — كيف وجدتنا؟",
    "src1": "إنستغرام", "src2": "تيليجرام", "src3": "تيك توك", "src4": "يوتيوب", "src5": "صديق / إحالة",
    "broker_step_title": "أوشكت على الانتهاء!\n\nلتحصل على وصول مجاني، افتح حساب {broker} عبر رابط الإحالة.\n\nرابط الإحالة: {link}\nكود الشريك: {code}\n\nهل لديك حساب {broker} عبر إحالتنا؟",
    "btn_already_have": "نعم، لدي حساب بالفعل",
    "btn_open_broker": "افتح حساب {broker}",
    "other_broker_msg": "ما هو الوسيط الذي تستخدمه؟\n\nاكتب الاسم أدناه:",
    "not_partner": "ليس لدينا شراكة إحالة مع {broker} حتى الآن.\n\nشركاؤنا هم Exness و XM.\n\nهل تريد فتح حساب معهم؟",
    "coming_soon": "رابط إحالة {broker} قادم قريباً!\n\nالآن يرجى التسجيل مع Exness أو XM.",
    "btn_open_exness": "افتح حساب Exness",
    "btn_open_xm": "افتح حساب XM",
    "account_details_prompt": "رائع!\n\nأرسل رقم حسابك وبريدك الإلكتروني بهذا الشكل:\n\nرقم الحساب: 12345678\nالبريد: yourname@email.com",
    "eligible_title": "أنت مؤهل لـ Rebatrix!\n\nالوسيط: {broker}\nحجم الحساب: {size}\nالدولة: {country}\nاسترداد شهري متوقع: {est}\n\nتريد الرقم الدقيق؟ استخدم الحاسبة.",
    "btn_claim": "🚀 احصل على ريبيتسي — مجانا",
    "btn_calc_exact": "🧮 احسب المبلغ الدقيق",
    "calc_step1": "حاسبة الريبيتس\n\nالخطوة 1 — مع أي وسيط تتداول XAUUSD؟",
    "calc_step2": "الوسيط: {broker}\n\nالخطوة 2 — نوع الحساب؟\n\nStandard — فارق سعر أوسع\nRaw/ECN — فارق سعر ضيق + عمولة",
    "btn_standard": "حساب Standard",
    "btn_raw": "حساب Raw / ECN",
    "calc_step3": "{broker} | {label} | ${rate}/لوت\n\nالخطوة 3 — كم لوت تتداول يومياً في XAUUSD؟\n\nمبتدئ: 1 لوت\nمنتظم: 3+ لوت\nنشط: 7+ لوت\n\nاكتب عددك أدناه:",
    "calc_result": "هذا ما تتركه على الطاولة...\n\nالوسيط: {broker}\nالحساب: {label}\nلوتات يومية: {d}\nالمعدل: ${rate}/لوت\n\nشهرياً: ${m} غير محصلة\nسنوياً: ${y} غير محصلة\n\nهذه ${y} سنوياً تذهب لوسيطك.\n\nسجل مجاناً وابدأ بتحصيلها",
    "btn_stop_losing": "🚀 لا تترك أموالك — انضم مجاناً",
    "btn_calc_again": "🔄 احسب مجدداً",
    "app_received": "تم استلام طلبك!\n\nسنتحقق من حسابك ونرسل لك الرابط خلال 24 ساعة.\n\nإذا احتجت مساعدة اضغط الزر أدناه.",
    "invalid_lots": "الرجاء إدخال رقم صحيح مثل 2 أو 0.5",
    "fallback": "اكتب /start للبدء",
},

"id": {
    "welcome": "👋 Selamat datang di Rebatrix!\n\nDapatkan cashback di setiap transaksi forex — menang atau kalah.\n\nApa yang ingin kamu lakukan?",
    "btn_rebates": "💰 Apa itu rebates?",
    "btn_start": "✅ Saya tahu — mari mulai",
    "btn_calc": "🧮 Hitung rebates saya",
    "btn_socials": "🌐 Sosial Media Kami",
    "btn_support": "💬 Hubungi Support 24/7",
    "btn_home": "🏠 Menu utama",
    "explain_title": "Apa itu rebates forex?",
    "explain_body": "Setiap kali kamu membuka transaksi, broker kamu mengambil spread atau komisi.\n\nRebatrix membagikan sebagian (hingga 92%) kembali ke kamu secara otomatis.\n\nKamu trading seperti biasa\nCashback di setiap transaksi\nBerlaku untuk transaksi menang dan kalah\n\nGratis bergabung. Tanpa syarat tersembunyi.",
    "btn_watch": "▶️ Tonton Video",
    "btn_got_it": "✅ Mengerti — mari mulai",
    "socials_title": "Ikuti kami dan tetap update!\n\nGabung grup Telegram kami untuk giveaway dan pengumuman.",
    "btn_telegram": "Grup Telegram",
    "btn_website": "🌐 Website",
    "support_title": "💬 Hubungi Support 24/7\n\nTim kami siap membantu kapan saja.",
    "btn_whatsapp": "💬 Chat di WhatsApp",
    "step1": "Langkah 1 — Broker apa yang kamu gunakan?",
    "step2": "Langkah 2 — Berapa ukuran akun kamu?",
    "step3": "Langkah 3 — Sudah berapa lama kamu trading?",
    "step3_op1": "Kurang dari 6 bulan",
    "step3_op2": "6 bulan - 2 tahun",
    "step3_op3": "Lebih dari 2 tahun",
    "step4": "Langkah 4 — Dari negara mana kamu?",
    "btn_type_country": "🌐 Ketik negara saya",
    "type_country": "Ketik nama negaramu di bawah:",
    "step5": "Langkah 5 — Dari mana kamu tahu kami?",
    "src1": "Instagram", "src2": "Telegram", "src3": "TikTok", "src4": "YouTube", "src5": "Teman / Referral",
    "broker_step_title": "Hampir selesai!\n\nUntuk akses GRATIS, buka akun {broker} menggunakan link referral kami.\n\nLink Referral: {link}\nKode Partner: {code}\n\nSudah punya akun {broker} melalui referral kami?",
    "btn_already_have": "Ya, saya sudah punya akun",
    "btn_open_broker": "Buka Akun {broker}",
    "other_broker_msg": "Broker apa yang kamu gunakan?\n\nKetik namanya di bawah:",
    "not_partner": "Kami belum memiliki kemitraan referral dengan {broker}.\n\nMitra kami adalah Exness dan XM.\n\nMau buka akun di salah satunya?",
    "coming_soon": "Link referral {broker} segera hadir!\n\nUntuk sekarang daftar di Exness atau XM.",
    "btn_open_exness": "Buka Akun Exness",
    "btn_open_xm": "Buka Akun XM",
    "account_details_prompt": "Bagus!\n\nKirimkan ID Akun dan Email kamu dalam format ini:\n\nID Akun: 12345678\nEmail: yourname@email.com",
    "eligible_title": "Kamu memenuhi syarat untuk Rebatrix!\n\nBroker: {broker}\nUkuran akun: {size}\nNegara: {country}\nPerkiraan cashback bulanan: {est}\n\nMau angka pastinya? Gunakan kalkulator.",
    "btn_claim": "🚀 Klaim Rebates Saya — Gratis",
    "btn_calc_exact": "🧮 Hitung jumlah pasti",
    "calc_step1": "Kalkulator Rebates\n\nLangkah 1 — Broker apa yang kamu gunakan untuk XAUUSD?",
    "calc_step2": "Broker: {broker}\n\nLangkah 2 — Tipe akun?\n\nStandard — spread lebih lebar\nRaw/ECN — spread ketat + komisi",
    "btn_standard": "Akun Standard",
    "btn_raw": "Akun Raw / ECN",
    "calc_step3": "{broker} | {label} | ${rate}/lot\n\nLangkah 3 — Berapa lot XAUUSD yang kamu trading per hari?\n\nCasual: 1 lot\nRegular: 3+ lot\nAktif: 7+ lot\n\nKetik angkamu di bawah:",
    "calc_result": "Ini yang kamu tinggalkan begitu saja...\n\nBroker: {broker}\nAkun: {label}\nLot harian: {d}\nRate: ${rate}/lot\n\nBulanan: ${m} tidak terkumpul\nTahunan: ${y} tidak terkumpul\n\nItu ${y} per tahun yang seharusnya kembali ke kamu.\n\nDaftar gratis di Rebatrix dan mulai kumpulkan",
    "btn_stop_losing": "🚀 Jangan biarkan uangmu — Gabung Gratis",
    "btn_calc_again": "🔄 Hitung lagi",
    "app_received": "Aplikasi diterima!\n\nKami akan memverifikasi akun kamu dan mengirim link dalam 24 jam.\n\nJika butuh bantuan tap tombol di bawah.",
    "invalid_lots": "Masukkan angka yang valid seperti 2 atau 0.5",
    "fallback": "Ketik /start untuk mulai",
},

"ur": {
    "welcome": "👋 Rebatrix میں خوش آمدید!\n\nہر فاریکس ٹریڈ پر کیش بیک کمائیں — جیتیں یا ہاریں۔\n\nآپ کیا کرنا چاہتے ہیں؟",
    "btn_rebates": "💰 ریبیٹس کیا ہیں؟",
    "btn_start": "✅ میں جانتا ہوں — شروع کریں",
    "btn_calc": "🧮 میری ریبیٹس حساب کریں",
    "btn_socials": "🌐 ہمارے سوشل میڈیا",
    "btn_support": "💬 سپورٹ 24/7",
    "btn_home": "🏠 مین مینو",
    "explain_title": "فاریکس ریبیٹس کیا ہیں؟",
    "explain_body": "ہر بار جب آپ ٹریڈ کھولتے ہیں، آپ کا بروکر اسپریڈ یا کمیشن کماتا ہے۔\n\nRebatrix اس کا ایک حصہ (92% تک) آپ کو خودکار واپس کرتا ہے۔\n\nآپ معمول کے مطابق ٹریڈ کریں\nہر ٹریڈ پر کیش بیک\nجیتنے اور ہارنے دونوں ٹریڈز پر کام کرتا ہے\n\nشامل ہونا مفت ہے۔ کوئی چھپی شرط نہیں۔",
    "btn_watch": "▶️ ویڈیو دیکھیں",
    "btn_got_it": "✅ سمجھ گیا — آگے بڑھیں",
    "socials_title": "ہمیں فالو کریں اور اپ ڈیٹ رہیں!\n\nگیو اوے اور اعلانات کے لیے ہمارے ٹیلیگرام گروپ میں شامل ہوں۔",
    "btn_telegram": "ٹیلیگرام گروپ",
    "btn_website": "🌐 ویب سائٹ",
    "support_title": "💬 سپورٹ 24/7\n\nہماری ٹیم ہمہ وقت دستیاب ہے۔",
    "btn_whatsapp": "💬 واٹس ایپ پر چیٹ کریں",
    "step1": "مرحلہ 1 — آپ کس بروکر کے ساتھ ٹریڈ کرتے ہیں؟",
    "step2": "مرحلہ 2 — آپ کے اکاؤنٹ کا حجم کیا ہے؟",
    "step3": "مرحلہ 3 — آپ کتنے عرصے سے ٹریڈ کر رہے ہیں؟",
    "step3_op1": "6 مہینے سے کم",
    "step3_op2": "6 مہینے - 2 سال",
    "step3_op3": "2 سال سے زیادہ",
    "step4": "مرحلہ 4 — آپ کس ملک سے ہیں؟",
    "btn_type_country": "🌐 ملک کا نام لکھیں",
    "type_country": "نیچے اپنے ملک کا نام لکھیں:",
    "step5": "مرحلہ 5 — آپ نے ہمیں کہاں سے ڈھونڈا؟",
    "src1": "انسٹاگرام", "src2": "ٹیلیگرام", "src3": "ٹک ٹاک", "src4": "یوٹیوب", "src5": "دوست / ریفرل",
    "broker_step_title": "تقریباً مکمل!\n\nمفت رسائی کے لیے ہمارے ریفرل لنک سے {broker} اکاؤنٹ کھولیں۔\n\nریفرل لنک: {link}\nپارٹنر کوڈ: {code}\n\nکیا آپ کا پہلے سے {broker} اکاؤنٹ ہمارے ریفرل سے ہے؟",
    "btn_already_have": "ہاں، میرا پہلے سے اکاؤنٹ ہے",
    "btn_open_broker": "{broker} اکاؤنٹ کھولیں",
    "other_broker_msg": "آپ کون سا بروکر استعمال کرتے ہیں؟\n\nنام نیچے لکھیں:",
    "not_partner": "ہماری ابھی {broker} کے ساتھ پارٹنرشپ نہیں ہے۔\n\nہمارے پارٹنرز Exness اور XM ہیں۔\n\nکیا آن میں سے کسی کے ساتھ اکاؤنٹ کھولنا چاہتے ہیں؟",
    "coming_soon": "{broker} ریفرل لنک جلد آ رہا ہے!\n\nابھی Exness یا XM سے رجسٹر کریں۔",
    "btn_open_exness": "Exness اکاؤنٹ کھولیں",
    "btn_open_xm": "XM اکاؤنٹ کھولیں",
    "account_details_prompt": "شاندار!\n\nاپنا اکاؤنٹ ID اور ای میل اس فارمیٹ میں بھیجیں:\n\nاکاؤنٹ ID: 12345678\nای میل: yourname@email.com",
    "eligible_title": "آپ Rebatrix کے اہل ہیں!\n\nبروکر: {broker}\nاکاؤنٹ کا حجم: {size}\nملک: {country}\nمتوقع ماہانہ کیش بیک: {est}\n\nصحیح رقم جاننا چاہتے ہیں؟ کیلکولیٹر استعمال کریں۔",
    "btn_claim": "🚀 میری ریبیٹس حاصل کریں — مفت",
    "btn_calc_exact": "🧮 صحیح رقم حساب کریں",
    "calc_step1": "ریبیٹس کیلکولیٹر\n\nمرحلہ 1 — آپ XAUUSD کے لیے کون سا بروکر استعمال کرتے ہیں؟",
    "calc_step2": "بروکر: {broker}\n\nمرحلہ 2 — اکاؤنٹ کی قسم؟\n\nStandard — زیادہ اسپریڈ\nRaw/ECN — کم اسپریڈ + کمیشن",
    "btn_standard": "Standard اکاؤنٹ",
    "btn_raw": "Raw / ECN اکاؤنٹ",
    "calc_step3": "{broker} | {label} | ${rate}/لاٹ\n\nمرحلہ 3 — آپ روزانہ XAUUSD میں کتنے لاٹ ٹریڈ کرتے ہیں؟\n\nمعمولی: 1 لاٹ\nباقاعدہ: 3+ لاٹ\nفعال: 7+ لاٹ\n\nنیچے اپنا نمبر لکھیں:",
    "calc_result": "یہ ہے جو آپ چھوڑ رہے ہیں...\n\nبروکر: {broker}\nاکاؤنٹ: {label}\nروزانہ لاٹ: {d}\nریٹ: ${rate}/لاٹ\n\nماہانہ: ${m} نہیں ملا\nسالانہ: ${y} نہیں ملا\n\nیہ ${y} سالانہ آپ کے بروکر کو جا رہا ہے۔\n\nمفت رجسٹر کریں اور جمع کرنا شروع کریں",
    "btn_stop_losing": "🚀 پیسے ضائع نہ کریں — مفت شامل ہوں",
    "btn_calc_again": "🔄 دوبارہ حساب کریں",
    "app_received": "درخواست موصول ہوئی!\n\nہم 24 گھنٹوں میں آپ کا اکاؤنٹ تصدیق کر کے لنک بھیجیں گے۔\n\nمدد کی ضرورت ہو تو نیچے بٹن دبائیں۔",
    "invalid_lots": "براہ کرم درست نمبر لکھیں جیسے 2 یا 0.5",
    "fallback": "/start لکھ کر شروع کریں",
},

"fr": {
    "welcome": "👋 Bienvenue sur Rebatrix!\n\nGagnez du cashback sur chaque trade forex — gagnant ou perdant.\n\nQue souhaitez-vous faire?",
    "btn_rebates": "💰 Qu'est-ce que les rebates?",
    "btn_start": "✅ Je sais — commençons",
    "btn_calc": "🧮 Calculer mes rebates",
    "btn_socials": "🌐 Nos Réseaux Sociaux",
    "btn_support": "💬 Support 24/7",
    "btn_home": "🏠 Menu principal",
    "explain_title": "Qu'est-ce que les rebates forex?",
    "explain_body": "Chaque fois que vous ouvrez un trade, votre broker prend un spread ou une commission.\n\nRebatrix partage une partie (jusqu'à 92%) avec vous automatiquement.\n\nVous tradez normalement\nCashback sur chaque trade\nFonctionne sur les trades gagnants ET perdants\n\nGratuit. Sans conditions cachées.",
    "btn_watch": "▶️ Regarder la vidéo",
    "btn_got_it": "✅ Compris — allons-y",
    "socials_title": "Suivez-nous et restez informé!\n\nRejoignez notre groupe Telegram pour les cadeaux et annonces.",
    "btn_telegram": "Groupe Telegram",
    "btn_website": "🌐 Site Web",
    "support_title": "💬 Support 24/7\n\nNotre équipe est disponible à toute heure.",
    "btn_whatsapp": "💬 Chatter sur WhatsApp",
    "step1": "Étape 1 — Quel broker utilisez-vous?",
    "step2": "Étape 2 — Quelle est la taille de votre compte?",
    "step3": "Étape 3 — Depuis combien de temps tradez-vous?",
    "step3_op1": "Moins de 6 mois",
    "step3_op2": "6 mois - 2 ans",
    "step3_op3": "Plus de 2 ans",
    "step4": "Étape 4 — De quel pays venez-vous?",
    "btn_type_country": "🌐 Tapez votre pays",
    "type_country": "Tapez le nom de votre pays ci-dessous:",
    "step5": "Étape 5 — Comment nous avez-vous trouvés?",
    "src1": "Instagram", "src2": "Telegram", "src3": "TikTok", "src4": "YouTube", "src5": "Ami / Parrainage",
    "broker_step_title": "Presque terminé!\n\nPour un accès GRATUIT, ouvrez votre compte {broker} via notre lien de parrainage.\n\nLien de parrainage: {link}\nCode partenaire: {code}\n\nVous avez déjà un compte {broker} via notre parrainage?",
    "btn_already_have": "Oui, j'ai déjà un compte",
    "btn_open_broker": "Ouvrir un compte {broker}",
    "other_broker_msg": "Quel broker utilisez-vous?\n\nTapez le nom ci-dessous:",
    "not_partner": "Nous n'avons pas encore de partenariat avec {broker}.\n\nNos partenaires sont Exness et XM.\n\nVoulez-vous ouvrir un compte chez l'un d'eux?",
    "coming_soon": "Le lien de parrainage {broker} arrive bientôt!\n\nPour l'instant inscrivez-vous chez Exness ou XM.",
    "btn_open_exness": "Ouvrir un compte Exness",
    "btn_open_xm": "Ouvrir un compte XM",
    "account_details_prompt": "Super!\n\nEnvoyez votre ID de compte et Email dans ce format:\n\nID Compte: 12345678\nEmail: yourname@email.com",
    "eligible_title": "Vous êtes éligible à Rebatrix!\n\nBroker: {broker}\nTaille du compte: {size}\nPays: {country}\nCashback mensuel estimé: {est}\n\nVoulez-vous le montant exact? Utilisez la calculatrice.",
    "btn_claim": "🚀 Réclamer mes rebates — Gratuit",
    "btn_calc_exact": "🧮 Calculer le montant exact",
    "calc_step1": "Calculatrice de Rebates\n\nÉtape 1 — Quel broker utilisez-vous pour XAUUSD?",
    "calc_step2": "Broker: {broker}\n\nÉtape 2 — Type de compte?\n\nStandard — spread plus large\nRaw/ECN — spread serré + commission",
    "btn_standard": "Compte Standard",
    "btn_raw": "Compte Raw / ECN",
    "calc_step3": "{broker} | {label} | ${rate}/lot\n\nÉtape 3 — Combien de lots XAUUSD tradez-vous par jour?\n\nDébutant: 1 lot\nRégulier: 3+ lots\nActif: 7+ lots\n\nTapez votre nombre ci-dessous:",
    "calc_result": "Voici ce que vous laissez sur la table...\n\nBroker: {broker}\nCompte: {label}\nLots quotidiens: {d}\nTaux: ${rate}/lot\n\nMensuel: ${m} non collecté\nAnnuel: ${y} non collecté\n\nC'est ${y} par an qui va à votre broker.\n\nInscrivez-vous gratuitement et commencez à collecter",
    "btn_stop_losing": "🚀 Arrêtez de perdre de l'argent — Gratuit",
    "btn_calc_again": "🔄 Calculer à nouveau",
    "app_received": "Demande reçue!\n\nNous vérifierons votre compte et vous enverrons le lien dans 24 heures.\n\nSi vous avez besoin d'aide tapez le bouton ci-dessous.",
    "invalid_lots": "Veuillez entrer un nombre valide comme 2 ou 0.5",
    "fallback": "Tapez /start pour commencer",
},

}

def t(uid, key, **kwargs):
    lang = USER.get(uid, {}).get("lang", "en")
    text = T.get(lang, T["en"]).get(key, T["en"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text

def lang_of(uid):
    return USER.get(uid, {}).get("lang", "en")

# ── LANGUAGE SELECTION ────────────────────────────────────

async def start(update, context):
    uid = update.effective_user.id
    USER[uid] = {}
    await update.message.reply_text(
    "🌍 Please select your language / اختر لغتك / Pilih bahasa / زبان منتخب کریں / Choisissez votre langue",
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("🇬🇧 English",    callback_data="lang_en")],
    [InlineKeyboardButton("🇸🇦 العربية",    callback_data="lang_ar")],
    [InlineKeyboardButton("🇮🇩 Indonesian", callback_data="lang_id")],
    [InlineKeyboardButton("🇵🇰 اردو",       callback_data="lang_ur")],
    [InlineKeyboardButton("🇫🇷 Français",   callback_data="lang_fr")],
    ])
    )

async def set_lang(update, context):
    q = update.callback_query
    uid  = q.from_user.id
    lang = q.data.replace("lang_", "")
    if uid not in USER:
        USER[uid] = {}
    USER[uid]["lang"] = lang
    await q.edit_message_text(
    t(uid, "welcome"),
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(t(uid, "btn_rebates"), callback_data="explain")],
    [InlineKeyboardButton(t(uid, "btn_start"),   callback_data="onboard")],
    [InlineKeyboardButton(t(uid, "btn_calc"),    callback_data="calc")],
    [InlineKeyboardButton(t(uid, "btn_socials"), callback_data="socials")],
    [InlineKeyboardButton(t(uid, "btn_support"), callback_data="support")],
    ])
    )

def home_kb(uid):
    return InlineKeyboardMarkup([
    [InlineKeyboardButton(t(uid, "btn_rebates"), callback_data="explain")],
    [InlineKeyboardButton(t(uid, "btn_start"),   callback_data="onboard")],
    [InlineKeyboardButton(t(uid, "btn_calc"),    callback_data="calc")],
    [InlineKeyboardButton(t(uid, "btn_socials"), callback_data="socials")],
    [InlineKeyboardButton(t(uid, "btn_support"), callback_data="support")],
    ])

def back_btn(uid):
    return [InlineKeyboardButton(t(uid, "btn_home"), callback_data="home")]

    # ── BUTTON HANDLER ────────────────────────────────────────

async def button(update, context):
    q = update.callback_query
    await q.answer()
    uid  = q.from_user.id
    data = q.data
    if uid not in USER:
        USER[uid] = {"lang": "en"}
    elif "lang" not in USER[uid]:
        USER[uid]["lang"] = "en"
    u = USER[uid]

    if data.startswith("lang_"):
        await set_lang(update, context)
        return

    if data == "home":
        USER[uid] = {"lang": u.get("lang", "en")}
        await q.edit_message_text(t(uid, "welcome"), reply_markup=home_kb(uid))

    elif data == "explain":
        await q.edit_message_text(
            t(uid, "explain_body"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_watch"),  url=VIDEO_URL)],
                [InlineKeyboardButton(t(uid, "btn_got_it"), callback_data="onboard")],
                [InlineKeyboardButton(t(uid, "btn_calc"),   callback_data="calc")],
                back_btn(uid),
            ])
        )

    elif data == "socials":
        await q.edit_message_text(
            t(uid, "socials_title"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_telegram"), url=TELEGRAM_GROUP)],
                [InlineKeyboardButton("🎵 TikTok",            url=TIKTOK)],
                [InlineKeyboardButton("📸 Instagram",         url=INSTAGRAM)],
                [InlineKeyboardButton("▶️ YouTube",           url=YOUTUBE)],
                [InlineKeyboardButton(t(uid, "btn_website"),  url=SIGNUP_LINK)],
                back_btn(uid),
            ])
        )

    elif data == "support":
        await q.edit_message_text(
            t(uid, "support_title"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_whatsapp"), url=WHATSAPP)],
                back_btn(uid),
            ])
        )

    elif data == "onboard":
        u["flow"] = "onboard"
        kb = [[InlineKeyboardButton(n, callback_data=f"ob_{k}")] for n, k in BROKERS]
        kb.append(back_btn(uid))
        await q.edit_message_text(t(uid, "step1"), reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("ob_"):
        u["broker"] = data.replace("ob_", "")
        lang = lang_of(uid)
        sizes = SIZE_MAP[lang]
        await q.edit_message_text(
            t(uid, "step2"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(sizes["1"], callback_data="os_1")],
                [InlineKeyboardButton(sizes["2"], callback_data="os_2")],
                [InlineKeyboardButton(sizes["3"], callback_data="os_3")],
                [InlineKeyboardButton(sizes["4"], callback_data="os_4")],
                [InlineKeyboardButton(sizes["5"], callback_data="os_5")],
                back_btn(uid),
            ])
        )

    elif data.startswith("os_"):
        u["size"] = data.replace("os_", "")
        await q.edit_message_text(
            t(uid, "step3"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "step3_op1"), callback_data="oe_new")],
                [InlineKeyboardButton(t(uid, "step3_op2"), callback_data="oe_mid")],
                [InlineKeyboardButton(t(uid, "step3_op3"), callback_data="oe_pro")],
                back_btn(uid),
            ])
        )

    elif data.startswith("oe_"):
        u["exp"] = data.replace("oe_", "")
        await q.edit_message_text(
            t(uid, "step4"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇦🇪 UAE",      callback_data="or_uae"),
                 InlineKeyboardButton("🇮🇳 India",    callback_data="or_india")],
                [InlineKeyboardButton("🇵🇰 Pakistan", callback_data="or_pak"),
                 InlineKeyboardButton("🇺🇸 USA",      callback_data="or_usa")],
                [InlineKeyboardButton(t(uid, "btn_type_country"), callback_data="or_type")],
                back_btn(uid),
            ])
        )

    elif data.startswith("or_"):
        if data == "or_type":
            u["waiting"] = "country"
            await q.edit_message_text(t(uid, "type_country"))
        else:
            cm = {"or_uae": "UAE", "or_india": "India", "or_pak": "Pakistan", "or_usa": "USA"}
            u["country"] = cm.get(data, "Other")
            await q.edit_message_text(
                t(uid, "step5"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(t(uid, "src1"), callback_data="src_ig"),
                     InlineKeyboardButton(t(uid, "src2"), callback_data="src_tg")],
                    [InlineKeyboardButton(t(uid, "src3"), callback_data="src_tt"),
                     InlineKeyboardButton(t(uid, "src4"), callback_data="src_yt")],
                    [InlineKeyboardButton(t(uid, "src5"), callback_data="src_fr")],
                    back_btn(uid),
                ])
            )

    elif data.startswith("src_"):
        src_map = {"src_ig": "Instagram", "src_tg": "Telegram", "src_tt": "TikTok", "src_yt": "YouTube", "src_fr": "Friend/Referral"}
        u["source"] = src_map.get(data, "Other")
        await _show_broker_step(q.edit_message_text, uid, u, u.get("broker", "exness"))

    elif data == "already_have_account":
        u["waiting"] = "account_details"
        await q.edit_message_text(t(uid, "account_details_prompt"))

    elif data.startswith("switch_"):
        broker = data.replace("switch_", "")
        u["broker"] = broker
        await _show_broker_step(q.edit_message_text, uid, u, broker)

    elif data == "calc":
        u["flow"] = "calc"
        kb = [[InlineKeyboardButton(n, callback_data=f"cb_{k}")] for n, k in BROKERS]
        kb.append(back_btn(uid))
        await q.edit_message_text(t(uid, "calc_step1"), reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("cb_"):
        u["cb"] = data.replace("cb_", "")
        broker = u["cb"]
        await q.edit_message_text(
            t(uid, "calc_step2", broker=BD.get(broker, broker)),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_standard"), callback_data="ca_std")],
                [InlineKeyboardButton(t(uid, "btn_raw"),      callback_data="ca_raw")],
                back_btn(uid),
            ])
        )

    elif data.startswith("ca_"):
        acc    = data.replace("ca_", "")
        broker = u.get("cb", "exness")
        rate   = RATES.get(broker, {}).get(acc, 3.00)
        u["ca"]      = acc
        u["rate"]    = rate
        u["waiting"] = "lots"
        label = "Raw/ECN" if acc == "raw" else "Standard"
        await q.edit_message_text(
            t(uid, "calc_step3", broker=BD.get(broker, broker), label=label, rate=rate)
        )

async def _show_broker_step(send_fn, uid, u, broker):
    b           = dict(zip(["exness","icmarkets","xm"], [{"name":"Exness","link":"https://one.exnessonelink.com/a/rebatrix","code":"rebatrix"},{"name":"IC Markets","link":None,"code":None},{"name":"XM","link":"https://clicks.pipaffiliates.com/c?c=1116352&l=en&p=1","code":"VG4RX"}])).get(broker, {})
    broker_name = b.get("name", broker.title())

    if broker == "other":
        u["waiting"] = "other_broker"
        await send_fn(t(uid, "other_broker_msg"))
        return

    if broker in ["icmarkets"]:
        await send_fn(
            t(uid, "coming_soon", broker=broker_name),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_open_exness"), callback_data="switch_exness")],
                [InlineKeyboardButton(t(uid, "btn_open_xm"),     callback_data="switch_xm")],
                [InlineKeyboardButton(t(uid, "btn_home"),        callback_data="home")],
            ])
        )
        return

    link = b.get("link")
    code = b.get("code")
    u["selected_broker"] = broker

    await send_fn(
        t(uid, "broker_step_title", broker=broker_name, link=str(link), code=str(code)),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid, "btn_already_have"),                     callback_data="already_have_account")],
            [InlineKeyboardButton(t(uid, "btn_open_broker", broker=broker_name),  url=link)],
            [InlineKeyboardButton(t(uid, "btn_home"),                             callback_data="home")],
        ])
    )

    # ── MESSAGE HANDLER ───────────────────────────────────────

async def message(update, context):
    uid  = update.effective_user.id
    text = update.message.text.strip()
    if uid not in USER:
        USER[uid] = {"lang": "en"}
    elif "lang" not in USER[uid]:
        USER[uid]["lang"] = "en"
    u = USER[uid]

    if u.get("waiting") == "country":
        u["country"] = text
        u["waiting"] = None
        await update.message.reply_text(
            t(uid, "step5"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "src1"), callback_data="src_ig"),
                 InlineKeyboardButton(t(uid, "src2"), callback_data="src_tg")],
                [InlineKeyboardButton(t(uid, "src3"), callback_data="src_tt"),
                 InlineKeyboardButton(t(uid, "src4"), callback_data="src_yt")],
                [InlineKeyboardButton(t(uid, "src5"), callback_data="src_fr")],
                back_btn(uid),
            ])
        )

    elif u.get("waiting") == "other_broker":
        u["broker_custom"] = text
        u["waiting"] = None
        await update.message.reply_text(
            t(uid, "not_partner", broker=text),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_open_exness"), callback_data="switch_exness")],
                [InlineKeyboardButton(t(uid, "btn_open_xm"),     callback_data="switch_xm")],
                [InlineKeyboardButton(t(uid, "btn_home"),        callback_data="home")],
            ])
        )

    elif u.get("waiting") == "account_details":
        u["account_details"] = text
        u["waiting"] = None
        user        = update.effective_user
        name        = user.full_name
        username    = "@" + user.username if user.username else "No username"
        broker      = u.get("broker", "unknown")
        lang        = lang_of(uid)
        size        = SIZE_MAP[lang].get(u.get("size", ""), "Unknown")
        country     = u.get("country", "Unknown")
        source      = u.get("source", "Unknown")
        broker_name = BD.get(broker, broker.title())

        try:
            await context.bot.send_message(
                chat_id=7114761739,
                text=(
                    "NEW VIP APPLICATION\n\n"
                    "Name: " + name + "\n"
                    "Username: " + username + "\n"
                    "User ID: " + str(uid) + "\n"
                    "Language: " + lang.upper() + "\n"
                    "Broker: " + broker_name + "\n"
                    "Account size: " + size + "\n"
                    "Country: " + country + "\n"
                    "Found us via: " + source + "\n\n"
                    "Account details:\n" + text + "\n\n"
                    "To approve: /approve " + str(uid) + "\n"
                    "To reject:  /reject "  + str(uid)
                )
            )
        except Exception:
            pass

        await update.message.reply_text(
            t(uid, "app_received"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_whatsapp"), url=WHATSAPP)],
                [InlineKeyboardButton(t(uid, "btn_home"),     callback_data="home")],
            ])
        )

    elif u.get("waiting") == "lots":
        try:
            d = float(text)
            if d <= 0:
                raise ValueError
        except Exception:
            await update.message.reply_text(t(uid, "invalid_lots"))
            return
        broker = u.get("cb", "exness")
        acc    = u.get("ca", "std")
        rate   = u.get("rate", 3.00)
        label  = "Raw/ECN" if acc == "raw" else "Standard"
        lang   = lang_of(uid)
        m      = round(d * 22  * rate, 2)
        y      = round(d * 252 * rate, 2)
        u["waiting"] = None
        await update.message.reply_text(
            t(uid, "calc_result", broker=BD.get(broker, broker), label=label, d=d, rate=rate, m=m, y=y),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "btn_stop_losing"), url=SIGNUP_LINK)],
                [InlineKeyboardButton(t(uid, "btn_calc_again"),  callback_data="calc")],
                [InlineKeyboardButton(t(uid, "btn_home"),        callback_data="home")],
            ])
        )
    else:
        await update.message.reply_text(t(uid, "fallback"))

    # ── ADMIN ─────────────────────────────────────────────────

async def approve(update, context):
    if update.effective_user.id != 7114761739:
        return
    if not context.args:
        await update.message.reply_text("Usage: /approve [user_id]")
        return
    try:
        target_uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    lang = USER.get(target_uid, {}).get("lang", "en")
    msgs = {
    "en": "Congratulations! Your account has been verified.\n\nYou can now access Rebatrix!\n\n" + SIGNUP_LINK,
    "ar": "تهانينا! تم التحقق من حسابك.\n\nيمكنك الآن الوصول إلى Rebatrix!\n\n" + SIGNUP_LINK,
    "id": "Selamat! Akun kamu telah diverifikasi.\n\nKamu sekarang bisa mengakses Rebatrix!\n\n" + SIGNUP_LINK,
    "ur": "مبارک ہو! آپ کا اکاؤنٹ تصدیق ہو گیا ہے۔\n\nاب آپ Rebatrix تک رسائی حاصل کر سکتے ہیں!\n\n" + SIGNUP_LINK,
    "fr": "Félicitations! Votre compte a été vérifié.\n\nVous pouvez maintenant accéder à Rebatrix!\n\n" + SIGNUP_LINK,
    }
    await context.bot.send_message(chat_id=target_uid, text=msgs.get(lang, msgs["en"]))
    await update.message.reply_text("Approved! Link sent to user " + str(target_uid))

async def reject(update, context):
    if update.effective_user.id != 7114761739:
        return
    if not context.args:
        await update.message.reply_text("Usage: /reject [user_id]")
        return
    try:
        target_uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    lang = USER.get(target_uid, {}).get("lang", "en")
    msgs = {
    "en": "We could not verify your account. Please make sure you signed up correctly and try again. Type /start to reapply.",
    "ar": "لم نتمكن من التحقق من حسابك. تأكد من التسجيل بشكل صحيح وحاول مجدداً. اكتب /start للتقديم مجدداً.",
    "id": "Kami tidak dapat memverifikasi akun kamu. Pastikan kamu mendaftar dengan benar dan coba lagi. Ketik /start untuk mendaftar ulang.",
    "ur": "ہم آپ کے اکاؤنٹ کی تصدیق نہیں کر سکے۔ دوبارہ کوشش کریں۔ /start لکھ کر دوبارہ درخواست دیں۔",
    "fr": "Nous n’avons pas pu verifier votre compte. Assurez-vous d’avoir bien suivi les etapes. Tapez /start pour repostuler.",
    }
    await context.bot.send_message(chat_id=target_uid, text=msgs.get(lang, msgs["en"]))
    await update.message.reply_text("Rejected. User " + str(target_uid) + " notified.")

# ── MAIN ──────────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject",  reject))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    app.add_error_handler(lambda update, context: logging.exception("Unhandled error: %s", context.error))
    print("Rebatrix multilingual bot running…")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()