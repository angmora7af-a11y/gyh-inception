# Notificaciones del Sistema — G&H Gestión

**G&H Obras y Estructuras Metálicas S.A.S**
Versión 1.0 — SEM-27 (2026-07-14)

**Canales:** Email (plataforma) · WhatsApp API (externo — cliente) · In-app (notificación en interfaz)
**Prioridad:** Alta = acción inmediata requerida · Media = informativa / recordatorio · Baja = confirmación / log

---

## Autenticación y Seguridad (2FA)

> El sistema requiere **segundo factor de autenticación (2FA)** en cada inicio de sesión. Tras ingresar usuario y contraseña, se envía un **código de seguridad de 6 dígitos al correo electrónico registrado**. El código tiene vigencia de 10 minutos. Sin validarlo, el acceso no se habilita.

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-01 | Inicio de sesión — verificación 2FA | Usuario autenticado | Email | Alta | Código OTP de 6 dígitos · Vigencia 10 min · Asunto: "Tu código de acceso G&H Sistema" |
| N-02 | Solicitud de recuperación de contraseña | Usuario solicitante | Email | Alta | Enlace seguro de restablecimiento · Vigencia 30 min |
| N-03 | Contraseña cambiada exitosamente | Usuario | Email | Media | Confirmación del cambio · Instrucciones si no fue el usuario quien lo realizó |
| N-04 | Múltiples intentos de acceso fallidos (>=5) | Admin · SuperAdmin | Email + In-app | Alta | Alerta de seguridad: usuario afectado · IP · Fecha y hora del último intento |

---

## Cotizaciones

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-05 | Cotización enviada al cliente | Cliente | Email + WhatsApp | Media | PDF adjunto con valores comerciales · Datos de contacto comercial G&H |
| N-06 | Precios especiales asignados a un cliente | Facturación | Email | Alta | Notificación obligatoria por escrito de precios acordados por Comercial · Nombre del cliente · Productos afectados |

---

## Registro y Aprobación de Clientes

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-07 | Nuevo cliente ingresado — inicia revisión multi-área | Contabilidad · Jurídica · Comercial | Email + In-app | Alta | Ficha básica del cliente · Link al formulario FT-AC-001 · Plazo sugerido de respuesta |
| N-08 | Área sin concepto registrado (recordatorio automático) | Área(s) pendiente(s) | Email + In-app | Media | Nombre del cliente · Días transcurridos · Link directo al formulario de concepto |
| N-09 | Cliente APROBADO — todos los conceptos favorables | Comercial · Todas las áreas | Email + In-app | Alta | Estado: Activo · Nombre del cliente · Puede proceder con pedido de inmediato |
| N-10 | Cliente RECHAZADO | Comercial | Email + In-app | Alta | Motivo(s) del rechazo por área · Documentación faltante o inconsistente |
| N-11 | CEO fuerza aprobación (override) | Todas las áreas · Auditoría | Email + In-app | Alta | Aprobación bajo responsabilidad del CEO/Ingeniero · Motivo y fecha registrados en auditoría |

---

## Contratos y Firma Electrónica

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-12 | Contrato generado — pendiente de firma | Cliente externo / Área interna | Email (Ooku) | Alta | Invitación de firma electrónica vía Ooku · Resumen del contrato · Fecha límite de firma |
| N-13 | Recordatorio de firma pendiente (configurable: 24h/48h) | Cliente | Email | Media | Enlace directo al documento · Datos de contacto G&H para resolver dudas |
| N-14 | Contrato firmado exitosamente | Admin · Comercial | Email + In-app | Alta | Contrato activado · Operaciones habilitadas · Link al documento firmado |

---

## Almacén, Pedidos y Logística

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-15 | Ingeniero / Comercial autoriza despacho | Despachador · Conductor asignado | Email + In-app | Alta | Detalle del pedido: equipos, destino, ruta, hora estimada de salida |
| N-16 | Conductor asignado a ruta de despacho | Conductor | Email + In-app | Alta | Cronograma del viaje: equipos, dirección, km, cliente, obra y frente |
| N-17 | Pedido completado — contador de alquiler inicia | Almacén · Facturación | In-app | Alta | Fecha de inicio de alquiler · Listado completo de equipos entregados · Obra y frente |
| N-18 | Envío parcial registrado — equipos pendientes en cola | Almacén · Comercial | In-app | Media | Equipos pendientes · Programados para siguiente viaje · Estimado de despacho |
| N-19 | Alerta de próxima recogida (configurable: N días antes) | Jefe de Almacén · Recepción | Email + In-app | Alta | Lista de equipos a recoger · Cliente, obra y frente · Fecha acordada de devolución |
| N-20 | Devolución con daño o faltante detectado en inspección | Almacén · Comercial · Facturación | Email + In-app | Alta | Equipos afectados · Estado clasificado (Dañado / Faltante) · Genera reposición automática |
| N-21 | Cancelación de pedido registrada | Ingeniería · Comercial | Email + In-app | Alta | Pedido cancelado · Motivo registrado · Equipos liberados y devueltos al stock |
| N-22 | Stock de consumible por debajo del mínimo configurado | Jefe de Almacén | Email + In-app | Media | Producto · Cantidad actual vs. mínimo · Unidad de negocio · Sugerencia de reabastecimiento |

---

## Facturación y Cartera

| ID | Evento Disparador | Destinatario | Canal | Prioridad | Descripción del Contenido |
|----|-------------------|--------------|-------|-----------|---------------------------|
| N-23 | Proforma generada para revisión del cliente | Cliente | Email + WhatsApp | Alta | Detalle de cobros (alquiler, transporte, reposiciones) · Solicita aprobación explícita antes de factura |
| N-24 | Cliente aprueba la proforma | Facturación | In-app | Alta | Autorización recibida · Proceder con generación de factura oficial |
| N-25 | Factura emitida y transmitida a Siigo / DIAN | Cliente · Comercial | Email | Alta | CUFE · Fecha de emisión · Valores · Recomendación: validar estado en portal DIAN |
| N-26 | Error en transmisión a Siigo / DIAN | Facturación · Admin | Email + In-app | Alta | Descripción del error · Acción manual requerida · Datos de la factura afectada |
| N-27 | Factura próxima a vencer (configurable: N días antes) | Cartera · Comercial | Email + In-app | Media | Cliente · Número de factura · Valor pendiente · Días para vencimiento |
| N-28 | Factura vencida — cliente en mora | Cartera · Comercial · CEO | Email + In-app | Alta | Estado mora · Días vencidos · Valor pendiente · Inicia gestión de cobro |
| N-29 | Pago registrado y confirmado | Cartera · Comercial | In-app | Baja | Referencia de pago · Monto aplicado · Factura(s) saldadas |
