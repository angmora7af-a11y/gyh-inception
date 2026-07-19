#!/usr/bin/env python3
"""
Generador de HTML para diagramas Mermaid (.mmd)

Convierte archivos .mmd a HTML interactivo usando Mermaid.js

Uso:
    python render_mermaid.py <archivo.mmd>              # Renderiza un archivo
    python render_mermaid.py --all                      # Renderiza todos los .mmd
    python render_mermaid.py --architecture             # Solo diagramas de architecture/
    python render_mermaid.py --output <directorio>      # Especifica directorio de salida

Autor: G&H Obras y Estructuras Metálicas
Fecha: Julio 2026
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - G&H Sistemas</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '#1A365D',
                primaryTextColor: '#FFFFFF',
                primaryBorderColor: '#1A365D',
                lineColor: '#4A5568',
                secondaryColor: '#EDF2F7',
                fontFamily: 'Montserrat, sans-serif'
            }}
        }});
    </script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #1A365D 0%, #2D3748 100%);
            color: white;
            padding: 30px 40px;
            border-bottom: 4px solid #FF9F1C;
        }}

        header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
            font-weight: 300;
        }}

        header .metadata {{
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.8;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}

        header .metadata span {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}

        .content {{
            padding: 40px;
        }}

        .diagram-container {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 30px;
            margin: 20px 0;
            border: 1px solid #e5e7eb;
            overflow-x: auto;
        }}

        .mermaid {{
            display: flex;
            justify-content: center;
            min-height: 400px;
        }}

        .actions {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: white;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #1A365D 0%, #2D3748 100%);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26, 54, 93, 0.4);
        }}

        .btn-secondary {{
            background: linear-gradient(135deg, #FF9F1C 0%, #E8910A 100%);
        }}

        .btn-secondary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 159, 28, 0.4);
        }}

        .info-box {{
            background: #EDF2F7;
            border-left: 4px solid #1A365D;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }}

        .info-box h3 {{
            color: #1A365D;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}

        .info-box p {{
            color: #4A5568;
            line-height: 1.6;
        }}

        footer {{
            background: #f9fafb;
            padding: 20px 40px;
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
            border-top: 1px solid #e5e7eb;
        }}

        footer a {{
            color: #1A365D;
            text-decoration: none;
            font-weight: 600;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}

            .actions {{
                display: none;
            }}

            header {{
                background: #1A365D;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}

        @media (max-width: 768px) {{
            header {{
                padding: 20px;
            }}

            header h1 {{
                font-size: 1.5em;
            }}

            .content {{
                padding: 20px;
            }}

            .diagram-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <div class="subtitle">G&H Obras y Estructuras Metálicas S.A.S.</div>
            <div class="metadata">
                <span>📅 Generado: {timestamp}</span>
                <span>📄 Archivo: {filename}</span>
                <span>🏢 NIT: 901.218.896-8</span>
            </div>
        </header>

        <div class="content">
            <div class="actions">
                <button class="btn btn-primary" onclick="window.print()">
                    🖨️ Imprimir / Exportar PDF
                </button>
                <button class="btn btn-secondary" onclick="downloadSVG()">
                    💾 Descargar SVG
                </button>
                <button class="btn btn-primary" onclick="zoomIn()">
                    🔍 Zoom In
                </button>
                <button class="btn btn-primary" onclick="zoomOut()">
                    🔎 Zoom Out
                </button>
                <button class="btn btn-primary" onclick="resetZoom()">
                    ↩️ Reset Zoom
                </button>
            </div>

            <div class="info-box">
                <h3>📊 Acerca de este diagrama</h3>
                <p>
                    Este diagrama forma parte de la documentación técnica del sistema de gestión de G&H.
                    Los diagramas están construidos con Mermaid.js y son interactivos.
                    Puedes hacer zoom, exportar a PDF o descargar como SVG.
                </p>
            </div>

            <div class="diagram-container" id="diagram-wrapper">
                <pre class="mermaid">
{mermaid_content}
                </pre>
            </div>

            <div class="info-box">
                <h3>💡 Consejos de uso</h3>
                <p>
                    • <strong>Zoom:</strong> Usa los botones de zoom o Ctrl + Scroll del mouse<br>
                    • <strong>Exportar PDF:</strong> Usa el botón "Imprimir" y selecciona "Guardar como PDF"<br>
                    • <strong>Descargar SVG:</strong> Formato vectorial escalable para edición<br>
                    • <strong>Navegación:</strong> Los diagramas grandes pueden tener scroll horizontal
                </p>
            </div>
        </div>

        <footer>
            <p>
                Documentación generada automáticamente por
                <a href="https://github.com/mermaid-js/mermaid" target="_blank">Mermaid.js</a>
                | G&H Obras y Estructuras Metálicas | {year}
            </p>
        </footer>
    </div>

    <script>
        let currentZoom = 1;

        function zoomIn() {{
            currentZoom += 0.1;
            applyZoom();
        }}

        function zoomOut() {{
            currentZoom = Math.max(0.3, currentZoom - 0.1);
            applyZoom();
        }}

        function resetZoom() {{
            currentZoom = 1;
            applyZoom();
        }}

        function applyZoom() {{
            const diagram = document.querySelector('#diagram-wrapper');
            diagram.style.transform = `scale(${{currentZoom}})`;
            diagram.style.transformOrigin = 'top left';
        }}

        function downloadSVG() {{
            const svg = document.querySelector('.mermaid svg');
            if (!svg) {{
                alert('Esperando a que se renderice el diagrama...');
                return;
            }}

            const svgData = new XMLSerializer().serializeToString(svg);
            const blob = new Blob([svgData], {{ type: 'image/svg+xml' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = '{filename_base}.svg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }}

        // Zoom con rueda del mouse
        document.querySelector('#diagram-wrapper').addEventListener('wheel', (e) => {{
            if (e.ctrlKey || e.metaKey) {{
                e.preventDefault();
                if (e.deltaY < 0) {{
                    zoomIn();
                }} else {{
                    zoomOut();
                }}
            }}
        }});
    </script>
</body>
</html>
"""


