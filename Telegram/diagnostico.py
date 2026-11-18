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
import Objetos
import threading
import mariadb
connection = mariadb.connect(host="localhost", port=3306, database="Banco_da_Millie", user="root", password="50BMG")
cursor = connection.cursor()
while True:
    print("Escolha qual verificação em loop você gostaria de fazer no banco:\n 1-verificar Transferencia\n 2-verificar Compra\n 3-verificar Adesão\n 4-verificar log\n 5-verificar Cotações")
    codigo = int(input())
    match codigo:
        case 1:
            cursor.execute("select * from Verificar_Transferencia_Boni order by id_promocoes desc")
            print("\n")
            print(cursor.fetchall())
            print("\n")
        case 2:
            cursor.execute("select * from Verificar_Compra_Boni order by id_promocoes desc")
            print("\n")
            print(cursor.fetchall())
            print("\n")
        case 3:
            cursor.execute("select * from Verificar_Adesao_Boni order by id_promocoes desc")
            print("\n")
            print(cursor.fetchall())
            print("\n")
        case 4:
            #O ultimo id de log inserido foi o 72
            cursor.execute("select * from log_operacoes where id > 69 order by id desc")
            print("\n")
            print(cursor.fetchall())
            print("\n")
        case 5:
            cursor.execute("select * from cotacoes")
            print("\n")
            print(cursor.fetchall())
            print("\n")
        case 0:
            break