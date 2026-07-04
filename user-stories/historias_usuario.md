# Historias de Usuario — G&H Sistema de Gestión
**G&H Obras y Estructuras Metálicas S.A.S**
Versión 1.1 — SEM-27 (2026-07-04)

---

## Roles del Sistema

| Rol | Descripción |
|-----|-------------|
| **SuperAdmin** | Configuración global del sistema, reglas de negocio, parámetros de trayecto |
| **Admin** | Administra usuarios, catálogo y configuración del sistema |
| **Comercial** | Gestiona prospectos, cotizaciones y relación con el cliente; autoriza despachos |
| **Dibujante** | Realiza modelamiento técnico y genera cotizaciones de materiales |
| **Contabilidad** | Valida viabilidad financiera y gestiona cartera |
| **Facturación** | Genera facturas, gestiona CUFE/DIAN, aplica centros de costo y retenciones |
| **Jurídica** | Valida documentación legal, listas LAFT y contratos |
| **Almacén** | Gestiona inventario, remisiones y agenda de transporte |
| **Despachador** | Verifica y carga equipos en bodega; clasifica estado de devoluciones |
| **Conductor** | Ejecuta transporte de equipos a obras |
| **Recepción** | Genera el cronograma diario de recogidas y cortes |

---

## Módulo 1 — Cotizaciones

### US-001 · Creación de cotización técnica por dibujante
**Como** Dibujante  
**Quiero** cargar los planos del cliente (DWG/DXF/PDF) y generar el desglose de materiales en el sistema  
**Para** reducir el tiempo de modelamiento actual de 4-6 horas en AutoCAD

**Criterios de Aceptación**
- [ ] AC-001: El sistema permite subir archivos en formatos DWG, DXF, PDF y XLSX.
- [ ] AC-002: Se puede asociar la cotización a un cliente, obra y frente de obra específicos.
- [ ] AC-003: El dibujante puede importar el Excel de materiales exportado desde AutoCAD.
- [ ] AC-004: El sistema consulta el catálogo oficial y asigna precios automáticamente a cada ítem importado.
- [ ] AC-005: Se registra el tiempo de modelamiento (horas empleadas) como métrica del sistema.
- [ ] AC-006: La cotización queda en estado "Borrador" hasta que el Comercial la revise.
- [ ] AC-007: El sistema diferencia la línea de negocio: Formaleta Metálica (Excel FM), Formaleta FP/FT (Excel separado), Multidireccional, Transporte u Otros.

---

### US-002 · Completar cotización con valores comerciales
**Como** Comercial  
**Quiero** recibir la cotización técnica del dibujante y agregarle los valores comerciales, descuentos e IVA  
**Para** generar el PDF final que se envía al cliente

**Criterios de Aceptación**
- [ ] AC-001: El Comercial puede seleccionar los tipos de negocio aplicables: Venta, Alquiler, Transporte y/o Reposición.
- [ ] AC-002: Para ítems de transporte, el precio se calcula por peso Y volumen (el que resulte mayor determina la tarifa, no solo tonelaje).
- [ ] AC-003: Se pueden agregar accesorios y servicios adicionales a la cotización.
- [ ] AC-004: El sistema calcula automáticamente subtotales, IVA y total.
- [ ] AC-005: Para ítems que aplican, el sistema soporta cálculo de precios por metro cuadrado ($/m²).
- [ ] AC-006: El PDF generado incluye logo, datos de G&H, cliente, obra, ítems y totales con retenciones.
- [ ] AC-007: El PDF puede enviarse directamente al cliente desde el sistema.
- [ ] AC-008: Si se aplican precios especiales, el sistema genera una notificación obligatoria por escrito a Facturación.

---

### US-003 · Consulta de catálogos de precios
**Como** Dibujante o Comercial  
**Quiero** consultar el catálogo oficial de productos con precios vigentes  
**Para** asignar valores correctos a cada ítem sin depender de documentos físicos o Excel externos

**Criterios de Aceptación**
- [ ] AC-001: El catálogo muestra código, nombre, descripción, precio de venta, precio de alquiler/día y precio de reposición.
- [ ] AC-002: El catálogo indica si el producto aplica precio por m².
- [ ] AC-003: Cada producto tiene un código de revisión para trazabilidad de cambios de precio.
- [ ] AC-004: Solo el Admin puede crear, editar o desactivar productos del catálogo.
- [ ] AC-005: El sistema distingue entre el catálogo general anual (actualizado por Recepción) y catálogos especiales por cliente (acordados por Comercial).
- [ ] AC-006: Los ítems de transporte muestran el parámetro de cálculo: por peso, por volumen o el mayor de los dos.

