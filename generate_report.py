#!/usr/bin/env python3
"""
G&H Obras y Estructuras Metálicas S.A.S
Generador de Reporte HTML — Fase de Inception
Uso:  python3 generate_report.py
Salida: GYH_InceptionReport.html
"""
import re
import html as _html
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
OUT  = BASE / "GYH_InceptionReport.html"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def rf(rel):
    p = BASE / rel
    return p.read_text(encoding='utf-8') if p.exists() else ""

# ─── Markdown → HTML (subset: headings, tables, lists, code, checkboxes) ──────

def md2html(src):
    lines = src.splitlines()
    out, state = [], None

    def close():
        nonlocal state
        if state == 'ul':    out.append('</ul>')
        elif state == 'ol':  out.append('</ol>')
        elif state == 'tbl': out.append('</tbody></table></div>')
        state = None

    def inline(t):
        t = _html.escape(t)
        t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        return t

    i = 0
    while i < len(lines):
        L = lines[i]; i += 1

        if not L.strip():
            close(); continue

        # headings
        for n in (4, 3, 2, 1):
            if L.startswith('#' * n + ' '):
                close()
                out.append(f'<h{n}>{inline(L[n+1:])}</h{n}>')
                break
        else:
            # hr
            if L.strip() in ('---', '***', '___'):
                close(); out.append('<hr>'); continue

            # table
            if L.strip().startswith('|'):
                if state != 'tbl':
                    close()
                    cells = [c.strip() for c in L.strip().strip('|').split('|')]
                    out.append('<div class="table-wrap"><table><thead><tr>')
                    for c in cells: out.append(f'<th>{inline(c)}</th>')
                    out.append('</tr></thead><tbody>')
                    state = 'tbl'
                    # skip separator row
                    if i < len(lines) and re.match(r'^\|[\s\-|:]+\|$', lines[i].strip()):
                        i += 1
                    continue
                cells = [c.strip() for c in L.strip().strip('|').split('|')]
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
                continue

            if state == 'tbl' and not L.strip().startswith('|'):
                close()

            # unordered list / checkboxes
            m = re.match(r'^([ \t]*)[-*]\s+(.*)', L)
            if m:
                content = m.group(2)
                if state != 'ul': close(); out.append('<ul class="md-list">'); state = 'ul'
                if re.match(r'\[[ x]\]\s', content, re.I):
                    checked = content[1].lower() == 'x'
                    text = content[4:].strip()
                    chk = '<span class="chk chk-ok">✓</span>' if checked else '<span class="chk">☐</span>'
                    cls = ' class="check-item done"' if checked else ' class="check-item"'
                    out.append(f'<li{cls}>{chk} {inline(text)}</li>')
                else:
                    out.append(f'<li>{inline(content)}</li>')
                continue

            if state == 'ul': close()

            # ordered list
            m2 = re.match(r'^\d+\.\s+(.*)', L)
            if m2:
                if state != 'ol': close(); out.append('<ol>'); state = 'ol'
                out.append(f'<li>{inline(m2.group(1))}</li>')
                continue

            if state == 'ol': close()

            out.append(f'<p>{inline(L)}</p>')

    close()
    return '\n'.join(out)

# ─── DBML parser: tablas + enums ──────────────────────────────────────────────

def _extract_blocks(src, keyword):
    """Extrae bloques 'keyword Name { ... }' respetando llaves anidadas."""
    results = []
    for m in re.finditer(rf'{keyword}\s+(\w+)\s*\{{', src):
        name, start = m.group(1), m.end() - 1
        depth, pos = 1, start + 1
        while pos < len(src) and depth:
            depth += (src[pos] == '{') - (src[pos] == '}')
            pos += 1
        results.append((name, src[start+1:pos-1]))
    return results

def parse_dbml(src):
    tables, enums = [], []

    for ename, body in _extract_blocks(src, 'Enum'):
        vals = re.findall(r'^\s{2}(\w+)', body, re.MULTILINE)
        notes = dict(re.findall(r'(\w+)\s+\[note:\s*[\'"]([^\'"]+)[\'"]', body))
        enums.append({'name': ename, 'values': vals, 'notes': notes})

    for tname, body in _extract_blocks(src, 'Table'):
        note_m = re.search(r"Note:\s*'([^']*)'", body)
        note = note_m.group(1).strip() if note_m else ''
        cols = []
        for cm in re.finditer(r'^\s{2}(\w+)\s+(\S+)\s*(.*?)$', body, re.MULTILINE):
            cname, ctype, rest = cm.group(1), cm.group(2), cm.group(3).strip()
            if cname in ('indexes', 'Note', 'note'): continue
            cols.append({
                'name': cname, 'type': ctype,
                'pk':   '[pk]' in rest,
                'nn':   '[not null]' in rest,
                'uniq': '[unique' in rest,
                'fk':   'ref:' in rest,
                'raw':  rest,
            })
        if cols:
            tables.append({'name': tname, 'cols': cols, 'note': note})

    return tables, enums

