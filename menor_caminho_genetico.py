#*****************************************************************************#
# Algoritmo genético para encontrar o menor caminho no problema do caixeiro
# viajante (Travelling salesman problem). Neste exemplo foi utilizado exemplo 
# arquivo romania2950.tsp para encontrar o menor caminho entre duas cidades
# na Romênia
#*****************************************************************************#
import random
import time
import heapq
import math

TAMANHO_INICIAL = 20
TEMPO_MAXIMO = 600
RANDOM_RANGE = 999
TAXA_MUTACAO = 0.1
NUMERO_MAXIMO = 9999999999999999999999999
#*****************************************************************************#
class Coordenadas:
    x: float
    y: float

#*****************************************************************************#
class Cromossomo:

    distancia: int
    aCidades: list 

    def __lt__(self,other):
        return self.distancia > other.distancia

#*****************************************************************************#
def leArquivo(cArquivo):

    nArquivo = open( cArquivo,'r')
    aArquivo = nArquivo.readlines()
    aCidades = []

    for cLinha in aArquivo:
        aLinha = cLinha.split()    
        
        if aLinha and soNumero(aLinha[0]) :   
            aCidade = list( float(num) for num in aLinha)

            oCoordenadas = Coordenadas()
            oCoordenadas.x = aCidade[1]
            oCoordenadas.y = aCidade[2]    
            aCidades.append(oCoordenadas)

    print("ARQUIVO '"+ cArquivo+"' LIDO. FORAM INSERIDAS " +str(len(aCidades))+ " CIDADES.")            
    return aCidades

#*****************************************************************************#
def soNumero(cLinha):
    for cCaracter in cLinha:
        return cCaracter.isdigit()

#*****************************************************************************#
def geraHashPopulacao():
    
    aCidadesAuxiliar = []

    for oCoordenadas in aCidadesGlobal:
        aCidadesAuxiliar.append(oCoordenadas)

    for n in range(TAMANHO_INICIAL):
        oNovoCromossomo = Cromossomo()
        random.shuffle(aCidadesAuxiliar)
        oNovoCromossomo.aCidades = retornaArrayDeCoordenadas(aCidadesAuxiliar)
        oNovoCromossomo.distancia = calculaDistanciaCromossomo(oNovoCromossomo.aCidades)
        heapq.heappush(hPopulacaoGlobal, oNovoCromossomo)

    print("Gerada populacao inicial com tamanho: " + str(len(hPopulacaoGlobal)))

#*****************************************************************************#
def calculaDistanciaCromossomo(aCidades):
    nDistancia = 0
    for i in range(len(aCidades)-1):
        nDistancia += caculaDistancia( aCidades[i], aCidades[i+1])
    return nDistancia

#*****************************************************************************#
def caculaDistancia( oCidade1, oCidade2 ):
    return math.sqrt( math.pow( oCidade1.x - oCidade1.y, 2) + math.pow( oCidade2.x - oCidade2.y, 2) )

#*****************************************************************************#
def geraPaisPeloMetodoDaRoleta(hPopulacao):

    aCromossomosRoleta = pegaCromossomosAleatorios(hPopulacao)
    aMelhoresPais      = selecionaDoisMelhoresPais(aCromossomosRoleta)
    oCromossomoFilho   = crossOver(aMelhoresPais)
    return oCromossomoFilho

#*****************************************************************************#
def selecionaDoisMelhoresPais(aCromossomosRoleta):
    return [PegaMelhorPai(aCromossomosRoleta[0]), PegaMelhorPai(aCromossomosRoleta[1])]

#*****************************************************************************#
def PegaMelhorPai(aCromossomosRoleta):
    oMelhor = aCromossomosRoleta[0]
    for oCromossomo in aCromossomosRoleta:
        if (oCromossomo.distancia < oMelhor.distancia):
            oMelhor = oCromossomo

    return oMelhor

