# Propuesta de Navegación — G&H Sistema de Gestión
**Inception Report · G&H Obras y Estructuras Metálicas S.A.S**
Versión 1.0 — 2026-07-04 · Autor: UX/IA Review

---

## Principio de organización

La información fluye de **alto nivel de negocio → detalle técnico**:

```
Negocio (¿qué es?) → Proceso (¿cómo opera?) → Actores (¿quién?) →
Módulos (¿cómo funciona cada área?) → Pantallas (¿qué ve el usuario?) →
Requisitos (¿qué se valida?) → Técnica (¿cómo se construye?)
```

---

## Estructura de Navegación Propuesta

```
G&H Sistema — Inception Report
│
├── [SIDEBAR GRUPO 1] ─── Visión y Contexto
│   └── #overview ............... Resumen Ejecutivo del Proyecto
│
├── [SIDEBAR GRUPO 2] ─── Proceso de Negocio
│   └── #flujo-principal ........ Flujo Principal del Negocio
│
├── [SIDEBAR GRUPO 3] ─── Actores del Sistema
│   └── #roles .................. Roles y Permisos
│       ├── Descripción de roles (12 roles)
│       ├── Matriz RBAC por módulo
│       └── Diagrama de roles y acciones
│
├── [SIDEBAR GRUPO 4] ─── Flujos por Módulo
│   ├── #cotizacion ............. Módulo de Cotizaciones
│   ├── #registro-cliente ....... Registro y Aprobación de Clientes
│   └── #inventarios ............ Inventarios y Logística
│
├── [SIDEBAR GRUPO 5] ─── Mapas de Pantallas (Sitemaps)
│   ├── #sitemap-auth ........... Autenticación y Dashboard
│   ├── #sitemap-clientes ....... Clientes
│   ├── #sitemap-cotizaciones ... Cotizaciones
│   ├── #sitemap-contratos ...... Contratos
│   ├── #sitemap-inventarios .... Inventarios
│   ├── #sitemap-facturacion .... Facturación y Cartera
│   └── #sitemap-auditoria ...... Auditoría y Configuración
│
├── [SIDEBAR GRUPO 6] ─── Requerimientos Funcionales
│   ├── #historias .............. Historias de Usuario
│   └── #checklist .............. Checklist Validado
│
└── [SIDEBAR GRUPO 7] ─── Arquitectura Técnica
    ├── #arquitectura ........... Arquitectura del Sistema
    └── #database ............... Esquema de Base de Datos
```

---

## Detalle de cada sección

---

### GRUPO 1 — Visión y Contexto
**Propósito:** Orientar al lector. Primer contacto con el proyecto.

#### `#overview` — Resumen Ejecutivo del Proyecto
*Anchor actual: `#overview` — sin cambios*

Contenido que aloja:
- **Hero header:** nombre del sistema, empresa, fecha, chips de métricas rápidas
- **Métricas de escala:** ~180 clientes, 50 obras/cliente, 3–4 frentes/obra, 6–12 cotizaciones/dibujante/semana
- **Módulos del sistema (10):** lista numerada con descripción breve
- **Stack tecnológico:** React + TypeScript, FastAPI, PostgreSQL, Ooku, Siigo→DIAN, S3, Email/WhatsApp, Geocoding
- **Roles del sistema (12):** chips visuales por rol
- **Callout SEM-27:** resumen de los principales cambios de la semana 27
- **Callout ciudades y documentos de referencia**

> **Razón de posición:** Es el punto de entrada. Cualquier persona que abra el reporte debe entender en 30 segundos qué es G&H, qué problema resuelve el sistema, a qué escala opera y con qué tecnología.

---

### GRUPO 2 — Proceso de Negocio
**Propósito:** Mostrar el ciclo completo de operación antes de entrar en módulos.

#### `#flujo-principal` — Flujo Principal del Negocio
*Anchor actual: `#flujo-principal` — sin cambios*

Contenido que aloja:
- **Diagrama:** `01_flujo_principal_gyh.mmd`
- Ciclo completo: Cotización → Aprobación multi-área → Contrato → Almacén (pedidos, despacho, devolución) → Facturación (proforma → Siigo → DIAN/CUFE) → Cartera
- Incluye flujos SEM-27: pedidos parciales, verificación 3 fuentes, centros de costo 13/14, modalidades de factura, catálogos duales

