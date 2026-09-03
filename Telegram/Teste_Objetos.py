from datetime import datetime


class Cotacao:
    def __init__(self, Plataforma: str, Agencia: str, Media: float, Data, Monte: str):
        self.Plataforma = Plataforma
        self.Agencia = Agencia
        self.Media = Media
        self.Monte = Monte
        self.Data = Data

    def Print_Cota(self):
        print('--'*40 + '\nPlataforma: ', self.Plataforma)
        print('Agencia: ', self.Agencia)
        print('Valor Médio Cotação: R$', self.Media)
        print('Montante Acumulado: ', self.Monte)
        print('Última Atualização: ', self.Data.strftime("%d/%m/%Y %H:%M"))


Smiles_Data = datetime(2026, 8, 28, 10, 30)
Smiles_Cota = Cotacao('Balcão de Milhas', 'Smiles', 15.0, Smiles_Data, 500000)

Smiles_Cota.Print_Cota()