# ─── HTML builders ────────────────────────────────────────────────────────────

def diagram_section(sec_id, title, subtitle, filepath):
    raw   = rf(filepath)
    fname = Path(filepath).name
    stem  = Path(filepath).stem
    return f'''
<section id="{sec_id}">
  <div class="section-header">
    <h2>{title}</h2>
    <p class="section-sub">{subtitle}</p>
  </div>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📊 {fname}</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-{sec_id}"
              data-filename="{stem}.svg"
              title="Descargar como SVG vectorial">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-{sec_id}">
      <pre class="mermaid">{raw}</pre>
    </div>
  </div>
</section>'''

def multi_diagram_section(sec_id, title, subtitle, diagrams):
    """Renderiza múltiples diagramas dentro de una sección (para sitemaps segmentados)."""
    blocks = ''
    for (sub_id, label, filepath) in diagrams:
        raw  = rf(filepath)
        fname = Path(filepath).name
        stem  = Path(filepath).stem
        blocks += f'''
  <div class="diagram-block" style="margin-bottom:1.5rem">
    <div class="diagram-label">
      <span>📊 {label} &nbsp;·&nbsp; {fname}</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-{sub_id}"
              data-filename="{stem}.svg"
              title="Descargar como SVG vectorial">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-{sub_id}">
      <pre class="mermaid">{raw}</pre>
    </div>
  </div>'''
    return f'''
<section id="{sec_id}">
  <div class="section-header">
    <h2>{title}</h2>
    <p class="section-sub">{subtitle}</p>
  </div>
  {blocks}
</section>'''

def roles_section(tabla_md, mmd_path):
    tabla_html = md2html(tabla_md)
    raw   = rf(mmd_path)
    fname = Path(mmd_path).name
    stem  = Path(mmd_path).stem
    return f'''
<section id="roles">
  <div class="section-header">
    <h2>Roles y Permisos (RBAC)</h2>
    <p class="section-sub">8 roles · CEO/Ingeniero · Admin · Comercial · Dibujante · Contabilidad · Jurídica · Almacén · Conductor</p>
  </div>
  <div class="callout warn">
    <strong>Nuevo (Feedback 24-jun):</strong> Se añadió el rol <strong>CEO/Ingeniero</strong> con perfil de consulta, acceso a motivos de rechazo y capacidad de forzar la aprobación de un cliente bajo su estricta responsabilidad.
  </div>
  <div class="md-content">{tabla_html}</div>
  <h3 style="margin-top:2rem">Diagrama de Permisos por Rol</h3>
  <div class="diagram-block">
    <div class="diagram-label">
      <span>📊 {fname}</span>
      <button class="btn-dl-svg"
              data-wrap="wrap-roles-mmd"
              data-filename="{stem}.svg"
              title="Descargar como SVG vectorial">
        ⬇ Descargar SVG
      </button>
    </div>
    <div class="mermaid-wrap" id="wrap-roles-mmd">
      <pre class="mermaid">{raw}</pre>
    </div>
  </div>
</section>'''

