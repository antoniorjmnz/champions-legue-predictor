# solver.py
"""Algoritmo de backtracking determinista para construir el sorteo."""

from constraints import compute_candidates
from state import teams, adj, deg, add_edge, remove_edge, E
from config import N_MATCHES

calls = 0  # número de llamadas recursivas al solver


def search(edge_no: int = 0) -> bool:
    """Intenta construir un sorteo válido mediante backtracking determinista."""
    global calls
    calls += 1

    # Caso base: hemos colocado todos los emparejamientos
    if edge_no == E:
        # Comprobamos que todos tienen N_MATCHES rivales
        return all(d == N_MATCHES for d in deg)

    # Heurística MRV: elegir el equipo con menos opciones posibles
    best_i = None
    best_candidates = None

    for i in range(len(teams)):
        if deg[i] >= N_MATCHES:
            continue

        cand = compute_candidates(i)
        if not cand:
            # Este equipo no puede completar sus rivales -> rama muerta
            return False

        if best_i is None or len(cand) < len(best_candidates):
            best_i = i
            best_candidates = cand

    # Orden determinista de candidatos:
    # primero menor grado, luego por bombo, país y nombre
    best_candidates.sort(
        key=lambda j: (
            deg[j],
            teams[j].pot,
            teams[j].country,
            teams[j].name,
        )
    )

    for j in best_candidates:
        add_edge(best_i, j)
        if search(edge_no + 1):
            return True
        remove_edge(best_i, j)

    return False
