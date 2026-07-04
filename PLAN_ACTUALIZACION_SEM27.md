# Plan de Actualización — SEM-27 · Entrevistas de Feedback (Facturación e Inventario)
**G&H Obras y Estructuras Metálicas S.A.S**
Generado: 2026-07-04 · Basado en: `interviews/facturacion.txt` + `interviews/inventario.txt` + `feedback_24_jun.txt`

---

## Resumen ejecutivo

Las entrevistas con el área de facturación (Lenix y Angie) y el área de almacén/logística revelan **13 hallazgos nuevos de negocio en facturación** y **13 hallazgos nuevos en inventario** que no están recogidos en la documentación actual. Este plan lista qué archivo cambia, por qué, y exactamente qué debe modificarse. El `generate_report.py` no necesita cambios estructurales; al actualizar los archivos `.mmd` y `.md`, el reporte HTML se regenera automáticamente.

---

## Índice de hallazgos por módulo

### Facturación (nuevos — de `interviews/facturacion.txt`)
| # | Hallazgo | Impacto |
|---|----------|---------|
| F-1 | Centros de costo: 13 = Alquileres · 14 = Ventas/Reposiciones → aplicación automática por tipo de línea | Flujo, DB, US |
| F-2 | Retenciones por tipo de concepto: transporte ≠ alquiler (Rte. 1% flete vs. alquiler). Si se mezclan, Siigo rechaza la factura. Cada línea debe tener su retención automática | Flujo, Sitemap, US, Checklist |
| F-3 | Catálogos DUALES: (a) catálogo general anual + (b) precios especiales por cliente (ej: Marval = 30 obras, mismos precios) | Flujo cotización, Roles, DB, US |
| F-4 | Modalidades de facturación: por remisión, consolidada o "por valor" ("meta lo que quepa en este monto") | Flujo, US |
| F-5 | Validación de envío: CUFE + Radian (DIAN) es la prueba oficial, no el estado en Siigo | Flujo, US, Checklist |
| F-6 | Clientes con dominio público (Gmail/Hotmail) no pueden dar "recibido" electrónico → Cartera les llama; los corporativos con sistema contable sí dan el triple check automático | Flujo, US |
| F-7 | Coordinadora de Facturación (Lenix) necesita permiso de **crear/editar cliente** por el caso Bronz/fiducia (contrato a nombre del consorcio pero paga la fiducia; solo 2 clientes fiducia para 16 frentes) | Roles (tabla + diagrama) |
| F-8 | Precio de transporte: por **peso Y volumen** (un camión que va lleno en volumen pero no alcanza el tope de toneladas se cobra al valor de ese camión) — no solo toneladas | Flujo cotización, Checklist, US |
| F-9 | Período principal de facturación: **mensual** con cortes por obra y por línea de producto | Flujo, US |
| F-10 | Informes por equipo: funcionalidad existente en Siigo pero inhabilitada/rota → requerimiento para el nuevo sistema | US |
| F-11 | Una remisión puede descontarse de **múltiples clientes y/o frentes** (caso subcontratista + contratante en misma obra con equipo revuelto) | Flujo inventario, DB, US |
| F-12 | Separación de responsabilidades: Facturación **solo genera y valida envío a DIAN**; Cartera hace el seguimiento de pagos y cobros | Flujo principal, Roles |
| F-13 | Actualización de precios del catálogo: **Recepción** actualiza los listados anualmente y los distribuye a todas las áreas; comerciales notifican por escrito cuando dan precios especiales fuera de catálogo | Roles, Flujo cotización |