def db_section(tables, enums, raw):
    # Enum pills
    enum_html = ''
    for e in enums:
        vals = ', '.join(e['values'][:6])
        more = f' +{len(e["values"])-6}' if len(e['values']) > 6 else ''
        enum_html += f'<div class="enum-pill"><strong>{e["name"]}</strong><span class="enum-vals">{vals}{more}</span></div>\n'

    MODULE_COLORS = {
        'usuarios': '#1A365D', 'auditoria': '#1A365D', 'notificaciones': '#1A365D',
        'clientes': '#2C7A7B', 'contactos': '#2C7A7B', 'referencias': '#2C7A7B',
        'accionistas': '#2C7A7B', 'autorizacion': '#2C7A7B', 'aprobaciones': '#2C7A7B',
        'documentos': '#2C7A7B', 'obras': '#2C7A7B', 'frentes': '#2C7A7B',
        'catalogo': '#553C9A', 'cotizaciones': '#553C9A', 'cotizacion': '#553C9A',
        'archivos': '#553C9A',
        'ordenes': '#6B46C1', 'contratos': '#6B46C1',
        'conductores': '#276749', 'remisiones': '#276749', 'remision': '#276749',
        'agenda': '#276749',
        'facturas': '#744210', 'factura': '#744210', 'pagos': '#744210',
        'cartera': '#744210',
    }

    cards_html = ''
    for t in tables:
        color = '#1A365D'
        for prefix, c in MODULE_COLORS.items():
            if t['name'].startswith(prefix):
                color = c; break

        note_html = f'<p class="t-note">{_html.escape(t["note"])}</p>' if t['note'] else ''
        col_rows = ''
        for c in t['cols'][:7]:
            badges = ''
            if c['pk']:   badges += '<span class="badge pk">PK</span>'
            if c['fk']:   badges += '<span class="badge fk">FK</span>'
            if c['uniq']: badges += '<span class="badge uniq">UQ</span>'
            col_rows += f'<tr><td><code>{c["name"]}</code></td><td class="t-type">{c["type"]}</td><td>{badges}</td></tr>'
        more_txt = f'<p class="t-more">+ {len(t["cols"])-7} columnas más</p>' if len(t['cols']) > 7 else ''

        cards_html += f'''
<div class="t-card" style="--tcolor:{color}">
  <div class="t-head">
    <span class="t-name">{t["name"]}</span>
    <span class="t-count">{len(t["cols"])} cols</span>
  </div>
  {note_html}
  <table class="t-cols"><tbody>{col_rows}</tbody></table>
  {more_txt}
</div>'''

    return f'''
<section id="database">
  <div class="section-header">
    <h2>Base de Datos — Schema PostgreSQL</h2>
    <p class="section-sub">DBML v1.0 · {len(tables)} tablas · {len(enums)} enumeraciones</p>
  </div>
  <div class="callout">
    <strong>Motor:</strong> PostgreSQL &nbsp;·&nbsp; <strong>Escala inicial:</strong> ~180 clientes · 50 obras/cliente · 3-4 frentes/obra
    &nbsp;·&nbsp; <strong>Basado en:</strong> FT-AC-001 v2.0 · Checklist Validación Clientes · Autorización Centrales de Riesgo
  </div>

  <div class="db-legend">
    <span style="border-color:#1A365D;color:#1A365D">⬛ Seguridad / Transversal</span>
    <span style="border-color:#2C7A7B;color:#2C7A7B">⬛ Clientes / Obras</span>
    <span style="border-color:#553C9A;color:#553C9A">⬛ Cotizaciones</span>
    <span style="border-color:#6B46C1;color:#6B46C1">⬛ Contratos</span>
    <span style="border-color:#276749;color:#276749">⬛ Inventarios</span>
    <span style="border-color:#744210;color:#744210">⬛ Facturación</span>
  </div>

  <h3>Enumeraciones ({len(enums)})</h3>
  <div class="enum-grid">{enum_html}</div>

  <h3>Tablas ({len(tables)})</h3>
  <div class="t-grid">{cards_html}</div>

  <h3>Código DBML completo</h3>
  <details>
    <summary>▶ Ver schema completo (.dbml)</summary>
    <pre class="code-block">{_html.escape(raw)}</pre>
  </details>
</section>'''

# ─── Overview section ─────────────────────────────────────────────────────────