> **Razón de posición:** El lector ve el macro-proceso antes de entrar en el detalle de roles o módulos. Esto establece el contexto que hace que todo lo demás tenga sentido.

---

### GRUPO 3 — Actores del Sistema
**Propósito:** Definir quién opera cada parte del proceso antes de ver los módulos.

#### `#roles` — Roles y Permisos
*Anchor actual: `#roles` — se mueve de posición 7 a posición 3*

Contenido que aloja (todos los entregables actuales, reordenados internamente):

1. **Descripción de roles (tabla de 12 roles):**
   - CEO/Ingeniero, SuperAdmin, Admin, Comercial, Dibujante, Contabilidad, Facturación, Jurídica, Almacén, Conductor, Despachador, Recepción

2. **Matriz RBAC completa por módulo (tablas Markdown):**
   - Módulo Clientes y Prospectos
   - Módulo Cotizaciones
   - Módulo Contratos
   - Módulo Almacén y Conductores
   - Módulo Facturación
   - Módulo Cartera
   - Auditoría y Configuración

3. **Tablas de referencia de reglas de negocio:**
   - Catálogo de productos — líneas de negocio
   - Tipos de catálogo de precios (general anual vs. especial por cliente)
   - Centros de costo (13 Alquiler · 14 Ventas/Reposiciones)
   - Condiciones de pago
   - Reglas de liquidación de conductores
   - Integración DIAN — flujo Siigo

4. **Diagrama visual de roles:** `06_roles_y_permisos.mmd`

> **Razón de posición:** Conocer los 12 actores y sus permisos es prerequisito para entender los flujos de módulo. La pregunta "¿quién puede hacer qué?" se responde aquí antes de entrar en detalle en cada módulo.

---

### GRUPO 4 — Flujos por Módulo
**Propósito:** Profundizar en los módulos de negocio más complejos con sus diagramas de flujo detallados.

#### `#cotizacion` — Módulo de Cotizaciones
*Anchor actual: `#cotizacion` — sin cambios*

Contenido que aloja:
- **Diagrama:** `03_modulo_cotizacion.mmd`
- Flujo: Dibujante (carga planos, importa Excel AutoCAD, consulta catálogo dual) → Comercial (valores comerciales, precios especiales, notificación por escrito a Facturación) → Contabilidad (retenciones por tipo, centros de costo) → Salida (PDF + Orden de Compra)
- SEM-27 incluido: catálogos duales, precio transporte por peso Y volumen, retenciones diferenciadas

---

#### `#registro-cliente` — Registro y Aprobación de Clientes
*Anchor actual: `#registro-cliente` — sin cambios*

Contenido que aloja:
- **Diagrama:** `04_registro_aprobacion_cliente.mmd`
- Flujo: Formulario FT-AC-001 (9 secciones) → Aprobación simultánea 3 áreas (Contabilidad + Jurídica + Comercial) → CEO fuerza aprobación si aplica → Activación de operaciones
- Campos específicos: tipo de dominio de correo, sistema contable del cliente (impactan cartera)
- Caso fiducia: Facturación puede editar nombre de facturación

---

#### `#inventarios` — Inventarios y Logística
*Anchor actual: `#inventarios` — sin cambios*

Contenido que aloja:
- **Diagrama:** `05_modulo_inventarios_logistica.mmd`
- Flujo: Cronograma Recepción (Viviana) → Autorización ingeniero → Remisión de salida → Pedidos parciales (¿completo? → inicio contador alquiler) → Devolución (verificación 3 fuentes: conductor + despachador + fotos portería) → Inspección 6 estados (OK/Dañado/Baja/Mantenimiento/Faltante/Ajeno) → Préstamo entre frentes
- SEM-27 incluido: 8 hallazgos de inventario aplicados en el diagrama

---

### GRUPO 5 — Mapas de Pantallas (Sitemaps)
**Propósito:** Mostrar qué pantallas y rutas existen en la aplicación por módulo. Artefacto UX/UI.

