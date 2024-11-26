import random
from collections import deque

# Entradas do usuário
GRID_SIZE = int(input("Defina o tamanho do grid (entre 10 e 20): "))
while GRID_SIZE < 10 or GRID_SIZE > 20:
    GRID_SIZE = int(input("Tamanho inválido. Por favor, insira um valor entre 10 e 20: "))

# Tempo até o próximo ciclo (máximo 200)
TOTAL_SIMULATION_TIME = int(input("Defina o tempo até o próximo ciclo (no máximo 200): "))
while TOTAL_SIMULATION_TIME <= 0 or TOTAL_SIMULATION_TIME > 200:
    TOTAL_SIMULATION_TIME = int(input("Tempo inválido. Por favor, insira um valor positivo até 200: "))

# Recursos disponíveis no planeta (quantidade finita)
RECURSOS = {
    'Cristais Energéticos': {'valor': 10, 'quantidade': random.randint(10, 15)},
    'Blocos de Metal Raro': {'valor': 20, 'quantidade': random.randint(10, 15)},
    'Estruturas Antigas': {'valor': 50, 'quantidade': random.randint(5, 7)}
}

# Mostrar a quantidade total de recursos gerados
print("\nQuantidade de recursos gerados:")
for recurso, atributos in RECURSOS.items():
    print(f"{recurso}: {atributos['quantidade']} unidades")

# Definindo obstáculos
OBSTACULOS = ['Rio', 'Montanha']
MAX_OBSTACULOS = int(0.2 * GRID_SIZE * GRID_SIZE)  # 20% do grid
NUM_OBSTACULOS = random.randint(int(0.1 * MAX_OBSTACULOS), MAX_OBSTACULOS)

# Contador de recursos entregues
recursos_entregues = {'Cristais Energéticos': 0, 'Blocos de Metal Raro': 0, 'Estruturas Antigas': 0}

# Variável para armazenar informações compartilhadas entre agentes
painel_informacoes = []

def bfs(grid, start, goal):
    queue = deque()
    queue.append((start, []))
    visited = set()
    visited.add(start)
    while queue:
        current_pos, path = queue.popleft()
        if current_pos == goal:
            return path[0] if path else None  # Retorna o primeiro movimento
        for movimento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nova_posicao = (current_pos[0] + movimento[0], current_pos[1] + movimento[1])
            if (0 <= nova_posicao[0] < GRID_SIZE and 0 <= nova_posicao[1] < GRID_SIZE and
                not grid[nova_posicao[0]][nova_posicao[1]] in OBSTACULOS and
                nova_posicao not in visited):
                visited.add(nova_posicao)
                queue.append((nova_posicao, path + [movimento]))
    return None  # Se não houver caminho

