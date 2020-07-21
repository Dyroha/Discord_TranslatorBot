import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from googletrans import Translator
from googletrans import LANGUAGES

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.')
translator = Translator()

@client.event
async def on_ready():
    print("Bot is ready.")

# Translates a sentence written after .translate
@client.command(aliases=['trans', 't', 'Translate'])
async def translate(ctx, *, text):
    print(text)
    trans = translator.translate(text)
    print(trans)
    await ctx.send(f'Original: {text}\nTranslated from {LANGUAGES.get(trans.src)}: {trans.text}')

# Translates the last number messages from the current chat and sends it to the quirying user
@client.command(aliases=['ta','above'])
async def translate_above(ctx, number):
    messages = await ctx.channel.history(limit=int(number)).flatten()
    me = ctx.author
    translatedList = []
    translatedText = ""
    for x in messages:
        if x.content[0] != "." and x.author.bot == False:
            translatedMessage = translator.translate(x.content)
            translatedList.append(f'{x.author.name} From: {LANGUAGES.get(translatedMessage.src)} \n{translatedMessage.text}')
    translatedText += ctx.channel.name + "\n"
    for x in range(len(translatedList)):
        translatedText += translatedList[-(x+1)] + "\n"
    await me.send(str(translatedText))



client.run(TOKEN)