from pathlib import Path
SETA_CIMA     = '▲'
SETA_DIREITA  = '►'
SETA_ESQUERDA = '◄'
SETA_BAIXO    = '▼'
      
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
                aLinha[j] = 'S'
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
    
    while aPosicoesAbertas != [] and not lEncontrou:
        
        aPosicaoAtual = aPosicoesAbertas[0]
        aVizinhos = procuraVizinhos(aPosicaoAtual[LINHA], aPosicaoAtual[COLUNA], aMapa, aPosicoesVerificados)
        calculaCustos(aPosicaoAtual, aVizinhos, dPosicoesCalculadas, aFinal)

        for aVizinho in aVizinhos:
            if (aVizinho not in aPosicoesAbertas):
                aPosicoesAbertas.append(aVizinho)
        
        aPosicoesAbertas.remove(aPosicaoAtual)                
        aPosicoesVerificados.append(aPosicaoAtual)
        if (aFinal in aPosicoesVerificados):
            lEncontrou = True
            aPercurso = montaPercurso(aPosicaoAtual, dPosicoesCalculadas, aInicio)
    
    desenhaMapaCompleto(aMapa, aPercurso, aInicio, aFinal)

    print(' ----- Fim da execução ----- ')

#********************************************************************************#
def main():
    cArquivo = ' '
    while cArquivo != '0':
        cArquivo = input("Digite o nome do arquivo ou ZERO para sair: ")
        cPath = Path( cArquivo )
        if cPath.is_file():
            nHandle = open(cArquivo, 'r')
            executa( nHandle )
            nHandle.close()
        else:
            if cArquivo == '0':
                print(" --- Fim do programa :) ---")
            else:
                print("Arquivo " + cArquivo +" nao encontrado!")

#********************************************************************************#
if __name__ == "__main__":
    main()
