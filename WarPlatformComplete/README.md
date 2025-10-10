# WAR Platform - Estratégia e Teoria dos Jogos

## Descrição

Esta é uma plataforma educacional para ensino de estratégia usando o jogo WAR com IA e Algoritmos Genéticos. O projeto inclui um backend Flask e um frontend web que simula partidas entre bots IA, com integração de um chatbot OpenAI para análise de jogadas usando Teoria dos Jogos.

## Funcionalidades

- 🎮 **Simulação de Jogo WAR**: Partidas automáticas entre 6 bots IA com diferentes estratégias
- 🧠 **Análise de Jogadas com IA**: Chatbot integrado com OpenAI que analisa jogadas usando Teoria dos Jogos
- 📊 **Visualização em Tempo Real**: Mapa interativo mostrando territórios, tropas e movimentações
- ⚡ **Controles de Velocidade**: Auto-play com velocidades configuráveis (lento, normal, rápido)
- 📈 **Estatísticas Detalhadas**: Acompanhamento de turnos, rodadas e status dos jogadores

## Estrutura do Projeto

```
warEstrategiaBackFuncionalManus/
├── war-api/                    # Backend Flask
│   └── src/
│       ├── main.py            # Servidor principal
│       ├── chatbot_service.py # Integração OpenAI
│       ├── static/            # Frontend compilado
│       └── requirements.txt   # Dependências Python
└── war-platform/              # Frontend React (código fonte)
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Configuração e Instalação

### Pré-requisitos

- Python 3.8+
- Node.js 16+
- Chave da API OpenAI

### 1. Configuração do Backend

```bash
cd war-api/src
pip install -r requirements.txt
```

### 2. Configuração da API OpenAI

**IMPORTANTE**: Você precisa configurar sua chave da API OpenAI antes de usar o chatbot.

Abra o arquivo `war-api/src/chatbot_service.py` e localize a linha:

```python
openai.api_key = "SUA_CHAVE_OPENAI_AQUI"  # ⚠️ SUBSTITUA PELA SUA CHAVE
```

Substitua `"SUA_CHAVE_OPENAI_AQUI"` pela sua chave real da OpenAI.

**Alternativa**: Configure como variável de ambiente:

```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

### 3. Executar a Aplicação

#### 1.Backend
```bash
cd war-api/src
python main.py
```
#### 2.Front-end
```bash
cd WarPlatformComplete/war-platform
npm install
npm run dev       # http://localhost:5173
```

A aplicação estará disponível em: `http://localhost:5000`

## Como Usar

### Interface Principal

1. **Acesse** `http://localhost:5000` no seu navegador
2. **Clique** em "Iniciar Jogo" no menu superior
3. **Inicie uma partida** clicando em "Iniciar Partida"

### Controles do Jogo

- **Iniciar Partida**: Cria um novo jogo com 6 bots IA
- **Próximo Turno**: Executa o próximo turno manualmente
- **🧠 Analisar Jogada**: Analisa a última jogada usando IA (requer API OpenAI)
- **Reiniciar**: Reseta o jogo atual
- **Auto Play**: Execução automática de turnos
- **Velocidade**: Controla a velocidade do auto-play

### Análise de Jogadas com IA

O chatbot OpenAI analisa as jogadas usando conceitos de Teoria dos Jogos:

- **Equilíbrio de Nash**: Identifica estratégias ótimas
- **Estratégias Dominantes**: Avalia vantagens competitivas
- **Payoff Esperado**: Calcula retornos esperados
- **Análise de Risco**: Avalia probabilidades de sucesso

**Para usar a análise:**
1. Execute pelo menos um turno
2. Clique no botão "🧠 Analisar Jogada"
3. Aguarde a análise (pode levar alguns segundos)
4. Veja o resultado no painel lateral

## API Endpoints

### Jogo

- `POST /api/game/start` - Inicia um novo jogo
- `POST /api/game/<game_id>/next-turn` - Executa próximo turno
- `GET /api/game/<game_id>/state` - Obtém estado atual do jogo

### Análise IA

- `POST /api/game/<game_id>/analyze-move` - Analisa a última jogada com OpenAI

**Exemplo de resposta da análise:**

```json
{
  "success": true,
  "analysis": "Análise estratégica detalhada da jogada usando Teoria dos Jogos..."
}
```

## Estratégias dos Bots

Os bots IA implementam diferentes estratégias:

1. **Pacifista absoluto** - Evita conflitos
2. **Oportunista** - Ataca quando vantajoso
3. **Invasor moderado** - Estratégia equilibrada
4. **Caçador de bônus** - Foca em bônus de continente
5. **Expansão segura** - Crescimento controlado
6. **Fortaleza** - Estratégia defensiva

## Desenvolvimento

### Frontend (React)

Para modificar o frontend:

```bash
cd war-platform
npm install
npm run dev  # Desenvolvimento
npm run build  # Produção
```

### Backend (Flask)

O backend está em `war-api/src/main.py`. Principais componentes:

- **Game Logic**: Lógica do jogo WAR
- **Bot Strategies**: Implementação das estratégias IA
- **OpenAI Integration**: Chatbot para análise de jogadas

## Solução de Problemas

### Erro: "Chave da API OpenAI não configurada"

- Verifique se configurou a chave no arquivo `chatbot_service.py`
- Ou configure a variável de ambiente `OPENAI_API_KEY`

### Erro: "Módulo não encontrado"

```bash
pip install -r requirements.txt
```

### Interface não carrega

- Verifique se o servidor Flask está rodando na porta 5000
- Acesse `http://localhost:5000` (não `127.0.0.1`)

### Botão "Analisar Jogada" não funciona

- Certifique-se de que a chave OpenAI está configurada
- Execute pelo menos um turno antes de tentar analisar
- Verifique a conexão com a internet

## Tecnologias Utilizadas

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **IA**: OpenAI GPT-4
- **Visualização**: SVG, Canvas
- **Arquitetura**: REST API

## Licença

MIT License - Veja o arquivo LICENSE para detalhes.

## Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Suporte

Para dúvidas ou problemas:

- Abra uma issue no GitHub
- Verifique a documentação da API OpenAI
- Consulte os logs do Flask para debugging

---

**Desenvolvido para fins educacionais - Ensino de Estratégia e Teoria dos Jogos**

