# -*- coding: utf-8 -*-
"""
Configurações e constantes para o jogo WAR.
"""

import random

# --- Parâmetros do Algoritmo Genético ---
NUM_INDIVIDUOS = 40
NUM_GERACOES = 500
TAXA_MUTACAO_INICIAL = 0.7
NUM_PARTIDAS_SIM = 20  # Partidas jogadas para avaliar cada gene/indivíduo
TAXA_CROSSOVER_INICIAL = 0.7  # recombinação muito alta no início, vai decaindo a cada geração
ELITE = 6  # Número de melhores pais a preservar

# --- Mapeamento de Estratégias ---
ESTRATEGIAS = {
    '000': 'Pacifista absoluto',
    '001': 'Contra-golpe',
    '010': 'Fortaleza',
    '011': 'Retomada',
    '100': 'Expansão segura',
    '101': 'Oportunista',
    '110': 'Invasor moderado',
    '111': 'Caçador de bônus'
}

# --- Configurações do Jogo ---
NUM_JOGADORES = 6
TROPAS_INICIAIS_POR_JOGADOR = 20
MAX_RODADAS = 100

# --- Territórios do Jogo WAR ---
TERRITORIOS = [
    # América do Norte
    "Alasca", "Mackenzie", "Vancouver", "Groenlândia", "Labrador", "Ottawa", 
    "Nova York", "Califórnia", "México",
    
    # América do Sul
    "Venezuela", "Peru", "Brasil", "Argentina",
    
    # Europa
    "Inglaterra", "Islândia", "França", "Polônia", "Alemanha", "Suécia", "Moscou",
    
    # Ásia
    "Vladivostok", "Sibéria", "Tchita", "Dudinka", "Mongólia", "Omsk", "Aral", 
    "Japão", "China", "Vietnã", "Índia", "Oriente Médio",
    
    # África
    "Egito", "Argélia", "Sudão", "Congo", "África do Sul", "Madagascar",
    
    # Oceania
    "Austrália", "Bornéu", "Nova Guiné", "Sumatra"
]

# --- Adjacências entre territórios ---
MAPA_WAR = {
    # América do Norte
    "Alasca": ["Mackenzie", "Vancouver", "Vladivostok"],
    "Mackenzie": ["Alasca", "Vancouver", "Ottawa", "Groenlândia"],
    "Vancouver": ["Alasca", "Mackenzie", "Ottawa", "Califórnia"],
    "Groenlândia": ["Labrador", "Mackenzie", "Islândia"],
    "Labrador": ["Groenlândia", "Ottawa", "Nova York"],
    "Ottawa": ["Mackenzie", "Vancouver", "Califórnia", "Nova York", "Labrador"],
    "Nova York": ["Ottawa", "Califórnia", "México", "Labrador"],
    "Califórnia": ["Vancouver", "Ottawa", "Nova York", "México"],
    "México": ["Califórnia", "Nova York", "Venezuela"],

    # América do Sul
    "Venezuela": ["México", "Brasil", "Peru"],
    "Peru": ["Venezuela", "Brasil", "Argentina"],
    "Brasil": ["Venezuela", "Peru", "Argentina", "Argélia"],
    "Argentina": ["Peru", "Brasil"],

    # Europa
    "Inglaterra": ["Islândia", "França", "Alemanha", "Suécia"],
    "Islândia": ["Groenlândia", "Inglaterra"],
    "França": ["Inglaterra", "Alemanha", "Argélia", "Polônia"],
    "Polônia": ["França", "Alemanha", "Suécia", "Moscou", "Oriente Médio", "Egito"],
    "Alemanha": ["França", "Polônia", "Suécia", "Inglaterra"],
    "Suécia": ["Alemanha", "Polônia", "Moscou", "Inglaterra"],
    "Moscou": ["Suécia", "Polônia", "Omsk", "Aral", "Oriente Médio"],

    # Ásia
    "Vladivostok": ["Alasca", "Sibéria", "Tchita", "China"],
    "Sibéria": ["Vladivostok", "Tchita", "Dudinka"],
    "Tchita": ["Vladivostok", "Sibéria", "Dudinka", "Mongólia", "China"],
    "Dudinka": ["Sibéria", "Tchita", "Mongólia", "Omsk"],
    "Mongólia": ["Tchita", "Dudinka", "Omsk", "China"],
    "Omsk": ["Mongólia", "Dudinka", "Aral", "Moscou"],
    "Aral": ["Omsk", "Moscou", "China", "Índia", "Oriente Médio"],
    "Japão": ["China", "Vladivostok"],
    "China": ["Japão", "Vietnã", "Índia", "Aral", "Mongólia", "Tchita", "Vladivostok", "Omsk"],
    "Vietnã": ["Bornéu", "China", "Índia"],
    "Índia": ["China", "Aral", "Oriente Médio", "Sumatra", "Vietnã"],
    "Oriente Médio": ["Moscou", "Egito", "Índia", "Aral", "Polônia"],

    # África
    "Egito": ["Polônia", "Argélia", "Sudão", "Oriente Médio"],
    "Argélia": ["França", "Egito", "Sudão", "Congo", "Brasil"],
    "Sudão": ["Argélia", "Egito", "Congo", "África do Sul", "Madagascar"],
    "Congo": ["Argélia", "Sudão", "África do Sul"],
    "África do Sul": ["Sudão", "Congo", "Madagascar"],
    "Madagascar": ["África do Sul", "Sudão"],

    # Oceania
    "Austrália": ["Nova Guiné", "Bornéu", "Sumatra"],
    "Bornéu": ["Austrália", "Nova Guiné", "Vietnã"],
    "Nova Guiné": ["Austrália", "Bornéu"],
    "Sumatra": ["Austrália", "Índia"]
}

