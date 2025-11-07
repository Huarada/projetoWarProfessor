# -*- coding: utf-8 -*-
"""
Servidor Flask para a API do jogo WAR.
"""
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import os

# Importar módulos do jogo WAR
from src.bot import WarBot
from src.game import GameState, GameLogic
from src.genetic_algorithm import GeneticAlgorithm
from src.config import ESTRATEGIAS, TERRITORIOS
from src.config import MAPA_WAR
from src.chatbot_service import analyze_move_with_gpt

# CHAVE DA OPENAI (mantido como você já usava)
MINHACHAVEAPI = os.environ.get("OPENAI_API_KEY")  # INSIRA SUA CHAVE AQUI SE NÃO USAR VARIÁVEL DE AMBIENTE

app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)  # Permitir requisições de qualquer origem


@app.route("/")
def serve_index():
    return app.send_static_file("index.html")


# Armazenar jogos ativos
active_games = {}

# Cores para os jogadores
PLAYER_COLORS = [
    "#FF6B6B",  # Vermelho
    "#4ECDC4",  # Turquesa
    "#45B7D1",  # Azul
    "#96CEB4",  # Verde
    "#FFEAA7",  # Amarelo
    "#DDA0DD"   # Roxo
]


class HumanPlayer:
    """Representa o jogador humano (controlado pelo usuário)."""
    def __init__(self, id_):
        self.id = id_
        self.is_human = True
        # manter nomes compatíveis com fronte/back existente
        self.estrategia = "Decisão manual"
        self.strategy = "Decisão manual"
        self.gene = "HUMANO"


