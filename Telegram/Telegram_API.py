
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
from datetime import datetime
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
"""Telegram_Client = TelegramClient(
    "session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)
"""
limit = 1
# 1. Faz o login/validação fora das funções (na Thread Principal)
with TelegramClient('session_millie_API', TELEGRAM_API_ID, TELEGRAM_API_HASH) as client_login:
    print("[SISTEMA] Login do Telegram validado com sucesso!")
# Ao sair do 'with', o client_login desconecta e libera o arquivo .session automaticamente!

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


# Função para entrar nos canais do telegram
async def Entrar_Canal(Telegram_Client, Canal):
    print('Entrando no Canal: ', Canal)
    try:
        await Telegram_Client(JoinChannelRequest(Canal))
        print(f"Sucesso em entrar no Canal {Canal}")
    except:
        print(f"falha ao entrar no Canal {Canal}")
        # print(f"Erro: {e}")


# Função para pesquisar as mensagens dentro do canal do telegram
async def Procura_mensagem(Telegram_Client, Canal, limit, Palavra):
    print('Procurando mensagem...')
    async for message in Telegram_Client.iter_messages(Canal, limit, search=Palavra):
        print(f'Mensagem encontrada.' + '*'*40 + '\n')
        if message.text:
            return message



# Função para requisitar ao Gemini estruturação da mensagem em JSON (Exclusivo para cotação)
def Prompt_Gemini_Cotacao(Prompt: str):
    print('[SISTEMA] Iniciando Prompt_Gemini_Cotacao...')
    count = 1
    while count <= 5:
        print(
            f'[SISTEMA] Tentativa {count}/ 5 para enviar o Prompt ao Gemini.')
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
            if count == 5:
                print(
                    '[SISTEMA] Número máximo de tentativas atingido. Falha ao enviar o Prompt ao Gemini.')
                return None
            count += 1

# Função para requisitar ao Gemini estruturação da mensagem em JSON (Todo tipo de promoção)


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

# Salvando dados de Cotação dentro do banco de dados


