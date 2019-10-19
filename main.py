# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 23:22:36 2019

@author: Lucas de Pace
"""
import re
from gurobipy import *

class App:
    def __init__(self, n, age):
        self.n = n
        self.tarefas = []
        
    def addTarefa(self,tarefa):
        self.tarefas.append(tarefa)
            
    
class Tarefa:
    def __init__(self, nInstrucoes, idMV,qtdDados,arcos):
        self.nInstrucoes = nInstrucoes
        self.idMV = idMV
        self.qtdDados = qtdDados
        self.arcos = arcos
    
class Network:
    def __init__(self,nComputadores):
        self.nComputadores = nComputadores
        self.computadores = []
        
    def addComputador(self,computador):
        self.computadores.append(computador)
        
class Computador:
        def __init__(self, tempoInstrucao, nNucleos,TB,N,TR):
            self.tempoInstrucao = tempoInstrucao
            self.nNucleos = nNucleos
            self.TB = TB
            self.N = N
            self.TR = float(TR)
            
class Repositorio:
    def __init__(self,o,SV,BV,TV):
        self.o = o 
        self.SV = SV
        self.BV = BV
        self.TV = TV
            
            
            
            
        
" Lendo arquivo de aplicacoes e salvando na classe App"
with open('app/simple_8_app.dat', 'r') as f:
    data = f.read()
    
"Instanciando classe"        
app = App("","")


result = re.search('n: (.*)\n', data)
app.n =int (result.group(1))

"pegando n de instrucoes dentro de cada tarefa do app"
result = re.search('\(1\)(.*)\]\n', data)
result = result.group(1).split()

"pegando ID da maquina virtual que contem o software para executar a tarefa"
s = re.search('S: \[ \(1\)(.*)\]\n', data)
s = s.group(1).split()

"""Pegando a quantidade de dados transmitidos entre a tarefa i e j. A tarefa i armazena um vetor
com a a quantidade de dado para toda tarefa j [0..N]
"""
qtdDados = []
for x in range(app.n):
    b = re.search('\(' +str(x+1)+ ' 1\)(.*)\n', data)
    b = b.group(1).split()
    qtdDados.append(b)
    
    
"""Pegando os arcos que existem entre as tarefas
A tarefa i tem um arco para j se o valor de ij nessa matriz for 1. Caso contrario, 0.
"""
arcos = []
for x in range(app.n):
    b = re.findall('\(' +str(x+1)+ ' 1\)(.*)\n', data)
    arcos.append(b[1])
    
    
"Instanciando o app/tarefa"
for x in range(app.n):
    tarefa = Tarefa(int(result[x]), int(s[x]),qtdDados[x],arcos)
    app.addTarefa(tarefa)

"""
Leitura dos dados das redes -----------------------------------------
""" 

" Lendo arquivo de aplicacoes e salvando na classe App"
with open('networks/n05.dat', 'r') as f:
    fileNetworks = f.read()
"Instanciando a classe Rede"

network = Network("")

" Leitura do numero de computadores na rede"
nComputadores = re.search('m: (.*)\n', fileNetworks)
network.nComputadores = int (nComputadores.group(1))

"Leitura do tempo que o computador leva para executar 1 instrucao"
"pegando n de instrucoes dentro de cada tarefa do app"
tInstrucoes = re.search('\(1\)(.*)\]\n', fileNetworks)
tInstrucoes = tInstrucoes.group(1).split()



"Leitura do numero de nucleos de processamento de um pc"
nNucleo = re.findall('\(1\)(.*)\]\n', fileNetworks)
nNucleo = nNucleo[1].split()


"TB -> Tempo necessario para transmitir uma unidade entre o pc i e j"
TB = []
for x in range(network.nComputadores):
    b = re.search('\(' +str(x)+ ' 1\)(.*)\n', fileNetworks)
    b = b.group(1).split()
    TB.append(b)

    
    
"N -> Conjunto de computadores conectados ( i e j ). I esta conectado com I, e se ij, entao ji"
N = []
for x in range(network.nComputadores):
    b = re.findall('\(' +str(x)+ ' 1\)(.*)\n', fileNetworks)
    N.append(b[1])
    
"TR -> Tempo para transmitir uma unidade entre o pc e a mv"
TR = re.findall('\(1\)(.*)\]\n', fileNetworks)
TR = TR[2].split()


for x in range(network.nComputadores):
    computador = Computador(float(tInstrucoes[x]), nNucleo[x],TB[x], N[x], TR[x])
    network.addComputador(computador)

"""

Leitura das VM`s

"""

" Lendo arquivo de VMS"
with open('vms/vpr_62.dat', 'r') as f:
    fileVM = f.read()
    
"Instanciando a classe Repositorio"
repositorio = Repositorio("","","","")

"Lendo: o -> Numero de MV no repositorio"
o = re.search('o: (.*)\n', fileVM)
repositorio.o= int(o.group(1))


"SV -> Software disponivel na mv"
SV = re.findall('\(1\)(.*)\]\n', fileVM)
SV = SV[0].split()
repositorio.SV = SV


"BV -> tamanho da vm em Megabytes"
BV = re.findall('\(1\)(.*)\]\n', fileVM)
BV = BV[1].split()
repositorio.BV = BV


"TV -> tempo de inicializacao em segundos"
TV = re.findall('\(1\)(.*)\]\n', fileVM)
TV = TV[2].split()
repositorio.TV = TV



sum = 0

tMax = []

softwaresRequeridos = []
"Pegando todos os softwares requeridos pelas tarefas e tirando da lista os que sao repetidos ( ja foram baixados)"
for i in range(app.n):
    softwaresRequeridos.append([app.tarefas[i].idMV][0])
softwaresRequeridos = list( dict.fromkeys(softwaresRequeridos) )

for j in range(network.nComputadores):
    for i in range(app.n):
        sum += app.tarefas[i].nInstrucoes*network.computadores[j].tempoInstrucao
        sum += int(repositorio.TV[app.tarefas[i].idMV-1])
    for i in range(len(softwaresRequeridos)):
        sum += float(repositorio.BV[softwaresRequeridos[i]])*network.computadores[j].TR

    
    tMax.append(sum)
    sum = 0
print(min(tMax))