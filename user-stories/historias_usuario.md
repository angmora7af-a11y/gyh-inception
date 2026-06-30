# Historias de Usuario — G&H Sistema de Gestión
**G&H Obras y Estructuras Metálicas S.A.S**
Versión 1.0 — Sesión 2026-06-16

---

## Roles del Sistema

| Rol | Descripción |
|-----|-------------|
| **Comercial** | Gestiona prospectos, cotizaciones y relación con el cliente |
| **Dibujante** | Realiza modelamiento técnico y genera cotizaciones de materiales |
| **Contabilidad** | Valida viabilidad financiera, facturación y cartera |
| **Jurídica** | Valida documentación legal, listas LAFT y contratos |
| **Almacén** | Gestiona inventario, remisiones y agenda de transporte |
| **Conductor** | Ejecuta transporte de equipos a obras |
| **Admin** | Administra usuarios, catálogo y configuración del sistema |

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

---

### US-002 · Completar cotización con valores comerciales
**Como** Comercial  
**Quiero** recibir la cotización técnica del dibujante y agregarle los valores comerciales, descuentos e IVA  
**Para** generar el PDF final que se envía al cliente

**Criterios de Aceptación**
- [ ] AC-001: El Comercial puede seleccionar los tipos de negocio aplicables: Venta, Alquiler, Transporte y/o Reposición.
- [ ] AC-002: Se pueden agregar accesorios y servicios adicionales a la cotización.
- [ ] AC-003: El sistema calcula automáticamente subtotales, IVA y total.
- [ ] AC-004: Para ítems que aplican, el sistema soporta cálculo de precios por metro cuadrado ($/m²).
- [ ] AC-005: El PDF generado incluye logo, datos de G&H, cliente, obra, ítems y totales con retenciones.
- [ ] AC-006: El PDF puede enviarse directamente al cliente desde el sistema.

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

---

## Módulo 2 — Registro y Aprobación de Clientes

### US-004 · Diligenciar formulario único de registro de cliente
**Como** Comercial  
**Quiero** completar el formulario FT-AC-001 digitalmente en el sistema  
**Para** reemplazar el proceso manual en Excel y estandarizar la captura de datos

**Criterios de Aceptación**
- [ ] AC-001: El formulario cubre las 8 secciones del FT-AC-001 v2.0: Info General, Contacto, Referencias Bancarias, Referencias Comerciales, Tributaria, Contable, Socios/Accionistas e Información de Obra.
- [ ] AC-002: Se puede adjuntar: RUT, Cámara de Comercio, Cédula del Representante Legal, Estados Financieros, Autorización de Centrales de Riesgo y Carta de Presentación.
- [ ] AC-003: Los campos obligatorios se validan antes de pasar al proceso de aprobación.
- [ ] AC-004: El formulario genera automáticamente un código de revisión único por cliente.
- [ ] AC-005: Se registra la ciudad de la sucursal asociada (Bogotá, Ibagué o Armenia).

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

### US-007 · Generar y firmar contrato
**Como** Comercial  
**Quiero** generar la Orden de Compra y enviar el contrato a firma electrónica  
**Para** oficializar la relación con el cliente sin depender de procesos físicos

**Criterios de Aceptación**
- [ ] AC-001: La Orden de Compra se genera automáticamente a partir de la cotización aprobada por el cliente.
- [ ] AC-002: El sistema se integra con DocuSign u Okc para enviar el contrato a firma.
- [ ] AC-003: Se envía notificación al cliente y al equipo Comercial cuando el contrato está pendiente de firma.
- [ ] AC-004: Al confirmar la firma, el contrato cambia automáticamente a estado "Firmado".
- [ ] AC-005: El estado "Firmado" dispara automáticamente la activación del cliente en el módulo de Operaciones/Inventarios.

---

## Módulo 4 — Inventarios y Logística

### US-008 · Generar remisión de salida de equipos
**Como** Jefe de Almacén  
**Quiero** generar la remisión de salida de equipos asociada a una Orden de Compra  
**Para** actualizar el Kardex y tener control del inventario enviado a cada frente de obra

