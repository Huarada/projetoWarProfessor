# Back-end do Jogo WAR com Algoritmo Genético

Este projeto implementa um back-end em Python para simular partidas do jogo WAR entre bots controlados por IA, onde cada bot utiliza uma estratégia definida por um algoritmo genético.

## 🎯 Características Principais

- **6 Bots Simultâneos**: Cada partida é jogada entre 6 bots com diferentes estratégias
- **8 Estratégias Diferentes**: Baseadas em genes de 3 bits (000 a 111)
- **Algoritmo Genético**: Evolução das estratégias ao longo de gerações
- **Simulação Realista**: Implementação completa das regras do WAR
- **Heurísticas Avançadas**: Distribuição inteligente de tropas baseada em ameaças

## 🧬 Estratégias Disponíveis

| Gene | Estratégia | Descrição |
|------|------------|-----------|
| 000 | Pacifista absoluto | Não ataca nunca, só se defende |
| 001 | Contra-golpe | Só ataca se foi atacado no turno anterior |
| 010 | Fortaleza | Só ataca inimigos muito mais fracos (2:1) |
| 011 | Retomada | Prioriza reconquistar territórios perdidos |
| 100 | Expansão segura | Ataca com vantagem clara (diferença de 3+) |
| 101 | Oportunista | Ataca territórios mal defendidos (1-2 tropas) |
| 110 | Invasor moderado | Ataca quando tem mais tropas que o adversário |
| 111 | Caçador de bônus | Foca em conquistar continentes completos |

## 📁 Estrutura do Projeto

```
backend/
├── config.py              # Configurações e constantes
├── game.py                 # Lógica do jogo WAR
├── bot.py                  # Implementação dos bots
├── genetic_algorithm.py    # Algoritmo genético
├── main.py                 # Simulação completa
├── demo.py                 # Demonstração rápida
├── requirements.txt        # Dependências
└── README.md              # Esta documentação
```

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Execução Rápida (Demonstração)

```bash
# Executar demonstração com configurações reduzidas
python demo.py
```

### Simulação Completa

```bash
# Executar simulação completa (500 gerações)
python main.py
```

### Configurações Personalizadas

Edite o arquivo `config.py` para ajustar:

- `NUM_GERACOES`: Número de gerações do algoritmo genético (padrão: 500)
- `NUM_INDIVIDUOS`: Tamanho da população (padrão: 40)
- `NUM_PARTIDAS_SIM`: Partidas por avaliação (padrão: 20)
- `TAXA_MUTACAO_INICIAL`: Taxa inicial de mutação (padrão: 0.7)
- `TAXA_CROSSOVER_INICIAL`: Taxa inicial de crossover (padrão: 0.7)

## 🎮 Mecânicas do Jogo

### Inicialização
- 42 territórios distribuídos aleatoriamente entre 6 jogadores
- 20 tropas iniciais por jogador
- Cada território começa com pelo menos 1 tropa

### Turno do Jogador
1. **Receber Tropas**: Baseado em territórios controlados e bônus de continentes
2. **Distribuir Tropas**: Usando heurística NBSRx (Normalized Border Strength Ratio)
3. **Atacar**: Baseado na estratégia do bot (até 10 ataques por turno)
4. **Redistribuir**: Mover tropas de territórios internos para fronteiras

### Combate
- Atacante vence se tiver mais tropas que o defensor
- Atacante perde 20% das tropas do defensor (punição reduzida)
- Território conquistado recebe tropas do atacante (deixando 1 na origem)

### Vitória
- Controlar todos os 42 territórios
- Ou ter mais territórios após 100 rodadas (limite de tempo)

## 🧠 Algoritmo Genético

### Parâmetros
- **População**: 40 indivíduos
- **Gerações**: 500
- **Elitismo**: 6 melhores preservados
- **Mutação**: Taxa decrescente (0.7 → 0.35)
- **Crossover**: Taxa decrescente (0.7 → 0.49)

### Fitness
- **Vitórias**: 100 pontos por vitória
- **Territórios**: 2 pontos por território conquistado
- **Fórmula**: `(vitórias/partidas × 100) + (territórios_médios × 2)`

### Evolução
1. **Avaliação**: Cada bot joga 20 partidas contra outros bots aleatórios
2. **Seleção**: Elitismo + seleção por roleta
3. **Crossover**: Ponto único entre genes de 3 bits
4. **Mutação**: Bit flip com probabilidade decrescente

## 📊 Resultados Esperados

Com base nos testes realizados, as estratégias mais eficazes tendem a ser:

