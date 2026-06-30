# Checklist Validado — G&H Sistema de Gestión
**Validación cruzada con transcripción sesión 2026-06-16 y formularios FT-AC-001 v2.0**

---

## Estado General

| Módulo | Items | Cubiertos | Estado |
|--------|-------|-----------|--------|
| Datos y Migración | 5 | 5 | ✅ Completo |
| Módulo Comercial y Cotización | 7 | 7 | ✅ Completo |
| Registro y Aprobación de Clientes | 3 | 3 | ✅ Completo |
| Contratos y Firma | 2 | 2 | ✅ Completo |
| Inventarios y Logística | 4 | 4 | ✅ Completo |
| Requerimientos Transversales | 3 | 3 | ✅ Completo |
| **TOTAL** | **24** | **24** | **✅ 100%** |

---

## 1. Checklist de Datos y Métricas de Migración

> Valida la estructura de PostgreSQL para soportar el volumen histórico

- [x] **Capacidad de Carga de Clientes:** Soporte para ~**180 clientes** (130 Bogotá, 50 Ibagué/Armenia).
  - *Cubierto en:* tabla `clientes` con campo `ciudad_sucursal` (enum: bogota, ibague, armenia).

- [x] **Estructura Geográfica / Sucursales:** Campos de segmentación por ciudades core.
  - *Cubierto en:* `clientes.ciudad_sucursal` + índice en la columna para filtrado eficiente.

- [x] **Nivel 1 (Cliente):** Registro único con código de revisión automático.
  - *Cubierto en:* `clientes.codigo_revision` (varchar unique auto-generado).

- [x] **Nivel 2 (Obra):** Hasta **50 obras independientes** por cliente.
  - *Cubierto en:* tabla `obras` con FK a `clientes.id`.

- [x] **Nivel 3 (Frente de Obra):** 3-4 frentes por obra.
  - *Cubierto en:* tabla `frentes_obra` con FK a `obras.id`.

- [x] **Historial de Prospección:** Registro de ~**50 prospectos nuevos/mes** con trazabilidad.
  - *Cubierto en:* `clientes.estado_cliente = 'prospecto'` + campo `created_at` + auditoría.

---

## 2. Checklist para el Módulo Comercial y de Cotización

> Frontend React + Lógica FastAPI para el flujo de preventa

- [x] **Módulo de Dibujantes (Optimización):** Flujo técnico para agilizar proceso actual (4-6 horas AutoCAD).
  - *Cubierto en:* tabla `cotizaciones` con `horas_modelamiento` + flujo en `03_modulo_cotizacion.mmd`.
  - *Historia de usuario:* US-001.

- [x] **Carga y Lectura de Archivos:** Canal para planos (DWG/DXF) y exportación/importación Excel.
  - *Cubierto en:* tabla `archivos_planos` (formatos: dwg, dxf, pdf, xlsx) + `cotizaciones.archivo_excel_url`.
  - *Historia de usuario:* US-001, AC-001, AC-003.

- [x] **Integración de Catálogos Oficiales:** Precios del cliente para asignación automática.
  - *Cubierto en:* tabla `catalogo_productos` con precios de venta, alquiler/día y reposición + US-003.

- [x] **Generador de Cotizaciones en PDF:** Export final con valores comerciales e IVA.
  - *Cubierto en:* `cotizaciones.pdf_cotizacion_url` + US-002, AC-005.

- [x] **Venta:** Productos/materiales existentes en catálogo.
  - *Cubierto en:* `cotizacion_items.tipo_item = 'venta'` + `cotizaciones.incluye_venta`.

- [x] **Alquiler:** Equipos y maquinaria temporal.
  - *Cubierto en:* `cotizacion_items.tipo_item = 'alquiler'` + `cotizacion_items.dias_alquiler`.

- [x] **Transporte:** Costos de logística, trayectos ida y vuelta.
  - *Cubierto en:* `tipo_item_cotizacion = 'transporte_ida'` y `'transporte_vuelta'`.

- [x] **Reposición:** Cobros por pérdida o no devolución.
  - *Cubierto en:* `tipo_item_cotizacion = 'reposicion'` + `catalogo_productos.precio_reposicion`.

---

## 3. Checklist Documental para Registro de Clientes

> Reemplaza el formato Excel CHECKLIST VALIDACION CLIENTES BOGOTA

- [x] **Validación de Roles Simultáneos:** Bloqueo hasta que las 3 áreas den concepto.
  - *Cubierto en:* tabla `aprobaciones_cliente` con índice `UNIQUE(cliente_id, area)`.
  - *Lógica:* `estado_cliente` solo avanza a 'aprobado' cuando las 3 áreas tienen `es_favorable = true`.
  - *Historia de usuario:* US-005.

  - [x] **Contabilidad:** Validación financiera y de crédito.
  - [x] **Jurídica:** Validación documental y listas LAFT (Circular 09/2016, Ley 1581/2012).
  - [x] **Comercial:** Validación de la oportunidad de negocio.

