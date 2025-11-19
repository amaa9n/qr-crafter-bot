import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuration ---
# Your bot token is read from the environment variable "BOT_TOKEN"
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Your Mini App URL
MINI_APP_URL = "https://qrcrafter-bot.vercel.app"

# --- Handler Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command. Greets the user and provides instructions and features."""
    
    user_name = update.effective_user.first_name if update.effective_user else "User"

    # 1. The Welcome Message (Detailed and structured)
    welcome_message = (
        f"👋 **Hello, {user_name}! Welcome to QR Crafter Bot!**\n\n"
        "I’m your gateway to creating powerful, custom QR codes right here in Telegram.\n\n"
        
        "### ✨ **Key Features of QR Crafter:**\n"
        "* **Versatile Content:** URLs, Text, WiFi, vCards, Emails, and more.\n"
        "* **Deep Customization:** Modify colors, shapes, and margins for a unique look.\n"
        "* **Branding:** Embed your own **Logo** into the QR code with AI enhancement.\n"
        "* **High-Res Export:** Download as a high-quality PNG, or send directly as a **PDF** to this chat.\n"
        
        "\n### ⚙️ **How to Use (4 Simple Steps):**\n"
        "1.  Press the **Launch App** button below.\n"
        "2.  Choose a content type and input your data.\n"
        "3.  Customize your design and add your logo.\n"
        "4.  Generate and use the **Send as PDF** button to get the result back in your chat!\n"
    )

    # 2. Create the Keyboard Buttons
    
    # 2a. Main Mini App Button (The core action)
    mini_app_button = InlineKeyboardButton(
        text="🚀 Launch QR Crafter Mini App",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    # 3. Assemble the Keyboard (Single row for launch)
    keyboard = InlineKeyboardMarkup([
        [mini_app_button]
    ])

    # 4. Send the Message
    await update.message.reply_text(
        welcome_message,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# --- Main Function to Run the Bot ---

def main():
    if not BOT_TOKEN:
        print("FATAL ERROR: BOT_TOKEN is not set in environment variables.")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is starting via polling...")
    application.run_polling(poll_interval=3.0) 
    
if __name__ == '__main__':
    main()
