import requests

from config.settings import BOT_TOKEN
from inventory.models import Status


def generate_msg(inventory):
    match inventory.status:
        case Status.accepted:
            return f"Hurmatli mijoz!\nBuyurtmangiz muvaffaqiyatli qabul qilindi.\nBuyurtma raqami:{inventory.number}"
        case Status.sent:
            return f"Hurmatli mijoz!\n{inventory.number} raqamli buyurtmangiz yo'lga chiqdi."
        case Status.delivered:
            return f"Hurmatli mijoz!\n{inventory.number} raqamli buyurtmangiz {inventory.recipient.name} ulashish punkitiga yetkazildi.\nManzil: {inventory.recipient.address}"
        case Status.closed:
            return f"Hurmatli mijoz!\n{inventory.number} raqamli buyurtmangiz muvaffaqiyatli yetkazildi.\nBizning xizmatlarimizdan foydalanganiz uchun rahmat!"


def send_telegram_message(chat_id, inventory):
    inventory.refresh_from_db()
    message = generate_msg(inventory)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    print(response)
    return response.json()
