# Scheduling Grid Applications With Software Requirements

# O que é escalonamento

  O escalonamento (ou scheduling, em inglês) refere-se ao processo de alocar recursos de computação, como processadores, memória e dispositivos de armazenamento, para as tarefas a serem executadas em um sistema computacional. No contexto de sistemas em grade (grid), o escalonamento envolve a alocação de recursos distribuídos geograficamente para a execução de aplicações em uma grade de computadores interconectados. O objetivo do escalonamento é maximizar a utilização dos recursos disponíveis, minimizando o tempo de espera da execução de tarefas. 


# O problema

  Este software é um script Python que resolve um problema de escalonamento de tarefas usando otimização matemática. O problema é definido da seguinte forma: dada um conjunto de tarefas, cada uma com um número específico de instruções, um conjunto de dependências entre as tarefas e um conjunto de computadores com diferentes velocidades de processamento e capacidades de comunicação, encontrar um cronograma ótimo para executar as tarefas nos computadores que minimiza o tempo total de conclusão.
  
  Imagine o seguinte cenário: Bob precisa executar uma aplicação pesada que consiste em várias tarefas, algumas das quais podem depender umas das outras. Cada tarefa precisa ser executada em um software específico, que está em uma máquina virtual instalada em um computador. Para isso, o software precisa ser baixado, instalado e executado a partir de um repositório de máquinas virtuais. Cada tarefa tem várias instruções a serem executadas, e cada computador tem uma capacidade de processamento diferente para as tarefas. Embora possa ser possível executar duas tarefas em um mesmo computador em momentos diferentes, será necessário baixar a máquina virtual correspondente ao novo software, caso a máquina não o tenha. Qual é a forma mais rápida de executar esta aplicação?

# Solução

  Para resolver esse problema, o código usa a biblioteca de otimização Gurobi, que é uma ferramenta para resolver problemas de programação linear e inteira mista. O código lê dados de entrada de arquivos e constrói um modelo matemático que representa o problema de escalonamento de tarefas. O modelo é então resolvido usando o solver Gurobi, e a solução é impressa no console.


# Definição

![image](https://user-images.githubusercontent.com/38995017/234465400-54d2ab40-e438-49bd-be82-68f2f5aa9767.png)

# Dados Relacionados

![image](https://user-images.githubusercontent.com/38995017/234466081-d88ae52e-a5fc-484e-b151-a803d4c2e938.png)

# Variáveis

![image](https://user-images.githubusercontent.com/38995017/234466102-1b7594f8-81d3-4a7c-ab35-c4cb00088361.png)

# Objetivo 

![image](https://user-images.githubusercontent.com/38995017/234466124-3f9203d1-06d9-459c-aa1b-163d7cdd2bbe.png)

Minimizar o tempo total para a realização de uma determinada aplicação.

# Restrições
 

| ![restricao](https://user-images.githubusercontent.com/38995017/234466158-06e77f44-e956-435c-86b9-7f44c99c3a21.png) | 
|:--:| 
|  Garante que toda tarefa deve ser executada e realizada apenas 1 vez |


| ![restricao](https://user-images.githubusercontent.com/38995017/234466192-49ef1948-ef4a-40af-95b3-536c04f1499c.png) | 
|:--:| 
|  Para a tarefa j ser executada, a i deve ser executada. Então a tarefa i deve terminar seu processamento no computador c e transferir os dados para o computador c', antes de j ser executada |


| ![restricao](https://user-images.githubusercontent.com/38995017/234466322-78692a69-8f14-4ef8-a2b7-4965cb0a10e8.png) | 
|:--:| 
|  Garante que as tarefas só serão executadas após o término da transferência e instalação da máquina virtual |


| ![restricao](https://user-images.githubusercontent.com/38995017/234466340-68a642c0-9916-438c-b281-3e9ec797ed65.png) | 
|:--:| 
| Garante que um computador c somente irá baixar, instalar ou executar uma tarefa i, se, e somente se, houver núcleo do computador disponível ( que não está em uso ). |


| ![restricao](https://user-images.githubusercontent.com/38995017/234466360-e6d66807-0f08-4f0e-b354-e3c10523662f.png) | 
|:--:| 
| Garante que nenhuma tarefa irá ser executada em um intervalo depois do tempo máximo |



  
# Tecnologias
  

 - Leitura de Dados:
	 - Expressões Regulares
- Ambiente
	- Spyder
	- Windows
- Solvar
	- Gurobi - Python



# Resultados

![image](https://user-images.githubusercontent.com/38995017/234469417-1b5712a9-1365-4d94-8255-69a85ead86d9.png)