def Salvar_Cotacao_BD(cotacao: Objetos.Cotacao):
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

                    call criar_cota(%s, %s, %s, %s);
                """
        cursor.execute(sql, (
            cotacao.Plataforma,
            cotacao.Valor_min,
            cotacao.Valor_max,
            cotacao.Agencia
        ))
        connection.commit()
    except mariadb.Error as e:
        print(
            f"[ERRO] Erro ao salvar dados no banco de dados: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

# Salvando dados de qualquer promoção dentro do banco de dados


def Salvar_Promocao_BD(promocao: any):
    try:
        tipo = type(promocao).__name__
        print(f"[SISTEMA] Salvando promoção de {tipo} no banco de dados")
        connection = mariadb.connect(
            host="100.79.171.116",
            port=3306,
            database="Banco_da_Millie",
            user="java_user",
            password="50BMG"
        )
        cursor = connection.cursor()
        if tipo == 'Transferencia_Bonificada':
            cod_tipo = 1
        elif tipo == 'Compra_Bonificada':
            cod_tipo = 2
        elif tipo == 'Adesao_Bonificada':
            cod_tipo = 3
        else:
            print(f"[ERRO] Tipo de promoção desconhecido: {tipo}")
            return
        # Query SQL com placeholders (?)
        sql = """   
                call adicionar_promo(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
        cursor.execute(sql, (
            promocao.link,
            promocao.Origem,
            promocao.Data_Vencimento,
            promocao.Valor_milheiro_origem,
            cod_tipo,
            promocao.Destino if type(
                promocao).__name__ == 'Transferencia_Bonificada' else None,
            promocao.Porcent_High if type(
                promocao).__name__ != 'Adesao_Bonificada' else None,
            promocao.Porcent_Low if type(
                promocao).__name__ != 'Adesao_Bonificada' else None,
            promocao.Milhas if type(
                promocao).__name__ == 'Adesao_Bonificada' else None


        ))
        connection.commit()
        print("[SISTEMA] Dados enviados com sucesso")
    except mariadb.Error as e:
        print(
            f"[ERRO] Erro ao salvar dados no banco de dados: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

#função para apagar e verificar as promoções se necessario
def verificarPromocoes(horarioAtual: datetime):
    try:
        connection = mariadb.connect(
                    host="100.79.171.116",
                    port=3306,
                    database="Banco_da_Millie",
                    user="java_user",
                    password="50BMG"
                )
        cursor = connection.cursor()
        sql = "call Verificar_promos(%s)"
        cursor.execute(sql, (horarioAtual))
        connection.commit()
        #Essa parte será alterada depois para melhor tratamento de erros
    except mariadb.Error as e:
        print("Algo deu errado na operação de verificação")
    finally:
        if 'connection' in locals():
            connection.close()

"""Essa função Executa todos os trabalhos necessários para extração de dados do Telegram seja para testes ou execução 24/7
Função é executada apenas quando a thread responsável é ativada "start" digitado no terminal"""


async def executar_trabalho(Telegram_Client):
    # O programa está todo anexado com degubs para verificar atualização do programa em tempo real
    print("[SISTEMA] Conectando ao Telegram...")
    # A sessão do telegram já foi criada anteriormente, logo nesse comando somente se faz necessário conectar a sessão que foi iniciada
    await Telegram_Client.connect()
    # Verificação caso houver erro de conexão
    if not await Telegram_Client.is_user_authorized():
        print('[ERRO] Sessão não autenticada! Rode o login uma vez fora da thread.')
        return
    print('[SISTEMA] Conectado com sucesso! Entrando nos canais...')

    # Instanciando os Link dos canais do Telegram é possível tem muito mais que apenas dois, por equanto estamos limitando apenas a esses
    Canal_Cota = 'https://t.me/cotacoes'
    Canal_Pronto_voar = 'https://t.me/canalpontospravoar'

    # Entrando No Canal de Cotações de Milhas
    await Entrar_Canal(Telegram_Client, Canal_Cota)
    await Entrar_Canal(Telegram_Client, Canal_Pronto_voar)

    # Pesquisa inicial das promoções e cotações iniciais
    print(
        '*'*40 + 'Coletando dados iniciais, primeiro acesso aos canais do Telegram...')

    # Coletando última mensagem de Cotação de milhas
    print('Coletando última mensagem de Cotação de milhas')
    Palavra_Procura = 'balcão de milhas'
    mensagem_Cota = await Procura_mensagem(Telegram_Client, Canal_Cota, limit, Palavra_Procura)
    Prompt = (
        "Instruções para extrair dados da mensagem a seguir:\n"
        "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
        "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
        "3. Valor mínimo: Valor mínimo da cotação\n"
        "4. Valor máximo: Valor máximo da cotação\n"
        "5. Data: Data da mensagem (ex: 01/01/2024)\n"
        "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
    ) + mensagem_Cota.text
    # Solicitando Resposta do Gemini
    Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(Prompt)
    # Imprimindo e salvando valores de cotação
    if Resposta is not None:
        for cota in Resposta:
            cota.Print_Cota()
            Salvar_Cotacao_BD(cota)

    # Coletando última mensagem de Transferência Bonificada
    print('Coletando última mensagem de Transferência Bonificada')

    try:
        Palavra_Procura = 'transferência bonificada'
        mensagem_Transf = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)
        Prompt = (
            "Instruções para extrair dados da mensagem a seguir:\n"
            "Origem: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.)"
            "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
            "Destino: Nome da agencia de milhas de destino (ex: Smiles, Latam Pass, etc.)"
            "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
            "Porcent_high: Porcentagem máxima da bonificação\n"
            "Porcent_Low: Porcentagem mínima da bonificação\n"
            "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
            "link: Link para acessar a promoção\n"
            "Sempre acessar o link da promoção para confirmar os detalhes \n\n") + mensagem_Transf.text
        # Extraindo tipo de estrutura necessária para o Gemini enviar a Resposta
        schema = Objetos.Transferencia_Bonificada
        # Solicitando Resposta do Gemini
        Resposta = Prompt_Gemini_Promocao(Prompt, schema)
        if Resposta is not None:
            Resposta.Print_Transf()
            Salvar_Promocao_BD(Resposta)

        # Coletando última mensagem de Compra Bonificada
        print('Coletando última mensagem de Compra Bonificada')
        Palavra_Procura = 'comprar pontos'
        mensagem_Compra = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)
        Prompt = (
            "Instruções para extrair dados da mensagem a seguir:\n"
            "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
            "Porcent_high: Porcentagem máxima da bonificação\n"
            "Porcent_Low: Porcentagem mínima da bonificação\n"
            "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
            "link: Link para acessar a promoção\n"
            "Sempre acessar o link da promoção para confirmar os detalhes \n\n"
        ) + mensagem_Compra.text
        schema = Objetos.Compra_Bonificada
        Resposta = Prompt_Gemini_Promocao(Resposta, schema)
        if Resposta is not None:
            Resposta.Print_Compra()
            Salvar_Promocao_BD(Resposta)

        # Coletando última mensagem de Adesão a Clube Bonificada
        print('Coletando última mensagem de Adesão a Clube Bonificada')
        Palavra_Procura = 'adesão'
        mensagem_Adesao = await Procura_mensagem(Telegram_Client, Canal_Pronto_voar, limit, Palavra_Procura)
        Prompt = (
            "Instruções para extrair dados da mensagem a seguir:\n"
            "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
            "Milhas: Quantidade de milhas adquiridas na adesão\n"
            "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
            "link: Link para acessar a promoção\n"
            "Sempre acessar o link da promoção para confirmar os detalhes \n\n"
        ) + mensagem_Adesao.text
        schema = Objetos.Adesao_Bonificada
        Resposta = Prompt_Gemini_Promocao(Prompt, schema)
        if Resposta is not None:
            Resposta.Print_Adesao()
            Salvar_Promocao_BD(Resposta)
    except Exception as e:
        print(f"[ERRO] Erro no Scraping: {e}")
    print("Aperte Enter para continuar")
    # selecionando como vai rodar o programa, em Menu de opções para testar perguntas ao Gemini e BD ou Programa 24/7 padrão
    selecao = input(
        "Escolha 'menu' de testes ou 'prog' para iniciar o programa 24/7 'Aguardando mensagens do Telegram':\n").strip().casefold()

    

    #------------------------------Parte importante, é aqui que começa o programa de verdade!!!
    if selecao == 'prog':
        # Programa roda em loop infinito 24/7 para monitorar e extrair dados do Telegram
        print("[SISTEMA] Ciclo 24/7 iniciando...")
        print("\n\n[SISTEMA] Aguardando mensagem do Telegram chegar...")
        # Aguardando mensagens do Telegram (Período de Teste para melhorar resposta do Gemini)
        # Extraindo dados necessários dos canais utilizados
        Entidade_Canal_Cota = await Telegram_Client.get_entity(Canal_Cota)
        Entidade_Canal_Pronto_voar = await Telegram_Client.get_entity(Canal_Pronto_voar)
        Entidade_me = await Telegram_Client.get_entity('me')
        # salvando id(s) para conexão nos canais
        id_cota = utils.get_peer_id(Entidade_Canal_Cota)
        id_pronto_voar = utils.get_peer_id(Entidade_Canal_Pronto_voar)
        id_me = utils.get_peer_id(Entidade_me)

        # aguardando evento de nova mensagem em qualquer um dos canais listados
        @Telegram_Client.on(events.NewMessage(chats=[id_cota, id_pronto_voar, id_me]))
        async def handler(event):
            print("[SISTEMA] Mensagem recebida! traduzindo...")

            # Verificando de qual canal a mensagem veio
            # Canal de Cotações Milhas possui apenas mensagens sobre cotações de milhas
            if event.chat_id == id_cota:
                print("[SISTEMA] Nova mensagem de Cotação de Milhas recebida.")
                mensagem_Cota = event.message.text

                # Perguntando ao Gemini sobre Cotação de milhas
                Prompt = (
                    "Instruções para extrair dados da mensagem a seguir:\n"
                    "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
                    "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
                    "3. Valor mínimo: Valor mínimo da cotação\n"
                    "4. Valor máximo: Valor máximo da cotação\n"
                    "5. Data: Data da mensagem (ex: 01/01/2024)\n"
                    "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
                ) + mensagem_Cota

                Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(Prompt)

                # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                if Resposta:
                    print("\nResposta do Gemini:\n")
                    #print("-" * 40)
                    print("Tamanho de objetos da lista: " + str(len(Resposta)))

                    for cota in Resposta:
                        cota.Print_Cota()
                        Salvar_Cotacao_BD(cota)

            # Canal Prontos para voar possui diversas promoções e propagandas diferentes
            elif event.chat_id == id_pronto_voar:
                if 'transferência bonificada' in event.message.text.casefold():
                    print(
                        "[SISTEMA] Nova mensagem de Transferência Bonificada recebida.")
                    mensagem_Transf = event.message.text
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Origem: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Destino: Nome da agencia de milhas de destino (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes\n"
                        "valor_milheiro_agencia: pesquisar o valor do milheiro na agência de origem da promoção\n\n") + mensagem_Transf
                    schema = Objetos.Transferencia_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:\n")
                        print("-" * 40)
                        Resposta.Print_Transf()
                        Salvar_Promocao_BD(Resposta)

                # Compra bonificada aparece com dois formatos diferentes, então é necessário verificar ambos
                elif ('comprar milhas' in event.message.text.casefold()) or ('comprar pontos' in event.message.text.casefold()):
                    print(
                        "[SISTEMA] Nova mensagem de Compra Bonificada recebida.")
                    mensagem_Compra = event.message.text
                    # Perguntando ao Gemini sobre Compra Bonificada
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes \n"
                        "valor_milheiro_agencia: pesquisar o valor do milheiro na agência de origem da promoção\n\n"
                    ) + mensagem_Compra
                    schema = Objetos.Compra_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Compra()
                        Salvar_Promocao_BD(Resposta)

                elif 'adesão' in event.message.text.casefold():
                    print(
                        "[SISTEMA] Nova mensagem de Adesão a Clube Bonificada recebida.")
                    mensagem_Adesao = event.message.text
                    # Perguntando ao Gemini sobre Adesão a clubes bonificada
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Milhas: Quantidade de milhas adquiridas na adesão\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes\n"
                        "valor_milheiro_agencia: pesquisar o valor do milheiro na agência de origem da promoção\n\n"
                    ) + mensagem_Adesao
                    schema = Objetos.Adesao_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Adesao()
                        Salvar_Promocao_BD(Resposta)
                else:
                    print(
                        "[SISTEMA] Mensagem recebida, mas não corresponde a nenhuma categoria conhecida.")
            #chamar a função aqui
                verificarPromocoes(datetime.now(),)

            # Chat pessoal para testes dentro do fluxo 24/7
            # CHAT PESSOAL EXCLUSIVO PARA TESTES
            elif event.chat_id == id_me:
                print("[SISTEMA] Fonte: Chat Pessoal.\n" + "*"*40)
                await Telegram_Client.send_message(id_me, f"Mensagem Recebida! Identificando tipo...")
                # Identificando tipo Cotação de milhas
                if ("balcão de milhas") in event.message.text.casefold():
                    print(
                        "[SISTEMA] Nova mensagem de Cotação de Milhas recebida.")
                    await Telegram_Client.send_message(id_me, "Identificado Modelo de cotação de milhas")

                    mensagem_Cota = event.message.text
                    # Perguntando ao Gemini sobre Cotação de milhas
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "1. Plataforma: Nome da plataforma de venda de milhas (Balcao de milhas, Hotmilhas, etc.)\n"
                        "2. Agencia: Nome da agencia de milhas (ex: Smiles, Latam Pass, TudoAzul, etc.)\n"
                        "3. Valor mínimo: Valor mínimo da cotação\n"
                        "4. Valor máximo: Valor máximo da cotação\n"
                        "5. Data: Data da mensagem (ex: 01/01/2024)\n"
                        "6. Moeda: Moeda da cotação (ex: BRL, USD, EUR, etc.)\n\n"
                    ) + mensagem_Cota

                    print("[SISTEMA] Prompt gerado para o Gemini:\n" + Prompt)

                    # Gerando a lista de cotações para realizar Update no banco de dados
                    Resposta: list[Objetos.Cotacao] = Prompt_Gemini_Cotacao(
                        Prompt)
                    print("[SISTEMA] Resposta do Gemini recebida:\n")

                    await Telegram_Client.send_message(id_me, "Mensagem traduzida para JSON")
                    for cota in Resposta:
                        cota.Print_Cota()
                        cota_menssagem_telegram = cota.toString()
                        await Telegram_Client.send_message(id_me, cota_menssagem_telegram)
                    for cota in Resposta:
                        Salvar_Cotacao_BD(cota)
                # Identificando Mensagem de trnasferência bonificada
                elif "transferência bonificada" in event.message.text.casefold():
                    print(
                        "[SISTEMA] Nova mensagem de Transferência Bonificada recebida.")
                    await Telegram_Client.send_message(id_me, "Identificado Modelo de Transferência Bonificada")
                    mensagem_Transf = event.message.text
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Origem: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Destino: Nome da agencia de milhas de destino (ex: Smiles, Latam Pass, etc.)"
                        "caso haja vários add diversos + o tipo (banco, agencia etc.)\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes \n\n") + mensagem_Transf
                    schema = Objetos.Transferencia_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:\n")
                        print("-" * 40)
                        Resposta.Print_Transf()
                        Resposta_String = Resposta.toString()
                        await Telegram_Client.send_message(id_me, Resposta_String)
                        Salvar_Promocao_BD(Resposta)
                # Identificando Mensagem de Compra bonificada de milhas
                elif "comprar milhas" in event.message.text.casefold() or "comprar pontos" in event.message.text.casefold() or \
                        (("compra" in event.message.text.casefold()) and ("pontos" in event.message.text.casefold())):
                    print(
                        "[SISTEMA] Nova mensagem de Compra Bonificada recebida.")
                    await Telegram_Client.send_message(id_me, "Identificado Modelo de Compra Bonificada")
                    mensagem_Compra = event.message.text
                    # Perguntando ao Gemini sobre Compra Bonificada
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Porcent_high: Porcentagem máxima da bonificação\n"
                        "Porcent_Low: Porcentagem mínima da bonificação\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes \n\n"
                    ) + mensagem_Compra
                    schema = Objetos.Compra_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Compra()
                        Resposta_String = Resposta.toString()
                        await Telegram_Client.send_message(id_me, Resposta_String)
                        Salvar_Promocao_BD(Resposta)
                # Identificando mensagem como adesão bonificada
                elif "adesão" in event.message.text.casefold():
                    print(
                        "[SISTEMA] Nova mensagem de Adesão a Clube Bonificada recebida.")
                    await Telegram_Client.send_message(id_me, "Identificado Modelo de Adesão a Clube Bonificada")
                    mensagem_Adesao = event.message.text
                    # Perguntando ao Gemini sobre Adesão a clubes bonificada
                    Prompt = (
                        "Instruções para extrair dados da mensagem a seguir:\n"
                        "Agencia: Nome da agencia de milhas de origem (ex: Smiles, Latam Pass, etc.), caso houver vários usar palavra diversos\n"
                        "Milhas: Quantidade de milhas adquiridas na adesão\n"
                        "Data_Vencimento: Data de vencimento da promoção (ex: 01/01/2024)\n"
                        "link: Link para acessar a promoção\n"
                        "Sempre acessar o link da promoção para confirmar os detalhes \n\n"
                    ) + mensagem_Adesao
                    schema = Objetos.Adesao_Bonificada
                    Resposta = Prompt_Gemini_Promocao(Prompt, schema)

                    # Imprimindo a resposta do Gemini ou informando que não foi encontrada
                    if Resposta is not None:
                        print("\nResposta do Gemini:")
                        print("-" * 40)
                        Resposta.Print_Adesao()
                        Resposta_String = Resposta.toString()
                        await Telegram_Client.send_message(id_me, Resposta_String)
                        Salvar_Promocao_BD(Resposta)
                else:
                    print(f"Mensagem não identificada:")
                # 1. Define as duas funções primeiro

        # Aviso de que o programa aguarda mensagem do Telegram chegar
        async def aviso_periodico():
            while True:
                print('\n\n[SISTEMA] Aguardando mensagem do Telegram chegar...')
                await asyncio.sleep(120)

        async def vigiar_parada():
            while programa_ativo.is_set():
                await asyncio.sleep(0.5)
            print('[SISTEMA] Sinal de parada recebido. Desconectando Telegram...')
            await Telegram_Client.disconnect()

        # 2. Inicia as duas tarefas juntas
        tarefa_aviso = asyncio.create_task(aviso_periodico())
        tarefa_vigia = asyncio.create_task(vigiar_parada())

        # 3. Roda o Telegram 24/7 apenas UMA vez
        try:
            await Telegram_Client.run_until_disconnected()
        finally:
            tarefa_aviso.cancel()
            tarefa_vigia.cancel()
            print('[SISTEMA] Programa 24/7 encerrado...')
    else:
        print("[AVISO]Opção escolhida não é válida. retornando ao standby do programa.")


