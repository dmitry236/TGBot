from create_bot import bot
from PIL import Image
import random
import os

async def get_bot_username():
    bot_info = await bot.get_me()
    return bot_info.username

async def generate_pack_name(user_id: int, bot_username: str) -> str:
    random_id = random.randint(1, 999999)
    return f"pack{user_id}_{random_id}_by_{bot_username}"

def process_sticker_image(input_path: str) -> str:
    output_path = input_path.replace('.png', '_processed.png')
    with Image.open(input_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        new_img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        
        ratio = min(512.0 / img.width, 512.0 / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        x = (512 - new_size[0]) // 2
        y = (512 - new_size[1]) // 2
        
        new_img.paste(resized_img, (x, y), resized_img)
        
        new_img.save(output_path, 'PNG')
    
    os.remove(input_path)
    return output_path