class Agente:
    def __init__(self, tipo, posicao_inicial):
        self.tipo = tipo
        self.posicao = posicao_inicial
        self.memoria = []  # Apenas para agentes com memória
        self.recursos_coletados = []
        self.total_entregue = 0
        self.retornando_base = False  # Indica se o agente está retornando à base
        self.destino = None  # Para agentes que planejam rotas
        self.conhecimento_recursos = []  # Para agentes que armazenam informações sobre recursos
        self.id = random.randint(1000, 9999)  # Identificador único para o agente

    def decidir(self, passos_restantes):
        # Se o tempo restante for menor que a distância até a base, retorna à base
        distancia_ate_base = abs(self.posicao[0]) + abs(self.posicao[1])
        if passos_restantes <= distancia_ate_base + 1:  # +1 para garantir que chegue a tempo
            self.retornando_base = True

    def mover_para_base(self, grid):
        movimento = bfs(grid, self.posicao, (0, 0))
        if movimento:
            nova_posicao = (self.posicao[0] + movimento[0], self.posicao[1] + movimento[1])
            self.posicao = nova_posicao
        else:
            # Se não houver caminho, move aleatoriamente
            self.mover_aleatoriamente(grid)

    def mover_para_recurso(self, grid):
        if self.destino is None or grid[self.destino[0]][self.destino[1]] not in RECURSOS:
            # Seleciona um novo destino
            recursos_possiveis = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                                  if grid[i][j] in RECURSOS and RECURSOS[grid[i][j]]['quantidade'] > 0]
            if recursos_possiveis:
                # Seleciona o recurso mais próximo
                self.destino = min(recursos_possiveis,
                                   key=lambda pos: abs(pos[0] - self.posicao[0]) + abs(pos[1] - self.posicao[1]))
            else:
                self.mover_aleatoriamente(grid)
                return

        movimento = bfs(grid, self.posicao, self.destino)
        if movimento:
            nova_posicao = (self.posicao[0] + movimento[0], self.posicao[1] + movimento[1])
            self.posicao = nova_posicao
        else:
            # Se não houver caminho, move aleatoriamente
            self.mover_aleatoriamente(grid)

    def mover_aleatoriamente(self, grid):
        movimentos_possiveis = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        random.shuffle(movimentos_possiveis)
        for movimento in movimentos_possiveis:
            nova_posicao = (self.posicao[0] + movimento[0], self.posicao[1] + movimento[1])
            # Garantir que não sai do grid e não entra em obstáculos
            if (0 <= nova_posicao[0] < GRID_SIZE and 0 <= nova_posicao[1] < GRID_SIZE and
                not self.posicao_obstaculo(nova_posicao, grid)):
                self.posicao = nova_posicao
                break
        if self.tipo == 'Baseado em Estado':
            if nova_posicao not in self.memoria:
                self.memoria.append(nova_posicao)

    def mover(self, grid, passos_restantes):
        self.decidir(passos_restantes)
        if self.retornando_base:
            self.mover_para_base(grid)
        elif self.tipo == 'Reativo Simples':
            self.mover_aleatoriamente(grid)
        elif self.tipo == 'Baseado em Estado':
            self.mover_aleatoriamente(grid)
        elif self.tipo == 'Baseado em Objetivos':
            self.mover_para_recurso(grid)
        elif isinstance(self, AgenteCooperativo):
            if self.destino:
                self.mover_para_destino(grid)
            else:
                self.mover_para_recurso(grid)
        elif isinstance(self, AgenteBDI):
            self.agir(grid)

    def coletar(self, grid):
        x, y = self.posicao
        if grid[x][y] in RECURSOS and RECURSOS[grid[x][y]]['quantidade'] > 0:
            recurso_atual = grid[x][y]
            if (self.tipo == 'Reativo Simples' and recurso_atual == 'Cristais Energéticos') or \
                    (self.tipo != 'Reativo Simples'):
                # Verifica se é necessário ajuda para coletar (Estruturas Antigas)
                if recurso_atual == 'Estruturas Antigas':
                    if isinstance(self, AgenteCooperativo):
                        self.solicitar_ajuda(recurso_atual, (x, y))
                    else:
                        # Outros agentes não podem coletar sozinhos Estruturas Antigas
                        return
                else:
                    self.recursos_coletados.append(recurso_atual)
                    RECURSOS[recurso_atual]['quantidade'] -= 1
                    grid[x][y] = ''
                    self.retornando_base = True  # Agente começa a retornar à base
                    self.destino = None  # Limpa o destino após coletar
                    # Comunica aos outros agentes que o recurso foi coletado
                    self.comunicar_remocao_recurso((x, y))
                    # Comunica descoberta do recurso (para agentes que comunicam)
                    self.comunicar_recurso((x, y), recurso_atual)

    def entregar(self):
        # Caso o agente volte para a base (posição (0, 0))
        if self.posicao == (0, 0) and self.recursos_coletados:
            for recurso in self.recursos_coletados:
                recursos_entregues[recurso] += 1
            entregues = len(self.recursos_coletados)
            self.total_entregue += entregues
            self.recursos_coletados.clear()
            self.retornando_base = False  # Agente pode voltar a coletar recursos
            return entregues
        return 0

    def posicao_obstaculo(self, posicao, grid):
        x, y = posicao
        return grid[x][y] in OBSTACULOS

    def comunicar_recurso(self, posicao, recurso):
        # Adiciona informação ao painel de informações compartilhado
        painel_informacoes.append({'posicao': posicao, 'recurso': recurso})

    def comunicar_remocao_recurso(self, posicao):
        # Remove informação do painel quando um recurso foi coletado
        global painel_informacoes
        painel_informacoes = [info for info in painel_informacoes if info['posicao'] != posicao]