---

## Módulo 2 — Registro y Aprobación de Clientes

### US-004 · Diligenciar formulario único de registro de cliente
**Como** Comercial  
**Quiero** completar el formulario FT-AC-001 digitalmente en el sistema  
**Para** reemplazar el proceso manual en Excel y estandarizar la captura de datos

**Criterios de Aceptación**
- [ ] AC-001: El formulario cubre las 9 secciones del FT-AC-001 v2.0: Info General, Contacto, Referencias Bancarias, Referencias Comerciales, Tributaria, Contable, Socios/Accionistas, Información de Obra y Autorización Centrales de Riesgo.
- [ ] AC-002: Se puede adjuntar: RUT, Cámara de Comercio, Cédula del Representante Legal, Estados Financieros, Autorización de Centrales de Riesgo y Carta de Presentación.
- [ ] AC-003: Los campos obligatorios se validan antes de pasar al proceso de aprobación.
- [ ] AC-004: El formulario genera automáticamente un código de revisión único por cliente.
- [ ] AC-005: Se registra la ciudad de la sucursal asociada (Bogotá, Ibagué o Armenia).
- [ ] AC-006: En la sección VI se registra el tipo de dominio del correo del cliente (corporativo o público) para determinar la estrategia de seguimiento en Cartera y el triple check en DIAN.

---

### US-005 · Dar concepto de aprobación de cliente
**Como** Contabilidad, Jurídica o Comercial  
**Quiero** revisar la información del cliente y registrar mi concepto (Favorable / No Favorable) con comentarios  
**Para** cumplir el proceso de validación multi-área y permitir o bloquear el avance al contrato

**Criterios de Aceptación**
- [ ] AC-001: Cada área visualiza la información del cliente y los documentos adjuntos antes de dar concepto.
- [ ] AC-002: El campo de comentario es obligatorio — no se puede guardar el concepto sin justificarlo.
- [ ] AC-003: Los tres conceptos son independientes y pueden darse simultáneamente.
- [ ] AC-004: El sistema solo permite avanzar a Orden de Compra cuando los 3 conceptos son "Favorable".
- [ ] AC-005: Si algún área da concepto "No Favorable", el cliente pasa a estado "Rechazado" y se notifica al equipo Comercial con los motivos.
- [ ] AC-006: El sistema envía notificación automática a las áreas con conceptos pendientes para agilizar el proceso.
- [ ] AC-007: El CEO/Ingeniero puede forzar la aprobación desde su perfil bajo su responsabilidad, aunque haya conceptos no favorables.

---

### US-006 · Ver historial de aprobaciones y anotaciones
**Como** cualquier usuario con acceso al módulo de clientes  
**Quiero** ver el historial de conceptos y comentarios de todas las áreas  
**Para** tener trazabilidad del proceso de aprobación de cada cliente

**Criterios de Aceptación**
- [ ] AC-001: Se muestra quién dio el concepto, cuándo y cuál fue la decisión.
- [ ] AC-002: Los comentarios de cada área son visibles para todos los roles autorizados.
- [ ] AC-003: El historial es de solo lectura — no se puede modificar un concepto ya dado.

---

## Módulo 3 — Contratos y Firma Electrónica

### US-007 · Gestionar contratos para clientes nuevos y existentes
**Como** Comercial  
**Quiero** gestionar la creación o asociación de contratos tanto para clientes nuevos como existentes  
**Para** activar operaciones sin requerir pasos innecesarios para clientes con relación establecida

**Criterios de Aceptación**
- [ ] AC-001: La Orden de Compra se genera para clientes nuevos (a partir de cotización aprobada) y para clientes existentes con nuevos pedidos.
- [ ] AC-002: Para clientes con **contrato interno existente** (ya tienen contrato vigente con G&H), se puede activar operaciones directamente sin pasar por firma electrónica.
- [ ] AC-003: Para clientes externos o primer contrato, el sistema envía a firma mediante Ooku.
- [ ] AC-004: El campo `tipo_origen_contrato` define el flujo: `interno` (activación directa) o `externo` (requiere firma Ooku).
- [ ] AC-005: Al confirmar la firma (contratos externos), el estado cambia automáticamente a "Firmado" y activa el módulo de Almacén.
- [ ] AC-006: Se envía notificación al cliente y al equipo Comercial cuando el contrato externo está pendiente de firma.