# Função de execução das threads
def loop_trabalho():
    print("[SISTEMA] Iniciando a thread de trabalho...")

    # Cria e define um loop assíncrono exclusivo para esta thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while programa_ativo.is_set():
        print("[SISTEMA] Aguardando sinal para iniciar o trabalho")
        iniciar_trabalho.wait()

        if not programa_ativo.is_set():
            break

        print("[SISTEMA] Comando start recebido.")
        try:
            # Instancia o cliente DENTRO da thread para não haver conflito de loop
            Telegram_Client = TelegramClient(
                "session_millie_API", TELEGRAM_API_ID, TELEGRAM_API_HASH, loop=loop)
            loop.run_until_complete(executar_trabalho(Telegram_Client))

        except Exception as e:
            print(
                f"[ERRO] Ocorreu um erro durante a execução do trabalho: {e}")

        finally:
            iniciar_trabalho.clear()
            print("[SISTEMA] Telegram Client desconectado.")
            print("[SISTEMA] Trabalho concluído." + "*" * 40)
            print("[SISTEMA] Sistema retornando ao estado de Standby" + "*" * 40)

    loop.close()
    print("[SISTEMA] Programa encerrando definitivamente.\n" + "=" * 40)


# Função de ativação da Thread
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


# Função de pausar ou encerrar a Thread
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


