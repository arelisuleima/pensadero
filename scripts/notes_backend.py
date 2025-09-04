#!/usr/bin/env python3

import os
import sys
import json
import uuid


# Usamos XDG_CONFIG_HOME para la portabilidad
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
NOTES_DIR = os.path.join(XDG_CONFIG_HOME, 'eww/notes')
CURRENT_FILE_PATH = os.path.join(XDG_CONFIG_HOME, 'eww/current_note_file.txt')

def get_notes_list():
    """Retorna una lista JSON con los nombres de los archivos de notas."""
    try:
        notes_files = [f for f in os.listdir(NOTES_DIR) if f.endswith('.md')]
        notes_list = []
        for file in notes_files:
            filepath = os.path.join(NOTES_DIR, file)

            # Título por defecto = nombre del archivo
            title = os.path.splitext(file)[0].replace('-', ' ').title()

            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line:  # si no está vacía
                    if first_line.startswith("#"):
                        title = first_line.lstrip("#").strip()
                    else:
                        title = first_line  # usa la primera línea tal cual
            
            # Truncar título si es muy largo
            display_title = title if len(title) <= 15 else title[:15] + "..."

            notes_list.append({
                "title": display_title,
                "filename": file
            })

        print(json.dumps(notes_list))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

        
  

def get_note_content(filename=None):
    """Retorna el contenido de una nota como texto con formato Pango."""
    
    # Si no hay filename por argumento, lee el archivo current_note_file.txt
    if not filename:
        try:
            with open(CURRENT_FILE_PATH, 'r', encoding='utf-8') as f:
                filename = f.read().strip()
        except FileNotFoundError:
            filename = "welcome.md"  # fallback
    
    # Definir el filepath aquí para usarlo en la excepción
    filepath = os.path.join(NOTES_DIR, filename)

    try:
        # Intenta leer el archivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Convertimos Markdown a símbolos y respetamos saltos de línea en Pango
           # content = content.replace('[ ]', '☐').replace('-', '●')
            content_lines = content.splitlines()
            formatted_lines = []

            for line in content_lines:
                if line.startswith('# '):
                    # Formato para el título principal
                    formatted_lines.append(f"{line[2:].strip()}\n")
                else:
                    formatted_lines.append(line)

            print(f"\n".join(formatted_lines))

    except (FileNotFoundError, IOError):
        # Esta parte se ejecuta si el archivo de la nota no existe
        
        # 1. Guarda el nombre de la nota de bienvenida en el archivo de estado
        with open(CURRENT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write("welcome.md")
        
        # 2. Llama a la función de nuevo para mostrar la nota de bienvenida
        get_note_content(filename="welcome.md")

def save_note(filename, content):
    """Guarda o actualiza una nota."""
    filepath = os.path.join(NOTES_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def new_note():
    """Crea una nueva nota con nombre único."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    new_name = f"nota-{uuid.uuid4().hex[:6]}.md"
    filepath = os.path.join(NOTES_DIR, new_name)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# 🗒️ Nota nueva \nSelecciona → Editar ← para añadir contenido a esta nota.")
    print(f"{new_name}")

def delete_note(filename):
    """Elimina la nota indicada si existe, excepto la nota de bienvenida."""
    try:
        if filename == "welcome.md":
            print("No se puede eliminar la nota de bienvenida.")
            return
        
        filepath = os.path.join(NOTES_DIR, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Nota eliminada: {filename}")
        else:
            print(f"La nota {filename} no existe.")
    except Exception as e:
        print(f"Error al borrar la nota: {e}")

def main():
    if len(sys.argv) < 2:
        # Si no se pasa argumento, mostrar nota actual
        get_note_content()
        sys.exit(0)

    command = sys.argv[1]

    if command == "list":
        get_notes_list()
    elif command == "get":
        filename = sys.argv[2] if len(sys.argv) >= 3 else None
        get_note_content(filename)
    elif command == "save" and len(sys.argv) == 4:
        save_note(sys.argv[2], sys.argv[3])
    elif command == "new":
        new_note()
    elif command == "delete" and len(sys.argv) == 3:
        delete_note(sys.argv[2])

if __name__ == "__main__":
    main()