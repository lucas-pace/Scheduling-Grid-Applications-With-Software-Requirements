# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 23:22:36 2019

@author: Lucas de Pace
"""
import re
import numpy as np
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
        self.arcos = arcos.split()
    
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
    tarefa = Tarefa(int(result[x]), int(s[x]),qtdDados[x],arcos[x])
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
        "Primeiro somatorio"
        sum += app.tarefas[i].nInstrucoes*network.computadores[j].tempoInstrucao
        "Terceiro somatorio ( -1 pois comeca no 0 o indice, nao no 1)"
        sum += int(repositorio.TV[app.tarefas[i].idMV-1])
    for i in range(len(softwaresRequeridos)):
        sum += float(repositorio.BV[softwaresRequeridos[i]])*network.computadores[j].TR

    
    tMax.append(sum)
    sum = 0
    
tMax = min(tMax)


"""
Constantes
"""
N = []
for i in range (network.nComputadores):
    N.append(network.computadores[i].nNucleos)
V = []
for i in range (app.n):
    V.append(app.tarefas[i].idMV)
    
    
    
TB = np.zeros((len(V),network.nComputadores))
for i in range(len(V)):
    for j in range(network.nComputadores):
        TB[i][j] = network.computadores[j].TR * float(repositorio.BV[i]) + float(repositorio.TV[i])
        
TE = np.zeros((app.n,network.nComputadores))
for i in range(app.n):
    for j in range(network.nComputadores):
        TE[i][j] = app.tarefas[i].nInstrucoes * network.computadores[j].tempoInstrucao

"""
Passa pelos arcos procurando tarefas com arcos = 1. Quando acha, e colocado na listaTarefa e para cada dupla (A,B) de tarefas com arco,
e calculado para todos os pares de computador da rede (k,l) o tempo que leva para transferir os dados da tarefa A no computador k para tarefa 
B no computador l.
"""
listaTarefa = []
TT = np.zeros((network.nComputadores,network.nComputadores))
for i in range(app.n):
    for j in range(app.n):
        if app.tarefas[i].arcos[j] == '1':
            for k in range(network.nComputadores):
                for l in range(network.nComputadores):
                    TT[k][l] = float(app.tarefas[i].qtdDados[j]) * float(network.computadores[k].TB[l])
            listaTarefa.append([i,j,TT])
            TT = np.zeros((network.nComputadores,network.nComputadores))

m = Model()

scaling = 10 #"intervalo min de tempo"
x = {}
l = ()
t = 1
for i in range(app.n):
    for c in range(network.nComputadores):
        for t in range(int(tMax)):
            x[i,c,t,int(t+TE[i][c])] = m.addVar(vtype=GRB.BINARY,
                name=("x["+str(i)+","+str(c)+","+str(t)+","+str(int(t+TE[i][c]))+"]"))

y = ()
for v in range(len(V)):
    for c in range(network.nComputadores):
        for t in range(int(tMax)):
            y += ((v,c,t,int(t+TB[v][c])),)
m.addVars(y, vtype=GRB.BINARY)
varTmax = m.addVar(vtype=GRB.INTEGER, name="tMax", ub=int(tMax),obj=1)

for i in range(app.n):
    for c in range(network.nComputadores):
        for t in range(int(tMax)):
            m.addConstr(int(t+TE[i][c]) * x[i,c,t,int(t+TE[i][c])] <= varTmax,
                        name=("c1["+str(i)+","+str(c)+","+str(t)+","+str(int(t+TE[i][c]))+"]"))

for i in range(app.n):
    m.addConstr(quicksum( x[i,c,t,int(t+TE[i][c])] for c in range(network.nComputadores)  for t in range(int(tMax))) == 1,
                        name=("c2["+str(i)+"]"))



m.update()
m.write("modelo.lp")