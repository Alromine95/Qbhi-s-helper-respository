import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai

# 1. Paste your secret keys here
TELEGRAM_TOKEN = "8946954745:AAEfBuP-Q3Q9vpq_5UT8t8_5oZIOpxL_g_8"
GEMINI_API_KEY = "AQ.Ab8RN6Kkk-0eF5OPuzTiR9U3DwsS1ltG7lF0eYBmlvBC_KVSpQ"

# Enable logging to follow what the bot does in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Initialize the Google Gemini client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    user_text = update.message.text
    chat_id = update.message.chat_id
    logger.info(f"Received message: {user_text}")
    
    try:
        # 3. Call Gemini's lightning fast and free Flash model
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are a helpful AI assistant inside a public Telegram group chat. Keep your response concise. Message: {user_text}"
        )
        ai_reply = response.text
        
        # Send response back to Telegram
        await context.bot.send_message(chat_id=chat_id, text=ai_reply)
        logger.info(f"Replied successfully using Gemini free tier!")
        
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")

def main():
    print("--- SWAPPING TO GEMINI: Bot Attempting to Start ---")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("--- POLLING STARTED: Bot is now listening ---")
    app.run_polling()

if __name__ == "__main__":
    main()

