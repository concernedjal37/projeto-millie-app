
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
from http import client
import json
import os
import time
from dotenv import load_dotenv, find_dotenv
from google.genai import types
from google import genai
from pydantic import TypeAdapter
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient, events
from telethon import utils
from typing import Type, TypeVar
from pydantic import BaseModel
import Objetos
import threading
import mariadb

print('[SISTEMA] Abrindo Bibliotecas...')
print('[SISTEMA] Carregando variáveis de ambiente...')

# Carregando variáveis de ambiente do arquivo .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# instanciando o cliente do Telegram e do Gemini
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(' Variáveis de ambiente carregadas com sucesso.\n'+'*'*40)


print('[SISTEMA] Estabelecendo chaves de acesso...')
# Aplicando Chaves de API do Telegram
Telegram_Client = TelegramClient(
    "session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)
limit = 1

# Aplicando Chave de API do Gemini
Gemini_Client = genai.Client(api_key=GEMINI_API_KEY)
print('[INFO]Chaves de acesso estabelecidas.\n'+'*'*40)
# Função para entrar em um canal do Telegram

# Estabelecendo variáveis para thread
# Manter a thread ativa enquanto o programa estiver em execução
programa_ativo = threading.Event()
# Manter a thread em standby enquanto não houver tarefas a serem executadas
iniciar_trabalho = threading.Event()
# Evento para parar o telethon 24/7
evento_parar = threading.Event()
# Salvar a referencia da thread para poder controlá-la (start, stop)
thread_tarefa = None

T = TypeVar('T', bound=BaseModel)


async def Entrar_Canal(Telegram_Client, Canal):
    print('Entrando no Canal: ', Canal)
    try:
        await Telegram_Client(JoinChannelRequest(Canal))
        print(f"Sucesso em entrar no Canal {Canal}")
    except:
        print(f"falha ao entrar no Canal {Canal}")
        # print(f"Erro: {e}")


async def Procura_mensagem(Telegram_Client, Canal, limit, Palavra):
    print('Procurando mensagem...')
    async for message in Telegram_Client.iter_messages(Canal, limit, search=Palavra):
        print(f'Mensagem encontrada.' + '*'*40 + '\n')
        if message.text:
            return message


def Prompt_Gemini_Cotacao(Prompt: str):
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Objetos.Cotacao]
            }
        )

        print('[SISTEMA] Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Cotacao
        adapter = TypeAdapter(list[Objetos.Cotacao])
        return adapter.validate_json(response.text)

    except Exception as e:
        print('[SISTEMA] Erro na conexão com o Gemini ou na validação do JSON:')
        print(e)
        return None


def Prompt_Gemini_Promocao(Prompt: str, Schema: Type[T]) -> T | None:
    print('Enviando Prompt para o Gemini...\nAguarde a resposta...')
    try:
        response = Gemini_Client.chats.create(
            model='gemini-3.5-flash-lite').send_message(
            message=Prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Schema
            }
        )
        print('Resposta recebida do Gemini.\n')
        # Retornando a resposta do Gemini como um objeto Transferencia_Bonificada
        return Schema.model_validate_json(response.text)

    except Exception as e:
        print("Erro na conexão com o Gemini ou na validação do JSON:")
        print(e)
        return None