class AgenteCooperativo(Agente):
    def __init__(self, tipo, posicao_inicial):
        super().__init__(tipo, posicao_inicial)
        self.solicitacoes_ajuda = []

    def solicitar_ajuda(self, recurso, posicao):
        # Calcula a utilidade de ajudar com base na distância e número de agentes disponíveis
        agentes_disponiveis = [agente for agente in agentes if agente != self and not agente.retornando_base]
        if agentes_disponiveis:
            # Solicita ajuda aos agentes disponíveis
            for agente in agentes_disponiveis:
                agente.receber_solicitacao_ajuda(self, recurso, posicao)
        else:
            # Se não há agentes disponíveis, retorna
            return

    def receber_solicitacao_ajuda(self, agente_solicitante, recurso, posicao):
        # Calcula a utilidade de ajudar
        distancia = abs(self.posicao[0] - posicao[0]) + abs(self.posicao[1] - posicao[1])
        utilidade = 1 / (1 + distancia)
        # Decide se ajuda ou não (simplificação: sempre ajuda se não estiver ocupado)
        if not self.retornando_base:
            self.destino = posicao

    def mover_para_destino(self, grid):
        movimento = bfs(grid, self.posicao, self.destino)
        if movimento:
            nova_posicao = (self.posicao[0] + movimento[0], self.posicao[1] + movimento[1])
            self.posicao = nova_posicao
        else:
            self.mover_aleatoriamente(grid)
        # Verifica se chegou ao destino
        if self.posicao == self.destino:
            # Coleta o recurso em conjunto
            x, y = self.posicao
            if grid[x][y] == 'Estruturas Antigas':
                self.recursos_coletados.append('Estruturas Antigas')
                RECURSOS['Estruturas Antigas']['quantidade'] -= 1
                grid[x][y] = ''
                self.retornando_base = True
                self.destino = None
                # Comunica aos outros agentes que o recurso foi coletado
                self.comunicar_remocao_recurso((x, y))

class AgenteBDI(Agente):
    def __init__(self, tipo, posicao_inicial):
        super().__init__(tipo, posicao_inicial)
        self.crencas = []  # Informações sobre localização dos recursos
        self.desejos = 'Coletar o maior número de recursos coletivamente, considerando o valor de utilidade'
        self.intencoes = []

    def atualizar_crencas(self, grid):
        # Atualizar crenças com informações do painel de informações compartilhado
        for info in painel_informacoes:
            if info not in self.crencas:
                self.crencas.append(info)

    def agir(self, grid):
        if self.retornando_base:
            self.mover_para_base(grid)
        elif self.intencoes:
            self.mover_para_destino(grid)
        else:
            self.formular_intencoes()
            if not self.intencoes:
                self.mover_aleatoriamente(grid)

    def mover_para_destino(self, grid):
        destino_info = self.intencoes[0]
        destino_pos = destino_info['posicao']
        movimento = bfs(grid, self.posicao, destino_pos)
        if movimento:
            nova_posicao = (self.posicao[0] + movimento[0], self.posicao[1] + movimento[1])
            self.posicao = nova_posicao
        else:
            # Se o caminho estiver bloqueado, reconsidera intenções
            self.intencoes.pop(0)
            return
        # Verifica se chegou ao destino
        if self.posicao == destino_pos:
            self.coletar(grid)
            self.intencoes.pop(0)

    def formular_intencoes(self):
        # Ordena as crenças por utilidade (valor do recurso)
        self.crencas.sort(key=lambda x: RECURSOS[x['recurso']]['valor'], reverse=True)
        self.intencoes = self.crencas.copy()

    def coletar(self, grid):
        super().coletar(grid)
        # Atualiza crenças e intenções após coletar
        self.atualizar_crencas(grid)

    def comunicar_recurso(self, posicao, recurso):
        super().comunicar_recurso(posicao, recurso)