1. **Invasor moderado (110)**: Equilibrio entre agressividade e cautela
2. **Expansão segura (100)**: Ataques calculados com vantagem
3. **Oportunista (101)**: Aproveitamento de territórios fracos

As estratégias defensivas (Pacifista, Fortaleza) tendem a ter menor fitness devido à natureza competitiva do jogo.

## 🔧 Personalização

### Adicionando Novas Estratégias

1. Edite `config.py` para adicionar novos mapeamentos em `ESTRATEGIAS`
2. Modifique `bot.py` no método `escolher_ataque()` para implementar a lógica
3. Ajuste o tamanho do gene se necessário (atualmente 3 bits = 8 estratégias)

### Modificando Regras do Jogo

- **Combate**: Edite `GameLogic.executar_ataque()` em `game.py`
- **Distribuição**: Modifique as heurísticas em `GameLogic.distribuir_tropas()`
- **Mapa**: Altere `MAPA_WAR` e `TERRITORIOS` em `config.py`

## 📈 Monitoramento

O sistema gera automaticamente:

- **Logs de execução**: Progresso das gerações em tempo real
- **Arquivo JSON**: Resultados detalhados salvos em `resultados_simulacao.json`
- **Estatísticas**: Fitness por geração, distribuição de estratégias

## ⚡ Performance

- **Partida individual**: ~0.05 segundos
- **Geração completa**: ~30-60 segundos
- **Simulação completa**: ~4-8 horas (500 gerações)

## 🤝 Baseado no Trabalho Original

Este back-end foi desenvolvido com base no notebook Jupyter `Genetica_testeGenomaDiminuicaoPunitivaTeste3.ipynb`, mantendo fidelidade às heurísticas e algoritmos originais, mas com uma arquitetura modular e extensível.

---

**Desenvolvido para demonstrar a aplicação de algoritmos genéticos em jogos de estratégia.**



## 🤖 Chatbot de Análise com OpenAI

### Funcionalidade

O sistema agora inclui um chatbot integrado que utiliza a API da OpenAI para analisar jogadas usando conceitos de **Teoria dos Jogos**. O chatbot é ativado apenas quando solicitado pelo usuário através do botão "Analisar Jogada" na interface, economizando créditos da API.

### Configuração da API OpenAI

**IMPORTANTE**: Para utilizar o chatbot, você deve configurar sua chave da API OpenAI.

#### Opção 1: Variável de Ambiente (Recomendado)
```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

#### Opção 2: Edição Direta do Código
Edite o arquivo `chatbot_service.py` e insira sua chave na linha:
```python
openai.api_key = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_AQUI")
```

### Como Funciona

1. **Ativação**: O usuário clica no botão "Analisar Jogada" na interface do jogo
2. **Coleta de Dados**: O sistema captura o estado atual do tabuleiro e a última ação realizada
3. **Análise**: A IA analisa a jogada usando conceitos como:
   - Equilíbrio de Nash
   - Estratégias dominantes e dominadas
   - Payoff esperado
   - Risco versus recompensa
   - Ameaças e alianças implícitas
   - Controle de territórios críticos
4. **Resposta**: O chatbot retorna uma análise detalhada (máximo 500 palavras) explicando o raciocínio estratégico

### Endpoint da API

```
POST /api/game/<game_id>/analyze-move
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "analysis": "Análise detalhada da jogada...",
  "analyzed_action": {
    "type": "attack",
    "player": 0,
    "from": "Brasil",
    "to": "Argentina",
    "success": true
  },
  "game_round": 5
}
```

**Resposta de Erro:**
```json
{
  "error": "Nenhuma jogada para analisar",
  "message": "Execute pelo menos um turno antes de solicitar análise"
}
```

### Limitações

- Requer chave válida da API OpenAI
- Funciona apenas após pelo menos uma jogada ter sido executada
- Análise limitada a 500 palavras para otimizar custos
- Utiliza o modelo `gpt-4o-mini` para equilibrar qualidade e custo

### Arquivos Relacionados

- `chatbot_service.py`: Serviço de integração com OpenAI
- `main.py`: Endpoint `/analyze-move` adicionado
- `GameBoard.jsx`: Interface com botão "Analisar Jogada"

### Solução de Problemas

**Erro: "Chave da API OpenAI não configurada"**
- Verifique se a variável de ambiente `OPENAI_API_KEY` está definida
- Ou edite diretamente o arquivo `chatbot_service.py`

**Erro: "Nenhuma jogada para analisar"**
- Execute pelo menos um turno do jogo antes de solicitar análise

**Erro de conexão com OpenAI**
- Verifique sua conexão com a internet
- Confirme se sua chave da API é válida e tem créditos disponíveis