### Inventario / Logística (nuevos — de `interviews/inventario.txt`)
| # | Hallazgo | Impacto |
|---|----------|---------|
| I-1 | **Flujo bidireccional Almacén ↔ Recepción** diario: Viviana (Recepción) envía cronograma cada día; Almacén (Angie) devuelve las recogidas realizadas | Flujo, Roles, Diagrama |
| I-2 | **Pedidos parciales**: un pedido puede enviarse en múltiples viajes hasta completarse; Angie controla en Excel con fórmula de pendiente; estado: "salió parcial" / "salió completo" | Flujo inventario, Sitemap, DB, US |
| I-3 | **Inicio del alquiler**: el contador de días corre desde que el pedido está **completo** (no desde el primer envío parcial) | Flujo inventario, US, DB |
| I-4 | **3 fuentes de control en devolución**: (a) formato del conductor, (b) formato del despachador (en bodega), (c) fotos de portería de la obra → comparación manual; chapetas en canecas = no verificable por foto | Flujo inventario, US |
| I-5 | **Rol Despachador**: persona fija en bodega que cuenta el equipo que entra/sale (distinto del conductor). Actualmente no está como rol en el sistema | Roles, Diagrama arquitectura |
| I-6 | **Cancelación de pedidos**: las obras pueden cancelar; no existe política definida; la gestiona el ingeniero con el cliente → requerimiento de política documentada | US, Checklist |
| I-7 | **Mantenimiento vs. Reposición**: el conductor define el estado inicial (mantenimiento = equipo reparable, asumido por G&H; reposición = cobro al cliente); el despachador puede corregir esa clasificación | Flujo inventario, US, Checklist |
| I-8 | **Equipo ajeno**: puede llegar equipo que NO es de G&H → debe devolverse a la empresa correspondiente; debe tener categoría específica en el sistema | Flujo inventario, DB |
| I-9 | **Préstamo de equipo entre frentes**: en obras grandes (ej: El Bronz con 15 sucursales), el equipo se presta entre frentes; al devolver, el frente que devuelve no coincide con el que lo recibió → desajuste de inventario; Angie busca manualmente en cuál frente puede descontar sin quedar en negativo | Flujo inventario, US |
| I-10 | **Inventario en negativo**: el módulo actual convierte todo a positivo → saldo real desconocido; el nuevo sistema debe mostrar negativos correctamente para identificar descuadres | US, Checklist |
| I-11 | **No existe inventario estandarizado real**: solo catálogos; el conteo anual fracasó porque el personal asignado no sabía distinguir referencias (tubo 1" vs 1.5" vs 2") | Flujo, Checklist |
| I-12 | **Códigos separados alquiler vs. venta**: al hacer una venta a veces toman equipo del inventario de alquiler, descuadrando códigos → el sistema debe proteger esta distinción | DB, US |
| I-13 | **Ingenieros coordinan el despacho**: son quienes autorizan qué sale, cuándo, verifican si hay contrato firmado, si hay fundida en obra ese día, etc. → son actores clave del flujo de salida | Flujo inventario, Roles |

---

## Cambios por archivo

---

### 1. `architecture/01_flujo_principal_gyh.mmd` — Flujo Principal

**Qué cambiar:**

**a) Módulo INVENTARIOS** — añadir sub-nodos:
- Dividir `SALIDA` en dos pasos: (1) el ingeniero autoriza el despacho y (2) Almacén genera remisión de salida
- Añadir nodo `PARCIAL` para pedidos en múltiples viajes: decisión `¿Pedido completo?` → si No, sigue acumulando; si Sí, inicia contador de alquiler
- Renombrar `ENTRADA` → incluir en su label la lógica de 3 fuentes: conductor + despachador + fotos
- Añadir nodo `MANT` (Mantenimiento): en la decisión de `ITEMQ` (estado de equipo devuelto) agregar rama "Mantenimiento" que no genera cobro (va a reparación interna) → diferente de "Daño" que sí genera cobro
- Añadir nodo `EQUIPO_AJENO` en la inspección de entrada: equipo que no pertenece a G&H
- Hacer explícita la distinción: la remisión puede descontarse de múltiples clientes/frentes (nota en el nodo o subgraph)

**b) Módulo FACTURACIÓN** — ajustar nodos:
- Separar claramente: `FACTURA` solo genera y valida envío a DIAN (CUFE + Radian)
- `CARTERA` es quien hace seguimiento de pago; añadir flujo: cliente con dominio público → llamada telefónica; cliente corporativo → triple check automático
- Añadir decisión `¿Modalidad factura?` → por remisión / consolidada / por valor
- Añadir nota de centros de costo (13 alquileres, 14 ventas/reposiciones)

**c) Módulo PREVENTA (COTIZACIÓN)** — añadir tipo de catálogo:
- Añadir decisión en cotización: `¿Cliente con precio especial?` → usa catálogo especial del cliente; si no, usa catálogo general

**Nodos a agregar (texto sugerido):**
```
INGAPRUEBA["👷 Ingeniero autoriza\ndespacho + verifica\ncontrato y fecha de obra"]
PEDIDOQ{"¿Pedido\ncompleto?"}
PARCIAL_ACU["📦 Acumular viajes\nhasta completar pedido"]
ALQUILER_INICIA["📅 Inicia contador\ndías de alquiler"]
MANT["🔧 Mantenimiento\nReparación interna\n(sin cobro al cliente)"]
EQUIPO_AJENO["↩️ Equipo ajeno\nDevolver a empresa\ncorrespondiente"]
CUFE["📋 CUFE + Radian\nValidación DIAN\n(prueba oficial de envío)"]
MODALIDADFAC{"¿Modalidad\nde factura?"}
```

---

### 2. `architecture/02_arquitectura_sistema.mmd` — Arquitectura del Sistema

**Qué cambiar:**

**a) Usuarios del sistema** — añadir:
- `U7["📦 Despachador"]` (bodeguero que cuenta equipos, distinto del conductor)
- Actualizar `U3` de "Contabilidad" a incluir "Facturación / Cartera" como descripción
- Añadir `U8["🏗️ Recepción"]` (Viviana → cronograma diario)

**b) Frontend** — añadir:
- `FE5` (Módulo Inventarios) debe indicar: "Remisiones · Pedidos Parciales · Agenda · Despachador"
- `FE6` (Módulo Facturación) debe indicar: "Facturas · Centros Costo · DIAN/CUFE · Cartera"

**c) Backend** — añadir:
- `BE4` (Inventarios API): añadir "Pedidos Parciales · Kardex negativo · Préstamo entre frentes"
- `BE5` (Facturación API): añadir "Centros de Costo · Retenciones por línea · CUFE"
- Nuevo: `BE9["🏪 Catálogo API\nPrecios general + especiales\npor cliente"]`

**d) Base de Datos** — añadir:
- `DB3` (inventario): añadir "Pedidos · Parciales · Códigos alquiler/venta"
- `DB6` (catálogo): añadir "Precios especiales por cliente · Unidades negocio"
- Nuevo: `DB7[("🗄️ pedidos\nParciales · Estado · Autorización ingeniero")]`

**e) Integraciones Externas** — añadir:
- `EXT4["📊 DIAN / Radian\nCUFE · Validación factura electrónica"]`

---

### 3. `architecture/03_modulo_cotizacion.mmd` — Módulo de Cotizaciones

**Qué cambiar:**

**a) En el subgraph DIBUJANTE:**
- Ajustar `CATALOG` para indicar que consulta primero si el cliente tiene precios especiales:
  ```
  CATALOG["📚 Consulta Catálogo\n¿Cliente con precio especial?\n→ Catálogo del cliente\nSi no → Catálogo general anual"]
  ```
