import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

TOKEN = "8435170082:AAGXECObruJX0FB0jcTOw7ODQCP75GQqBsI"

# --- HÀM CÀO DỮ LIỆU ---
def get_du_doan():
    url = "https://atrungroi.com/du-doan-xsmb-1-11-2025-soi-cau-xo-so-mien-bac-01-11-2025.html"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Tìm đoạn có kết quả dự đoán
        div = soup.find("div", class_="col-12 col-md-8 col-lg-8")
        if not div:
            return "❌ Không tìm thấy dữ liệu dự đoán."

        text = div.get_text(separator="\n", strip=True)
        return text[:2000]  # Giới hạn cho Telegram
    except Exception as e:
        return f"Lỗi khi cào dữ liệu: {e}"

# --- LỆNH /start ---
def start(update, context):
    update.message.reply_text("🤖 Xin chào! Dùng lệnh /du_doan để xem dự đoán XSMB hôm nay.")

# --- LỆNH /du_doan ---
def du_doan(update, context):
    update.message.reply_text("🔍 Đang lấy dữ liệu dự đoán, vui lòng chờ...")
    data = get_du_doan()
    update.message.reply_text(data)

# --- CHẠY BOT ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("du_doan", du_doan))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()