#*****************************************************************************#
def pegaCromossomosAleatorios(hPopulacao):
    
    aPlayer1 = pegaAleatorios(hPopulacao)
    aPlayer2 = pegaAleatorios(hPopulacao)

    return [aPlayer1, aPlayer2]

#*****************************************************************************#
def pegaAleatorios(hPopulacao):

    aPlayer = []
    for n in range(3):
        oCromossomo = hPopulacao[tamanhoAleatorioPopulacao()]
        aPlayer.append(oCromossomo)

    return aPlayer

#*****************************************************************************#
def crossOver(aMelhoresPais):

    nIndex1 = random.randrange(1,RANDOM_RANGE)% len(aCidadesGlobal)
    nIndex2 = random.randrange(1,RANDOM_RANGE)% len(aCidadesGlobal)

    #print('************************')
    #print('CROSSOVER')
    #print('************************')
    oPai1 = aMelhoresPais[0]
    oPai2 = aMelhoresPais[1]
    oFilho1 = Cromossomo()
    oFilho2 = Cromossomo()
    
    oFilho1.aCidades = []
    oFilho2.aCidades = []

    if (nIndex1 > nIndex2):
        nAuxiliar = nIndex2
        nIndex2 = nIndex1
        nIndex1 = nAuxiliar
    
    #print('Index 1:', nIndex1 )
    #print('Index 2:', nIndex2 )
    #print('************************')

    for x in range(nIndex1, nIndex2):    

        oCoordenadas1 = copiaCoordenadas(oPai2.aCidades[x])
        oFilho1.aCidades.append(oCoordenadas1)
        oCoordenadas2 = copiaCoordenadas(oPai1.aCidades[x])
        oFilho2.aCidades.append(oCoordenadas2)

    for x in range(nIndex1):

        if not (cidadeJaInserida(oPai1.aCidades[x], oFilho2.aCidades)):
            oCoordenadas2 = copiaCoordenadas(oPai1.aCidades[x])
            oFilho2.aCidades.append(oCoordenadas2)
        if not (cidadeJaInserida(oPai2.aCidades[x], oFilho1.aCidades)):
            oCoordenadas1 = copiaCoordenadas(oPai2.aCidades[x])
            oFilho1.aCidades.append(oCoordenadas1)

    for x in range(nIndex2, len(aCidadesGlobal)):
        if not (cidadeJaInserida(oPai1.aCidades[x], oFilho2.aCidades)):
            oCoordenadas2 = copiaCoordenadas(oPai1.aCidades[x])
            oFilho2.aCidades.append(oCoordenadas2)
        if not (cidadeJaInserida(oPai2.aCidades[x], oFilho1.aCidades)):
            oCoordenadas1 = copiaCoordenadas(oPai2.aCidades[x])
            oFilho1.aCidades.append(oCoordenadas1)

    oFilho1.distancia = calculaDistanciaCromossomo(oFilho1.aCidades)
    oFilho2.distancia = calculaDistanciaCromossomo(oFilho2.aCidades)
    #print('Distancia 1:', oFilho1.distancia, ' tamanho:', len(oFilho1.aCidades))
    #print('Distancia 2:',oFilho2.distancia, ' tamanho:', len(oFilho2.aCidades))
    if (oFilho1.distancia > oFilho2.distancia):
        return oFilho1
    return oFilho2

#*****************************************************************************#   
def mutacao(oFilho):

    for i in range(len(oFilho.aCidades)):
        nAuxiliar = random.randrange(1,RANDOM_RANGE)%1000
        if(nAuxiliar < TAXA_MUTACAO*1000):
           nPosicaoTrocar = random.randrange(1,RANDOM_RANGE)%len(aCidadesGlobal) 
           if i > 2950:
                print(i)
           if nPosicaoTrocar > 2950:
                print( nPosicaoTrocar)
           oFilho.aCidades[i], oFilho.aCidades[nPosicaoTrocar] = oFilho.aCidades[nPosicaoTrocar], oFilho.aCidades[i]

