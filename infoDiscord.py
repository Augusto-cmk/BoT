import discord
from discord.ext.commands import Bot
from discord.flags import Intents
import pandas as pd
import asyncio

def remove_quote(s):
    s=str(s).split("'")
    s="".join(s)
    return s

def remove_quote_id(s,id):
    s=str(s).split("'")
    s="".join(s)
    s=s+str(id)
    return s


class MyBot(Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.userBot = None
        self.comandos = ["&savedf","&senddf","&creatdf","&resetdf","&message"]
        self.respostas = {
                    "&savedf":"Salva o dataframe para atualizar o arquivo",
                    "&senddf":"Envia o arquivo com os dados do servidor",
                    "&creatdf":"Cria um dataframe novo caso ocorra algum problema",
                    "&resetdf":"Reseta os dados existentes no arquivo",
                    "&message":"Envia um feedback com a quantidade de mensagens do canal",
                    "&mymessage":"Envia um feedback com a quantidade de mensagens que você enviou no canal"
                }
        try:
            self.df = pd.read_csv("info_discord.csv").drop(['Unnamed: 0'],axis=1)
        except Exception:
            self.df = pd.DataFrame(columns=["ID","message","cargo","username_insert","channel_insert","server_insert"])
            self.df.to_csv("info_discord.csv")
    
    async def on_ready(self):
        self.userBot = self.user

    async def on_message(self,message):
        
        if("&" not in message.content and message.author != self.userBot):
            channel_insert=remove_quote_id(str(message.channel.name),str(message.channel.id))
            server_insert=remove_quote_id(str(message.guild),str(message.guild.id))
            username_insert=remove_quote(str(message.author.name))
            mensagem = message.content
            cargo = message.author.roles[-1].name
            id = message.author
            self.df.loc[len(self.df)] = [id,mensagem,cargo,username_insert,channel_insert,server_insert]
        else:
            if message.content == "&savedf":
                self.df.to_csv("info_discord.csv")
                await message.channel.send("Dataframe salvo com sucesso!")
            
            elif message.content == "&senddf":
                await message.channel.send(file=discord.File("info_discord.csv"))
            
            elif message.content == "&creatdf":
                try:
                    pd.read_csv("info_discord.csv")
                    await message.channel.send("O arquivo csv já existe!")
                except Exception:
                    self.df = pd.DataFrame(columns=["ID","message","cargo","username_insert","channel_insert","server_insert"])
                    self.df.to_csv("info_discord.csv")
                    await message.channel.send("O arquivo csv criado com sucesso!")

            elif message.content == "&resetdf":
                self.df = pd.DataFrame(columns=["ID","message","cargo","username_insert","channel_insert","server_insert"])
                self.df.to_csv("info_discord.csv")
                await message.channel.send("Arquivo csv resetado com sucesso!")

            elif message.content == "&message":
                qtdMensagens = self.df[self.df['channel_insert'] == remove_quote_id(str(message.channel.name),str(message.channel.id))]['message'].size
                await message.channel.send(f"Foram enviadas {qtdMensagens} mensagens neste canal")

            elif message.content == "&help":
                resposta = ""
                for comando in self.comandos:
                    resposta += f"Comando: {comando} - {self.respostas[comando]}\n"

                await message.channel.send(resposta)

bot = MyBot(command_prefix="&",intents=discord.Intents.all())
bot.run('MTAzNDY2MzkyNDkxOTk3NTk0Nw.G66rpv.DWBCtzhEMOorEKk_9nvY60lNVT83ecvJkoB7cI')