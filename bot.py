import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
MINI_APP_URL = "https://qrcrafter-bot.vercel.app"

# --- Placeholder URLs (Update these when ready!) ---
# These are used for external links like support/funding.
SUPPORT_URL = "https://t.me/QrCrafterbot?start=support" 
BUY_ME_A_COFFEE_URL = "https://your.actual.support/link" 

# --- Command Definitions for Telegram Menu ---
# This list will be used to set the official bot command list.
COMMANDS = [
    BotCommand("start", "🚀 Main Menu & Launch App"),
    BotCommand("launch", "✨ Launch QR Crafter Mini App directly"),
    BotCommand("features", "💡 See all powerful features"),
    BotCommand("guide", "📚 Step-by-step usage guide"),
    # Add these back when ready:
    # BotCommand("support", "💬 Contact Support / Help"),
]

# --- Handler Functions ---

async def set_bot_commands(application):
    """Sets the official list of commands for the bot menu."""
    await application.bot.set_my_commands(COMMANDS)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start. Shows the main menu with a launch button and command guidance."""
    
    user_name = update.effective_user.first_name if update.effective_user else "User"

    welcome_message = (
        f"🌟 **Welcome to QR Crafter, {user_name}!**\n\n"
        "The ultimate Telegram Mini App for custom, high-quality QR codes.\n\n"
        "**🔥 QUICK LAUNCH:** Press the button below to start creating immediately!\n"
        "**👇 Need help?** Use the command menu (`/`) or buttons below to explore features and guides."
    )

    # 1. Main Launch Button
    launch_button = InlineKeyboardButton(
        text="🚀 Launch QR Crafter Mini App",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    # 2. Command Buttons
    features_button = InlineKeyboardButton(text="💡 Features", callback_data='cmd_features')
    guide_button = InlineKeyboardButton(text="📚 Guide", callback_data='cmd_guide')
    
    # Optional Buttons (Add back when ready)
    # support_button = InlineKeyboardButton(text="💬 Support", url=SUPPORT_URL)
    # coffee_button = InlineKeyboardButton(text="☕ Support", url=BUY_ME_A_COFFEE_URL)

    keyboard = InlineKeyboardMarkup([
        [launch_button],
        [features_button, guide_button]
        # Example of adding a third row:
        # [support_button, coffee_button] 
    ])

    await update.message.reply_text(
        welcome_message,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def launch_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /launch. Redirects to the main menu handler."""
    # Simply call the menu function to send the same rich message
    await menu(update, context)


async def show_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /features and the corresponding inline button."""
    
    # Message content based on screenshots 24063, 24064, 24065, 24066
    features_text = (
        "✨ **QR Crafter Key Features**\n\n"
        
        "**1. Versatile Content Types:**\n"
        "   - Create QR codes for **URLs**, **Text**, **WiFi**, **vCards**, **Emails**, **SMS**, **Phone**, and **Location** (Geo-coordinates).\n\n"
        
        "**2. Deep Customization & Branding:**\n"
        "   - **Style Control:** Modify the style of QR code dots and corners.\n"
        "   - **Branding:** Seamlessly embed your brand **Logo**.\n"
        "   - **AI Enhancement:** Logo sharpening for crisp, high-quality appearance.\n\n"
        
        "**3. Professional Export:**\n"
        "   - **High-Resolution Export:** Download as a print-ready **PNG**.\n"
        "   - **Telegram Integration:** Send your custom QR code directly back to this chat as a high-quality **PDF**.\n\n"
        
        "**4. Advanced Reliability:**\n"
        "   - **Robust Error Correction:** Multiple levels to ensure your code scans reliably every time.\n"
    )
    
    # Button to return to the main action
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="🚀 Launch QR Crafter Mini App", web_app=WebAppInfo(url=MINI_APP_URL))
    ]])

    await update.message.reply_text(
        features_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /guide and the corresponding inline button."""
    
    # Message content based on screenshots 24061 and 24062
    guide_text = (
        "📚 **Step-by-Step Guide to Creating a QR Code**\n\n"
        
        "1. **Step 1: Add Content**\n"
        "   - Launch the Mini App and choose a content type (URL, Text, WiFi, etc.).\n"
        "   - Enter the information you want to encode.\n\n"
        
        "2. **Step 2: Customize Design**\n"
        "   - Personalize the look: change **Colors**, **Shapes**, and add your own **Logo**.\n\n"
        
        "3. **Step 3: Generate & Preview**\n"
        "   - Instantly generate your QR code to see a live preview. Make adjustments until it's perfect.\n\n"
        
        "4. **Step 4: Download or Send**\n"
        "   - Download a high-quality **PNG** or use the **'Send as PDF'** button to deliver the QR code directly to your Telegram chat.\n"
    )

    # Button to return to the main action
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="🚀 Start Crafting Now!", web_app=WebAppInfo(url=MINI_APP_URL))
    ]])

    await update.message.reply_text(
        guide_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button presses from the menu (e.g., Features, Guide)."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press
    
    # Simulate calling the command handlers based on callback data
    if query.data == 'cmd_features':
        # Temporarily use the query object to simulate a message update
        await show_features(query, context)
    elif query.data == 'cmd_guide':
        await show_guide(query, context)


# --- Main Function to Run the Bot ---

def main():
    if not BOT_TOKEN:
        print("FATAL ERROR: BOT_TOKEN is not set in environment variables.")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", menu))
    application.add_handler(CommandHandler("launch", launch_app))
    application.add_handler(CommandHandler("features", show_features))
    application.add_handler(CommandHandler("guide", show_guide))
    
    # Register the callback handler for inline buttons
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Set the official bot commands list asynchronously
    application.job_queue.run_once(lambda context: set_bot_commands(application), 0)
    
    print("Bot is starting with rich command structure...")
    application.run_polling(poll_interval=3.0) 
    
if __name__ == '__main__':
    main()
