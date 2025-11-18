# data.py
"""Generación de bombos aleatorios + creación de objetos Team."""

import random
from dataclasses import dataclass
from config import ALL_TEAMS_2026


@dataclass
class Team:
    name: str
    country: str
    pot: int
    idx: int


# Mapa de países para cada equipo
country_map = {
    "Real Madrid": "ESP", "Pafos": "CYP", "PSV": "NED", "Qarabag": "AZE",
    "Atlético de Madrid": "ESP", "Tottenham": "ENG", "Marseille": "FRA",
    "Juventus": "ITA", "Union Saint-Gilloise": "BEL",

    "Galatasaray": "TUR", "Newcastle": "ENG", "Bayer Leverkusen": "GER",
    "Arsenal": "ENG", "Slavia Praha": "CZE", "Olympiacos": "GRE",
    "Athletic Club": "ESP", "Villarreal": "ESP", "Paris Saint-Germain": "FRA",

    "Napoli": "ITA", "Inter": "ITA", "Bayern München": "GER",
    "Manchester City": "ENG", "Benfica": "POR", "Eintracht Frankfurt": "GER",
    "Atalanta": "ITA", "Borussia Dortmund": "GER", "Sporting CP": "POR",

    "Chelsea": "ENG", "Club Brugge": "BEL", "Bodo/Glimt": "NOR",
    "Kairat Almaty": "KAZ", "Monaco": "FRA", "Liverpool": "ENG",
    "Ajax": "NED", "Barcelona": "ESP", "Copenhagen": "DEN",
}


def generar_bombos_aleatorios():
    """Devuelve una lista de 4 bombos (listas de 9 equipos) generados aleatoriamente."""
    equipos = ALL_TEAMS_2026.copy()
    random.shuffle(equipos)
    return [
        equipos[0:9],
        equipos[9:18],
        equipos[18:27],
        equipos[27:36],
    ]


def load_teams():
    """Crea la lista de Team a partir de bombos aleatorios."""
    teams = []
    bombos = generar_bombos_aleatorios()
    idx = 0

    for pot_number, bombo in enumerate(bombos, start=1):
        for name in bombo:
            country = country_map.get(name, "UNK")
            teams.append(
                Team(
                    name=name,
                    country=country,
                    pot=pot_number,
                    idx=idx,
                )
            )
            idx += 1

    # Orden determinista dentro del solver (por pot, país, nombre)
    teams.sort(key=lambda t: (t.pot, t.country, t.name))
    return teams