- Añadir: `UNEG{"¿Unidad de negocio?"}` con ramas a Formaleta Metálica, Multidireccional, Formaleta Plástica, Formaleta Tradicional, Transporte (ya en checklist pero faltaba explicitarlo en el flujo de cotización)

**b) En el subgraph COMERCIAL:**
- Añadir detalle en `DESCUENTO`:
  ```
  PRECIOSPEC["💲 Precio especial por cliente\nAcuerdo fuera de catálogo\n(notificación escrita al área de facturación)"]
  ```
- Para transporte: añadir nota de que el precio es por **peso Y volumen** (no solo toneladas)

**c) En CONTABILIDAD_REV:**
- Actualizar `RETENC` para especificar: "Transporte: Rte. 1% · Alquiler: Rte. según tarifa · Centro Costo 13/14"

**d) En SALIDA:**
- Antes de `ORDEN`, añadir: `PRECSPEC_NOT["📧 Notificar a Facturación\nprecios especiales acordados\npor escrito"]`

---

### 4. `architecture/04_registro_aprobacion_cliente.mmd` — Registro y Aprobación de Clientes

**Qué cambiar:**

Sin cambios estructurales nuevos. Ya incorpora: notas obligatorias por área, CEO con aprobación forzada, notificación automática. Sin embargo, ajustar:

**a) En el nodo de rechazo** — añadir subpath:
- `RECHAZADO` → `CEO_REVISA["🏗️ CEO puede revisar\nmotivos detallados y\nforzar aprobación bajo\nsu responsabilidad"]`
- Añadir flecha desde `RECHAZADO` al CEO_REVISA con label "¿CEO fuerza aprobación?"

**b) En `F3` (Referencias Bancarias) y `F4` (Referencias Comerciales):**
- El sistema debe registrar si el cliente tiene **dominio de correo público** (Gmail/Hotmail) o **corporativo** → esto afecta la estrategia de cobro en cartera
- Añadir campo en la sección de contacto: `Tipo de sistema contable del cliente` (Con / Sin sistema contable)

**c) Mencionar explícitamente** que Facturación puede editar datos del cliente por el caso de clientes con múltiples frentes y facturación a fiducia diferente del contratante

---

### 5. `architecture/05_modulo_inventarios_logistica.mmd` — Inventarios y Logística

**Es el diagrama con más cambios (8 hallazgos nuevos).**

**a) Añadir nodo INGENIERO antes de REMSAL:**
```
INGENIERO["👷 Ingeniero autoriza\ndespacho:\n― Contrato firmado ✓\n― Fecha no hay fundida ✓\n― Pedido listo ✓"]
```
Flujo: `KARDEX_TOTAL → INGENIERO → REMSAL`

**b) Añadir flujo de pedidos parciales:**
```
PEDIDOQ{"¿Pedido\ncompleto?"}
PARCIAL_ACU["📋 Acumular envío parcial\n(Angie registra qué salió\ny qué queda pendiente)"]
```
Flujo: Después de `ENTREGA`, añadir `PEDIDOQ`. Si No → `PARCIAL_ACU` → vuelve a `AGENDA` para el siguiente viaje. Si Sí → `ALQUILER_INICIA["📅 Inicia contador días\nalquiler — pedido completo"]` → `ALQUILER_VIGENTE`.

**c) En RETORNO — ampliar `ITEMQ`** con una cuarta rama:
```
ITEM_MANT["🔧 Mantenimiento\nReparación interna\nG&H asume el costo\n(no se cobra al cliente)"]
ITEM_AJENO["↩️ Equipo ajeno\nDevolver a empresa\ncorrespondiente"]
```

**d) En la inspección de entrada**, añadir subgraph de las 3 fuentes:
```
subgraph VERIFICACION["🔍 Verificación 3 Fuentes"]
    VF1["📋 Formato Conductor\n(lo que dice haber traído)"]
    VF2["📋 Formato Despachador\n(conteo físico en bodega)"]
    VF3["📸 Fotos Portería Obra\n(evidencia salida desde obra)"]
    CUADRA{"¿Cuadra?"}
    AJUSTE["⚖️ Acción de Ajuste\nCruzar frentes/clientes\nhasta cuadrar inventario"]
end
```

**e) Añadir flujo de préstamo entre frentes:**
```
PRESTAMO["↔️ Equipo prestado\nentre frentes de obra\n(descontar del frente correcto)"]
CRUCE_FRENTES["🔄 Cruzar frentes/sucursales\ndel mismo cliente para\ncuadrar inventario"]
```

**f) Añadir flujo diario Viviana:**
```
VIVIANA["📅 Cronograma diario\n— Viviana (Recepción)\nCliente · Obra · Fecha corte"]
RECOGIDAS_REPORTADAS["📤 Angie reporta\nrecogidas realizadas\na Viviana"]
```

**g) Actualizar la nota del Kardex total:**
```
KARDEX_TOTAL["📊 Stock Total (Momento Cero)\nBodega + En Clientes + En Producción\n⚠️ Sin inventario real — catálogos\n(negativos visibles en el nuevo sistema)"]
```

**h) Añadir nodo de cancelación:**
```
CANCELQ{"¿Obra cancela\nel pedido?"}
CANCELACION["❌ Cancelación\nde Pedido\nGestión por Ingeniero"]
```

---

### 6. `architecture/06_roles_y_permisos.mmd` — Diagrama de Roles

**Qué cambiar:**

