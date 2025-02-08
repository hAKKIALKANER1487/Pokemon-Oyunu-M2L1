import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import discord
class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['forms'][0]['name']  # Bir Pokémon'un adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"""Pokémon'un ismi: {self.name} Pokémon'un gücü: {self.power} Pokémon'un sağlığı: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None
                

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"         
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!"
        
  

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
     async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDovuscu Pokémon sağlık kullandı. Eklenen guc: {super_power}"
async def go(ctx):
    author = ctx.author.name  # Komutu çağıran kullanıcının adını alır
    if author not in Pokemon.pokemons:  # Bu kullanıcı için zaten bir Pokémon olup olmadığını kontrol ederiz
        chance = random.randint(1, 3)  # 1 ile 3 arasında rastgele bir sayı oluştururuz
        # Rastgele sayıya göre bir Pokémon nesnesi oluştururuz
        if chance == 1:
            pokemon = Pokemon(author)  # Standart bir Pokémon oluştururuz
        elif chance == 2:
            pokemon = Wizard(author)  # Wizard türünde bir Pokémon oluştururuz
        elif chance == 3:
            pokemon = Fighter(author)  # Fighter türünde bir Pokémon oluştururuz
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi göndeririz
        image_url = await pokemon.show_img()  # Pokémon görüntüsünün URL'sini alırız
        if image_url:
            embed = discord.Embed()  # Gömülü bir mesaj (embed) oluştururuz
            embed.set_image(url=image_url)  # Gömülü mesaja görüntüyü ekleriz
            await ctx.send(embed=embed)  # Görüntülü gömülü mesajı göndeririz
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")  # Görüntü yüklenemezse hata mesajı veririz
    else:
        await ctx.send("Zaten bir Pokémon oluşturmuşsun.")  # Kullanıcıya zaten bir Pokémon oluşturduğunu bildiririz

async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon'a sahip olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz
     


import asyncio

async def main():
    wizard = Wizard("Mike Tyson")
    fighter = Fighter("Muhammed Ali")

    # Pokémon bilgilerini göster
    wizard_info = await wizard.info()
    fighter_info = await fighter.info()
    print(wizard_info)
    print("#" * 10)
    print(fighter_info)
    print("#" * 10)

    # Saldırı senaryosu
    attack_result1 = await wizard.attack(fighter)
    attack_result2 = await fighter.attack(wizard)

    print(attack_result1)
    print(attack_result2)

# asyncio döngüsü ile çalıştır
asyncio.run(main())