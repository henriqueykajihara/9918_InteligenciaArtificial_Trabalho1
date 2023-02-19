from pathlib import Path
import time
import os

# SOU PROGRAMADOR BACKEND, PFV NÃO EXIJA QUE A INTERAÇÃO COM O USUÁRIO SEJA BONITA

ESPACO = ' '
OBSTACULO = '█'
PONTO_INICIO = 'I'
PONTO_FIM    = 'F'
LINHA = 0
COLUNA = 1

#********************************************************************************#
def geraMapaDePosicoes( nHandle ):
    aMapa = []
    aLinha = nHandle.readline().split()
    while aLinha:
        aNovaLinha = []
        for i in aLinha:
            aNovaLinha.append(int(i))
            #aLinha[i] = int(aLinha[i])
        aMapa.append(aNovaLinha)
        aLinha = nHandle.readline().split()
    #print(aMapa)
    return aMapa

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

#********************************************************************************#
def procuraVizinhos(nLinhaAtual, nColunaAtual, aMapa, aPosicoesVerificados):
    aVizinhos = []
    nTamanhoMapa = len(aMapa) -1
    #VERIFICANDO POSICAO ACIMA
    if (nLinhaAtual -1 >= 0) and (aMapa[nLinhaAtual -1][nColunaAtual] != 1):
        aVizinho = (nLinhaAtual -1, nColunaAtual)
        if (aVizinho not in aPosicoesVerificados):
            aVizinhos.append(aVizinho)
    
    #VERIFICANDO POSICAO ABAIXO
    if (nLinhaAtual +1 <= nTamanhoMapa) and (aMapa[nLinhaAtual +1][nColunaAtual] != 1):
        aVizinho = (nLinhaAtual +1, nColunaAtual)
        if (aVizinho not in aPosicoesVerificados):
            aVizinhos.append(aVizinho)

    #VERIFICANDO POSICAO ESQUERDA
    if (nColunaAtual -1 >= 0) and (aMapa[nLinhaAtual][nColunaAtual -1] != 1):
        aVizinho = (nLinhaAtual, nColunaAtual -1)
        if (aVizinho not in aPosicoesVerificados):
            aVizinhos.append(aVizinho)

    #VERIFICANDO POSICAO DIREITA
    if (nColunaAtual +1 <= nTamanhoMapa) and (aMapa[nLinhaAtual][nColunaAtual +1] != 1):
        aVizinho = (nLinhaAtual, nColunaAtual +1)
        if (aVizinho not in aPosicoesVerificados):
            aVizinhos.append(aVizinho)

    return aVizinhos
        
#********************************************************************************#
def distanciaManhattan(aVizinho, aFinal):
    return ( abs(aFinal[0] - aVizinho[0]) + abs(aFinal[1] - aVizinho[1]))

#********************************************************************************#
def calculaCustos(aPosicaoAtual, aVizinhos, dPosicoesCalculadas, aFinal):  
    
    for aVizinho in aVizinhos:
        nResultado = distanciaManhattan(aVizinho, aFinal)
        try:
            nCusto = dPosicoesCalculadas[aPosicaoAtual][1] +1
        except:
            nCusto = 1
        dPosicoesCalculadas[aVizinho] = (aVizinho, nCusto, nResultado, aPosicaoAtual)

#********************************************************************************#
def desenhaMapaCompleto(aMapa, aPercurso, aInicio, aFinal):
    
    aMapaCompleto = []
    nTracejado = 0
    for i in range(len(aMapa)):
        aLinha = []
        for j in range(len(aMapa[i])):
            if aMapa[i][j] == 0:
                aLinha.append(ESPACO)
            if aMapa[i][j] == 1:
                aLinha.append(OBSTACULO)
            if ( (i,j) in aPercurso):
                aLinha[j] = '•'
        if not nTracejado:
            nTracejado = len(aLinha)
        aMapaCompleto.append(aLinha)

    aMapaCompleto[aInicio[0]][aInicio[1]] = PONTO_INICIO
    aMapaCompleto[aFinal[0]][aFinal[1]] = PONTO_FIM

    #print(aPercurso)
    print('-' * nTracejado *2)
    print('Percurso percorrido de', aInicio, 'a', aFinal )
    print('-' * nTracejado *2)
    for aLinha in aMapaCompleto:
        for cElemento in aLinha:
            print(cElemento, end=' ')
        print()
    print('-' * nTracejado *2)

#********************************************************************************#
def montaPercurso(aPosicaoAtual, dPosicoesCalculadas, aInicio):
    
    aPercurso = []
    if aPosicaoAtual != aInicio:
        aOrigem = dPosicoesCalculadas[aPosicaoAtual][3]
    else:
        aOrigem = aInicio

    aPercurso.append(aPosicaoAtual)
    while aOrigem != aInicio:
        aPercurso.append(aOrigem)
        aOrigem = dPosicoesCalculadas[aOrigem][3]
    aPercurso.reverse()
    return aPercurso 

#********************************************************************************#
def executa( nHandle ):

    nInicio = time.time()
    aMapa =  geraMapaDePosicoes( nHandle )
    lEncontrou = False
    aInicio = pegaCoordenadas( aMapa, 'iniciais: ')
    aFinal = pegaCoordenadas( aMapa, 'finais: ')

    if aInicio == aFinal:
        print('Posição inicial IGUAL a final! Execução abortada.')
        return

    aPosicoesVerificados = []
    aPosicoesAbertas = []
    aPosicoesAbertas.append(aInicio)
    dPosicoesCalculadas = {}
    nQuantidadePassos = 0
    
    while aPosicoesAbertas != [] and not lEncontrou:
        
        aPosicaoAtual = aPosicoesAbertas[0]
        aVizinhos = procuraVizinhos(aPosicaoAtual[LINHA], aPosicaoAtual[COLUNA], aMapa, aPosicoesVerificados)
        calculaCustos(aPosicaoAtual, aVizinhos, dPosicoesCalculadas, aFinal)

        for aVizinho in aVizinhos:
            if (aVizinho not in aPosicoesAbertas):
                aPosicoesAbertas.append(aVizinho)
        
        aPosicoesAbertas.remove(aPosicaoAtual)                
        aPosicoesVerificados.append(aPosicaoAtual)
        nQuantidadePassos += 1
        if (aFinal in aPosicoesVerificados):
            lEncontrou = True
            aPercurso = montaPercurso(aPosicaoAtual, dPosicoesCalculadas, aInicio)
    
    desenhaMapaCompleto(aMapa, aPercurso, aInicio, aFinal)
    print('Executado em: ', time.time() - nInicio, 'ms com o melhor resultado encontrado:', nQuantidadePassos)
    print(' ----- Fim da execução ----- ')

#********************************************************************************#
def nivelValido(cNivel):
    return ( cNivel in ['0', '1', '2', '3'] )
    
#********************************************************************************#
def main():
    cNivel = ' '
    while cNivel != '0':

        print('+------------------------------------+')
        print('+---------      A ESTRELA    --------+')
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
                executa( nHandle )
                nHandle.close()
            else:
                if cArquivo == '0':
                    print(" --- Fim do programa :) ---")
                else:
                    print("Arquivo " + cArquivo +" nao encontrado!")                   
        else:
            os.system('cls')
            print('Opção ',cNivel,' invalida!')
        #os.system('cls')

#********************************************************************************#
if __name__ == "__main__":
    main()
