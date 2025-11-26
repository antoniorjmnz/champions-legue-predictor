"""Parámetros del sorteo y lista de equipos de la temporada 2025-2026."""

# Número de rivales por equipo
N_MATCHES = 8

# Número obligatorio de rivales por bombo
PER_POT = 2

# Límite máximo de rivales del mismo país (MISMOS país → en la práctica 0)
# En la Champions real no se enfrentan equipos del mismo país en la fase liga,
# así que lo ponemos a 0 para todos.
MAX_SAME_COUNTRY = {
    "default": 0,  # ningún rival del mismo país
    "ENG": 0,      # Inglaterra tampoco puede enfrentarse entre sí
}

# Límite de rivales de un mismo país DISTINTO al propio
# (por ejemplo, Barça contra equipos italianos).
# Pedro te ha dicho que aquí se puede ser laxo y permitir hasta 3.
MAX_RIVALS_PER_COUNTRY = 3

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