# --- Continentes e seus territórios ---
CONTINENTES = {
    "América do Norte": [
        "Alasca", "Mackenzie", "Vancouver", "Groenlândia", "Labrador", 
        "Ottawa", "Nova York", "Califórnia", "México"
    ],
    "América do Sul": [
        "Venezuela", "Peru", "Brasil", "Argentina"
    ],
    "Europa": [
        "Inglaterra", "Islândia", "França", "Polônia", "Alemanha", "Suécia", "Moscou"
    ],
    "Ásia": [
        "Vladivostok", "Sibéria", "Tchita", "Dudinka", "Mongólia", "Omsk", 
        "Aral", "Japão", "China", "Vietnã", "Índia", "Oriente Médio"
    ],
    "África": [
        "Egito", "Argélia", "Sudão", "Congo", "África do Sul", "Madagascar"
    ],
    "Oceania": [
        "Austrália", "Bornéu", "Nova Guiné", "Sumatra"
    ]
}

# --- Bônus por continente ---
BONUS_CONTINENTES = {
    "América do Norte": 5,
    "América do Sul": 2,
    "Europa": 5,
    "Ásia": 7,
    "África": 3,
    "Oceania": 2
}

def gerar_gene_aleatorio():
    """Gera um gene aleatório de 3 bits."""
    return ''.join(random.choice('01') for _ in range(3))

def validar_configuracao():
    """Valida se as configurações estão corretas."""
    # Verificar se todos os territórios têm adjacências
    for territorio in TERRITORIOS:
        if territorio not in ADJACENCIAS:
            raise ValueError(f"Território {territorio} não tem adjacências definidas")
    
    # Verificar se as adjacências são simétricas
    for territorio, adjacentes in ADJACENCIAS.items():
        for adjacente in adjacentes:
            if territorio not in ADJACENCIAS.get(adjacente, []):
                print(f"Aviso: Adjacência não simétrica entre {territorio} e {adjacente}")
    
    # Verificar se todos os territórios pertencem a um continente
    territorios_continentes = set()
    for continente, territorios in CONTINENTES.items():
        territorios_continentes.update(territorios)
    
    territorios_faltando = set(TERRITORIOS) - territorios_continentes
    if territorios_faltando:
        raise ValueError(f"Territórios sem continente: {territorios_faltando}")
    
    print("Configuração validada com sucesso!")

# Validar configuração ao importar o módulo
if __name__ == "__main__":
    validar_configuracao()

