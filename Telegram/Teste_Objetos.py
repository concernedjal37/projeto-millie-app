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
Arquivo: Teste_Objetos.py
Descrição:
 
EMPRESA:       [Millie Tecnologies]
SISTEMA:       [Millie App - Desenvolvimento de Software]
MÓDULO:        []
ARQUIVO:       [Teste_Objetos.py]
--------------------------------------------------------------------------
DESCRIÇÃO:  [Este arquivo contém as classes de objetos que representam as] 
            [respostas estruturadas em JSON do Gemini para as estruturas de dados]
            [de Cotação de Milhas, Transferências,, Compras, e Adesões Bonificadas]
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

from datetime import datetime

# Classe de cotação de milhas


class Cotacao:
    def __init__(self, Plataforma: str, Agencia: str, Media: float, Data_Vencimento, Monte: str):
        self.Plataforma = Plataforma
        self.Agencia = Agencia
        self.Media = Media
        self.Monte = Monte
        self.Data_Vencimento = Data_Vencimento

    def Print_Cota(self):
        print('--'*40 + '\nPlataforma: ', self.Plataforma)
        print('Agencia: ', self.Agencia)
        print('Valor Médio Cotação: R$', self.Media)
        print('Montante Acumulado: ', self.Monte)
        print('Última Atualização: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))

# Classe de transferencia bonificada de milhas


class Transferencia_Bonificada:
    def __init__(self, Origem: str, Destino: str, Porcent_High: float, Porcent_Low: float, Data_Vencimento, link: str):
        self.Origem = Origem
        self.Destino = Destino
        self.Porcent_High = Porcent_High
        self.Porcent_Low = Porcent_Low
        self.Data_Vencimento = Data_Vencimento
        self.link = link

    def Print_Transf(self):
        print('--'*40 + '\nOrigem: ', self.Origem)
        print('Destino: ', self.Destino)
        print('Porcentagem Alta: ', self.Porcent_High)
        print('Porcentagem Baixa: ', self.Porcent_Low)
        print('Última Atualização: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Informações da Promoção: ', self.link)


# Classe de compra bonificada de milhas

class Compra_Bonificada:
    def __init__(self, Agencia: str, Porcent_High: float, Porcent_Low: float, Data_Vencimento, link: str):
        self.Agencia = Agencia
        self.Porcent_High = Porcent_High
        self.Porcent_Low = Porcent_Low
        self.Data_Vencimento = Data_Vencimento
        self.link = link

    def Print_Compra(self):
        print('--'*40 + '\nAgência / Plataforma: ', self.Agencia)
        print('Porcentagem Alta: ', self.Porcent_High)
        print('Porcentagem Baixa: ', self.Porcent_Low)
        print('Última Atualização: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Informações da Promoção: ', self.link)


# Classe de adesão bonificada à uma agencia ou plataforma

class Adesao_Bonificada:
    def __init__(self, Agencia: str, Milhas: int, Data_Vencimento, link: str):
        self.Agencia = Agencia
        self.Milhas = Milhas
        self.Data_Vencimento = Data_Vencimento
        self.link = link

    def Print_Adesao(self):
        print('--'*40 + '\nAgência / Plataforma: ', self.Agencia)
        print('Milhas Bonificadas: ', self.Milhas)
        print('Última Atualização: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Informações da Promoção: ', self.link)