> **Cambio clave respecto al estado actual:** Los 7 sitemaps pasan de estar todos en un único `#sitemaps` a tener **anclas individuales**, lo que permite navegar directamente al sitemap de un módulo específico desde el sidebar.

---

#### `#sitemap-auth` — Autenticación y Dashboard
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_01_auth_dashboard.mmd`

Contenido:
- `/login` — Iniciar sesión
- `/forgot-password` — Recuperar contraseña
- `/dashboard` — KPIs y métricas · Alertas pendientes · Actividad reciente

---

#### `#sitemap-clientes` — Clientes
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_02_clientes.mmd`

Contenido:
- `/clientes` — Lista de clientes y prospectos
- `/clientes/nuevo` — Formulario FT-AC-001 (nuevo cliente)
- `/clientes/:id` — Detalle del cliente
  - `/clientes/:id/registro` — Formulario FT-AC-001 (edición)
  - `/clientes/:id/documentos` — Documentos adjuntos
  - `/clientes/:id/aprobacion` — Aprobación multi-área
  - `/clientes/:id/obras` — Obras y frentes
  - `/clientes/:id/historial` — Historial de conceptos

---

#### `#sitemap-cotizaciones` — Cotizaciones
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_03_cotizaciones.mmd`

Contenido:
- `/cotizaciones` — Lista de cotizaciones
- `/cotizaciones/nueva` — Nueva cotización
- `/cotizaciones/:id` — Detalle
  - `/cotizaciones/:id/planos` — Carga de planos (DWG/DXF/PDF)
  - `/cotizaciones/:id/materiales` — Desglose de materiales (importación Excel)
  - `/cotizaciones/:id/items` — Ítems y precios (Venta · Alquiler · Transporte · Reposición)
  - `/cotizaciones/:id/pdf` — Generar y enviar PDF
- `/catalogo` — Catálogo de precios (general + especial por cliente)

---

#### `#sitemap-contratos` — Contratos
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_04_contratos.mmd`

Contenido:
- `/contratos` — Lista de contratos
- `/contratos/:id/orden-compra` — Orden de compra
- `/contratos/:id/firma` — Firma electrónica vía Ooku
- `/contratos/:id/estado` — Estado del contrato (Pendiente → Firmado → Activo)

---

#### `#sitemap-inventarios` — Inventarios
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_05_inventarios.mmd`

Contenido:
- `/inventarios/stock` — Stock / Kardex (Bodega + Clientes + Producción)
- `/inventarios/pedidos` — Pedidos (Estado: Pendiente · Parcial · Completo · Cancelado)
  - `/inventarios/pedidos/:id/parciales` — Envíos parciales acumulados
- `/inventarios/remisiones` — Remisiones de salida
  - `/inventarios/remisiones/nueva` — Nueva remisión
- `/inventarios/devoluciones` — Devoluciones
  - `/inventarios/devoluciones/inspeccion` — Inspección 3 fuentes + clasificación 6 estados
- `/inventarios/devoluciones/ajeno` — Equipos ajenos (no son de G&H)
- `/inventarios/prestamos-frentes` — Préstamo de equipo entre frentes
- `/inventarios/agenda` — Agenda de transporte (conductores + vehículos)
- `/inventarios/conductores` — Gestión de conductores (disponibilidad, indisponibilidad, km)
- `/inventarios/cronograma` — Cronograma diario de recogidas (Recepción ↔ Almacén)
- `/inventarios/cancelaciones` — Cancelaciones de pedidos
- `/inventarios/alertas` — Próximas recogidas (alertas proactivas)

---

#### `#sitemap-facturacion` — Facturación y Cartera
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_06_facturacion.mmd`

Sub-módulo Facturación:
- `/facturacion/facturas` — Lista de facturas
  - `/facturacion/facturas/nueva` — Nueva factura (selección modalidad: por remisión · consolidada · por valor)
  - `/facturacion/facturas/:id` — Detalle de factura
  - `/facturacion/facturas/:id/dian` — Estado CUFE / Radian (validación envío DIAN)
  - `/facturacion/facturas/:id/pago` — Registrar pago
- `/facturacion/proformas` — Proformas (previa aprobación cliente)
- `/facturacion/cortes` — Cortes mensuales por cliente
- `/facturacion/centros-costo` — Centros de costo (13 Alquiler · 14 Ventas)
- `/facturacion/retenciones` — Retenciones por tipo de concepto
- `/facturacion/catalogo/general` — Catálogo general anual de precios
- `/facturacion/catalogo/especiales` — Precios especiales por cliente

Sub-módulo Cartera (independiente):
- `/cartera` — Vista de cartera (mora · días vencidos · monto pendiente)
- `/cartera/gestion` — Registrar gestión de cobro (notas · acuerdos · estados)
  - Estados: Nueva · En Gestión · Acuerdo de Pago · Demanda · Castigada · Recuperada
- `/cartera/juridico` — Cobro jurídico

---

#### `#sitemap-auditoria` — Auditoría y Configuración
*Anchor actual: parte de `#sitemaps` — se divide en anchor propio*
Fuente: `sitemaps/sitemap_07_auditoria_config.mmd`

