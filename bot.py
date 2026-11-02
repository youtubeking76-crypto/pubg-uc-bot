from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from flask import Flask, request
import os

# 🔴 አዲሱን የቦት ቶከን እዚህ ያስገቡ (በ @BotFather /revoke አድርገው አዲስ ያመንጩ)
TOKEN = "9232334688:AAHZvYQr6homNcwoLVvT9VOYaWMGyCLyoxo"

app = Flask(__name__)

def get_inline_menu():
    keyboard = [
        [InlineKeyboardButton("😋INVITE TO EARN UC😋", callback_data='invite')],
        [
            InlineKeyboardButton("💸WITHDRAW💸", callback_data='withdraw'),
            InlineKeyboardButton("💰Balance💰", callback_data='balance')
        ],
        [
            InlineKeyboardButton("💲Daily Rewards💲", callback_data='rewards'),
            InlineKeyboardButton("💚SPONSORE💚", callback_data='sponsore')
        ],
        [
            InlineKeyboardButton("How it' WORKS", callback_data='how_works'),
            InlineKeyboardButton("Help", callback_data='help')
        ],
        [
            InlineKeyboardButton("⬅️Back", callback_data='back'),
            InlineKeyboardButton("🔼Main Menu", callback_data='main_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🎮 Main Menu:"
    await update.message.reply_text(text, reply_markup=get_inline_menu())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'invite':
        await query.edit_message_text("🔗 Your invite link: https://t.me/Freepubgmuc_bot?start=ref123", reply_markup=get_inline_menu())
    elif query.data == 'withdraw':
        await query.edit_message_text("💸 Minimum withdrawal is 1000 UC.", reply_markup=get_inline_menu())
    elif query.data == 'balance':
        await query.edit_message_text("💰 Your current UC balance: 0 UC", reply_markup=get_inline_menu())
    elif query.data == 'rewards':
        await query.edit_message_text("💲 Come back tomorrow!", reply_markup=get_inline_menu())
    elif query.data == 'sponsore':
        await query.edit_message_text("💚 Thanks to our sponsors!", reply_markup=get_inline_menu())
    elif query.data == 'how_works':
        await query.edit_message_text("ℹ️ Invite friends to earn UC.", reply_markup=get_inline_menu())
    elif query.data == 'help':
        await query.edit_message_text("📞 Contact: @YourSupportUsername", reply_markup=get_inline_menu())
    elif query.data == 'main_menu' or query.data == 'back':
        await query.edit_message_text("🎮 Main Menu:", reply_markup=get_inline_menu())

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "❌ Unknown Command!\n\nℹ️ Do not send Messages directly to the Bot or reload the Menu by pressing /start"
    await update.message.reply_text(text)

# የቴሌግራም አፕሊኬሽን ማዘጋጀት
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_click))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

# የዌብ ሰርቨር መግቢያ (Health Check)
@app.route('/')
def index():
    return "Bot is running!"

# የቴሌግራም መልዕክቶችን የሚቀበል (Webhook)
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