---

## Módulo 4 — Almacén / Pedidos y Logística

### US-008 · Gestionar pedidos parciales y control de despacho
**Como** Jefe de Almacén  
**Quiero** crear pedidos y registrar envíos parciales hasta completar el pedido  
**Para** controlar cuándo inicia el contador de días de alquiler y cuánto queda pendiente por despachar

**Criterios de Aceptación**
- [ ] AC-001: Un pedido puede despacharse en múltiples viajes; el sistema acumula remisiones parciales.
- [ ] AC-002: El contador de días de alquiler inicia únicamente cuando el pedido está marcado como "Completo".
- [ ] AC-003: El sistema muestra en todo momento qué cantidades han sido enviadas y qué queda pendiente.
- [ ] AC-004: El Ingeniero o Comercial debe autorizar el despacho verificando: contrato firmado, fecha libre en obra y pedido listo.
- [ ] AC-005: Si la obra cancela el pedido, el motivo queda registrado y se notifica a Ingeniería.
- [ ] AC-006: La remisión de salida incluye: pedido, frente de obra, cantidades, conductor, vehículo, placa y dirección de destino.
- [ ] AC-007: Al confirmar la remisión, el Kardex descuenta automáticamente el stock de cada producto.

---

### US-009 · Programar agenda de transporte y gestión de conductores
**Como** Jefe de Almacén  
**Quiero** programar la agenda de conductores y gestionar su disponibilidad  
**Para** coordinar eficientemente la logística de equipos entre bodega y obras

**Criterios de Aceptación**
- [ ] AC-001: La agenda muestra un calendario interactivo con los despachos y recogidas programadas.
- [ ] AC-002: Se puede asignar conductor, vehículo, hora de inicio, hora de fin y dirección a cada viaje.
- [ ] AC-003: El sistema permite registrar períodos de indisponibilidad de conductores (mantenimiento, reposición de equipos, u otro motivo), con fechas desde/hasta.
- [ ] AC-004: El sistema calcula la distancia y trayecto entre punto de recogida y punto de entrega (integración con API de mapas), aplicando la regla configurable de valor por km, combustible y capacidad de carga (peso + volumen).
- [ ] AC-005: El sistema genera alertas automáticas de próximas recogidas para equipos en alquiler.
- [ ] AC-006: El conductor puede ver su agenda asignada desde su perfil.

---

### US-010 · Registrar devolución con verificación de 3 fuentes y clasificar estado de equipos
**Como** Jefe de Almacén o Despachador  
**Quiero** registrar el retorno de equipos con verificación cruzada de 3 fuentes y clasificar el estado de cada equipo  
**Para** actualizar el Kardex, calcular días de alquiler y gestionar las novedades correctamente

**Criterios de Aceptación**
- [ ] AC-001: La remisión de entrada se vincula a la remisión de salida y al pedido original.
- [ ] AC-002: La verificación cruza 3 fuentes: formato del conductor, conteo físico del despachador y fotos de portería de la obra.
- [ ] AC-003: Cuando las cantidades no cuadran, el sistema permite acción de ajuste cruzando frentes o sucursales del mismo cliente (equipos prestados entre frentes).
- [ ] AC-004: Cada equipo se puede clasificar en 5 estados: OK / Dañado / Mantenimiento / Faltante / Ajeno.
- [ ] AC-005: Equipos en estado "Mantenimiento" quedan en bodega pendiente de reparación; G&H asume el costo (no se factura al cliente).
- [ ] AC-006: Equipos en estado "Faltante" generan automáticamente un ítem de Reposición en la factura (cobro al cliente según catálogo).
- [ ] AC-007: Equipos en estado "Ajeno" (no son de G&H) se registran en el módulo de Equipos Ajenos para ser devueltos a la empresa correspondiente.
- [ ] AC-008: Los días de alquiler se calculan desde la fecha en que el pedido quedó "Completo" hasta la fecha de entrada.
- [ ] AC-009: El Kardex se actualiza al confirmar la recepción, reflejando saldos negativos si hay descuadres.

---

### US-015 · Cronograma diario de recogidas y cortes
**Como** Recepción (Viviana)  
**Quiero** crear y publicar el cronograma diario de recogidas y cortes  
**Para** que Almacén ejecute las recogidas y reporte el resultado al final del día