OVERVIEW = '''
<section id="overview">
  <div class="section-header">
    <h2>Resumen del Proyecto</h2>
    <p class="section-sub">G&H Obras y Estructuras Metálicas S.A.S · NIT: 901.218.896-8 · Bogotá · Sesión 2026-06-16 + Feedback 2026-06-24</p>
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
      <h3>Módulos del Sistema</h3>
      <ul class="module-list">
        <li><span class="mod-badge">01</span> Cotizaciones — Dibujante + Comercial</li>
        <li><span class="mod-badge">02</span> Registro y Aprobación de Clientes</li>
        <li><span class="mod-badge">03</span> Contratos y Firma Electrónica</li>
        <li><span class="mod-badge">04</span> Inventarios y Logística</li>
        <li><span class="mod-badge">05</span> Facturación y Cartera</li>
        <li><span class="mod-badge">06</span> Auditoría y Notificaciones</li>
      </ul>
    </div>
    <div class="info-card">
      <h3>Stack Tecnológico</h3>
      <ul class="stack-list">
        <li><span class="stack-tag fe">Frontend</span> React + TypeScript</li>
        <li><span class="stack-tag be">Backend</span> FastAPI (Python)</li>
        <li><span class="stack-tag db">Base de Datos</span> PostgreSQL</li>
        <li><span class="stack-tag ex">Firma</span> DocuSign / Okc</li>
        <li><span class="stack-tag ex">Storage</span> S3 Compatible</li>
        <li><span class="stack-tag ex">Notif.</span> Email + WhatsApp API</li>
      </ul>
    </div>
  </div>

  <div class="info-card" style="margin-top:1rem">
    <h3>Roles del Sistema (8)</h3>
    <div class="roles-grid">
      <div class="role-chip">💼 Comercial</div>
      <div class="role-chip">✏️ Dibujante</div>
      <div class="role-chip">📊 Contabilidad</div>
      <div class="role-chip">⚖️ Jurídica</div>
      <div class="role-chip">🏭 Almacén</div>
      <div class="role-chip">🚛 Conductor</div>
      <div class="role-chip admin">👑 Admin</div>
      <div class="role-chip ceo">🏗️ CEO/Ingeniero</div>
    </div>
  </div>

  <div class="callout" style="margin-top:1.25rem">
    <strong>🆕 Ajustes Feedback 24-jun:</strong>
    Subdivisión del catálogo por unidades de negocio (5) ·
    Notas por especialidad en aprobación de clientes ·
    Rol CEO/Ingeniero con aprobación final ·
    Producción incluida en el Kardex de inventario ·
    Alertas de recogidas logísticas ·
    Campos de fecha y hora en transacciones
  </div>

  <div class="callout warn" style="margin-top:.75rem">
    <strong>📍 Ciudades:</strong> Bogotá (130 clientes) · Ibagué + Armenia (50 clientes) &nbsp;·&nbsp;
    <strong>Documentos de referencia:</strong> FT-AC-001 v2.0 · CHECKLIST VALIDACION CLIENTES BOGOTA ·
    Autorización Centrales de Riesgo (Ley 1581/2012 · Circular 09/2016)
  </div>
</section>'''

# ─── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
:root {
  --bg:#F7FAFC; --surface:#FFFFFF; --surface2:#EDF2F7; --border:#CBD5E0;
  --text:#1A202C; --muted:#718096;
  --primary:#1A365D; --primary2:#2C5282;
  --accent:#FF9F1C; --accent2:#E8910A;
  --steel:#4A5568; --success:#38A169; --danger:#E53E3E;
  --nav-w:270px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}

/* Layout */
.layout{display:grid;grid-template-columns:var(--nav-w) 1fr;min-height:100vh}
@media(max-width:960px){.layout{grid-template-columns:1fr}nav{position:relative;height:auto;width:100%}}

