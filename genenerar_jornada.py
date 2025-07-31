import json

# -------------------------------
# Cargar datos desde tu JSON
# -------------------------------
RUTA_JSON = "datos.json"

with open(RUTA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# Preparar datos
# -------------------------------
jugadores = [j["nombre"] for j in data["liga"]]
victorias = {j["nombre"]: j["victorias"] for j in data["liga"]}
puntos = {j["nombre"]: j["puntos"] for j in data["liga"]}

# Crear historial de enfrentamientos
enfrentamientos_previos = {j: set() for j in jugadores}

for jornada in data["jornadas"]:
    for combate in jornada:
        l = combate["local"]
        v = combate["visitante"]
        enfrentamientos_previos[l].add(v)
        enfrentamientos_previos[v].add(l)

# Ordenar jugadores por victorias (desc), usando puntos como desempate
jugadores_ordenados = sorted(
    jugadores,
    key=lambda x: (-victorias[x], -puntos[x], x)
)

# -------------------------------
# Backtracking Swiss Optimizado
# -------------------------------
def generar_swiss_optimo(jugadores_ordenados, enfrentamientos_previos, victorias):
    n = len(jugadores_ordenados)
    mejor_solucion = None
    mejor_score = float("inf")  # Queremos minimizar la diferencia de victorias

    def calcular_score(pares):
        score = 0
        for a, b in pares:
            diff = abs(victorias[a] - victorias[b])
            score += diff  # Penaliza emparejamientos desbalanceados
        return score

    def backtrack(idx, pares_actuales, usados):
        nonlocal mejor_solucion, mejor_score

        # Si ya tenemos todos los pares
        if len(pares_actuales) == n // 2:
            score = calcular_score(pares_actuales)
            if score < mejor_score:
                mejor_score = score
                mejor_solucion = pares_actuales[:]
            return
        
        # Buscar siguiente jugador libre
        while idx < n and jugadores_ordenados[idx] in usados:
            idx += 1
        if idx >= n:
            return
        
        jugador = jugadores_ordenados[idx]
        
        # Intentar emparejar con rivales
        for i in range(idx + 1, n):
            rival = jugadores_ordenados[i]
            if rival in usados:
                continue
            if rival in enfrentamientos_previos[jugador]:
                continue
            
            # Probar este par
            pares_actuales.append((jugador, rival))
            usados.update([jugador, rival])
            
            backtrack(idx + 1, pares_actuales, usados)
            
            # Backtrack
            pares_actuales.pop()
            usados.remove(jugador)
            usados.remove(rival)

    backtrack(0, [], set())
    return mejor_solucion

# -------------------------------
# Generar jornada nueva
# -------------------------------
nueva_jornada = generar_swiss_optimo(jugadores_ordenados, enfrentamientos_previos, victorias)

if not nueva_jornada:
    print("⚠️ No se pudo generar una jornada sin repeticiones")
else:
    print("✅ Jornada generada:")
    for local, visitante in nueva_jornada:
        print(f"{local} vs {visitante}")

    # Añadir al JSON en el formato requerido
    jornada_json = [
        {"local": l, "visitante": v, "resultado": "-", "puntosGanados": 0}
        for l, v in nueva_jornada
    ]

    data["jornadas"].append(jornada_json)

    # Guardar cambios en el JSON
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ Jornada añadida al JSON correctamente.")