**Criterios de Aceptación**
- [ ] AC-001: Recepción crea el cronograma con: obra, cliente, número de corte y fecha de recogida.
- [ ] AC-002: El cronograma es visible para Almacén desde la sección de agenda.
- [ ] AC-003: Al finalizar el día, Almacén reporta qué recogidas se realizaron vs. las programadas.
- [ ] AC-004: El sistema notifica automáticamente a Recepción cuando Almacén actualiza el estado de las recogidas.

---

### US-016 · Registrar y gestionar equipo ajeno
**Como** Almacén o Despachador  
**Quiero** registrar equipos que no pertenecen a G&H y llegan en devoluciones  
**Para** devolverlos a la empresa propietaria y mantener el Kardex limpio

**Criterios de Aceptación**
- [ ] AC-001: Al clasificar un equipo como "Ajeno", se abre el formulario de equipo ajeno (descripción, empresa propietaria, fecha de recepción).
- [ ] AC-002: La lista de equipos ajenos muestra estado: "En Bodega" o "Devuelto".
- [ ] AC-003: Al devolver el equipo, se registra la fecha y a quién se entregó.
- [ ] AC-004: El sistema no incluye el equipo ajeno en el Kardex de G&H.

---

## Módulo 5 — Facturación

### US-011 · Generar proforma, factura y enviar a Siigo/DIAN
**Como** Facturación  
**Quiero** generar la proforma para el cliente, la factura oficial y enviarla a Siigo que la transmite a la DIAN  
**Para** asegurar un cobro correcto con la normativa y tener evidencia oficial de envío

**Criterios de Aceptación**
- [ ] AC-001: Antes de emitir la factura, el sistema genera una Proforma que especifica al cliente qué se le va a cobrar — el cliente puede aprobar o solicitar ajuste.
- [ ] AC-002: El sistema verifica las condiciones de pago del cliente antes del ciclo: días de tramitación específicos y ciclo de cobro (mes vencido es el default).
- [ ] AC-003: La factura se genera a partir de los ítems aprobados en la proforma.
- [ ] AC-004: Para alquiler, los días se calculan desde la fecha en que el pedido quedó **completo** (no desde la primera remisión parcial).
- [ ] AC-005: Para productos aplicables, el sistema calcula el cobro por metro cuadrado ($/m²).
- [ ] AC-006: La factura aplica retenciones según tipo de concepto — IVA, Rte. Fuente, ReteICA, ReteTransporte según corresponda; alquiler ≠ transporte ≠ venta.
- [ ] AC-007: El sistema aplica automáticamente el centro de costo: 13 (alquileres) · 14 (ventas/reposiciones). Transporte siempre en factura separada.
- [ ] AC-008: No se mezclan conceptos de diferente centro de costo en una misma factura (Siigo rechazaría el envío).
- [ ] AC-009: La factura se envía a **Siigo**, que la transmite a la DIAN. **No hay conexión directa** con la DIAN desde el sistema.
- [ ] AC-010: El estado de Siigo puede ser incorrecto — Facturación debe **validar manualmente en el portal DIAN** el estado real de la factura.
- [ ] AC-011: Facturación registra el seguimiento telefónico al cliente para confirmar que recibió y procesó la factura.
- [ ] AC-012: El CUFE queda disponible como evidencia oficial de envío (útil cuando el cliente alega no haber recibido la factura).

---

### US-017 · Configurar modalidad de facturación por cliente
**Como** Facturación  
**Quiero** configurar para cada cliente cómo prefiere recibir las facturas  
**Para** cumplir con sus preferencias y reducir devoluciones o discrepancias

**Criterios de Aceptación**
- [ ] AC-001: Las modalidades disponibles son: Por Remisión (una factura por cada remisión/contratista), Consolidada (todo el período), Por Valor ("lo que quepa").
- [ ] AC-002: El transporte siempre se factura por separado, independiente de la modalidad seleccionada.
- [ ] AC-003: La configuración de modalidad se guarda a nivel de cliente y se aplica automáticamente en cada nuevo corte.
- [ ] AC-004: Se puede modificar la modalidad para un corte específico sin cambiar la configuración general.

---

### US-018 · Gestionar cortes mensuales por cliente
**Como** Facturación  
**Quiero** ver todos los pedidos y ítems facturables de un cliente en un período  
**Para** generar los cortes mensuales correctamente según la modalidad configurada