Sub-módulo Auditoría:
- `/auditoria/log` — Log global (Quién · Cuándo · Qué · Módulo · IP)
- `/auditoria/usuario/:id` — Log filtrado por usuario
- `/auditoria/modulo/:name` — Log filtrado por módulo

Sub-módulo Reportería:
- `/reporteria` — Dashboard de reportes
  - Kardex por período · Facturas emitidas vs. pagadas · Cartera por antigüedad
  - Rotación de equipos · Conductores y trayectos · Cotizaciones por estado
- `/reporteria/exportar` — Exportación Excel / PDF

Sub-módulo Configuración:
- `/configuracion/usuarios` — Gestión de usuarios y roles (RBAC)
- `/configuracion/catalogo` — Catálogo de productos y líneas de negocio
- `/configuracion/precios-especiales` — Catálogos especiales por cliente
- `/configuracion/notificaciones` — Configuración de eventos y alertas (SuperAdmin)
- `/configuracion/conductores` — Reglas de conductores (km · combustible · peso/volumen)
- `/configuracion/firma` — Integración Ooku (API Keys)
- `/configuracion/global` — Parámetros globales del sistema (solo SuperAdmin)

---

### GRUPO 6 — Requerimientos Funcionales
**Propósito:** Especificaciones detalladas en lenguaje de negocio. El "qué" antes del "cómo".

#### `#historias` — Historias de Usuario
*Anchor actual: `#historias` — sin cambios*

Contenido que aloja (23 historias de usuario + resumen de métricas de escala):

**Módulo 1 — Cotizaciones**
- US-001: Creación de cotización técnica por dibujante
- US-002: Completar cotización con valores comerciales
- US-003: Consulta de catálogos de precios

**Módulo 2 — Registro y Aprobación de Clientes**
- US-004: Diligenciar formulario único FT-AC-001
- US-005: Dar concepto de aprobación de cliente
- US-006: Ver historial de aprobaciones

**Módulo 3 — Contratos y Firma Electrónica**
- US-007: Gestionar contratos para clientes nuevos y existentes

**Módulo 4 — Almacén / Pedidos y Logística**
- US-008: Gestionar pedidos parciales y control de despacho
- US-009: Programar agenda de transporte y gestión de conductores
- US-010: Registrar devolución con verificación 3 fuentes y clasificar estado
- US-015: Cronograma diario de recogidas y cortes (Recepción)
- US-016: Registrar y gestionar equipo ajeno

**Módulo 5 — Facturación**
- US-011: Generar proforma, factura y enviar a Siigo/DIAN
- US-017: Configurar modalidad de facturación por cliente
- US-018: Gestionar cortes mensuales por cliente
- US-019: Gestionar flujo Siigo → DIAN y seguimiento de factura
- US-012: Gestionar cartera de clientes en mora
- US-020: Editar datos de cliente para facturación (caso fiducia/consorcio)

**Módulo 6 — Cartera (independiente)**
- US-021: Gestionar estrategia de cobro según tipo de dominio de correo

**Módulo 7 — Reportería**
- US-022: Generar reportes de operaciones

