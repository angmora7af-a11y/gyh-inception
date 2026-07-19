#!/usr/bin/env python3
"""
Generador de HTML para toda la documentación GYH Inception
Genera un Inception Report completo similar a GYH_InceptionReportV6.HTML
Incluye diccionario completo de base de datos parseado desde DBML

Uso:
    python generate_docs_html.py
    python generate_docs_html.py --output ./html_output

Autor: G&H Obras y Estructuras Metálicas
Fecha: Julio 2026
"""

import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime


def read_mermaid_file(filepath):
    """Lee el contenido de un archivo .mmd"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer {filepath}: {str(e)}"


def parse_dbml(filepath):
    """
    Parsea el archivo DBML y extrae enumeraciones y tablas
    Retorna: (enums_dict, tables_list, dbml_content)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    enums = {}
    tables = []

    # Extraer enumeraciones
    enum_pattern = r'Enum\s+(\w+)\s*\{([^}]+)\}'
    for match in re.finditer(enum_pattern, content, re.DOTALL):
        enum_name = match.group(1)
        enum_body = match.group(2)

        # Extraer valores
        values = []
        for line in enum_body.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('//'):
                # Quitar comentarios inline
                value = line.split('[')[0].strip()
                if value:
                    values.append(value)

        enums[enum_name] = values

    # Extraer tablas
    table_pattern = r'Table\s+(\w+)\s*\{([^}]+)\}'
    for match in re.finditer(table_pattern, content, re.DOTALL):
        table_name = match.group(1)
        table_body = match.group(2)

        # Extraer note de la tabla
        table_note = ""
        note_match = re.search(r'Note:\s*[\'"]([^\'"]+)[\'"]', table_body)
        if note_match:
            table_note = note_match.group(1)

        # Extraer columnas
        columns = []
        for line in table_body.split('\n'):
            line = line.strip()
            # Buscar líneas que definen columnas: nombre tipo [constraints]
            col_match = re.match(r'(\w+)\s+(\w+(?:\([^)]+\))?)\s*(\[.*\])?', line)
            if col_match and not line.startswith('Note:') and not line.startswith('//'):
                col_name = col_match.group(1)
                col_type = col_match.group(2)
                constraints = col_match.group(3) or ''

                # Determinar badges
                badges = []
                if 'pk' in constraints.lower() or 'primary key' in constraints.lower():
                    badges.append('PK')
                if 'ref:' in constraints or '> ' in line:
                    badges.append('FK')
                if 'unique' in constraints.lower():
                    badges.append('UQ')
                if 'not null' in constraints.lower():
                    badges.append('NN')

                columns.append({
                    'name': col_name,
                    'type': col_type,
                    'badges': badges
                })

        if columns:  # Solo agregar si tiene columnas
            tables.append({
                'name': table_name,
                'note': table_note,
                'columns': columns,
                'column_count': len(columns)
            })

    return enums, tables, content


def generate_enum_pills_html(enums):
    """Genera el HTML para las pills de enumeraciones"""
    html_parts = []

    for enum_name, values in enums.items():
        # Mostrar primeros valores + count si son muchos
        if len(values) > 6:
            display_vals = ', '.join(values[:6]) + f' +{len(values)-6}'
        else:
            display_vals = ', '.join(values)

        html_parts.append(f'''<div class="enum-pill"><strong>{enum_name}</strong><span class="enum-vals">{display_vals}</span></div>''')

    return '\n'.join(html_parts)


def generate_table_cards_html(tables):
    """Genera el HTML para las tarjetas de tablas"""
    html_parts = []

    # Colores por módulo (basado en nombre de tabla)
    module_colors = {
        'usuarios': '#0B3C5D',
        'auditoria': '#0B3C5D',
        'notificaciones': '#0B3C5D',
        'clientes': '#2C7A7B',
        'contactos': '#2C7A7B',
        'obras': '#2C7A7B',
        'frentes': '#2C7A7B',
        'referencias': '#2C7A7B',
        'accionistas': '#2C7A7B',
        'autorizacion': '#2C7A7B',
        'aprobaciones': '#2C7A7B',
        'documentos': '#2C7A7B',
        'cotizaciones': '#553C9A',
        'cotizacion': '#553C9A',
        'archivos_planos': '#553C9A',
        'contratos': '#6B46C1',
        'ordenes_compra': '#6B46C1',
        'catalogo': '#276749',
        'kardex': '#276749',
        'pedidos': '#276749',
        'pedido': '#276749',
        'remisiones': '#276749',
        'remision': '#276749',
        'vehiculos': '#276749',
        'conductores': '#276749',
        'conductor': '#276749',
        'cronograma': '#276749',
        'equipos': '#276749',
        'agenda': '#276749',
        'consumibles': '#276749',
        'config': '#276749',
        'evaluacion': '#276749',
        'bodegas': '#276749',
        'facturas': '#744210',
        'factura': '#744210',
        'proformas': '#744210',
        'proforma': '#744210',
        'pagos': '#744210',
        'cartera': '#744210',
        'retenciones': '#744210',
    }

    def get_table_color(table_name):
        """Determina el color basado en el nombre de la tabla"""
        table_lower = table_name.lower()
        for key, color in module_colors.items():
            if key in table_lower:
                return color
        return '#4A5568'  # Color por defecto

    for table in tables:
        color = get_table_color(table['name'])

        # Primeras 7 columnas
        cols_to_show = min(7, len(table['columns']))
        cols_html = []

        for col in table['columns'][:cols_to_show]:
            badges_html = ''.join([
                f'<span class="badge {badge.lower()}">{badge}</span>'
                for badge in col['badges']
            ])
            cols_html.append(
                f'<tr><td><code>{col["name"]}</code></td>'
                f'<td class="t-type">{col["type"]}</td>'
                f'<td>{badges_html}</td></tr>'
            )

        cols_table = '<table class="t-cols"><tbody>' + ''.join(cols_html) + '</tbody></table>'

        # Mensaje de columnas adicionales
        remaining = table['column_count'] - cols_to_show
        more_msg = f'<p class="t-more">+ {remaining} columnas más</p>' if remaining > 0 else ''

        card_html = f'''<div class="t-card" style="--tcolor:{color}">
  <div class="t-head">
    <span class="t-name">{table['name']}</span>
    <span class="t-count">{table['column_count']} cols</span>
  </div>
  <p class="t-note">{table['note']}</p>
  {cols_table}
  {more_msg}
</div>'''

        html_parts.append(card_html)

    return '\n'.join(html_parts)