**Criterios de Aceptación**
- [ ] AC-001: El sistema agrupa todos los pedidos activos de un cliente en el período seleccionado.
- [ ] AC-002: Se muestra qué pedidos están completos (con alquiler iniciado) y cuáles están en proceso.
- [ ] AC-003: El sistema aplica la modalidad configurada para el cliente al generar el corte.
- [ ] AC-004: Si hay precios especiales vigentes, el sistema los usa automáticamente en la liquidación.

---

### US-019 · Gestionar flujo Siigo → DIAN y seguimiento de factura
**Como** Facturación  
**Quiero** enviar la factura a Siigo, validar su transmisión a la DIAN y hacer seguimiento con el cliente  
**Para** tener evidencia oficial de envío y confirmar que el cliente procesó el cobro

**Criterios de Aceptación**
- [ ] AC-001: La factura se envía desde el sistema a **Siigo** (no a la DIAN directamente).
- [ ] AC-002: Siigo transmite a la DIAN y genera el CUFE — el sistema registra la fecha y hora del envío a Siigo.
- [ ] AC-003: Facturación valida el estado en el **portal de la DIAN** directamente (el estado en Siigo puede ser incorrecto y no es confiable como fuente de verdad).
- [ ] AC-004: Los estados posibles en Radian (DIAN): Sin enviar · Enviada (CUFE generado) · Aceptada (triple check) · Rechazada (revisar errores) · Sin confirmar (dominio público).
- [ ] AC-005: Facturación registra el seguimiento telefónico al cliente confirmando que recibió y procesó la factura.
- [ ] AC-006: Si el cliente tiene dominio público (Gmail, Hotmail), nunca dará el triple check automático — Cartera hace la gestión telefónica.
- [ ] AC-007: El CUFE queda disponible como evidencia cuando el cliente alega no haber recibido la factura.

---

### US-012 · Gestionar cartera de clientes en mora
**Como** Facturación o Jurídica  
**Quiero** ver las facturas vencidas, registrar gestiones de cobro y hacer seguimiento  
**Para** reducir la cartera y coordinar cobros jurídicos cuando sea necesario

**Criterios de Aceptación**
- [ ] AC-001: La vista de cartera muestra cliente, factura, días en mora y monto pendiente.
- [ ] AC-002: Se pueden registrar notas de gestión: contactos realizados, acuerdos de pago, etc.
- [ ] AC-003: El sistema genera alertas automáticas para facturas que superan los días de plazo acordados.
- [ ] AC-004: La cartera tiene estados: Nueva, En Gestión, Acuerdo de Pago, Demanda, Castigada, Recuperada.
- [ ] AC-005: Si el cliente tiene dominio de correo público (Gmail/Hotmail/Yahoo), el sistema indica que se debe hacer seguimiento telefónico (el cliente nunca dará el triple check en DIAN).
- [ ] AC-006: Si el cliente alega no haber recibido la factura, el sistema muestra el CUFE como evidencia del envío oficial.
- [ ] AC-007: El módulo de Cartera funciona completamente independiente de Facturación — tiene su propia vista y flujo de trabajo.

---

### US-020 · Editar datos de cliente para facturación (caso fiducia/consorcio)
**Como** Facturación  
**Quiero** poder editar los datos del cliente que aparecen en la factura cuando el pagador difiere del contratante  
**Para** emitir la factura al nombre correcto (ej: fiducia paga pero el contrato es con el consorcio Bronz)

**Criterios de Aceptación**
- [ ] AC-001: Facturación puede editar el nombre de facturación sin modificar el registro oficial del cliente.
- [ ] AC-002: El nombre de facturación alternativo se guarda como campo separado y se usa en las facturas del período acordado.
- [ ] AC-003: El cambio queda auditado con quién lo hizo y cuándo.

---

## Módulo 6 — Cartera (independiente)

### US-021 · Gestionar estrategia de cobro según tipo de dominio de correo
**Como** Cartera  
**Quiero** que el sistema me indique la estrategia de cobro adecuada según el correo del cliente  
**Para** no perder tiempo intentando obtener confirmaciones que nunca llegarán de clientes con correo público

