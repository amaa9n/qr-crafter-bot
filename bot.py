import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes, 
    CallbackQueryHandler,
    Application
)

# --- Configuration & Environment ---
# Your Mini App URL
MINI_APP_URL = "https://qrcrafter-bot.vercel.app"

# Your Render Service URL (Used for setting the webhook path)
RENDER_SERVICE_URL = "https://qr-crafter-bot.onrender.com" 

# Placeholders (Update these when ready)
SUPPORT_URL = "https://t.me/QrCrafterbot?start=support" 
BUY_ME_A_COFFEE_URL = "https://your.actual.support/link" 

# Set up logging (Essential for debugging on Render)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Command Definitions for Telegram Menu ---
COMMANDS = [
    BotCommand("start", "🚀 Main Menu & Launch App"),
    BotCommand("launch", "✨ Launch QR Crafter Mini App directly"),
    BotCommand("features", "💡 See all powerful features"),
    BotCommand("guide", "📚 Step-by-step usage guide"),
]

# --- Handlers ---

async def set_bot_commands(application):
    """Sets the official list of commands for the bot menu."""
    await application.bot.set_my_commands(COMMANDS)
    logger.info("Bot commands set successfully.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name if update.effective_user else "User"
    welcome_message = (
        f"🌟 **Welcome to QR Crafter, {user_name}!**\n\n"
        "The ultimate Telegram Mini App for custom, high-quality QR codes.\n\n"
        "**🔥 QUICK LAUNCH:** Press the button below to start creating immediately!\n"
        "**👇 Need help?** Use the command menu (`/`) or buttons below to explore features and guides."
    )
    launch_button = InlineKeyboardButton(
        text="🚀 Launch QR Crafter Mini App",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    features_button = InlineKeyboardButton(text="💡 Features", callback_data='cmd_features')
    guide_button = InlineKeyboardButton(text="📚 Guide", callback_data='cmd_guide')
    
    keyboard = InlineKeyboardMarkup([
        [launch_button],
        [features_button, guide_button]
    ])
    await update.message.reply_text(
        welcome_message,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def launch_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)

async def show_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    features_text = (
        "✨ **QR Crafter Key Features**\n\n"
        "**1. Versatile Content Types:** URLs, Text, WiFi, vCards, Emails, and more.\n"
        "**2. Deep Customization & Branding:** Modify styles, embed your brand **Logo**, and enjoy AI sharpening.\n"
        "**3. Professional Export:** High-res **PNG** or send directly as a high-quality **PDF** to this chat.\n"
    )
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="🚀 Launch QR Crafter Mini App", web_app=WebAppInfo(url=MINI_APP_URL))
    ]])
    await (update.callback_query or update.message).reply_text(
        features_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guide_text = (
        "📚 **Step-by-Step Guide**\n\n"
        "1. **Add Content:** Launch the App and choose content type (URL, WiFi, etc.).\n"
        "2. **Customize Design:** Change **Colors**, **Shapes**, and add your **Logo**.\n"
        "3. **Generate:** Instantly preview your custom QR code.\n"
        "4. **Export:** Use the **'Send as PDF'** button to deliver the QR code directly to your Telegram chat.\n"
    )
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="🚀 Start Crafting Now!", web_app=WebAppInfo(url=MINI_APP_URL))
    ]])
    await (update.callback_query or update.message).reply_text(
        guide_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    
    if query.data == 'cmd_features':
        await show_features(update, context) 
    elif query.data == 'cmd_guide':
        await show_guide(update, context)


# --- Main Application Runner (Webhook) ---

def main() -> None:
    # 1. Get environment variables
    TOKEN = os.environ.get("BOT_TOKEN")
    
    # Render sets these automatically when deploying a Web Service
    PORT = int(os.environ.get("PORT", "8080")) 
    
    # Render provides its external URL via RENDER_EXTERNAL_URL
    WEBHOOK_BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", RENDER_SERVICE_URL)

    if not TOKEN:
        logger.error("FATAL ERROR: BOT_TOKEN is not set.")
        return

    # 2. Build the Application (FIXED: Call job_queue() without a parameter)
    # This enables JobQueue since the dependencies are now in requirements.txt
    application = Application.builder().token(TOKEN).job_queue().build()

    # 3. Register Handlers
    application.add_handler(CommandHandler("start", menu))
    application.add_handler(CommandHandler("launch", launch_app))
    application.add_handler(CommandHandler("features", show_features))
    application.add_handler(CommandHandler("guide", show_guide))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # 4. Set Commands and Run Webhook
    if WEBHOOK_BASE_URL:
        # Set commands once on startup
        application.job_queue.run_once(lambda context: set_bot_commands(application), 0)
        
        # The webhook path includes the token for security
        WEBHOOK_PATH = '/' + TOKEN 
        
        # Start the web server (Listens on the port Render requires)
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=WEBHOOK_PATH,
            webhook_url=WEBHOOK_BASE_URL + WEBHOOK_PATH
        )
        logger.info(f"✅ Bot started in Webhook mode on URL: {WEBHOOK_BASE_URL + WEBHOOK_PATH}")
    else:
        # Fallback to polling for local testing 
        logger.warning("⚠️ WEBHOOK_BASE_URL not set. Running in Polling mode for local testing.")
        application.run_polling(poll_interval=3.0) 

if __name__ == "__main__":
    main()
