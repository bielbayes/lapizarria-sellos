# Sellos del historial · LaPizarria (análisis de LaLiga)

Este repositorio existe para una sola cosa: **demostrar que no reescribimos
nuestro historial**.

Cada día publicamos aquí un *sello*: la huella criptográfica (SHA-256) del
historial completo de selecciones, encadenada con la del día anterior. Como
los commits de GitHub llevan fecha verificable, cualquiera puede comprobar
que lo que decíamos ayer sigue diciendo lo mismo hoy.

**No hace falta fiarse de nuestra palabra. Compruébalo:**

```bash
git clone https://github.com/bielbayes/lapizarria-sellos
cd lapizarria-sellos
python verificar.py
```

## Estado actual

| | |
|---|---|
| Sellos publicados | 15 |
| Selecciones en el historial | 57 |
| Último sello | `816ece9ff7dac01aa22f5fbcd3ea5c08…` |
| Fecha del último sello | 2026-08-25 |

## Cómo funciona

    sello_de_hoy = sha256(sello_de_ayer + huella_del_historial_de_hoy)

Si alguien modificara una selección del pasado, su huella cambiaría, y con
ella **todos** los sellos posteriores. La manipulación sería evidente al
comparar con lo ya publicado.

## Qué hay aquí

- `chain.jsonl` — la cadena de sellos, una línea por sello.
- `historial.json` — el histórico íntegro: cada selección con su fecha, su
  probabilidad, su cuota y la foto completa del mercado en ese instante, más
  sus resoluciones.
- `verificar.py` — el verificador, sin dependencias. Lee los dos archivos
  anteriores y comprueba toda la cadena.

## Aviso

Esto es análisis estadístico, no un servicio de pronósticos: no vendemos
picks, no hay suscripción y no enlazamos con casas de apuestas. Las apuestas
tienen un componente aleatorio irreducible y puedes perder tu dinero. +18.
[Juego responsable (DGOJ)](https://www.ordenacionjuego.es/es/juego-responsable-dgoj).
