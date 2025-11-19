# fixtures.py

from state import teams, adj


def generar_partidos_unicos():
    """
    Devuelve 144 partidos (local, visitante)
    uno por cada rival del sorteo.
    """
    partidos = []
    for i, rivales in enumerate(adj):
        for j in rivales:
            if i < j:  # evita duplicados
                local = teams[i].name
                visitante = teams[j].name
                partidos.append((local, visitante))
    return partidos


def print_fixtures(lista):
    print("\n==============================")
    print("     PARTIDOS (LOCAL/VISITANTE)")
    print("==============================\n")

    for local, visitante in lista:
        print(f"{local:22s} (LOCAL)  vs  {visitante}")
