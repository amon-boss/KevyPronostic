import os
import telebot
from telebot.types import ChatMemberUpdated
from keep_alive import keep_alive
import schedule
import threading
import time
from datetime import datetime

# Variables d’environnement
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# ✅ Message automatique du matin à 7h30 GMT
def send_morning_poll():
    current_time = datetime.utcnow().strftime('%H:%M')
    if current_time == "07:30":
        bot.send_message(GROUP_ID,
            "🌞 *Bonjour la famille KevyFlow Pronostic !*\n\n"
            "Que la vibe soit bonne, que les cotes soient douces et que la chance nous accompagne aujourd’hui 🍀⚽️🔥\n\n"
            "💬 *Petit sondage pour se chauffer ce matin :*")
        bot.send_poll(
            chat_id=GROUP_ID,
            question="Prêt Pour les gains d'aujourd'hui ❓🤞🏼🥲",
            options=["✅ Oui🫂😋", "❌ Non 🙂‍↔️😩", "🕝 Dans un instant 😎"],
            is_anonymous=False,
            allows_multiple_answers=False
        )

# 🌙 Message automatique du soir à 22h00 GMT
def send_night_poll():
    current_time = datetime.utcnow().strftime('%H:%M')
    if current_time == "22:00":
        bot.send_message(GROUP_ID,
            "🌙 *Bonne nuit les légendes KevyFlow 💫 !*\n\n"
            "Quelle que soit l'issue de la journée, l’important c’est de rester focus 🎯\nDemain est un autre jour, une nouvelle opportunité de GAGNER 🏆🔥\n\n"
            "💬 *Comment s’est passée ta journée ?*")
        bot.send_poll(
            chat_id=GROUP_ID,
            question="Ta journée a été ? 🎲",
            options=["💸 Gagnante 😍🔥", "😕 Perte 🥲", "📉 Neutre ou mixte"],
            is_anonymous=False,
            allows_multiple_answers=False
        )

# Lancer les tâches planifiées en arrière-plan
def run_schedule():
    schedule.every(1).minutes.do(send_morning_poll)
    schedule.every(1).minutes.do(send_night_poll)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

# 🎉 Message de bienvenue quand un nouveau membre rejoint
@bot.chat_member_handler()
def welcome_new_member(message: ChatMemberUpdated):
    if message.new_chat_member.status == "member":
        user = message.new_chat_member.user
        if not user.is_bot:
            bot.send_message(GROUP_ID,
                f"🎉 Bienvenue @{user.username or user.first_name} dans *KevyFlow Pronostic* 🤑💸 !\n\n"
                "🔥 Tu es ici pour gagner, apprendre, vibrer, et faire partie de la team la plus chaude de tout Telegram !\n\n"
                "👥 Membres, mettez un max de réactions pour accueillir notre nouveau champion ! 😎💥\n\n"
                "*Que la chance soit avec toi !* 🍀🔥")

# 🔄 Message par défaut si utilisateur envoie un message au bot
@bot.message_handler(func=lambda msg: True)
def fallback(msg):
    bot.reply_to(msg, "👋 Hey ! Je suis KevyBot et je m’occupe du groupe 😉\nJe travaille en coulisse pour que tout roule 🧠💡")

# ✅ Lancement du bot
print("🤖 KevyFlow Pronostic Bot est en marche !")
keep_alive()
bot.infinity_polling()