def parse_markdown_table(md_content):
    """
    Convierte tablas markdown a HTML
    Retorna el contenido con tablas convertidas
    """
    html_content = md_content

    # Convertir horizontal rules
    html_content = re.sub(r'^---+\s*$', r'<hr>', html_content, flags=re.MULTILINE)

    # Convertir headers (##, ###)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convertir blockquotes
    html_content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)

    # Convertir bold text (**text**)
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # Convertir párrafos normales (líneas que no son headers ni tablas)
    def wrap_paragraph(text):
        lines = text.split('\n')
        result = []
        in_paragraph = False
        paragraph_lines = []
        in_table = False

        for line in lines:
            stripped = line.strip()

            # Track if we're inside a table
            if '<div class="table-wrap">' in line:
                in_table = True
            if '</div>' in line and in_table:
                in_table = False
                # Add the closing div and continue
                if in_paragraph and paragraph_lines:
                    result.append('<p>' + ' '.join(paragraph_lines) + '</p>')
                    paragraph_lines = []
                    in_paragraph = False
                result.append(line)
                continue

            # Skip if it's a header, blockquote, table, or hr
            if (in_table or
                stripped.startswith('<h') or
                stripped.startswith('<blockquote') or
                stripped.startswith('<hr') or
                stripped.startswith('<div class="table-wrap') or
                stripped.startswith('<table>') or
                stripped.startswith('<thead') or
                stripped.startswith('<tbody') or
                stripped.startswith('<tr') or
                stripped.startswith('<td') or
                stripped.startswith('<th') or
                stripped.startswith('</table') or
                stripped.startswith('</thead') or
                stripped.startswith('</tbody') or
                stripped.startswith('</tr') or
                stripped.endswith('</h1>') or
                stripped.endswith('</h2>') or
                stripped.endswith('</h3>') or
                stripped.startswith('|') or
                not stripped):

                if in_paragraph and paragraph_lines:
                    result.append('<p>' + ' '.join(paragraph_lines) + '</p>')
                    paragraph_lines = []
                    in_paragraph = False
                result.append(line)
            else:
                paragraph_lines.append(stripped)
                in_paragraph = True

        if paragraph_lines:
            result.append('<p>' + ' '.join(paragraph_lines) + '</p>')

        return '\n'.join(result)

    # Convertir tablas markdown a HTML
    lines = html_content.split('\n')
    in_table = False
    table_html = []
    result = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detectar inicio de tabla (línea con |)
        if '|' in line and not in_table:
            in_table = True
            table_html = ['<div class="table-wrap">', '<table>', '<thead>', '<tr>']

            # Header row
            headers = [h.strip() for h in line.split('|') if h.strip()]
            for h in headers:
                # Process markdown in header content
                header_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h)
                table_html.append(f'<th>{header_content}</th>')
            table_html.append('</tr>')
            table_html.append('</thead>')

            # Skip separator line (|---|---|)
            i += 1
            if i < len(lines):
                i += 1  # Skip separator
                table_html.append('<tbody>')
                continue

        elif '|' in line and in_table:
            # Data row
            cells = [c.strip() for c in line.split('|') if c.strip()]
            table_html.append('<tr>')
            for c in cells:
                # Process markdown in cell content (bold, etc.)
                cell_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', c)
                table_html.append(f'<td>{cell_content}</td>')
            table_html.append('</tr>')
            i += 1
            continue

        elif in_table and not line:
            # End of table
            table_html.append('</tbody>')
            table_html.append('</table>')
            table_html.append('</div>')
            result.append('\n'.join(table_html))
            table_html = []
            in_table = False
            i += 1
            continue

        else:
            # Regular line
            if not in_table:
                result.append(line)
            i += 1

    # Close table if still open
    if in_table and table_html:
        table_html.append('</tbody>')
        table_html.append('</table>')
        table_html.append('</div>')
        result.append('\n'.join(table_html))

    # Wrap paragraphs
    result_text = '\n'.join(result)
    result_text = wrap_paragraph(result_text)

    return result_text


def parse_roles_permissions(filepath):
    """Lee y parsea el archivo de roles y permisos a HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return parse_markdown_table(content)


def parse_notifications(filepath):
    """Lee y parsea el archivo de notificaciones a HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return parse_markdown_table(content)


