# -*- coding: utf-8 -*-
"""
Script de demonstração rápida do back-end do jogo WAR.
"""

from src.genetic_algorithm import GeneticAlgorithm
from src.bot import WarBot
from src.config import ESTRATEGIAS
import time


def demo_partida_individual():
    """Demonstra uma partida individual entre bots."""
    print("=" * 60)
    print("DEMONSTRAÇÃO: PARTIDA INDIVIDUAL")
    print("=" * 60)
    
    # Criar bots com diferentes estratégias
    bots = [
        WarBot(0, '000'),  # Pacifista absoluto
        WarBot(1, '101'),  # Oportunista  
        WarBot(2, '110'),  # Invasor moderado
        WarBot(3, '111'),  # Caçador de bônus
        WarBot(4, '100'),  # Expansão segura
        WarBot(5, '010'),  # Fortaleza
    ]
    
    print("Bots participantes:")
    for bot in bots:
        print(f"  Bot {bot.id}: {bot.estrategia} ({bot.gene})")
    
    print("\nSimulando partida...")
    start = time.time()
    
    ag = GeneticAlgorithm()
    resultado = ag._simular_partida(bots)
    
    end = time.time()
    
    print(f"\nResultado da partida:")
    print(f"  Duração: {end-start:.3f} segundos")
    print(f"  Rodadas jogadas: {resultado['rodadas']}")
    print(f"  Vencedor: Bot {resultado['vencedor']} ({bots[resultado['vencedor']].estrategia})")
    
    print(f"\nTerritórios finais:")
    for bot_id, territorios in resultado['territorios_finais'].items():
        bot = next(b for b in bots if b.id == bot_id)
        print(f"  {bot.estrategia}: {territorios} territórios")
    
    return resultado


def demo_algoritmo_genetico_rapido():
    """Demonstra o algoritmo genético com configurações reduzidas."""
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO: ALGORITMO GENÉTICO (VERSÃO RÁPIDA)")
    print("=" * 60)
    
    # Configurações reduzidas para demonstração
    from . import config
    config_original = {
        'NUM_GERACOES': config.NUM_GERACOES,
        'NUM_INDIVIDUOS': config.NUM_INDIVIDUOS,
        'NUM_PARTIDAS_SIM': config.NUM_PARTIDAS_SIM
    }
    
    # Configurações para demo rápida
    config.NUM_GERACOES = 5
    config.NUM_INDIVIDUOS = 12
    config.NUM_PARTIDAS_SIM = 3
    
    print(f"Configurações da demonstração:")
    print(f"  Gerações: {config.NUM_GERACOES}")
    print(f"  População: {config.NUM_INDIVIDUOS}")
    print(f"  Partidas por avaliação: {config.NUM_PARTIDAS_SIM}")
    
    print(f"\nEstratégias disponíveis:")
    for gene, estrategia in ESTRATEGIAS.items():
        print(f"  {gene}: {estrategia}")
    
    print(f"\nIniciando evolução...")
    start = time.time()
    
    ag = GeneticAlgorithm()
    melhor_bot = ag.evoluir()
    
    end = time.time()
    
    print(f"\nResultados da evolução:")
    print(f"  Tempo total: {end-start:.2f} segundos")
    print(f"  Melhor estratégia: {melhor_bot.gene} - {melhor_bot.estrategia}")
    print(f"  Fitness final: {melhor_bot.fitness:.2f}")
    
    print(f"\nTop 5 estratégias:")
    for i, bot in enumerate(ag.populacao[:5]):
        print(f"  {i+1}. {bot.gene} ({bot.estrategia}) - Fitness: {bot.fitness:.2f}")
    
    # Restaurar configurações originais
    for key, value in config_original.items():
        setattr(config, key, value)
    
    return melhor_bot, ag


def main():
    """Função principal da demonstração."""
    print("DEMONSTRAÇÃO DO BACK-END DO JOGO WAR")
    print("Desenvolvido com base no algoritmo genético fornecido")
    
    # Demonstração 1: Partida individual
    demo_partida_individual()
    
    # Demonstração 2: Algoritmo genético rápido
    melhor_bot, ag = demo_algoritmo_genetico_rapido()
    
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 60)
    print("O back-end está funcionando corretamente!")
    print("Para executar simulações completas, use o arquivo main.py")
    print("Para configurações personalizadas, edite o arquivo config.py")


if __name__ == "__main__":
    main()