**a) Añadir rol `R_DESP` (Despachador):**
```
R_DESP["📦 DESPACHADOR"]:::rol
```
Permisos: `IV1` (ver stock), `IV5` (confirmar recepción), nuevo `IV7` ("Clasificar estado equipo: OK/Daño/Mant/Faltante/Ajeno")

**b) Añadir rol `R_REC` (Recepción):**
```
R_REC["🗓️ RECEPCIÓN"]:::rol
```
Permisos: nuevo `IV8` ("Enviar cronograma diario de recogidas"), `IV1` (ver stock solo lectura)

**c) En `MOD_FAC` — añadir acción para Facturación:**
```
FA5["Editar datos cliente (caso fiducia)"]:::accion
FA6["Generar CUFE / validar envío DIAN"]:::accion
FA7["Gestionar centros de costo 13/14"]:::accion
```
- `R_CONT` accede a `FA5 & FA6 & FA7`

**d) En `MOD_COT` — añadir:**
```
CQ7["Gestionar precios especiales por cliente"]:::accion
```
- Solo `R_COM` y `R_ADMIN`

**e) Añadir en `MOD_INV`:**
```
IV7["Clasificar estado equipo devuelto\n(OK / Daño / Mant / Faltante / Ajeno)"]:::accion
IV8["Enviar cronograma diario de recogidas"]:::accion
IV9["Autorizar despacho de pedido"]:::accion
```
- `IV7`: R_DESP y R_ALM
- `IV8`: R_REC
- `IV9`: R_COM (ingenieros/comerciales)

**f) R_CONT** — añadir permiso de editar cliente: `MC2` (con nota de "solo caso fiducia/facturación")

---

### 7. `architecture/06_roles_y_permisos_tabla.md` — Tabla de Roles

**Qué cambiar:**

**a) Añadir columnas** para los 2 nuevos roles: **Despachador** y **Recepción**. La tabla pasa de 8 a 10 roles.

**b) Módulo Clientes y Prospectos:**
| Acción | Nuevo: Despachador | Nuevo: Recepción |
|--------|--------------------|------------------|
| Ver lista de clientes/prospectos | ◎ | — |
| Crear / editar cliente | — | — |
| (todas las demás) | — | — |

Además: añadir nueva fila:
- `Editar datos de cliente para facturación (caso fiducia)` → Contabilidad ✓, Admin ✓, resto —

**c) Módulo Cotizaciones:**
- Añadir fila: `Gestionar catálogo de precios especiales por cliente` → Admin ✓, Comercial ✓, resto —

**d) Módulo Inventarios y Logística:**
Añadir filas:
- `Clasificar estado de equipo devuelto (OK/Daño/Mant/Faltante/Ajeno)` → Almacén ✓, Despachador ✓, resto —
- `Autorizar despacho de pedido` → Comercial ✓ (ingeniero), Admin ✓, resto —
- `Enviar cronograma diario de recogidas` → Recepción ✓, Admin ✓, resto —
- `Registrar equipo ajeno devuelto` → Almacén ✓, Despachador ✓, resto —

**e) Módulo Facturación:**
Añadir filas:
- `Generar CUFE y validar envío a DIAN` → Contabilidad ✓, Admin ✓, resto —
- `Gestionar centros de costo (13 Alquileres / 14 Ventas)` → Contabilidad ✓, Admin ✓, resto —
- `Editar datos de cliente para facturación (fiducia)` → Contabilidad ✓, Admin ✓, resto —

**f) Actualizar sección "Catálogo de Productos — Unidades de Negocio":**
Añadir tabla de tipos de precio:
```markdown
## Tipos de Catálogo de Precios
| Tipo | Descripción |
|------|-------------|
| **General anual** | Actualizado por Recepción cada año y distribuido a todas las áreas |
| **Especial por cliente** | Acordado por Comercial; notificación escrita a Facturación |
```

**g) Añadir sección de Centros de Costo:**
```markdown
## Centros de Costo — Facturación
| Centro | Tipo |
|--------|------|
| 13 | Alquileres |
| 14 | Ventas y Reposiciones |
```

---

### 8. `sitemaps/sitemap_05_inventarios.mmd` — Sitemap Inventarios

**Qué añadir:**

**a) En `S_REM` — añadir sub-nodos para pedidos parciales:**
```
INV_PED["📋 Pedidos\n/inventarios/pedidos\nEstado: Pendiente · Parcial · Completo"]
INV_PED_PARCIAL["⏳ Pedido Parcial\n/inventarios/pedidos/:id/parciales\nAcumulación de envíos"]
INV_REM --> INV_PED
INV_PED --> INV_PED_PARCIAL
```

**b) En `S_LOGISTICA` — añadir:**
```
INV_CRON["📅 Cronograma Diario Recogidas\n/inventarios/cronograma\n(Viviana → Almacén ida y vuelta)"]
INV_CANCEL["❌ Cancelaciones de Pedido\n/inventarios/cancelaciones"]
```

**c) Añadir nuevo subgraph `S_INSPECCION`:**
```
subgraph S_INSPECCION["INSPECCIÓN DE DEVOLUCIONES"]
    INV_INSP["🔍 Inspección\n/inventarios/devoluciones/inspeccion\nEstado: OK · Daño · Mant · Faltante · Ajeno"]
    INV_AJENO["↩️ Equipo Ajeno\n/inventarios/ajeno\nDevolución a empresa externa"]
    INV_PRESTA["↔️ Préstamo entre frentes\n/inventarios/prestamos-frentes"]
end
INV --> S_INSPECCION
```

---

### 9. `sitemaps/sitemap_06_facturacion.mmd` — Sitemap Facturación

