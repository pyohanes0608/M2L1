import discord
from discord.ext import commands
import os, random
import requests
from config import token
import aiohttp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'You have logged in as {bot.user}')
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

def get_dog_image_url():    
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('dog')
async def dog(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)
    
def get_fox_image_url():    
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']

@bot.command('fox')
async def fox(ctx):
    image_url = get_fox_image_url()
    await ctx.send("Contoh gambar Fox!!!")
    await ctx.send(image_url)
    
    
def get_animal_image_url():    
    urls = ['https://random.dog/woof.json', 'https://random-d.uk/api/random']
    url = random.choice(urls)
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('animal')
async def animal(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_animal_image_url()
    await ctx.send(image_url)
    

# Gunakan kecocokan huruf kecil agar API tidak eror (misal: 'Pikachu' -> 'pikachu')
async def get_pokemon_image_url(pokemon_name): 
    # Pastikan .lower() hanya berjalan, dan tidak merusak angka
    clean_name = str(pokemon_name).lower().strip()
    url = f'https://pokeapi.co/api/v2/pokemon/{clean_name}' 
    
    async with aiohttp.ClientSession() as session: 
        async with session.get(url) as response: 
            if response.status == 200: 
                data = await response.json() 
                img_url = data['sprites']['front_default'] 
                return img_url 
            else: 
                return None


@bot.command(name='pokemon') 
async def pokemon(ctx, *, name: str = None): # Menambahkan '*' agar nama dengan spasi juga terbaca
    # 1. Validasi jika pengguna lupa mengetik input
    if name is None:
        await ctx.send("Silakan masukkan nama atau ID Pokémon! Contoh: `!pokemon pikachu` atau `!pokemon 25`")
        return

    # 2. Bersihkan input dari spasi yang tidak sengaja terketik
    pokemon_input = name.strip()

    # Kirim pesan tunggu ke user
    msg = await ctx.send(f"Sedang mencari data Pokémon: **{pokemon_input}**...")
    
    # 3. Panggil fungsi API
    image_url = await get_pokemon_image_url(pokemon_input) 
    
    if image_url:
        await msg.delete() # Hapus pesan tunggu
        await ctx.send(image_url) # Kirim link gambar Pokémon
    else:
        await msg.edit(content=f"Pokémon dengan nama/ID '**{pokemon_input}**' tidak ditemukan. Periksa kembali input Anda!")


# Daftar caption acak yang bisa Anda ubah sesuai keinginan
CAPTIIONS = [
    "Haha, so relatable! 🤣",
    "A modern-day masterpiece. 🎭",
    "This meme is sponsored by laziness. ☕",
    "When reality doesn't match expectations... 🥲",
    "Don't try this at home, guys! ❌",
    "POV: You're coding and run into an error. 💻"
]

@bot.command()
async def mem(ctx):
    # 1. Tentukan path folder 'images' secara absolut
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images')
    
    try:
        # 2. Pilih gambar secara acak
        img_name = random.choice(os.listdir(images_dir))
        img_path = os.path.join(images_dir, img_name)
        
        # 3. Pilih caption secara acak dari list di atas
        random_caption = random.choice(CAPTIIONS)
        
        # 4. Buka file dan kirim gambar BESERTA caption-nya
        with open(img_path, 'rb') as f:
            picture = discord.File(f)
            # Menggunakan parameter 'content' untuk teks caption
            await ctx.send(content=random_caption, file=picture)
            
    except FileNotFoundError:
        await ctx.send("Oh no, the 'images' folder wasn't found!")
    except IndexError:
        await ctx.send("The 'images' folder is empty; please fill it with images first!")

bot.run(token)