def main():
    parser = argparse.ArgumentParser(
        description='Genera Inception Report HTML completo con diagramas embebidos'
    )
    parser.add_argument('--output', '-o', default='./html_output', help='Directorio de salida')
    args = parser.parse_args()

    # Directorios
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Timestamp
    now = datetime.now()
    timestamp_full = now.strftime("%d de %B de %Y a las %H:%M:%S")
    timestamp_short = now.strftime("%d de %B de %Y")

    # Leer todos los archivos .mmd
    print("📖 Leyendo archivos .mmd...")

    diagrams = {
        'flujo_principal': read_mermaid_file(base_dir / 'architecture/01_flujo_principal_gyh.mmd'),
        'arquitectura': read_mermaid_file(base_dir / 'architecture/02_arquitectura_sistema.mmd'),
        'cotizacion': read_mermaid_file(base_dir / 'architecture/03_modulo_cotizacion.mmd'),
        'registro_cliente': read_mermaid_file(base_dir / 'architecture/04_registro_aprobacion_cliente.mmd'),
        'inventarios': read_mermaid_file(base_dir / 'architecture/05_modulo_inventarios_logistica.mmd'),
        'roles': read_mermaid_file(base_dir / 'architecture/06_roles_y_permisos.mmd'),
        'integracion_siigo': read_mermaid_file(base_dir / 'architecture/07_integracion_siigo.mmd'),
        'kardex': read_mermaid_file(base_dir / 'architecture/08_modulo_kardex_facturacion.mmd'),
        'bodegas': read_mermaid_file(base_dir / 'architecture/09_bodegas_inventarios.mmd'),
        'validacion_dian': read_mermaid_file(base_dir / 'architecture/10_validacion_dian_radian.mmd'),
        'flujo_completo_siigo': read_mermaid_file(base_dir / 'architecture/11_flujo_completo_integracion_siigo.mmd'),

        # Sitemaps
        'sitemap_principal': read_mermaid_file(base_dir / 'sitemaps/sitemap_gyh_app.mmd'),
        'sitemap_auth': read_mermaid_file(base_dir / 'sitemaps/sitemap_01_auth_dashboard.mmd'),
        'sitemap_clientes': read_mermaid_file(base_dir / 'sitemaps/sitemap_02_clientes.mmd'),
        'sitemap_cotizaciones': read_mermaid_file(base_dir / 'sitemaps/sitemap_03_cotizaciones.mmd'),
        'sitemap_contratos': read_mermaid_file(base_dir / 'sitemaps/sitemap_04_contratos.mmd'),
        'sitemap_inventarios': read_mermaid_file(base_dir / 'sitemaps/sitemap_05_inventarios.mmd'),
        'sitemap_facturacion': read_mermaid_file(base_dir / 'sitemaps/sitemap_06_facturacion.mmd'),
        'sitemap_auditoria': read_mermaid_file(base_dir / 'sitemaps/sitemap_07_auditoria_config.mmd'),
    }

    # Parsear DBML
    print("📊 Parseando esquema de base de datos...")
    dbml_path = base_dir / 'database/gyh_schema.dbml'
    enums, tables, dbml_content = parse_dbml(dbml_path)

    enum_pills_html = generate_enum_pills_html(enums)
    table_cards_html = generate_table_cards_html(tables)

    # Parsear roles y permisos
    print("👥 Parseando roles y permisos...")
    roles_permissions_path = base_dir / 'architecture/06_roles_y_permisos_tabla.md'
    roles_permissions_html = parse_roles_permissions(roles_permissions_path)

    # Parsear notificaciones
    print("🔔 Parseando notificaciones...")
    notifications_path = base_dir / 'follow/notificaciones.md'
    notifications_html = parse_notifications(notifications_path)

    # Escapar contenido DBML para HTML
    dbml_content_escaped = (dbml_content
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#x27;')
    )

    print(f"   ✓ {len(enums)} enumeraciones encontradas")
    print(f"   ✓ {len(tables)} tablas encontradas")

    # Generar HTML
    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>G&H Sistema — Inception Report 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'base',
      securityLevel: 'loose',
      themeVariables: {{
        primaryColor: '#0B3C5D',
        primaryTextColor: '#FFFFFF',
        primaryBorderColor: '#0B3C5D',
        lineColor: '#333333',
        secondaryColor: '#F2F2F2',
        clusterBkg: '#072B44',
        clusterBorder: '#0B3C5D',
        titleColor: '#FFFFFF',
        edgeLabelBackground: '#F9F9F9',
        fontFamily: 'Montserrat, sans-serif'
      }}
    }});

    /* ── SVG download helper ── */
    function downloadSVG(svgEl, filename) {{
      const clone = svgEl.cloneNode(true);
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
      const styles = Array.from(document.styleSheets)
        .flatMap(s => {{ try {{ return Array.from(s.cssRules); }} catch {{ return []; }} }})
        .map(r => r.cssText).join('\\n');
      const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
      styleEl.textContent = styles;
      clone.insertBefore(styleEl, clone.firstChild);
      const src = '<?xml version="1.0" encoding="UTF-8"?>\\n' +
                  new XMLSerializer().serializeToString(clone);
      const blob = new Blob([src], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url  = URL.createObjectURL(blob);
      const a    = Object.assign(document.createElement('a'), {{ href: url, download: filename }});
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1500);
    }}

    /* ── Render Mermaid + wire download buttons + ScrollSpy ── */
    document.addEventListener('DOMContentLoaded', async () => {{

      /* Render all mermaid blocks */
      const blocks = document.querySelectorAll('pre.mermaid');
      for (let i = 0; i < blocks.length; i++) {{
        const el   = blocks[i];
        const code = el.textContent.trim();
        const id   = 'mmd-gyh-' + i;
        try {{
          const {{ svg }} = await mermaid.render(id, code);
          const wrap = document.createElement('div');
          wrap.className = 'mmd-svg-wrap';
          wrap.innerHTML = svg;
          el.replaceWith(wrap);
        }} catch(err) {{
          const errEl = document.createElement('div');
          errEl.style.cssText = 'padding:1rem;background:#fef2f2;border-radius:8px;color:#b91c1c;font-size:.82rem;border:1px solid #fca5a5;';
          errEl.innerHTML = '<strong>Error al renderizar diagrama:</strong><br>' + (err.message || String(err));
          el.replaceWith(errEl);
        }}
      }}

      /* Wire download buttons */
      document.querySelectorAll('.btn-dl-svg').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const wrapEl = document.getElementById(btn.dataset.wrap);
          if (!wrapEl) return;
          const svgEl = wrapEl.querySelector('svg');
          if (!svgEl) {{
            btn.textContent = '⏳ Cargando…';
            setTimeout(() => {{ btn.textContent = '⬇ Descargar SVG'; }}, 1500);
            return;
          }}
          btn.classList.add('loading');
          btn.textContent = '⏳ Generando…';
          setTimeout(() => {{
            try {{
              downloadSVG(svgEl, btn.dataset.filename);
              btn.textContent = '✓ Descargado';
              setTimeout(() => {{
                btn.textContent = '⬇ Descargar SVG';
                btn.classList.remove('loading');
              }}, 1800);
            }} catch(e) {{
              btn.textContent = '⬇ Descargar SVG';
              btn.classList.remove('loading');
            }}
          }}, 80);
        }});
      }});

      /* ScrollSpy — resalta el link activo en el sidebar */
      const navLinks = document.querySelectorAll('nav a[href^="#"]');
      const sections = document.querySelectorAll('section[id]');
      const spy = new IntersectionObserver(entries => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            navLinks.forEach(a => a.classList.remove('active'));
            const hit = document.querySelector('nav a[href="#' + entry.target.id + '"]');
            if (hit) {{
              hit.classList.add('active');
              hit.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
            }}
          }}
        }});
      }}, {{ threshold: 0.18, rootMargin: '-5% 0px -65% 0px' }});
      sections.forEach(s => spy.observe(s));
    }});
  </script>
  <style>
/* ── Google Fonts se cargan en el <head> vía <link> ── */

:root {{
  /* Color tokens — GYH Bogotá Design System */
  --bg:       #F9F9F9;
  --surface:  #FFFFFF;
  --surface2: #F2F2F2;
  --border:   #E0E0E0;
  --text:     #1A1A1A;
  --muted:    #777777;
  --primary:  #0B3C5D;
  --primary2: #328CC1;
  --accent:   #F5A623;
  --accent2:  #D4901F;
  --steel:    #333333;
  --grey-300: #CCCCCC;
  --grey-900: #1C1C1C;
  --nav-dark: #072B44;
  --success:  #38A169;
  --danger:   #E53E3E;
  --nav-w:    270px;
  --shadow-low: 0px 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-med: 0px 4px 10px rgba(0, 0, 0, 0.12);
  --r-sm: 4px;
  --r-md: 8px;
  --r-lg: 12px;
  --transition-fast:   200ms ease-in-out;
  --transition-normal: 350ms ease;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Open Sans', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.65;
  font-size: 15px;
}}

/* ── Layout ── */
.layout {{ display: grid; grid-template-columns: var(--nav-w) 1fr; min-height: 100vh; }}
@media (max-width: 960px) {{
  .layout {{ grid-template-columns: 1fr; }}
  nav {{ position: relative; height: auto; width: 100%; }}
}}

