import os

# Nombre del archivo de entrada
input_file = "Practica01.py"

# Leer el contenido del archivo
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Variables para el procesamiento
current_section = None
section_content = []
output_dir = "src"
os.makedirs(output_dir, exist_ok=True)

for line in lines:
    if line.startswith("# # Sección"):
        # Guardar la sección anterior si existe
        if current_section is not None:
            output_file = os.path.join(output_dir, f"seccion_{current_section}.py")
            with open(output_file, "w", encoding="utf-8") as out_f:
                out_f.writelines(section_content)
        
        # Obtener el número de sección
        current_section = line.strip().split(" ")[-1]
        section_content = [line]  # Iniciar nueva sección
    else:
        section_content.append(line)

# Guardar la última sección
if current_section is not None:
    output_file = os.path.join(output_dir, f"seccion_{current_section}.py")
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.writelines(section_content)

print(f"Secciones guardadas en la carpeta '{output_dir}'")
