"""Estado global del sorteo: adyacencias, grados y contadores auxiliares."""

from collections import defaultdict
from data import load_teams
from config import N_MATCHES, PER_POT

# Cargar equipos (con bombos ya aleatorios)
teams = load_teams()
n = len(teams)

# Lista de rivales de cada equipo
adj = [set() for _ in range(n)]

# Grado (número de rivales)
deg = [0] * n

# pot_count[i][p] = rivales del bombo p
pot_count = [[0] * 5 for _ in range(n)]  # índice 0 no usado

# country_count[i][country] = nº de rivales de ese país (sea propio o extranjero)
country_count = [defaultdict(int) for _ in range(n)]

# Número total de emparejamientos
E = n * N_MATCHES // 2


def add_edge(i: int, j: int) -> None:
    """Añade un emparejamiento (i, j)."""
    adj[i].add(j)
    adj[j].add(i)

    deg[i] += 1
    deg[j] += 1

    pi, pj = teams[i].pot, teams[j].pot
    pot_count[i][pj] += 1
    pot_count[j][pi] += 1

    # Contamos SIEMPRE el país del rival
    ci, cj = teams[i].country, teams[j].country
    country_count[i][cj] += 1
    country_count[j][ci] += 1


def remove_edge(i: int, j: int) -> None:
    """Elimina el emparejamiento (i, j)."""
    if j in adj[i]:
        adj[i].remove(j)
    if i in adj[j]:
        adj[j].remove(i)

    deg[i] -= 1
    deg[j] -= 1

    pi, pj = teams[i].pot, teams[j].pot
    pot_count[i][pj] -= 1
    pot_count[j][pi] -= 1

    ci, cj = teams[i].country, teams[j].country
    country_count[i][cj] -= 1
    country_count[j][ci] -= 1