#*****************************************************************************#   
def cidadeJaInserida(oCidadeVerificada, aCidades):

    for oCidade in aCidades:
        if (oCidadeVerificada.x == oCidade.x and oCidadeVerificada.y == oCidade.y):
            return True
    return False

#*****************************************************************************#   
def retornaArrayDeCoordenadas(aArray):
    aCidades = []
    for n in range(len(aArray)):
        oCoordenadas = copiaCoordenadas(aArray[n])
        aCidades.append(oCoordenadas)
    return aCidades

#*****************************************************************************#
def tamanhoAleatorioPopulacao():
    return random.randrange(1,RANDOM_RANGE)% len(hPopulacaoGlobal)

#*****************************************************************************#
def copiaCoordenadas(oCoordenadas):
    oNovaCoordenada = Coordenadas()
    oNovaCoordenada.x = oCoordenadas.x
    oNovaCoordenada.y = oCoordenadas.y
    return oNovaCoordenada

#*****************************************************************************#
def atualizaPopulacao(oCromossomo):
    heapq.heappop(hPopulacaoGlobal)
    heapq.heappush(oCromossomo)

#*****************************************************************************#
def buscaLocalComTempoLimitado(oCromossomo):
    
    nInicio = time.time()
    nDistanciaAnterior = oCromossomo.distancia
    
    oFilho = Cromossomo()
    oFilho.aCidades = retornaArrayDeCoordenadas(oCromossomo.aCidades)
    oFilho.distancia = 0

    while ((time.time()-nInicio) < 10 ):
        nIndex1 = random.randrange(1,RANDOM_RANGE)% len(aCidadesGlobal)
        nIndex2 = random.randrange(1,RANDOM_RANGE)% len(aCidadesGlobal)

        if (nIndex1 != nIndex2):
            oCoordenadaAuxiliar = oFilho.aCidades[nIndex1]
            oFilho.aCidades[nIndex1] = oFilho.aCidades[nIndex2]
            oFilho.aCidades[nIndex2] = oCoordenadaAuxiliar
        oFilho.distancia = calculaDistanciaCromossomo(oFilho.aCidades)

        if (oFilho.distancia < nDistanciaAnterior):
            return oFilho

    return oCromossomo

#*****************************************************************************#
def calculaSolucoes():

    oCromossomo = geraHashPopulacao()
    nIteracoes = 0
    nInicio = time.time()
    nMelhorSolucao = NUMERO_MAXIMO
    cArquivo = open("arquivo.txt", "a")
    
    while (time.time() - nInicio) < TEMPO_MAXIMO:
        random.seed(time.time())
        oCromossomoFilho = geraPaisPeloMetodoDaRoleta(hPopulacaoGlobal)
        mutacao(oCromossomoFilho)
        oCromossomoFilho.distancia = calculaDistanciaCromossomo(oCromossomoFilho.aCidades)
        #buscaLocalComTempoLimitado(oCromossomoFilho)
        nIteracoes+= 1     
        if (oCromossomoFilho.distancia < nMelhorSolucao):
            print( 'Iteracao:', nIteracoes, ' melhor solucao:' , oCromossomoFilho.distancia,' no tempo:', time.time() - nInicio )
        #    cString = 'Iteracao:', nIteracoes, ' melhor solucao:' , oCromossomoFilho.distancia,' no tempo:', time.time() - nInicio
        #    print( cString )
        #    cArquivo.write( cString )

            nMelhorSolucao = oCromossomoFilho.distancia
    cArquivo.close()

#*****************************************************************************#
def executa():

    calculaSolucoes()
    print("Finish")
#*****************************************************************************#

aArquivos = ['romania2950.tsp' ]

for cArquivo in aArquivos:
    hPopulacaoGlobal = []
    print(cArquivo)
    aCidadesGlobal = leArquivo(cArquivo)
    executa()
    print('********************************')
