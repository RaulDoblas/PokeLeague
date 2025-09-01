import json
import random

# -------------------------------
# Cargar datos desde tu JSON
# -------------------------------
RUTA_JSON = "datos.json"

with open(RUTA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# Comprobar si la última jornada está completada
# -------------------------------
if data["jornadas"]:
    ultima_jornada = data["jornadas"][-1]
    inacabada = any(combate["resultado"] == "-" for combate in ultima_jornada)

    if inacabada:
        print("⚠️ No se puede generar una nueva jornada: la última aún no está completada.")
        exit(0)

# -------------------------------
# Preparar datos
# -------------------------------
jugadores = [j["nombre"] for j in data["liga"]]

# Crear historial de enfrentamientos
enfrentamientos_previos = {j: set() for j in jugadores}

for jornada in data["jornadas"]:
    for combate in jornada:
        l = combate["local"]
        v = combate["visitante"]
        enfrentamientos_previos[l].add(v)
        enfrentamientos_previos[v].add(l)

# -------------------------------
# Generar emparejamientos sin repetir
# -------------------------------
def generar_jornada(jugadores, enfrentamientos_previos, max_intentos=5000):
    jugadores_restantes = jugadores[:]
    random.shuffle(jugadores_restantes)
    n = len(jugadores_restantes)

    for _ in range(max_intentos):
        pares = []
        valido = True

        for i in range(0, n, 2):
            a, b = jugadores_restantes[i], jugadores_restantes[i + 1]

            if b in enfrentamientos_previos[a]:
                valido = False
                break
            pares.append((a, b))

        if valido:
            return pares

        # remezclar y volver a intentar
        random.shuffle(jugadores_restantes)

    return None

# -------------------------------
# Generar jornada nueva
# -------------------------------
nueva_jornada = generar_jornada(jugadores, enfrentamientos_previos)

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
