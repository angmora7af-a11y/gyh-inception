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

def roles_section(tabla_md, mmd_path=None):
    tabla_html = md2html(tabla_md)
    return f'''
<section id="roles">
  <div class="section-header">
    <h2>Roles y Permisos (RBAC)</h2>
    <p class="section-sub">12 roles · SuperAdmin · Admin · CEO/Ingeniero · Comercial · Dibujante · Contabilidad · Facturación · Jurídica · Almacén · Despachador · Conductor · Recepción</p>
  </div>
  <div class="callout warn">
    <strong>SEM-27:</strong> Roles <strong>Despachador</strong> y <strong>Recepción</strong> agregados.
    <strong>Facturación</strong> separada de Contabilidad como rol independiente.
    <strong>SuperAdmin</strong> para configuración global del sistema.
    El <strong>CEO/Ingeniero</strong> conserva perfil de consulta, acceso a motivos de rechazo y aprobación forzada.
  </div>
  <div class="md-content">{tabla_html}</div>
</section>'''

def db_section(tables, enums, raw):
    # Enum pills
    enum_html = ''
    for e in enums:
        vals = ', '.join(e['values'][:6])
        more = f' +{len(e["values"])-6}' if len(e['values']) > 6 else ''
        enum_html += f'<div class="enum-pill"><strong>{e["name"]}</strong><span class="enum-vals">{vals}{more}</span></div>\n'

    MODULE_COLORS = {
        'usuarios': '#0B3C5D', 'auditoria': '#0B3C5D', 'notificaciones': '#0B3C5D',
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
        color = '#0B3C5D'
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
    <h2>Esquema de Base de Datos — PostgreSQL</h2>
    <p class="section-sub">DBML v1.0 · {len(tables)} tablas · {len(enums)} enumeraciones · Escala: ~180 clientes · 50 obras · 3-4 frentes</p>
  </div>
  <div class="callout">
    <strong>Motor:</strong> PostgreSQL &nbsp;·&nbsp;
    <strong>Basado en:</strong> FT-AC-001 v2.0 · Checklist Validación Clientes · Autorización Centrales de Riesgo
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
    <h2>Resumen Ejecutivo del Proyecto</h2>
    <p class="section-sub">G&H Obras y Estructuras Metálicas S.A.S · NIT: 901.218.896-8 · Bogotá · SEM-27 actualizado 2026-07-04</p>
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
      </ul>
    </div>
    <div class="info-card">
      <h3>Stack Tecnológico</h3>
      <ul class="stack-list">
        <li><span class="stack-tag fe">Frontend</span> React + TypeScript</li>
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
    <h3>Roles del Sistema (12)</h3>
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
      <div class="role-chip admin">👑 Admin</div>
      <div class="role-chip admin">🛡️ SuperAdmin</div>
      <div class="role-chip ceo">🏗️ CEO/Ingeniero</div>
    </div>
  </div>

  <div class="callout" style="margin-top:1.25rem">
    <strong>🆕 SEM-27 — Principales cambios:</strong>
    Pedidos parciales (alquiler inicia al completarse) ·
    Verificación 3 fuentes en devoluciones ·
    6 estados de equipos (+ Baja) ·
    Roles Despachador · Recepción · Facturación · SuperAdmin ·
    Integración Siigo→DIAN (no directa) ·
    Proforma antes de factura ·
    Transporte: G&H o Cliente ·
    Catálogos duales · Centros de costo 13/14 ·
    Condiciones de pago por cliente ·
    Módulo Reportería · Cartera independiente
  </div>

  <div class="callout warn" style="margin-top:.75rem">
    <strong>📍 Ciudades:</strong> Bogotá (130 clientes) · Ibagué + Armenia (50 clientes) &nbsp;·&nbsp;
    <strong>Documentos de referencia:</strong> FT-AC-001 v2.0 · CHECKLIST VALIDACION CLIENTES BOGOTA ·
    Autorización Centrales de Riesgo (Ley 1581/2012 · Circular 09/2016)
  </div>
</section>'''

# ─── CSS — Design System GYH Bogotá ──────────────────────────────────────────

CSS = """
/* ── Google Fonts se cargan en el <head> vía <link> ── */

:root {
  /* Color tokens — GYH Bogotá Design System */
  --bg:       #F9F9F9;   /* Grey/50  */
  --surface:  #FFFFFF;
  --surface2: #F2F2F2;   /* Grey/100 */
  --border:   #E0E0E0;   /* Grey/200 */
  --text:     #1A1A1A;   /* Main/Black */
  --muted:    #777777;   /* Grey/500 */
  --primary:  #0B3C5D;   /* Main/Corporate Blue */
  --primary2: #328CC1;   /* Secondary/Light Blue */
  --accent:   #F5A623;   /* Main/Construction Yellow */
  --accent2:  #D4901F;   /* accent darkened */
  --steel:      #333333;   /* Grey/800 */
  --grey-300:   #CCCCCC;   /* Grey/300 — secondary icons tint */
  --grey-900:   #1C1C1C;   /* Grey/900 — footer block bg */
  --nav-dark:   #072B44;   /* sidebar header bg */
  --success:    #38A169;
  --danger:     #E53E3E;
  --nav-w:      270px;
  /* Shadow tokens */
  --shadow-low: 0px 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-med: 0px 4px 10px rgba(0, 0, 0, 0.12);
  /* Radius tokens */
  --r-sm: 4px;
  --r-md: 8px;
  --r-lg: 12px;
  /* Spacing tokens */
  --sp-xs:   4px;
  --sp-s:    8px;
  --sp-m:   16px;
  --sp-l:   24px;
  --sp-xl:  32px;
  --sp-xxl: 48px;
  --sp-hug: 64px;
  /* Motion tokens */
  --transition-fast:   200ms ease-in-out;
  --transition-normal: 350ms ease;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Open Sans', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.65;
  font-size: 15px;
}

/* ── Layout ── */
.layout { display: grid; grid-template-columns: var(--nav-w) 1fr; min-height: 100vh; }
@media (max-width: 960px) {
  .layout { grid-template-columns: 1fr; }
  nav { position: relative; height: auto; width: 100%; }
}

/* ── Sidebar ── */
nav {
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  background: var(--primary);
  color: #fff;
  padding: 0 0 2rem;
  font-size: .82rem;
  box-shadow: var(--shadow-med);
  font-family: 'Open Sans', system-ui, sans-serif;
}
.nav-brand {
  display: flex; align-items: center; gap: .75rem;
  padding: 1.25rem 1rem;
  background: var(--nav-dark);
  border-bottom: 1px solid rgba(255,255,255,.1);
  margin-bottom: .5rem;
}
.nav-logo {
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
}
.nav-brand strong {
  display: block;
  color: #fff;
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: .85rem;
  font-weight: 700;
  line-height: 1.3;
}
.nav-brand small { color: rgba(255,255,255,.45); font-size: .68rem; }
.nav-group {
  font-size: .6rem;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: rgba(255,255,255,.35);
  padding: 1rem 1rem .3rem;
  font-family: 'Montserrat', system-ui, sans-serif;
  font-weight: 600;
}
nav a {
  display: block;
  padding: .4rem 1rem;
  color: rgba(255,255,255,.68);
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all var(--transition-fast);
}
nav a:hover,
nav a.active {
  color: var(--accent);
  background: rgba(255,255,255,.07);
  border-left-color: var(--accent);
}

/* ── Main ── */
main {
  padding: 2rem 2.5rem 4rem;
  background: var(--bg);
  max-width: 1200px;    /* Grid — Desktop Layout: max-width 1200px */
}
@media (max-width: 720px) { main { padding: 1rem 1rem 3rem; } }

/* ── Hero ── */
.hero {
  background: linear-gradient(135deg, var(--primary) 0%, #0E5080 100%);
  color: #fff;
  border-radius: var(--r-lg);
  padding: 2.5rem 2rem;
  margin-bottom: 2.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-med);
}
.hero::before {
  content: '';
  position: absolute; right: -80px; top: -80px;
  width: 260px; height: 260px;
  border-radius: 50%;
  background: rgba(245,166,35,.12);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute; right: 40px; bottom: -40px;
  width: 140px; height: 140px;
  border-radius: 50%;
  background: rgba(255,255,255,.06);
  pointer-events: none;
}
.hero-tag {
  font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  color: var(--accent);
  font-weight: 700;
  margin-bottom: .5rem;
  font-family: 'Montserrat', system-ui, sans-serif;
}
.hero h1 {
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: .4rem;
  letter-spacing: -.02em;
}
.hero p { color: rgba(255,255,255,.62); font-size: .92rem; }
.hero-meta { display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1.5rem; }
.hero-chip {
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;
  padding: .22rem .72rem;
  font-size: .73rem;
  color: rgba(255,255,255,.85);
}

/* ── Sections ── */
section { margin-bottom: 3.5rem; scroll-margin-top: 1rem; }
.section-header { margin-bottom: 1.5rem; padding-bottom: .7rem; border-bottom: 3px solid var(--accent); }
.section-header h2 {
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 1.4rem;
  color: var(--primary);
  font-weight: 800;
  letter-spacing: -.01em;
}
.section-sub { color: var(--muted); font-size: .84rem; margin-top: .3rem; }
section h3 {
  font-family: 'Montserrat', system-ui, sans-serif;
  font-size: 1rem;
  color: var(--primary);
  margin: 1.75rem 0 .75rem;
  font-weight: 700;
}

/* ── Diagrams ── */
.diagram-block {
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--shadow-low);
  margin-bottom: 1rem;
}
.diagram-label {
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
}
.btn-dl-svg {
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
}
.btn-dl-svg:hover { background: var(--accent2); transform: translateY(-1px); }
.btn-dl-svg:active { transform: translateY(0); }
.btn-dl-svg.loading { opacity: .6; cursor: wait; }
.mermaid-wrap { padding: 1.5rem; overflow-x: auto; background: #fff; min-height: 80px; }
.mmd-svg-wrap svg { max-width: 100%; height: auto; }

/* ── Metrics ── */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
  gap: .9rem;
  margin-bottom: 1.5rem;
}
.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.2rem 1rem;
  text-align: center;
  border-top: 4px solid var(--accent);
  box-shadow: var(--shadow-low);
  transition: box-shadow var(--transition-fast);
}
.metric-card:hover { box-shadow: var(--shadow-med); }
.metric-icon { display: block; font-size: 1.65rem; margin-bottom: .45rem; }
.metric-value {
  display: block;
  font-size: 1.65rem;
  font-weight: 900;
  color: var(--primary);
  font-family: 'Montserrat', system-ui, sans-serif;
  letter-spacing: -.02em;
}
.metric-label { display: block; font-size: .66rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; margin-top: .2rem; }

/* ── Info cards ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
@media (max-width: 680px) { .two-col { grid-template-columns: 1fr; } }
.info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1.25rem;
  box-shadow: var(--shadow-low);
}
.info-card h3 {
  color: var(--primary);
  font-size: .95rem;
  font-family: 'Montserrat', system-ui, sans-serif;
  font-weight: 700;
  margin-bottom: .75rem;
  border-bottom: 1px solid var(--surface2);
  padding-bottom: .4rem;
}
.module-list, .stack-list { list-style: none; }
.module-list li, .stack-list li {
  padding: .35rem 0;
  border-bottom: 1px solid var(--surface2);
  font-size: .84rem;
  color: var(--steel);
  display: flex;
  align-items: center;
  gap: .5rem;
}
.module-list li:last-child, .stack-list li:last-child { border-bottom: none; }
.mod-badge {
  background: var(--primary);
  color: #fff;
  border-radius: var(--r-sm);
  padding: .1rem .4rem;
  font-size: .66rem;
  font-weight: 700;
  font-family: 'Montserrat', system-ui, sans-serif;
  flex-shrink: 0;
}
.stack-tag {
  padding: .12rem .45rem;
  border-radius: var(--r-sm);
  font-size: .66rem;
  font-weight: 700;
  font-family: 'Montserrat', system-ui, sans-serif;
  flex-shrink: 0;
}
.stack-tag.fe { background: #EBF8FF; color: #2B6CB0; }
.stack-tag.be { background: #F0FFF4; color: #276749; }
.stack-tag.db { background: #FAF5FF; color: #6B46C1; }
.stack-tag.ex { background: #FFFBEB; color: #92400E; }
.roles-grid { display: flex; flex-wrap: wrap; gap: .5rem; padding-top: .25rem; }
.role-chip {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: .28rem .82rem;
  font-size: .78rem;
  color: var(--primary);
  font-weight: 600;
  font-family: 'Montserrat', system-ui, sans-serif;
}
.role-chip.admin { background: #FFFBEB; border-color: var(--accent); color: #92400E; }
.role-chip.ceo   { background: #FFF5F5; border-color: #E53E3E;        color: #C53030; }

/* ── Callout ── */
.callout {
  background: #EBF8FF;
  border-left: 4px solid var(--primary2);
  border-radius: 0 var(--r-md) var(--r-md) 0;
  padding: .88rem 1.1rem;
  margin: 1rem 0;
  font-size: .84rem;
  line-height: 1.6;
}
.callout.warn { background: #FFFBEB; border-left-color: var(--accent); }

/* ── DB tables ── */
.db-legend { display: flex; flex-wrap: wrap; gap: .6rem; margin-bottom: 1.25rem; }
.db-legend span {
  border: 1px solid;
  border-radius: var(--r-sm);
  padding: .2rem .55rem;
  font-size: .7rem;
  font-weight: 600;
  font-family: 'Montserrat', system-ui, sans-serif;
}
.t-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: .9rem; margin-bottom: 1.5rem; }
.t-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  overflow: hidden;
  box-shadow: var(--shadow-low);
  transition: box-shadow var(--transition-fast);
}
.t-card:hover { box-shadow: var(--shadow-med); }
.t-head {
  background: var(--tcolor, var(--primary));
  color: #fff;
  padding: .55rem .9rem;
  display: flex; align-items: center; gap: .5rem;
}
.t-name { font-weight: 700; font-size: .84rem; flex: 1; font-family: ui-monospace, monospace; }
.t-count { font-size: .64rem; color: rgba(255,255,255,.6); background: rgba(255,255,255,.12); padding: .1rem .4rem; border-radius: 3px; }
.t-note { font-size: .72rem; color: var(--muted); padding: .45rem .8rem; background: var(--surface2); border-bottom: 1px solid var(--border); line-height: 1.4; }
.t-cols { width: 100%; border-collapse: collapse; font-size: .75rem; }
.t-cols td { padding: .28rem .75rem; border-bottom: 1px solid #f1f5f9; }
.t-cols tr:last-child td { border-bottom: none; }
.t-cols td:first-child code { font-size: .74rem; color: var(--primary); font-weight: 600; }
.t-type { color: var(--muted); font-family: ui-monospace, monospace; font-size: .7rem; }
.t-more { font-size: .7rem; color: var(--muted); padding: .35rem .75rem; background: var(--surface2); text-align: center; font-style: italic; }
.badge { display: inline-block; padding: .05rem .3rem; border-radius: 3px; font-size: .6rem; font-weight: 700; margin-right: .15rem; }
.badge.pk   { background: #FEF3C7; color: #92400E; }
.badge.fk   { background: #E0E7FF; color: #3730A3; }
.badge.uniq { background: #D1FAE5; color: #065F46; }
.enum-grid { display: flex; flex-wrap: wrap; gap: .7rem; margin-bottom: 1.5rem; }
.enum-pill {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: .55rem .85rem;
  min-width: 150px;
  box-shadow: var(--shadow-low);
}
.enum-pill strong { display: block; color: var(--primary); font-size: .78rem; margin-bottom: .2rem; font-family: 'Montserrat', system-ui, sans-serif; }
.enum-vals { color: var(--muted); font-size: .7rem; font-family: ui-monospace, monospace; line-height: 1.6; }
details { margin-top: 1rem; }
details summary { cursor: pointer; color: var(--primary); font-size: .86rem; font-weight: 700; padding: .5rem 0; user-select: none; font-family: 'Montserrat', system-ui, sans-serif; }
.code-block {
  background: #072B44;
  color: #E2E8F0;
  border-radius: var(--r-md);
  padding: 1.25rem;
  font-size: .75rem;
  overflow-x: auto;
  line-height: 1.75;
  max-height: 500px;
  overflow-y: auto;
  font-family: ui-monospace, monospace;
  border: 1px solid rgba(255,255,255,.08);
  margin-top: .75rem;
}

/* ── Markdown content ── */
.md-content h1 { font-size: 1.35rem; color: var(--primary); margin: 1.5rem 0 .75rem; border-bottom: 2px solid var(--accent); padding-bottom: .35rem; font-family: 'Montserrat', system-ui, sans-serif; font-weight: 800; }
.md-content h2 { font-size: 1.15rem; color: var(--primary); margin: 2rem 0 .75rem; border-bottom: 1px solid var(--border); padding-bottom: .35rem; font-family: 'Montserrat', system-ui, sans-serif; font-weight: 700; }
.md-content h3 { font-size: .97rem; color: var(--primary2); margin: 1.4rem 0 .5rem; font-family: 'Montserrat', system-ui, sans-serif; font-weight: 700; }
.md-content h4 { font-size: .9rem; color: var(--steel); margin: 1rem 0 .4rem; font-style: italic; }
.md-content p  { margin: .5rem 0; color: var(--text); font-size: .86rem; }
.md-content code { background: var(--surface2); padding: .1rem .38rem; border-radius: var(--r-sm); font-size: .8em; color: #6B46C1; }
.md-content strong { color: var(--primary); }
.md-content hr { border: none; border-top: 2px solid var(--border); margin: 2rem 0; }
.md-content ul.md-list { margin: .5rem 0 .5rem 1.4rem; }
.md-content ol { margin: .5rem 0 .5rem 1.4rem; }
.md-content li { margin: .28rem 0; font-size: .86rem; }
.check-item { list-style: none; display: flex; align-items: flex-start; gap: .5rem; margin-left: -1.4rem; padding: .2rem 0; }
.chk { flex-shrink: 0; width: 1.3rem; text-align: center; color: var(--muted); margin-top: .05rem; font-size: .9rem; }
.chk-ok { color: var(--success); }
.check-item.done { color: #276749; }
.table-wrap { overflow-x: auto; margin: 1rem 0; }
.md-content table { width: 100%; border-collapse: collapse; font-size: .81rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md); overflow: hidden; }
.md-content th { background: var(--primary); color: #fff; padding: .45rem .75rem; text-align: left; font-size: .78rem; font-weight: 700; font-family: 'Montserrat', system-ui, sans-serif; }
.md-content td { padding: .4rem .75rem; border-bottom: 1px solid var(--border); vertical-align: top; text-align: center; }
.md-content td:first-child { text-align: left; }
.md-content tr:nth-child(even) td { background: var(--surface2); }

/* ── Footer ── */
footer { padding-top: 2rem; border-top: 2px solid var(--border); color: var(--muted); font-size: .78rem; margin-top: 2rem; }
footer strong { color: var(--primary); font-family: 'Montserrat', system-ui, sans-serif; }

/* ── Breadcrumb nav-trail (section dividers in sidebar) ── */
.nav-divider { height: 1px; background: rgba(255,255,255,.08); margin: .4rem .75rem; }

@media print { nav { display: none; } .layout { grid-template-columns: 1fr; } body { font-size: 11pt; } }
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
    num_diagrams = 6 + num_sitemaps

    # ── Sitemaps individuales (cada uno con su propio anchor) ──
    sm_auth = diagram_section(
        "sitemap-auth",
        "Mapa de Pantallas — Autenticación y Dashboard",
        "Acceso al sistema · KPIs · Alertas pendientes · Actividad reciente",
        "sitemaps/sitemap_01_auth_dashboard.mmd")

    sm_clientes = diagram_section(
        "sitemap-clientes",
        "Mapa de Pantallas — Clientes",
        "Lista · Formulario FT-AC-001 · Documentos · Aprobación multi-área · Obras y Frentes · Historial",
        "sitemaps/sitemap_02_clientes.mmd")

    sm_cotizaciones = diagram_section(
        "sitemap-cotizaciones",
        "Mapa de Pantallas — Cotizaciones",
        "Carga de planos · Materiales AutoCAD · Ítems y precios · PDF · Catálogo general y especial",
        "sitemaps/sitemap_03_cotizaciones.mmd")

    sm_contratos = diagram_section(
        "sitemap-contratos",
        "Mapa de Pantallas — Contratos",
        "Orden de compra · Firma electrónica Ooku · Estado del contrato (Pendiente → Firmado → Activo)",
        "sitemaps/sitemap_04_contratos.mmd")

    sm_inventarios = diagram_section(
        "sitemap-inventarios",
        "Mapa de Pantallas — Inventarios y Logística",
        "Kardex · Pedidos parciales · Remisiones · Devoluciones 3 fuentes · Agenda · Conductores · Cronograma",
        "sitemaps/sitemap_05_inventarios.mmd")

    sm_facturacion = diagram_section(
        "sitemap-facturacion",
        "Mapa de Pantallas — Facturación y Cartera",
        "Proformas · Facturas · Modalidades · CUFE/DIAN · Centros costo · Cartera independiente",
        "sitemaps/sitemap_06_facturacion.mmd")

    sm_auditoria = diagram_section(
        "sitemap-auditoria",
        "Mapa de Pantallas — Auditoría, Reportería y Configuración",
        "Log inmutable · Reportes KPI · Usuarios/Roles · Catálogo · Notificaciones · Parámetros SuperAdmin",
        "sitemaps/sitemap_07_auditoria_config.mmd")

    html = f"""<!DOCTYPE html>
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
  <style>{CSS}</style>
</head>
<body>
<div class="layout">

<!-- ═══════════════ SIDEBAR ═══════════════ -->
<nav>
  <div class="nav-brand">
    <span class="nav-logo">G&amp;H</span>
    <div><strong>G&amp;H Sistema</strong><small>Inception Report · 2026</small></div>
  </div>

  <div class="nav-group">Visión y Contexto</div>
  <a href="#overview">📊 Resumen Ejecutivo</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Proceso de Negocio</div>
  <a href="#flujo-principal">🔄 Flujo Principal del Negocio</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Actores del Sistema</div>
  <a href="#roles">🔐 Roles y Permisos</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Flujos por Módulo</div>
  <a href="#cotizacion">📋 Cotizaciones</a>
  <a href="#registro-cliente">👥 Registro y Aprobación</a>
  <a href="#inventarios">📦 Inventarios y Logística</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Mapas de Pantallas</div>
  <a href="#sitemap-auth">🔐 Auth · Dashboard</a>
  <a href="#sitemap-clientes">👥 Clientes</a>
  <a href="#sitemap-cotizaciones">📋 Cotizaciones</a>
  <a href="#sitemap-contratos">📝 Contratos</a>
  <a href="#sitemap-inventarios">📦 Inventarios</a>
  <a href="#sitemap-facturacion">💳 Facturación · Cartera</a>
  <a href="#sitemap-auditoria">🔍 Auditoría · Config</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Requerimientos Funcionales</div>
  <a href="#historias">📖 Historias de Usuario</a>
  <a href="#checklist">✅ Checklist Validado</a>

  <div class="nav-divider"></div>
  <div class="nav-group">Arquitectura Técnica</div>
  <a href="#arquitectura">🏗️ Arquitectura del Sistema</a>
  <a href="#database">🗄️ Esquema de Base de Datos</a>
</nav>

<!-- ═══════════════ MAIN ═══════════════ -->
<main>

  <header class="hero">
    <p class="hero-tag">Fase de Inception · Documentación Técnica · G&amp;H Obras y Estructuras Metálicas S.A.S</p>
    <h1>Sistema de Gestión G&amp;H</h1>
    <p>Cotizaciones · Clientes · Contratos · Inventarios · Facturación · Auditoría</p>
    <div class="hero-meta">
      <span class="hero-chip">📅 {today}</span>
      <span class="hero-chip">🗄️ {len(tables)} tablas PostgreSQL</span>
      <span class="hero-chip">📊 {num_diagrams} diagramas Mermaid</span>
      <span class="hero-chip">👤 12 roles del sistema</span>
      <span class="hero-chip">🗺️ {num_sitemaps} sitemaps por módulo</span>
      <span class="hero-chip">🆕 SEM-27 aplicado</span>
    </div>
  </header>

  {OVERVIEW}

  {diagram_section("flujo-principal",
    "Flujo Principal del Negocio",
    "Ciclo completo: Cotización → Aprobación multi-área → Contrato → Almacén → Facturación → Cartera",
    "architecture/01_flujo_principal_gyh.mmd")}

  {roles_section(roles_tabla_md, "architecture/06_roles_y_permisos.mmd")}

  {diagram_section("cotizacion",
    "Módulo de Cotizaciones",
    "Dibujante (AutoCAD 4-6h) → Importar Excel → Catálogo dual → Comercial → Precios especiales → PDF → Orden de Compra",
    "architecture/03_modulo_cotizacion.mmd")}

  {diagram_section("registro-cliente",
    "Registro y Aprobación de Clientes",
    "Formulario FT-AC-001 v2.0 · 9 secciones · Checklist documental · Concepto + nota obligatoria por 3 áreas · Aprobación forzada CEO",
    "architecture/04_registro_aprobacion_cliente.mmd")}

  {diagram_section("inventarios",
    "Inventarios y Logística",
    "Pedidos parciales · Autorización ingeniero · Remisiones · Devolución 3 fuentes · 6 estados · Préstamo entre frentes · Cronograma",
    "architecture/05_modulo_inventarios_logistica.mmd")}

  {sm_auth}
  {sm_clientes}
  {sm_cotizaciones}
  {sm_contratos}
  {sm_inventarios}
  {sm_facturacion}
  {sm_auditoria}

  <section id="historias">
    <div class="section-header">
      <h2>Historias de Usuario</h2>
      <p class="section-sub">23 historias · SEM-27 (2026-07-04) · Criterios de aceptación verificables · Roles asignados</p>
    </div>
    <div class="md-content">{us_html}</div>
  </section>

  <section id="checklist">
    <div class="section-header">
      <h2>Checklist Validado</h2>
      <p class="section-sub">Sesión 2026-06-16 · Feedback 2026-06-24 · SEM-27 2026-07-04 · Cubre todos los módulos del sistema</p>
    </div>
    <div class="md-content">{ck_html}</div>
  </section>

  {diagram_section("arquitectura",
    "Arquitectura del Sistema",
    "React + FastAPI + PostgreSQL · 12 módulos frontend · 12 servicios backend · 9 grupos BD · Ooku · Siigo/DIAN · Maps",
    "architecture/02_arquitectura_sistema.mmd")}

  {db_html}

  <footer>
    <p><strong>G&amp;H Obras y Estructuras Metálicas S.A.S</strong> &nbsp;·&nbsp; NIT: 901.218.896-8 &nbsp;·&nbsp; Calle 64 #112C-27, Engativá, Bogotá — Colombia</p>
    <p style="margin-top:.4rem">Generado el {today} &nbsp;·&nbsp; Sesión: 2026-06-16 &nbsp;·&nbsp; Feedback: 2026-06-24 &nbsp;·&nbsp; SEM-27: 2026-07-04 &nbsp;·&nbsp; imagineapps.co</p>
  </footer>

</main>
</div>
</body>
</html>"""

    OUT.write_text(html, encoding='utf-8')
    size_kb = OUT.stat().st_size / 1024
    print(f"✅ Generado: {OUT.name}  ({size_kb:.0f} KB)")
    print(f"   Tablas: {len(tables)}  ·  Enums: {len(enums)}")
    print(f"   Sitemaps individuales: {num_sitemaps}")
    print(f"   Abre en el navegador:")
    print(f"   file://{OUT}")

if __name__ == '__main__':
    generate()
