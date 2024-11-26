# simulacao-agentes
Atividade apresentada a disciplina de IA, curso de Ciências da Computação - UFMA
Prof. Dr. Tiago Bonini
Rondineli Seba Salomão

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

Características do Ambiente

Grid: Representa o ambiente bidimensional onde os agentes se movem.
Base: Localizada na posição (0, 0), é o ponto de partida e retorno dos agentes.
Obstáculos: Distribuídos aleatoriamente, representam rios e montanhas que os agentes devem evitar.
Recursos: Distribuídos aleatoriamente, possuem quantidades limitadas e valores distintos.
Funcionamento da Simulação

Inicialização:
O usuário define o tamanho do grid e o tempo total de simulação.
Recursos e obstáculos são distribuídos aleatoriamente no grid.
Os agentes são posicionados na base.
Execução da Simulação:
Em cada passo, os agentes:
Atualizam suas crenças (quando aplicável).
Decidem se devem retornar à base.
Movem-se de acordo com suas estratégias.
Coletam recursos disponíveis em suas posições.
Entregam recursos na base.
O tempo total é decrementado a cada passo.
Exibição de Informações:
As posições dos agentes são exibidas em 1/4, 2/4, 3/4 e 4/4 do tempo total de simulação.
Informações sobre recursos coletados e desempenho são apresentadas ao final.
Encerramento:
Antes da tempestade de radiação, é garantido que todos os agentes retornem à base.
Um relatório final é gerado, comparando o desempenho dos agentes e detalhando os recursos coletados.
Resultados Esperados

Desempenho dos Agentes: Espera-se que agentes com estratégias mais avançadas (como o Agente BDI) tenham um desempenho superior na coleta de recursos de maior valor.
Cooperação: Agentes cooperativos podem melhorar a eficiência coletiva, especialmente na coleta de recursos que exigem colaboração.
Aprendizado: O Agente Baseado em Estado evita áreas já exploradas, otimizando sua exploração.
Conclusão

Este projeto demonstra a implementação de diferentes paradigmas de agentes autônomos em um ambiente simulado. Através da interação entre agentes e ambiente, é possível observar como diferentes estratégias impactam na eficiência e no desempenho coletivo. A simulação fornece uma plataforma para estudar comportamentos emergentes e a eficácia de técnicas de inteligência artificial na resolução de problemas complexos.

Possíveis Extensões

Implementação de Novos Agentes: Como agentes baseados em aprendizado de máquina ou agentes adaptativos.
Melhoria na Cooperação: Desenvolvimento de protocolos de comunicação mais avançados entre os agentes.
Ambientes Dinâmicos: Introduzir mudanças no ambiente durante a simulação, como novos recursos ou obstáculos.