**Qué añadir:**

**a) En `S_FAC`:**
```
FAC_MOD["📋 Modalidad de Factura\n/facturacion/facturas/nueva\n→ Por remisión · Consolidada · Por valor"]
FAC_CC["🏷️ Centro de Costo\n/facturacion/centros-costo\n13 Alquiler · 14 Venta"]
FAC_DIAN["📋 CUFE / Radian\n/facturacion/:id/dian\nValidación envío DIAN"]
```

**b) Nuevo subgraph `S_CATALOGO_PRECIOS`:**
```
subgraph S_CAT_PRECIOS["CATÁLOGOS DE PRECIOS"]
    FAC_CAT_GEN["📚 Catálogo General\n/facturacion/catalogo/general\nPrecios anuales"]
    FAC_CAT_ESP["⭐ Precios Especiales\n/facturacion/catalogo/especiales\nPor cliente"]
end
FAC --> S_CAT_PRECIOS
```

**c) En `S_CART`** — detallar estados de cartera:
```
FAC_CART_EST["📊 Estados de Cartera\nNueva · En Gestión · Acuerdo Pago\nDemanda · Castigada · Recuperada"]
FAC_CART_CONT["📞 Gestión de Contacto\nCliente dominio público → llamada\nCliente corporativo → validar triple check DIAN"]
```

---

### 10. `user-stories/historias_usuario.md` — Historias de Usuario

**Añadir las siguientes historias nuevas:**

#### US-015 · Facturación por modalidad (nueva)
**Como** Coordinadora de Facturación  
**Quiero** elegir la modalidad de factura al generarla: por remisión / consolidada / por valor  
**Para** adaptar el cobro a la preferencia de cada cliente

**CAs:**
- AC-001: El sistema permite seleccionar: "Por remisión" (una factura por remisión), "Consolidada" (alquiler de un mes en una factura) o "Por valor" (el usuario define el monto y el sistema incluye ítems hasta alcanzarlo)
- AC-002: Transporte siempre va en factura separada (retención diferente)
- AC-003: El sistema aplica automáticamente el centro de costo 13 a alquileres y 14 a ventas/reposiciones
- AC-004: Cada tipo de concepto carga automáticamente su retención por defecto (sin ajuste manual)

#### US-016 · Catálogos de precios duales (nueva)
**Como** Dibujante o Comercial  
**Quiero** que el sistema detecte si el cliente tiene precios especiales y aplique el catálogo correcto automáticamente  
**Para** evitar errores de precio y el proceso manual actual

**CAs:**
- AC-001: Al crear una cotización, el sistema verifica si el cliente tiene precios especiales registrados
- AC-002: Si tiene precios especiales, se aplica su catálogo; si no, se aplica el catálogo general vigente
- AC-003: Solo Admin puede crear/editar catálogos de precios especiales por cliente
- AC-004: El precio de transporte se calcula por peso Y volumen (la restricción de volumen puede activar la tarifa del camión aunque no se alcance el tope de toneladas)

#### US-017 · Validación de envío de factura a DIAN (nueva)
**Como** Coordinadora de Facturación  
**Quiero** validar que la factura fue efectivamente enviada y registrada en la DIAN  
**Para** tener una prueba oficial de envío independientemente del estado que muestra Siigo

**CAs:**
- AC-001: Al generar la factura, el sistema registra el CUFE y el estado en el Radian
- AC-002: La prueba de envío es el registro en la DIAN; el estado en Siigo se muestra como referencia pero no es la fuente de verdad
- AC-003: El sistema distingue entre clientes con sistema contable (dan triple check automático) y clientes con dominio público (Gmail/Hotmail — no darán el check, seguimiento por teléfono)
- AC-004: Al detectar un cliente con dominio público, el sistema genera alerta a Cartera para seguimiento telefónico manual

#### US-018 · Gestión de pedidos parciales de inventario (nueva)
**Como** Jefe de Almacén  
**Quiero** registrar el envío de un pedido en múltiples viajes y marcar cuándo está completo  
**Para** que el alquiler inicie solo cuando el pedido está completamente entregado

**CAs:**
- AC-001: Un pedido puede tener estado: Pendiente / Parcial / Completo
- AC-002: Cada envío parcial se registra como una remisión vinculada al mismo pedido
- AC-003: El sistema muestra qué ítems han salido y cuáles quedan pendientes por pedido
- AC-004: El contador de días de alquiler se inicia **solo** cuando el pedido alcanza el estado "Completo"
- AC-005: El ingeniero debe autorizar el despacho antes de que Almacén genere la remisión (verificando: contrato firmado, fecha libre de obra)
- AC-006: El pedido puede marcarse como "Cancelado" con motivo y registro del ingeniero que aprobó la cancelación

#### US-019 · Inspección multi-fuente de devoluciones (nueva)
**Como** Jefe de Almacén o Despachador  
**Quiero** registrar la devolución comparando el formato del conductor, el conteo del despachador y las fotos de portería  
**Para** tener trazabilidad completa y resolver discrepancias con evidencias

**CAs:**
- AC-001: La devolución registra: (a) lo que dice el conductor, (b) el conteo del despachador, (c) adjuntos de fotos
- AC-002: Si no cuadran, el sistema marca la discrepancia y permite registrar el ajuste con justificación
- AC-003: Cada equipo devuelto se clasifica como: OK / Dañado / Mantenimiento / Faltante / Ajeno
  - Mantenimiento: G&H asume el costo de reparación; no se factura al cliente
  - Faltante: se genera ítem de reposición (cobro al cliente según precio del catálogo)
  - Ajeno: equipo no perteneciente a G&H → se registra para devolución a empresa externa
