# state.py
"""Estado global del sorteo: adyacencias, grados y contadores auxiliares."""

from collections import defaultdict
from data import load_teams
from config import N_MATCHES, PER_POT

# Cargar equipos (con bombos ya aleatorios)
teams = load_teams()
n = len(teams)

# Lista de rivales de cada equipo (grafo no dirigido)
adj = [set() for _ in range(n)]

# Grado (número de rivales) de cada equipo
deg = [0] * n

# pot_count[i][p] = cuántos rivales tiene el equipo i del bombo p (1..4)
pot_count = [[0] * 5 for _ in range(n)]  # índice 0 sin usar

# country_count[i][c] = cuántos rivales del país c tiene el equipo i
# (solo contamos rivales del MISMO país para la restricción de MAX_SAME_COUNTRY)
country_count = [defaultdict(int) for _ in range(n)]

# Número total de emparejamientos (cada partido cuenta para 2 equipos)
E = n * N_MATCHES // 2


def add_edge(i: int, j: int) -> None:
    """Añade un emparejamiento (i, j) al estado global."""
    adj[i].add(j)
    adj[j].add(i)

    deg[i] += 1
    deg[j] += 1

    pi, pj = teams[i].pot, teams[j].pot
    pot_count[i][pj] += 1
    pot_count[j][pi] += 1

    ci, cj = teams[i].country, teams[j].country
    if ci == cj:
        # Solo contamos rivales del mismo país
        country_count[i][ci] += 1
        country_count[j][cj] += 1


def remove_edge(i: int, j: int) -> None:
    """Deshace el emparejamiento (i, j)."""
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
    if ci == cj:
        country_count[i][ci] -= 1
        country_count[j][cj] -= 1
