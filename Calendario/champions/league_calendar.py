"""
Generación del calendario UEFA 2025/26

Con:
 - 8 jornadas
 - 1 partido por jornada y equipo
 - 4 casa / 4 fuera por equipo (garantizado por fixtures.py con Euler)
 - Sin city-clash (misma ciudad, mismo día) siempre que sea posible
 - Todos los partidos a las 21:00
"""

from collections import defaultdict
from datetime import datetime, timedelta
import random

# ---------------------------------------------------------
# CITY-CLASH: equipos que comparten ciudad
# ---------------------------------------------------------
TEAM_CITY = {
    "Real Madrid": "Madrid",
    "Atlético de Madrid": "Madrid",
    "Arsenal": "Londres",
    "Chelsea": "Londres",
    "Tottenham": "Londres",
}

# ---------------------------------------------------------
# FECHAS UEFA OFICIALES POR JORNADA
# ---------------------------------------------------------
FECHAS_JORNADAS = {
    1: ("2025-09-16", "2025-09-18"),
    2: ("2025-09-30", "2025-10-02"),
    3: ("2025-10-21", "2025-10-23"),
    4: ("2025-11-04", "2025-11-06"),
    5: ("2025-11-25", "2025-11-27"),
    6: ("2025-12-09", "2025-12-11"),
    7: ("2026-01-20", "2026-01-21"),
    8: ("2026-01-27", "2026-01-28"),
}

HORA_OFICIAL = "21:00"


# ---------------------------------------------------------
# AUXILIAR: generar lista de fechas en un rango
# ---------------------------------------------------------
def _rango_fechas(inicio_str, fin_str):
    inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
    fin = datetime.strptime(fin_str, "%Y-%m-%d")
    res = []
    d = inicio
    while d <= fin:
        res.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return res


# ---------------------------------------------------------
# CALENDARIO PRINCIPAL
# ---------------------------------------------------------
def generate_league_calendar(fixtures):
    """
    fixtures: lista de tuplas (local, visitante) ya ORIENTADAS,
              con 4 casa / 4 fuera por equipo.

    Devuelve:
      dict[jornada] -> lista de partidos:
        {
          "local": str,
          "visitante": str,
          "fecha": "YYYY-MM-DD",
          "hora": "HH:MM"
        }
    """
    NUM_JORNADAS = 8

    # Normalizamos fixtures a objetos
    partidos = [{"local": a, "visitante": b} for (a, b) in fixtures]

    # Para cada equipo, jornadas en las que ya juega
    jornadas_por_equipo = defaultdict(set)

    # Jornada asignada a cada partido (por índice)
    asignacion_jornada = [None] * len(partidos)

    # ---------------------------------------------------------
    # BACKTRACKING SOLO PARA ASIGNAR JORNADAS (sin home/away)
    # ---------------------------------------------------------
    def backtrack(k):
        # k = número de partidos ya asignados
        if k == len(partidos):
            return True

        # Elegimos el partido sin jornada asignada con menor nº de opciones (MRV)
        mejor_idx = None
        mejor_dom = None

        for i, p in enumerate(partidos):
            if asignacion_jornada[i] is not None:
                continue

            a = p["local"]
            b = p["visitante"]

            # Jornadas donde a y b están libres
            dom = [
                j
                for j in range(1, NUM_JORNADAS + 1)
                if j not in jornadas_por_equipo[a]
                and j not in jornadas_por_equipo[b]
            ]

            if not dom:
                # Este partido no se puede colocar -> poda
                return False

            if mejor_dom is None or len(dom) < len(mejor_dom):
                mejor_dom = dom
                mejor_idx = i
                if len(dom) == 1:
                    break

        # Asignamos ese partido a una jornada posible
        random.shuffle(mejor_dom)
        i = mejor_idx
        a = partidos[i]["local"]
        b = partidos[i]["visitante"]

        for j in mejor_dom:
            asignacion_jornada[i] = j
            jornadas_por_equipo[a].add(j)
            jornadas_por_equipo[b].add(j)

            if backtrack(k + 1):
                return True

            # deshacer
            jornadas_por_equipo[a].remove(j)
            jornadas_por_equipo[b].remove(j)
            asignacion_jornada[i] = None

        return False

    ok = backtrack(0)
    if not ok:
        raise RuntimeError(
            "❌ No se pudo asignar un calendario de 8 jornadas (1 partido por jornada y equipo)."
        )

    # Construimos la estructura jornadas[j] = lista de (local, visitante)
    jornadas_brutas = {j: [] for j in range(1, NUM_JORNADAS + 1)}
    for idx, j in enumerate(asignacion_jornada):
        p = partidos[idx]
        jornadas_brutas[j].append((p["local"], p["visitante"]))

    # ---------------------------------------------------------
    # ASIGNACIÓN DE FECHAS (EVITAR CITY-CLASH)
    # ---------------------------------------------------------
    calendario = {j: [] for j in range(1, NUM_JORNADAS + 1)}

    # city_used[fecha] = set de ciudades que ya juegan en casa ese día
    city_used = defaultdict(set)

    def asignar_fecha(local, inicio, fin):
        fechas = _rango_fechas(inicio, fin)
        ciudad = TEAM_CITY.get(local)

        if ciudad is None:
            # Equipo sin conflicto de ciudad -> primera fecha del rango
            return fechas[0]

        # Intentamos una fecha donde su ciudad aún no tenga partido en casa
        for f in fechas:
            if ciudad not in city_used[f]:
                return f

        # Si no hay ninguna libre (muy raro), devolvemos la primera
        return fechas[0]

    for j in range(1, NUM_JORNADAS + 1):
        inicio, fin = FECHAS_JORNADAS[j]

        for (local, visitante) in jornadas_brutas[j]:
            fecha = asignar_fecha(local, inicio, fin)
            ciudad = TEAM_CITY.get(local)
            if ciudad:
                city_used[fecha].add(ciudad)

            calendario[j].append(
                {
                    "local": local,
                    "visitante": visitante,
                    "fecha": fecha,
                    "hora": HORA_OFICIAL,
                }
            )

    return calendario


# ---------------------------------------------------------
# IMPRIMIR
# ---------------------------------------------------------
def print_calendar(jornadas):
    print("\n==============================")
    print("      CALENDARIO OFICIAL")
    print("==============================\n")

    for j in sorted(jornadas.keys()):
        print(f"\n---------- Jornada {j} ----------")
        for p in jornadas[j]:
            print(
                f"{p['fecha']}  {p['hora']}  |  "
                f"{p['local']:22s} (LOCAL)  vs  "
                f"{p['visitante']:22s} (VISITANTE)"
            )
