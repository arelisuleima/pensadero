#!/usr/bin/env bash
# Script para seleccionar y registrar una nota como archivo actual para EWW

set -euo pipefail

# Primer argumento del script (ruta del archivo de nota seleccionado)
file="$1"

# Directorio de configuración de EWW 
EWW_DIR="/home/arelisuleima/.config/eww"

# Archivo donde se guardará la ruta de la nota actual
CURRENT_FILE="$EWW_DIR/current_note_file.txt"

# Guardar la ruta del archivo seleccionado en CURRENT_FILE
# -n: Evita agregar nueva línea al final
echo -n "$file" > "$CURRENT_FILE"

# Actualizar la variable en EWW con la nueva nota seleccionada
eww update current_note_file="$file"

# Forzar la actualización del widget de notas en EWW
# || true: Ignora errores si el poll falla
eww poll notes_content_pango || true