# Configurando o ambiente
grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Posicionando recursos de forma aleatória
def distribuir_recursos():
    for recurso, atributos in RECURSOS.items():
        count = 0
        while count < atributos['quantidade']:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if grid[x][y] == '':
                grid[x][y] = recurso
                count +=1
distribuir_recursos()

# Posicionando obstáculos de forma aleatória
def distribuir_obstaculos():
    count = 0
    while count < NUM_OBSTACULOS:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[x][y] == '':
            grid[x][y] = random.choice(OBSTACULOS)
            count += 1
distribuir_obstaculos()

# Exibindo o grid com recursos e obstáculos
def exibir_grid():
    simbolos = {
        '': '.',
        'Cristais Energéticos': 'C',
        'Blocos de Metal Raro': 'M',
        'Estruturas Antigas': 'E',
        'Rio': 'R',
        'Montanha': 'T',
    }
    print("\nGrid:")
    for i in range(GRID_SIZE):
        linha = ''
        for j in range(GRID_SIZE):
            if (i, j) == (0, 0):
                linha += 'B '  # Base
            else:
                linha += simbolos.get(grid[i][j], '.') + ' '
        print(linha)
exibir_grid()

# Instanciando os agentes
agentes = [
    Agente('Reativo Simples', (0, 0)),
    Agente('Baseado em Estado', (0, 0)),
    Agente('Baseado em Objetivos', (0, 0)),
    AgenteCooperativo('Cooperativo', (0, 0)),
    AgenteBDI('BDI', (0, 0))
]

# Simulação
def simular():
    total_passos = 0
    passos_restantes = TOTAL_SIMULATION_TIME
    while total_passos < TOTAL_SIMULATION_TIME:
        for agente in agentes:
            if isinstance(agente, AgenteBDI):
                agente.atualizar_crencas(grid)
            agente.mover(grid, passos_restantes)
            agente.coletar(grid)
            agente.entregar()
        total_passos += 1
        passos_restantes -= 1

        # Mostrar posições dos agentes em 1/4, 2/4, 3/4 e 4/4 do tempo total de simulação
        if total_passos == TOTAL_SIMULATION_TIME // 4 or total_passos == TOTAL_SIMULATION_TIME // 2 or \
           total_passos == (3 * TOTAL_SIMULATION_TIME) // 4 or total_passos == TOTAL_SIMULATION_TIME:
            print(f"\nPosições dos agentes no passo {total_passos}:")
            for agente in agentes:
                print(f"Agente {agente.tipo} está na posição {agente.posicao}")

        # Verificar se todos os recursos foram coletados
        recursos_restantes = sum([atributos['quantidade'] for atributos in RECURSOS.values()])
        if recursos_restantes == 0:
            print(f"\nTodos os recursos foram coletados em {total_passos} passos!")
            break

    # Garantir que os agentes retornem à base antes da tempestade de radiação
    for agente in agentes:
        while agente.posicao != (0, 0):
            agente.mover_para_base(grid)
            agente.entregar()
    print("\nTodos os agentes retornaram à base antes da tempestade de radiação.")

simular()

# Avaliando o desempenho
for agente in agentes:
    print(f'\nAgente {agente.tipo} coletou e entregou um total de {agente.total_entregue} recursos.')

# Comparação de desempenho dos agentes
print("\nComparação de desempenho dos agentes:")
agentes.sort(key=lambda x: x.total_entregue, reverse=True)
for agente in agentes:
    print(f'Agente {agente.tipo}: {agente.total_entregue} recursos entregues.')

# Relatório final de recursos entregues
print("\nRecursos entregues:")
for recurso, quantidade in recursos_entregues.items():
    print(f'{recurso}: {quantidade} unidades entregues.')