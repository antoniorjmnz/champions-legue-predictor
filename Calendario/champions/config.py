# config.py
"""Parámetros del sorteo y lista de equipos de la temporada 2025-2026."""

# Número de rivales por equipo
N_MATCHES = 8

# Número obligatorio de rivales por bombo
PER_POT = 2

# Límite máximo de rivales del mismo país
MAX_SAME_COUNTRY = {
    "default": 1,  # por defecto, máximo 1 rival del mismo país
    "ENG": 2,  # Inglaterra puede tener hasta 2 rivales ingleses
}

# Lista de los 36 equipos de la fase liga 2025-2026
ALL_TEAMS_2026 = [
    "Real Madrid",
    "Pafos",
    "PSV",
    "Qarabag",
    "Atlético de Madrid",
    "Tottenham",
    "Marseille",
    "Juventus",
    "Union Saint-Gilloise",
    "Galatasaray",
    "Newcastle",
    "Bayer Leverkusen",
    "Arsenal",
    "Slavia Praha",
    "Olympiacos",
    "Athletic Club",
    "Villarreal",
    "Paris Saint-Germain",
    "Napoli",
    "Inter",
    "Bayern München",
    "Manchester City",
    "Benfica",
    "Eintracht Frankfurt",
    "Atalanta",
    "Borussia Dortmund",
    "Sporting CP",
    "Chelsea",
    "Club Brugge",
    "Bodo/Glimt",
    "Kairat Almaty",
    "Monaco",
    "Liverpool",
    "Ajax",
    "Barcelona",
    "Copenhagen",
]
