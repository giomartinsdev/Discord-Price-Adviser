import discord
import re
import asyncio

async def start(bot_id, id_usu, data_prod, data_values):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    def extract_price(mensagem):
        price = re.compile(r'R\$(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)')
        finded_price = price.findall(mensagem)
        if finded_price:
            return float(finded_price[0].replace('.', '').replace(',', '.'))

    @client.event
    async def on_ready():
        print(f"Produtos ->{data_prod}")
        print(f"Valores ->{data_values} \n")

        print(f'Bot conectado como {client.user}.')

    @client.event
    async def on_message(message):
        message_cleaned = message.content.lower()
        price = extract_price(message.content)
        if message.author == client.user:
            return
        i = 0
        for content in data_prod:
            if content in message_cleaned and price <= data_values[i]:
                user = await client.fetch_user(id_usu)
                await user.send(message.content)
                print(f"DEBUG: KEY: {content} -> TRIGGER: {price}")
            i = i + 1

    await client.start(bot_id)


if __name__ == '__main__':
    data_prod = []
    data_values = []
    menu = True
    while (menu):
        match input("Gostaria de inserir algum produto? (S/N): ").lower():
            case "s":
                data_prod.append(input("Escreva o produto que gostaria de ser notificado: ").lower())
                data_values.append(float(input("Até quanto gostaria de ser notificado?: ")))
                validate = True
                pass
            case "n":
                print("Okay, passando...")
                validate = True
                pass
            case _:
                print("Valor invalido")
                validate = False

        if (validate != False):


            bot_id = '' # id do bot
            id_usu = '' # id da conta pra ser notificada


            print(""" _____                         ___       __      
| ___ \      (_)              / _ \     | |       (_)                             |   By giomartinsdev
| |_/ / _ __  _   ___   ___  / /_\ \  __| |__   __ _  ___   ___  _ __             | github.com/giomartinsdev
|  __/ | '__|| | / __| / _ \ |  _  | / _` |\ \ / /| |/ __| / _ \| '__|            |
| |    | |   | || (__ |  __/ | | | || (_| | \ V / | |\__ \|  __/| |               |
\_|    |_|   |_| \___| \___| \_| |_/ \__,_|  \_/  |_||___/ \___||_|   
""")
            asyncio.run(start(bot_id, id_usu, data_prod, data_values))