- AC-004: El despachador puede reclasificar el estado asignado por el conductor

#### US-020 · Cruce de inventario entre frentes de obra (nueva)
**Como** Jefe de Almacén  
**Quiero** poder descontar el equipo devuelto del frente correcto aunque el conductor lo trajo del frente equivocado  
**Para** mantener el inventario cuadrado sin rechazar la devolución

**CAs:**
- AC-001: Al registrar una devolución, si el frente registrado queda en negativo, el sistema sugiere los frentes del mismo cliente donde podría descontarse
- AC-002: El sistema muestra el inventario con valores negativos reales (no los convierte a positivo)
- AC-003: El usuario puede reasignar la devolución a otro frente del mismo cliente con registro de auditoría
- AC-004: Para clientes con múltiples sucursales (ej: El Bronz con 15 frentes), se puede ver el inventario consolidado y el desglose por frente

#### US-021 · Gestión de catálogo con precios especiales por cliente (nueva)
**Como** Coordinadora de Facturación  
**Quiero** editar los datos del cliente en el caso de que facture a una entidad diferente del contratante  
**Para** poder emitir facturas a la fiducia correcta sin crear clientes duplicados

**CAs:**
- AC-001: Contabilidad tiene permiso de editar el nombre de facturación del cliente (sin modificar otros datos del expediente)
- AC-002: Se registra el motivo del cambio y quién lo hizo (auditoría)
- AC-003: Un cliente puede tener un "Nombre de contrato" (quien firma) y un "Nombre de facturación" (quien paga/recibe la factura) como campos separados

#### US-022 · Cronograma diario de recogidas (nueva)
**Como** Recepción (Viviana)  
**Quiero** enviar el cronograma diario de cortes y recogidas al área de Almacén desde el sistema  
**Para** reemplazar el Excel enviado por correo y tener trazabilidad del cronograma

**CAs:**
- AC-001: Recepción puede crear y publicar el cronograma diario con: obra, cliente, número de corte, fecha
- AC-002: Almacén ve el cronograma en su módulo y actualiza el estado de cada recogida
- AC-003: Al final del día, el sistema genera el reporte de recogidas realizadas vs. programadas
- AC-004: El sistema genera alerta si una recogida programada no se completó

#### US-023 · Informes por equipo (nueva)
**Como** Coordinadora de Facturación o Jefe de Almacén  
**Quiero** generar informes por referencia de equipo (cuánto ha estado alquilado, dónde está, historial de reposiciones)  
**Para** tener visibilidad de la rentabilidad y estado de cada equipo

**CAs:**
- AC-001: El informe muestra por código de equipo: ubicación actual, días en alquiler acumulados, veces en mantenimiento, veces en reposición
- AC-002: Se puede filtrar por unidad de negocio, fecha y cliente
- AC-003: El informe distingue entre código de alquiler y código de venta

---

**Actualizar las siguientes historias existentes:**

#### US-010 (actualizar)
- Añadir AC-006: El sistema muestra explícitamente cuando la cantidad devuelta genera inventario negativo en algún frente, para que el usuario gestione el cruce manual
- Añadir AC-007: El mantenimiento (equipo dañado reparable) queda registrado por separado de la reposición (equipo irrecuperable o perdido)

#### US-011 (actualizar)
- Añadir AC-007: La factura aplica automáticamente el centro de costo 13 a alquileres y 14 a ventas/reposiciones
- Añadir AC-008: Si el cliente tiene precios especiales, el sistema los aplica automáticamente al generar la factura
- Añadir AC-009: El precio de transporte se calcula por peso Y volumen (el sistema carga la tarifa del camión si el volumen ocupa la totalidad, aunque no se alcance el tope en toneladas)
- Actualizar AC-002: El cálculo de días de alquiler parte de la fecha en que el **pedido quedó completo** (no del primer envío parcial)

#### US-012 (actualizar — Cartera)
- Añadir AC-005: El sistema marca si el cliente tiene dominio público (Gmail/Hotmail) o corporativo, para guiar la estrategia de cobro (llamada vs. triple check automático DIAN)
- Añadir AC-006: El módulo de Cartera incluye la opción de adjuntar la evidencia CUFE + Radian como prueba de envío ante el cliente que alega no haber recibido la factura

#### US-008 (actualizar — Remisión de salida)
- Añadir AC-005: Antes de generar la remisión, el sistema requiere la autorización del ingeniero/comercial (verificación de contrato firmado + disponibilidad de obra)
- Añadir AC-006: La remisión puede vincularse a múltiples clientes/frentes cuando el equipo es de un subcontratista y el contratante

---

### 11. `checklist-validado.md` — Checklist Validado

**Añadir al módulo de Inventarios:**
```markdown
- [ ] Pedidos parciales: estado Pendiente / Parcial / Completo por pedido
- [ ] Inicio del alquiler: desde la fecha en que el pedido queda completo (no desde el primer parcial)
- [ ] Autorización del ingeniero antes del despacho (contrato, fecha de obra, disponibilidad)
- [ ] Cronograma diario Recepción → Almacén (Viviana → Angie), con reporte de retorno
- [ ] Inspección de devolución con 3 fuentes: conductor + despachador + fotos portería
- [ ] Clasificación ampliada: OK · Dañado · **Mantenimiento** · Faltante · **Ajeno**
  - Mantenimiento: G&H asume costo; no cobra al cliente
  - Ajeno: devolver a empresa correspondiente
- [ ] Cruce de inventario entre frentes del mismo cliente (préstamo de equipo entre frentes)
- [ ] Inventario muestra saldos negativos reales (no convierte a positivo)
- [ ] Política de cancelación de pedidos (documentada con el ingeniero)
- [ ] Separación de códigos de producto: alquiler ≠ venta
- [ ] Catálogos como fuente de verdad (no hay inventario estandarizado real aún)
```

