# verificar_calendario.py

TEAM_CITY = {
    "Real Madrid": "Madrid",
    "Atlético de Madrid": "Madrid",
    "Arsenal": "Londres",
    "Chelsea": "Londres",
    "Tottenham": "Londres",
}

# Rango oficial de jornadas (igual que en calendar.py)
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

from datetime import datetime


def verificar_calendario(jornadas):
    print("\n==============================")
    print("     VERIFICACIÓN DEL CALENDARIO")
    print("==============================\n")

    errores = 0

    # ----------------------------------------------
    # 1. Verificar que no haya equipos jugando 2 veces en la MISMA jornada
    # ----------------------------------------------
    for j, partidos in jornadas.items():
        equipos = []
        for p in partidos:
            equipos.append(p["local"])
            equipos.append(p["visitante"])

        duplicados = {x for x in equipos if equipos.count(x) > 1}

        if duplicados:
            errores += 1
            print(f"❌ Jornada {j}: equipos con 2 partidos -> {duplicados}")
        else:
            print(f"✔ Jornada {j}: ningún equipo juega dos veces")

    print("\n----------------------------------------------")

    # ----------------------------------------------
    # 2. Verificar CITY-CLASH: misma ciudad NO juega en casa el mismo día
    # ----------------------------------------------
    for j, partidos in jornadas.items():
        fecha_ciudad = {}  # fecha -> ciudad -> equipo

        for p in partidos:
            local = p["local"]
            fecha = p["fecha"]
            ciudad = TEAM_CITY.get(local)

            if not ciudad:
                continue  # ciudades no conflictivas no importan

            if fecha not in fecha_ciudad:
                fecha_ciudad[fecha] = {}

            if ciudad in fecha_ciudad[fecha]:
                errores += 1
                print(
                    f"❌ CITY-CLASH en Jornada {j}, fecha {fecha}: "
                    f"{local} coincide con {fecha_ciudad[fecha][ciudad]} (misma ciudad)"
                )
            else:
                fecha_ciudad[fecha][ciudad] = local

    print("\n----------------------------------------------")

    # ----------------------------------------------
    # 3. Verificar que cada fecha esté dentro del rango oficial de la jornada
    # ----------------------------------------------
    for j, partidos in jornadas.items():
        inicio_str, fin_str = FECHAS_JORNADAS[j]
        inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
        fin = datetime.strptime(fin_str, "%Y-%m-%d")

        for p in partidos:
            fecha = datetime.strptime(p["fecha"], "%Y-%m-%d")

            if not (inicio <= fecha <= fin):
                errores += 1
                print(
                    f"❌ Fecha fuera de rango en Jornada {j}: "
                    f"{p['local']} vs {p['visitante']} ({p['fecha']})"
                )

    print("\n----------------------------------------------")

    # ----------------------------------------------
    # 4. Resumen final
    # ----------------------------------------------
    if errores == 0:
        print("TODO CORRECTO – El calendario cumple todas las reglas ")
    else:
        print(f"ERRORES Encontrados {errores} problema(s). Revisa arriba.")

    print("----------------------------------------------\n")