**Criterios de Aceptación**
- [ ] AC-001: Para clientes con correo corporativo (sistema contable propio), el sistema muestra el estado del triple check en DIAN automáticamente.
- [ ] AC-002: Para clientes con correo público (Gmail, Hotmail, Yahoo), el sistema indica "Sin confirmar" y asigna una tarea de llamada telefónica.
- [ ] AC-003: El CUFE está disponible como evidencia en caso de disputa.

---

## Módulo 7 — Reportería

### US-022 · Generar reportes de operaciones
**Como** Admin, SuperAdmin o Comercial  
**Quiero** acceder a reportes consolidados de las operaciones del sistema  
**Para** tomar decisiones de negocio basadas en datos reales

**Criterios de Aceptación**
- [ ] AC-001: El módulo de Reportería incluye al menos: Kardex por período, Facturas emitidas vs. pagadas, Cartera por antigüedad, Rotación de equipos, Conductores y trayectos, Cotizaciones por estado.
- [ ] AC-002: Los reportes se pueden filtrar por fecha, cliente, obra, línea de negocio y sucursal.
- [ ] AC-003: Se pueden exportar en formato Excel y PDF.
- [ ] AC-004: Los datos de reportería se generan a partir de las vistas materializadas del sistema, sin afectar el rendimiento operacional.

---

## Módulo 8 — Auditoría y Notificaciones (Transversal)

### US-013 · Consultar log global de auditoría
**Como** Admin o Contabilidad  
**Quiero** consultar el registro de todas las acciones realizadas en el sistema  
**Para** tener trazabilidad completa de quién hizo qué y cuándo

**Criterios de Aceptación**
- [ ] AC-001: El log registra: usuario, acción, módulo, registro afectado, fecha/hora e IP.
- [ ] AC-002: Se puede filtrar por usuario, módulo, rango de fechas y tipo de acción.
- [ ] AC-003: El log es de solo lectura — ningún usuario puede modificar o borrar registros.
- [ ] AC-004: Los datos anteriores y nuevos de cada cambio quedan almacenados en JSON.

---

### US-014 · Recibir notificaciones de procesos pendientes
**Como** cualquier usuario del sistema  
**Quiero** recibir notificaciones cuando hay acciones que requieren mi atención  
**Para** no depender de comunicaciones manuales por WhatsApp o email para empujar los procesos

**Criterios de Aceptación**
- [ ] AC-001: Contabilidad, Jurídica y Comercial reciben alerta cuando hay una aprobación de cliente pendiente de su concepto.
- [ ] AC-002: El Almacén recibe alerta automática de próximas recogidas de equipos en alquiler.
- [ ] AC-003: El Comercial recibe alerta cuando un contrato lleva más de X días sin ser firmado.
- [ ] AC-004: Facturación recibe alerta cuando una factura está próxima a vencer o ya venció.
- [ ] AC-005: Recepción recibe alerta cuando Almacén actualiza el estado del cronograma diario.
- [ ] AC-006: Las notificaciones se muestran en el sistema y pueden enviarse por email.
- [ ] AC-007: El módulo de Notificaciones tiene una sección de configuración donde el SuperAdmin define qué eventos disparan qué alertas.

---

### US-023 · Configuración de reglas de negocio por SuperAdmin
**Como** SuperAdmin  
**Quiero** configurar los parámetros globales del sistema  
**Para** adaptar las reglas de negocio sin necesidad de cambios en el código

**Criterios de Aceptación**
- [ ] AC-001: Se pueden configurar: tarifa por km para conductores, regla de combustible, capacidad por tipo de camión (peso y volumen máximo).
- [ ] AC-002: Se pueden configurar los porcentajes de retenciones por tipo de concepto con vigencia desde/hasta.
- [ ] AC-003: Se puede activar o desactivar el módulo de confirmación de proformas por cliente.
- [ ] AC-004: Los cambios de configuración quedan auditados con quién los hizo y cuándo.

---

## Resumen de Métricas de Escala (para QA y Pruebas de Carga)

| Métrica | Valor |
|---------|-------|
| Clientes en migración inicial | ~180 (130 Bogotá, 50 Ibagué/Armenia) |
| Obras por cliente | Hasta 50 |
| Frentes por obra | 3-4 |
| Cotizaciones por dibujante/semana | 6-12 |
| Prospectos nuevos por mes | ~50 |
| Tiempo modelamiento actual (AutoCAD) | 4-6 horas |
| Documentos del checklist por cliente | ~6 tipos |
| Áreas de aprobación | 3 (Contabilidad, Jurídica, Comercial) |
| Roles del sistema | 11 |
