import logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SIGNUP_LINK = "https://rebatrix.club"
logging.basicConfig(level=logging.INFO)
RATES = {"exness":{"std":6.00,"raw":3.00},"icmarkets":{"std":5.50,"raw":2.75},"xm":{"std":8.50,"raw":4.25}}
BROKERS = [("Exness","exness"),("IC Markets","icmarkets"),("XM","xm")]
BD = {k:n for n,k in BROKERS}
USER = {}
SIZE_MAP = {"1":"Under $500","2":"$500-$2,500","3":"$2,500-$10,000","4":"$10,000-$50,000","5":"$50,000-$1M+"}
EST_MAP = {"1":"$5-$20","2":"$30-$100","3":"$100-$400","4":"$400-$2,000","5":"$2,000+"}

async def start(update, context):
    USER[update.effective_user.id] = {}
    await update.message.reply_text(
        "👋 Welcome to Rebatrix!\n\nEarn cashback on every forex trade — win or lose.\n\nWhat would you like to do?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 What are rebates?",callback_data="explain")],
            [InlineKeyboardButton("✅ I know — lets get started",callback_data="onboard")],
            [InlineKeyboardButton("🧮 Calculate my rebates",callback_data="calc")]
        ]))

async def button(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data
    if uid not in USER:
        USER[uid] = {}
    u = USER[uid]

    if data == "home":
        USER[uid] = {}
        await q.edit_message_text(
            "👋 Welcome to Rebatrix!\n\nEarn cashback on every forex trade — win or lose.\n\nWhat would you like to do?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 What are rebates?",callback_data="explain")],
                [InlineKeyboardButton("✅ I know — lets get started",callback_data="onboard")],
                [InlineKeyboardButton("🧮 Calculate my rebates",callback_data="calc")]
            ]))

    elif data == "explain":
        await q.edit_message_text(
            "📚 What are forex rebates?\n\nEvery time you open a trade, your broker earns a spread or commission.\n\nRebatrix shares a portion back with you automatically.\n\n✅ You trade as normal\n✅ Cashback on every trade\n✅ Works on winning AND losing trades\n\nFree to join. No catch.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Got it — lets go",callback_data="onboard")],
                [InlineKeyboardButton("🧮 Calculate my rebates",callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data == "onboard":
        u["flow"] = "onboard"
        await q.edit_message_text(
            "🔍 Step 1 — Which broker do you trade with?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness",callback_data="ob_exness"),InlineKeyboardButton("IC Markets",callback_data="ob_icmarkets")],
                [InlineKeyboardButton("XM",callback_data="ob_xm")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("ob_"):
        u["broker"] = data.replace("ob_","")
        await q.edit_message_text(
            "💵 Step 2 — What is your account size?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Under $500",callback_data="os_1")],
                [InlineKeyboardButton("$500 - $2,500",callback_data="os_2")],
                [InlineKeyboardButton("$2,500 - $10,000",callback_data="os_3")],
                [InlineKeyboardButton("$10,000 - $50,000",callback_data="os_4")],
                [InlineKeyboardButton("$50,000 - $1M+",callback_data="os_5")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("os_"):
        u["size"] = data.replace("os_","")
        await q.edit_message_text(
            "📊 Step 3 — How long have you been trading?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🆕 Less than 6 months",callback_data="oe_new")],
                [InlineKeyboardButton("📈 6 months - 2 years",callback_data="oe_mid")],
                [InlineKeyboardButton("🏆 2+ years",callback_data="oe_pro")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("oe_"):
        u["exp"] = data.replace("oe_","")
        await q.edit_message_text(
            "🌍 Step 4 — Which country are you from?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇦🇪 UAE",callback_data="or_uae"),InlineKeyboardButton("🇮🇳 India",callback_data="or_india")],
                [InlineKeyboardButton("🇵🇰 Pakistan",callback_data="or_pak"),InlineKeyboardButton("🇺🇸 USA",callback_data="or_usa")],
                [InlineKeyboardButton("🌐 Type my country",callback_data="or_type")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("or_"):
        if data == "or_type":
            u["waiting"] = "country"
            await q.edit_message_text("✏️ Type your country name below:")
        else:
            cm = {"or_uae":"🇦🇪 UAE","or_india":"🇮🇳 India","or_pak":"🇵🇰 Pakistan","or_usa":"🇺🇸 USA"}
            u["country"] = cm.get(data,"Other")
            broker = u.get("broker","exness")
            size = u.get("size","2")
            est = EST_MAP.get(size,"$30-$100")
            sz = SIZE_MAP.get(size,size)
            await q.edit_message_text(
                "✅ You are eligible for Rebatrix!\n\nBroker: " + BD.get(broker,broker) + "\nAccount: " + sz + "\nCountry: " + u["country"] + "\n💰 Est. monthly cashback: " + est + "\n\nWant the exact number? Use the calculator below.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Claim My Rebates — Free",url=SIGNUP_LINK)],
                    [InlineKeyboardButton("🧮 Calculate exact amount",callback_data="calc")],
                    [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
                ]))

    elif data == "calc":
        u["flow"] = "calc"
        await q.edit_message_text(
            "🧮 Rebate Calculator\n\nStep 1 — Which broker?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness",callback_data="cb_exness"),InlineKeyboardButton("IC Markets",callback_data="cb_icmarkets")],
                [InlineKeyboardButton("XM",callback_data="cb_xm")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("cb_"):
        u["cb"] = data.replace("cb_","")
        broker = u["cb"]
        await q.edit_message_text(
            "✅ Broker: " + BD.get(broker,broker) + "\n\nStep 2 — Account type?\n\n📊 Standard — wider spread, no commission\n⚡ Raw/ECN — tight spread, commission per trade",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 Standard Account",callback_data="ca_std")],
                [InlineKeyboardButton("⚡ Raw / ECN Account",callback_data="ca_raw")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif data.startswith("ca_"):
        acc = data.replace("ca_","")
        broker = u.get("cb","exness")
        rate = RATES.get(broker,{}).get(acc,3.00)
        u["ca"] = acc
        u["rate"] = rate
        u["waiting"] = "lots"
        label = "Raw/ECN" if acc=="raw" else "Standard"
        await q.edit_message_text(
            "✅ " + BD.get(broker,broker) + " | " + label + " | $" + str(rate) + "/lot\n\nStep 3 — How many lots of XAUUSD per day?\n\n• Casual: 1 lot\n• Regular: 3+ lots\n• Active: 7+ lots\n\nType your number below:")

async def message(update, context):
    uid = update.effective_user.id
    text = update.message.text.strip()
    if uid not in USER:
        USER[uid] = {}
    u = USER[uid]

    if u.get("waiting") == "country":
        u["country"] = text
        u["waiting"] = None
        broker = u.get("broker","exness")
        size = u.get("size","2")
        est = EST_MAP.get(size,"$30-$100")
        sz = SIZE_MAP.get(size,size)
        await update.message.reply_text(
            "✅ You are eligible for Rebatrix!\n\nBroker: " + BD.get(broker,broker) + "\nAccount: " + sz + "\nCountry: " + text + "\n💰 Est. monthly cashback: " + est + "\n\nWant the exact number? Use the calculator below.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Claim My Rebates — Free",url=SIGNUP_LINK)],
                [InlineKeyboardButton("🧮 Calculate exact amount",callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))

    elif u.get("waiting") == "lots":
        try:
            d = float(text)
            if d <= 0:
                raise ValueError
        except Exception:
            await update.message.reply_text("⚠️ Enter a number like 2 or 0.5")
            return
        broker = u.get("cb","exness")
        acc = u.get("ca","std")
        rate = u.get("rate",3.00)
        label = "Raw/ECN" if acc=="raw" else "Standard"
        m = round(d*22*rate,2)
        y = round(d*252*rate,2)
        u["waiting"] = None
        await update.message.reply_text(
            "💸 Here is what you are leaving on the table...\n\nBroker: " + BD.get(broker,broker) + "\nAccount: " + label + "\nDaily lots: " + str(d) + "\nRate: $" + str(rate) + "/lot\n\n━━━━━━━━━━━━━━━━\n📅 Monthly:  $" + str(m) + " uncollected\n📆 Yearly:   $" + str(y) + " uncollected\n━━━━━━━━━━━━━━━━\n\nThat is $" + str(y) + " every year going to your broker that should be coming back to you.\n\nSign up free on Rebatrix and start collecting it 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Stop leaving money — Join Free",url=SIGNUP_LINK)],
                [InlineKeyboardButton("🔄 Calculate again",callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu",callback_data="home")]
            ]))
    else:
        await update.message.reply_text("Type /start to begin 👋")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message))
    print("Rebatrix bot running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
    elif data.startswith("os_"):
        u["size"] = data.replace("os_","")
        await q.edit_message_text("📊 *Step 3 — How long have you been trading?*",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🆕 Less than 6 months",callback_data="oe_new")],[InlineKeyboardButton("📈 6 months – 2 years",callback_data="oe_mid")],[InlineKeyboardButton("🏆 2+ years",callback_data="oe_pro")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    elif data.startswith("oe_"):
        u["exp"] = data.replace("oe_","")
        await q.edit_message_text("🌍 *Step 4 — Which country are you from?*",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🇦🇪 UAE",callback_data="or_uae"),InlineKeyboardButton("🇮🇳 India",callback_data="or_india")],[InlineKeyboardButton("🇵🇰 Pakistan",callback_data="or_pak"),InlineKeyboardButton("🇺🇸 USA",callback_data="or_usa")],[InlineKeyboardButton("🌐 Type my country",callback_data="or_type")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    elif data.startswith("or_"):
        if data == "or_type":
            u["waiting"] = "country"
            await q.edit_message_text("✏️ *Type your country name below:*",parse_mode="Markdown")
        else:
            cm = {"or_uae":"🇦🇪 UAE","or_india":"🇮🇳 India","or_pak":"🇵🇰 Pakistan","or_usa":"🇺🇸 USA"}
            u["country"] = cm.get(data,"🌐 Other")
            size_map = {"1":"Under $500","2":"$500–$2,500","3":"$2,500–$10,000","4":"$10,000–$50,000","5":"$50,000–$1M+"}
            broker = u.get("broker","exness")
            size = u.get("size","2")
            est_map = {"1":"$5–$20","2":"$30–$100","3":"$100–$400","4":"$400–$2,000","5":"$2,000+"}
            est = est_map.get(size,"$30–$100")
            await q.edit_message_text(f"✅ *You are eligible for Rebatrix!*\n\nBroker: *{BD.get(broker,broker)}*\nAccount: *{size_map.get(size,size)}*\nCountry: *{u['country']}*\n💰 Est. monthly cashback: *{est}*\n\n_Want the exact number? Use the calculator 👇_",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Claim My Rebates — Free",url=SIGNUP_LINK)],[InlineKeyboardButton("🧮 Calculate exact amount",callback_data="calc")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    elif data == "calc":
        u["flow"] = "calc"
        await q.edit_message_text("🧮 *Rebate Calculator*\n\n*Step 1 — Which broker?*",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Exness",callback_data="cb_exness"),InlineKeyboardButton("IC Markets",callback_data="cb_icmarkets")],[InlineKeyboardButton("XM",callback_data="cb_xm")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    elif data.startswith("cb_"):
        u["cb"] = data.replace("cb_","")
        broker = u["cb"]
        await q.edit_message_text(f"✅ Broker: *{BD.get(broker,broker)}*\n\n*Step 2 — Account type?*\n\n📊 *Standard* — wider spread, no commission\n⚡ *Raw/ECN* — tight spread, commission per trade",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊 Standard Account",callback_data="ca_std")],[InlineKeyboardButton("⚡ Raw / ECN Account",callback_data="ca_raw")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    elif data.startswith("ca_"):
        acc = data.replace("ca_","")
        broker = u.get("cb","exness")
        rate = RATES.get(broker,{}).get(acc,3.00)
        u["ca"] = acc
        u["rate"] = rate
        u["waiting"] = "lots"
        label = "Raw/ECN" if acc=="raw" else "Standard"
        await q.edit_message_text(f"✅ *{BD.get(broker,broker)}* | *{label}* | *${rate:.2f}/lot*\n\n*Step 3 — How many lots of XAUUSD per day?*\n\n• Casual → 1 lot\n• Regular → 3+ lots\n• Active → 7+ lots\n\n_Type your number below:_",parse_mode="Markdown")

async def message(update, context):
    uid = update.effective_user.id
    text = update.message.text.strip()
    if uid not in USER: USER[uid] = {}
    u = USER[uid]
    if u.get("waiting") == "country":
        u["country"] = text
        u["waiting"] = None
        broker = u.get("broker","exness")
        size = u.get("size","2")
        size_map = {"1":"Under $500","2":"$500–$2,500","3":"$2,500–$10,000","4":"$10,000–$50,000","5":"$50,000–$1M+"}
        est_map = {"1":"$5–$20","2":"$30–$100","3":"$100–$400","4":"$400–$2,000","5":"$2,000+"}
        est = est_map.get(size,"$30–$100")
        await update.message.reply_text(f"✅ *You are eligible for Rebatrix!*\n\nBroker: *{BD.get(broker,broker)}*\nAccount: *{size_map.get(size,size)}*\nCo
untry: *{text}*\n💰 Est. monthly cashback: *{est}*\n\n_Want the exact number? Use the calculator 👇_",parse_mode="Markdown",reply_markup=InlineKeyboardMarku
p([[InlineKeyboardButton("🚀 Claim My Rebates — Free",url=SIGNUP_LINK)],[InlineKeyboardButton("🧮 Calculate exact amount",callback_data="calc")],[InlineKeybo
ardButton("🏠 Main menu",callback_data="home")]]))
    elif u.get("waiting") == "lots":
        try:
            d = float(text)
            if d <= 0: raise ValueError
        except:
            await update.message.reply_text("⚠️ Enter a number like 2 or 0.5")
            return
        broker = u.get("cb","exness")
        acc = u.get("ca","std")
        rate = u.get("rate",3.00)
        label = "Raw/ECN" if acc=="raw" else "Standard"
        m = d*22*rate
        y = d*252*rate
        u["waiting"] = None
        await update.message.reply_text(f"💸 *Here's what you're leaving on the table...*\n\nBroker: *{BD.get(broker,broker)}*\nAccount: *{label}*\nDaily lo
ts: *{d}*\nRate: *${rate:.2f}/lot*\n\n━━━━━━━━━━━━━━━━\n📅 Monthly:  *${m:,.2f} uncollected*\n📆 Yearly:   *${y:,.2f} uncollected*\n━━━━━━━━━━━━━━━━\n\nThat
's *${y:,.2f} every year* going to your broker that should be coming back to you.\n\nSign up free on Rebatrix and start collecting it 👇",parse_mode="Markdo
wn",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Stop leaving money — Join Free",url=SIGNUP_LINK)],[InlineKeyboardButton("🔄 Calculate again
",callback_data="calc")],[InlineKeyboardButton("🏠 Main menu",callback_data="home")]]))
    else:
        await update.message.reply_text("Type /start to begin 👋")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message))
    print("✅ Rebatrix bot running...")
    app.run_polling(drop_pending_updates=True)
if __name__ == "__main__":
    main()
