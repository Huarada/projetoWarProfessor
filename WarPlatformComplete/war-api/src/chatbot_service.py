import openai
import os

MINHACHAVEAPI = os.environ.get("OPENAI_API_KEY")
# IMPORTANTE: Configure sua chave da API OpenAI aqui
# Você pode definir a variável de ambiente OPENAI_API_KEY ou inserir diretamente abaixo
openai.api_key = MINHACHAVEAPI  # INSIRA SUA CHAVE AQUI SE NÃO USAR VARIÁVEL DE AMBIENTE


def analyze_move_with_gpt(game_state, last_action):
    """
    Analisa uma jogada usando GPT-4 com base na Teoria dos Jogos.
    
    Args:
        game_state: Estado atual do jogo (dicionário com territórios e jogadores)
        last_action: Última ação realizada (dicionário com detalhes do ataque)
    
    Returns:
        str: Análise da jogada baseada em Teoria dos Jogos
    """
    if not openai.api_key:
        return "Erro: Chave da API OpenAI não configurada. Configure a variável OPENAI_API_KEY ou insira diretamente no código."
    
    # Extrair informações relevantes do estado do jogo
    table_configuration = {}
    
    # Organizar territórios por jogador
    for territory, info in game_state.get('territories', {}).items():
        player_id = info.get('dono')
        if player_id is not None:
            player_name = f"Jogador {player_id}"
            if player_name not in table_configuration:
                table_configuration[player_name] = []
            table_configuration[player_name].append(territory)
    
    # Formatar informações do ataque
    attack_info = {}
    if last_action and last_action.get('type') == 'attack':
        player_id = last_action.get('player', 0)
        attack_info = {
            "jogador_que_atacou": f"Jogador {player_id}",
            "origem": last_action.get("from", "Origem desconhecida"),
            "destino": last_action.get("to", "Destino desconhecido"),
            "sucesso": "Sim" if last_action.get("success", False) else "Não"
        }

        attack_success = last_action.get('success', False)
        attack_info['sucesso'] = attack_success
    else:
        attack_info = {"Nenhum ataque realizado": "Jogador não atacou neste turno"}

    prompt = prompt = f"""
Você é um especialista em Teoria dos Jogos e Inteligência Artificial, com profundo conhecimento em jogos de estratégia como WAR. 
Sua função é analisar criticamente o estado de um tabuleiro de WAR fornecido pelo usuário e explicar, com base na Teoria dos Jogos, 
o raciocínio estratégico por trás de uma jogada específica que foi realizada.

O jogo WAR é um jogo de estratégia onde os jogadores competem por territórios e continentes, utilizando tropas para atacar e defender. 
As decisões tomadas pelos jogadores são influenciadas por fatores como alianças, controle de territórios e a dinâmica de poder entre os jogadores.

O objetivo é adquirir o máximo de territórios possíveis, focando em dominar continentes e eliminar os adversários.

Utilize conceitos como:  
- Equilíbrio de Nash  
- Estratégias dominantes e dominadas  
- Payoff esperado  
- Risco versus recompensa  
- Ameaças e alianças implícitas  
- Controle de territórios críticos e fronteiras vulneráveis  

Ao explicar os conceitos, use uma linguagem simples e educativa, como se estivesse ensinando alunos do ensino médio. 
Sempre que mencionar um termo técnico, explique-o de forma intuitiva e com exemplos cotidianos.

Instruções:  
Analise a jogada descrita abaixo com base no estado atual do tabuleiro. 
Explique por que essa jogada pode ter sido feita, qual era o objetivo estratégico dela, e se foi uma decisão racional ou subótima, com base nos princípios da Teoria dos Jogos. 
A explicação deve ter tom de professor e incentivar o aluno a refletir sobre o raciocínio por trás da jogada.

Se possível, compare com alternativas que o jogador poderia ter feito e analise os possíveis desdobramentos estratégicos dessa ação.  
Mostre como diferentes decisões poderiam levar a resultados distintos.

Sua resposta deve ser clara, educativa e acessível, evitando jargões técnicos e linguagem excessivamente matemática. 
Use analogias simples quando possível (por exemplo, comparar defender um território a “fortalecer uma região antes de atacar”). 
Não use mais de 300 palavras.

Finalize sua análise com uma breve conclusão profissional e estratégica, resumindo o que poderia ser otimizado na jogada. 
Evite perguntas diretas ao jogador. Use um tom analítico e objetivo, semelhante ao de um relatório tático.


Atenção:
- Use apenas as informações da seção "Jogada analisada" para identificar quem executou a jogada.
- O campo "jogador_que_atacou" representa o jogador que realizou a ação. 
- O campo "current_player" no estado do jogo refere-se ao próximo jogador e não deve ser usado.

Configuração atual do tabuleiro:
{table_configuration}

Jogada analisada:
{attack_info}
"""


    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # modelo mais estável e eficiente
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o General WAR, um estrategista divertido e didático. "
                        "Sempre conclua seu raciocínio antes de encerrar a resposta, "
                        "mantendo coerência e completude. "
                        "Evite deixar frases inacabadas, mesmo que precise encurtar o texto."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=900,        #  aumenta o espaço para respostas longas
            temperature=0.7,
            presence_penalty=0.1,  #  evita repetições
            frequency_penalty=0.2  #  melhora fluidez e evita redundâncias
        )

        # Se o modelo parar abruptamente, tenta extrair o texto bruto completo
        reply = response.choices[0].message.content.strip()

        # Correção extra: se a última frase terminar sem pontuação, adicione reticências
        if reply and reply[-1] not in ".!?":
            reply += "..."

        return reply

    except Exception as e:
        return f"Erro ao analisar jogada: {str(e)}. Verifique se a chave da API OpenAI está configurada corretamente."