**Añadir al módulo de Facturación:**
```markdown
- [ ] Modalidades de facturación: por remisión · consolidada · por valor
- [ ] Centros de costo automáticos: 13 Alquiler · 14 Ventas/Reposiciones
- [ ] Retenciones por tipo de concepto automáticas (transporte ≠ alquiler; no mezclar en una sola factura)
- [ ] Catálogos duales: general anual + especial por cliente
- [ ] Precio de transporte: por peso Y volumen (no solo toneladas)
- [ ] Validación de envío: CUFE + Radian (DIAN) como prueba oficial
- [ ] Distinción de clientes por tipo de dominio: corporativo (triple check DIAN) vs. público (seguimiento telefónico)
- [ ] Permiso de editar datos de cliente para Contabilidad/Facturación (caso fiducia vs. consorcio)
- [ ] Una remisión puede descontarse de múltiples clientes/frentes
- [ ] Informes por equipo (rentabilidad, historial de alquiler, mantenimiento, reposiciones)
- [ ] Facturación solo genera y valida envío a DIAN; Cartera gestiona el cobro
- [ ] Cortes de facturación: principalmente mensual, por obra y por línea de producto
```

**Añadir nuevos roles al checklist de Configuración:**
```markdown
- [ ] Rol Despachador: conteo físico de equipos en bodega, clasificación de devoluciones
- [ ] Rol Recepción: cronograma diario de recogidas y cortes
```

---

### 12. `database/gyh_schema.dbml` — Schema de Base de Datos

**Tablas a añadir/modificar:**

#### a) Tabla `pedidos` (nueva)
```dbml
Table pedidos {
  id             uuid          [pk]
  orden_compra_id uuid         [ref: > ordenes_compra.id, not null]
  obra_id        uuid          [ref: > obras.id, not null]
  frente_id      uuid          [ref: > frentes.id]
  estado         varchar(20)   [note: 'pendiente | parcial | completo | cancelado']
  fecha_pedido   date          [not null]
  autorizado_por uuid          [ref: > usuarios.id, note: 'Ingeniero/Comercial que autoriza']
  fecha_autorizacion timestamp
  motivo_cancelacion text
  cancelado_por  uuid          [ref: > usuarios.id]
  fecha_alquiler_inicio date   [note: 'Se establece cuando estado = completo']
  created_at     timestamp     [not null]
}
```

#### b) Tabla `pedido_items` (nueva)
```dbml
Table pedido_items {
  id             uuid     [pk]
  pedido_id      uuid     [ref: > pedidos.id, not null]
  catalogo_id    uuid     [ref: > catalogo.id, not null]
  cantidad_pedida int     [not null]
  cantidad_enviada int    [not null, default: 0]
  cantidad_pendiente int  [note: 'calculada: pedida - enviada']
}
```

#### c) Tabla `remisiones` (modificar — añadir campos)
Añadir:
```dbml
  pedido_id        uuid     [ref: > pedidos.id]
  es_parcial       boolean  [default: false]
  formato_conductor text    [note: 'Registro del conductor en devolución']
  formato_despachador text  [note: 'Conteo del despachador en bodega']
  fotos_porteria   text[]   [note: 'URLs de fotos de portería de obra']
  cruce_ajuste     text     [note: 'Justificación de ajuste por préstamo entre frentes']
```

#### d) Tabla `remision_items` (modificar — añadir estados)
Cambiar el enum de estado de equipo devuelto de 3 a 5 valores:
```dbml
Enum estado_equipo {
  ok            [note: 'Buen estado']
  danado        [note: 'Dañado, genera novedad']
  mantenimiento [note: 'Reparable, G&H asume costo, no se factura']
  faltante      [note: 'No retornó, genera reposición']
  ajeno         [note: 'No pertenece a G&H, devolver']
}
```

#### e) Tabla `catalogo` (modificar)
Añadir:
```dbml
  centro_costo   varchar(5)  [note: '13=alquiler, 14=venta/reposicion']
  unidad_negocio varchar(50) [note: 'formaleta_metalica|multidireccional|transporte|formaleta_plastica|formaleta_tradicional']
  codigo_tipo    varchar(10) [note: 'alquiler|venta']
  precio_transporte_calculo varchar(20) [note: 'toneladas|peso_volumen']
```

#### f) Tabla `catalogo_precios_cliente` (nueva)
```dbml
Table catalogo_precios_cliente {
  id              uuid     [pk]
  cliente_id      uuid     [ref: > clientes.id, not null]
  catalogo_id     uuid     [ref: > catalogo.id, not null]
  precio_alquiler decimal(12,2)
  precio_venta    decimal(12,2)
  precio_reposicion decimal(12,2)
  vigente_desde   date     [not null]
  vigente_hasta   date
  nota            text     [note: 'Acuerdo comercial, por escrito']
  registrado_por  uuid     [ref: > usuarios.id]
  created_at      timestamp [not null]
}
```

#### g) Tabla `clientes` (modificar)
Añadir:
```dbml
  nombre_facturacion   varchar(200) [note: 'Nombre para factura (puede ser fiducia)']
  tipo_dominio_correo  varchar(20)  [note: 'corporativo|publico']
  tiene_sistema_contable boolean    [default: false]
```