# Verificação do terminal constante para ativação, pausa ou encerramento da thread (tarefa)
if __name__ == "__main__":
    while True:
        comando = input(
            "Digite 'start', 'stop' ou 'sair': ").strip().casefold()

        if comando == "start":
            start()
        elif comando == "stop":
            stop()
        elif comando == "sair":
            stop()
            break
        else:
            print("Comando inválido. Digite 'start', 'stop' ou 'sair'.")





    #-------Parte não utilizada
        """elif selecao == 'menu':
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
                        if mensagem_Cota is not None:
                            print(
                                "[SISTEMA] Salvando dados de Cotação de Milhas no banco de dados...")
                            Salvar_Cotacao_BD(mensagem_Cota)
                        if mensagem_Transf is not None:
                            print(
                                "[SISTEMA] Salvando dados de Transferência de Milhas no banco de dados...")
                            Salvar_Promocao_BD(mensagem_Transf)
                        if mensagem_Compra is not None:
                            print(
                                "[SISTEMA] Salvando dados de Compra de Milhas no banco de dados...")
                            Salvar_Promocao_BD(mensagem_Compra)
                        if mensagem_Adesao is not None:
                            print(
                                "[SISTEMA] Salvando dados de Adesão a Clubes Bonificadas no banco de dados...")
                            Salvar_Promocao_BD(mensagem_Adesao)

                    case '0':
                        print("[SISTEMA] Encerrando o programa...")
                        break
                    case _:
                        print("[AVISO] Opção inválida. Tente novamente.")
                        """
        #Acabou a parte que não dá para se utilizar