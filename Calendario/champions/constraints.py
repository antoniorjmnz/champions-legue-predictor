# constraints.py
"""Comprobación de restricciones para decidir si se puede emparejar i con j."""

from config import N_MATCHES, PER_POT, MAX_RIVALS_PER_COUNTRY
from state import teams, adj, deg, pot_count


def _forbid_same_country(i: int, j: int) -> bool:
    """
    Restricción 1:
    - PROHÍBE que dos equipos del mismo país se enfrenten.
    Ejemplo: Barça vs Real Madrid, USG vs Club Brugge, etc. NO permitidos.
    """
    return teams[i].country != teams[j].country


def _limit_per_country(i: int, j: int) -> bool:
    """
    Restricción 2:
    - Limita cuántos rivales puede tener un equipo de un MISMO país extranjero.
      (p.ej. Barça contra italianos: Inter, Juve y Atalanta → máximo 3).

    Implementación:
    - Contamos, para i, cuántos rivales del país de j tiene ya.
    - Contamos, para j, cuántos rivales del país de i tiene ya.
    - Ambos deben estar por debajo de MAX_RIVALS_PER_COUNTRY.
    """
    ci = teams[i].country
    cj = teams[j].country

    # Si fueran del mismo país, ya lo bloquea _forbid_same_country
    if ci == cj:
        return True

    # Cuenta cuántos rivales del país cj tiene i
    count_i_cj = 0
    for k in adj[i]:
        if teams[k].country == cj:
            count_i_cj += 1

    if count_i_cj >= MAX_RIVALS_PER_COUNTRY:
        return False

    # Cuenta cuántos rivales del país ci tiene j
    count_j_ci = 0
    for k in adj[j]:
        if teams[k].country == ci:
            count_j_ci += 1

    if count_j_ci >= MAX_RIVALS_PER_COUNTRY:
        return False

    return True


def can_add_edge(i: int, j: int) -> bool:
    """Devuelve True si se puede emparejar i con j sin romper ninguna restricción."""
    if i == j:
        return False

    # Ya son rivales
    if j in adj[i]:
        return False

    # Límite de 8 rivales por equipo
    if deg[i] >= N_MATCHES or deg[j] >= N_MATCHES:
        return False

    # Límite de 2 rivales por bombo
    pi, pj = teams[i].pot, teams[j].pot
    if pot_count[i][pj] >= PER_POT:
        return False
    if pot_count[j][pi] >= PER_POT:
        return False

    # 1) Prohibir rivales del mismo país
    if not _forbid_same_country(i, j):
        return False

    # 2) Limitar rivales de un mismo país extranjero (máx 3)
    if not _limit_per_country(i, j):
        return False

    return True


def compute_candidates(i: int):
    """Devuelve la lista de índices j que pueden ser rivales válidos de i."""
    if deg[i] >= N_MATCHES:
        return []
    return [
        j for j in range(len(teams))
        if can_add_edge(i, j)
    ]
