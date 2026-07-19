# REVISIÓN COMPLETA DEL MODELO DBML Y ARQUITECTURA ETL
## G&H Obras y Estructuras Metálicas S.A.S.
### Fecha: 18 de Julio 2026
### Versión: 2.0 — Post SEM-27

---

## 📋 TABLA DE CONTENIDO

1. [Inventario Completo de Tablas DBML](#inventario-completo-de-tablas-dbml)
2. [Validación contra Prototipo](#validación-contra-prototipo)
3. [Arquitectura ETL para KPIs y Tableros](#arquitectura-etl-para-kpis-y-tableros)
4. [Tablas de Hechos (FACT) y Dimensiones (DIM)](#tablas-de-hechos-fact-y-dimensiones-dim)
5. [Agregados y Métricas por Rol](#agregados-y-métricas-por-rol)
6. [Proceso de ETL y Actualización](#proceso-de-etl-y-actualización)
7. [Especificación de Dashboards](#especificación-de-dashboards)

---

## 1. INVENTARIO COMPLETO DE TABLAS DBML

### 1.1. MÓDULO: USUARIOS Y SEGURIDAD

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 1 | `usuarios` | Usuarios del sistema con RBAC (12 roles) | Dimensión | ✅ Completo |

**Campos clave**: id, nombre, email, rol, activo

---

### 1.2. MÓDULO: AUDITORÍA Y NOTIFICACIONES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 2 | `auditoria` | Log inmutable de acciones del sistema | Hecho | ✅ Completo |
| 3 | `notificaciones` | Motor de notificaciones push | Operacional | ✅ Completo |

**Campos clave auditoria**: usuario_id, accion, tabla_afectada, datos_anteriores, datos_nuevos, created_at
**Campos clave notificaciones**: usuario_id, tipo, mensaje, leida, created_at

---

### 1.3. MÓDULO: CLIENTES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 4 | `clientes` | Registro central de clientes (~180 inicial) | Dimensión | ✅ Completo |
| 5 | `contactos_cliente` | Contactos de pago y facturación | Dimensión | ✅ Completo |
| 6 | `referencias_bancarias` | Referencias bancarias (hasta 2/cliente) | Dimensión | ✅ Completo |
| 7 | `referencias_comerciales` | Referencias comerciales (hasta 2/cliente) | Dimensión | ✅ Completo |
| 8 | `accionistas` | Accionistas con >5% capital | Dimensión | ✅ Completo |
| 9 | `autorizacion_centrales_riesgo` | Autorización Ley 1581/2012 | Dimensión | ✅ Completo |
| 10 | `aprobaciones_cliente` | Checklist digital de aprobación (3 áreas) | Hecho | ✅ Completo |
| 11 | `documentos_registro` | Checklist de documentos (RUT, Cámara, etc.) | Dimensión | ✅ Completo |

**Total tablas módulo Clientes**: 8 tablas

---

### 1.4. MÓDULO: OBRAS Y FRENTES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 12 | `obras` | Obras por cliente (hasta 50/cliente) | Dimensión | ✅ Completo |
| 13 | `frentes_obra` | Frentes dentro de una obra (3-4/obra) | Dimensión | ✅ Completo |

**Total tablas módulo Obras**: 2 tablas

---

### 1.5. MÓDULO: CATÁLOGO DE PRODUCTOS

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 14 | `catalogo_productos` | Catálogo general anual | Dimensión | ✅ Completo |
| 15 | `catalogo_precios_cliente` | Precios especiales por cliente | Dimensión | ✅ Completo |
| 16 | `retenciones_config` | Retenciones por tipo de concepto | Dimensión | ✅ Completo |
| 17 | `config_tarifas_transporte` | Tarifas de transporte por zona | Dimensión | ✅ Completo |
| 18 | `config_criterios_liquidacion_conductor` | Criterios de bonificación conductores | Dimensión | ✅ Completo |
| 19 | `evaluacion_criterios_conductor` | Evaluación por viaje de criterios | Hecho | ✅ Completo |

**Total tablas módulo Catálogo**: 6 tablas

**NUEVOS CAMPOS (Julio 2026)** en `catalogo_productos`:
- `unidad_kardex`, `unidad_facturacion`: Conversión automática de unidades
- `largo_m`, `ancho_m`, `alto_m`: Para cálculo automático de m²

---

### 1.6. MÓDULO: KARDEX DE CONSUMIBLES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 20 | `consumibles_catalogo` | Materiales de uso interno (no alquiler) | Dimensión | ✅ Completo |
| 21 | `kardex_consumibles` | Movimientos de consumibles | Hecho | ✅ Completo |

**Total tablas módulo Consumibles**: 2 tablas

**Fuente**: KARDEX.xlsx — hojas: PINTURA, DISOLVENTE, SOLDADURA 6013, SOLDADURA MIG, TORNILLOS, CONSUMIBLES

---

### 1.7. MÓDULO: COTIZACIONES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 22 | `cotizaciones` | Cotizaciones (6-12/semana por dibujante) | Hecho | ✅ Completo |
| 23 | `cotizacion_items` | Líneas de cotización | Hecho | ✅ Completo |
| 24 | `archivos_planos` | Planos AutoCAD/PDF de cotización | Dimensión | ✅ Completo |

**Total tablas módulo Cotizaciones**: 3 tablas

---

### 1.8. MÓDULO: CONTRATOS Y ÓRDENES

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 25 | `ordenes_compra` | Orden generada post-aprobación cotización | Hecho | ✅ Completo |
| 26 | `contratos` | Contratos con firma electrónica | Hecho | ✅ Completo |

**Total tablas módulo Contratos**: 2 tablas

---

### 1.9. MÓDULO: INVENTARIOS Y LOGÍSTICA

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 27 | `pedidos` | Pedidos de despacho (parcial/completo) | Hecho | ✅ Completo |
| 28 | `pedido_items` | Ítems de pedido | Hecho | ✅ Completo |
| 29 | `vehiculos` | Flota G&H con dimensiones/capacidades | Dimensión | ✅ Completo |
| 30 | `conductores` | Conductores para transporte | Dimensión | ✅ Completo |
| 31 | `conductor_vehiculos` | Historial asignación conductor↔vehículo | Hecho | ✅ Completo |
| 32 | `remisiones` | Remisiones de salida/entrada | Hecho | ✅ Completo |
| 33 | `remision_items` | Detalle de equipos por remisión | Hecho | ✅ Completo |
| 34 | `cronograma_recogidas` | Cronograma diario Recepción→Almacén | Hecho | ✅ Completo |
| 35 | `equipos_ajenos` | Equipo externo recibido en devoluciones | Operacional | ✅ Completo |
| 36 | `agenda_transporte` | Agenda jefe de almacén | Hecho | ✅ Completo |

**Total tablas módulo Inventarios**: 10 tablas

**CAMPOS CRÍTICOS SEM-27**:
- `remision_items`: `condicion_devolucion` (BUENO/REGULAR/MALO)
- `remision_items`: `largo_m`, `ancho_m`, `alto_m`, `peso_kg_unitario`, `peso_total_kg`
- `remisiones`: Verificación 3 fuentes (`formato_conductor`, `formato_despachador`, `fotos_porteria_urls`)

---

### 1.10. MÓDULO: FACTURACIÓN Y CARTERA

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 37 | `facturas` | Facturación electrónica con CUFE/Radian | Hecho | ✅ Completo |
| 38 | `factura_items` | Líneas de factura con retenciones | Hecho | ✅ Completo |
| 39 | `pagos` | Registro de pagos | Hecho | ✅ Completo |
| 40 | `cartera` | Gestión de cartera y cobro | Hecho | ✅ Completo |

**Total tablas módulo Facturación**: 4 tablas

**CAMPOS CRÍTICOS SEM-27**:
- `facturas`: `modalidad_factura` (por_remision|consolidada|por_valor)
- `facturas`: `centro_costo` (13=alquiler, 14=venta/reposición)
- `facturas`: `estado_radian` (fuente de verdad, no Siigo)
- `clientes`: `tipo_dominio_correo` (corporativo=triple check, público=llamada)

---

### 1.11. MÓDULO: KARDEX DE MOVIMIENTOS

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 41 | `kardex_movimientos` | Kardex transaccional de equipos | Hecho | ✅ Completo |

**Total tablas módulo Kardex**: 1 tabla

**Fuente**: Equivalente digital al Listado de Kardex de Clientes de Siigo

---

### 1.12. MÓDULO: REPORTERÍA (Pre-calculados)

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 42 | `rpt_kardex_cliente` | Kardex clientes por período | Agregado | ✅ Completo |
| 43 | `rpt_estado_pedidos` | Estado pedidos (COMPLETO/PARCIAL) | Agregado | ✅ Completo |
| 44 | `rpt_facturacion_periodo` | Facturación por período y cliente | Agregado | ✅ Completo |
| 45 | `rpt_cartera_vencida` | Cartera vencida por tramos (aging) | Agregado | ✅ Completo |
| 46 | `rpt_conductores_viajes` | Liquidación conductores por período | Agregado | ✅ Completo |
| 47 | `rpt_inventario_rotacion` | Rotación inventario por producto | Agregado | ✅ Completo |

**Total tablas módulo Reportería**: 6 tablas

---

### 1.13. MÓDULO: INVENTARIOS POR BODEGA (NUEVO — Julio 2026)

| # | Tabla | Descripción | Tipo | Estado |
|---|-------|-------------|------|--------|
| 48 | `bodegas_inventario` | Distribución de stock por bodega | Dimensión | ✅ Completo |

**Total tablas módulo Bodegas**: 1 tabla

**4 BODEGAS**:
- **Bodega 1** (Engativá): Principal
- **Bodega 2** (Luz): Secundaria
- **Bodega 40** (Mantenimiento): Equipos en reparación
- **Bodega 50** (Clientes): Equipos alquilados

**FILOSOFÍA CONSULTIVA**:
- Muestra disponibilidad
- Advierte si stock < 50 unidades
- NO bloquea operaciones

---

## 📊 RESUMEN INVENTARIO DBML

| Módulo | Tablas | Tipo |
|--------|--------|------|
| Usuarios y Seguridad | 1 | Dimensión |
| Auditoría y Notificaciones | 2 | Hecho/Operacional |
| Clientes | 8 | Dimensión/Hecho |
| Obras y Frentes | 2 | Dimensión |
| Catálogo de Productos | 6 | Dimensión/Hecho |
| Kardex Consumibles | 2 | Dimensión/Hecho |
| Cotizaciones | 3 | Hecho/Dimensión |
| Contratos y Órdenes | 2 | Hecho |
| Inventarios y Logística | 10 | Hecho/Dimensión/Operacional |
| Facturación y Cartera | 4 | Hecho |
| Kardex Movimientos | 1 | Hecho |
| Reportería (Pre-calculados) | 6 | Agregado |
| Inventarios por Bodega | 1 | Dimensión |

**TOTAL: 48 TABLAS**

---

## 2. VALIDACIÓN CONTRA PROTOTIPO

### 2.1. Tablas Implementadas en Prototipo React

Basado en el análisis del código del prototipo (`/gyh-prototipo/src/`):

| Módulo | Pantalla | Tablas Utilizadas | Estado |
|--------|----------|-------------------|--------|
| **Auth** | Login.jsx | `usuarios` | ✅ Implementado |
| **Dashboard** | Dashboard.jsx | `usuarios`, `clientes`, `cotizaciones`, `pedidos`, `facturas` | ✅ Implementado |
| **Clientes** | ClientesList.jsx | `clientes`, `aprobaciones_cliente` | ✅ Implementado |
| **Clientes** | ClienteDetail.jsx | `clientes`, `contactos_cliente`, `obras`, `frentes_obra`, `documentos_registro` | ✅ Implementado |
| **Clientes** | ClienteForm.jsx | `clientes`, `referencias_bancarias`, `referencias_comerciales`, `accionistas` | ✅ Implementado |
| **Cotizaciones** | CotizacionesList.jsx | `cotizaciones`, `clientes`, `usuarios` | ✅ Implementado |
| **Cotizaciones** | CotizacionDetail.jsx | `cotizaciones`, `cotizacion_items`, `catalogo_productos`, `archivos_planos` | ✅ Implementado |
| **Cotizaciones** | CotizacionForm.jsx | `cotizaciones`, `cotizacion_items`, `catalogo_productos`, `obras`, `frentes_obra` | ✅ Implementado |
| **Contratos** | ContratosList.jsx | `contratos`, `ordenes_compra`, `clientes` | ✅ Implementado |
| **Almacén** | Stock.jsx | `catalogo_productos`, `bodegas_inventario` | ✅ Implementado |
| **Almacén** | Remisiones.jsx | `remisiones`, `pedidos`, `clientes`, `obras` | ✅ Implementado |
| **Almacén** | RemisionDetail.jsx | `remisiones`, `remision_items`, `catalogo_productos` | ✅ Implementado |
| **Almacén** | PedidoDetail.jsx | `pedidos`, `pedido_items`, `remisiones` | ✅ Implementado |
| **Almacén** | Agenda.jsx | `agenda_transporte`, `conductores`, `vehiculos`, `remisiones` | ✅ Implementado |
| **Almacén** | Conductores.jsx | `conductores`, `vehiculos`, `conductor_vehiculos` | ✅ Implementado |
| **Almacén** | Cronograma.jsx | `cronograma_recogidas`, `clientes`, `obras` | ✅ Implementado |
| **Almacén** | Consumibles.jsx | `consumibles_catalogo`, `kardex_consumibles` | ✅ Implementado |
| **Cartera** | Cartera.jsx | `cartera`, `facturas`, `pagos`, `clientes` | ✅ Implementado |
| **Reportes** | Reportes.jsx | `rpt_kardex_cliente`, `rpt_facturacion_periodo`, `rpt_cartera_vencida` | ✅ Implementado |
| **Auditoría** | Auditoria.jsx | `auditoria`, `usuarios` | ✅ Implementado |
| **Config** | Configuracion.jsx | `retenciones_config`, `config_tarifas_transporte`, `config_criterios_liquidacion_conductor` | ✅ Implementado |

### 2.2. Tablas NO Utilizadas en Prototipo (Requieren Atención)

| # | Tabla | Razón | Prioridad | Acción Recomendada |
|---|-------|-------|-----------|-------------------|
| 1 | `autorizacion_centrales_riesgo` | No hay pantalla específica de autorización | Media | Agregar a ClienteDetail como sección colapsable |
| 2 | `equipos_ajenos` | No hay gestión de equipos ajenos | Baja | Agregar modal en RemisionDetail para registrar equipos ajenos |
| 3 | `evaluacion_criterios_conductor` | No hay evaluación de criterios | Alta | **CRÍTICO**: Agregar en vista de liquidación conductores |
| 4 | `kardex_movimientos` | Usa datos directos de remisiones | Media | Agregar vista "Kardex Transaccional" en módulo Reportes |
| 5 | `rpt_estado_pedidos` | Dashboard usa datos directos | Media | Usar esta tabla para optimizar Dashboard |
| 6 | `rpt_conductores_viajes` | No hay liquidación conductores | Alta | **CRÍTICO**: Agregar pantalla de liquidación |

---

## 3. ARQUITECTURA ETL PARA KPIS Y TABLEROS

### 3.1. Principios de Diseño ETL

1. **Separación de Capas**:
   - **ODS (Operational Data Store)**: Tablas operacionales (clientes, pedidos, remisiones, etc.)
   - **DWH (Data Warehouse)**: Tablas de hechos (FACT) y dimensiones (DIM)
   - **Agregados**: Tablas pre-calculadas para dashboards (rpt_*)

2. **Actualización**:
   - **Tiempo Real**: Tablas operacionales (INSERT/UPDATE directo)
   - **Batch Nocturno**: Tablas de agregados (proceso ETL a las 2:00 AM)
   - **On-Demand**: Dashboards con filtros personalizados

3. **Granularidad**:
   - **Detalle**: Nivel transaccional (cada remisión, cada factura)
   - **Resumen Diario**: Agregado por día
   - **Resumen Mensual**: Agregado por mes
   - **Resumen Anual**: Agregado por año

---

### 3.2. Capa ODS (Operational Data Store)

**Tablas Operacionales (48 existentes)** — ya documentadas arriba

---

### 3.3. Capa DWH (Data Warehouse)

#### 3.3.1. Tablas de Hechos (FACT)

**PROPUESTA: Crear 12 tablas FACT adicionales**

```sql
-- ============================================================
-- TABLAS DE HECHOS (FACT TABLES) — Para análisis y BI
-- ============================================================

-- FACT 1: Hechos de cotizaciones
Table fact_cotizaciones {
  id                  bigserial    [pk]
  fecha_cotizacion    date         [not null]
  anio                integer      [not null]
  mes                 integer      [not null]
  trimestre           integer      [not null]
  semana              integer      [not null]

  cotizacion_id       uuid         [not null, ref: > cotizaciones.id]
  cliente_id          uuid         [not null, ref: > clientes.id]
  obra_id             uuid         [ref: > obras.id]
  dibujante_id        uuid         [ref: > usuarios.id]
  comercial_id        uuid         [ref: > usuarios.id]
  ciudad_sucursal     ciudad_sucursal

  estado              estado_cotizacion [not null]
  incluye_venta       boolean      [default: false]
  incluye_alquiler    boolean      [default: false]
  incluye_transporte  boolean      [default: false]

  subtotal            decimal(18,2) [default: 0]
  descuento           decimal(18,2) [default: 0]
  iva                 decimal(18,2) [default: 0]
  total               decimal(18,2) [default: 0]

  horas_modelamiento  decimal(4,2)
  dias_hasta_respuesta integer     [note: 'Días desde creación hasta aprobación/rechazo']
  tasa_conversion     decimal(5,2) [note: '% de conversión a orden de compra']

  created_at          timestamp    [default: `now()`]
  updated_at          timestamp    [default: `now()`]

  indexes {
    (cliente_id, fecha_cotizacion)
    (comercial_id, fecha_cotizacion)
    (dibujante_id, fecha_cotizacion)
    (anio, mes)
    estado
  }

  Note: '''
    Tabla de hechos para análisis de cotizaciones.

    KPIs derivados:
    - Volumen de cotizaciones por período
    - Tasa de conversión cotización→orden
    - Tiempo promedio de respuesta
    - Valor promedio de cotización
    - Distribución por tipo de negocio
    - Productividad por dibujante (cotizaciones/semana)
  '''
}

-- FACT 2: Hechos de pedidos
Table fact_pedidos {
  id                     bigserial    [pk]
  fecha_pedido           date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]
  trimestre              integer      [not null]

  pedido_id              uuid         [not null, ref: > pedidos.id]
  orden_compra_id        uuid         [not null, ref: > ordenes_compra.id]
  cliente_id             uuid         [not null, ref: > clientes.id]
  obra_id                uuid         [not null, ref: > obras.id]
  frente_id              uuid         [ref: > frentes_obra.id]
  ciudad_sucursal        ciudad_sucursal

  estado                 estado_pedido [not null]
  es_parcial             boolean      [default: false]
  dias_hasta_completo    integer      [note: 'Días desde pedido hasta estado = completo']
  dias_en_obra           integer      [note: 'Días desde pedido completo hasta devolución total']

  total_items            integer      [default: 0]
  items_despachados      integer      [default: 0]
  items_devueltos        integer      [default: 0]
  items_pendientes       integer      [default: 0]

  valor_estimado_alquiler decimal(18,2) [note: 'Valor estimado del alquiler (días × tarifa)']
  valor_real_facturado    decimal(18,2) [note: 'Valor real facturado al cliente']

  tiene_novedades        boolean      [default: false]
  tiene_faltantes        boolean      [default: false]
  tiene_danos            boolean      [default: false]

  created_at             timestamp    [default: `now()`]
  updated_at             timestamp    [default: `now()`]

  indexes {
    (cliente_id, fecha_pedido)
    (obra_id, fecha_pedido)
    (anio, mes)
    estado
  }

  Note: '''
    Tabla de hechos para análisis de pedidos.

    KPIs derivados:
    - Pedidos completos vs parciales
    - Tiempo promedio hasta despacho completo
    - Días promedio de alquiler por pedido
    - Valor promedio por pedido
    - Tasa de novedades (daños, faltantes)
    - Rotación de equipos
  '''
}

-- FACT 3: Hechos de remisiones
Table fact_remisiones {
  id                     bigserial    [pk]
  fecha_remision         date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]
  trimestre              integer      [not null]

  remision_id            uuid         [not null, ref: > remisiones.id]
  tipo_remision          tipo_remision [not null]
  pedido_id              uuid         [ref: > pedidos.id]
  cliente_id             uuid         [not null, ref: > clientes.id]
  obra_id                uuid         [not null, ref: > obras.id]
  conductor_id           uuid         [ref: > conductores.id]
  vehiculo_id            uuid         [ref: > vehiculos.id]

  total_items            integer      [default: 0]
  peso_total_kg          decimal(12,3) [default: 0]
  volumen_total_m3       decimal(10,3) [default: 0]

  cobra_transporte       boolean      [default: false]
  valor_transporte       decimal(15,2)
  zona_transporte        varchar(50)  [note: 'bogota|fuera_bogota|ibague|armenia']

  tiene_novedades        boolean      [default: false]
  tiene_equipos_ajenos   boolean      [default: false]

  dias_desde_salida      integer      [note: 'Solo para tipo = entrada_devolucion']

  created_at             timestamp    [default: `now()`]
  updated_at             timestamp    [default: `now()`]

  indexes {
    (cliente_id, fecha_remision)
    (conductor_id, fecha_remision)
    (anio, mes)
    tipo_remision
  }

  Note: '''
    Tabla de hechos para análisis de remisiones.

    KPIs derivados:
    - Volumen de despachos/devoluciones
    - Peso y volumen transportado
    - Valor de transporte facturado
    - Días promedio de ciclo (salida→devolución)
    - Tasa de novedades en devoluciones
    - Productividad por conductor
  '''
}

-- FACT 4: Hechos de facturación
Table fact_facturacion {
  id                     bigserial    [pk]
  fecha_factura          date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]
  trimestre              integer      [not null]

  factura_id             uuid         [not null, ref: > facturas.id]
  orden_compra_id        uuid         [not null, ref: > ordenes_compra.id]
  cliente_id             uuid         [not null, ref: > clientes.id]
  ciudad_sucursal        ciudad_sucursal

  modalidad_factura      modalidad_factura
  centro_costo           varchar(5)   [note: '13=alquiler, 14=venta/reposición']
  estado                 estado_factura
  estado_radian          estado_radian

  subtotal               decimal(18,2) [not null]
  descuento              decimal(18,2) [default: 0]
  iva                    decimal(18,2) [default: 0]
  rte_fuente             decimal(18,2) [default: 0]
  rte_ica                decimal(18,2) [default: 0]
  total                  decimal(18,2) [not null]
  saldo_pendiente        decimal(18,2) [not null]

  dias_hasta_vencimiento integer
  dias_mora              integer      [default: 0]

  tiene_dominio_corporativo boolean   [note: 'Del campo tipo_dominio_correo del cliente']
  requiere_seguimiento_telefonico boolean

  created_at             timestamp    [default: `now()`]
  updated_at             timestamp    [default: `now()`]

  indexes {
    (cliente_id, fecha_factura)
    (anio, mes)
    estado
    estado_radian
    centro_costo
  }

  Note: '''
    Tabla de hechos para análisis de facturación.

    KPIs derivados:
    - Facturación por período
    - Facturación por centro de costo
    - Tasa de aprobación DIAN
    - Valor promedio de factura
    - Días promedio hasta pago
    - Cartera vencida por tramos
    - Retenciones totales
  '''
}

-- FACT 5: Hechos de inventario (movimientos diarios)
Table fact_inventario_movimientos {
  id                     bigserial    [pk]
  fecha_movimiento       date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]
  trimestre              integer      [not null]

  producto_id            uuid         [not null, ref: > catalogo_productos.id]
  bodega_id              bodega_id    [not null]
  tipo_producto          tipo_producto
  unidad_negocio         varchar(50)

  tipo_movimiento        varchar(30)  [not null, note: 'salida|entrada_devolucion|ajuste|baja|mantenimiento']

  cantidad_salida        integer      [default: 0]
  cantidad_entrada       integer      [default: 0]
  stock_inicial_dia      integer      [default: 0]
  stock_final_dia        integer      [default: 0]

  remision_id            uuid         [ref: > remisiones.id]
  cliente_id             uuid         [ref: > clientes.id]

  valor_unitario         decimal(15,2)
  valor_total_movimiento decimal(18,2)

  created_at             timestamp    [default: `now()`]

  indexes {
    (producto_id, fecha_movimiento)
    (bodega_id, fecha_movimiento)
    (anio, mes)
    tipo_movimiento
  }

  Note: '''
    Tabla de hechos para análisis de inventario.

    KPIs derivados:
    - Rotación de inventario por producto
    - Stock promedio por bodega
    - Días de inventario disponible
    - Valor de inventario
    - Tasa de merma/baja
    - Análisis de movimientos por tipo
  '''
}

-- FACT 6: Hechos de productividad por rol
Table fact_productividad_usuarios {
  id                     bigserial    [pk]
  fecha                  date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]
  semana                 integer      [not null]

  usuario_id             uuid         [not null, ref: > usuarios.id]
  rol                    rol_usuario  [not null]

  -- Métricas por rol (según aplique)
  cotizaciones_creadas   integer      [default: 0, note: 'Dibujante/Comercial']
  horas_modelamiento     decimal(6,2) [default: 0, note: 'Dibujante']
  clientes_registrados   integer      [default: 0, note: 'Comercial/Soporte Atención']
  clientes_aprobados     integer      [default: 0, note: 'Contabilidad/Jurídica/Comercial']
  remisiones_procesadas  integer      [default: 0, note: 'Almacén/Despachador']
  viajes_realizados      integer      [default: 0, note: 'Conductor']
  facturas_generadas     integer      [default: 0, note: 'Facturación']
  pagos_registrados      integer      [default: 0, note: 'Cartera']

  acciones_total         integer      [default: 0, note: 'Total de acciones en auditoria']

  created_at             timestamp    [default: `now()`]

  indexes {
    (usuario_id, fecha)
    (rol, fecha)
    (anio, mes)
  }

  Note: '''
    Tabla de hechos para análisis de productividad por usuario/rol.

    KPIs derivados:
    - Productividad individual por rol
    - Comparativa entre usuarios del mismo rol
    - Tendencias de productividad
    - Identificación de cuellos de botella
    - Planificación de recursos
  '''
}

-- FACT 7: Hechos de tiempos de ciclo
Table fact_tiempos_ciclo {
  id                     bigserial    [pk]
  fecha_inicio           date         [not null]
  fecha_fin              date
  anio                   integer      [not null]
  mes                    integer      [not null]

  tipo_ciclo             varchar(50)  [not null, note: 'prospecto_a_cliente|cotizacion_a_orden|pedido_a_completo|alquiler_completo|factura_a_pago']

  cliente_id             uuid         [ref: > clientes.id]
  cotizacion_id          uuid         [ref: > cotizaciones.id]
  pedido_id              uuid         [ref: > pedidos.id]
  factura_id             uuid         [ref: > facturas.id]

  dias_ciclo             integer      [note: 'Duración total del ciclo en días']
  estado_final           varchar(50)  [note: 'Estado en el que terminó el ciclo']

  created_at             timestamp    [default: `now()`]

  indexes {
    tipo_ciclo
    (cliente_id, tipo_ciclo)
    (anio, mes)
  }

  Note: '''
    Tabla de hechos para análisis de tiempos de ciclo.

    Ciclos medidos:
    1. Prospecto → Cliente Aprobado
    2. Cotización → Orden de Compra
    3. Pedido → Pedido Completo
    4. Alquiler (Salida → Devolución Total)
    5. Factura → Pago Completo

    KPIs derivados:
    - Tiempo promedio por tipo de ciclo
    - Identificación de demoras
    - Optimización de procesos
    - Predicción de tiempos
  '''
}

-- FACT 8: Hechos de calidad de servicio
Table fact_calidad_servicio {
  id                     bigserial    [pk]
  fecha                  date         [not null]
  anio                   integer      [not null]
  mes                    integer      [not null]

  tipo_evento            varchar(50)  [not null, note: 'pedido_incompleto|novedad_devolucion|factura_rechazada|cliente_insatisfecho']
  severidad              varchar(20)  [note: 'baja|media|alta|critica']

  cliente_id             uuid         [ref: > clientes.id]
  obra_id                uuid         [ref: > obras.id]
  pedido_id              uuid         [ref: > pedidos.id]
  remision_id            uuid         [ref: > remisiones.id]
  factura_id             uuid         [ref: > facturas.id]

  descripcion            text
  causa_raiz             text
  accion_correctiva      text

  resuelto               boolean      [default: false]
  dias_hasta_resolucion  integer

  created_at             timestamp    [default: `now()`]
  updated_at             timestamp    [default: `now()`]

  indexes {
    tipo_evento
    (cliente_id, fecha)
    severidad
    resuelto
  }

  Note: '''
    Tabla de hechos para análisis de calidad de servicio.

    KPIs derivados:
    - Tasa de incidencias por tipo
    - Tiempo promedio de resolución
    - Clientes con más incidencias
    - Tendencias de calidad
    - Efectividad de acciones correctivas
  '''
}
```

---

#### 3.3.2. Dimensiones Adicionales

Las dimensiones existentes (clientes, productos, usuarios, etc.) son suficientes.

**PROPUESTA: Crear 2 dimensiones de tiempo**

```sql
-- DIM 1: Dimensión de tiempo (Fecha)
Table dim_fecha {
  fecha                date         [pk]
  anio                 integer      [not null]
  mes                  integer      [not null]
  mes_nombre           varchar(20)  [note: 'Enero, Febrero, ...']
  trimestre            integer      [not null]
  trimestre_nombre     varchar(10)  [note: 'Q1, Q2, Q3, Q4']
  semana               integer      [not null]
  dia_del_mes          integer      [not null]
  dia_de_la_semana     integer      [not null, note: '1=Lunes, 7=Domingo']
  dia_nombre           varchar(20)  [note: 'Lunes, Martes, ...']
  es_fin_de_semana     boolean      [default: false]
  es_festivo           boolean      [default: false]
  nombre_festivo       varchar(100)

  Note: '''
    Dimensión de tiempo para análisis temporal.
    Permite filtrar y agrupar por año, mes, trimestre, semana, día.
    Se genera una fila por cada fecha desde 2020-01-01 hasta 2030-12-31.
  '''
}

-- DIM 2: Dimensión de hora (para análisis intradiario)
Table dim_hora {
  hora                 integer      [pk, note: '0-23']
  hora_12h             varchar(10)  [note: '12 AM - 11 PM']
  periodo_dia          varchar(20)  [note: 'Madrugada|Mañana|Tarde|Noche']
  turno_trabajo        varchar(20)  [note: 'Diurno|Nocturno']

  Note: '''
    Dimensión de hora para análisis de patrones horarios.
    Útil para analizar:
    - Horas pico de despachos
    - Tiempos de llegada de conductores
    - Patrones de facturación
  '''
}
```

---

### 3.4. Capa de Agregados (Reportería)

**PROPUESTA: Ampliar de 6 a 15 tablas de agregados**

#### 3.4.1. Agregados Existentes (6 tablas)

Ya documentados en inventario:
1. `rpt_kardex_cliente`
2. `rpt_estado_pedidos`
3. `rpt_facturacion_periodo`
4. `rpt_cartera_vencida`
5. `rpt_conductores_viajes`
6. `rpt_inventario_rotacion`

#### 3.4.2. Nuevos Agregados Propuestos (9 tablas adicionales)

```sql
-- AGG 7: Resumen mensual de cotizaciones
Table agg_cotizaciones_mes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]
  ciudad_sucursal        ciudad_sucursal
  dibujante_id           uuid         [ref: > usuarios.id]
  comercial_id           uuid         [ref: > usuarios.id]

  total_cotizaciones     integer      [default: 0]
  cotizaciones_borrador  integer      [default: 0]
  cotizaciones_enviadas  integer      [default: 0]
  cotizaciones_aprobadas integer      [default: 0]
  cotizaciones_rechazadas integer     [default: 0]
  cotizaciones_vencidas  integer      [default: 0]

  tasa_aprobacion        decimal(5,2) [note: '% de cotizaciones aprobadas']
  tiempo_prom_respuesta  decimal(6,2) [note: 'Días promedio hasta respuesta']

  valor_total_cotizado   decimal(18,2) [default: 0]
  valor_total_aprobado   decimal(18,2) [default: 0]

  horas_modelamiento_total decimal(8,2) [default: 0]

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    ciudad_sucursal
    dibujante_id
    comercial_id
  }

  Note: 'Agregado mensual de cotizaciones por sucursal, dibujante y comercial'
}

-- AGG 8: Resumen mensual de ventas y alquileres
Table agg_ventas_mes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]
  ciudad_sucursal        ciudad_sucursal
  centro_costo           varchar(5)   [note: '13=alquiler, 14=venta/reposición']

  total_facturas         integer      [default: 0]
  subtotal               decimal(18,2) [default: 0]
  iva                    decimal(18,2) [default: 0]
  retenciones            decimal(18,2) [default: 0]
  total_facturado        decimal(18,2) [default: 0]
  total_cobrado          decimal(18,2) [default: 0]
  saldo_pendiente        decimal(18,2) [default: 0]

  clientes_activos       integer      [default: 0, note: 'Clientes que facturaron en el mes']
  ticket_promedio        decimal(18,2) [default: 0]

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    ciudad_sucursal
    centro_costo
  }

  Note: 'Agregado mensual de ventas y alquileres por sucursal y centro de costo'
}

-- AGG 9: Resumen mensual de inventarios
Table agg_inventario_mes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]
  bodega_id              bodega_id    [not null]
  tipo_producto          tipo_producto
  unidad_negocio         varchar(50)

  stock_inicial_mes      integer      [default: 0]
  stock_final_mes        integer      [default: 0]
  stock_promedio_mes     integer      [default: 0]

  total_salidas          integer      [default: 0]
  total_entradas         integer      [default: 0]
  total_bajas            integer      [default: 0]
  total_mantenimiento    integer      [default: 0]

  tasa_rotacion          decimal(6,2) [note: 'Veces que rotó en el mes']
  dias_inventario        decimal(6,2) [note: 'Días de inventario disponible']

  valor_inventario       decimal(18,2) [default: 0]

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    bodega_id
    tipo_producto
  }

  Note: 'Agregado mensual de inventarios por bodega y tipo de producto'
}

-- AGG 10: Resumen de productividad por equipo
Table agg_productividad_equipo {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]

  area                   varchar(50)  [note: 'comercial|dibujante|almacen|facturacion|cartera']

  total_usuarios_activos integer      [default: 0]
  acciones_promedio      decimal(8,2) [default: 0]
  productividad_promedio decimal(8,2) [default: 0, note: 'Métrica específica por área']

  -- Métricas específicas
  cotizaciones_por_dibujante decimal(6,2)
  clientes_por_comercial     decimal(6,2)
  remisiones_por_despachador decimal(6,2)
  facturas_por_usuario       decimal(6,2)

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    area
  }

  Note: 'Agregado mensual de productividad por área/equipo'
}

-- AGG 11: Indicadores de calidad de servicio
Table agg_calidad_servicio_mes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]

  total_pedidos          integer      [default: 0]
  pedidos_completos      integer      [default: 0]
  pedidos_parciales      integer      [default: 0]
  pedidos_con_novedades  integer      [default: 0]

  total_remisiones       integer      [default: 0]
  remisiones_con_danos   integer      [default: 0]
  remisiones_con_faltantes integer   [default: 0]

  total_facturas_dian    integer      [default: 0]
  facturas_aprobadas_dian integer    [default: 0]
  facturas_rechazadas_dian integer   [default: 0]

  tasa_pedidos_completos decimal(5,2) [note: '%']
  tasa_novedades         decimal(5,2) [note: '%']
  tasa_aprobacion_dian   decimal(5,2) [note: '%']

  tiempo_prom_despacho   decimal(6,2) [note: 'Días promedio hasta pedido completo']
  tiempo_prom_devolucion decimal(6,2) [note: 'Días promedio de alquiler']

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
  }

  Note: 'Agregado mensual de indicadores de calidad de servicio'
}

-- AGG 12: Análisis de clientes (RFM)
Table agg_analisis_clientes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  fecha_corte            date         [not null]
  cliente_id             uuid         [not null, ref: > clientes.id]

  -- RFM (Recency, Frequency, Monetary)
  dias_ultima_factura    integer      [note: 'R: Recency - días desde última factura']
  total_facturas_12m     integer      [note: 'F: Frequency - facturas últimos 12 meses']
  valor_total_12m        decimal(18,2) [note: 'M: Monetary - valor facturado últimos 12 meses']

  score_r                integer      [note: '1-5 (5 = más reciente)']
  score_f                integer      [note: '1-5 (5 = más frecuente)']
  score_m                integer      [note: '1-5 (5 = mayor valor)']
  score_rfm              integer      [note: 'Suma de R+F+M (3-15)']

  segmento               varchar(30)  [note: 'Campeones|Leales|Potenciales|En Riesgo|Perdidos']

  -- Métricas adicionales
  total_obras_activas    integer      [default: 0]
  ticket_promedio        decimal(18,2)
  dias_promedio_pago     decimal(6,2)
  tiene_mora             boolean      [default: false]

  generado_at            timestamp    [default: `now()`]

  indexes {
    (cliente_id, fecha_corte)
    segmento
    score_rfm
  }

  Note: '''
    Análisis RFM de clientes para segmentación.

    Segmentos:
    - Campeones (RFM 12-15): Clientes top
    - Leales (RFM 9-11): Clientes frecuentes
    - Potenciales (RFM 6-8): Oportunidad de crecimiento
    - En Riesgo (RFM 4-5): Requieren atención
    - Perdidos (RFM 3): Reactivación urgente
  '''
}

-- AGG 13: Forecast de facturación
Table agg_forecast_facturacion {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]
  tipo_forecast          varchar(20)  [note: 'optimista|realista|pesimista']

  pedidos_pendientes     integer      [default: 0]
  valor_pedidos_pendientes decimal(18,2) [default: 0]

  alquileres_activos     integer      [default: 0]
  valor_alquileres_mes   decimal(18,2) [default: 0]

  contratos_vigentes     integer      [default: 0]
  valor_contratos_mes    decimal(18,2) [default: 0]

  forecast_mes           decimal(18,2) [note: 'Proyección de facturación del mes']
  margen_error           decimal(5,2) [note: '% de margen de error']

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    tipo_forecast
  }

  Note: 'Proyección de facturación mensual basada en pedidos, alquileres y contratos activos'
}

-- AGG 14: Indicadores de transporte
Table agg_transporte_mes {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  anio                   integer      [not null]
  mes                    integer      [not null]
  conductor_id           uuid         [ref: > conductores.id]
  vehiculo_id            uuid         [ref: > vehiculos.id]
  zona                   varchar(50)

  total_viajes           integer      [default: 0]
  km_total               decimal(12,2) [default: 0]
  peso_total_ton         decimal(12,3) [default: 0]
  volumen_total_m3       decimal(12,3) [default: 0]

  valor_transporte_facturado decimal(18,2) [default: 0]
  valor_liquidacion_conductor decimal(18,2) [default: 0]
  margen_transporte      decimal(18,2) [note: 'facturado - liquidación']

  viajes_calificados     integer      [default: 0, note: 'Viajes que cumplieron criterios']
  tasa_calificacion      decimal(5,2) [note: '%']

  generado_at            timestamp    [default: `now()`]

  indexes {
    (anio, mes)
    conductor_id
    vehiculo_id
  }

  Note: 'Agregado mensual de indicadores de transporte por conductor y vehículo'
}

-- AGG 15: Dashboard ejecutivo (resumen general)
Table agg_dashboard_ejecutivo {
  id                     uuid         [pk, default: `gen_random_uuid()`]
  fecha_corte            date         [not null]
  periodo                varchar(20)  [note: 'dia|semana|mes|trimestre|ano']

  -- Comercial
  clientes_nuevos        integer      [default: 0]
  clientes_activos       integer      [default: 0]
  cotizaciones_nuevas    integer      [default: 0]
  tasa_conversion        decimal(5,2)

  -- Operacional
  pedidos_nuevos         integer      [default: 0]
  pedidos_completos      integer      [default: 0]
  pedidos_incompletos    integer      [default: 0]
  remisiones_salida      integer      [default: 0]
  remisiones_entrada     integer      [default: 0]

  -- Inventario
  stock_disponible_valor decimal(18,2)
  stock_en_alquiler_valor decimal(18,2)
  tasa_rotacion_global   decimal(6,2)

  -- Financiero
  facturacion_periodo    decimal(18,2)
  cobros_periodo         decimal(18,2)
  cartera_total          decimal(18,2)
  cartera_vencida        decimal(18,2)

  -- Calidad
  tasa_pedidos_completos decimal(5,2)
  tasa_novedades         decimal(5,2)
  tasa_aprobacion_dian   decimal(5,2)

  generado_at            timestamp    [default: `now()`]

  indexes {
    (fecha_corte, periodo)
  }

  Note: '''
    Dashboard ejecutivo con KPIs clave del negocio.
    Se genera diariamente, semanalmente, mensualmente, trimestralmente y anualmente.
  '''
}
```

---

## 4. TABLAS DE HECHOS (FACT) Y DIMENSIONES (DIM)

### 4.1. Resumen de Tablas FACT (8 nuevas)

| # | Tabla FACT | Granularidad | Actualización | KPIs Principales |
|---|------------|--------------|---------------|------------------|
| 1 | `fact_cotizaciones` | Por cotizacion | Tiempo real | Tasa conversión, tiempo respuesta, productividad dibujante |
| 2 | `fact_pedidos` | Por pedido | Tiempo real | Pedidos completos/parciales, días de alquiler, valor promedio |
| 3 | `fact_remisiones` | Por remisión | Tiempo real | Volumen despachos, peso/volumen, ciclo salida-devolución |
| 4 | `fact_facturacion` | Por factura | Tiempo real | Facturación por CC, retenciones, días hasta pago, cartera |
| 5 | `fact_inventario_movimientos` | Por movimiento | Tiempo real | Rotación, stock, días inventario, valor inventario |
| 6 | `fact_productividad_usuarios` | Por usuario/día | Batch diario | Productividad por rol, comparativa, tendencias |
| 7 | `fact_tiempos_ciclo` | Por ciclo | Tiempo real | Tiempo promedio por ciclo, optimización procesos |
| 8 | `fact_calidad_servicio` | Por evento | Tiempo real | Tasa incidencias, tiempo resolución, tendencias calidad |

### 4.2. Resumen de Dimensiones (2 nuevas + existentes)

| # | Tabla DIM | Tipo | Descripción |
|---|-----------|------|-------------|
| 1 | `dim_fecha` | Tiempo | Análisis temporal (año, mes, trimestre, semana, día) |
| 2 | `dim_hora` | Tiempo | Análisis horario (patrones intradiarios) |
| * | Existentes | Negocio | clientes, usuarios, productos, obras, frentes, conductores, vehículos, etc. |

---

## 5. AGREGADOS Y MÉTRICAS POR ROL

### 5.1. Matriz de Dashboards y KPIs por Rol

| Rol | Dashboard Principal | KPIs Clave | Tablas Agregadas | Actualización |
|-----|---------------------|-----------|------------------|---------------|
| **CEO / Gerencia** | Dashboard Ejecutivo | Facturación, Cartera, Clientes Activos, Rotación Inventario | `agg_dashboard_ejecutivo` | Tiempo real |
| **Comercial** | Dashboard Comercial | Cotizaciones, Tasa Conversión, Pipeline, Clientes Nuevos | `agg_cotizaciones_mes`, `agg_analisis_clientes` | Tiempo real |
| **Dibujante** | Dashboard Productividad | Cotizaciones/Semana, Horas Modelamiento, Tasa Aprobación | `agg_productividad_equipo`, `fact_cotizaciones` | Tiempo real |
| **Almacén** | Dashboard Operacional | Pedidos Pendientes, Remisiones, Stock por Bodega | `rpt_estado_pedidos`, `agg_inventario_mes` | Tiempo real |
| **Conductor** | Dashboard Viajes | Viajes, Km, Peso, Liquidación | `agg_transporte_mes`, `rpt_conductores_viajes` | Tiempo real |
| **Facturación** | Dashboard Facturación | Facturas Emitidas, CUFE/Radian, Retenciones | `agg_ventas_mes`, `fact_facturacion` | Tiempo real |
| **Contabilidad** | Dashboard Financiero | Cartera, Aging, Forecast, Retenciones | `rpt_cartera_vencida`, `agg_forecast_facturacion` | Batch diario |
| **Despachador** | Dashboard Despachos | Remisiones, Novedades, Equipos Ajenos | `fact_remisiones`, `agg_calidad_servicio_mes` | Tiempo real |
| **Recepción** | Dashboard Cronograma | Recogidas Programadas, Cortes, Pendientes | `cronograma_recogidas` | Tiempo real |
| **SuperAdmin** | Dashboard Sistema | Usuarios Activos, Auditoría, Configuraciones | `auditoria`, `usuarios` | Tiempo real |

---

### 5.2. Especificación Detallada de Dashboards

#### 5.2.1. Dashboard Ejecutivo (CEO/Gerencia)

**Fuente**: `agg_dashboard_ejecutivo`

**KPIs Principales**:
1. **Facturación del Mes** (vs mes anterior, vs mismo mes año anterior)
   - Gráfica: Line chart con tendencia mensual
   - Desglose: Por centro de costo (13=Alquiler, 14=Venta)
   - Meta: Definida en configuración

2. **Cartera Total y Vencida**
   - Gráfica: Donut chart (cobrado vs pendiente vs vencido)
   - Desglose: Por tramos de mora (0-30, 31-60, 61-90, +90 días)
   - Indicador: % de cartera vencida

3. **Clientes Activos**
   - Número total de clientes con facturación en el mes
   - Comparativa: vs mes anterior
   - Segmentación RFM: Campeones, Leales, Potenciales, En Riesgo, Perdidos

4. **Tasa de Utilización de Inventario**
   - % de inventario en alquiler vs disponible
   - Gráfica: Gauge chart
   - Desglose: Por bodega

5. **Pedidos Completos vs Incompletos**
   - Gráfica: Bar chart
   - Alertas: Pedidos incompletos > 7 días

6. **Calidad de Servicio**
   - Tasa de pedidos completos
   - Tasa de novedades en devoluciones
   - Tasa de aprobación DIAN

**Filtros**:
- Período: Día, Semana, Mes, Trimestre, Año
- Sucursal: Bogotá, Ibagué, Armenia
- Centro de Costo: 13 (Alquiler), 14 (Venta)

---

#### 5.2.2. Dashboard Comercial

**Fuentes**: `agg_cotizaciones_mes`, `agg_analisis_clientes`, `fact_cotizaciones`

**KPIs Principales**:
1. **Pipeline de Cotizaciones**
   - Funnel chart: Borrador → En Revisión → Enviada → Aprobada
   - Tasa de conversión por etapa
   - Valor total en pipeline

2. **Cotizaciones por Estado**
   - Gráfica: Stacked bar chart
   - Desglose: Aprobadas, Rechazadas, Vencidas, Pendientes

3. **Tasa de Conversión**
   - Cotización → Orden de Compra
   - Comparativa: vs mes anterior
   - Por comercial

4. **Tiempo Promedio de Respuesta**
   - Días desde envío hasta aprobación/rechazo
   - Gráfica: Line chart con tendencia
   - Meta: < 7 días

5. **Productividad por Comercial**
   - Cotizaciones creadas/mes
   - Clientes nuevos registrados
   - Valor promedio de cotización

6. **Análisis RFM de Clientes**
   - Segmentación: Campeones, Leales, Potenciales, En Riesgo, Perdidos
   - Gráfica: Scatter plot (Frecuencia vs Valor)
   - Alertas: Clientes "En Riesgo" requieren atención

**Filtros**:
- Comercial: Todos, Individual
- Dibujante: Todos, Individual
- Período: Mes, Trimestre, Año
- Estado: Todos, Específico

---

#### 5.2.3. Dashboard Almacén

**Fuentes**: `rpt_estado_pedidos`, `agg_inventario_mes`, `fact_remisiones`

**KPIs Principales**:
1. **Pedidos por Estado**
   - KPI Cards: Pendientes, Parciales, Completos
   - Alertas: Pedidos incompletos > 7 días (🔴)
   - Gráfica: Pie chart

2. **Stock por Bodega**
   - Tabla: Bodega 1, 2, 40, 50
   - Columnas: Disponible, En Alquiler, Mantenimiento
   - Indicadores de nivel: 🔴 Sin stock, 🟡 Stock bajo, 🟢 Stock OK

3. **Remisiones del Día**
   - Lista de remisiones: Salidas y Entradas
   - Estado: Programada, En Tránsito, Entregada
   - Conductor asignado

4. **Cronograma de Recogidas**
   - Vista de calendario
   - Recogidas programadas vs realizadas
   - Alertas: Recogidas pendientes

5. **Novedades en Devoluciones**
   - Equipos dañados
   - Faltantes
   - Equipos ajenos
   - Requieren mantenimiento

6. **Rotación de Inventario**
   - Productos más rotados
   - Productos con baja rotación (candidatos a venta)
   - Días promedio de alquiler

**Filtros**:
- Bodega: Todas, Individual
- Fecha: Hoy, Semana, Mes
- Estado Pedido: Todos, Específico
- Tipo Remisión: Salida, Entrada, Cambio

---

#### 5.2.4. Dashboard Facturación

**Fuentes**: `agg_ventas_mes`, `fact_facturacion`, `facturas`

**KPIs Principales**:
1. **Facturas por Estado**
   - KPI Cards: Pendientes, Enviadas, Pagadas, Vencidas
   - Alertas: Facturas rechazadas DIAN (🔴)
   - Gráfica: Stacked bar chart

2. **Validación DIAN/Radian**
   - Estados: Sin Enviar, Enviada, Aceptada, Rechazada, Sin Confirmar
   - Tasa de aprobación: % facturas aceptadas
   - Alertas: Facturas pendientes validación > 48h

3. **Facturación por Centro de Costo**
   - CC 13 (Alquiler): Valor facturado
   - CC 14 (Venta/Reposición): Valor facturado
   - Comparativa mes anterior

4. **Retenciones Aplicadas**
   - Rte. Fuente por tipo (Alquiler, Transporte, Venta)
   - Rte. ICA
   - IVA
   - Gráfica: Stacked bar chart

5. **Modalidades de Facturación**
   - Por Remisión
   - Consolidada
   - Por Valor
   - Distribución y valor promedio

6. **Seguimiento Telefónico**
   - Clientes con dominio público (Gmail, Hotmail)
   - Facturas que requieren llamada
   - Estado: Pendiente, Contactado, Confirmado

**Filtros**:
- Centro de Costo: Todos, 13, 14
- Estado DIAN: Todos, Específico
- Período: Mes, Trimestre
- Cliente: Todos, Individual

---

#### 5.2.5. Dashboard Contabilidad/Cartera

**Fuentes**: `rpt_cartera_vencida`, `agg_forecast_facturacion`, `cartera`

**KPIs Principales**:
1. **Aging de Cartera**
   - Gráfica: Stacked horizontal bar chart
   - Tramos: 0-30, 31-60, 61-90, 91-180, +180 días
   - Valor total por tramo

2. **Top Clientes en Mora**
   - Tabla: Cliente, Monto, Días Mora, Última Gestión
   - Ordenado por monto descendente
   - Alertas: Mora > 90 días (🔴)

3. **Gestión de Cobro**
   - Facturas gestionadas hoy/semana
   - Tipo de contacto: Llamada, Email, Visita
   - Efectividad: % de pagos post-gestión

4. **Forecast de Facturación**
   - Proyección del mes en curso
   - Escenarios: Optimista, Realista, Pesimista
   - Comparativa con meta

5. **Pagos Recibidos**
   - Valor total pagado en el período
   - Método de pago: Transferencia, Efectivo, Cheque
   - Gráfica: Pie chart

6. **Indicador de Salud Financiera**
   - DSO (Days Sales Outstanding): Días promedio de cobro
   - % Cartera Vencida vs Total
   - Tendencia mensual

**Filtros**:
- Tramo de Mora: Todos, Específico
- Cliente: Todos, Individual
- Período: Mes, Trimestre, Año
- Estado Gestión: Todos, En Gestión, Acuerdo Pago, Demanda

---

#### 5.2.6. Dashboard Conductores

**Fuentes**: `agg_transporte_mes`, `rpt_conductores_viajes`, `agenda_transporte`

**KPIs Principales**:
1. **Viajes del Mes**
   - Total viajes realizados
   - Km totales recorridos
   - Toneladas transportadas
   - Gráfica: Line chart con tendencia diaria

2. **Liquidación Estimada**
   - Valor total a pagar
   - Desglose: Por km, por tonelada, bonificaciones
   - Comparativa mes anterior

3. **Cumplimiento de Criterios**
   - MP (Mantenimiento Preventivo): X/Y viajes
   - RTE (Recoger Totalidad): X/Y viajes
   - SER (Sale y Regresa): X/Y viajes
   - CL (Entrega mismo día): X/Y viajes
   - PP (Presentación Personal): X/Y viajes
   - Gráfica: Radial chart

4. **Viajes Calificados**
   - Viajes que califican para pago por tonelada
   - % de calificación
   - Alertas: Criterios no cumplidos

5. **Agenda del Día**
   - Lista de viajes programados
   - Hora inicio, destino, remisión
   - Estado: Pendiente, En Curso, Completado

6. **Historial de Vehículos**
   - Vehículos asignados en el período
   - Km por vehículo
   - Mantenimientos realizados

**Filtros**:
- Conductor: Individual (cada conductor ve solo sus datos)
- Período: Día, Semana, Mes
- Criterio: Todos, Específico
- Estado: Todos, Específico

---

#### 5.2.7. Dashboard Despachador

**Fuentes**: `fact_remisiones`, `agg_calidad_servicio_mes`, `remisiones`

**KPIs Principales**:
1. **Remisiones del Día**
   - Salidas programadas
   - Entradas esperadas
   - Estado: Programada, En Tránsito, Entregada, Recibida

2. **Conteo Físico vs Documentado**
   - Formato conductor vs Conteo despachador
   - Discrepancias
   - Equipos ajenos detectados

3. **Clasificación de Estado**
   - Equipos devueltos: BUENO, REGULAR, MALO
   - % por estado
   - Gráfica: Stacked bar chart

4. **Novedades Registradas**
   - Daños
   - Faltantes
   - Equipos ajenos
   - Requieren mantenimiento
   - Bajas

5. **Productividad**
   - Remisiones procesadas en el día
   - Tiempo promedio de procesamiento
   - Comparativa con otros despachadores

6. **Equipos Ajenos**
   - Lista de equipos ajenos en bodega
   - Empresa origen
   - Días en bodega
   - Estado: En Bodega, Devuelto

**Filtros**:
- Fecha: Hoy, Semana, Mes
- Tipo Remisión: Salida, Entrada
- Estado: Todos, Específico
- Novedad: Todos, Con Novedad

---

#### 5.2.8. Dashboard Recepción

**Fuentes**: `cronograma_recogidas`, `clientes`, `obras`

**KPIs Principales**:
1. **Cronograma del Día**
   - Recogidas programadas
   - Cliente, Obra, Frente
   - Número de corte (CT=XXXXX)
   - Estado: Programada, Parcial, Completada, Sin Recoger

2. **Cortes del Mes**
   - Total de cortes programados
   - Cortes completados
   - Cortes pendientes
   - Gráfica: Gauge chart (% completado)

3. **Alertas de Recogida**
   - Recogidas vencidas (fecha corte pasada)
   - Recogidas parciales pendientes
   - Clientes con múltiples cortes

4. **Actualización de Cronograma**
   - Formulario rápido para registrar nuevas recogidas
   - Campos: Cliente, Obra, Número Corte, Fecha Corte

5. **Notas y Observaciones**
   - Observaciones por cliente/obra
   - Instrucciones especiales de recogida
   - Contacto en obra

6. **Resumen Mensual**
   - Total recogidas programadas vs realizadas
   - Clientes atendidos
   - Obras cerradas

**Filtros**:
- Fecha: Hoy, Semana, Mes
- Estado: Todos, Programada, Completada, Sin Recoger
- Cliente: Todos, Individual
- Obra: Todas, Individual

---

#### 5.2.9. Dashboard SuperAdmin

**Fuentes**: `auditoria`, `usuarios`, `configuraciones`

**KPIs Principales**:
1. **Usuarios Activos**
   - Total usuarios por rol
   - Últimos logins
   - Usuarios inactivos (sin login > 30 días)

2. **Auditoría de Acciones**
   - Acciones por tipo: CREATE, UPDATE, DELETE, LOGIN
   - Top 10 usuarios con más acciones
   - Tabla afectada más modificada
   - Gráfica: Line chart de acciones por día

3. **Configuraciones del Sistema**
   - Tarifas de transporte por zona
   - Retenciones por tipo
   - Criterios de liquidación conductores
   - Última actualización

4. **Seguridad**
   - Intentos de login fallidos
   - IPs bloqueadas
   - Cambios en permisos de usuarios

5. **Rendimiento del Sistema**
   - Tiempo de respuesta promedio (API)
   - Procesos ETL: Estado, última ejecución, duración
   - Alertas de sistema

6. **Mantenimiento**
   - Tareas programadas
   - Backups realizados
   - Espacio en disco

**Filtros**:
- Usuario: Todos, Individual
- Tipo Acción: Todos, Específico
- Tabla: Todas, Específica
- Período: Día, Semana, Mes

---

## 6. PROCESO DE ETL Y ACTUALIZACIÓN

### 6.1. Flujo de Datos

```
TRANSACCIONAL (ODS)
    ↓ Tiempo Real
HECHOS (FACT)
    ↓ Batch Nocturno (2:00 AM)
AGREGADOS (AGG / RPT)
    ↓ On-Demand
DASHBOARDS
```

### 6.2. Procesos ETL

#### 6.2.1. ETL Tiempo Real (Triggers)

Tablas que se actualizan en tiempo real al insertar/actualizar datos transaccionales:

```sql
-- Trigger: Al crear una cotización → Insertar en fact_cotizaciones
CREATE TRIGGER trg_fact_cotizaciones_insert
AFTER INSERT ON cotizaciones
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_cotizaciones();

-- Trigger: Al crear un pedido → Insertar en fact_pedidos
CREATE TRIGGER trg_fact_pedidos_insert
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_pedidos();

-- Trigger: Al crear una remisión → Insertar en fact_remisiones
CREATE TRIGGER trg_fact_remisiones_insert
AFTER INSERT ON remisiones
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_remisiones();

-- Trigger: Al crear una factura → Insertar en fact_facturacion
CREATE TRIGGER trg_fact_facturacion_insert
AFTER INSERT ON facturas
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_facturacion();

-- Trigger: Al crear un movimiento de inventario → Insertar en fact_inventario_movimientos
CREATE TRIGGER trg_fact_inventario_insert
AFTER INSERT ON kardex_movimientos
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_inventario();

-- Trigger: Al registrar auditoría → Actualizar fact_productividad_usuarios
CREATE TRIGGER trg_fact_productividad_insert
AFTER INSERT ON auditoria
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_fact_productividad();
```

**Ventaja**: Los dashboards siempre muestran datos actualizados.

---

#### 6.2.2. ETL Batch Nocturno (Stored Procedures)

Procesos que se ejecutan cada noche a las 2:00 AM:

```sql
-- Procedimiento principal de ETL
CREATE PROCEDURE sp_etl_nocturno()
BEGIN
    -- 1. Limpiar tablas de agregados del día anterior
    TRUNCATE agg_dashboard_ejecutivo WHERE fecha_corte < CURRENT_DATE;

    -- 2. Regenerar agregados mensuales
    CALL sp_generar_agg_cotizaciones_mes();
    CALL sp_generar_agg_ventas_mes();
    CALL sp_generar_agg_inventario_mes();
    CALL sp_generar_agg_productividad_equipo();
    CALL sp_generar_agg_calidad_servicio_mes();
    CALL sp_generar_agg_analisis_clientes();
    CALL sp_generar_agg_forecast_facturacion();
    CALL sp_generar_agg_transporte_mes();

    -- 3. Generar dashboard ejecutivo
    CALL sp_generar_dashboard_ejecutivo('dia');
    CALL sp_generar_dashboard_ejecutivo('semana');
    CALL sp_generar_dashboard_ejecutivo('mes');
    CALL sp_generar_dashboard_ejecutivo('trimestre');
    CALL sp_generar_dashboard_ejecutivo('ano');

    -- 4. Actualizar reportería existente
    CALL sp_actualizar_rpt_kardex_cliente();
    CALL sp_actualizar_rpt_estado_pedidos();
    CALL sp_actualizar_rpt_facturacion_periodo();
    CALL sp_actualizar_rpt_cartera_vencida();
    CALL sp_actualizar_rpt_conductores_viajes();
    CALL sp_actualizar_rpt_inventario_rotacion();

    -- 5. Log de ejecución
    INSERT INTO etl_log (proceso, fecha_ejecucion, estado, duracion_seg)
    VALUES ('ETL Nocturno', NOW(), 'COMPLETADO', EXTRACT(EPOCH FROM (NOW() - start_time)));
END;
```

**Ejecución**: Cron job que ejecuta `sp_etl_nocturno()` cada noche.

---

#### 6.2.3. ETL On-Demand (Dashboards Personalizados)

Cuando un usuario filtra un dashboard con parámetros personalizados (ej: "Ver facturación del cliente X entre fecha Y y Z"), se ejecuta una consulta SQL directa:

```sql
-- Ejemplo: Consulta on-demand de facturación por cliente y período
SELECT
    f.fecha_emision,
    f.numero_factura,
    c.razon_social,
    f.subtotal,
    f.iva,
    f.rte_fuente,
    f.rte_ica,
    f.total,
    f.saldo_pendiente,
    f.estado,
    f.estado_radian
FROM facturas f
JOIN clientes c ON f.cliente_id = c.id
WHERE f.cliente_id = :cliente_id
  AND f.fecha_emision BETWEEN :fecha_inicio AND :fecha_fin
ORDER BY f.fecha_emision DESC;
```

**Optimización**: Índices en columnas de filtro frecuente (`cliente_id`, `fecha_emision`, `estado`, etc.)

---

### 6.3. Tabla de Control de ETL

```sql
-- Tabla para monitorear ejecuciones de ETL
Table etl_log {
  id                bigserial    [pk]
  proceso           varchar(100) [not null, note: 'Nombre del proceso ETL']
  fecha_ejecucion   timestamp    [default: `now()`]
  estado            varchar(20)  [note: 'INICIADO|COMPLETADO|ERROR']
  duracion_seg      integer      [note: 'Duración en segundos']
  registros_procesados integer   [note: 'Cantidad de registros procesados']
  error_mensaje     text         [note: 'Mensaje de error si aplica']

  indexes {
    proceso
    fecha_ejecucion
  }

  Note: 'Log de ejecuciones de procesos ETL — monitoreo y auditoría'
}
```

---

## 7. ESPECIFICACIÓN DE DASHBOARDS

### 7.1. Estructura de Componentes de Dashboard

Cada dashboard en el prototipo React debe tener la siguiente estructura:

```jsx
// Estructura estándar de dashboard
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { getData } from '../../data/store';

const DashboardXYZ = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [filters, setFilters] = useState({
    periodo: 'mes',
    fecha_inicio: null,
    fecha_fin: null
  });

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    // Cargar datos desde tablas agregadas o FACT
    const result = await getData('agg_dashboard_xyz', filters);
    setData(result);
  };

  return (
    <div className="dashboard-container">
      {/* Header con título y filtros */}
      <DashboardHeader title="Dashboard XYZ" filters={filters} onChange={setFilters} />

      {/* KPI Cards */}
      <div className="kpi-grid">
        <KPICard title="KPI 1" value={data?.kpi1} trend="+5%" />
        <KPICard title="KPI 2" value={data?.kpi2} trend="-2%" />
      </div>

      {/* Gráficas */}
      <div className="charts-grid">
        <ChartComponent type="line" data={data?.chartData1} />
        <ChartComponent type="bar" data={data?.chartData2} />
      </div>

      {/* Tabla de detalle */}
      <DataTable columns={columns} data={data?.tableData} />
    </div>
  );
};
```

---

### 7.2. Componentes Reutilizables

**Crear en `/src/components/dashboards/`**:

1. **KPICard.jsx**: Tarjeta de KPI con título, valor, tendencia y ícono
2. **ChartComponent.jsx**: Wrapper para Recharts con tipos (line, bar, pie, donut, area, scatter)
3. **DataTable.jsx**: Tabla con paginación, ordenamiento, filtros
4. **DashboardHeader.jsx**: Header con título, breadcrumb, filtros globales
5. **FilterPanel.jsx**: Panel de filtros lateral o colapsable
6. **ExportButton.jsx**: Botón para exportar a PDF/Excel
7. **DateRangePicker.jsx**: Selector de rango de fechas
8. **TrendIndicator.jsx**: Indicador de tendencia (↑ +5%, ↓ -2%)

---

### 7.3. Paleta de Colores para Gráficas

```css
/* En design-system.css */
--chart-primary: #b5000b;
--chart-secondary: #1a1c1c;
--chart-success: #38A169;
--chart-warning: #FF9F1C;
--chart-danger: #E53E3E;
--chart-info: #3182CE;
--chart-purple: #805AD5;
--chart-teal: #38B2AC;
--chart-pink: #D53F8C;
--chart-orange: #DD6B20;

/* Gradientes para áreas */
--chart-gradient-primary: linear-gradient(180deg, rgba(181,0,11,0.3) 0%, rgba(181,0,11,0) 100%);
--chart-gradient-success: linear-gradient(180deg, rgba(56,161,105,0.3) 0%, rgba(56,161,105,0) 100%);
```

---

## 📊 RESUMEN FINAL

### Totales de Tablas

| Categoría | Cantidad | Detalle |
|-----------|----------|---------|
| **Tablas Operacionales (ODS)** | 48 | Inventario DBML completo |
| **Tablas de Hechos (FACT)** | 8 | Nuevas propuestas para análisis |
| **Dimensiones (DIM)** | 2 | dim_fecha, dim_hora |
| **Agregados (AGG/RPT)** | 15 | 6 existentes + 9 nuevos |
| **Control ETL** | 1 | etl_log |
| **TOTAL** | **74 tablas** | Sistema completo de datos |

### Dashboards por Rol

| Rol | Dashboards | KPIs | Actualización |
|-----|-----------|------|---------------|
| CEO/Gerencia | 1 | 6 | Tiempo real |
| Comercial | 1 | 6 | Tiempo real |
| Dibujante | 1 | 5 | Tiempo real |
| Almacén | 1 | 6 | Tiempo real |
| Conductor | 1 | 6 | Tiempo real |
| Facturación | 1 | 6 | Tiempo real |
| Contabilidad/Cartera | 1 | 6 | Batch diario |
| Despachador | 1 | 6 | Tiempo real |
| Recepción | 1 | 6 | Tiempo real |
| SuperAdmin | 1 | 6 | Tiempo real |
| **TOTAL** | **10 dashboards** | **59 KPIs** | - |

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Modelo de Datos (2 semanas)
- [ ] Crear 8 tablas FACT en PostgreSQL
- [ ] Crear 2 tablas DIM (dim_fecha, dim_hora)
- [ ] Crear 9 nuevos agregados (AGG)
- [ ] Crear tabla de control ETL (etl_log)
- [ ] Generar scripts de migración

### Fase 2: Procesos ETL (2 semanas)
- [ ] Implementar triggers para actualización tiempo real de FACT
- [ ] Crear stored procedures para agregados nocturnos
- [ ] Configurar cron job para ETL nocturno (2:00 AM)
- [ ] Implementar tabla de log de ETL
- [ ] Pruebas de integridad de datos

### Fase 3: Componentes de Dashboard (3 semanas)
- [ ] Crear componentes reutilizables (KPICard, ChartComponent, etc.)
- [ ] Implementar Dashboard Ejecutivo (CEO)
- [ ] Implementar Dashboard Comercial
- [ ] Implementar Dashboard Almacén
- [ ] Implementar Dashboard Facturación
- [ ] Implementar Dashboard Contabilidad/Cartera
- [ ] Implementar Dashboard Conductores
- [ ] Implementar Dashboard Despachador
- [ ] Implementar Dashboard Recepción
- [ ] Implementar Dashboard SuperAdmin

### Fase 4: Integración y Optimización (1 semana)
- [ ] Optimizar consultas SQL con índices
- [ ] Implementar caché de dashboards
- [ ] Pruebas de carga y rendimiento
- [ ] Ajustes de UX/UI según feedback
- [ ] Documentación de usuario

### Fase 5: Validación y Lanzamiento (1 semana)
- [ ] Pruebas con usuarios finales por rol
- [ ] Ajustes basados en feedback
- [ ] Capacitación a usuarios
- [ ] Lanzamiento a producción
- [ ] Monitoreo post-lanzamiento

---

**Versión:** 2.0
**Fecha:** 18 de Julio 2026
**Autor:** Equipo de Desarrollo G&H
**Estado:** Propuesta Completa — Pendiente de Aprobación

---

