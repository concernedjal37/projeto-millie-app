
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
ARQUIVO:       [Telegram_API.py]
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
import json
import os
from dotenv import load_dotenv, find_dotenv
from google.genai import types
from google import genai
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import Objetos
import threading
import mariadb

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
# Estabelecendo variáveis para thread
executando = threading.Event()
thread_tarefa = None


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
        print(f'Mensagem encontrada.' + '*'*40 + '\n')
        if message.text:
            return message

# Funçao de Prompt do Gemini para Cotação de Milhas
# Resposta do Gemini estruturada em JSON

# Função de Prompt do Gemini para Transferências Bonificadas de Milhas
# Resposta do Gemini estruturada em JSON


def Prompt_Gemini_Cotacao(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Objetos.Cotacao
            }
        )

        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Cotacao
        return Objetos.Cotacao.model_validate_json(response.text)

    except Exception as e:
        print("Erro na conexão com o Gemini ou na validação do JSON:")
        print(e)
        return None


def Prompt_Gemini_Transferencia(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Objetos.Transferencia_Bonificada
            }
        )
        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Transferencia_Bonificada
        return Objetos.Transferencia_Bonificada.model_validate_json(response.text)
    except Exception as e:
        print("Erro na conexão com o Gemini ou na validação do JSON:")
        print(e)
        return None


def Prompt_Gemini_Compra(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Objetos.Compra_Bonificada
            }
        )
        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Compra_Bonificada
        return Objetos.Compra_Bonificada.model_validate_json(response.text)
    except Exception as e:
        print("Erro na conexão com o Gemini ou na validação do JSON:")
        print(e)
        return None


def Prompt_Gemini_Adesao(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Objetos.Adesao_Bonificada
            }
        )
        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Adesao_Bonificada
        return Objetos.Adesao_Bonificada.model_validate_json(response.text)
    except Exception as e:
        print("Erro na conexão com o Gemini ou na validação do JSON:")
        print(e)
        return None


def loop_trabalho():
    """Função que roda 24/7 enquanto o evento estiver ativo."""
    print("[SISTEMA] Thread iniciada.")

    while executando.is_set():
        async def main():
            # Instanciando os Link dos canais do Telegram
            Canal_Cota = 'https://t.me/cotacoes'
            Canal_Pronto_voar = 'https://t.me/canalpontospravoar'

            # Entrando No Canal de Cotações de Milhas
            await Entrar_Canal(Telegram_Client, Canal_Cota)
            await Entrar_Canal(Telegram_Client, Canal_Pronto_voar)

            print(
                '*'*40 + 'Coletando dados iniciais, primeiro acesso aos canais do Telegram...')
            # Coletando última mensagem de Cotação de milhas
            print('Coletando última mensagem de Cotação de milhas')
            Palavra_Procura = 'Tendencias'
            mensagem_Cota = await Procura_mensagem(Telegram_Client, Canal_Cota, limit, Palavra_Procura)

            # Coletando última mensagem de Transferência Bonificada
            print('Coletando última mensagem de Transferência Bonificada')
            Palavra_Procura = 'Transferência bonificada'
            mensagem_Transf = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

            # Coletando última mensagem de Compra Bonificada
            print('Coletando última mensagem de Compra Bonificada')
            Palavra_Procura = 'Compra de milhas'
            mensagem_Compra = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

            # Coletando última mensagem de Adesão a Clube Bonificada
            print('Coletando última mensagem de Adesão a Clube Bonificada')
            Palavra_Procura = 'Adesão'
            mensagem_Adesao = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

            while True:
                # Menu de opções do Teste da API do Telegram

                print('Menu Teste Telegram API')
                print('-'*40)
                print('1 - Perguntar ao Gemini sobre Cotação de Milhas')
                print('2 - Perguntar ao Gemini sobre Transferência Bonificada')
                print('3 - Perguntar ao Gemini sobre Compra Bonificada')
                print('4 - Perguntar ao Gemini sobre Adesão a Clube Bonificada')
                print('6 - Salvando dados de Cotação de Milhas')
                print('0 - Sair')
                Opcao = input('Escolha uma opção: ')
                # Executando a opção escolhida
                match Opcao:
                    case '1':
                        # Perguntando ao Gemini sobre Cotação de milhas
                        Prompt = mensagem_Cota.text
                        Resposta = Prompt_Gemini_Cotacao(Prompt)

                        # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                        if Resposta is not None:
                            print("\nResposta do Gemini:")
                            print("-" * 40)
                            Resposta.Print_Cota()
                    case '2':
                        # Perguntando ao Gemini sobre Transferência Bonificada
                        Prompt = mensagem_Transf.text
                        Resposta = Prompt_Gemini_Transferencia(Prompt)
                        # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                        if Resposta is not None:
                            print("\nResposta do Gemini:")
                            print("-" * 40)
                            Resposta.Print_Transf()

                        opcao = 0
                    case '3':
                        # Perguntando ao Gemini sobre Compra Bonificada
                        Prompt = mensagem_Compra.text
                        Resposta = Prompt_Gemini_Compra(Prompt)

                        # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                        if Resposta is not None:
                            print("\nResposta do Gemini:")
                            print("-" * 40)
                            Resposta.Print_Compra()
                    case '4':
                        # Perguntando ao Gemini sobre Adesão a clubes bonificada
                        Prompt = mensagem_Adesao.text
                        Resposta = Prompt_Gemini_Adesao(Prompt)

                        # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                        if Resposta is not None:
                            print("\nResposta do Gemini:")
                            print("-" * 40)
                            Resposta.Print_Adesao()

                    case '6':
                        # Salvando dados de Cotação de Milhas no banco de dados
                        try:
                            connection = mariadb.connect(
                                host="100.79.171.116",
                                port=3306,
                                database="Banco_da_Millie",
                                user="java_user",
                                password="50BMG"
                            )
                            cursor = connection.cursor()

                            # Query SQL com placeholders (?)
                            sql = """
                                INSERT INTO cotacoes (Plataforma, valor)
                                VALUES (?, ?)
                            """
                            cursor.execute(sql, (
                                Resposta.Plataforma,
                                Resposta.Media
                            ))
                            connection.commit()
                        except mariadb.Error as e:
                            print(
                                f"[ERRO] Erro ao salvar dados no banco de dados: {e}")
                        finally:
                            if 'connection' in locals():
                                connection.close()

        with Telegram_Client:
            Telegram_Client.loop.run_until_complete(main())
            executando.wait(timeout=5)
        print("[SISTEMA] Thread encerrada.")


def start():
    """Inicia a thread se ela não estiver ativa."""
    global thread_tarefa

    if thread_tarefa is not None and thread_tarefa.is_alive():
        print("[AVISO] A tarefa já está rodando!")
        return

    executando.set()
    thread_tarefa = threading.Thread(target=loop_trabalho, daemon=True)
    thread_tarefa.start()


def stop():
    """Para a thread com segurança."""
    if not executando.is_set():
        print("[AVISO] A tarefa não está rodando.")
        return

    print("[SISTEMA] Parando a thread...")
    executando.clear()
    if thread_tarefa:
        thread_tarefa.join()


if __name__ == "__main__":
    while True:
        comando = input("> ").strip().lower()

        if comando == "start":
            start()
        elif comando == "stop":
            stop()
        elif comando == "sair":
            stop()
            break
