# disaster_response.py

import random
import folium
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict

# --- MÓDULO 1: SIMULAÇÃO DE DADOS ---
def generate_simulated_data(num_tweets=100, num_coordinates=50):
    """
    Gera dados fictícios de tweets e coordenadas de GPS.
    """
    print("Gerando dados simulados...")

    keywords = ["terremoto", "desabamento", "ajuda", "resgate", "salvar", "urgente"]
    
    # Lista de tweets com diferentes sentimentos
    tweet_templates = [
        "{} na nossa área. A situação é urgente, precisamos de ajuda!",
        "Acabei de sentir um forte {}. Muita gente desesperada.",
        "Equipes de {} estão no local. Agradecemos o trabalho duro.",
        "Depois do {}, estamos nos recuperando lentamente.",
        "Graças a Deus a equipe de {} chegou. Estão conseguindo {} vidas.",
        "Estou seguro, mas muitos precisam de ajuda com o {}."
    ]

    tweets = [random.choice(tweet_templates).format(random.choice(keywords)) for _ in range(num_tweets)]
    
    # Coordenadas em torno de uma área central (ex: Cidade do México)
    central_lat, central_lon = 19.4326, -99.1332
    coordinates = [(central_lat + random.uniform(-0.1, 0.1), central_lon + random.uniform(-0.1, 0.1)) for _ in range(num_coordinates)]

    print(f"{num_tweets} tweets e {num_coordinates} coordenadas geradas.")
    return tweets, coordinates

# --- MÓDULO 2: ANÁLISE DE SENTIMENTO ---
def analyze_sentiment(tweets):
    """
    Analisa o sentimento de cada tweet para determinar a urgência.
    """
    print("\nAnalisando o sentimento dos tweets...")
    sid = SentimentIntensityAnalyzer()
    sentiment_results = []
    
    for tweet in tweets:
        score = sid.polarity_scores(tweet)
        
        # Classifica com base no score
        if score['compound'] >= 0.05:
            sentiment = "Positivo"
            urgency = "Baixa"
        elif score['compound'] <= -0.05:
            sentiment = "Negativo"
            urgency = "Alta"
        else:
            sentiment = "Neutro"
            urgency = "Média"
            
        sentiment_results.append({
            'tweet': tweet,
            'sentiment': sentiment,
            'urgency': urgency
        })
    
    print("Análise de sentimento concluída.")
    return sentiment_results

# --- MÓDULO 3: MÓDULO DE MAPEAMENTO ---
def create_interactive_map(coordinates, sentiment_results):
    """
    Cria um mapa HTML interativo com marcadores coloridos para representar a urgência.
    """
    print("\nCriando mapa interativo...")
    
    # Ponto central do mapa
    central_lat, central_lon = 19.4326, -99.1332
    m = folium.Map(location=[central_lat, central_lon], zoom_start=13)
    
    # Agrupa as coordenadas por tipo de urgência para facilitar a visualização
    urgency_groups = defaultdict(list)
    for coord, result in zip(coordinates, sentiment_results):
        urgency_groups[result['urgency']].append(coord)
    
    # Adiciona marcadores coloridos ao mapa
    colors = {"Alta": "red", "Média": "orange", "Baixa": "green"}
    
    for urgency, coords_list in urgency_groups.items():
        for coord in coords_list:
            folium.CircleMarker(
                location=coord,
                radius=5,
                color=colors[urgency],
                fill=True,
                fill_color=colors[urgency],
                fill_opacity=0.7,
                tooltip=f"Urgência: {urgency}"
            ).add_to(m)

    map_filename = "disaster_map.html"
    m.save(map_filename)
    print(f"Mapa salvo como '{map_filename}'")
    return map_filename

# --- MÓDULO 4: MÓDULO DE ALERTA E RELATÓRIO ---
def generate_report(sentiment_results, map_filename):
    """
    Gera um relatório resumido com base nos dados analisados.
    """
    print("\nGerando relatório de alerta...")
    
    high_urgency_count = sum(1 for r in sentiment_results if r['urgency'] == "Alta")
    
    report = f"""
    *** Relatório de Resposta a Desastres ***
    
    - Análise de Sentimento:
        - Total de mensagens de alta urgência: {high_urgency_count}
        - Mensagens de alta urgência:
    """
    
    # Adiciona os 5 primeiros tweets de alta urgência
    high_urgency_tweets = [r['tweet'] for r in sentiment_results if r['urgency'] == "Alta"]
    for tweet in high_urgency_tweets[:5]:
        report += f"\t- '{tweet}'\n"
        
    report += f"""
    
    - Mapeamento:
        - Um mapa interativo foi criado e salvo como '{map_filename}'.
        - Ele mostra a localização dos incidentes com marcadores coloridos:
          - Vermelho: Alta Urgência
          - Laranja: Média Urgência
          - Verde: Baixa Urgência
          
    - Ação Recomendada:
        - Focar equipes de resgate nas áreas com marcadores vermelhos no mapa.
    """
    
    print(report)

# --- FLUXO PRINCIPAL DO SCRIPT ---
if __name__ == "__main__":
    tweets, coordinates = generate_simulated_data()
    sentiment_results = analyze_sentiment(tweets)
    map_filename = create_interactive_map(coordinates, sentiment_results)
    generate_report(sentiment_results, map_filename)
