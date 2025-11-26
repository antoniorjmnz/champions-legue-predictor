"""Punto de entrada: ejecuta el sorteo y muestra el resultado por pantalla."""

from solver import search, calls
from state import teams, adj, deg, pot_count
from config import N_MATCHES, PER_POT, MAX_SAME_COUNTRY, MAX_RIVALS_PER_COUNTRY
from data import generar_bombos_aleatorios  # (no se usa directamente, pero lo dejamos)
from fixtures import (
    generar_partidos_unicos,
    asignar_local_visitante,
    print_partidos_bonitos,
    print_partidos_por_equipo_ordenados,
)
from league_calendar import generate_league_calendar, print_calendar
from verificador_partidos import verificar_partidos
from verificar_calendario import verificar_calendario as verificar_calendario_bloques


def mostrar_bombos():
    print("\n==============================")
    print("       BOMBOS GENERADOS")
    print("==============================")

    # reconstruir los bombos a partir del atributo pot
    bombos = {1: [], 2: [], 3: [], 4: []}
    for t in teams:
        bombos[t.pot].append(t.name)

    for p in range(1, 5):
        print(f"\nBOMBO {p}:")
        for eq in bombos[p]:
            print(" -", eq)


def check_constraints() -> bool:
    """Verifica que todos los equipos cumplen las restricciones básicas (8 rivales, 2 por bombo)."""
    ok = True
    for i, t in enumerate(teams):
        if deg[i] != N_MATCHES:
            print("❌ Grado incorrecto en", t.name, "->", deg[i])
            ok = False

        # Comprobar que tiene exactamente PER_POT rivales de cada bombo
        for p in range(1, 5):
            if pot_count[i][p] != PER_POT:
                print(f"❌ Error bombo {p} en {t.name}: {pot_count[i][p]}")
                ok = False

    return ok


def print_diagnostics():
    print("\n==============================")
    print("     DIAGNÓSTICO DETALLADO")
    print("==============================\n")

    for i, t in enumerate(teams):
        name = t.name
        pot = t.pot
        country = t.country

        rivals_idx = adj[i]
        rivals = sorted([teams[j].name for j in rivals_idx])
        rival_countries = [teams[j].country for j in rivals_idx]
        rival_pots = [teams[j].pot for j in rivals_idx]

        # Límite del mismo país (si no hay caso especial, usa default)
        country_limit = MAX_SAME_COUNTRY.get(country, MAX_SAME_COUNTRY["default"])

        # Número de rivales del mismo país
        same_country_count = sum(1 for c in rival_countries if c == country)

        # Conteo por país
        country_count_map = {}
        for c in rival_countries:
            country_count_map[c] = country_count_map.get(c, 0) + 1

        # Máx. rivales de un mismo país extranjero
        worst_country = None
        max_foreign = 0
        for c, cnt in country_count_map.items():
            if c != country and cnt > max_foreign:
                max_foreign = cnt
                worst_country = c
        ok_foreign = (max_foreign <= MAX_RIVALS_PER_COUNTRY) if worst_country else True

        # Conteo por bombo
        pot_count_map = {}
        for p in rival_pots:
            pot_count_map[p] = pot_count_map.get(p, 0) + 1

        # Comprobaciones
        ok_same_country = same_country_count <= country_limit
        ok_by_pot = all(pot_count_map.get(p, 0) == PER_POT for p in range(1, 5))
        ok_deg = len(rivals) == N_MATCHES

        print(f"🔵 {name} ({country}, B{pot})")
        print(f"   Rivales ({len(rivals)}): {rivals}")

        print(
            f"   ➤ Rivales del mismo país: {same_country_count}/{country_limit} "
            f"{'✔' if ok_same_country else '❌'}"
        )
        print(f"   ➤ Rivales por país: {country_count_map}")

        if worst_country:
            print(
                f"   ➤ Máx. rivales de un país extranjero: "
                f"{max_foreign} de {worst_country} "
                f"(límite {MAX_RIVALS_PER_COUNTRY}) "
                f"{'✔' if ok_foreign else '❌'}"
            )
        else:
            print(
                f"   ➤ Máx. rivales de un país extranjero: 0 "
                f"(límite {MAX_RIVALS_PER_COUNTRY}) ✔"
            )

        print(f"   ➤ Rivales por bombo: {pot_count_map}")

        print(f"   ➤ {N_MATCHES} rivales obligatorios: {'✔' if ok_deg else '❌'}")
        print(f"   ➤ {PER_POT} por bombo: {'✔' if ok_by_pot else '❌'}")

        print("----------------------------------------------------")


def main():
    print("Generando sorteo determinista con bombos aleatorios...")
    mostrar_bombos()
    found = search()
    print("¿Solución encontrada?:", found, "| Llamadas recursivas:", calls)

    if not found:
        print("❌ No se encontró solución.")
        return

    ok = check_constraints()
    print("¿Restricciones básicas correctas?:", ok)
    print_diagnostics()

    # Generar emparejamientos únicos
    partidos_sin_orientar = generar_partidos_unicos()

    # Asignar local/visitante (4 casa / 4 fuera)
    partidos_finales = asignar_local_visitante(partidos_sin_orientar)

    # Imprimir lista global + verificación de 4/4 e ida/vuelta
    print_partidos_bonitos(partidos_finales)
    verificar_partidos(partidos_finales)
    print_partidos_por_equipo_ordenados(partidos_finales)

    # OPCIONAL: generar calendario por jornadas/bloques UEFA
    # calendario = generate_league_calendar(partidos_finales)
    # print_calendar(calendario)
    # verificar_calendario_bloques(calendario)


if __name__ == "__main__":
    main()
