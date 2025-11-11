import random

def generar_calendario(equipos_dict):
    
    # 4 bombos vacíos de lista de listas
    lista_bombo = [[] for _ in range(4)]
    # Lista de los nombres de los equipos
    lista_equipos = list(equipos_dict.keys())
    exito =  False

    while(not exito):
        
        exito =  generar_bombos(lista_bombo, lista_equipos, equipos_dict)
        
        if exito:
            print("Bombos generados con éxito:")    
            for i, bombo in enumerate(lista_bombo):
                print(f"Bombo {i+1}: {bombo}")
        else:
            print("No se pudo generar una distribución válida de bombos.")
            
            for i, bombo in enumerate(lista_bombo):
                print(f"Bombo {i+1}: {bombo}")
            
            for bombo in lista_bombo:
                bombo.clear()
            lista_equipos = list(equipos_dict.keys())    
            print("Rehaciendo bombos...\n")

    x = generar_partidos(lista_bombo, equipos_dict)



def generar_partidos(lb, equipos_dict, rivales_por_bombo=2):
    partidos = []

    for i, bombo_actual in enumerate(lb):
        otros_bombos = [lb[j] for j in range(len(lb)) if j != i]

        for equipo in bombo_actual:
            pais_equipo = equipos_dict[equipo]['country']

            for bombo_rival in otros_bombos:
                # Filtramos rivales válidos (no mismo país)
                rivales_validos = [r for r in bombo_rival if equipos_dict[r]['country'] != pais_equipo]

                if len(rivales_validos) < rivales_por_bombo:
                    raise ValueError(f"No hay suficientes rivales válidos para {equipo} en bombo {i+1}")

                rivales = random.sample(rivales_validos, rivales_por_bombo)

                for rival in rivales:
                    partidos.append({"local": equipo, "visitante": rival})
                    partidos.append({"local": rival, "visitante": equipo})

    print("\n--- CALENDARIO DE PARTIDOS ---\n")
    for partido in partidos:
        print(f"{partido['local']:<20} vs {partido['visitante']:<20}")
    print(f"\nNúmero total de partidos generados: {len(partidos)}\n")    
    print(partidos)
    return partidos






def generar_bombos(lb, lista_equipos, equipos_dict):
    
    for i in range(4):
        intentos = 0
        print(lb[i])

        while len(lb[i]) < 9 and lista_equipos:
            
            random.shuffle(lista_equipos)
            equipo = random.choice(lista_equipos)
            pais_equipo = equipos_dict[equipo]['country']
            paises_en_bombo = [equipos_dict[eq]['country'] for eq in lb[i]]
            
            print(f"Intentando añadir {equipo} al bombo {i+1}")
            print(f"Equipos en bombo {i+1} actualmente: {lb[i]}")
            
            # Aquí se comprueba que no hay más de dos equipos de un país en el bombo
            conteo_pais = paises_en_bombo.count(pais_equipo)
            print(intentos)
            if equipo not in lb[i] and conteo_pais < 2:
                lb[i].append(equipo)
                lista_equipos.remove(equipo)
            else:
                intentos += 1

            if intentos > 10:
                break
            
        if len(lb[i]) < 9:
            print(f"Reiniciando sorteo debido a demasiados intentos.")
            return False

    return True
    
    print(lb)


if __name__ == "__main__":
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

    bombos = generar_calendario(TEAMS_DICT)
