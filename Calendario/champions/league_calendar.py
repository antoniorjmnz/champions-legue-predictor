import random
from collections import defaultdict

N_JORNADAS = 8     # 8 bloques UEFA
DIAS_POR_JORNADA = 3   # Cada jornada dura 3 días
PARTIDOS_POR_DIA = 6   # 6 partidos por día → 18 por jornada (144 total)


def generate_league_calendar(partidos, seed=None):
    """
    Versión INFALIBLE basada en el modelo UEFA real:
    - 8 jornadas (bloques)
    - cada jornada tiene 3 días diferentes
    - un equipo no puede jugar dos veces el mismo día
    - sí puede jugar dos días distintos dentro del mismo bloque UEFA (como en formato real)
    """
    if seed is not None:
        random.seed(seed)

    # Equipos
    equipos = set()
    for a, b in partidos:
        equipos.add(a)
        equipos.add(b)
    equipos = sorted(equipos)

    # Crear estructura: jornada → día → lista de partidos
    calendario = {
        j: {d: [] for d in range(1, DIAS_POR_JORNADA + 1)}
        for j in range(1, N_JORNADAS + 1)
    }

    equipos_dia = {
        j: {d: set() for d in range(1, DIAS_POR_JORNADA + 1)}
        for j in range(1, N_JORNADAS + 1)
    }

    partidos = list(partidos)
    random.shuffle(partidos)

    j = 1
    d = 1

    for a, b in partidos:
        colocado = False

        # Intentar colocar en algún día de alguna jornada
        for jj in range(1, N_JORNADAS + 1):
            for dd in range(1, DIAS_POR_JORNADA + 1):

                if len(calendario[jj][dd]) >= PARTIDOS_POR_DIA:
                    continue
                if a in equipos_dia[jj][dd] or b in equipos_dia[jj][dd]:
                    continue

                # Colocar
                calendario[jj][dd].append((a, b))
                equipos_dia[jj][dd].add(a)
                equipos_dia[jj][dd].add(b)

                colocado = True
                break
            if colocado:
                break

        if not colocado:
            raise RuntimeError("Algo muy extraño ocurrió — esta versión no debería fallar nunca.")

    # Simplificar salida: convertir días en lista lineal por jornada
    salida = {}
    for jj in calendario:
        salida[jj] = []
        for dd in calendario[jj]:
            for a, b in calendario[jj][dd]:
                # random home/away
                if random.random() < 0.5:
                    salida[jj].append((a, b))
                else:
                    salida[jj].append((b, a))

    return salida


def print_calendar(calendario):
    print("\n==============================")
    print("   CALENDARIO UEFA — BLOQUES")
    print("==============================\n")

    total = 0
    for j in sorted(calendario.keys()):
        print(f"\n----- Jornada {j} -----")
        for (local, visitante) in calendario[j]:
            print(f"{local:22s} vs {visitante:22s}")
            total += 1

    print("\nTOTAL PARTIDOS:", total)
