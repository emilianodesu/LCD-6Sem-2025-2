import sys
import re
import nbformat

def generate_markdown_toc(notebook_path):
    # Carga el notebook
    nb = nbformat.read(notebook_path, as_version=4)
    toc_lines = []

    # Recorre cada celda Markdown buscando líneas que empiecen con '#'
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            for line in cell.source.splitlines():
                m = re.match(r'^(#+)\s+(.*)', line)
                if m:
                    level = len(m.group(1))       # número de '#' → nivel
                    title = m.group(2).strip()    # el texto del encabezado
                    indent = '  ' * (level - 1)   # sangrado según nivel
                    # genera un slug para el enlace
                    slug = re.sub(r'[^\w\- ]', '', title).lower().replace(' ', '-')
                    toc_lines.append(f'{indent}- [{title}](#{slug})')

    return '\n'.join(toc_lines)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python toc.py MiNotebook.ipynb")
        sys.exit(1)
    print(generate_markdown_toc(sys.argv[1]))
