# -*- coding: utf-8 -*-
"""
Módulo de lógica do jogo WAR.
Contém as classes GameState e GameLogic para gerenciar o estado e as regras do jogo.
"""

import random
from collections import deque
from src.config import TERRITORIOS,MAPA_WAR, CONTINENTES, BONUS_CONTINENTES, NUM_JOGADORES, TROPAS_INICIAIS_POR_JOGADOR



class GameState:
    """Representa o estado atual do tabuleiro do jogo WAR."""
    
    def __init__(self):
        self.territorios = {}
        self.jogadores = []
        self.rodada_atual = 0
        self.historico_perdas = {}  # Para rastrear se um jogador perdeu território na rodada anterior
        
    def inicializar_tabuleiro(self, jogadores):
        """Inicializa o tabuleiro com territórios e jogadores."""
        self.jogadores = jogadores
        
        # Inicializar todos os territórios
        for territorio in TERRITORIOS:
            self.territorios[territorio] = {
                'dono': None,
                'tropas': 0
            }
        
        # Distribuir territórios aleatoriamente entre os jogadores
        territorios_embaralhados = TERRITORIOS.copy()
        random.shuffle(territorios_embaralhados)
        
        for i, territorio in enumerate(territorios_embaralhados):
            jogador = jogadores[i % len(jogadores)]
            self.territorios[territorio]['dono'] = jogador.id
            self.territorios[territorio]['tropas'] = 1  # Cada território começa com 1 tropa
        
        # Distribuir tropas restantes
        tropas_restantes_por_jogador = TROPAS_INICIAIS_POR_JOGADOR - (len(TERRITORIOS) // len(jogadores))
        
        for jogador in jogadores:
            meus_territorios = self.get_territorios_jogador(jogador.id)
            tropas_restantes = tropas_restantes_por_jogador
            
            # Distribuir tropas restantes aleatoriamente
            while tropas_restantes > 0:
                territorio = random.choice(meus_territorios)
                self.territorios[territorio]['tropas'] += 1
                tropas_restantes -= 1
        
        # Inicializar histórico de perdas
        for jogador in jogadores:
            self.historico_perdas[jogador.id] = False
    
    def get_territorios_jogador(self, jogador_id):
        """Retorna lista de territórios pertencentes ao jogador."""
        return [t for t, info in self.territorios.items() if info['dono'] == jogador_id]
    
    def get_inimigos_jogador(self, jogador_id):
        """Retorna lista de territórios que não pertencem ao jogador."""
        return [t for t, info in self.territorios.items() if info['dono'] != jogador_id]
    
    def copy(self):
        """Retorna uma cópia profunda do estado do jogo."""
        return copy.deepcopy(self)


class GameLogic:
    """Contém a lógica e regras do jogo WAR."""
    
    @staticmethod
    def calcular_unidades_recebidas(game_state, jogador_id):
        """Calcula o número de tropas que um jogador recebe no início do turno."""
        meus_territorios = game_state.get_territorios_jogador(jogador_id)
        
        # Tropas base: número de territórios dividido por 2 (mínimo 3)
        tropas_base = max(3, len(meus_territorios) // 2)
        
        # Bônus por continentes
        bonus_continentes = GameLogic.bonus_continentes(game_state, jogador_id)
        
        return tropas_base + bonus_continentes
    
    @staticmethod
    def bonus_continentes(game_state, jogador_id):
        """Calcula o bônus de tropas por continentes controlados."""
        bonus = 0
        for nome_continente, territorios_continente in CONTINENTES.items():
            if all(game_state.territorios[t]['dono'] == jogador_id for t in territorios_continente):
                bonus += BONUS_CONTINENTES[nome_continente]
        return bonus
    
    @staticmethod
    def calcular_BSTx(game_state, territorio, inimigos):
        """Calcula Border Strength Total - soma das tropas inimigas adjacentes."""
        return sum(game_state.territorios[t]['tropas'] for t in MAPA_WAR[territorio] if t in inimigos)
    
    @staticmethod
    def calcular_BSRx(game_state, territorio, inimigos):
        """Calcula Border Strength Ratio - razão entre tropas inimigas adjacentes e próprias."""
        bstx = GameLogic.calcular_BSTx(game_state, territorio, inimigos)
        unidades_x = game_state.territorios[territorio]['tropas']
        return bstx / unidades_x if unidades_x > 0 else float('inf')
    
    @staticmethod
    def calcular_NBSRx(game_state, meus_territorios, inimigos):
        """Calcula Normalized Border Strength Ratio para todos os territórios."""
        bsrxs = {t: GameLogic.calcular_BSRx(game_state, t, inimigos) for t in meus_territorios}
        soma = sum(bsrxs.values())
        return {t: (bsrxs[t] / soma if soma > 0 else 0) for t in meus_territorios}
    
    @staticmethod
    def distribuir_tropas(game_state, jogador_id, unidades_disponiveis):
        """Distribui tropas usando a heurística NBSRx."""
        meus_territorios = game_state.get_territorios_jogador(jogador_id)
        inimigos = game_state.get_inimigos_jogador(jogador_id)
        
        if not meus_territorios:
            return
        
        nbsrxs = GameLogic.calcular_NBSRx(game_state, meus_territorios, inimigos)
        
        # Distribuir tropas proporcionalmente ao NBSRx
        for territorio in meus_territorios:
            alocar = int(round(nbsrxs[territorio] * unidades_disponiveis))
            game_state.territorios[territorio]['tropas'] += alocar
            unidades_disponiveis -= alocar
        
        # Distribuir tropas restantes para o território mais ameaçado
        if unidades_disponiveis > 0 and meus_territorios:
            mais_ameacado = max(nbsrxs, key=nbsrxs.get)
            game_state.territorios[mais_ameacado]['tropas'] += unidades_disponiveis
    
    @staticmethod
    def jogadas_possiveis(game_state, jogador_id):
        """Retorna lista de ataques possíveis para um jogador."""
        meus_territorios = game_state.get_territorios_jogador(jogador_id)
        jogadas = []
        
        for territorio in meus_territorios:
            if game_state.territorios[territorio]['tropas'] > 1:  # Precisa ter mais de 1 tropa para atacar
                for adjacente in MAPA_WAR[territorio]:
                    if game_state.territorios[adjacente]['dono'] != jogador_id:
                        jogadas.append((territorio, adjacente))
        
        return jogadas
    
    @staticmethod
    def executar_ataque(game_state, origem, destino):
        """Executa um ataque entre dois territórios."""
        tropas_atacante = game_state.territorios[origem]['tropas']
        tropas_defensor = game_state.territorios[destino]['tropas']
        dono_defensor = game_state.territorios[destino]['dono']
        
        if tropas_atacante > tropas_defensor:
            # Ataque bem-sucedido
            # Punição reduzida: atacante perde apenas 20% das tropas do defensor
            perda = int(round(tropas_defensor * 0.2))
            tropas_restantes = tropas_atacante - perda
            tropas_movidas = max(1, tropas_restantes - 1)
            
            # Atualizar territórios
            game_state.territorios[destino]['dono'] = game_state.territorios[origem]['dono']
            game_state.territorios[destino]['tropas'] = tropas_movidas
            game_state.territorios[origem]['tropas'] = 1
            
            # Marcar que o defensor perdeu território
            game_state.historico_perdas[dono_defensor] = True
            
            return True
        else:
            # Ataque falhou - atacante perde 1 tropa
            game_state.territorios[origem]['tropas'] -= 1
            return False
    
    @staticmethod
    def territorios_conectados(game_state, origem, meus_territorios):
        """Retorna todos territórios conectados à origem usando BFS."""
        visitados = set()
        fila = deque([origem])
        
        while fila:
            atual = fila.popleft()
            if atual not in visitados and atual in meus_territorios:
                visitados.add(atual)
                for vizinho in MAPA_WAR[atual]:
                    if vizinho in meus_territorios and vizinho not in visitados:
                        fila.append(vizinho)
        
        if origem in visitados:
            visitados.remove(origem)
        return visitados
    
    @staticmethod
    def redistribuir_tropas(game_state, jogador_id):
        """Redistribui tropas usando heurística defensiva nas fronteiras."""
        meus_territorios = game_state.get_territorios_jogador(jogador_id)
        inimigos = game_state.get_inimigos_jogador(jogador_id)
        
        if not meus_territorios:
            return
        
        # Calcular NBSRx para todos os territórios
        nbsrxs = GameLogic.calcular_NBSRx(game_state, meus_territorios, inimigos)
        
        # Identificar fronteiras (territórios com vizinhos inimigos)
        fronteiras = []
        internos = []
        
        for territorio in meus_territorios:
            tem_vizinho_inimigo = any(
                game_state.territorios[v]['dono'] != jogador_id 
                for v in MAPA_WAR[territorio]
            )
            if tem_vizinho_inimigo:
                fronteiras.append(territorio)
            else:
                internos.append(territorio)
        
        # Mover tropas excedentes dos territórios internos para as fronteiras
        for t_interno in internos:
            tropas_excedente = game_state.territorios[t_interno]['tropas'] - 1
            if tropas_excedente <= 0:
                continue
            
            # Encontrar fronteiras conectadas
            conectados = GameLogic.territorios_conectados(game_state, t_interno, meus_territorios)
            fronteiras_conectadas = [f for f in fronteiras if f in conectados]
            
            if not fronteiras_conectadas:
                continue
            
            # Distribuir proporcionalmente ao NBSRx das fronteiras conectadas
            soma_pesos = sum(nbsrxs[f] for f in fronteiras_conectadas)
            
            for fronteira in fronteiras_conectadas:
                if tropas_excedente <= 0:
                    break
                
                frac = nbsrxs[fronteira] / soma_pesos if soma_pesos > 0 else 1 / len(fronteiras_conectadas)
                mover = int(round(frac * tropas_excedente))
                mover = min(mover, tropas_excedente)
                
                if mover > 0:
                    game_state.territorios[t_interno]['tropas'] -= mover
                    game_state.territorios[fronteira]['tropas'] += mover
                    tropas_excedente -= mover
    
    @staticmethod
    def verificar_vencedor(game_state):
        """Verifica se há um vencedor (jogador que controla todos os territórios)."""
        donos = set(info['dono'] for info in game_state.territorios.values())
        if len(donos) == 1:
            return list(donos)[0]
        return None
    
    @staticmethod
    def jogador_eliminado(game_state, jogador_id):
        """Verifica se um jogador foi eliminado (não possui territórios)."""
        return len(game_state.get_territorios_jogador(jogador_id)) == 0