#### h) Tabla `facturas` (modificar)
Añadir:
```dbml
  modalidad_factura varchar(20) [note: 'por_remision|consolidada|por_valor']
  centro_costo      varchar(5)  [note: '13=alquiler, 14=venta']
  cufe              varchar(100) [note: 'Código Único de Factura Electrónica']
  estado_radian     varchar(30)  [note: 'enviada|aceptada|rechazada_dian|sin_confirmar']
  fecha_cufe        timestamp
```

#### i) Tabla `retenciones_config` (nueva)
```dbml
Table retenciones_config {
  id              uuid     [pk]
  tipo_concepto   varchar(30) [note: 'alquiler|transporte|venta|reposicion']
  nombre_retencion varchar(30) [note: 'rte_fuente|rte_ica|iva']
  porcentaje      decimal(5,2) [not null]
  vigente_desde   date     [not null]
  vigente_hasta   date
  created_by      uuid     [ref: > usuarios.id]
}
```

#### j) Tabla `cronograma_recogidas` (nueva)
```dbml
Table cronograma_recogidas {
  id              uuid     [pk]
  fecha           date     [not null]
  obra_id         uuid     [ref: > obras.id, not null]
  cliente_id      uuid     [ref: > clientes.id, not null]
  numero_corte    varchar(30)
  estado          varchar(20) [note: 'programada|parcial|completada|sin_recoger']
  registrado_por  uuid     [ref: > usuarios.id, note: 'Viviana - Recepción']
  updated_at      timestamp
}
```

#### k) Tabla `equipos_ajenos` (nueva)
```dbml
Table equipos_ajenos {
  id              uuid     [pk]
  remision_id     uuid     [ref: > remisiones.id]
  descripcion     text     [not null]
  empresa_origen  varchar(200)
  fecha_recepcion date     [not null]
  estado          varchar(20) [note: 'en_bodega|devuelto']
  fecha_devolucion date
  devuelto_a      varchar(200)
}
```

---

### 13. `generate_report.py` — Script de Generación

**Sin cambios en la lógica.** Solo actualizar en la constante `OVERVIEW` el bloque de texto descriptivo:

**En las chips del hero**, actualizar:
- Cambiar `'🆕 Feedback 24-jun aplicado'` → `'🆕 SEM-27 · Entrevistas aplicadas'`
- Actualizar la fecha de la sesión al 2026-07-04

**En `OVERVIEW`**, actualizar el callout de ajustes:
```python
# Línea ~386 — actualizar el texto del callout
<strong>🆕 Ajustes SEM-27 (Entrevistas Facturación e Inventario):</strong>
Pedidos parciales con inicio de alquiler al completar ·
Centros de costo automáticos (13/14) ·
Retenciones por tipo de concepto (transporte ≠ alquiler) ·
Catálogos duales (general + especial por cliente) ·
Precio transporte por peso Y volumen ·
Validación CUFE + Radian DIAN ·
Rol Despachador y Recepción ·
Cruce de inventario entre frentes ·
Modalidades de factura · US-015 a US-023 añadidas
```

**En `roles_section`**, actualizar la etiqueta de 8 a 10 roles:
```python
# Línea ~222
p class="section-sub">10 roles · CEO/Ingeniero · Admin · Comercial · Dibujante · Contabilidad · Jurídica · Almacén · Conductor · Despachador · Recepción
```

**En `db_section`**, el callout ya es dinámico con `len(tables)`, no necesita cambio.

---

## Orden de ejecución recomendado

```
1. database/gyh_schema.dbml           → Base de todo
2. architecture/06_roles_y_permisos_tabla.md
3. architecture/06_roles_y_permisos.mmd
4. architecture/01_flujo_principal_gyh.mmd
5. architecture/02_arquitectura_sistema.mmd
6. architecture/03_modulo_cotizacion.mmd
7. architecture/04_registro_aprobacion_cliente.mmd
8. architecture/05_modulo_inventarios_logistica.mmd  ← más cambios
9. sitemaps/sitemap_05_inventarios.mmd
10. sitemaps/sitemap_06_facturacion.mmd
11. user-stories/historias_usuario.md              ← 9 US nuevas + 4 actualizadas
12. checklist-validado.md
13. generate_report.py                             ← solo textos OVERVIEW
14. python3 generate_report.py                     ← prueba final
```

---

## Archivos NO modificados (no hay cambios requeridos)
- `sitemaps/sitemap_01_auth_dashboard.mmd`
- `sitemaps/sitemap_02_clientes.mmd`
- `sitemaps/sitemap_03_cotizaciones.mmd`
- `sitemaps/sitemap_04_contratos.mmd`
- `sitemaps/sitemap_07_auditoria_config.mmd`

Estos sitemaps no recibieron información nueva en las entrevistas.

---

## Criterios de verificación post-aplicación

| Verificación | Cómo |
|---|---|
| El script genera HTML sin errores | `python3 generate_report.py` → sin traceback |
| Los diagramas .mmd son válidos | Pegar en mermaid.live; todos deben renderizar |
| Los 10 roles aparecen en la tabla | Ver sección Roles en el HTML generado |
| Las 23 historias de usuario aparecen | Ver sección Historias en el HTML |
| Los nuevos estados de equipo devuelto aparecen (5) | Buscar "Mantenimiento" y "Ajeno" en el HTML |
| Catálogos duales visibles en el flujo de cotización | Ver diagrama 03 en el HTML |
| Pedidos parciales visibles en inventario | Ver diagrama 05 en el HTML |
| CUFE/Radian visible en facturación | Ver diagrama 01 y sitemap 06 en el HTML |