**Módulo 8 — Auditoría y Notificaciones (Transversal)**
- US-013: Consultar log global de auditoría
- US-014: Recibir notificaciones de procesos pendientes
- US-023: Configuración de reglas de negocio por SuperAdmin

---

#### `#checklist` — Checklist Validado
*Anchor actual: `#checklist` — sin cambios*

Contenido que aloja (todos los ítems validados agrupados por módulo):
- ✅ Módulo de Clientes y Aprobación (10 ítems)
- ✅ Módulo de Cotizaciones (12 ítems)
- ✅ Módulo de Contratos (5 ítems)
- ✅ Módulo de Almacén / Inventarios y Logística (18 ítems)
- ✅ Módulo de Facturación (12 ítems)
- ✅ Módulo de Cartera (4 ítems)
- ✅ Módulo de Reportería (4 ítems)
- ✅ Módulo de Auditoría (4 ítems)
- ✅ Módulo de Notificaciones (4 ítems)
- ✅ Configuración y Seguridad (7 ítems + 12 roles)
- 📌 Pendientes (8 ítems abiertos)

---

### GRUPO 7 — Arquitectura Técnica
**Propósito:** El "cómo se construye". Solo se consulta una vez comprendido el negocio.

#### `#arquitectura` — Arquitectura del Sistema
*Anchor actual: `#arquitectura` — se mueve de posición 2 a posición 6*
Fuente: `architecture/02_arquitectura_sistema.mmd`

Contenido que aloja:
- **Diagrama de arquitectura completo:** React + FastAPI + PostgreSQL + Integraciones externas
- Usuarios (12 roles) → Frontend (10 módulos) → Backend (12 servicios) → Base de Datos (9 grupos) → Storage S3 → Integraciones externas (Ooku, Email, WhatsApp, DIAN/Radian, Maps/Geocoding)

---

#### `#database` — Esquema de Base de Datos
*Anchor actual: `#database` — se mueve de posición 4 a posición 7 (última)*
Fuente: `database/gyh_schema.dbml`

Contenido que aloja:
- **Enums del sistema** (estados de pedido, estados de factura, tipos de retención, estados de equipo, etc.)
- **42 tablas PostgreSQL** agrupadas por dominio:
  - Usuarios y acceso
  - Clientes y prospectos
  - Cotizaciones y catálogo
  - Contratos
  - Almacén, pedidos, remisiones, conductores
  - Facturación, proformas, cartera
  - Auditoría y notificaciones
- **SQL completo** (sección expandible / `<details>`)

---

## Comparativa: Estado Actual vs. Propuesta

| # | Estado Actual (sidebar) | # | Propuesta (sidebar) | Cambio |
|---|------------------------|---|---------------------|--------|
| 1 | Visión General → Resumen | 1 | Visión y Contexto → Resumen | = sin cambio |
| 2 | Arquitectura → **Arquitectura del Sistema** | 2 | Proceso de Negocio → **Flujo Principal** | ↕ se intercambian |
| 3 | Arquitectura → **Flujo Principal** | 3 | Actores → **Roles y Permisos** | ↑ sube de posición 7 |
| 4 | Arquitectura → **Cotizaciones** | 4 | Módulos → **Cotizaciones** | ≈ mismo lugar |
| 5 | Arquitectura → **Registro y Aprobación** | 5 | Módulos → **Registro y Aprobación** | ≈ mismo lugar |
| 6 | Arquitectura → **Inventarios** | 6 | Módulos → **Inventarios** | ≈ mismo lugar |
| 7 | Arquitectura → **Roles y Permisos** | 7 | Sitemaps → **Auth · Dashboard** | ↓ baja de posición 2 |
| 8 | Sitemaps → Auth · Dashboard | 8 | Sitemaps → **Clientes** | Se individualizan |
| 9 | Sitemaps → Clientes · Cotizaciones | 9 | Sitemaps → **Cotizaciones** | Se individualizan |
| 10 | Sitemaps → Inventarios · Facturación | 10 | Sitemaps → **Contratos** | Se individualizan |
| 11 | Sitemaps → Auditoría · Config | 11 | Sitemaps → **Inventarios** | Se individualizan |
| 12 | Base de Datos → **Schema PostgreSQL** | 12 | Sitemaps → **Facturación y Cartera** | Se individualizan |
| 13 | Requerimientos → **Historias de Usuario** | 13 | Sitemaps → **Auditoría y Config** | Se individualizan |
| 14 | Requerimientos → **Checklist Validado** | 14 | Requerimientos → **Historias de Usuario** | ≈ mismo lugar |
| — | — | 15 | Requerimientos → **Checklist Validado** | ≈ mismo lugar |
| — | — | 16 | Técnica → **Arquitectura del Sistema** | ↓ baja al final |
| — | — | 17 | Técnica → **Schema PostgreSQL** | ↓ baja al final |

