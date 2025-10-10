# -*- coding: utf-8 -*-
"""
Módulo do algoritmo genético para evolução das estratégias dos bots.
"""

import random
import time
from src.bot import WarBot
from src.game import GameState, GameLogic
from src.config import (
    ESTRATEGIAS, NUM_INDIVIDUOS, NUM_GERACOES, TAXA_MUTACAO_INICIAL, 
    TAXA_CROSSOVER_INICIAL, ELITE, NUM_PARTIDAS_SIM, NUM_JOGADORES, MAX_RODADAS
)


class GeneticAlgorithm:
    """Implementa o algoritmo genético para evolução das estratégias dos bots."""
    
    def __init__(self):
        self.populacao = []
        self.geracao_atual = 0
        self.melhor_fitness_por_geracao = []
        self.fitness_medio_por_geracao = []
        self.historico_estrategias = []
    
    def gerar_populacao_inicial(self):
        """Gera a população inicial de bots com genes aleatórios."""
        self.populacao = []
        
        for i in range(NUM_INDIVIDUOS):
            # Gera um gene aleatório de 3 bits
            gene = ''.join(random.choice(['0', '1']) for _ in range(3))
            bot = WarBot(i, gene)
            self.populacao.append(bot)
        
        print(f"População inicial gerada com {NUM_INDIVIDUOS} indivíduos")
        return self.populacao
    
    def avaliar_populacao(self):
        """Avalia a performance de cada bot na população."""
        print(f"Avaliando população da geração {self.geracao_atual}...")
        
        # Reset das estatísticas de todos os bots
        for bot in self.populacao:
            bot.reset_stats()
        
        # Simular partidas para avaliar cada bot
        for partida in range(NUM_PARTIDAS_SIM):
            if partida % 5 == 0:
                print(f"  Simulando partida {partida + 1}/{NUM_PARTIDAS_SIM}")
            
            # Selecionar 6 bots aleatórios para a partida
            bots_partida = random.sample(self.populacao, NUM_JOGADORES)
            resultado = self._simular_partida(bots_partida)
            
            # Atualizar estatísticas dos bots
            for bot in bots_partida:
                bot.partidas_jogadas += 1
                if resultado['vencedor'] == bot.id:
                    bot.vitorias += 1
                bot.territorios_conquistados += resultado['territorios_finais'][bot.id]
        
        # Calcular fitness de cada bot
        for bot in self.populacao:
            bot.calcular_fitness()
        
        # Ordenar população por fitness (decrescente)
        self.populacao.sort(key=lambda b: b.fitness, reverse=True)
        
        # Registrar estatísticas da geração
        melhor_fitness = self.populacao[0].fitness
        fitness_medio = sum(bot.fitness for bot in self.populacao) / len(self.populacao)
        
        self.melhor_fitness_por_geracao.append(melhor_fitness)
        self.fitness_medio_por_geracao.append(fitness_medio)
        
        print(f"  Melhor fitness: {melhor_fitness:.2f}")
        print(f"  Fitness médio: {fitness_medio:.2f}")
        print(f"  Melhor estratégia: {self.populacao[0].estrategia}")
    
    def _simular_partida(self, bots):
        """Simula uma partida completa entre os bots fornecidos."""
        # Inicializar estado do jogo
        game_state = GameState()
        game_state.inicializar_tabuleiro(bots)
        
        rodada = 0
        bots_ativos = bots.copy()
        
        while rodada < MAX_RODADAS and len(bots_ativos) > 1:
            # Reset do histórico de perdas no início de cada rodada
            for bot in bots_ativos:
                game_state.historico_perdas[bot.id] = False
            
            for bot in bots_ativos.copy():
                if GameLogic.jogador_eliminado(game_state, bot.id):
                    bots_ativos.remove(bot)
                    continue
                
                # Fase 1: Receber tropas
                tropas_recebidas = GameLogic.calcular_unidades_recebidas(game_state, bot.id)
                GameLogic.distribuir_tropas(game_state, bot.id, tropas_recebidas)
                
                # Fase 2: Atacar
                max_ataques = 10  # Limite de ataques por turno
                ataques_realizados = 0
                
                while ataques_realizados < max_ataques:
                    jogadas = GameLogic.jogadas_possiveis(game_state, bot.id)
                    ataque = bot.escolher_ataque(game_state, jogadas)
                    
                    if ataque is None:
                        break
                    
                    origem, destino = ataque
                    sucesso = GameLogic.executar_ataque(game_state, origem, destino)
                    ataques_realizados += 1
                    
                    if not sucesso:
                        break  # Se o ataque falhou, para de atacar
                
                # Fase 3: Redistribuir tropas
                GameLogic.redistribuir_tropas(game_state, bot.id)
                
                # Verificar se há vencedor
                vencedor = GameLogic.verificar_vencedor(game_state)
                if vencedor:
                    break
            
            rodada += 1
            
            # Verificar se há vencedor
            vencedor = GameLogic.verificar_vencedor(game_state)
            if vencedor:
                break
        
        # Determinar resultado da partida
        if len(bots_ativos) == 1:
            vencedor_id = bots_ativos[0].id
        elif len(bots_ativos) > 1:
            # Se não há vencedor claro, escolhe quem tem mais territórios
            territorios_por_bot = {}
            for bot in bots_ativos:
                territorios_por_bot[bot.id] = len(game_state.get_territorios_jogador(bot.id))
            vencedor_id = max(territorios_por_bot, key=territorios_por_bot.get)
        else:
            # Caso extremo - escolhe um bot aleatório
            vencedor_id = random.choice(bots).id
        
        # Contar territórios finais de cada bot
        territorios_finais = {}
        for bot in bots:
            territorios_finais[bot.id] = len(game_state.get_territorios_jogador(bot.id))
        
        return {
            'vencedor': vencedor_id,
            'territorios_finais': territorios_finais,
            'rodadas': rodada
        }
    
    def selecionar_pais(self):
        """Seleciona os melhores bots para reprodução."""
        # Elitismo: preserva os melhores
        elite_bots = self.populacao[:ELITE]
        
        # Seleção por roleta para o restante
        fitness_total = sum(bot.fitness for bot in self.populacao)
        
        pais_selecionados = elite_bots.copy()
        
        while len(pais_selecionados) < NUM_INDIVIDUOS // 2:
            # Seleção por roleta
            valor_roleta = random.uniform(0, fitness_total)
            soma_fitness = 0
            
            for bot in self.populacao:
                soma_fitness += bot.fitness
                if soma_fitness >= valor_roleta:
                    if bot not in pais_selecionados:
                        pais_selecionados.append(bot)
                    break
        
        return pais_selecionados
    
    def crossover(self, pai1, pai2):
        """Realiza crossover entre dois pais para gerar dois filhos."""
        if random.random() > self._taxa_crossover_atual():
            # Sem crossover, retorna cópias dos pais
            return pai1.gene, pai2.gene
        
        # Crossover de ponto único
        ponto_corte = random.randint(1, 2)  # Para genes de 3 bits
        
        filho1 = pai1.gene[:ponto_corte] + pai2.gene[ponto_corte:]
        filho2 = pai2.gene[:ponto_corte] + pai1.gene[ponto_corte:]
        
        return filho1, filho2
    
    def mutacao(self, gene):
        """Aplica mutação em um gene."""
        if random.random() > self._taxa_mutacao_atual():
            return gene
        
        # Mutação de bit flip
        posicao = random.randint(0, 2)  # Para genes de 3 bits
        gene_lista = list(gene)
        gene_lista[posicao] = '1' if gene_lista[posicao] == '0' else '0'
        
        return ''.join(gene_lista)
    
    def _taxa_mutacao_atual(self):
        """Calcula a taxa de mutação atual (decai com as gerações)."""
        from src.config import NUM_GERACOES
        decaimento = self.geracao_atual / NUM_GERACOES
        return TAXA_MUTACAO_INICIAL * (1 - decaimento * 0.5)
    
    def _taxa_crossover_atual(self):
        """Calcula a taxa de crossover atual (decai com as gerações)."""
        from src.config import NUM_GERACOES
        decaimento = self.geracao_atual / NUM_GERACOES
        return TAXA_CROSSOVER_INICIAL * (1 - decaimento * 0.3)
    
    def gerar_nova_geracao(self):
        """Gera uma nova geração através de seleção, crossover e mutação."""
        pais = self.selecionar_pais()
        nova_populacao = []
        
        # Preservar elite
        for i in range(ELITE):
            elite_bot = WarBot(len(nova_populacao), self.populacao[i].gene)
            nova_populacao.append(elite_bot)
        
        # Gerar novos indivíduos
        while len(nova_populacao) < NUM_INDIVIDUOS:
            pai1, pai2 = random.sample(pais, 2)
            filho1_gene, filho2_gene = self.crossover(pai1, pai2)
            
            # Aplicar mutação
            filho1_gene = self.mutacao(filho1_gene)
            filho2_gene = self.mutacao(filho2_gene)
            
            # Criar novos bots
            if len(nova_populacao) < NUM_INDIVIDUOS:
                bot1 = WarBot(len(nova_populacao), filho1_gene)
                nova_populacao.append(bot1)
            
            if len(nova_populacao) < NUM_INDIVIDUOS:
                bot2 = WarBot(len(nova_populacao), filho2_gene)
                nova_populacao.append(bot2)
        
        self.populacao = nova_populacao
    
    def evoluir(self):
        """Executa o processo completo de evolução do algoritmo genético."""
        # Usar as configurações atuais do módulo config
        from src.config import NUM_GERACOES, NUM_INDIVIDUOS, NUM_PARTIDAS_SIM
        
        print(f"Iniciando evolução por {NUM_GERACOES} gerações...")
        print(f"População: {NUM_INDIVIDUOS}, Partidas por avaliação: {NUM_PARTIDAS_SIM}")
        print("-" * 60)
        
        # Gerar população inicial
        self.gerar_populacao_inicial()
        
        for geracao in range(NUM_GERACOES):
            self.geracao_atual = geracao
            print(f"\n=== GERAÇÃO {geracao + 1}/{NUM_GERACOES} ===")
            
            # Avaliar população atual
            self.avaliar_populacao()
            
            # Registrar estratégias da geração
            estrategias_geracao = {}
            for bot in self.populacao:
                if bot.gene not in estrategias_geracao:
                    estrategias_geracao[bot.gene] = 0
                estrategias_geracao[bot.gene] += 1
            
            self.historico_estrategias.append(estrategias_geracao)
            
            # Gerar próxima geração (exceto na última)
            if geracao < NUM_GERACOES - 1:
                self.gerar_nova_geracao()
        
        print("\n" + "=" * 60)
        print("EVOLUÇÃO CONCLUÍDA!")
        print(f"Melhor bot: {self.populacao[0]}")
        print(f"Fitness final: {self.populacao[0].fitness:.2f}")
        
        return self.populacao[0]
    
    def get_estatisticas(self):
        """Retorna estatísticas da evolução."""
        return {
            'melhor_fitness_por_geracao': self.melhor_fitness_por_geracao,
            'fitness_medio_por_geracao': self.fitness_medio_por_geracao,
            'historico_estrategias': self.historico_estrategias,
            'melhor_bot': self.populacao[0] if self.populacao else None
        }

