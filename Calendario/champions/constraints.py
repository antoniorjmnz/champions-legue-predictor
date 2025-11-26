from state import teams, adj, deg, pot_count, country_count
from config import N_MATCHES, PER_POT, MAX_SAME_COUNTRY, MAX_RIVALS_PER_COUNTRY


def compute_candidates(i: int):
    """
    Devuelve los candidatos válidos para emparejar con el equipo i
    aplicando TODAS las restricciones:
        ❌ no repetir rival
        ❌ no exceder 8 rivales
        ❌ no contra equipos del mismo país (regla Champions)
        ❌ no exceder el límite por bombo (2 por bombo)
        ❌ no exceder el límite de rivales por país extranjero (máx. 3)
        ❌ no crear conflicto con rivales futuros (forward checking básico)
    """

    candidates = []

    ti = teams[i]
    pot_i = ti.pot
    country_i = ti.country

    for j in range(len(teams)):
        if j == i:
            continue

        # 1. ya son rivales → no permitido
        if j in adj[i]:
            continue

        # 2. no sobrepasar 8 rivales
        if deg[j] >= N_MATCHES:
            continue

        # 3. REGLA IMPORTANTE DEL PROFESOR:
        #    NO SE PUEDE JUGAR CONTRA EQUIPOS DEL MISMO PAÍS
        if teams[j].country == country_i:
            continue

        # 4. no exceder rivales por bombo
        pj = teams[j].pot
        if pot_count[i][pj] >= PER_POT:
            continue
        if pot_count[j][pot_i] >= PER_POT:
            continue

        # 4.b) no exceder el límite de rivales de un mismo país extranjero (máx. 3)
        country_j = teams[j].country
        if country_count[i][country_j] >= MAX_RIVALS_PER_COUNTRY:
            continue
        if country_count[j][country_i] >= MAX_RIVALS_PER_COUNTRY:
            continue

        # 5. "forward checking" básico:
        #    ambos equipos deben poder completar 8 rivales
        restantes_i = N_MATCHES - deg[i]
        restantes_j = N_MATCHES - deg[j]

        posibles_i = sum(
            1
            for k in range(len(teams))
            if k != i
            and k not in adj[i]
            and teams[k].country != country_i
            and pot_count[i][teams[k].pot] < PER_POT
        )

        posibles_j = sum(
            1
            for k in range(len(teams))
            if k != j
            and k not in adj[j]
            and teams[k].country != teams[j].country
            and pot_count[j][teams[k].pot] < PER_POT
        )

        if posibles_i < restantes_i:
            continue

        if posibles_j < restantes_j:
            continue

        # candidato válido
        candidates.append(j)

    return candidates