**Cambios clave:**
1. `Arquitectura del Sistema` (el diagrama más técnico) se mueve del principio al final
2. `Flujo Principal del Negocio` sube a segundo lugar — es el contexto macro de todo
3. `Roles y Permisos` sube antes de los módulos, porque los actores explican quién hace qué en cada módulo
4. Los 7 sitemaps pasan de estar **agrupados en un link** a tener **anclas individuales** en el sidebar, lo que elimina el scroll oculto dentro de la sección y permite navegación directa

---

## Nuevo marcado del sidebar (HTML)

```html
<nav>
  <div class="nav-brand">
    <span class="nav-logo">G&amp;H</span>
    <div><strong>G&amp;H Sistema</strong><small>Inception Report · 2026</small></div>
  </div>

  <!-- GRUPO 1 -->
  <div class="nav-group">Visión y Contexto</div>
  <a href="#overview">📊 Resumen Ejecutivo</a>

  <!-- GRUPO 2 -->
  <div class="nav-group">Proceso de Negocio</div>
  <a href="#flujo-principal">🔄 Flujo Principal del Negocio</a>

  <!-- GRUPO 3 -->
  <div class="nav-group">Actores del Sistema</div>
  <a href="#roles">🔐 Roles y Permisos</a>

  <!-- GRUPO 4 -->
  <div class="nav-group">Flujos por Módulo</div>
  <a href="#cotizacion">📋 Cotizaciones</a>
  <a href="#registro-cliente">👥 Registro y Aprobación</a>
  <a href="#inventarios">📦 Inventarios y Logística</a>

  <!-- GRUPO 5 -->
  <div class="nav-group">Mapas de Pantallas</div>
  <a href="#sitemap-auth">🔐 Auth · Dashboard</a>
  <a href="#sitemap-clientes">👥 Clientes</a>
  <a href="#sitemap-cotizaciones">📋 Cotizaciones</a>
  <a href="#sitemap-contratos">📝 Contratos</a>
  <a href="#sitemap-inventarios">📦 Inventarios</a>
  <a href="#sitemap-facturacion">💳 Facturación · Cartera</a>
  <a href="#sitemap-auditoria">🔍 Auditoría · Config</a>

  <!-- GRUPO 6 -->
  <div class="nav-group">Requerimientos Funcionales</div>
  <a href="#historias">📖 Historias de Usuario</a>
  <a href="#checklist">✅ Checklist Validado</a>

  <!-- GRUPO 7 -->
  <div class="nav-group">Arquitectura Técnica</div>
  <a href="#arquitectura">🏗️ Arquitectura del Sistema</a>
  <a href="#database">🗄️ Esquema de Base de Datos</a>
</nav>
```

---

## Notas de implementación

1. **Ningún contenido se elimina ni resume** — todos los entregables existentes se conservan íntegramente.
2. **El `#sitemaps` se divide en 7 secciones con anclas propias** (`#sitemap-auth`, `#sitemap-clientes`, etc.) para habilitar la navegación directa desde el sidebar. En el `generate_report.py`, cada sitemap `.mmd` genera su propia `<section id="sitemap-xxx">` en lugar de todas dentro de una sola `<section id="sitemaps">`.
3. **La `<section id="roles">` se mueve físicamente** antes del bloque de `#cotizacion` en el HTML generado.
4. **Las secciones `#arquitectura` y `#database`** se mueven al final del `<main>`, después del `#checklist`.
5. **El `generate_report.py`** requiere reordenar el bloque de `sections_order` para que produzca el HTML en el nuevo orden.
