# -*- coding: utf-8 -*-
"""
Servidor Flask para a API do jogo WAR.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import threading
import time
from datetime import datetime
import os

# Importar módulos do jogo WAR
from src.bot import WarBot
from src.game import GameState, GameLogic
from src.genetic_algorithm import GeneticAlgorithm
from src.config import ESTRATEGIAS, TERRITORIOS
from src.chatbot_service import analyze_move_with_gpt


#CHAVE DA OPENAI

MINHACHAVEAPI = os.environ.get("OPENAI_API_KEY") #INSIRA SUA CHAVE AQUI

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
        """Inicializa uma nova partida."""
        # Criar bots com estratégias diferentes
        self.bots = [
            WarBot(0, '000'),  # Pacifista absoluto
            WarBot(1, '101'),  # Oportunista
            WarBot(2, '110'),  # Invasor moderado
            WarBot(3, '111'),  # Caçador de bônus
            WarBot(4, '100'),  # Expansão segura
            WarBot(5, '010'),  # Fortaleza
        ]
        
        # Inicializar estado do jogo
        self.game_state = GameState()
        self.game_state.inicializar_tabuleiro(self.bots)
        
        self.status = "playing"
        self.current_player_index = 0
        self.round_number = 1
        
        # Salvar estado inicial no histórico
        self._save_state_to_history()
        
    def execute_turn(self):
        """Executa o turno do jogador atual."""
        if self.status != "playing":
            return False
            
        current_bot = self.bots[self.current_player_index]
        
        # Verificar se o bot foi eliminado
        if GameLogic.jogador_eliminado(self.game_state, current_bot.id):
            self._next_player()
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
        
        # Salvar estado no histórico
        self._save_state_to_history()
        
        return True
    
    def _next_player(self):
        """Avança para o próximo jogador."""
        self.current_player_index = (self.current_player_index + 1) % len(self.bots)
        if self.current_player_index == 0:
            self.round_number += 1
    
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
            
            players_info.append({
                "id": bot.id,
                "strategy": bot.estrategia,
                "gene": bot.gene,
                "territories_count": len(territories),
                "total_troops": total_troops,
                "color": PLAYER_COLORS[bot.id],
                "eliminated": len(territories) == 0
            })
        
        return {
            "game_id": self.game_id,
            "status": self.status,
            "current_round": self.round_number,
            "current_player": self.current_player_index,
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
    
    # Inicializar jogo
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
    """Executa o próximo turno."""
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    game_session = active_games[game_id]
    
    if game_session.status != "playing":
        return jsonify({"error": "Game is not in playing state"}), 400
    
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
        # Aqui você pode usar OpenAI diretamente
        from openai import OpenAI
        client = OpenAI(api_key=MINHACHAVEAPI) #Insira sua chave OPENAI aqui

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ou gpt-3.5 se preferir
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
        # Chamar o serviço de análise
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

if __name__ == '__main__':
    print("Iniciando servidor Flask para WAR Game API...")
    print("Acesse http://localhost:5000 para a API")
    app.run(host='0.0.0.0', port=5000, debug=True)

