import discord
import re
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

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
                content = content.upper()
                user = await client.fetch_user(id_usu)
                await user.send(f"A mensagem foi enviada por conter a chave: {content}, pelo valor de: {price}R$\n{message.content}")
            i = i + 1

    await client.start(bot_id)

if __name__ == '__main__':
    # Lê os valores das variáveis de ambiente ou usa valores padrão
    bot_id = os.getenv('BOT_ID', '')
    id_usu = os.getenv('ID_USU', '')
    data_prod = os.getenv('DATA_PROD', '').split(',')
    data_values = list(map(float, os.getenv('DATA_VALUES', '').split(','))) 

    asyncio.run(start(bot_id, id_usu, data_prod, data_values))
