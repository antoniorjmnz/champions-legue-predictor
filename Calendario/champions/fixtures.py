from state import teams, adj


def generar_partidos_unicos_ida_vuelta():
    """
    Genera TODOS los partidos con orientación:
        - Ida  (A vs B)
        - Vuelta (B vs A)

    Total = 288 partidos (144 emparejamientos * 2).
    """
    partidos = []

    nombres = {i: teams[i].name for i in range(len(teams))}

    for i, rivales in enumerate(adj):
        for j in rivales:
            if i < j:
                A = nombres[i]
                B = nombres[j]

                # Ida
                partidos.append((A, B))

                # Vuelta
                partidos.append((B, A))

    # Orden alfabético por equipo LOCAL
    partidos.sort(key=lambda x: (x[0], x[1]))

    return partidos


def print_partidos_bonitos(partidos):
    """
    Imprime los 288 partidos (ida y vuelta) con formato elegante.
    """
    print("\n==============================")
    print("     LISTADO COMPLETO")
    print("        (IDA + VUELTA)")
    print("==============================\n")

    for local, visitante in partidos:
        print(f"{local:22s} (LOCAL)     vs     {visitante:22s} (VISITANTE)")

    print("\nTOTAL PARTIDOS:", len(partidos))
