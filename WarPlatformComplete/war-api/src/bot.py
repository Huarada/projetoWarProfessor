# -*- coding: utf-8 -*-
"""
Módulo de bot para o jogo WAR.
Contém a classe WarBot que representa um jogador controlado por IA.
"""

import random
from src.config import ESTRATEGIAS


class WarBot:
    """Representa um jogador controlado por IA no jogo WAR."""
    
    def __init__(self, bot_id, gene):
        self.id = bot_id
        self.gene = gene
        self.estrategia = ESTRATEGIAS.get(gene, "Estratégia desconhecida")
        self.vitorias = 0
        self.territorios_conquistados = 0
        self.partidas_jogadas = 0
        self.fitness = 0.0
    
    def escolher_ataque(self, game_state, jogadas_possiveis):
        """Decide qual ataque realizar com base na estratégia do bot."""
        if not jogadas_possiveis:
            return None
        
        perdeu_territorio = game_state.historico_perdas.get(self.id, False)
        
        if self.gene == '000':  # Pacifista absoluto
            return None
        
        elif self.gene == '001':  # Contra-golpe
            if perdeu_territorio:
                return jogadas_possiveis[0]
            else:
                return None
        
        elif self.gene == '010':  # Fortaleza
            for origem, destino in jogadas_possiveis:
                tropas_origem = game_state.territorios[origem]['tropas']
                tropas_destino = game_state.territorios[destino]['tropas']
                if tropas_origem > 2 * tropas_destino:
                    return (origem, destino)
            return None
        
        elif self.gene == '011':  # Retomada
            if perdeu_territorio:
                for origem, destino in jogadas_possiveis:
                    if game_state.territorios[destino]['dono'] != self.id:
                        return (origem, destino)
            return None
        
        elif self.gene == '100':  # Expansão segura
            for origem, destino in jogadas_possiveis:
                tropas_origem = game_state.territorios[origem]['tropas']
                tropas_destino = game_state.territorios[destino]['tropas']
                if tropas_origem > tropas_destino + 2:
                    return (origem, destino)
            return None
        
        elif self.gene == '101':  # Oportunista
            for origem, destino in jogadas_possiveis:
                tropas_destino = game_state.territorios[destino]['tropas']
                if tropas_destino <= 2:
                    return (origem, destino)
            return None
        
        elif self.gene == '110':  # Invasor moderado
            for origem, destino in jogadas_possiveis:
                tropas_origem = game_state.territorios[origem]['tropas']
                tropas_destino = game_state.territorios[destino]['tropas']
                if tropas_origem > tropas_destino:
                    return (origem, destino)
            return None
        
        elif self.gene == '111':  # Caçador de bônus
            # Prioriza ataques que podem completar continentes
            ataques_continente = self._encontrar_ataques_continente(game_state, jogadas_possiveis)
            if ataques_continente:
                return ataques_continente[0]
            # Se não há ataques para continentes, ataca qualquer um
            return jogadas_possiveis[0] if jogadas_possiveis else None
        
        else:
            return None
    
    def _encontrar_ataques_continente(self, game_state, jogadas_possiveis):
        """Encontra ataques que podem ajudar a completar continentes."""
        from src.config import CONTINENTES
        
        ataques_continente = []
        meus_territorios = game_state.get_territorios_jogador(self.id)
        
        for nome_continente, territorios_continente in CONTINENTES.items():
            # Verifica quantos territórios do continente já possui
            meus_no_continente = [t for t in territorios_continente if t in meus_territorios]
            
            # Se possui a maioria dos territórios do continente
            if len(meus_no_continente) >= len(territorios_continente) * 0.6:
                for origem, destino in jogadas_possiveis:
                    if destino in territorios_continente:
                        ataques_continente.append((origem, destino))
        
        return ataques_continente
    
    def calcular_fitness(self):
        """Calcula o fitness do bot baseado em suas performances."""
        if self.partidas_jogadas == 0:
            self.fitness = 0.0
            return self.fitness
        
        # Fitness baseado em vitórias e territórios conquistados
        taxa_vitoria = self.vitorias / self.partidas_jogadas
        media_territorios = self.territorios_conquistados / self.partidas_jogadas
        
        # Peso maior para vitórias, mas territórios também contam
        self.fitness = (taxa_vitoria * 100) + (media_territorios * 2)
        
        return self.fitness
    
    def reset_stats(self):
        """Reseta as estatísticas do bot para uma nova avaliação."""
        self.vitorias = 0
        self.territorios_conquistados = 0
        self.partidas_jogadas = 0
        self.fitness = 0.0
    
    def __str__(self):
        return f"Bot {self.id} ({self.gene} - {self.estrategia})"
    
    def __repr__(self):
        return f"WarBot(id={self.id}, gene='{self.gene}', fitness={self.fitness:.2f})"

