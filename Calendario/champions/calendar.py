# calendar.py
"""
Generación del calendario fase liga:
 - 8 partidos por equipo (4 casa / 4 fuera)
 - 8 jornadas
 - Sin partidos duplicados por jornada
 - Evita CITY-CLASH (equipos de la misma ciudad en casa el mismo día)
 - Fechas reales UEFA 2025/26
"""

from collections import defaultdict
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Compatibilidad _strptime
# ---------------------------------------------------------------------------
day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
day_name = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]
month_abbr = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_name = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

# ---------------------------------------------------------------------------
# Equipos por ciudad para evitar CITY-CLASH
# ---------------------------------------------------------------------------
TEAM_CITY = {
    "Real Madrid": "Madrid",
    "Atlético de Madrid": "Madrid",

    "Arsenal": "Londres",
    "Chelsea": "Londres",
    "Tottenham": "Londres",
}

HORARIOS = ["18:45", "21:00"]

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

# ---------------------------------------------------------------------------

def fecha_random(inicio_str, fin_str):
    inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
    fin = datetime.strptime(fin_str, "%Y-%m-%d")
    días = (fin - inicio).days
    return (inicio + timedelta(days=random.randint(0, días))).strftime("%Y-%m-%d")


def hay_city_clash(partidos_jornada, local_equipo, fecha):
    ciudad = TEAM_CITY.get(local_equipo)
    if not ciudad:
        return False
    for p in partidos_jornada:
        if TEAM_CITY.get(p["local"]) == ciudad and p["fecha"] == fecha:
            return True
    return False

# ---------------------------------------------------------------------------
# GENERADOR DE CALENDARIO
# ---------------------------------------------------------------------------

def generate_league_calendar(fixtures):

    unique_matches = list(fixtures)
    NUM_JORNADAS = 8

    jornadas = {j: [] for j in range(1, NUM_JORNADAS + 1)}
    equipos_en_jornada = {j: set() for j in range(1, NUM_JORNADAS + 1)}

    home = defaultdict(int)
    away = defaultdict(int)

    # ---------------- BACKTRACKING ----------------

    def backtrack(pending):
        if not pending:
            # Todos 4 casa / 4 fuera
            for eq in home:
                if home[eq] != 4 or away[eq] != 4:
                    return False
            return True

        # MRV (partido con menos jornadas posibles)
        best_match = None
        best_opts = None

        for (a, b) in pending:
            posibles = [
                j for j in range(1, NUM_JORNADAS + 1)
                if a not in equipos_en_jornada[j]
                and b not in equipos_en_jornada[j]
            ]
            if not posibles:
                return False

            if best_opts is None or len(posibles) < len(best_opts):
                best_match = (a, b)
                best_opts = posibles

        random.shuffle(best_opts)

        a, b = best_match
        remaining = list(pending)
        remaining.remove(best_match)

        for j in best_opts:

            # probar orientación A local / B visitante y viceversa
            for local, visitante in [(a, b), (b, a)]:

                if home[local] >= 4 or away[visitante] >= 4:
                    continue

                jornadas[j].append((local, visitante))
                equipos_en_jornada[j].add(local)
                equipos_en_jornada[j].add(visitante)
                home[local] += 1
                away[visitante] += 1

                if backtrack(remaining):
                    return True

                # deshacer
                jornadas[j].pop()
                equipos_en_jornada[j].remove(local)
                equipos_en_jornada[j].remove(visitante)
                home[local] -= 1
                away[visitante] -= 1

        return False

    # ---------------- EJECUTAR BACKTRACK ----------------

    ok = backtrack(unique_matches)

    if not ok:
        print("❌ No se generó un calendario válido 4/4.")
        return {j: [] for j in range(1, NUM_JORNADAS + 1)}

    # ---------------- ASIGNAR FECHAS ----------------

    calendario_final = {j: [] for j in range(1, NUM_JORNADAS + 1)}

    for j in range(1, NUM_JORNADAS + 1):
        inicio, fin = FECHAS_JORNADAS[j]

        for (local, visitante) in jornadas[j]:

            # buscar fecha sin city clash
            for _ in range(20):
                fecha = fecha_random(inicio, fin)
                if not hay_city_clash(calendario_final[j], local, fecha):
                    break

            hora = random.choice(HORARIOS)

            calendario_final[j].append({
                "local": local,
                "visitante": visitante,
                "fecha": fecha,
                "hora": hora
            })

    return calendario_final


# ---------------------------------------------------------------------------
# PRINT DEL CALENDARIO
# ---------------------------------------------------------------------------

def print_calendar(jornadas):
    print("\n==============================")
    print("      CALENDARIO OFICIAL")
    print("==============================\n")

    for j in range(1, 9):
        print(f"\n---------- Jornada {j} ----------")
        for p in jornadas[j]:
            print(
                f"{p['fecha']}  {p['hora']}  |  "
                f"{p['local']:22s} (LOCAL)  vs  "
                f"{p['visitante']:22s} (VISITANTE)"
            )
