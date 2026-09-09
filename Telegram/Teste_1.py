
"""
**__**
Projeto: Millie App 1.0
Equipe: **Desenvolvedores Universitários PUC - MG**

Gerente & Dev Back-end: Mateus Coelho Pires
Product Owner & Dev Back-end: Lamôni Leal Pereira
Dev Front-end: Arthur Utsch
Designer e Sup Front-end: Luiza Mariano
Analista QA e Administradora: Bruna Santiago
**__**
Arquivo: Teste_1.py
Descrição:
 
EMPRESA:       [Millie Tecnologies]
SISTEMA:       [Millie App - Desenvolvimento de Software]
MÓDULO:        []
ARQUIVO:       [Teste_1.py]
--------------------------------------------------------------------------
DESCRIÇÃO:  [Este arquivo contém as funções principais da integração]
 [da API Telegram com API Gemini, tem como objetivo gerar os objetos estruturados]
 [em JSON necesários para análise de dados, incluindo valores de cotação de milhas]
 [transferências, compras e adesões a clubes bonificadas.]
--------------------------------------------------------------------------
AUTOR:         [Lamoni Leal Pereira] <lamoni.pereira@sga.pucminas.br>
DATA CRIAÇÃO:  [09/09/2026]
--------------------------------------------------------------------------
DIREITOS:      (c) Copyright [2026] - [Millie Tecnologies]. 
               Todos os direitos reservados. Este código é confidencial e 
               propriedade interna da empresa.
==========================================================================
----------  --------------  -------  -------------------------------------
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from datetime import datetime
from google.genai import types
from google import genai
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import Teste_Objetos
import telethon
print('Abrindo Bibliotecas...')
print('Carregando variáveis de ambiente...')
# Carregando variáveis de ambiente do arquivo .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# instanciando o cliente do Telegram e do Gemini
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print('Variáveis de ambiente carregadas com sucesso.\n'+'*'*40)


print('Estabelecendo chaves de acesso...')
# Aplicando Chaves de API do Telegram
Telegram_Client = TelegramClient(
    "session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)
limit = 1
# Aplicando Chave de API do Gemini
Gemini_Client = genai.Client(api_key=GEMINI_API_KEY)
print('Chaves de acesso estabelecidas.\n'+'*'*40)
# Função para entrar em um canal do Telegram


async def Entrar_Canal(Telegram_Client, Canal):
    print('Entrando no Canal: ', Canal)
    try:
        await Telegram_Client(JoinChannelRequest(Canal))
        print(f"Sucesso em entrar no Canal {Canal}")
    except:
        print(f"falha ao entrar no Canal {Canal}")
        # print(f"Erro: {e}")

# Função de busca por mensagens em um canal do Telegram com base em uma palavra-chave


async def Procura_mensagem(Telegram_Client, Canal, limit, Palavra):
    print('Procurando mensagem...')
    async for message in Telegram_Client.iter_messages(Canal, limit, search=Palavra):
        print(f"Mensagem encontrada.\n")
        if message.text:
            return message

# Funçao de Prompt do Gemini para Cotação de Milhas
# Resposta do Gemini estruturada em JSON


def Prompt_Gemini_Cotacao(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.models.generate_content(
            model='gemini-3.5-flash',
            contents=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Teste_Objetos.Cotacao
            }
        )

        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Cotacao
        return response.parsed
    except Exception as e:
        print("Erro na conexão com o Gemini:")
        print(e)
        return None

# Função de Prompt do Gemini para Transferências Bonificadas de Milhas
# Resposta do Gemini estruturada em JSON


def Prompt_Gemini_Transferencia(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.models.generate_content(
            model='gemini-3.5-flash',
            contents=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Teste_Objetos.Transferencia_Bonificada
            }
        )
        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Transferencia_Bonificada
        return response.parsed
    except Exception as e:
        print("Erro na conexão com o Gemini:")
        print(e)
        return None


async def main():
    # Instanciando os Link dos canais do Telegram
    Canal_Cota = 'https://t.me/cotacoes'
    Canal_Pronto_voar = 'https://t.me/canalpontospravoar'
    Opcao = ' '  # Instanciando a variável de opção do menu
    while Opcao != '0':
        # Menu de opções do Teste da API do Telegram
        print('Menu Teste Telegram API')
        print('-'*40)
        print('1 - Entrar em todos os canais')
        print('2 - Pesquisar Cotação de Milhas')
        print('3 - Pesquisar Transferência Bonificada')
        print('4 - Perguntar ao Gemini sobre Cotação de Milhas')
        print('5 - Perguntar ao Gemini sobre Transferência Bonificada')
        print('0 - Sair')
        Opcao = input("Digite a Opção: ")

        # Executando a opção escolhida
        match Opcao:
            case '1':
                # Entrando No Canal de Cotações de Milhas
                await Entrar_Canal(Telegram_Client, Canal_Cota)
                await Entrar_Canal(Telegram_Client, Canal_Pronto_voar)
            case '2':
                # Coletando Última Mensagem de Cotação de milhas
                Palavra_Procura = 'Tendencias'
                mensagem_Cota = await Procura_mensagem(Telegram_Client, Canal_Cota, limit, Palavra_Procura)
                # Imprimindo a mensagem encontrada ou informando que não foi encontrada
                if mensagem_Cota is not None:
                    print(mensagem_Cota.text)
                else:
                    print('Mensagem Não Encontrada')
            case '3':
                # Coletando Última Mensagem de Transferência Bonificada
                Palavra_Procura = 'Transferência bonificada'
                mensagem_Transf = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)
                # Imprimindo a mensagem encontrada ou informando que não foi encontrada
                if mensagem_Transf is not None:
                    print(mensagem_Transf.text)
                else:
                    print('Mensagem Não Encontrada')
            case '4':
                # Coletando Última Mensagem de Cotação de milhas
                Prompt = mensagem_Cota.text
                Resposta = Prompt_Gemini_Cotacao(Prompt)
                # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                if Resposta is not None:
                    print("\nResposta do Gemini:")
                    print("-" * 40)
                    Resposta.Print_Cota()
            case '5':
                # Coletando Última Mensagem de Transferência Bonificada
                Prompt = mensagem_Transf.text
                Resposta = Prompt_Gemini_Transferencia(Prompt)
                # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                if Resposta is not None:
                    print("\nResposta do Gemini:")
                    print("-" * 40)
                    Resposta.Print_Transferencia()

with Telegram_Client:
    Telegram_Client.loop.run_until_complete(main())
