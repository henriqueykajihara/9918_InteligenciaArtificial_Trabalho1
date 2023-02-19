from pathlib import Path
from random import randint
import os, time

# SOU PROGRAMADOR BACKEND, PFV NÃO EXIJA QUE A INTERAÇÃO COM O USUÁRIO SEJA BONITA
# O algoritmo genético deste caso irá 

TAMANHO_POPULACAO = 20
POSICAO_X = 0
POSICAO_Y = 1

#*****************************************************************************#
class Cromossomo:
    def __init__(self, nQuantidadePassos, aPosicao, aInicio, aFinal):

        self.nQuantidadePassos = nQuantidadePassos #
        self.aPosicao = aPosicao #Cima, Baixo, Esquerda, Direita
        #self.nDistanciaFaltante = 0 #fitness
        #self.aCaminhosPossiveis = []
        #self.aPosicaoAtual = []
        self.aInicio = aInicio
        self.aFinal = aFinal
    
    def movimentoRandomico(self, aMapa, aPosicao):
        aVizinhos = self.procuraVizinho(aMapa, aPosicao[POSICAO_X], aPosicao[POSICAO_Y])
        return self.retornaPosicaoAleatoria(aVizinhos)

    def procuraVizinhos(self, aMapa, nLinhaAtual, nColunaAtual):
        
        aVizinhos = []
        nTamanhoMapa = len(aMapa) -1
        #VERIFICANDO POSICAO ACIMA
        if (nLinhaAtual -1 >= 0) and (aMapa[nLinhaAtual -1][nColunaAtual] != 1):
            aVizinho = (nLinhaAtual -1, nColunaAtual)
            aVizinhos.append(aVizinho)

        #VERIFICANDO POSICAO ABAIXO
        if (nLinhaAtual +1 <= nTamanhoMapa) and (aMapa[nLinhaAtual +1][nColunaAtual] != 1):
            aVizinho = (nLinhaAtual +1, nColunaAtual)
            aVizinhos.append(aVizinho)

        #VERIFICANDO POSICAO ESQUERDA
        if (nColunaAtual -1 >= 0) and (aMapa[nLinhaAtual][nColunaAtual -1] != 1):
            aVizinho = (nLinhaAtual, nColunaAtual -1)
            aVizinhos.append(aVizinho)

        #VERIFICANDO POSICAO DIREITA
        if (nColunaAtual +1 <= nTamanhoMapa) and (aMapa[nLinhaAtual][nColunaAtual +1] != 1):
            aVizinho = (nLinhaAtual, nColunaAtual +1)
            aVizinhos.append(aVizinho)

        return aVizinhos

    def retornaPosicaoAleatoria(self, aVizinhos):
        nPosicao = randint(1,len(aVizinhos)) -1
        return aVizinhos[nPosicao]

    def percorreLabirinto(self, aLabirinto):
        aPosicao = self.aInicio
        while aPosicao != self.aFinal:
            aVizinhos = self.procuraVizinhos(aLabirinto, aPosicao[POSICAO_X], aPosicao[POSICAO_Y])
            aPosicao = self.retornaPosicaoAleatoria(aVizinhos)
            self.nQuantidadePassos += 1

#*****************************************************************************#
class Populacao:

    def __init__(self, nPopulacaoMaxima, aInicio, aFinal):
        self.nPopulacaoMaxima = nPopulacaoMaxima
        self.aIndividuos = self.geraIndividuos(aInicio, aFinal)

    def geraIndividuos(self, aInicio, aFinal):
        aIndividuos = []
        for n in range(self.nPopulacaoMaxima):
            aIndividuos.append(Cromossomo(0, [], aInicio, aFinal))
        return aIndividuos

    #def mutacao(self, nPercentualDeMutacao):

#********************************************************************************#
def pegaCoordenadas(aMapa, cLegenda):

    lPosicoesValidas = False
    while not lPosicoesValidas:
        aEntrada = input("Digite as coordenadas " + cLegenda)
        aEntrada = aEntrada.split()
        nLinha = int(aEntrada[0])
        nColuna = int(aEntrada[0])
        if aMapa[nLinha][nColuna] == 1:
            print( "Coordenadas de obstaculos, selecione outra!")
        else:
            lPosicoesValidas = True

    return (nLinha, nColuna)

#*****************************************************************************#
def geraLabirinto( nHandle ):
    aLabirinto = []
    aLinha = nHandle.readline().split()
    while aLinha:
        aNovaLinha = []
        for i in aLinha:
            aNovaLinha.append(int(i))
        aLabirinto.append(aNovaLinha)
        aLinha = nHandle.readline().split()

    return aLabirinto

#*****************************************************************************#
def executa( aLabirinto ):
    
    aInicio = pegaCoordenadas( aLabirinto, 'iniciais: ')
    aFinal = pegaCoordenadas( aLabirinto, 'finais: ')
    oPopulacao = Populacao(TAMANHO_POPULACAO, aInicio, aFinal)
    
    
    nInicio = time.time()
    for oCromossomo in oPopulacao.aIndividuos:
        oCromossomo.percorreLabirinto(aLabirinto)
        oMelhorResultado = oCromossomo
        if oMelhorResultado.nQuantidadePassos > oCromossomo.nQuantidadePassos:
            oMelhorResultado = oCromossomo

    print('Executado em: ', time.time() - nInicio, 'ms com o melhor resultado encontrado:', oMelhorResultado.nQuantidadePassos)

#********************************************************************************#
def nivelValido(cNivel):
    return ( cNivel in ['0', '1', '2', '3'] )

#********************************************************************************#
def main():
    cNivel = ' '
    while cNivel != '0':
        print('+------------------------------------+')
        print('+--------- ALGORITMO GENETICO -------+')
        print('+------------------------------------+')
        print( '+ Selecione o nível ():    +')
        print( '+           1 - Fácil      +')
        print( '+           2 - Médio      +')
        print( '+           3 - Difícil    +')
        print( '+           0 - Sair       +')
        print('+------------------------------------+')
        cNivel = input('Selecione o nível ou ZERO para sair: ')
        print('+------------------------------------+')
        if nivelValido(cNivel):
            if cNivel == '1':
                cArquivo = 'facil.txt'
            if cNivel == '2':
                cArquivo = 'medio.txt'
            if cNivel == '3':
                cArquivo = 'dificil.txt'
            if cNivel == '0':
                cArquivo = '0'

            cPath = Path( cArquivo )
            if cPath.is_file():
                os.system('cls')
                
                nHandle = open(cArquivo, 'r')
                aLabirinto = geraLabirinto(nHandle)
                executa( aLabirinto )
                nHandle.close()
            else:
                if cArquivo == '0':
                    print(" --- Fim do programa :) ---")
                else:
                    print("Arquivo " + cArquivo +" nao encontrado!")                   
        else:
            os.system('cls')
            print('Opção ',cNivel,' invalida!')

#*****************************************************************************#
if __name__ == "__main__":
    main()