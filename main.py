from re import I
import discord
import glob
import os
from discord.ext import commands
from discord import *
import requests
import colorama
from PIL import Image, ImageFont, ImageDraw
import winreg
import hashlib
import requests
import secrets
import argparse
intents=discord.Intents.default() 
intents.message_content = True
colorama.init()


bot = commands.Bot(command_prefix = "!", description= "DataSearch v0.1", intents=intents)
os.chdir('/Databases')
list_doss_combo = len(os.listdir('/Databases/DB Combolist'))
list_doss_ecoleFR = len(os.listdir('/Databases/DB Ecoles FR'))
list_doss_jeux = len(os.listdir('/Databases/Jeux'))
list_doss_mails = len(os.listdir('/Databases/Mails'))
list_doss_reseaux_sociaux = len(os.listdir('/Databases/Reseaux sociaux'))
list_doss_reseaux_others = len(os.listdir('/Databases/Sites Randoms'))
list_doss = list_doss_combo + list_doss_ecoleFR + list_doss_jeux + list_doss_mails + list_doss_reseaux_sociaux + list_doss_reseaux_others
list_doss_international = len(os.listdir('/Databases/Sites Randoms/2800 DB International/data'))
list_doss_fini = "Nombre de Databases Françaises : ``" + str(list_doss) + "``\nNombre de Databases International : ``" + str(list_doss_international) + "``"
list_doss_total = int(list_doss) + int(list_doss_international)
myrz_key = "b958a769042ea5f76af57d7614e7f3a1"

cookies = {'login': 'nppr22',
           'user_hash': 'a7ebc0faad8eb7c9dda59b2272226c1f',
           'PHPSESSID': 'kn2pc9s2m17k19o8r7fhbkpio5'}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
def key_generate():
    random_key = secrets.token_hex(16)
    print(f"[~]Activating {random_key}")
    key_activation(random_key)

def key_default():
    regedit = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    regedit_key = winreg.OpenKey(regedit, "SOFTWARE\Microsoft\Cryptography")
    computer_guid = winreg.QueryValueEx(regedit_key, "MachineGuid")[0]
    data = computer_guid.encode("utf-16-le")
    default_key = hashlib.md5(
        data).hexdigest() 
    print(f"[~]Activating {default_key}")
    key_activation(default_key)




def key_activation(key):
    global key_transfer
    key_transfer = key
    req = requests.post('https://antipublic.one/main/account.php', data={'your_key': key}, cookies=cookies,headers=headers)
    data = req.json()
    if data["success"]:
        print(f"{colorama.Fore.LIGHTGREEN_EX}[+]{key}")
        
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}[-]Error, key {key} has expired")

key_generate()


myrz_key=str(key_transfer)
myrz_check = "b958a769042ea5f76af57d7614e7f3a1"
myrz_key = myrz_key
if myrz_key == myrz_check:
    print("Clé non genéré")
else:
    print("Clé OK " + myrz_key)


@bot.event
async def on_ready():
    print("Ready !")

@bot.command()
async def db_info(ctx):
    embed=discord.Embed(title="Information sur le bot", url="https://discord.gg/EeMb88EAUr", description=list_doss_fini, color=0xFF5733)
    await ctx.send(embed=embed)




@bot.command()
async def coucou(ctx):
    print("coucou")
    await ctx.send("Coucou")


@bot.command()
async def mail(ctx, mail):
    mail_text = "Recherche de " + mail + " dans " + str(list_doss_total) + " Databases..."
    reachable = "Le mail a été trouver !\n"
    embed=discord.Embed(title=mail_text, color=0x4d72b8)
    embed.set_footer(text="© Datasearch 2022")
    await ctx.send(embed=embed)
    fichier = open("combine.txt","r")#recherche local
    finito_compress = "Le mail est introuvable dans la Database local :'("
    for ligne in fichier:
        if mail in ligne:
            finito_compress = reachable + ligne
            await ctx.send(finito_compress)    
        print(reachable)
        print(ligne)
       
    req = requests.get(f'https://antipublic.one/api/email_search.php?key={myrz_key}&email={mail}',headers=headers)
    data = req.json()
    if data["success"]:
        embed=discord.Embed(title="_Le mail a été trouvé !_", color=0xFF0000)
        embed.add_field(name="Message envoyé.",value="Va voir dans tes messages privés je t'ai envoyé le résulat de ta recherche :tada:", inline=False)
        embed.set_author(name="DataSearch", url="https://discord.gg/sGtf9CQzyE", icon_url="https://voltastream.fr/datasearchlogo.png")
        embed.set_thumbnail(url="https://voltastream.fr/datasearchfull.png")
        await ctx.send(embed=embed)

        for combo in data["results"]:
            result = len(data["results"])
            embed=discord.Embed(title="_Clique ici pour rejoindre notre serveur_", url="https://discord.gg/EeMb88EAUr", color=0xFF0000)
            embed.add_field(name="** Résulats trouvés pour ta recherche :**", value= "``" + combo['line'] + "``", inline=True)
            embed.set_footer(text="Nombre de Résultats : " + str(len(data["results"])))
            embed.set_author(name="DataSearch", url="https://discord.gg/sGtf9CQzyE", icon_url="https://voltastream.fr/datasearchlogo.png")
            embed.set_thumbnail(url="https://voltastream.fr/datasearchfull.png")
            await ctx.author.send(embed=embed)

            print(f"[+]{combo['line']}")

    else:
        print("No more results")
        embed=discord.Embed(title="_Clique ici pour rejoindre notre serveur_", url="https://discord.gg/EeMb88EAUr", color=0xFF0000)
        embed.add_field(name="** Aucun résultat trouvé pour ta recherche :(**", value= "Contacte le staff si tu souhaites une recherche sur nos Databases Privés", inline=True)
        embed.set_footer(text="*Un supplément sera peut être demandé*")
        embed.set_author(name="DataSearch", url="https://discord.gg/sGtf9CQzyE", icon_url="https://voltastream.fr/datasearchlogo.png")
        embed.set_thumbnail(url="https://voltastream.fr/datasearchfull.png")
        await ctx.send(embed=embed)





























bot.run("MTAzMDkyNzA2ODY5Njk0ODgyNw.GnFzHN.P-r5bEJH8BtGpbpDZresxFd4EasBp-Nzrn7PNE")