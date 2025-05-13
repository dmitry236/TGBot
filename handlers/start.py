from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from keyboards.all_kb import main_kb
from create_bot import bot
from acetone_api import ask_acetone

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, этот бот умеет удалять фон изображения и создавать стикеры',
                          reply_markup=main_kb(message.from_user.id))
@start_router.message(F.text =='📝 Удалить фон изображения')
async def cmd_start_2(message: Message):
    await message.answer('Отправьте изображение на котором нужно удалить фон')


@start_router.message(F.photo)
async def handle_photo(message: Message):
    # Получаем информацию о фото
    photo = message.photo[-1]  # Берем последнее фото (самое высокое качество)
    
    # Скачиваем фото
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # Скачиваем файл
    downloaded_file = await bot.download_file(file_path)
    
    # Сохраняем фото локально (опционально)
    with open("downloaded_photo.jpg", "wb") as new_file:
        new_file.write(downloaded_file.read())
    
    # Здесь вы можете отправить фото в другой файл для обработки
    # Например, импортировать функцию из другого модуля и передать ей путь к файлу
    
    # Вариант 1: передать путь к сохраненному файлу
    #result = ask_acetone("./downloaded_photo.jpg")
    ask_acetone("downloaded_photo.jpg") 
    #image = Image.open("output.png")
    
    
    # Вариант 2: передать байты изображения напрямую
    # downloaded_file.seek(0)  # Сбрасываем указатель в начало файла
    # result = process_image(downloaded_file.read())
    
    await message.answer_document(document=FSInputFile('output.png'))