/* ── Sidebar ── */
nav {{
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  background: var(--primary);
  color: #fff;
  padding: 0 0 2rem;
  font-size: .82rem;
  box-shadow: var(--shadow-med);
  font-family: 'Open Sans', system-ui, sans-serif;
}}
.nav-brand {{
  display: flex; align-items: center; gap: .75rem;
  padding: 1.25rem 1rem;
  background: var(--nav-dark);
  border-bottom: 1px solid rgba(255,255,255,.1);
  margin-bottom: .5rem;
}}
.nav-logo {{
  background: var(--accent);
  color: var(--primary);
  font-family: 'Montserrat', system-ui, sans-serif;
  font-weight: 900;
  font-size: 1.1rem;
  padding: .3rem .55rem;
  border-radius: var(--r-sm);
  line-height: 1;
  flex-shrink: 0;
  letter-spacing: -.02em;
}}
.nav-brand strong {{
  display: block;
  color: #fff;
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: .85rem;
  font-weight: 700;
  line-height: 1.3;
}}
.nav-brand small {{ color: rgba(255,255,255,.45); font-size: .68rem; }}
.nav-group {{
  font-size: .6rem;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: rgba(255,255,255,.35);
  padding: 1rem 1rem .3rem;
  font-family: 'Montserrat', system-ui, sans-serif;
  font-weight: 600;
}}
.nav-divider {{
  border-top: 1px solid rgba(255,255,255,.08);
  margin: .75rem 0;
}}
nav a {{
  display: block;
  padding: .4rem 1rem;
  color: rgba(255,255,255,.68);
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all var(--transition-fast);
}}
nav a:hover,
nav a.active {{
  color: var(--accent);
  background: rgba(255,255,255,.07);
  border-left-color: var(--accent);
}}

/* ── Main ── */
main {{
  padding: 2rem 2.5rem 4rem;
  background: var(--bg);
  max-width: 1200px;
}}
@media (max-width: 720px) {{ main {{ padding: 1rem 1rem 3rem; }} }}

/* ── Hero ── */
.hero {{
  background: linear-gradient(135deg, var(--primary) 0%, #0E5080 100%);
  color: #fff;
  border-radius: var(--r-lg);
  padding: 2.5rem 2rem;
  margin-bottom: 2.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-med);
}}
.hero::before {{
  content: '';
  position: absolute; right: -80px; top: -80px;
  width: 260px; height: 260px;
  border-radius: 50%;
  background: rgba(245,166,35,.12);
  pointer-events: none;
}}
.hero::after {{
  content: '';
  position: absolute; right: 40px; bottom: -40px;
  width: 140px; height: 140px;
  border-radius: 50%;
  background: rgba(255,255,255,.06);
  pointer-events: none;
}}
.hero-tag {{
  font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  color: var(--accent);
  font-weight: 700;
  margin-bottom: .5rem;
  font-family: 'Montserrat', system-ui, sans-serif;
}}
.hero h1 {{
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: .4rem;
  letter-spacing: -.02em;
}}
.hero p {{ color: rgba(255,255,255,.62); font-size: .92rem; }}
.hero-meta {{ display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1.5rem; }}
.hero-chip {{
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;
  padding: .22rem .72rem;
  font-size: .73rem;
  color: rgba(255,255,255,.85);
}}

/* ── Sections ── */
section {{ margin-bottom: 3.5rem; scroll-margin-top: 1rem; }}
.section-header {{ margin-bottom: 1.5rem; padding-bottom: .7rem; border-bottom: 3px solid var(--accent); }}
.section-header h2 {{
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 1.4rem;
  color: var(--primary);
  font-weight: 800;
  letter-spacing: -.01em;
}}
.section-sub {{ color: var(--muted); font-size: .84rem; margin-top: .3rem; }}
section h3 {{
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 1rem;
  color: var(--primary);
  margin: 1.75rem 0 .75rem;
  font-weight: 700;
}}

/* ── Diagrams ── */
.diagram-block {{
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--shadow-low);
  margin-bottom: 1rem;
}}
.diagram-label {{
  background: var(--primary);
  color: rgba(255,255,255,.72);
  padding: .42rem 1rem;
  font-size: .7rem;
  font-family: ui-monospace, monospace;
  letter-spacing: .04em;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .75rem;
}}
.btn-dl-svg {{
  flex-shrink: 0;
  background: var(--accent);
  color: var(--primary);
  border: none;
  border-radius: var(--r-sm);
  padding: .28rem .75rem;
  font-size: .7rem;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Montserrat', system-ui, sans-serif;
  letter-spacing: .02em;
  transition: background var(--transition-fast), transform var(--transition-fast);
}}
.btn-dl-svg:hover {{ background: var(--accent2); transform: translateY(-1px); }}
.btn-dl-svg:active {{ transform: translateY(0); }}
.btn-dl-svg.loading {{ opacity: .6; cursor: wait; }}
.mermaid-wrap {{ padding: 1.5rem; overflow-x: auto; background: #fff; min-height: 80px; }}
.mmd-svg-wrap svg {{ max-width: 100%; height: auto; }}

/* ── Metrics ── */
.metrics-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
  gap: .9rem;
  margin-bottom: 1.5rem;
}}
.metric-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.2rem 1rem;
  text-align: center;
  border-top: 4px solid var(--accent);
  box-shadow: var(--shadow-low);
  transition: box-shadow var(--transition-fast);
}}
.metric-card:hover {{ box-shadow: var(--shadow-med); }}
.metric-icon {{ display: block; font-size: 1.65rem; margin-bottom: .45rem; }}
.metric-value {{
  display: block;
  font-size: 1.65rem;
  font-weight: 900;
  color: var(--primary);
  font-family: 'Montserrat', system-ui, sans-serif;
  letter-spacing: -.02em;
}}
.metric-label {{ display: block; font-size: .66rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; margin-top: .2rem; }}

