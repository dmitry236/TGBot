from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from keyboards import main_kb
from create_bot import bot
from acetone_api import ask_acetone
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, этот бот умеет удалять фон изображения и создавать стикеры',
                          reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text =='📝 Удалить фон изображения') 
async def remove_background(message: Message):
    await message.answer('Отправьте изображение на котором нужно удалить фон')

@start_router.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1] 
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)
    
    with open("downloaded_photo.jpg", "wb") as new_file:
        new_file.write(downloaded_file.read())

    ask_acetone("downloaded_photo.jpg") 
    
    await message.answer_document(document=FSInputFile('output.png'))
    


class StickerCreation(StatesGroup):
    name = State()
    title = State()
    stikers = State()

@start_router.message(F.text == "📚 Создать стикерпак")
async def start_create_stikers(message: Message, state: FSMContext):
    await message.answer('Выберите короткое название, которое ' \
    'будет использоваться в адресе Вашего набора. Например, ' \
    'для этого набора используется короткое название «Animals»:\
    https://telegram.me/addstickers/Animals') 
    await state.set_state(Form.name)

     



