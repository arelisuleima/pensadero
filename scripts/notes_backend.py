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
            title = os.path.splitext(file)[0].replace('-', ' ').title() # Título por defecto
            
            # Intentar leer la primera línea para encontrar el título con #
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('#'):
                        # Quita el #, espacios y saltos de línea
                        title = line.strip().lstrip('#').strip()
                        break # Ya que encontramos el título, salimos del bucle
            
            notes_list.append({
                "title": title,
                "filename": file
            })
        print(json.dumps(notes_list))
    except FileNotFoundError:
        print(json.dumps([]))

def get_note_content(filename=None):
    """Retorna el contenido de una nota como texto con formato Pango."""
    # Si no hay filename por argumento, lee el archivo current_note_file.txt
    if not filename:
        try:
            with open(CURRENT_FILE_PATH, 'r', encoding='utf-8') as f:
                filename = f.read().strip()
        except FileNotFoundError:
            filename = "welcome.md"  # fallback

    try:
        filepath = filename if os.path.isabs(filename) else os.path.join(NOTES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Convertimos Markdown a símbolos y respetamos saltos de línea en Pango
            content = content.replace('[ ]', '☐').replace('[x]', '✅')
            content_lines = content.splitlines()
            formatted_lines = []

            for line in content_lines:
                if line.startswith('# '):
                    formatted_lines.append(f"{line[2:].strip()}\n")
                elif line.startswith('## '):
                    formatted_lines.append(f"{line[3:].strip()}\n")
                else:
                    formatted_lines.append(line)

            title = os.path.splitext(filename)[0].replace('-', ' ').title()
            print(f"\n".join(formatted_lines))
    except (FileNotFoundError, IOError):
        #Muestra el mensaje cuando la nota se elimina
        print(f' La nota "{filename}" fue eliminada')

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
        f.write("# 🗒️ Nota nueva \n\nSelecciona → Editar ← para añadir contenido a esta nota.")
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