async def executar_trabalho():
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
    Palavra_Procura = 'Balcão de milhas'
    mensagem_Cota = await Procura_mensagem(Telegram_Client, Canal_Cota, limit, Palavra_Procura)

    # Coletando última mensagem de Transferência Bonificada
    print('Coletando última mensagem de Transferência Bonificada')
    Palavra_Procura = 'Transferência bonificada'
    mensagem_Transf = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

    # Coletando última mensagem de Compra Bonificada
    print('Coletando última mensagem de Compra Bonificada')
    Palavra_Procura = 'Comprar milhas'
    mensagem_Compra = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

    # Coletando última mensagem de Adesão a Clube Bonificada
    print('Coletando última mensagem de Adesão a Clube Bonificada')
    Palavra_Procura = 'Adesão'
    mensagem_Adesao = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)

    selecao = input(
        "Escolha 'menu' de testes ou 'prog' para iniciar o programa 24/7 'Aguardando mensagens do Telegram'")
    if selecao == 'prog':
        print("[SISTEMA] Ciclo 24/7 iniciando...")
        print("[SISTEMA] Aguardando mensagem do Telegram chegar...")
        # Aguardando mensagens do Telegram (Período de Teste para melhorar resposta do Gemini)
        Entidade_Canal_Cota = await Telegram_Client.get_entity(Canal_Cota)
        Entidade_Canal_Pronto_voar = await Telegram_Client.get_entity(Canal_Pronto_voar)
        Entidade_me = await Telegram_Client.get_entity('me')

        id_cota = utils.get_peer_id(Entidade_Canal_Cota)
        id_pronto_voar = utils.get_peer_id(Entidade_Canal_Pronto_voar)
        id_me = utils.get_peer_id(Entidade_me)

        @Telegram_Client.on(events.NewMessage(chats=[id_cota, id_pronto_voar, id_me]))
        async def handler(event):
            print("[SISTEMA] Mensagem recebida! traduzindo...")

            # Verificando de qual canal a mensagem veio
            # Canal de Cotações Milhas possui apenas mensagens sobre cotações de milhas
            if event.chat_id == id_cota:
                print("[SISTEMA] Nova mensagem de Cotação de Milhas recebida.")
                mensagem_Cota = event.message.text

                # Perguntando ao Gemini sobre Cotação de milhas
                Instruções_Cota = (
                    "Instruções para extrair dados da mensagem a seguir:\n"
                    "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
                    "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
                    "3. Valor mínimo: Valor mínimo da cotação\n"
                    "4. Valor máximo: Valor máximo da cotação\n"
                    "5. Data: Data da mensagem (ex: 01/01/2024)\n"
                    "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
                )

                Prompt = Instruções_Cota + mensagem_Cota.text
                Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(
                    Prompt)

                # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                if Resposta is not None:
                    print("\nResposta do Gemini:")
                    print("-" * 40)

                    for cota in Resposta:
                        cota.Print_Cota()

            # Canal Prontos para voar possui diversas promoções e propagandas diferentes
            elif event.chat_id == id_pronto_voar:
                if 'Transferência bonificada' in event.message.text:
                    print(
                        "[SISTEMA] Nova mensagem de Transferência Bonificada recebida.")
                    mensagem_Transf = event.message.text
                    Instruções_Transf = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Origem: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Destino: Nome da agencia de milhas de destino (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n")
                    schema = Objetos.Transferencia_Bonificada
                    Prompt = Instruções_Transf + mensagem_Transf.text
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Transf()

                # Compra bonificada aparece com dois formatos diferentes, então é necessário verificar ambos
                elif ('Comprar milhas' in event.message.text) or ('Comprar pontos' in event.message.text):
                    print(
                        "[SISTEMA] Nova mensagem de Compra Bonificada recebida.")
                    mensagem_Compra = event.message.text
                    # Perguntando ao Gemini sobre Compra Bonificada
                    Instruções_Compra = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n"
                    )
                    schema = Objetos.Compra_Bonificada
                    Prompt = Instruções_Compra + mensagem_Compra.text
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Compra()

                elif 'Adesão' in event.message.text:
                    print(
                        "[SISTEMA] Nova mensagem de Adesão a Clube Bonificada recebida.")
                    mensagem_Adesao = event.message.text
                    # Perguntando ao Gemini sobre Adesão a clubes bonificada
                    Instruções_Adesao = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Milhas: Quantidade de milhas adquiridas na adesão\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n"
                    )
                    schema = Objetos.Adesao_Bonificada
                    Prompt = Instruções_Adesao + mensagem_Adesao.text
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Adesao()
                else:
                    print(
                        "[SISTEMA] Mensagem recebida, mas não corresponde a nenhuma categoria conhecida.")

            # Chat pessoal para testes dentro do fluxo 24/7
            elif event.chat_id == id_me:
                print("[SISTEMA] Identificando tipo de mensagem enviada.")
                await Telegram_Client.send_message('me', "Mensagem Recebida! Identificando tipo de promoção/cotção")
                if "Milhas" in event.message.text:
                    print(
                        "[SISTEMA] Nova mensagem de Cotação de Milhas recebida.")
                    await Telegram_Client.send_message('me', "Identificado Modelo de cotação de milhas")

                    mensagem_Cota = event.message.text

                    # Perguntando ao Gemini sobre Cotação de milhas
                    Instruções_Cota = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
                        "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
                        "3. Valor mínimo: Valor mínimo da cotação\n"
                        "4. Valor máximo: Valor máximo da cotação\n"
                        "5. Data: Data da mensagem (ex: 01/01/2024)\n"
                        "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
                    )

                    Prompt = Instruções_Cota + mensagem_Cota.text
                    Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(
                        Prompt)
                    await Telegram_Client.send_message('me', "Mensagem traduzida para JSON")
                    for cota in Resposta:
                        cota.Print_Cota()
                        cota_menssagem_telegram = cota.toString()
                        await Telegram_Client.send_message('me', cota_menssagem_telegram)

        async def aviso_periodico():
            while True:
                print('[SISTEMA] Aguardando mensagem do Telegram chegar...')
                await asyncio.sleep(20)  # Pausa assíncrona de 20 segundos

        # Inicia o aviso periódico em segundo plano
        tarefa_aviso = asyncio.create_task(aviso_periodico())

        try:
            # 4. Mantém o código aguardando mensagens 24/7 até ser desconectado/parado
            await Telegram_Client.run_until_disconnected()
        finally:
            # Cancela o aviso de 20s quando o programa for encerrado
            tarefa_aviso.cancel()

    elif selecao == 'menu':
        while True:
            # Menu de opções perguntar ao Gemini
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
                    Instruções_Cota = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
                        "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
                        "3. Valor mínimo: Valor mínimo da cotação\n"
                        "4. Valor máximo: Valor máximo da cotação\n"
                        "5. Data: Data da mensagem (ex: 01/01/2024)\n"
                        "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
                    )

                    Prompt = Instruções_Cota + mensagem_Cota.text
                    Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(
                        Prompt)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)

                        for cota in Resposta:
                            cota.Print_Cota()
                case '2':
                    # Perguntando ao Gemini sobre Transferência Bonificada
                    Instruções_Transf = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Origem: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Destino: Nome da agencia de milhas de destino (ex: Smiles, Latam Pass, etc.)caso houver vários usar palavra diversos\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n")

                    schema = Objetos.Transferencia_Bonificada
                    Prompt = Instruções_Transf + mensagem_Transf.text
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)
                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Transf()
                case '3':
                    # Perguntando ao Gemini sobre Compra Bonificada
                    Instruções_Compra = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n"
                    )
                    Prompt = Instruções_Compra + mensagem_Compra.text
                    schema = Objetos.Compra_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Compra()
                case '4':
                    # Perguntando ao Gemini sobre Adesão a clubes bonificada
                    Instruções_Adesao = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Milhas: Quantidade de milhas adquiridas na adesão\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n\n"
                    )
                    Prompt = Instruções_Adesao + mensagem_Adesao.text
                    schema = Objetos.Adesao_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

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
                case '0':
                    print("[SISTEMA] Encerrando o programa...")
                    break
                case _:
                    print("[AVISO] Opção inválida. Tente novamente.")
    else:
        print("[AVISO]Opção escolhida não é válida. retornando ao standby do programa.")