- [x] **Conceptos Obligatorios:** Estado Favorable / No Favorable.
  - *Cubierto en:* `aprobaciones_cliente.es_favorable` (boolean) + `estado_aprobacion` (enum).

- [x] **Caja de Anotaciones / Comentarios:** Campo de texto obligatorio por área.
  - *Cubierto en:* `aprobaciones_cliente.concepto` (text, NOT NULL en lógica de negocio).
  - *Historia de usuario:* US-005, AC-002.

- [x] **Formulario FT-AC-001 v2.0 completo:** Secciones I-IX capturadas.
  - *Cubierto en:* tablas `clientes`, `contactos_cliente`, `referencias_bancarias`, `referencias_comerciales`, `accionistas`, `autorizacion_centrales_riesgo`, `documentos_registro`.

---

## 4. Checklist para el Módulo de Contratos y Firma

- [x] **Firma Electrónica:** Integración API con plataformas de firma digital (DocuSign / Okc).
  - *Cubierto en:* tabla `contratos` con campos `plataforma_firma`, `id_documento_externo`, `url_documento_firmado`, `fecha_firma`.
  - *Historia de usuario:* US-007.

- [x] **Transición a Operaciones:** Contrato firmado activa automáticamente el módulo de Inventarios.
  - *Cubierto en:* trigger automático en `contratos.estado = 'firmado'` → `ordenes_compra.estado = 'activa'`.
  - *Historia de usuario:* US-007, AC-005.

---

## 5. Checklist para el Módulo de Inventarios

- [x] **Remisiones de Salida:** Generación automática en el Kardex al despacho.
  - *Cubierto en:* tablas `remisiones` + `remision_items` con actualización de `catalogo_productos.stock_actual`.
  - *Historia de usuario:* US-008.

- [x] **Módulo de Agenda y Próximas Recogidas:** Calendario interactivo para el Jefe de Almacén.
  - *Cubierto en:* tabla `agenda_transporte` + `sitemap → /inventarios/agenda`.
  - *Historia de usuario:* US-009.

- [x] **Asignación de Conductores:** Conductor, vehículo, horario y dirección por orden de recogida.
  - *Cubierto en:* tabla `conductores` + FK en `remisiones.conductor_id` y `agenda_transporte.conductor_id`.
  - *Historia de usuario:* US-009, AC-002.

- [x] **Cruce de Devoluciones:** Lógica de entrada para restaurar Kardex y calcular días de alquiler.
  - *Cubierto en:* `tipo_remision = 'entrada_devolucion'` + cálculo de días entre remisión salida y entrada.
  - *Historia de usuario:* US-010.

---

## 6. Checklist de Requerimientos Transversales

- [x] **Cálculo por Metro Cuadrado ($/m²):** Lógica en facturación y cotizaciones.
  - *Cubierto en:* `catalogo_productos.calcula_por_m2` + `catalogo_productos.precio_por_m2` + campos `area_m2` en `cotizacion_items` y `factura_items`.
  - *Historia de usuario:* US-002 AC-004, US-011 AC-003.

- [x] **Módulo de Auditoría Global:** ¿Quién? ¿Cuándo? ¿Qué tipo de cambio?
  - *Cubierto en:* tabla `auditoria` con campos: `usuario_id`, `created_at`, `accion`, `tabla_afectada`, `datos_anteriores`, `datos_nuevos`.
  - *Historia de usuario:* US-013.

- [x] **Motor de Notificaciones:**
  - [x] Alertas para aprobaciones pendientes entre áreas.
    - *Cubierto en:* tabla `notificaciones` con `tipo = 'aprobacion_pendiente'` + US-014 AC-001.
  - [x] Alertas logísticas para recogida de maquinaria.
    - *Cubierto en:* `tipo_notificacion = 'recogida_programada'` + US-014 AC-002.

---

## Items adicionales identificados en documentos (no estaban en checklist original)

- [x] **Autorización de Centrales de Riesgo (Ley 1581/2012):** Capturada como documento adjunto y tabla propia `autorizacion_centrales_riesgo`.
- [x] **Listas LAFT:** Campo de validación en `aprobaciones_cliente` para el área de Jurídica.
- [x] **Cláusulas de Arrendamiento:** El contrato incluye cláusulas del FT-AC-001 Sección IX (tarifa inicia desde remisión, faltantes se cobran a valor comercial, no traslado sin autorización).
- [x] **Accionistas >5% capital:** Capturados en tabla `accionistas` con campo `es_pep` para Personas Expuestas Políticamente.
- [x] **Retenciones (Rte. Fuente + ICA):** Campos en tabla `clientes` y `facturas` para gestión por cliente.
- [x] **Prospectos sin venta:** El campo `estado_cliente = 'prospecto'` permite registrar los ~50 contactos mensuales que no siempre concretan compra.
