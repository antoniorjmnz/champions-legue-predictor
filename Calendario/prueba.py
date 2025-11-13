import random
from metaheuristica_rivales import generar_rivales_metaheuristica
from collections import Counter

def generar_bombos(lista_equipos, num_bombos=4):
    bombos = [[] for _ in range(num_bombos)]
    equipos_disponibles = lista_equipos.copy()
    random.shuffle(equipos_disponibles)
    idx = 0
    while equipos_disponibles:
        equipo = equipos_disponibles.pop()
        bombos[idx % num_bombos].append(equipo)
        idx += 1
    return bombos

def imprimir_rivales(rivales, equipos_dict):
    print("\n===== RIVALES POR EQUIPO =====\n")
    for eq in sorted(rivales.keys()):
        pais = equipos_dict[eq]['country']
        rivales_list = sorted(list(rivales[eq]))
        paises = Counter([equipos_dict[r]['country'] for r in rivales[eq]])
        paises_str = ', '.join([f"{k}x{v}" for k, v in paises.items()])
        print(f"{eq} ({pais}) | Total rivales: {len(rivales_list)} -> [{paises_str}] -> {', '.join(rivales_list)}")
    print("\n=============================\n")

def generar_rivales(equipos_dict, max_iter=10000):
    lista_equipos = list(equipos_dict.keys())
    bombos = generar_bombos(lista_equipos, num_bombos=4)

    print("Bombos generados:")
    for i, bombo in enumerate(bombos):
        print(f"Bombo {i+1}: {bombo}")

    print("\nGenerando rivales...")
    rivales = generar_rivales_metaheuristica(
    lista_equipos,
    equipos_dict,
    bombos,
    iteraciones=5000,
    max_mismo_pais=1 
    )


    if rivales:
        print("Rivales generados correctamente.")
        imprimir_rivales(rivales, equipos_dict)
    else:
        print("No se pudo generar rivales válidos.")

    return rivales

if __name__ == "__main__":
    # Equipos y países
    TEAMS_EXAMPLE = [
        "Liverpool", "Arsenal", "Manchester City", "Chelsea", "Tottenham", "Newcastle",
        "Barcelona", "Real Madrid", "Atlético de Madrid", "Athletic Club", "Villarreal",
        "Napoli", "Inter", "Atalanta", "Juventus",
        "Bayern München", "Bayer Leverkusen", "Eintracht Frankfurt", "Borussia Dortmund",
        "Paris Saint-Germain", "Marseille", "Monaco",
        "PSV", "Ajax",
        "Benfica", "Sporting CP",
        "Club Brugge", "Union Saint-Gilloise",
        "Galatasaray", "Slavia Praha", "Olympiacos", "Copenhagen",
        "Bodo/Glimt", "Pafos", "Kairat Almaty", "Qarabag"
    ]

    COUNTRY_OF_EXAMPLE = {
        "Liverpool": "ENG", "Arsenal": "ENG", "Manchester City": "ENG",
        "Chelsea": "ENG", "Tottenham": "ENG", "Newcastle": "ENG",
        "Barcelona": "ESP", "Real Madrid": "ESP", "Atlético de Madrid": "ESP",
        "Athletic Club": "ESP", "Villarreal": "ESP",
        "Napoli": "ITA", "Inter": "ITA", "Atalanta": "ITA", "Juventus": "ITA",
        "Bayern München": "GER", "Bayer Leverkusen": "GER",
        "Eintracht Frankfurt": "GER", "Borussia Dortmund": "GER",
        "Paris Saint-Germain": "FRA", "Marseille": "FRA", "Monaco": "FRA",
        "PSV": "NED", "Ajax": "NED",
        "Benfica": "POR", "Sporting CP": "POR",
        "Club Brugge": "BEL", "Union Saint-Gilloise": "BEL",
        "Galatasaray": "TUR",
        "Slavia Praha": "CZE",
        "Olympiacos": "GRE",
        "Copenhagen": "DEN",
        "Bodo/Glimt": "NOR",
        "Pafos": "CYP",
        "Kairat Almaty": "KAZ",
        "Qarabag": "AZE"
    }

    TEAMS_DICT = {team: {"country": COUNTRY_OF_EXAMPLE[team]} for team in TEAMS_EXAMPLE}

    generar_rivales(TEAMS_DICT)