class GameSession:
    """Classe para gerenciar uma sessão de jogo."""
    def __init__(self, game_id):
        self.game_id = game_id
        self.status = "waiting"  # waiting, playing, paused, finished
        self.game_state = None
        self.bots = []
        self.current_player_index = 0
        self.round_number = 0
        self.last_action = None
        self.history = []
        self.auto_play = False
        self.speed = "normal"  # slow, normal, fast
        self.created_at = datetime.now()

    def initialize_game(self):
        """Inicializa uma nova partida com 6 bots (padrão)."""

        import random

        # Função auxiliar interna — gera gene de 9 bits (E1 + E2 + P)
        def gerar_gene_hibrido():
            e1 = format(random.randint(0, 7), "03b")
            e2 = format(random.randint(0, 7), "03b")
            p = format(random.randint(0, 7), "03b")
            return e1 + e2 + p

        # Cria os 6 bots com genes híbridos
        self.bots = [WarBot(i, gerar_gene_hibrido()) for i in range(6)]

        # Mantém o fluxo normal de inicialização
        self._init_state_common()


    def initialize_with_human(self):
        """Inicializa uma nova partida com o jogador humano no id=0 + 5 bots híbridos."""
        import random

        # Função auxiliar: gera gene de 9 bits (E1 + E2 + P)
        def gerar_gene_hibrido():
            e1 = format(random.randint(0, 7), "03b")
            e2 = format(random.randint(0, 7), "03b")
            p = format(random.randint(0, 7), "03b")
            return e1 + e2 + p

        # Jogador humano (id 0)
        humano = HumanPlayer(0)

        # Cria 5 bots com genes híbridos
        bots = [WarBot(i, gerar_gene_hibrido()) for i in range(1, 6)]

        self.bots = [humano] + bots
        self._init_state_common()


    def _init_state_common(self):
        """Inicialização comum do tabuleiro/estado."""
        self.game_state = GameState()
        self.game_state.inicializar_tabuleiro(self.bots)
        self.status = "playing"
        self.current_player_index = 0
        self.round_number = 1
        self._save_state_to_history()

    def is_human_turn(self) -> bool:
        """True se o jogador atual é humano."""
        if not self.bots:
            return False
        current = self.bots[self.current_player_index]
        return getattr(current, "is_human", False) is True

    def execute_turn(self):
        """Executa o turno do jogador atual (apenas bots)."""
        if self.status != "playing":
            return False

        # Se for humano, não deixa o backend executar automaticamente
        if self.is_human_turn():
            return False

        current_bot = self.bots[self.current_player_index]

        # Verificar se o bot foi eliminado
        if GameLogic.jogador_eliminado(self.game_state, current_bot.id):
            self._next_player()
            self._save_state_to_history()
            return True

        # Reset do histórico de perdas no início de cada rodada
        if self.current_player_index == 0:
            for bot in self.bots:
                self.game_state.historico_perdas[bot.id] = False

        # Fase 1: Receber tropas
        tropas_recebidas = GameLogic.calcular_unidades_recebidas(self.game_state, current_bot.id)
        GameLogic.distribuir_tropas(self.game_state, current_bot.id, tropas_recebidas)

        # Fase 2: Atacar
        max_ataques = 10
        ataques_realizados = 0
        last_attack = None

        while ataques_realizados < max_ataques:
            jogadas = GameLogic.jogadas_possiveis(self.game_state, current_bot.id)
            ataque = current_bot.escolher_ataque(self.game_state, jogadas)

            if ataque is None:
                break

            origem, destino = ataque
            sucesso = GameLogic.executar_ataque(self.game_state, origem, destino)

            last_attack = {
                "type": "attack",
                "player": current_bot.id,
                "from": origem,
                "to": destino,
                "success": sucesso,
                "troops_moved": self.game_state.territorios[destino]['tropas'] if sucesso else 0
            }

            ataques_realizados += 1
            if not sucesso:
                break

        # Fase 3: Redistribuir tropas
        GameLogic.redistribuir_tropas(self.game_state, current_bot.id)

        # Atualizar última ação
        if last_attack:
            self.last_action = last_attack
        else:
            self.last_action = {
                "type": "no_attack",
                "player": current_bot.id,
                "reason": "no_valid_attacks"
            }

        # Verificar vencedor
        vencedor = GameLogic.verificar_vencedor(self.game_state)
        if vencedor is not None:
            self.status = "finished"
            self.last_action["winner"] = vencedor

        # Próximo jogador
        self._next_player()
        self._save_state_to_history()
        return True

    def _next_player(self):
        """Avança para o próximo jogador."""
        self.current_player_index = (self.current_player_index + 1) % len(self.bots)
        if self.current_player_index == 0:
            self.round_number += 1
            # se for o humano, calcular tropas recebidas
            if self.is_human_turn():
                tropas = GameLogic.calcular_unidades_recebidas(self.game_state, 0)
                self.game_state.tropas_disponiveis[0] += tropas


    def _save_state_to_history(self):
        """Salva o estado atual no histórico."""
        state_copy = {
            "round": self.round_number,
            "current_player": self.current_player_index,
            "territories": dict(self.game_state.territorios),
            "last_action": self.last_action,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(state_copy)

    def get_state_dict(self):
        """Retorna o estado atual como dicionário."""
        if not self.game_state:
            return {
                "game_id": self.game_id,
                "status": self.status,
                "message": "Game not initialized"
            }

        # Contar territórios e tropas por jogador
        players_info = []
        for bot in self.bots:
            territories = self.game_state.get_territorios_jogador(bot.id)
            total_troops = sum(self.game_state.territorios[t]['tropas'] for t in territories)
            is_human = getattr(bot, "is_human", False) is True
            # manter chaves já esperadas pelo front
            players_info.append({
                "id": bot.id,
                "strategy": getattr(bot, "estrategia", None) or getattr(bot, "strategy", ""),
                "gene": getattr(bot, "gene", ""),
                "territories_count": len(territories),
                "total_troops": total_troops,
                "color": PLAYER_COLORS[bot.id],
                "eliminated": len(territories) == 0,
                "is_human": is_human,
            })

        return {
            "game_id": self.game_id,
            "status": self.status,
            "current_round": self.round_number,
            "current_player": self.current_player_index,
            "human_turn": self.is_human_turn(),
            "auto_play": self.auto_play,
            "speed": self.speed,
            "territories": self.game_state.territorios,
            "players": players_info,
            "last_action": self.last_action,
            "total_turns": len(self.history)
        }


@app.route('/<path:path>')
def serve_static(path):
    """Serve arquivos estáticos do frontend."""
    try:
        return app.send_static_file(path)
    except:
        # Se o arquivo não existir, serve o index.html (para roteamento do React)
        return app.send_static_file('index.html')


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Inicia uma nova partida."""
    data = request.get_json() or {}

    game_id = str(uuid.uuid4())
    game_session = GameSession(game_id)

    # Configurar opções
    game_session.auto_play = data.get('auto_play', False)
    game_session.speed = data.get('speed', 'normal')
    include_human = data.get('include_human', False)

    # Inicializar jogo
    if include_human:
        game_session.initialize_with_human()
    else:
        game_session.initialize_game()

    # Armazenar sessão
    active_games[game_id] = game_session

    return jsonify({
        "success": True,
        "game_id": game_id,
        "state": game_session.get_state_dict()
    })


@app.route('/api/game/<game_id>/state', methods=['GET'])
def get_game_state(game_id):
    """Obtém o estado atual do jogo."""
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404

    game_session = active_games[game_id]
    return jsonify(game_session.get_state_dict())


@app.route("/health")
def health():
    return "OK", 200


@app.route('/api/game/<game_id>/next-turn', methods=['POST'])
def next_turn(game_id):
    """Executa o próximo turno (bloqueia se for a vez do humano)."""
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404

    game_session = active_games[game_id]

    if game_session.status != "playing":
        return jsonify({"error": "Game is not in playing state"}), 400

    if game_session.is_human_turn():
        return jsonify({"error": "Human turn - aguarde ação do jogador"}), 400

    success = game_session.execute_turn()
    if success:
        return jsonify({
            "success": True,
            "state": game_session.get_state_dict()
        })
    else:
        return jsonify({"error": "Failed to execute turn"}), 500


@app.route('/api/game/<game_id>/control', methods=['POST'])
def control_game(game_id):
    """Controla o jogo (pause, resume, etc.)."""
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json() or {}
    action = data.get('action')

    game_session = active_games[game_id]

    if action == 'pause':
        game_session.status = "paused"
    elif action == 'resume':
        if game_session.status == "paused":
            game_session.status = "playing"
    elif action == 'toggle_auto_play':
        game_session.auto_play = not game_session.auto_play
    elif action == 'set_speed':
        speed = data.get('speed', 'normal')
        if speed in ['slow', 'normal', 'fast']:
            game_session.speed = speed

    return jsonify({
        "success": True,
        "state": game_session.get_state_dict()
    })


@app.route('/api/games', methods=['GET'])
def list_games():
    """Lista todos os jogos ativos."""
    games_list = []
    for game_id, session in active_games.items():
        games_list.append({
            "game_id": game_id,
            "status": session.status,
            "round": session.round_number,
            "created_at": session.created_at.isoformat()
        })

    return jsonify({"games": games_list})


@app.route('/api/territories', methods=['GET'])
def get_territories():
    """Retorna a lista de territórios disponíveis."""
    return jsonify({
        "territories": TERRITORIOS,
        "strategies": ESTRATEGIAS
    })


@app.route('/api/general/chat', methods=['POST'])
def general_chat():
    """Chat livre com o General (NLP)"""
    data = request.get_json() or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Mensagem vazia"}), 400

    try:
        from openai import OpenAI
        client = OpenAI(api_key=MINHACHAVEAPI)  # usa sua chave

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é o General WAR, um estrategista militar cartunesco. Responda de forma didática, curta e engraçada, dando dicas ou comentários sobre qualquer assunto que o jogador traga."},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "Erro ao processar mensagem", "message": str(e)}), 500


@app.route('/api/game/<game_id>/analyze-move', methods=['POST'])
def analyze_move(game_id):
    """Analisa a última jogada usando IA com Teoria dos Jogos."""
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404

    game_session = active_games[game_id]

    if not game_session.game_state:
        return jsonify({"error": "Game not initialized"}), 400

    # Obter estado atual do jogo
    current_state = game_session.get_state_dict()

    # Verificar se há uma última ação para analisar
    if not game_session.last_action:
        return jsonify({
            "error": "Nenhuma jogada para analisar",
            "message": "Execute pelo menos um turno antes de solicitar análise"
        }), 400

    try:
        analysis = analyze_move_with_gpt(current_state, game_session.last_action)
        return jsonify({
            "success": True,
            "analysis": analysis,
            "analyzed_action": game_session.last_action,
            "game_round": game_session.round_number
        })

    except Exception as e:
        return jsonify({
            "error": "Erro interno do servidor",
            "message": str(e)
        }), 500


# ---------------------- NOVOS ENDPOINTS P/ HUMANO ----------------------

@app.route('/api/player/action', methods=['POST'])
def player_action():
    """
    Executa ação do jogador humano: deploy | attack | fortify.
    Body:
    {
      "game_id": "...",
      "action": "deploy" | "attack" | "fortify",
      "params": { ... }
    }
    """
    data = request.get_json() or {}
    game_id = data.get('game_id')
    action = data.get('action')
    params = data.get('params', {}) or {}

    if not game_id or game_id not in active_games:
        return jsonify({"error": "Jogo não encontrado"}), 404

    game_session = active_games[game_id]
    if not game_session.is_human_turn():
        return jsonify({"error": "Não é a vez do humano"}), 400

    gs = game_session.game_state
    player_id = 0  # humano sempre id=0 neste modo

    try:
        if action == "deploy":
            import unicodedata

            territorio_raw = params.get('territorio', '').strip()
            qtd = int(params.get('tropas', 1))
            disponiveis = game_session.game_state.tropas_disponiveis.get(player_id, 0)

            if not territorio_raw:
                return jsonify({"error": "Território não informado"}), 400
            if qtd <= 0:
                return jsonify({"error": "Quantidade inválida"}), 400
            if qtd > disponiveis:
                return jsonify({"error": f"Você só tem {disponiveis} tropas disponíveis"}), 400

            # Normaliza acentos e letras (case + accent insensitive)
            def normalizar_nome(nome):
                return ''.join(
                    c for c in unicodedata.normalize('NFD', nome)
                    if unicodedata.category(c) != 'Mn'
                ).lower()

            territorio_normalizado = normalizar_nome(territorio_raw)

            # Mapeia nomes normalizados -> nomes reais
            correspondencias = {
                normalizar_nome(t): t for t in gs.territorios.keys()
            }
            territorio = correspondencias.get(territorio_normalizado)

            if not territorio:
                return jsonify({
                    "error": f"Território '{territorio_raw}' não encontrado."
                }), 400

            # Adiciona tropas e atualiza saldo
            GameLogic.adicionar_tropas(gs, player_id, territorio, qtd)
            game_session.game_state.tropas_disponiveis[player_id] -= qtd

            # Retorna estado completo e mensagem amigável
            return jsonify({
                "message": f"Tropas colocadas em {territorio}. "
                        f"Restam {game_session.game_state.tropas_disponiveis[player_id]} tropas.",
                "remaining": game_session.game_state.tropas_disponiveis[player_id],
                "state": game_session.get_state_dict()
            }), 200
        

        elif action == "attack":
            origem = params.get('origem')
            destino = params.get('destino')

            if not origem or not destino:
                return jsonify({"error": "Origem/destino não informados"}), 400

            # Verifica se origem pertence ao jogador humano
            terr = gs.territorios
            if terr.get(origem, {}).get('dono') != player_id:
                return jsonify({"error": f"O território {origem} não pertence ao jogador humano"}), 400

            # Verifica se tem tropas suficientes para atacar
            if terr[origem]['tropas'] <= 1:
                return jsonify({"error": f"O território {origem} possui apenas {terr[origem]['tropas']} tropa(s). É necessário mais de 1 para atacar."}), 400

            # Verifica se destino é vizinho de origem
            vizinhos = MAPA_WAR.get(origem, [])
            if destino not in vizinhos:
                return jsonify({
                    "error": f"O território {destino} não é vizinho de {origem}.",
                    "message": "Só é possível atacar territórios conectados."
                }), 400

            # Executa o ataque normalmente
            sucesso = GameLogic.executar_ataque(gs, origem, destino)
            game_session.last_action = {
                "type": "attack",
                "player": player_id,
                "from": origem,
                "to": destino,
                "success": sucesso
            }


        elif action == "fortify":
            origem = params.get('origem')
            destino = params.get('destino')
            qtd = int(params.get('tropas', 1))
            if not origem or not destino:
                return jsonify({"error": "Origem/destino não informados"}), 400
            GameLogic.mover_tropas(gs, player_id, origem, destino, qtd)
            game_session.last_action = {"type": "fortify", "player": player_id, "from": origem, "to": destino, "troops": qtd}

        else:
            return jsonify({"error": "Ação inválida"}), 400

        # verificar vitória após ação humana
        vencedor = GameLogic.verificar_vencedor(gs)
        if vencedor is not None:
            game_session.status = "finished"
            game_session.last_action["winner"] = vencedor

        game_session._save_state_to_history()
        return jsonify({"success": True, "state": game_session.get_state_dict()})

    except Exception as e:
        return jsonify({"error": "Falha ao executar ação", "message": str(e)}), 500


@app.route('/api/player/end-turn', methods=['POST'])
def player_end_turn():
    """
    Humano encerra sua vez e passa para o próximo jogador.
    Body: { "game_id": "..." }
    """
    data = request.get_json() or {}
    game_id = data.get('game_id')

    if not game_id or game_id not in active_games:
        return jsonify({"error": "Jogo não encontrado"}), 404

    game_session = active_games[game_id]
    if not game_session.is_human_turn():
        return jsonify({"error": "Não é a vez do humano"}), 400

    game_session._next_player()
    game_session._save_state_to_history()
    return jsonify({"success": True, "state": game_session.get_state_dict()})

# ----------------------------------------------------------------------


if __name__ == '__main__':
    print("Iniciando servidor Flask para WAR Game API...")
    print("Acesse http://localhost:5000 para a API")
    app.run(host='0.0.0.0', port=5000, debug=True)

