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
from pydantic import BaseModel

# Classe de cotação de milhas


class Cotacao(BaseModel):
    Plataforma: str
    Agencia: str
    Valor_min: float
    Valor_max: float
    Data: datetime
    Monte: str

    def Print_Cota(self):
        print('--'*40 + '\nPlataforma: ', self.Plataforma)
        print('Agencia: ', self.Agencia)
        print('Valor Mínimo Cotação: R$', self.Valor_min)
        print('Valor Máximo Cotação: R$', self.Valor_max)
        print('Montante Acumulado: ', self.Monte)
        print('Vencimento: ',
              self.Data.strftime("%d/%m/%Y %H:%M"))

    def toString(self):
        return (
            f'Plataforma: {self.Plataforma}\n'
            f'Agencia: {self.Agencia}\n'
            f'Valor Mínimo Cotação: R$ {self.Valor_min:.2f}\n'
            f'Valor Máximo Cotação: R$ {self.Valor_max:.2f}\n'
            f'Montante Acumulado: {self.Monte}\n'
            f"Vencimento: {self.Data.strftime('%d/%m/%Y %H:%M')}\n"
        )
# Classe de transferencia bonificada de milhas


class Transferencia_Bonificada(BaseModel):
    Origem: str
    Destino: str
    Porcent_High: float
    Porcent_Low: float
    Data_Vencimento: datetime
    Valor_milheiro_origem: float 
    link: str

    def Print_Transf(self):
        print('--'*40 + '\nOrigem: ', self.Origem)
        print('Destino: ', self.Destino)
        print('Porcentagem Alta: ', self.Porcent_High)
        print('Porcentagem Baixa: ', self.Porcent_Low)
        print('Vencimento: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Valor do milheiro da plataforma: ', self.Valor_milheiro_origem)
        print('Informações da Promoção: ', self.link)

    def toString(self):
        return (
            f'Origem: {self.Origem}\n'
            f'Destino: {self.Destino}\n'
            f'Valor Mínimo Bônus: {self.Porcent_Low:.2f} %\n'
            f'Valor Máximo Bônus: {self.Porcent_High:.2f} %\n'
            f"Vencimento: {self.Data_Vencimento.strftime('%d/%m/%Y %H:%M')}\n"
            f'Valor do milheiro da plataforma: {self.Valor_milheiro_origem:.2f} %\n'
            f"Link: {self.link}\n"
        )

# Classe de compra bonificada de milhas


class Compra_Bonificada(BaseModel):
    Origem: str
    Porcent_High: float
    Porcent_Low: float
    Data_Vencimento: datetime
    Valor_milheiro_origem: float 
    link: str

    def Print_Compra(self):
        print('--'*40 + '\nAgência / Plataforma: ', self.Origem)
        print('Porcentagem Alta: ', self.Porcent_High)
        print('Porcentagem Baixa: ', self.Porcent_Low)
        print('Vencimento: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Valor do milheiro da plataforma: ', self.Valor_milheiro_origem)
        print('Informações da Promoção: ', self.link)

    def toString(self):
        return (
            f'Origem: {self.Origem}\n'
            f'Valor Mínimo Bônus: {self.Porcent_Low:.2f} %\n'
            f'Valor Máximo Bônus: {self.Porcent_High:.2f} %\n'
            f"Vencimento: {self.Data_Vencimento.strftime('%d/%m/%Y %H:%M')}\n"
            f'Valor do milheiro da plataforma: {self.Valor_milheiro_origem:.2f} %\n'
            f"Link: {self.link}\n"
        )

# Classe de adesão bonificada à uma agencia ou plataforma


class Adesao_Bonificada(BaseModel):
    Origem: str
    Milhas: int
    Data_Vencimento: datetime
    Valor_milheiro_origem: float 
    link: str

    def Print_Adesao(self):
        print('--'*40 + '\nAgência / Plataforma: ', self.Origem)
        print('Milhas Bonificadas: ', self.Milhas)
        print('Vencimento: ',
              self.Data_Vencimento.strftime("%d/%m/%Y %H:%M"))
        print('Valor do milheiro da plataforma: ', self.Valor_milheiro_origem)
        print('Informações da Promoção: ', self.link)

    def toString(self):
        return (
            f'Origem: {self.Origem}\n'
            f'Quantidade de Milhas: {self.Milhas}\n'
            f"Vencimento: {self.Data_Vencimento.strftime('%d/%m/%Y %H:%M')}"
            f'Valor do milheiro da plataforma: {self.Valor_milheiro_origem:.2f} %\n'
            f"Link: {self.link}\n"
        )
