#!/usr/bin/env python3
import os
import re
import sys
import nbformat
from pathlib import Path
import argparse

def slugify(text):
    """Convierte un título en un slug válido para nombre de archivo."""
    slug = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s_-]+', '_', slug)

def partition_notebook(nb_path, out_dir, header_level=1):
    # Leer el notebook
    nb = nbformat.read(nb_path, as_version=4)

    # Preparar directorio de salida
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sections = []   # lista de (slug, title, [código])
    current = ("intro", "prelude", [])  # antes del primer header
    sections.append(current)

    header_pattern = re.compile(r'^(#{%d})\s+(.*)' % header_level)

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Buscar encabezado del nivel indicado
            for line in cell.source.splitlines():
                m = header_pattern.match(line)
                if m:
                    # iniciar nueva sección
                    title = m.group(2).strip()
                    slug = slugify(title)
                    current = (slug, title, [])
                    sections.append(current)
                    break
        elif cell.cell_type == 'code':
            # agregar código al bloque actual
            current[2].append(cell.source)

    # Escribir cada sección en su propio .py
    for idx, (slug, title, code_blocks) in enumerate(sections):
        if not code_blocks:
            continue  # saltar secciones sin código
        fname = f"{idx:02d}_{slug}.py"
        out_path = out_dir / fname
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"# Sección: {title}\n\n")
            for block in code_blocks:
                f.write(block.rstrip() + "\n\n")
        print(f"  → Generado: {out_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Particiona un .ipynb en múltiples .py según encabezados Markdown."
    )
    parser.add_argument('notebook', help="Ruta al archivo .ipynb")
    parser.add_argument('-o','--outdir', default='scripts',
                        help="Directorio donde escribir los .py (por defecto: ./scripts)")
    parser.add_argument('-l','--level', type=int, default=1,
                        help="Nivel de encabezado Markdown a usar como separador (por defecto: 1)")
    args = parser.parse_args()

    if not os.path.isfile(args.notebook):
        print(f"Error: no existe el archivo {args.notebook}", file=sys.stderr)
        sys.exit(1)

    partition_notebook(args.notebook, args.outdir, header_level=args.level)