/* Sidebar */
nav{position:sticky;top:0;height:100vh;overflow-y:auto;background:var(--primary);color:#fff;padding:0 0 2rem;font-size:.84rem;box-shadow:2px 0 12px rgba(0,0,0,.18)}
.nav-brand{display:flex;align-items:center;gap:.75rem;padding:1.25rem 1rem;background:#0F2440;border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:.5rem}
.nav-logo{background:var(--accent);color:var(--primary);font-weight:900;font-size:1.15rem;padding:.3rem .55rem;border-radius:6px;line-height:1;flex-shrink:0}
.nav-brand strong{display:block;color:#fff;font-size:.88rem;line-height:1.3}
.nav-brand small{color:rgba(255,255,255,.5);font-size:.7rem}
.nav-group{font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.38);padding:.9rem 1rem .3rem}
nav a{display:block;padding:.38rem 1rem;color:rgba(255,255,255,.72);text-decoration:none;border-left:3px solid transparent;transition:all .15s}
nav a:hover{color:var(--accent);background:rgba(255,255,255,.07);border-left-color:var(--accent)}

/* Main */
main{padding:2rem 2.5rem 4rem;background:var(--bg)}
@media(max-width:720px){main{padding:1rem 1rem 3rem}}

/* Hero */
.hero{background:linear-gradient(135deg,var(--primary) 0%,var(--primary2) 100%);color:#fff;border-radius:14px;padding:2.5rem 2rem;margin-bottom:2.5rem;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;right:-80px;top:-80px;width:260px;height:260px;border-radius:50%;background:rgba(255,159,28,.12);pointer-events:none}
.hero::after{content:'';position:absolute;right:40px;bottom:-40px;width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,.06);pointer-events:none}
.hero-tag{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);font-weight:700;margin-bottom:.5rem}
.hero h1{font-size:2rem;font-weight:900;margin-bottom:.4rem}
.hero p{color:rgba(255,255,255,.65);font-size:.92rem}
.hero-meta{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1.5rem}
.hero-chip{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:.22rem .7rem;font-size:.75rem;color:rgba(255,255,255,.88)}

/* Sections */
section{margin-bottom:3.5rem;scroll-margin-top:1rem}
.section-header{margin-bottom:1.5rem;padding-bottom:.7rem;border-bottom:3px solid var(--accent)}
.section-header h2{font-size:1.45rem;color:var(--primary);font-weight:800}
.section-sub{color:var(--muted);font-size:.86rem;margin-top:.3rem}
section h3{font-size:1.05rem;color:var(--primary);margin:1.75rem 0 .75rem;font-weight:700}

/* Diagrams */
.diagram-block{border:1px solid var(--border);border-radius:12px;overflow:hidden;background:var(--surface);box-shadow:0 2px 10px rgba(0,0,0,.07);margin-bottom:1rem}
.diagram-label{background:var(--primary);color:rgba(255,255,255,.75);padding:.4rem 1rem;font-size:.72rem;font-family:ui-monospace,monospace;letter-spacing:.04em;display:flex;align-items:center;justify-content:space-between;gap:.75rem}
.btn-dl-svg{flex-shrink:0;background:var(--accent);color:var(--primary);border:none;border-radius:5px;padding:.28rem .75rem;font-size:.72rem;font-weight:700;cursor:pointer;letter-spacing:.02em;font-family:inherit;transition:background .15s,transform .1s}
.btn-dl-svg:hover{background:var(--accent2);transform:translateY(-1px)}
.btn-dl-svg:active{transform:translateY(0)}
.btn-dl-svg.loading{opacity:.6;cursor:wait}
.mermaid-wrap{padding:1.5rem;overflow-x:auto;background:#fff;min-height:80px}
.mmd-svg-wrap svg{max-width:100%;height:auto}

/* Metrics */
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.9rem;margin-bottom:1.5rem}
.metric-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1rem;text-align:center;border-top:4px solid var(--accent);box-shadow:0 1px 4px rgba(0,0,0,.05)}
.metric-icon{display:block;font-size:1.7rem;margin-bottom:.45rem}
.metric-value{display:block;font-size:1.7rem;font-weight:900;color:var(--primary)}
.metric-label{display:block;font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-top:.2rem}

