import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from flask import Flask
from threading import Thread

# 1. SETUP WEB SERVER MINI (Agar Render Tidak Tidur)
app = Flask('')

@app.route('/')
def home():
    return "Server Berkah System Aktif 24 Jam!"

def run_web_server():
    # Render biasanya memberikan PORT otomatis di environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. SETUP TELEGRAM BOT ANDA
TOKEN = "8843551261:AAF5RZK4tFz9Gnmv_c-YIkYTeqx4896rMiE"
bot = telebot.TeleBot(TOKEN)

print("=== BERKAH SYSTEM BOT: MODE CLOUD DEPLOY ACTIVE ===")

def buat_menu_utama():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    tombol_cs = InlineKeyboardButton("🤖 Demo Bot CS / Toko Online", callback_data="demo_cs")
    tombol_scraping = InlineKeyboardButton("📂 Demo Bot Kirim Laporan Data (CSV)", callback_data="demo_scraping")
    tombol_sekolah = InlineKeyboardButton("🏫 Demo Bot Notifikasi Sekolah", callback_data="demo_sekolah")
    tombol_order = InlineKeyboardButton("📞 Hubungi Pengembang", url="https://t.me/iwan_developer")
    markup.add(tombol_cs, tombol_scraping, tombol_sekolah, tombol_order)
    return markup

@bot.message_handler(commands=['start'])
def kirim_sambutan(pesan):
    nama_user = pesan.from_user.first_name
    teks_sambutan = (
        f"Selamat datang {nama_user} di **Berkah System Automation**! 🚀\n\n"
        "Silakan **klik salah satu tombol di bawah ini** untuk mencoba langsung teknologi bot kami:"
    )
    bot.send_message(pesan.chat.id, teks_sambutan, reply_markup=buat_menu_utama(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def respon_tombol(call):
    if call.data == "demo_cs":
        teks_cs = "✨ **[SIMULASI BOT CS TOKO ONLINE]** ✨\n\nBot ini membalas otomatis 24 jam."
        bot.send_message(call.message.chat.id, teks_cs, reply_markup=buat_menu_utama(), parse_mode="Markdown")
    elif call.data == "demo_scraping":
        # Di Render nanti file CSV ini kita buat manual atau abaikan dulu untuk demo teks
        bot.send_message(call.message.chat.id, "⏳ **[SIMULASI AMBIL DATA]** Fitur laporan data sukses terintegrasi cloud!", reply_markup=buat_menu_utama())
    elif call.data == "demo_sekolah":
        teks_sekolah = "🔔 **[SIMULASI NOTIFIKASI SEKOLAH]** 🔔\n\nNotifikasi otomatis terkirim ke orang tua murid."
        bot.send_message(call.message.chat.id, teks_sekolah, reply_markup=buat_menu_utama(), parse_mode="Markdown")
    bot.answer_callback_query(call.id)

# 3. MENJALANKAN KEDUANYA BERSAMAAN (Web Server & Bot)
def jalankan_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Jalankan Web Server di thread (jalur latar belakang) pertama
    t = Thread(target=run_web_server)
    t.start()
    
    # Jalankan Bot Telegram di jalur utama
    jalankan_bot()
