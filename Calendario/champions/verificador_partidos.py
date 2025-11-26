def verificar_partidos(partidos):
    print("=== VERIFICANDO PARTIDOS ===")

    # 1. Duplicados exactos
    duplicados = set()
    vistos = set()
    for p in partidos:
        if p in vistos:
            duplicados.add(p)
        else:
            vistos.add(p)

    # 2. Duplicados invertidos
    invertidos = []
    parejas = set()
    for local, visitante in partidos:
        par = tuple(sorted([local, visitante]))
        if par in parejas:
            invertidos.append((local, visitante))
        else:
            parejas.add(par)

    # 3. Contar home/away por equipo
    home = {}
    away = {}
    for local, visitante in partidos:
        home[local] = home.get(local, 0) + 1
        away[visitante] = away.get(visitante, 0) + 1

    print("\n> DUPLICADOS EXACTOS:")
    print(duplicados if duplicados else "✔ Ninguno")

    print("\n> DUPLICADOS INVERTIDOS (IDA/VUELTA NO PERMITIDO):")
    if invertidos:
        print("❌ Se encontraron {} parejas invertidas:".format(len(invertidos)))
        for p in invertidos[:20]:
            print("  -", p)
    else:
        print("✔ Ninguno")

    print("\n> PARTIDOS EN CASA:")
    for team, n in sorted(home.items()):
        print(f"  {team}: {n}")
    print("\n> PARTIDOS FUERA:")
    for team, n in sorted(away.items()):
        print(f"  {team}: {n}")

    print("\n> VIOLACIONES 4 CASA / 4 FUERA:")
    errores = False
    for team in home:
        if home[team] != 4:
            print(f"❌ {team} tiene {home[team]} partidos en casa")
            errores = True
    for team in away:
        if away[team] != 4:
            print(f"❌ {team} tiene {away[team]} partidos fuera")
            errores = True

    if not errores:
        print("✔ Todos tienen 4 casa / 4 fuera")

    print("\n=== FIN VERIFICACIÓN ===")