async def vigiar_parada():
    # Fica rodando ENQUANTO programa_ativo estiver ligado (.set())
    while programa_ativo.is_set():
        await asyncio.sleep(0.5)

  # Quando stop() chamar programa_ativo.clear(), ele cai aqui:
    print("[SISTEMA] Sinal de parada recebido. Desconectando Telegram...")
    await Telegram_Client.disconnect()


def loop_trabalho():
    #
    print("[SISTEMA] Iniciando a thread de trabalho...")
    while programa_ativo.is_set():
        print("[SISTEMA] Aguardando sinal para iniciar o trabalho")

        # Aguarda até que a thread seja sinalizada para iniciar o trabalho
        iniciar_trabalho.wait()

        if not programa_ativo.is_set():
            break  # Sai do loop se o programa não estiver mais ativo

        print("[SISTEMA] Comando start recebido.")
        try:

            with Telegram_Client:
                Telegram_Client.loop.run_until_complete(executar_trabalho())

        except Exception as e:
            print(
                f"[ERRO] Ocorreu um erro durante a execução do trabalho: {e}")

        finally:
            iniciar_trabalho.clear()    # Reseta o evento para aguardar o próximo start
            print("[SISTEMA] Telegram Client desconectado.")
            print("[SISTEMA] Trabalho concluído." + "*"*40)
            print("[SISTEMA] Sistema retornando ao estado de Standby" + "*"*40)
    print("[SITEMA] Programa encerrando definitivamente.\n"+"="*40)


def start():
    """Inicia a thread se ela não estiver ativa."""
    global thread_tarefa

    if thread_tarefa is None or not thread_tarefa.is_alive():
        programa_ativo.set()  # Sinaliza que o programa está ativo (Liga o vigia)

        thread_tarefa = threading.Thread(
            target=loop_trabalho, name="Thread_Telegram_API", daemon=True
        )
        thread_tarefa.start()
        print("[SISTEMA] Programa iniciado com sucesso." + "\n" * 3)
    else:
        print("[AVISO] A thread já está em execução.")

    if iniciar_trabalho.is_set():
        print("[SISTEMA] Trabalho em execução")
        return
    iniciar_trabalho.set()  # Sinaliza para iniciar o trabalho
    print("[SISTEMA] Trabalho iniciado com sucesso.")


def stop():
    global thread_tarefa

    if thread_tarefa is None or not thread_tarefa.is_alive():
        print("[AVISO] A thread não está em execução.")
        return
    print("[SISTEMA] Interrompendo execução do programa")

    # 1. Informa que a thread deve ser encerrada (isso aciona o vigiar_parada no Telethon)
    programa_ativo.clear()

    # 2. Libera o wait(), caso a thread esteja em standby
    iniciar_trabalho.set()

    # 3. Aguarda a thread terminar e o Telethon desconectar com segurança
    thread_tarefa.join()

    # 4. Reseta as flags e a thread para permitir um futuro 'start' limpo
    iniciar_trabalho.clear()
    thread_tarefa = None

    print("[SISTEMA] Programa Encerrado com sucesso." + "\n" * 3)


if __name__ == "__main__":
    while True:
        comando = input("Digite 'start', 'stop' ou 'sair': ").strip().lower()

        if comando == "start":
            start()
        elif comando == "stop":
            stop()
        elif comando == "sair":
            stop()
            break
        else:
            print("Comando inválido. Digite 'start', 'stop' ou 'sair'.")
