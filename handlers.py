from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from keyboards import main_kb, second_kb
from create_bot import bot
from acetone_api import ask_acetone
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_stikerset import process_sticker_image, generate_pack_name, get_bot_username
import os

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, этот бот умеет удалять фон изображения и создавать стикеры',
                          reply_markup=main_kb())


class RemoveBackground(StatesGroup):
    get_photo = State()
    
@start_router.message(F.text =='📝 Удалить фон изображения') 
async def remove_background(message: Message, state = FSMContext):
    await message.answer('Отправьте изображение на котором нужно удалить фон')
    await state.set_state(RemoveBackground.get_photo)


@start_router.message(RemoveBackground.get_photo, F.photo)
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
    await message.answer("Ваше изображение готово", reply_markup=main_kb())
    


class StickerCreation(StatesGroup):
    name = State()
    first_sticker = State()
    stickers = State()

@start_router.message(F.text == "📚 Создать стикерпак")
async def start_create_stikers(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте название для вашего стикерпака") 
    await state.set_state(StickerCreation.name)

@start_router.message(StickerCreation.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        "Отлично! Теперь отправьте первый стикер для пака (изображение)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(StickerCreation.first_sticker)

@start_router.message(StickerCreation.first_sticker, F.photo)
async def process_first_sticker(message: Message, state: FSMContext):
    try:
        file_path = f"temp/{message.photo[-1].file_id}.png"
        await bot.download(message.photo[-1].file_id, destination=file_path)
        
        processed_path = process_sticker_image(file_path)
        
        data = await state.get_data()
        user_id = message.from_user.id
        bot_username = await get_bot_username()
        pack_name = await generate_pack_name(user_id, bot_username)
        
        await bot.create_new_sticker_set(
            user_id=user_id,
            name=pack_name,
            title=data['title'],
            stickers=[{
                'sticker': FSInputFile(processed_path),
                'emoji_list': ['🎨'],
                'format': 'static'
            }],
            sticker_format='static'
        )
        
        await state.update_data(pack_name=pack_name)
        os.remove(processed_path)
        
        await message.answer(
            "Стикерпак создан! Отправьте ещё стикеры или нажмите кнопку для завершения",
            reply_markup=second_kb()
        )
        await state.set_state(StickerCreation.stickers)
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {str(e)}",
            reply_markup=main_kb()
        )
        await state.clear()


@start_router.message(StickerCreation.stickers, F.photo)
async def process_sticker(message: Message, state: FSMContext):
    try:
        file_path = f"temp/{message.photo[-1].file_id}.png"
        await bot.download(message.photo[-1].file_id, destination=file_path)
        
        processed_path = process_sticker_image(file_path)
        
        data = await state.get_data()
        pack_name = data['pack_name']
        user_id = message.from_user.id
        
        await bot.add_sticker_to_set(
            user_id=user_id,
            name=pack_name,
            sticker={
                'sticker': FSInputFile(processed_path),
                'emoji_list': ['🎨'],
                'format': 'static'
            }
        )
        
        os.remove(processed_path)
        
        await message.answer(
            "Стикер успешно добавлен! Отправьте ещё один или нажмите кнопку для завершения",
            reply_markup=second_kb()
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при добавлении стикера: {str(e)}")
        await state.clear()

@start_router.message(StickerCreation.stickers, F.text == "✅ Завершить создание")
async def finish_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    pack_name = data['pack_name']
    await message.answer(
        f"Ваш стикерпак готов!\nt.me/addstickers/{pack_name}",
        reply_markup=main_kb()
    )
    await state.clear()

@start_router.message(StickerCreation.first_sticker)
@start_router.message(StickerCreation.stickers)
async def wrong_input(message: Message):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте изображение для стикера")