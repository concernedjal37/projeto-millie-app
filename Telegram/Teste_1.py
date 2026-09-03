from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from google import genai
from google.genai import types
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os
import asyncio


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
GEMINI_API_HASH = os.getenv("GEMINI_API_HASH")

Telegram_Client = TelegramClient(
    "session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)
limit = 1
Gemini_Client = genai.Client(
    api_key='GEMINI_API_HASH')


class Cotacao(BaseModel):
    Plataforma: str
    Agencia: str
    Media: float
    Data: datetime
    Monte: int

    def Print_Cota(self):
        print('--' * 40)
        print('Plataforma:', self.Plataforma)
        print('Agencia:', self.Agencia)
        print('Valor Médio Cotação: R$', self.Media)
        print('Montante Acumulado:', self.Monte)
        print(
            'Última Atualização:',
            self.Data.strftime("%d/%m/%Y %H:%M")
        )


async def Entrar_Canal(Telegram_Client, Canal):
    try:
        await Telegram_Client(JoinChannelRequest(Canal))
        print(f"Sucesso em entrar no Canal {Canal}")
    except:
        print(f"falha ao entrar no Canal {Canal}")
        # print(f"Erro: {e}")


async def Procura_mensagem(Telegram_Client, Canal, limit, Palavra):
    print('Procurando mensagem...')
    async for message in Telegram_Client.iter_messages(Canal, limit, search=Palavra):
        if message.text:
            return message


def Prompt_Gemini(Prompt: str):
    try:
        response = Gemini_Client.models.generate_content(
            model='gemini-3.5-flash',
            contents=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Cotacao
            }

        )

        return response.parsed
    except Exception as e:
        print("Erro na conexão com o Gemini:")
        print(e)
        return None


async def main():
    Canal_Cota = 'https://t.me/cotacoes'
    Opcao = ' '
    while Opcao != '0':

        print('Menu Teste Telegram API')
        print('-'*40)
        print('1 - Entrar no canal de Cotações')
        print('2 - Pesquisar no Canal de cotação uma mensagem de milhas')
        print('3 - Perguntar ao Gemini')
        print('0 - Sair')
        Opcao = input("Digite a Opção: ")
        match Opcao:
            case '1':
                # Entrando No Canal de Cotações de Milhas
                await Entrar_Canal(Telegram_Client, Canal_Cota)
            case '2':
                # Coletando Última Mensagem de Cotação de milhas
                Palavra_Procura = input("Digite a Palavra a se pesquisar: ")
                mensagem = await Procura_mensagem(Telegram_Client, Canal_Cota, limit, Palavra_Procura)
                if mensagem is not None:
                    print(mensagem.text)
                else:
                    print('Mensagem Não Encontrada')
            case '3':
                # Prompt = ("atualização de hoje venda de milhas na balcao de milhas,"" cotação da smiles é de R$15,90, 180000 milhas acumiladas")
                Prompt = mensagem.text
                Resposta = Prompt_Gemini(Prompt)

                if Resposta is not None:
                    print("\nResposta do Gemini:")
                    print("-" * 40)
                    Resposta.Print_Cota()
                # if cota is not None:
                #   cota.Print_Cota()
                # else:
                #   print("Não foi possível obter a cotação.")


with Telegram_Client:
    Telegram_Client.loop.run_until_complete(main())