**Criterios de Aceptación**
- [ ] AC-001: La remisión se asocia a una Orden de Compra, obra y frente de obra específicos.
- [ ] AC-002: Se registran los equipos, cantidades, conductor, vehículo, placa y dirección de destino.
- [ ] AC-003: Al confirmar la remisión, el Kardex descuenta automáticamente el stock de cada producto.
- [ ] AC-004: El conductor recibe notificación con el detalle del despacho.

---

### US-009 · Programar agenda de transporte y recogidas
**Como** Jefe de Almacén  
**Quiero** programar la agenda de conductores con fechas, horarios y direcciones de entrega y recogida  
**Para** coordinar eficientemente la logística de equipos entre bodega y obras

**Criterios de Aceptación**
- [ ] AC-001: La agenda muestra un calendario interactivo con los despachos y recogidas programadas.
- [ ] AC-002: Se puede asignar conductor, vehículo, hora de inicio, hora de fin y dirección a cada viaje.
- [ ] AC-003: El sistema genera alertas automáticas de próximas recogidas para equipos en alquiler.
- [ ] AC-004: El conductor puede ver su agenda asignada desde su perfil.

---

### US-010 · Registrar devolución y calcular días de alquiler
**Como** Jefe de Almacén  
**Quiero** registrar el retorno de equipos en alquiler e inspeccionar su estado  
**Para** actualizar el Kardex, calcular los días de alquiler transcurridos y gestionar reposiciones

**Criterios de Aceptación**
- [ ] AC-001: La remisión de entrada se vincula a la remisión de salida original.
- [ ] AC-002: Se puede marcar cada equipo como: OK, Dañado o Faltante.
- [ ] AC-003: El sistema calcula automáticamente los días entre la fecha de remisión salida y la fecha de entrada.
- [ ] AC-004: Los equipos marcados como "Faltante" generan automáticamente un ítem de Reposición en la factura.
- [ ] AC-005: El Kardex se actualiza al confirmar la recepción de los equipos en buen estado.

---

## Módulo 5 — Facturación y Cartera

### US-011 · Generar factura con cálculo de m² y días de alquiler
**Como** Contabilidad  
**Quiero** generar la factura a partir de la Orden de Compra con todos los ítems, retenciones y cálculos automáticos  
**Para** asegurar un cobro correcto y ágil al cliente

**Criterios de Aceptación**
- [ ] AC-001: La factura se genera a partir de los ítems de la cotización aprobada.
- [ ] AC-002: Para productos de alquiler, el cálculo incluye automáticamente los días desde la remisión de salida hasta la entrada.
- [ ] AC-003: Para productos que aplican, el sistema calcula el cobro por metro cuadrado ($/m²).
- [ ] AC-004: La factura aplica automáticamente las retenciones del cliente: Rte. Fuente, Rte. ICA e IVA según el formulario FT-AC-001.
- [ ] AC-005: Se genera el PDF de la factura electrónica.
- [ ] AC-006: Se registra el pago del cliente y se actualiza el saldo pendiente.

---

### US-012 · Gestionar cartera de clientes en mora
**Como** Contabilidad o Jurídica  
**Quiero** ver las facturas vencidas, registrar gestiones de cobro y hacer seguimiento  
**Para** reducir la cartera y coordinar cobros jurídicos cuando sea necesario

**Criterios de Aceptación**
- [ ] AC-001: La vista de cartera muestra cliente, factura, días en mora y monto pendiente.
- [ ] AC-002: Se pueden registrar notas de gestión: contactos realizados, acuerdos de pago, etc.
- [ ] AC-003: El sistema genera alertas automáticas para facturas que superan los días de plazo acordados.
- [ ] AC-004: La cartera tiene estados: Nueva, En Gestión, Acuerdo de Pago, Demanda, Castigada, Recuperada.

---

## Módulo 6 — Auditoría y Notificaciones (Transversal)

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
- [ ] AC-004: Contabilidad recibe alerta cuando una factura está próxima a vencer o ya venció.
- [ ] AC-005: Las notificaciones se muestran en el sistema y pueden enviarse por email.

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
