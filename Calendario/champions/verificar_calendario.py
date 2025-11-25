from collections import defaultdict

N_JORNADAS = 8


def verificar_calendario(calendario):
    """
    Verifica las propiedades básicas del calendario:
      - Hay exactamente 8 jornadas.
      - En cada jornada ningún equipo juega más de 1 partido.
      - El número total de partidos es coherente con el número de equipos.
      - Cada equipo juega exactamente 8 partidos (4 en casa y 4 fuera).

    NO se comprueban ya:
      - Fechas / horas concretas.
      - Restricciones de ciudades (clash entre equipos de la misma ciudad).
    """

    print("\n==============================")
    print("     VERIFICACIÓN DEL CALENDARIO")
    print("==============================\n")

    # 1) Comprobación de número de jornadas
    jornadas = sorted(calendario.keys())
    if len(jornadas) != N_JORNADAS:
        print(f"❌ El calendario tiene {len(jornadas)} jornadas y deberían ser {N_JORNADAS}.")
        return False

    # Estructuras para acumular estadísticas
    partidos_por_jornada = {}
    apariciones_por_jornada = {}   # jornada -> dict(equipo -> veces que aparece)
    partidos_por_equipo = defaultdict(int)
    home_count = defaultdict(int)
    away_count = defaultdict(int)
    parejas_globales = set()
    equipos = set()

    todo_ok = True

    # 2) Recorremos todas las jornadas
    for j in jornadas:
        partidos = calendario[j]
        partidos_por_jornada[j] = len(partidos)
        apariciones = defaultdict(int)

        for local, visitante in partidos:
            if local == visitante:
                print(f"❌ Jornada {j}: partido inválido {local} vs {visitante} (mismo equipo).")
                todo_ok = False
                continue

            # Contabilizamos apariciones en la jornada (para saber si alguien juega dos veces)
            apariciones[local] += 1
            apariciones[visitante] += 1

            # Contabilizamos estadísticas globales
            equipos.add(local)
            equipos.add(visitante)
            partidos_por_equipo[local] += 1
            partidos_por_equipo[visitante] += 1
            home_count[local] += 1
            away_count[visitante] += 1

            # Comprobamos duplicados globales de emparejamientos
            par_no_ordenado = tuple(sorted((local, visitante)))
            if par_no_ordenado in parejas_globales:
                print(
                    f"❌ El emparejamiento {local} vs {visitante} aparece más de una vez en el calendario."
                )
                todo_ok = False
            else:
                parejas_globales.add(par_no_ordenado)

        apariciones_por_jornada[j] = dict(apariciones)

        # Nadie puede jugar más de una vez en la misma jornada
        for eq, veces in apariciones.items():
            if veces > 1:
                print(f"❌ Jornada {j}: el equipo {eq} juega {veces} veces (solo debería jugar 1).")
                todo_ok = False

        # Si el calendario es perfecto, en cada jornada deben jugar todos los equipos
        if len(equipos) > 0:
            expected_partidos = len(equipos) // 2
            if len(partidos) != expected_partidos:
                print(
                    f"⚠ Jornada {j}: tiene {len(partidos)} partidos; "
                    f"con {len(equipos)} equipos se esperaban {expected_partidos}."
                )
            if len(apariciones) != len(equipos):
                print(
                    f"⚠ Jornada {j}: solo aparecen {len(apariciones)} equipos "
                    f"de {len(equipos)} posibles."
                )

    total_partidos = sum(partidos_por_jornada.values())

    print("----------------------------------------------")
    print(f"Jornadas totales: {len(jornadas)}")
    print(f"Equipos detectados: {len(equipos)}")
    print(f"Partidos totales: {total_partidos}")
    print("----------------------------------------------\n")

    # 3) Comprobación de partidos por equipo (8) y reparto 4/4
    for eq in sorted(equipos):
        total = partidos_por_equipo[eq]
        h = home_count[eq]
        a = away_count[eq]

        if total != 8:
            print(f"❌ El equipo {eq} juega {total} partidos y debería jugar 8.")
            todo_ok = False

        if h != 4 or a != 4:
            print(
                f"❌ El equipo {eq} tiene {h} partidos en casa y {a} fuera "
                "(deberían ser 4 y 4)."
            )
            todo_ok = False

    if todo_ok:
        print("----------------------------------------------")
        print("TODO CORRECTO – El calendario cumple todas las reglas básicas.")
        print("----------------------------------------------")
    else:
        print("----------------------------------------------")
        print("Se han encontrado problemas en el calendario.")
        print("----------------------------------------------")

    return todo_ok