/* ── Info cards ── */
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }}
@media (max-width: 680px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
.info-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.5rem;
  box-shadow: var(--shadow-low);
}}
.info-card h3 {{
  font-size: 1rem;
  color: var(--primary);
  margin: 0 0 1rem;
  font-weight: 700;
}}
.info-card ul {{ list-style: none; }}
.info-card ul li {{
  padding: .4rem 0;
  border-bottom: 1px solid var(--surface2);
  font-size: .88rem;
}}
.info-card ul li:last-child {{ border-bottom: none; }}
.mod-badge {{
  display: inline-block;
  background: var(--accent);
  color: var(--primary);
  font-size: .68rem;
  font-weight: 700;
  padding: .15rem .4rem;
  border-radius: var(--r-sm);
  margin-right: .5rem;
  font-family: 'Montserrat', system-ui, sans-serif;
}}
.stack-tag {{
  display: inline-block;
  font-size: .68rem;
  font-weight: 700;
  padding: .18rem .5rem;
  border-radius: var(--r-sm);
  margin-right: .5rem;
  font-family: 'Montserrat', system-ui, sans-serif;
}}
.stack-tag.fe {{ background: #3182CE; color: #fff; }}
.stack-tag.be {{ background: #38A169; color: #fff; }}
.stack-tag.db {{ background: #DD6B20; color: #fff; }}
.stack-tag.ex {{ background: #805AD5; color: #fff; }}

.roles-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: .6rem;
}}
.role-chip {{
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: .5rem .75rem;
  text-align: center;
  font-size: .78rem;
  font-weight: 600;
}}
.role-chip.admin {{ background: #FED7D7; border-color: #FC8181; color: #9B2C2C; }}
.role-chip.ceo {{ background: #C6F6D5; border-color: #68D391; color: #22543D; }}

.callout {{
  background: #EBF8FF;
  border-left: 4px solid #3182CE;
  padding: 1rem 1.25rem;
  border-radius: var(--r-sm);
  font-size: .88rem;
  line-height: 1.6;
}}
.callout.warn {{
  background: #FFFAF0;
  border-left-color: #DD6B20;
}}
.callout strong {{ color: var(--primary); }}

/* ── Database Styles ── */
.db-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  font-size: .82rem;
}}
.db-legend span {{
  padding: .3rem .7rem;
  border-radius: var(--r-sm);
  border: 2px solid;
  font-weight: 600;
}}

.enum-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: .7rem;
  margin-bottom: 2rem;
}}
.enum-pill {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: .6rem .9rem;
  font-size: .8rem;
}}
.enum-pill strong {{
  display: block;
  color: var(--primary);
  font-family: 'Montserrat', sans-serif;
  margin-bottom: .3rem;
}}
.enum-vals {{
  color: var(--muted);
  font-size: .74rem;
}}

.t-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}}
.t-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  overflow: hidden;
  box-shadow: var(--shadow-low);
  transition: box-shadow var(--transition-fast);
}}
.t-card:hover {{ box-shadow: var(--shadow-med); }}
.t-head {{
  background: var(--tcolor, var(--primary));
  color: #fff;
  padding: .55rem .9rem;
  display: flex;
  align-items: center;
  gap: .5rem;
}}
.t-name {{
  font-weight: 700;
  font-size: .84rem;
  flex: 1;
  font-family: ui-monospace, monospace;
}}
.t-count {{
  font-size: .64rem;
  color: rgba(255,255,255,.6);
  background: rgba(255,255,255,.12);
  padding: .1rem .4rem;
  border-radius: 3px;
}}
.t-note {{
  font-size: .72rem;
  color: var(--muted);
  padding: .45rem .8rem;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  line-height: 1.4;
}}
.t-cols {{
  width: 100%;
  border-collapse: collapse;
  font-size: .75rem;
}}
.t-cols td {{
  padding: .3rem .8rem;
  border-bottom: 1px solid var(--surface2);
}}
.t-cols tr:last-child td {{ border-bottom: none; }}
.t-cols code {{
  font-family: ui-monospace, monospace;
  color: var(--steel);
  font-weight: 600;
}}
.t-type {{
  color: var(--muted);
  font-family: ui-monospace, monospace;
}}
.t-more {{
  padding: .4rem .8rem;
  font-size: .72rem;
  color: var(--muted);
  font-style: italic;
  background: var(--surface);
}}

.badge {{
  display: inline-block;
  font-size: .6rem;
  font-weight: 700;
  padding: .15rem .35rem;
  border-radius: var(--r-sm);
  margin-left: .3rem;
  font-family: 'Montserrat', sans-serif;
}}
.badge.pk {{ background: #2C7A7B; color: #fff; }}
.badge.fk {{ background: #805AD5; color: #fff; }}
.badge.uq {{ background: #DD6B20; color: #fff; }}
.badge.nn {{ background: #4A5568; color: #fff; }}

.code-block {{
  background: #1E1E1E;
  color: #D4D4D4;
  padding: 1.5rem;
  border-radius: var(--r-md);
  overflow-x: auto;
  font-family: ui-monospace, monospace;
  font-size: .8rem;
  line-height: 1.5;
  max-height: 600px;
  overflow-y: auto;
}}

details {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1rem;
  margin: 1rem 0;
}}
details summary {{
  cursor: pointer;
  font-weight: 700;
  color: var(--primary);
  padding: .5rem;
  user-select: none;
}}
details summary:hover {{
  background: var(--surface2);
  border-radius: var(--r-sm);
}}
details[open] summary {{
  margin-bottom: 1rem;
}}

/* ── Markdown Content Tables ── */
.md-content {{
  line-height: 1.8;
}}
.md-content h1 {{
  font-size: 1.8rem;
  margin: 2rem 0 1rem;
  color: var(--primary);
}}
.md-content h2 {{
  font-size: 1.4rem;
  margin: 1.8rem 0 1rem;
  color: var(--steel);
  border-bottom: 2px solid var(--border);
  padding-bottom: .5rem;
}}
.md-content h3 {{
  font-size: 1.1rem;
  margin: 1.5rem 0 .8rem;
  color: var(--steel);
}}
.md-content p {{
  margin: 1rem 0;
}}
.md-content blockquote {{
  background: var(--surface2);
  border-left: 4px solid var(--primary);
  padding: .8rem 1.2rem;
  margin: 1rem 0;
  font-style: italic;
  color: var(--muted);
}}
.md-content strong {{
  color: var(--primary);
  font-weight: 700;
}}

.table-wrap {{
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  background: var(--surface);
}}
.table-wrap table {{
  width: 100%;
  border-collapse: collapse;
  font-size: .85rem;
}}
.table-wrap thead {{
  background: var(--primary);
  color: #fff;
}}
.table-wrap th {{
  padding: .8rem;
  text-align: left;
  font-weight: 700;
  font-size: .8rem;
  border-right: 1px solid rgba(255,255,255,.1);
}}
.table-wrap th:last-child {{
  border-right: none;
}}
.table-wrap td {{
  padding: .7rem .8rem;
  border-bottom: 1px solid var(--border);
  border-right: 1px solid var(--surface2);
}}
.table-wrap td:last-child {{
  border-right: none;
}}
.table-wrap tr:last-child td {{
  border-bottom: none;
}}
.table-wrap tbody tr:hover {{
  background: var(--surface2);
}}

/* ── Footer ── */
footer {{
  background: var(--grey-900);
  color: rgba(255,255,255,.7);
  padding: 2rem;
  text-align: center;
  font-size: .82rem;
  border-top: 3px solid var(--accent);
}}
footer p {{ margin: .3rem 0; }}
footer strong {{ color: var(--accent); }}

/* ── Print ── */
@media print {{
  nav {{ display: none; }}
  .layout {{ grid-template-columns: 1fr; }}
  .hero {{ background: var(--primary); -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .btn-dl-svg {{ display: none; }}
}}
  </style>
</head>
<body>

<div class="layout">

<!-- ═══════════════ SIDEBAR ═══════════════ -->
<nav>
  <div class="nav-brand">
    <span class="nav-logo">G&H</span>
    <div>
      <strong>Sistema de Gestión</strong>
      <small>Inception Report · 2026</small>
    </div>
  </div>

  <div class="nav-group">Visión General</div>
  <a href="#overview">📊 Resumen Ejecutivo</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Diagramas de Arquitectura</div>
  <a href="#flujo-principal">🔄 Flujo Principal GYH</a>
  <a href="#arquitectura">🏗️ Arquitectura del Sistema</a>
  <a href="#cotizacion">📋 Módulo de Cotizaciones</a>
  <a href="#registro-cliente">✅ Registro y Aprobación Cliente</a>
  <a href="#inventarios-logistica">📦 Inventarios y Logística</a>
  <a href="#roles-permisos">👥 Roles y Permisos</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Facturación e Integración</div>
  <a href="#integracion-siigo">🔗 Integración Siigo/DIAN</a>
  <a href="#kardex">📊 Kardex y Facturación</a>
  <a href="#bodegas">🏭 Bodegas e Inventarios</a>
  <a href="#validacion-dian">✅ Validación DIAN/Radian</a>
  <a href="#flujo-completo-siigo">🎯 Flujo Completo Siigo</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Mapas de Pantallas</div>
  <a href="#sitemap-principal">🗺️ Sitemap Principal</a>
  <a href="#sitemap-auth">🔐 Auth · Dashboard</a>
  <a href="#sitemap-clientes">👥 Clientes</a>
  <a href="#sitemap-cotizaciones">📋 Cotizaciones</a>
  <a href="#sitemap-contratos">📝 Contratos</a>
  <a href="#sitemap-inventarios">📦 Inventarios</a>
  <a href="#sitemap-facturacion">💳 Facturación · Cartera</a>
  <a href="#sitemap-auditoria">🔍 Auditoría · Config</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Arquitectura Técnica</div>
  <a href="#notificaciones">🔔 Notificaciones</a>
  <a href="#database">🗄️ Esquema de Base de Datos</a>
</nav>

<!-- ═══════════════ MAIN ═══════════════ -->
<main>

  <header class="hero">
    <p class="hero-tag">Fase de Inception · Documentación Técnica · G&H Obras y Estructuras Metálicas S.A.S</p>
    <h1>Sistema de Gestión G&H</h1>
    <p>Cotizaciones · Clientes · Contratos · Inventarios · Facturación · Auditoría</p>
    <div class="hero-meta">
      <span class="hero-chip">📅 {timestamp_short}</span>
      <span class="hero-chip">🗄️ {len(tables)} tablas PostgreSQL</span>
      <span class="hero-chip">📊 11 diagramas arquitectura</span>
      <span class="hero-chip">👤 13 roles del sistema</span>
      <span class="hero-chip">🗺️ 7 sitemaps por módulo</span>
      <span class="hero-chip">🆕 Julio 2026 actualizado</span>
    </div>
  </header>


<section id="overview">
  <div class="section-header">
    <h2>Resumen Ejecutivo del Proyecto</h2>
    <p class="section-sub">G&H Obras y Estructuras Metálicas S.A.S · NIT: 901.218.896-8 · Bogotá · Actualizado Julio 2026</p>
  </div>

  <div class="metrics-grid">
    <div class="metric-card"><span class="metric-icon">🏗️</span><span class="metric-value">~180</span><span class="metric-label">Clientes (migración)</span></div>
    <div class="metric-card"><span class="metric-icon">🏢</span><span class="metric-value">50</span><span class="metric-label">Obras / cliente</span></div>
    <div class="metric-card"><span class="metric-icon">🔧</span><span class="metric-value">3–4</span><span class="metric-label">Frentes / obra</span></div>
    <div class="metric-card"><span class="metric-icon">📋</span><span class="metric-value">6–12</span><span class="metric-label">Cotiz. / dibujante/sem</span></div>
    <div class="metric-card"><span class="metric-icon">👤</span><span class="metric-value">~50</span><span class="metric-label">Prospectos / mes</span></div>
    <div class="metric-card"><span class="metric-icon">⏱️</span><span class="metric-value">4–6h</span><span class="metric-label">Modelamiento AutoCAD</span></div>
  </div>

  <div class="two-col">
    <div class="info-card">
      <h3>Módulos del Sistema (10)</h3>
      <ul class="module-list">
        <li><span class="mod-badge">01</span> Cotizaciones — Catálogos duales · Líneas negocio</li>
        <li><span class="mod-badge">02</span> Registro y Aprobación de Clientes</li>
        <li><span class="mod-badge">03</span> Contratos y Firma Electrónica (Ooku)</li>
        <li><span class="mod-badge">04</span> Almacén — Pedidos · Remisiones · Conductores</li>
        <li><span class="mod-badge">05</span> Facturación — Proforma · Siigo/DIAN · Centros costo</li>
        <li><span class="mod-badge">06</span> Cartera — Módulo independiente</li>
        <li><span class="mod-badge">07</span> Auditoría — Log inmutable</li>
        <li><span class="mod-badge">08</span> Notificaciones — Configuración de eventos</li>
        <li><span class="mod-badge">09</span> Reportería — KPIs y exportaciones</li>
        <li><span class="mod-badge">10</span> Inventarios — 4 bodegas consultivas</li>
      </ul>
    </div>
    <div class="info-card">
      <h3>Stack Tecnológico</h3>
      <ul class="stack-list">
        <li><span class="stack-tag fe">Frontend</span> React 18 + TypeScript</li>
        <li><span class="stack-tag be">Backend</span> FastAPI (Python)</li>
        <li><span class="stack-tag db">Base de Datos</span> PostgreSQL</li>
        <li><span class="stack-tag ex">Firma</span> Ooku (firma electrónica)</li>
        <li><span class="stack-tag ex">Facturación</span> Siigo → DIAN</li>
        <li><span class="stack-tag ex">Storage</span> S3 Compatible</li>
        <li><span class="stack-tag ex">Notif.</span> Email + WhatsApp API</li>
        <li><span class="stack-tag ex">Mapas</span> API Geocoding (trayectos km)</li>
      </ul>
    </div>
  </div>

  <div class="info-card" style="margin-top:1rem">
    <h3>Roles del Sistema (13)</h3>
    <div class="roles-grid">
      <div class="role-chip">💼 Comercial</div>
      <div class="role-chip">✏️ Dibujante</div>
      <div class="role-chip">📊 Contabilidad</div>
      <div class="role-chip">💳 Facturación</div>
      <div class="role-chip">⚖️ Jurídica</div>
      <div class="role-chip">🏭 Almacén</div>
      <div class="role-chip">🚛 Conductor</div>
      <div class="role-chip">📦 Despachador</div>
      <div class="role-chip">🗓️ Recepción</div>
      <div class="role-chip">📞 Soporte Atención</div>
      <div class="role-chip admin">👑 Admin</div>
      <div class="role-chip admin">🛡️ SuperAdmin</div>
      <div class="role-chip ceo">🏗️ CEO/Ingeniero</div>
    </div>
  </div>

  <div class="callout" style="margin-top:1.25rem">
    <strong>🆕 Julio 2026 — Nuevas Funcionalidades:</strong>
    Rol Soporte Atención al Cliente ·
    Facturación por Kardex Detallado (devoluciones parciales) ·
    Conversión Automática de Unidades (UND → M²) ·
    Validación DIAN/Radian con Scraping Automático (CUFE) ·
    Cotización Autogestionada Web (portal público) ·
    Sistema de Inventarios Consultivo (4 bodegas, no bloqueante) ·
    Alertas de Pedidos Incompletos ·
    Integración Completa Siigo (cotización → pago)
  </div>

  <div class="callout warn" style="margin-top:.75rem">
    <strong>📍 Ciudades:</strong> Bogotá (130 clientes) · Ibagué + Armenia (50 clientes) &nbsp;·&nbsp;
    <strong>Documentos de referencia:</strong> FT-AC-001 v2.0 · CHECKLIST VALIDACION CLIENTES BOGOTA ·
    Autorización Centrales de Riesgo (Ley 1581/2012 · Circular 09/2016)
  </div>
</section>


<section id="flujo-principal">
  <div class="section-header">
    <h2>Flujo Principal del Negocio</h2>
    <p class="section-sub">Ciclo completo: Cotización → Aprobación multi-área → Contrato → Almacén → Facturación → Cartera</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📊 01_flujo_principal_gyh.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-flujo-principal"
              data-filename="01_flujo_principal_gyh.svg"
              title="Descargar como SVG vectorial">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-flujo-principal">
      <pre class="mermaid">{diagrams['flujo_principal']}</pre>
    </div>
  </div>
</section>


<section id="arquitectura">
  <div class="section-header">
    <h2>Arquitectura del Sistema</h2>
    <p class="section-sub">Diagrama de capas y componentes del sistema</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🏗️ 02_arquitectura_sistema.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-arquitectura"
              data-filename="02_arquitectura_sistema.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-arquitectura">
      <pre class="mermaid">{diagrams['arquitectura']}</pre>
    </div>
  </div>
</section>


<section id="cotizacion">
  <div class="section-header">
    <h2>Módulo de Cotizaciones</h2>
    <p class="section-sub">Proceso de cotización técnica + comercial + cotización autogestionada web</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📋 03_modulo_cotizacion.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-cotizacion"
              data-filename="03_modulo_cotizacion.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-cotizacion">
      <pre class="mermaid">{diagrams['cotizacion']}</pre>
    </div>
  </div>
</section>


<section id="registro-cliente">
  <div class="section-header">
    <h2>Registro y Aprobación de Clientes</h2>
    <p class="section-sub">Flujo de aprobación tripartita (Comercial, Contabilidad, Jurídica)</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>✅ 04_registro_aprobacion_cliente.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-registro-cliente"
              data-filename="04_registro_aprobacion_cliente.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-registro-cliente">
      <pre class="mermaid">{diagrams['registro_cliente']}</pre>
    </div>
  </div>
</section>


<section id="inventarios-logistica">
  <div class="section-header">
    <h2>Módulo de Inventarios y Logística</h2>
    <p class="section-sub">Gestión de stock, remisiones y agenda de transporte</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📦 05_modulo_inventarios_logistica.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-inventarios-logistica"
              data-filename="05_modulo_inventarios_logistica.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-inventarios-logistica">
      <pre class="mermaid">{diagrams['inventarios']}</pre>
    </div>
  </div>
</section>


<section id="roles-permisos">
  <div class="section-header">
    <h2>Roles y Permisos (RBAC)</h2>
    <p class="section-sub">13 roles · SuperAdmin · Admin · CEO/Ingeniero · Comercial · Dibujante · Contabilidad · Facturación · Jurídica · Almacén · Despachador · Conductor · Recepción · Soporte Atención</p>
  </div>
  <div class="callout warn">
    <strong>SEM-27:</strong> Roles <strong>Despachador</strong>, <strong>Recepción</strong> y <strong>Soporte Atención</strong> agregados.
    <strong>Facturación</strong> separada de Contabilidad como rol independiente.
    <strong>SuperAdmin</strong> para configuración global del sistema.
    El <strong>CEO/Ingeniero</strong> conserva perfil de consulta, acceso a motivos de rechazo y aprobación forzada.
  </div>
  <div class="md-content">{roles_permissions_html}</div>
</section>


<section id="integracion-siigo">
  <div class="section-header">
    <h2>Integración Siigo/DIAN</h2>
    <p class="section-sub">Secuencia de envío a Siigo y validación DIAN (6 fases)</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🔗 07_integracion_siigo.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-integracion-siigo"
              data-filename="07_integracion_siigo.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-integracion-siigo">
      <pre class="mermaid">{diagrams['integracion_siigo']}</pre>
    </div>
  </div>
</section>


<section id="kardex">
  <div class="section-header">
    <h2>Módulo Kardex y Facturación</h2>
    <p class="section-sub">Facturación detallada por kardex con devoluciones parciales</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📊 08_modulo_kardex_facturacion.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-kardex"
              data-filename="08_modulo_kardex_facturacion.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-kardex">
      <pre class="mermaid">{diagrams['kardex']}</pre>
    </div>
  </div>
</section>


<section id="bodegas">
  <div class="section-header">
    <h2>Sistema de Bodegas e Inventarios</h2>
    <p class="section-sub">4 bodegas consultivas (no restrictivas) con visibilidad por rol</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🏭 09_bodegas_inventarios.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-bodegas"
              data-filename="09_bodegas_inventarios.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-bodegas">
      <pre class="mermaid">{diagrams['bodegas']}</pre>
    </div>
  </div>
</section>


<section id="validacion-dian">
  <div class="section-header">
    <h2>Validación DIAN/Radian</h2>
    <p class="section-sub">Proceso de validación electrónica con automatizaciones</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>✅ 10_validacion_dian_radian.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-validacion-dian"
              data-filename="10_validacion_dian_radian.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-validacion-dian">
      <pre class="mermaid">{diagrams['validacion_dian']}</pre>
    </div>
  </div>
</section>


<section id="flujo-completo-siigo">
  <div class="section-header">
    <h2>📌 Flujo Completo de Integración Siigo</h2>
    <p class="section-sub">DIAGRAMA MAESTRO: Flujo completo desde cotización hasta pago con validación DIAN y scraping CUFE</p>
  </div>
  <div class="callout" style="margin-bottom:1rem">
    <strong>🎯 Diagrama Maestro de Integración</strong><br>
    Este diagrama documenta el flujo completo de integración con Siigo desde cotización hasta sincronización de pagos, incluyendo:
    • Envío opcional de cotización → Siigo<br>
    • Creación de pedidos (completos/parciales) → Siigo<br>
    • Remisiones de salida y devolución → Siigo<br>
    • Facturación → Siigo → DIAN<br>
    • Validación DIAN con scraping automático del CUFE<br>
    • Sincronización de pagos Siigo → GYH<br>
    • Especificaciones técnicas de scraping Python/Node<br>
    • API endpoints Siigo documentados
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🎯 11_flujo_completo_integracion_siigo.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-flujo-completo-siigo"
              data-filename="11_flujo_completo_integracion_siigo.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-flujo-completo-siigo">
      <pre class="mermaid">{diagrams['flujo_completo_siigo']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-principal">
  <div class="section-header">
    <h2>Sitemap Principal</h2>
    <p class="section-sub">Estructura completa de navegación del sistema</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🗺️ sitemap_gyh_app.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-principal"
              data-filename="sitemap_gyh_app.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-principal">
      <pre class="mermaid">{diagrams['sitemap_principal']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-auth">
  <div class="section-header">
    <h2>Sitemap: Auth y Dashboard</h2>
    <p class="section-sub">Autenticación y panel principal</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🔐 sitemap_01_auth_dashboard.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-auth"
              data-filename="sitemap_01_auth_dashboard.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-auth">
      <pre class="mermaid">{diagrams['sitemap_auth']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-clientes">
  <div class="section-header">
    <h2>Sitemap: Clientes</h2>
    <p class="section-sub">Gestión de clientes y prospectos</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>👥 sitemap_02_clientes.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-clientes"
              data-filename="sitemap_02_clientes.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-clientes">
      <pre class="mermaid">{diagrams['sitemap_clientes']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-cotizaciones">
  <div class="section-header">
    <h2>Sitemap: Cotizaciones</h2>
    <p class="section-sub">Cotizaciones técnicas y comerciales</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📋 sitemap_03_cotizaciones.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-cotizaciones"
              data-filename="sitemap_03_cotizaciones.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-cotizaciones">
      <pre class="mermaid">{diagrams['sitemap_cotizaciones']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-contratos">
  <div class="section-header">
    <h2>Sitemap: Contratos</h2>
    <p class="section-sub">Gestión de contratos y firma electrónica</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📝 sitemap_04_contratos.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-contratos"
              data-filename="sitemap_04_contratos.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-contratos">
      <pre class="mermaid">{diagrams['sitemap_contratos']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-inventarios">
  <div class="section-header">
    <h2>Sitemap: Inventarios</h2>
    <p class="section-sub">Gestión de inventarios, pedidos y remisiones</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📦 sitemap_05_inventarios.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-inventarios"
              data-filename="sitemap_05_inventarios.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-inventarios">
      <pre class="mermaid">{diagrams['sitemap_inventarios']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-facturacion">
  <div class="section-header">
    <h2>Sitemap: Facturación y Cartera</h2>
    <p class="section-sub">Facturación, proformas y gestión de cartera</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>💳 sitemap_06_facturacion.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-facturacion"
              data-filename="sitemap_06_facturacion.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-facturacion">
      <pre class="mermaid">{diagrams['sitemap_facturacion']}</pre>
    </div>
  </div>
</section>


<section id="sitemap-auditoria">
  <div class="section-header">
    <h2>Sitemap: Auditoría y Configuración</h2>
    <p class="section-sub">Auditoría, configuración del sistema y reportes</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>🔍 sitemap_07_auditoria_config.mmd</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-sitemap-auditoria"
              data-filename="sitemap_07_auditoria_config.svg">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-sitemap-auditoria">
      <pre class="mermaid">{diagrams['sitemap_auditoria']}</pre>
    </div>
  </div>
</section>


<section id="notificaciones">
  <div class="section-header">
    <h2>Notificaciones del Sistema — Módulo 08</h2>
    <p class="section-sub">29 notificaciones · Email · WhatsApp API · In-app · 2FA por correo en autenticación · Prioridades y destinatarios por evento</p>
  </div>
  <div class="callout">
    <strong>🔐 Segundo Factor (2FA):</strong> El sistema requiere verificación de código al correo en cada inicio de sesión — sin código válido, el acceso no se habilita.
    &nbsp;·&nbsp;
    <strong>Canales:</strong> <strong>Email</strong> (plataforma) · <strong>WhatsApp API</strong> (externo — cliente) · <strong>In-app</strong> (notificación en interfaz).
    &nbsp;·&nbsp;
    <strong>Prioridad Alta</strong> = acción inmediata · <strong>Media</strong> = recordatorio · <strong>Baja</strong> = log / confirmación.
  </div>
  <div class="md-content">{notifications_html}</div>
</section>


<section id="database">
  <div class="section-header">
    <h2>Esquema de Base de Datos — PostgreSQL</h2>
    <p class="section-sub">DBML v1.1 · {len(tables)} tablas · {len(enums)} enumeraciones · Actualizado Julio 2026</p>
  </div>

  <div class="callout">
    <strong>Motor:</strong> PostgreSQL &nbsp;·&nbsp;
    <strong>Basado en:</strong> FT-AC-001 v2.0 · Checklist Validación Clientes · Autorización Centrales de Riesgo · Julio 2026 (Kardex, Bodegas, Conversión Unidades, DIAN Scraping)
  </div>

  <div class="db-legend">
    <span style="border-color:#0B3C5D;color:#0B3C5D">⬛ Seguridad / Transversal</span>
    <span style="border-color:#2C7A7B;color:#2C7A7B">⬛ Clientes / Obras</span>
    <span style="border-color:#553C9A;color:#553C9A">⬛ Cotizaciones</span>
    <span style="border-color:#6B46C1;color:#6B46C1">⬛ Contratos</span>
    <span style="border-color:#276749;color:#276749">⬛ Inventarios</span>
    <span style="border-color:#744210;color:#744210">⬛ Facturación</span>
  </div>

  <h3>Enumeraciones ({len(enums)})</h3>
  <div class="enum-grid">
{enum_pills_html}
  </div>

  <h3>Tablas ({len(tables)})</h3>
  <div class="t-grid">
{table_cards_html}
  </div>

  <h3>Código DBML completo</h3>
  <details>
    <summary>▶ Ver schema completo (.dbml)</summary>
    <pre class="code-block">{dbml_content_escaped}</pre>
  </details>
</section>


<footer>
  <p><strong>G&H Obras y Estructuras Metálicas S.A.S.</strong></p>
  <p>NIT: 901.218.896-8 · Bogotá, Colombia</p>
  <p>Documentación generada automáticamente · {timestamp_full}</p>
  <p>Versión del sistema: Julio 2026 · 11 Diagramas · 13 Roles · {len(tables)} Tablas PostgreSQL</p>
</footer>

</main>
</div>

</body>
</html>
'''

    # Guardar archivo
    output_path = output_dir / 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ Inception Report generado exitosamente!")
    print(f"📁 Ubicación: {output_path.absolute()}")
    print(f"\n📊 Contenido incluido:")
    print(f"   • 11 Diagramas de arquitectura")
    print(f"   • 7 Sitemaps de navegación")
    print(f"   • {len(enums)} Enumeraciones de base de datos")
    print(f"   • {len(tables)} Tablas con diccionario completo")
    print(f"   • Código DBML completo expandible")
    print(f"   • Métricas y resumen ejecutivo")
    print(f"   • Diseño corporativo G&H")
    print(f"   • Navegación sticky con ScrollSpy")
    print(f"\n💡 Para visualizar:")
    print(f"   open {output_path.absolute()}")
    print(f"\n🎉 ¡Listo!")


if __name__ == '__main__':
    main()