/* Info cards */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}
@media(max-width:680px){.two-col{grid-template-columns:1fr}}
.info-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.25rem;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.info-card h3{color:var(--primary);font-size:1rem;margin-bottom:.75rem;border-bottom:1px solid var(--surface2);padding-bottom:.4rem}
.module-list,.stack-list{list-style:none}
.module-list li,.stack-list li{padding:.35rem 0;border-bottom:1px solid var(--surface2);font-size:.86rem;color:var(--steel);display:flex;align-items:center;gap:.5rem}
.module-list li:last-child,.stack-list li:last-child{border-bottom:none}
.mod-badge{background:var(--primary);color:#fff;border-radius:4px;padding:.1rem .4rem;font-size:.68rem;font-weight:700;flex-shrink:0}
.stack-tag{padding:.12rem .45rem;border-radius:4px;font-size:.68rem;font-weight:700;flex-shrink:0}
.stack-tag.fe{background:#EBF8FF;color:#2B6CB0}
.stack-tag.be{background:#F0FFF4;color:#276749}
.stack-tag.db{background:#FAF5FF;color:#6B46C1}
.stack-tag.ex{background:#FFFBEB;color:#92400E}
.roles-grid{display:flex;flex-wrap:wrap;gap:.5rem;padding-top:.25rem}
.role-chip{background:var(--surface2);border:1px solid var(--border);border-radius:999px;padding:.28rem .82rem;font-size:.8rem;color:var(--primary);font-weight:600}
.role-chip.admin{background:#FFFBEB;border-color:var(--accent);color:#92400E}
.role-chip.ceo{background:#FFF5F5;border-color:#E53E3E;color:#C53030}

/* Callout */
.callout{background:#EBF8FF;border-left:4px solid #3182CE;border-radius:0 8px 8px 0;padding:.85rem 1.1rem;margin:1rem 0;font-size:.86rem}
.callout.warn{background:#FFFBEB;border-left-color:var(--accent)}

/* DB tables */
.db-legend{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1.25rem}
.db-legend span{border:1px solid;border-radius:4px;padding:.2rem .55rem;font-size:.72rem;font-weight:600}
.t-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.9rem;margin-bottom:1.5rem}
.t-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.t-head{background:var(--tcolor,var(--primary));color:#fff;padding:.55rem .9rem;display:flex;align-items:center;gap:.5rem}
.t-name{font-weight:700;font-size:.86rem;flex:1;font-family:ui-monospace,monospace}
.t-count{font-size:.65rem;color:rgba(255,255,255,.6);background:rgba(255,255,255,.12);padding:.1rem .4rem;border-radius:3px}
.t-note{font-size:.73rem;color:var(--muted);padding:.45rem .8rem;background:var(--surface2);border-bottom:1px solid var(--border);line-height:1.4}
.t-cols{width:100%;border-collapse:collapse;font-size:.76rem}
.t-cols td{padding:.28rem .75rem;border-bottom:1px solid #f1f5f9}
.t-cols tr:last-child td{border-bottom:none}
.t-cols td:first-child code{font-size:.75rem;color:var(--primary);font-weight:600}
.t-type{color:var(--muted);font-family:ui-monospace,monospace;font-size:.7rem}
.t-more{font-size:.7rem;color:var(--muted);padding:.35rem .75rem;background:var(--surface2);text-align:center;font-style:italic}
.badge{display:inline-block;padding:.05rem .3rem;border-radius:3px;font-size:.62rem;font-weight:700;margin-right:.15rem}
.badge.pk{background:#FEF3C7;color:#92400E}
.badge.fk{background:#E0E7FF;color:#3730A3}
.badge.uniq{background:#D1FAE5;color:#065F46}
.enum-grid{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:1.5rem}
.enum-pill{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:.55rem .85rem;min-width:150px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.enum-pill strong{display:block;color:var(--primary);font-size:.8rem;margin-bottom:.2rem}
.enum-vals{color:var(--muted);font-size:.7rem;font-family:ui-monospace,monospace;line-height:1.6}
details{margin-top:1rem}
details summary{cursor:pointer;color:var(--primary);font-size:.88rem;font-weight:600;padding:.5rem 0;user-select:none}
.code-block{background:#1A202C;color:#E2E8F0;border-radius:10px;padding:1.25rem;font-size:.76rem;overflow-x:auto;line-height:1.75;max-height:500px;overflow-y:auto;font-family:ui-monospace,monospace;border:1px solid #2D3748;margin-top:.75rem}

/* Markdown content */
.md-content h1{font-size:1.4rem;color:var(--primary);margin:1.5rem 0 .75rem;border-bottom:2px solid var(--accent);padding-bottom:.35rem}
.md-content h2{font-size:1.2rem;color:var(--primary);margin:2rem 0 .75rem;border-bottom:1px solid var(--border);padding-bottom:.35rem}
.md-content h3{font-size:1rem;color:var(--primary2);margin:1.4rem 0 .5rem}
.md-content h4{font-size:.92rem;color:var(--steel);margin:1rem 0 .4rem;font-style:italic}
.md-content p{margin:.5rem 0;color:var(--text);font-size:.88rem}
.md-content code{background:#EDF2F7;padding:.1rem .38rem;border-radius:3px;font-size:.8em;color:#6B46C1}
.md-content strong{color:var(--primary)}
.md-content hr{border:none;border-top:2px solid var(--border);margin:2rem 0}
.md-content ul.md-list{margin:.5rem 0 .5rem 1.4rem}
.md-content ol{margin:.5rem 0 .5rem 1.4rem}
.md-content li{margin:.28rem 0;font-size:.88rem}
.check-item{list-style:none;display:flex;align-items:flex-start;gap:.5rem;margin-left:-1.4rem;padding:.2rem 0}
.chk{flex-shrink:0;width:1.3rem;text-align:center;color:var(--muted);margin-top:.05rem;font-size:.9rem}
.chk-ok{color:var(--success)}
.check-item.done{color:#276749}
.table-wrap{overflow-x:auto;margin:1rem 0}
.md-content table{width:100%;border-collapse:collapse;font-size:.82rem;background:var(--surface);border:1px solid var(--border);border-radius:8px;overflow:hidden}
.md-content th{background:var(--primary);color:#fff;padding:.45rem .75rem;text-align:left;font-size:.8rem;font-weight:600}
.md-content td{padding:.4rem .75rem;border-bottom:1px solid var(--border);vertical-align:top;text-align:center}
.md-content td:first-child{text-align:left}
.md-content tr:nth-child(even) td{background:var(--surface2)}

/* Footer */
footer{padding-top:2rem;border-top:2px solid var(--border);color:var(--muted);font-size:.8rem;margin-top:2rem}
footer strong{color:var(--primary)}

@media print{nav{display:none}.layout{grid-template-columns:1fr}body{font-size:11pt}}
"""

# ─── Main ─────────────────────────────────────────────────────────────────────

def generate():
    print("📂 Leyendo archivos…")

    dbml_raw          = rf('database/gyh_schema.dbml')
    tables, enums     = parse_dbml(dbml_raw)
    us_html           = md2html(rf('user-stories/historias_usuario.md'))
    ck_html           = md2html(rf('checklist-validado.md'))
    roles_tabla_md    = rf('architecture/06_roles_y_permisos_tabla.md')
    db_html           = db_section(tables, enums, dbml_raw)
    today             = date.today().strftime("%d de %B de %Y")

    num_sitemaps = len(list((BASE / 'sitemaps').glob('sitemap_0*.mmd')))
    num_diagrams = 6 + num_sitemaps  # 6 architecture + sitemaps

    SITEMAPS = [
        ('sm-auth',     'Auth y Dashboard',       'sitemaps/sitemap_01_auth_dashboard.mmd'),
        ('sm-clientes', 'Clientes y Aprobación',  'sitemaps/sitemap_02_clientes.mmd'),
        ('sm-cot',      'Cotizaciones y Catálogo', 'sitemaps/sitemap_03_cotizaciones.mmd'),
        ('sm-contratos','Contratos',               'sitemaps/sitemap_04_contratos.mmd'),
        ('sm-inv',      'Inventarios y Logística', 'sitemaps/sitemap_05_inventarios.mmd'),
        ('sm-fac',      'Facturación',             'sitemaps/sitemap_06_facturacion.mmd'),
        ('sm-aud',      'Auditoría y Config',      'sitemaps/sitemap_07_auditoria_config.mmd'),
    ]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>G&H Sistema — Inception Report 2026</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'base',
      securityLevel: 'loose',
      themeVariables: {{
        primaryColor: '#1A365D',
        primaryTextColor: '#FFFFFF',
        primaryBorderColor: '#1A365D',
        lineColor: '#4A5568',
        secondaryColor: '#EDF2F7',
        clusterBkg: '#2D3748',
        titleColor: '#FFFFFF',
        edgeLabelBackground: '#F7FAFC',
        fontFamily: 'Segoe UI, system-ui, sans-serif'
      }}
    }});

    /* ── SVG download helper ─────────────────────────────────── */
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

    /* ── Render Mermaid + wire download buttons ──────────────── */
    document.addEventListener('DOMContentLoaded', async () => {{
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
    }});
  </script>
  <style>{CSS}</style>
</head>
<body>
<div class="layout">

<nav>
  <div class="nav-brand">
    <span class="nav-logo">G&amp;H</span>
    <div><strong>G&amp;H Sistema</strong><small>Inception Report · 2026</small></div>
  </div>
  <div class="nav-group">Visión General</div>
  <a href="#overview">📊 Resumen del Proyecto</a>
  <div class="nav-group">Diagramas de Arquitectura</div>
  <a href="#arquitectura">🏗️ Arquitectura del Sistema</a>
  <a href="#flujo-principal">🔄 Flujo Principal del Negocio</a>
  <a href="#cotizacion">📋 Módulo Cotizaciones</a>
  <a href="#registro-cliente">👥 Registro y Aprobación</a>
  <a href="#inventarios">📦 Inventarios y Logística</a>
  <a href="#roles">🔐 Roles y Permisos</a>
  <div class="nav-group">Sitemaps por Flujo</div>
  <a href="#sitemaps">🗺️ Auth · Dashboard</a>
  <a href="#sitemaps">👥 Clientes · Cotizaciones</a>
  <a href="#sitemaps">📦 Inventarios · Facturación</a>
  <a href="#sitemaps">🔍 Auditoría · Config</a>
  <div class="nav-group">Base de Datos</div>
  <a href="#database">🗄️ Schema PostgreSQL</a>
  <div class="nav-group">Requerimientos</div>
  <a href="#historias">📖 Historias de Usuario</a>
  <a href="#checklist">✅ Checklist Validado</a>
</nav>

<main>

  <header class="hero">
    <p class="hero-tag">Fase de Inception · Documentación Técnica · G&amp;H Obras y Estructuras Metálicas S.A.S</p>
    <h1>Sistema de Gestión G&amp;H</h1>
    <p>Cotizaciones · Clientes · Contratos · Inventarios · Facturación · Auditoría</p>
    <div class="hero-meta">
      <span class="hero-chip">📅 {today}</span>
      <span class="hero-chip">🗄️ {len(tables)} tablas PostgreSQL</span>
      <span class="hero-chip">📊 {num_diagrams} diagramas Mermaid</span>
      <span class="hero-chip">👤 8 roles del sistema</span>
      <span class="hero-chip">🗺️ 7 sitemaps por flujo</span>
      <span class="hero-chip">🆕 Feedback 24-jun aplicado</span>
    </div>
  </header>

  {OVERVIEW}

  {diagram_section("arquitectura",
    "Arquitectura del Sistema",
    "React + FastAPI + PostgreSQL · Módulos · Integraciones externas: DocuSign / Okc · Email · WhatsApp",
    "architecture/02_arquitectura_sistema.mmd")}

  {diagram_section("flujo-principal",
    "Flujo Principal del Negocio",
    "Ciclo completo: Cotización → Aprobación multi-área → Contrato → Inventarios → Facturación → Cartera",
    "architecture/01_flujo_principal_gyh.mmd")}

  {diagram_section("cotizacion",
    "Módulo de Cotizaciones",
    "Dibujante (AutoCAD 4-6h) → Importar Excel → Catálogo por Unidad de Negocio → Comercial → PDF → Orden de Compra",
    "architecture/03_modulo_cotizacion.mmd")}

  {diagram_section("registro-cliente",
    "Registro y Aprobación de Clientes",
    "Formulario FT-AC-001 v2.0 · 9 secciones · Checklist documental · Concepto + nota obligatoria por 3 áreas · Aprobación final CEO",
    "architecture/04_registro_aprobacion_cliente.mmd")}

  {diagram_section("inventarios",
    "Inventarios y Logística",
    "Kardex (Bodega + Clientes + Producción) · Remisiones · Agenda de transporte · Alertas de recogidas · Devoluciones",
    "architecture/05_modulo_inventarios_logistica.mmd")}

  {roles_section(roles_tabla_md, "architecture/06_roles_y_permisos.mmd")}

  {multi_diagram_section("sitemaps",
    "Sitemaps por Flujo Principal",
    "Mapa de rutas segmentado por módulo — 7 flujos independientes",
    SITEMAPS)}

  {db_html}

  <section id="historias">
    <div class="section-header">
      <h2>Historias de Usuario</h2>
      <p class="section-sub">Sesión 2026-06-16 · Criterios de aceptación verificables · Roles asignados</p>
    </div>
    <div class="md-content">{us_html}</div>
  </section>

  <section id="checklist">
    <div class="section-header">
      <h2>Checklist Validado</h2>
      <p class="section-sub">Ítems de la sesión + ajustes del feedback 24-jun · Cubre todos los módulos del sistema</p>
    </div>
    <div class="md-content">{ck_html}</div>
  </section>

  <footer>
    <p><strong>G&amp;H Obras y Estructuras Metálicas S.A.S</strong> &nbsp;·&nbsp; NIT: 901.218.896-8 &nbsp;·&nbsp; Calle 64 #112C-27, Engativá, Bogotá — Colombia</p>
    <p style="margin-top:.4rem">Generado el {today} &nbsp;·&nbsp; Sesión: 2026-06-16 &nbsp;·&nbsp; Feedback: 2026-06-24 &nbsp;·&nbsp; Fase de Inception v2.0 &nbsp;·&nbsp; imagineapps.co</p>
  </footer>

</main>
</div>
</body>
</html>"""

    OUT.write_text(html, encoding='utf-8')
    size_kb = OUT.stat().st_size / 1024
    print(f"✅ Generado: {OUT.name}  ({size_kb:.0f} KB)")
    print(f"   Tablas: {len(tables)}  ·  Enums: {len(enums)}")
    print(f"   Sitemaps: {num_sitemaps}")
    print(f"   Abre en el navegador:")
    print(f"   file://{OUT}")

if __name__ == '__main__':
    generate()
