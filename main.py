import os
import qrcode
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await message.answer(f'Привет! Я бот QRcode Creator.\nЧтобы я смог сделать для тебя QR код отправь мне '
                         f'текст, из которого хочешь сделать QR код.')
    await message.answer('ВНИМАНИЕ\nДлина текста не должна превышать 400 символов.')


@dp.message_handler()
async def send_qr(message: types.Message):
    data = message.text
    if len(data) > 400:
        await bot.send_message(chat_id = message.chat.id,
                               text = 'Длина текста превышает лимит в 400 символов!\nПовторите попытку')
    else:
        img = qrcode.make(data)
        file_name = 'qr.png'
        img.save(file_name)
        photo = open(f'{file_name}', 'rb')
        await bot.send_photo(chat_id = message.chat.id, photo = photo)
        path = os.path.join(os.path.abspath(os.path.dirname(file_name)),f'{file_name}')
        os.remove(path)

if __name__ == '__main__':
    executor.start_polling(dp)