# constraints.py
"""Comprobación de restricciones para decidir si se puede emparejar i con j."""

from config import N_MATCHES, PER_POT, MAX_SAME_COUNTRY
from state import teams, adj, deg, pot_count, country_count


def _limit_same_country(i: int, j: int) -> bool:
    """Comprueba si añadir (i, j) respeta el límite de rivales del mismo país."""
    ci = teams[i].country
    cj = teams[j].country

    if ci != cj:
        # No son del mismo país -> no afecta a esta restricción
        return True

    limit_i = MAX_SAME_COUNTRY.get(ci, MAX_SAME_COUNTRY["default"])
    limit_j = MAX_SAME_COUNTRY.get(cj, MAX_SAME_COUNTRY["default"])

    return (
        country_count[i][ci] < limit_i
        and country_count[j][cj] < limit_j
    )


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

    # Límite de rivales del mismo país
    if not _limit_same_country(i, j):
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
