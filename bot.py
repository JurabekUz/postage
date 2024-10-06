import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from environs import Env


from sqlite import Database

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
db = Database()

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqam jo'natish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)


@dp.message(F.text == '/help')
async def command_help_handler(message: Message) -> None:
    await message.answer("Salom")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # check user
    user = db.select_user(telegram_id=message.from_user.id)
    if not user:
        await message.answer(
            f"Assalomu alaykum, {html.bold(message.from_user.full_name)}!\nTugmadan foydalanib raqamingizni ulashing.",
            reply_markup=phone_keyboard
        )
    else:
        await message.answer(f"Assalomu alaykum, {html.bold(message.from_user.full_name)}!", reply_markup=ReplyKeyboardRemove())


@dp.message(F.contact)
async def contact_handler(message: Message) -> None:
    phone_number = message.contact.phone_number
    # send message
    await message.answer(f"Raqamingiz: {message.contact.phone_number}", reply_markup=ReplyKeyboardRemove())

    # add user
    try:
        pn = phone_number[:4]+" "+phone_number[4:6]+" "+phone_number[6:9]+" "+phone_number[9:11] + " " + phone_number[11:]
        db.add_user(id=message.from_user.id, telegram_id=message.from_user.id, phone_number=pn)

        # new inventories
        new_inventory_number = db.get_new_inventories(pn)
        print("new inv numbers >> : ", new_inventory_number)
        for i in new_inventory_number:
            await message.answer(f"Hurmatli mijoz!\nBuyurtmangiz muvaffaqiyatli qabul qilindi.\nBuyurtma raqami: {i[0]}")
    except Exception as err:
        await message.answer("Kutilmagan xatolik yuz berdi!\nIltimos qayta urinib ko'ring")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer("Iltimos botdan to'g'ri foydalaning!")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def on_startup_notify(bot):
    print("admins", ADMINS)
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await on_startup_notify(bot)

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
