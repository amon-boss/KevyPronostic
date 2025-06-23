import os
import telebot
from telebot import types
from keep_alive import keep_alive
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# === Variables d'environnement ===
BOT_TOKEN = os.environ["BOT_TOKEN"]
GROUP_ID = int(os.environ["GROUP_ID"])

bot = telebot.TeleBot(BOT_TOKEN)
scheduler = BackgroundScheduler()

# === Bienvenue ===
@bot.message_handler(content_types=['new_chat_members'])
def welcome_user(message):
    for user in message.new_chat_members:
        username = f"@{user.username}" if user.username else user.first_name
        welcome_msg = (
            f"🎉 Bienvenue {username} dans *KevyPronostic* !\n\n"
            "Tu es ici pour gagner, apprendre et progresser chaque jour 📈🔥.\n"
            "Les membres actuels peuvent réagir à ce message pour souhaiter la bienvenue 🫂🤝 !\n\n"
            "🧠 Analyse + 🎯 Précision = 📊 Résultat 💵"
        )
        bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

# === Au revoir ===
@bot.message_handler(content_types=['left_chat_member'])
def goodbye_user(message):
    user = message.left_chat_member
    username = f"@{user.username}" if user.username else user.first_name
    bye_msg = (
        f"😢 {username} a quitté *KevyPronostic*...\n"
        "On espère te revoir bientôt parmi nous 💔.\n"
        "Bonne chance dans tes paris ! 🍀"
    )
    bot.send_message(message.chat.id, bye_msg, parse_mode='Markdown')

# === Message automatique du matin ===
def send_morning_message():
    now = datetime.now(pytz.timezone('Africa/Abidjan'))
    greeting = (
        "☀️ Bonjour la famille KevyPronostic ! 🤠💸\n\n"
        "Nouvelle journée, nouveaux gains 🧠📊\n"
        "Reste focus et ose croire 💯🔥"
    )
    poll_question = "Prêt pour les gains d'aujourd'hui ? 🤞🏼🥲"
    options = ["Oui 🫂😋", "Non 🙂‍↔️😩", "Dans un instant 🕝😎"]
    bot.send_message(GROUP_ID, greeting)
    bot.send_poll(GROUP_ID, poll_question, options, is_anonymous=False)

# === Message automatique du soir ===
def send_night_message():
    now = datetime.now(pytz.timezone('Africa/Abidjan'))
    motivation = (
        "🌙 La journée touche à sa fin...\n\n"
        "Qui ne risque rien 🙅🏼‍♂️ n'a rien ❌\n"
        "C'est quand tu sais pas que t'es en danger que t'es en danger,\n"
        "Si non si tu sais, tu n'es plus en danger 😎\n\n"
        "💤 Bonne nuit à vous ! 💤"
    )
    poll_question = "Ta journée a été ?"
    options = ["🎯 Gain ✅", "😓 Perte ❌", "🔁 Équilibre"]
    bot.send_message(GROUP_ID, motivation)
    bot.send_poll(GROUP_ID, poll_question, options, is_anonymous=False)

# === Planification automatique ===
scheduler.add_job(send_morning_message, 'cron', hour=7, minute=30, timezone='Africa/Abidjan')
scheduler.add_job(send_night_message, 'cron', hour=22, minute=30, timezone='Africa/Abidjan')
scheduler.start()

# === Fallback handler ===
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(message.chat.id, "😊 Je suis KevyBot, prêt à te motiver et te guider chaque jour !")

# === Keep Alive & Launch ===
keep_alive()
print("KevyBot est actif 🔥")
bot.infinity_polling()
