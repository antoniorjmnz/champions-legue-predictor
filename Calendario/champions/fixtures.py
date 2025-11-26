import random
from state import teams, adj


def generar_partidos_unicos():
    partidos = set()
    for i, rivales in enumerate(adj):
        for j in rivales:
            if i < j:
                A = teams[i].name
                B = teams[j].name
                partidos.add((A, B))
    return list(partidos)


# ============================
# HEURÍSTICAS IMPORTANTES
# ============================

def dificultad_equipo(eq):
    """
    Cuanto más difícil es su distribución esperada,
    más pronto deben colocarse sus partidos.
    """
    # Todos deben acabar con 4 y 4.
    # Equipos con rivales muy variados son más fáciles.
    # Equipos con rivales muy homogéneos son más difíciles.
    # Vamos a medirlo por dispersión de países.
    paises = {}
    for idx, team in enumerate(teams):
        if team.name == eq:
            for r in adj[idx]:
                paises[teams[r].country] = paises.get(teams[r].country, 0) + 1

    return -len(paises)   # menos países → más difícil (valor mayor)


def ordenar_partidos(partidos):
    """
    Ordenación MRV: los partidos más difíciles primero.
    """
    score = {}

    for A, B in partidos:
        sA = dificultad_equipo(A)
        sB = dificultad_equipo(B)
        score[(A, B)] = sA + sB

    # Orden descendente: más difíciles primero
    return sorted(partidos, key=lambda x: score[x], reverse=True)


# ============================
# BACKTRACKING 4/4 PERFECTO
# ============================

def asignar_local_visitante(partidos_raw):
    """
    Backtracking inteligente para asignar local/visitante sin romper 4/4.
    Se reinicia automáticamente si un orden no es bueno.
    """

    intentos = 0
    while True:
        intentos += 1

        # Copia y ordenación inteligente
        partidos = ordenar_partidos(partidos_raw.copy())
        random.shuffle(partidos[:12])   # Pequeña aleatoriedad controlada

        equipos = [t.name for t in teams]
        home = {t: 0 for t in equipos}
        away = {t: 0 for t in equipos}
        resultado = []

        LIMITE_RECURSION = 6000
        llamadas = 0

        def es_posible(home, away, pending):
            for eq in equipos:
                h, a = home[eq], away[eq]
                if h > 4 or a > 4:
                    return False
                if h + pending < 4:
                    return False
                if a + pending < 4:
                    return False
            return True

        def backtrack(idx):
            nonlocal llamadas
            llamadas += 1
            if llamadas > LIMITE_RECURSION:
                return False

            if idx == len(partidos):
                return True

            A, B = partidos[idx]

            opciones = [(A, B), (B, A)]
            random.shuffle(opciones)

            for local, visitante in opciones:
                if home[local] >= 4 or away[visitante] >= 4:
                    continue

                # asignar
                home[local] += 1
                away[visitante] += 1
                resultado.append((local, visitante))

                if es_posible(home, away, len(partidos) - idx - 1):
                    if backtrack(idx + 1):
                        return True

                # deshacer
                home[local] -= 1
                away[visitante] -= 1
                resultado.pop()

            return False

        if backtrack(0):
            print(f"✔ Local/visitante resuelto en {intentos} intento(s)")
            return resultado
        else:
            print(f"✘ Reintentando (intento {intentos})...")


# ============================
# PRINT
# ============================

def print_partidos_bonitos(partidos):
    print("\n==============================")
    print("     LISTA FINAL DE PARTIDOS")
    print("==============================\n")

    for local, visitante in partidos:
        print(f"{local:22s} (LOCAL)  vs  {visitante}")

    print("\nTOTAL PARTIDOS:", len(partidos))


def print_partidos_por_equipo_ordenados(partidos_finales):
    """
    Para cada equipo imprime sus 8 partidos en formato:
    EquipoA - EquipoB   (LOCAL EquipoA)
    EquipoA - EquipoB   (LOCAL EquipoB)

    Mucho más claro para el profesor.
    """

    # Diccionario: equipo -> lista de partidos [(local, visitante)]
    mapa = {t.name: [] for t in teams}

    for local, visitante in partidos_finales:
        # Añadir partido a ambos equipos
        mapa[local].append((local, visitante))
        mapa[visitante].append((local, visitante))

    print("\n====================================")
    print("    PARTIDOS POR EQUIPO (FORMATO LIMPIO)")
    print("====================================\n")

    # Orden alfabético de equipos
    for equipo in sorted(mapa.keys()):
        print(f"────────── {equipo} ──────────")

        # Ordenar sus 8 rivales alfabéticamente
        partidos = sorted(mapa[equipo], key=lambda x: (x[0], x[1]))

        for local, visitante in partidos:
            # Formato: A - B (LOCAL A o LOCAL B)
            print(f"{local}  -  {visitante}   (LOCAL {local})")

        print()
