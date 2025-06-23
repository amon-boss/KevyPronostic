import os
import telebot
from keep_alive import keep_alive

# 🔐 Variables d’environnement
BOT_TOKEN = os.environ['BOT_TOKEN']
GROUP_ID = int(os.environ['GROUP_ID'])

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        username = f"@{new_member.username}" if new_member.username else new_member.first_name
        welcome_text = f"🎉 Bienvenue {username} dans le groupe KevyFlow Prono ! 💯🔥"
        bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🤖 Bot KevyFlow Prono actif et prêt à accueillir les membres !")

print("✅ KevyFlowBot Prono est actif.")
keep_alive()
bot.infinity_polling()
