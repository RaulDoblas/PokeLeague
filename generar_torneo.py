#!/usr/bin/env python3
"""
Script para generar el bracket del torneo final basado en la clasificación de la liga.
Los mejores entrenadores se enfrentan en un torneo de eliminación directa.
"""

import json
import sys
from pathlib import Path


def generar_torneo(datos_file="datos.json"):
    """Genera el bracket del torneo basado en la clasificación."""
    # Leer datos actuales
    try:
        with open(datos_file, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {datos_file}")
        return False
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo {datos_file} no es un JSON válido")
        return False

    # Obtener clasificación ordenada por victorias
    liga = datos.get("liga", [])
    if not liga:
        print("❌ Error: No hay datos de la liga")
        return False

    # Ordenar por victorias (descendente), luego por derrotas (ascendente)
    liga_ordenada = sorted(
        liga,
        key=lambda x: (-x["victorias"], x["derrotas"])
    )

    # Número de entrenadores en el torneo (máximo 8 para el formato actual)
    num_participantes = min(len(liga_ordenada), 8)

    print(f"📊 Generando torneo con {num_participantes} participantes:")
    for i, entrenador in enumerate(liga_ordenada[:num_participantes], 1):
        print(f"   {i}. {entrenador['nombre']} ({entrenador['victorias']}V - {entrenador['derrotas']}D)")

    # Crear bracket según el número de participantes
    torneo = {}

    if num_participantes == 8:
        # Torneo completo con octavos
        torneo = {
            "octavos": [
                ["8", "1"],
                ["4", "5"],
                ["3", "6"],
                ["2", "7"]
            ],
            "cuartos": [
                ["Ganador 8-1", "Ganador 4-5"],
                ["Ganador 3-6", "Ganador 2-7"]
            ],
            "semis": [
                ["Ganador (8-1)-(4-5)", "Ganador (3-6)-(2-7)"]
            ],
            "final": [
                ["Ganador Semifinal 1", "Ganador Semifinal 2"]
            ]
        }
    elif num_participantes == 4:
        # Directo a semifinales
        torneo = {
            "octavos": [],
            "cuartos": [],
            "semis": [
                ["4", "1"],
                ["2", "3"]
            ],
            "final": [
                ["Ganador 4-1", "Ganador 2-3"]
            ]
        }
    elif num_participantes == 2:
        # Directo a final
        torneo = {
            "octavos": [],
            "cuartos": [],
            "semis": [],
            "final": [
                ["2", "1"]
            ]
        }
    else:
        print(f"⚠️  Advertencia: {num_participantes} participantes no es óptimo para un bracket de eliminación")

    # Actualizar datos
    datos["torneo"] = torneo

    # Guardar cambios
    try:
        with open(datos_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print("✅ Torneo generado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")
        return False


if __name__ == "__main__":
    generar_torneo()