def read_mermaid_file(filepath):
    """Lee el contenido de un archivo .mmd"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def generate_html(mermaid_content, title, filename, output_path):
    """Genera un archivo HTML desde contenido Mermaid"""
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    year = datetime.now().year
    filename_base = Path(filename).stem

    html_content = HTML_TEMPLATE.format(
        title=title,
        timestamp=timestamp,
        filename=filename,
        mermaid_content=mermaid_content,
        year=year,
        filename_base=filename_base
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def get_title_from_filename(filename):
    """Genera un título legible desde el nombre del archivo"""
    base = Path(filename).stem
    # Remover números iniciales y guiones
    base = base.lstrip('0123456789_')
    # Reemplazar guiones bajos y guiones con espacios
    title = base.replace('_', ' ').replace('-', ' ')
    # Capitalizar palabras
    return title.title()


def find_all_mmd_files(base_path, pattern='**/*.mmd'):
    """Encuentra todos los archivos .mmd en el directorio"""
    base = Path(base_path)
    return list(base.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description='Genera HTML interactivo desde diagramas Mermaid (.mmd)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python render_mermaid.py architecture/11_flujo_completo_integracion_siigo.mmd
  python render_mermaid.py --all
  python render_mermaid.py --architecture
  python render_mermaid.py architecture/*.mmd --output ./html_output
        """
    )

    parser.add_argument('input', nargs='?', help='Archivo .mmd a convertir')
    parser.add_argument('--all', action='store_true', help='Renderizar todos los archivos .mmd')
    parser.add_argument('--architecture', action='store_true', help='Renderizar solo diagramas de architecture/')
    parser.add_argument('--sitemaps', action='store_true', help='Renderizar solo sitemaps/')
    parser.add_argument('--output', '-o', default='./html_diagrams', help='Directorio de salida (default: ./html_diagrams)')
    parser.add_argument('--title', '-t', help='Título personalizado para el HTML')

    args = parser.parse_args()

    # Determinar el directorio base (asumiendo que el script está en gyh-inception/scripts/)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent

    # Crear directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    files_to_process = []

    if args.all:
        print("🔍 Buscando todos los archivos .mmd...")
        files_to_process = find_all_mmd_files(base_dir)
    elif args.architecture:
        print("🔍 Buscando archivos .mmd en architecture/...")
        files_to_process = find_all_mmd_files(base_dir / 'architecture')
    elif args.sitemaps:
        print("🔍 Buscando archivos .mmd en sitemaps/...")
        files_to_process = find_all_mmd_files(base_dir / 'sitemaps')
    elif args.input:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = base_dir / input_path

        if input_path.exists():
            files_to_process = [input_path]
        else:
            print(f"❌ Error: Archivo no encontrado: {input_path}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if not files_to_process:
        print("⚠️  No se encontraron archivos .mmd para procesar")
        sys.exit(0)

    print(f"\n📊 Procesando {len(files_to_process)} archivo(s)...\n")

    for mmd_file in files_to_process:
        try:
            # Leer contenido
            content = read_mermaid_file(mmd_file)

            # Generar título
            title = args.title or get_title_from_filename(mmd_file.name)

            # Nombre del archivo de salida
            output_filename = mmd_file.stem + '.html'
            output_path = output_dir / output_filename

            # Generar HTML
            generate_html(content, title, mmd_file.name, output_path)

            print(f"✅ {mmd_file.name} → {output_path}")

        except Exception as e:
            print(f"❌ Error procesando {mmd_file.name}: {str(e)}")

    print(f"\n🎉 Procesamiento completado!")
    print(f"📁 Archivos HTML generados en: {output_dir.absolute()}")
    print(f"\n💡 Abre los archivos HTML en tu navegador para ver los diagramas interactivos.")


if __name__ == '__main__':
    main()
