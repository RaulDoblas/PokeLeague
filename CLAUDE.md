# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PokeLeague is a static web application for managing a Pokémon league tournament. The league has two components:
- **Liga**: Swiss-style tournament where trainers compete across multiple match days
- **Torneo**: Single-elimination bracket at the end of the league

## Architecture

The application is built as a static site with a single data source:

### Core Data File: `datos.json`
This JSON file is the source of truth containing:
- `liga`: Trainer standings with `nombre`, `victorias`, `derrotas`
- `jornadas`: Array of match days, each containing matches with `local`, `visitante`, `resultado`
- `torneo`: Bracket structure with phases `octavos`, `cuartos`, `semis`, `final`
- `equipos`: Each trainer's Pokemon team
- `pokes`: Mapping of Pokemon names to sprite URLs

All HTML pages fetch `datos.json` via JavaScript and render the content dynamically.

### Pages
- `index.html`: League standings table + tournament bracket display
- `jornadas.html`: All match days with results
- `equipos.html`: Trainer teams with Pokemon sprites
- `reglas.html`: League rules

## Development Commands

### Generate new match days
- `python generar_jornada_normal.py` - Random match generation (checks if previous jornada is complete)
- `python generar_jornada.py` - Swiss-optimized match generation using backtracking

Both scripts read/write `datos.json`.

### Automation
GitHub Action (`.github/workflows/auto-jornada.yml`) runs daily at 08:00 to generate new match days using `generar_jornada_normal.py`.

## Important Implementation Notes

### Match Generation
- Scripts track previous matchups to avoid repeating pairs
- `generar_jornada_normal.py` checks if the last jornada has all results (not "-") before generating a new one
- `generar_jornada.py` uses backtracking to find optimal pairings minimizing win difference between opponents

### Tournament Bracket Display
The bracket uses a CSS grid with 4 columns (rounds). Round heights are defined in `alturas` object:
- `octavos`: 8 slots
- `cuartos`: 4 slots
- `semis`: 2 slots
- `final`: 1 slot

Matches span multiple grid rows to create visual spacing between rounds.

### Data Updates
When updating `datos.json`:
- Keep the JSON structure intact
- For new jornadas, use format: `{"local": "name", "visitante": "name", "resultado": "X - Y"}`
- Tournament bracket references can use placeholders like "Ganador X-Y" for TBC matches