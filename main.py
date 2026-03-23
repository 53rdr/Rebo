import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SIGNUP_LINK = "https://rebatrix.club"
logging.basicConfig(level=logging.INFO)

RATES = {
    "exness": {"std": 6.00, "raw": 3.00},
    "icmarkets": {"std": 5.50, "raw": 2.75},
    "xm": {"std": 8.50, "raw": 4.25},
}
BROKERS = [("Exness", "exness"), ("IC Markets", "icmarkets"), ("XM", "xm")]
BD = {k: n for n, k in BROKERS}
USER = {}
SIZE_MAP = {
    "1": "Under $500",
    "2": "$500 - $2,500",
    "3": "$2,500 - $10,000",
    "4": "$10,000 - $50,000",
    "5": "$50,000 - $1M+",
}
EST_MAP = {
    "1": "$5 - $20",
    "2": "$30 - $100",
    "3": "$100 - $400",
    "4": "$400 - $2,000",
    "5": "$2,000+",
}


def home_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 What are rebates?", callback_data="explain")],
        [InlineKeyboardButton("✅ I know — lets get started", callback_data="onboard")],
        [InlineKeyboardButton("🧮 Calculate my rebates", callback_data="calc")],
    ])


async def start(update, context):
    USER[update.effective_user.id] = {}
    await update.message.reply_text(
        "👋 Welcome to Rebatrix!\n\n"
        "Earn cashback on every forex trade — win or lose.\n\n"
        "What would you like to do?",
        reply_markup=home_markup()
    )


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
            "👋 Welcome to Rebatrix!\n\n"
            "Earn cashback on every forex trade — win or lose.\n\n"
            "What would you like to do?",
            reply_markup=home_markup()
        )

    elif data == "explain":
        await q.edit_message_text(
            "📚 What are forex rebates?\n\n"
            "Every time you open a trade, your broker earns a spread or commission.\n\n"
            "Rebatrix shares a portion back with you automatically.\n\n"
            "✅ You trade as normal\n"
            "✅ Cashback on every trade\n"
            "✅ Works on winning AND losing trades\n\n"
            "Free to join. No catch.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Got it — lets go", callback_data="onboard")],
                [InlineKeyboardButton("🧮 Calculate my rebates", callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data == "onboard":
        u["flow"] = "onboard"
        await q.edit_message_text(
            "🔍 Step 1 — Which broker do you trade with?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness", callback_data="ob_exness"),
                 InlineKeyboardButton("IC Markets", callback_data="ob_icmarkets")],
                [InlineKeyboardButton("XM", callback_data="ob_xm")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("ob_"):
        u["broker"] = data.replace("ob_", "")
        await q.edit_message_text(
            "💵 Step 2 — What is your account size?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Under $500", callback_data="os_1")],
                [InlineKeyboardButton("$500 - $2,500", callback_data="os_2")],
                [InlineKeyboardButton("$2,500 - $10,000", callback_data="os_3")],
                [InlineKeyboardButton("$10,000 - $50,000", callback_data="os_4")],
                [InlineKeyboardButton("$50,000 - $1M+", callback_data="os_5")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("os_"):
        u["size"] = data.replace("os_", "")
        await q.edit_message_text(
            "📊 Step 3 — How long have you been trading?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🆕 Less than 6 months", callback_data="oe_new")],
                [InlineKeyboardButton("📈 6 months - 2 years", callback_data="oe_mid")],
                [InlineKeyboardButton("🏆 2+ years", callback_data="oe_pro")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("oe_"):
        u["exp"] = data.replace("oe_", "")
        await q.edit_message_text(
            "🌍 Step 4 — Which country are you from?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇦🇪 UAE", callback_data="or_uae"),
                 InlineKeyboardButton("🇮🇳 India", callback_data="or_india")],
                [InlineKeyboardButton("🇵🇰 Pakistan", callback_data="or_pak"),
                 InlineKeyboardButton("🇺🇸 USA", callback_data="or_usa")],
                [InlineKeyboardButton("🌐 Type my country", callback_data="or_type")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("or_"):
        if data == "or_type":
            u["waiting"] = "country"
            await q.edit_message_text("✏️ Type your country name below:")
        else:
            cm = {
                "or_uae": "🇦🇪 UAE",
                "or_india": "🇮🇳 India",
                "or_pak": "🇵🇰 Pakistan",
                "or_usa": "🇺🇸 USA",
            }
            u["country"] = cm.get(data, "Other")
            broker = u.get("broker", "exness")
            size = u.get("size", "2")
            await q.edit_message_text(
                "✅ You are eligible for Rebatrix!\n\n"
                "Broker: " + BD.get(broker, broker) + "\n"
                "Account size: " + SIZE_MAP.get(size, size) + "\n"
                "Country: " + u["country"] + "\n"
                "💰 Est. monthly cashback: " + EST_MAP.get(size, "$30-$100") + "\n\n"
                "Want the exact number? Use the calculator below.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Claim My Rebates — Free", url=SIGNUP_LINK)],
                    [InlineKeyboardButton("🧮 Calculate exact amount", callback_data="calc")],
                    [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
                ])
            )

    elif data == "calc":
        u["flow"] = "calc"
        await q.edit_message_text(
            "🧮 Rebate Calculator\n\nStep 1 — Which broker do you use for XAUUSD?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Exness", callback_data="cb_exness"),
                 InlineKeyboardButton("IC Markets", callback_data="cb_icmarkets")],
                [InlineKeyboardButton("XM", callback_data="cb_xm")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("cb_"):
        u["cb"] = data.replace("cb_", "")
        broker = u["cb"]
        await q.edit_message_text(
            "✅ Broker: " + BD.get(broker, broker) + "\n\n"
            "Step 2 — What type of account do you have?\n\n"
            "📊 Standard — wider spread, no commission\n"
            "⚡ Raw/ECN — tight spread, commission per trade",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 Standard Account", callback_data="ca_std")],
                [InlineKeyboardButton("⚡ Raw / ECN Account", callback_data="ca_raw")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif data.startswith("ca_"):
        acc = data.replace("ca_", "")
        broker = u.get("cb", "exness")
        rate = RATES.get(broker, {}).get(acc, 3.00)
        u["ca"] = acc
        u["rate"] = rate
        u["waiting"] = "lots"
        label = "Raw/ECN" if acc == "raw" else "Standard"
        await q.edit_message_text(
            "✅ " + BD.get(broker, broker) + " | " + label + " | $" + str(rate) + "/lot\n\n"
            "Step 3 — How many lots of XAUUSD do you trade per day?\n\n"
            "• Casual: 1 lot\n"
            "• Regular: 3+ lots\n"
            "• Active: 7+ lots\n\n"
            "Type your number below:"
        )


async def message(update, context):
    uid = update.effective_user.id
    text = update.message.text.strip()
    if uid not in USER:
        USER[uid] = {}
    u = USER[uid]

    if u.get("waiting") == "country":
        u["country"] = text
        u["waiting"] = None
        broker = u.get("broker", "exness")
        size = u.get("size", "2")
        await update.message.reply_text(
            "✅ You are eligible for Rebatrix!\n\n"
            "Broker: " + BD.get(broker, broker) + "\n"
            "Account size: " + SIZE_MAP.get(size, size) + "\n"
            "Country: " + text + "\n"
            "💰 Est. monthly cashback: " + EST_MAP.get(size, "$30-$100") + "\n\n"
            "Want the exact number? Use the calculator below.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Claim My Rebates — Free", url=SIGNUP_LINK)],
                [InlineKeyboardButton("🧮 Calculate exact amount", callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )

    elif u.get("waiting") == "lots":
        try:
            d = float(text)
            if d <= 0:
                raise ValueError
        except Exception:
            await update.message.reply_text("⚠️ Enter a number like 2 or 0.5")
            return
        broker = u.get("cb", "exness")
        acc = u.get("ca", "std")
        rate = u.get("rate", 3.00)
        label = "Raw/ECN" if acc == "raw" else "Standard"
        m = round(d * 22 * rate, 2)
        y = round(d * 252 * rate, 2)
        u["waiting"] = None
        await update.message.reply_text(
            "💸 Here is what you are leaving on the table...\n\n"
            "Broker: " + BD.get(broker, broker) + "\n"
            "Account: " + label + "\n"
            "Daily lots: " + str(d) + "\n"
            "Rate: $" + str(rate) + "/lot\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "📅 Monthly:  $" + str(m) + " uncollected\n"
            "📆 Yearly:   $" + str(y) + " uncollected\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "That is $" + str(y) + " every year going to your broker "
            "that should be coming back to you.\n\n"
            "Sign up free on Rebatrix and start collecting it 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Stop leaving money — Join Free", url=SIGNUP_LINK)],
                [InlineKeyboardButton("🔄 Calculate again", callback_data="calc")],
                [InlineKeyboardButton("🏠 Main menu", callback_data="home")],
            ])
        )
    else:
        await update.message.reply_text("Type /start to begin 👋")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    print("Rebatrix bot running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
