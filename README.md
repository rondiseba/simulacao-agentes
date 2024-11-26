# simulacao-agentes
Atividade apresentada a disciplina de IA, curso de Ciências da Computação - UFMA

Simulação de coleta de recursos por agentes autônomos, com ambiente aleatorio.

Apresentação

Este projeto consiste em uma simulação onde diferentes tipos de agentes autônomos exploram um ambiente bidimensional (grid) para coletar recursos antes que ocorra uma tempestade de radiação. O objetivo é avaliar o desempenho de cada agente com base em suas características e estratégias de coleta.

Visão Geral da Simulação

Ambiente: Um grid bidimensional de tamanho definido pelo usuário (entre 10 e 20).
Recursos: Três tipos de recursos disponíveis no ambiente:
Cristais Energéticos (valor: 10)
Blocos de Metal Raro (valor: 20)
Estruturas Antigas (valor: 50)
Obstáculos: Rios e montanhas distribuídos aleatoriamente no grid.
Agentes: Cinco tipos de agentes com diferentes características e comportamentos.
Principais Funcionalidades

Configuração Personalizada: O usuário pode definir o tamanho do grid e o tempo total até a próxima tempestade de radiação (máximo de 200 passos).
Geração Aleatória de Recursos e Obstáculos: Recursos e obstáculos são posicionados aleatoriamente no grid, garantindo uma simulação única a cada execução.
Diversidade de Agentes: Cada agente possui comportamentos específicos que influenciam sua eficiência na coleta de recursos.
Movimentação Inteligente: Implementação do algoritmo BFS (Busca em Largura) para que os agentes planejem rotas evitando obstáculos.
Comunicação entre Agentes: Alguns agentes compartilham informações sobre a localização de recursos, melhorando a eficiência coletiva.
Simulação do Tempo: Os agentes devem gerenciar seu tempo para retornar à base antes da tempestade de radiação.
Relatórios de Desempenho: Ao final da simulação, é apresentado um resumo do desempenho de cada agente e a quantidade total de recursos coletados.
Descrição dos Agentes

1. Agente Reativo Simples
Características:
Move-se aleatoriamente pelo ambiente.
Coleta apenas Cristais Energéticos quando encontra um.
Objetivo: Explorar o ambiente sem memória ou planejamento, reagindo apenas ao encontrar um recurso específico.
2. Agente Baseado em Estado
Características:
Possui memória para evitar revisitar áreas já exploradas.
Pode armazenar informações sobre outros agentes.
Objetivo: Coletar o maior número de recursos coletivamente, considerando o valor de utilidade.
3. Agente Baseado em Objetivos
Características:
Focado em maximizar o número de recursos entregues.
Planeja rotas até recursos conhecidos utilizando o algoritmo BFS.
Objetivo: Priorizar a eficiência na coleta, direcionando-se diretamente aos recursos.
4. Agente Cooperativo (Baseado em Utilidade)
Características:
Calcula a utilidade de ajudar outros agentes a coletar recursos grandes com base na distância e no número de agentes disponíveis.
Pode colaborar na coleta de Estruturas Antigas, que requerem mais de um agente.
Objetivo: Melhorar a eficiência coletiva através da cooperação estratégica.
5. Agente BDI (Belief-Desire-Intention)
Características:
Recebe informações de todos os agentes sobre a localização dos recursos, atualizando suas crenças.
Administra um painel de informações com a localização dos recursos conhecidos.
Objetivo: Coletar o maior número de recursos coletivamente, considerando o valor de utilidade, através de um processo deliberativo baseado em crenças, desejos e intenções.



