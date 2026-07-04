# Checklist Validado — G&H Sistema de Gestión
**Sesión 2026-06-16 + Feedback 2026-06-24 + SEM-27 (2026-07-04)**

---

## ✅ Módulo de Clientes y Aprobación

- [x] Formulario FT-AC-001 v2.0 — 9 secciones digitalizadas en el sistema
- [x] Checklist documental: RUT, Cámara de Comercio, Cédula Rep. Legal, EEFF, Autorización Centrales de Riesgo, Carta de Presentación
- [x] Aprobación simultánea de 3 áreas: Comercial, Jurídica, Contabilidad
- [x] **Notas por especialidad obligatorias** — cada área registra justificación textual al dar concepto
- [x] **Rol CEO/Ingeniero** — perfil de consulta con acceso a motivos de rechazo detallados
- [x] **Aprobación forzada por CEO** — regla de negocio: el CEO tiene la última palabra bajo su responsabilidad
- [x] Notificación automática a todas las áreas para agilizar proceso de aprobación
- [x] **Tipo de dominio de correo del cliente** — Corporativo (triple check DIAN automático) vs. Público (Gmail/Hotmail/Yahoo → seguimiento telefónico por Cartera)
- [x] **Flujo dual de pedidos** — un pedido puede ser para un cliente nuevo (requiere aprobación) o para un cliente existente (nueva orden directamente)
- [x] **Edición de datos para facturación (caso fiducia)** — Facturación puede editar el nombre del pagador cuando difiere del contratante (ej: consorcio Bronz / fiducia)

---

## ✅ Módulo de Cotizaciones

- [x] Carga de planos en DWG, DXF, PDF desde el sistema
- [x] Importación de Excel de materiales exportado desde AutoCAD
- [x] Consulta automática del catálogo de precios y asignación de valores
- [x] **Líneas de negocio en cotización:**
  - [x] Formaleta Metálica (Excel FM — catálogo independiente)
  - [x] Formaleta FP / FT (Excel separado — catálogo independiente)
  - [x] Multidireccional
  - [x] Transporte
  - [x] Otros / Accesorios
- [x] Tipos de negocio: Venta, Alquiler, Transporte, Reposición
- [x] **Transporte calculado por peso Y volumen** — el que resulte mayor determina la tarifa (no solo tonelaje)
- [x] **Catálogo dual:**
  - [x] General anual (actualizado por Recepción, distribuido a todas las áreas)
  - [x] Especial por cliente (acordado por Comercial, notificado **por escrito** a Facturación)
- [x] Validación de retenciones: Rte. Fuente, Rte. ICA, IVA
- [x] **Retenciones diferenciadas por tipo de concepto** — transporte ≠ alquiler ≠ venta/reposición; si se mezclan, Siigo rechaza la factura
- [x] **Centros de costo: 13 (alquiler) · 14 (venta y reposición)** — transporte siempre en factura separada
- [x] Generación de PDF oficial con logo y datos completos
- [x] Envío de PDF directamente al cliente desde el sistema

---

## ✅ Módulo de Contratos

- [x] Generación de Orden de Compra a partir de cotización aprobada
- [x] **Flujo dual de contratos:**
  - [x] **Contrato interno existente** — cliente ya tiene contrato vigente con G&H → activa operaciones directamente, sin firma electrónica
  - [x] **Nuevo contrato (externo o primer contrato)** — requiere firma electrónica vía Ooku
- [x] **Firma electrónica vía Ooku** (plataforma correcta)
- [x] Seguimiento del estado del contrato (Pendiente → Firmado → Activo)
- [x] Activación automática de operaciones al completar la firma (contratos externos)

---

## ✅ Módulo de Almacén (antes: Inventarios y Logística)

- [x] Kardex con remisiones de salida y entrada
- [x] **Stock total (Momento Cero): Bodega + Equipos en Clientes + Equipos en Producción**
- [x] **Sin inventario físico estandarizado** — el sistema trabaja con catálogos; saldos negativos visibles cuando hay descuadres
- [x] **Pedidos con control de parciales:**
  - [x] Un pedido puede despacharse en múltiples viajes
  - [x] El contador de días de alquiler inicia solo cuando el pedido está **completo**
  - [x] El sistema muestra cantidades enviadas vs. pendientes en tiempo real
- [x] **Autorización de despacho por Ingeniero/Comercial** — verificar: contrato firmado, fecha libre en obra, pedido listo
- [x] **Cancelación de pedidos** — motivo registrado, notificación a Ingeniería
- [x] **Verificación de 3 fuentes en devoluciones:**
  - [x] Formato del conductor (lo que dice haber traído)
  - [x] Conteo físico del Despachador en bodega
  - [x] Fotos de portería de la obra (evidencia de salida)
- [x] **Inspección previa a facturación** — se realiza antes de pasar a Facturación: equipo OK · Mantenimiento (G&H asume) · Baja (dar de baja)
- [x] **6 estados de inspección de equipos devueltos:**
  - [x] OK — Kardex restaurado
  - [x] Dañado — novedad + presupuesto reparación
  - [x] **Baja** — equipo dado de baja definitivamente (destrucción irreparable); se registra internamente, no genera reposición
  - [x] Mantenimiento — G&H asume el costo (no se factura al cliente)
  - [x] Faltante — genera ítem de Reposición (cobro al cliente)
  - [x] Ajeno — no es de G&H, se registra y devuelve a empresa correspondiente
- [x] **Préstamo entre frentes** — acción de ajuste cruzando frentes o sucursales del mismo cliente cuando las cantidades no cuadran
- [x] **Cronograma diario de Recepción** — Viviana crea el cronograma (obra, cliente, N° corte, fecha); Almacén reporta realizadas vs. programadas
- [x] **Registro de equipo ajeno** — lista con estado y seguimiento hasta devolución
- [x] **Gestión de conductores:**
  - [x] Registro de indisponibilidad (mantenimiento, reposición de equipos, otro) con fechas desde/hasta
  - [x] Cálculo de trayecto: punto recogida → destino en km (regla configurable de tarifa/km)
  - [x] Regla configurable: combustible + peso y volumen máximo por camión
- [x] Agenda de transporte: conductor, vehículo, placa, hora, dirección
- [x] Cálculo de días de alquiler: **fecha pedido completo** → fecha remisión entrada
- [x] Reposición automática por faltante (cobro al cliente)
- [x] **Alertas proactivas de recogidas pendientes** — triggers para optimizar rutas de transporte
- [x] **Registro de fecha y hora en todas las transacciones** (campos globales)
- [ ] *(Fase 3)* Evidencias de entrega: firma digital + fotografías por conductores

---

## ✅ Módulo de Facturación

- [x] **Proveedor de transporte configurable:** G&H lo pone y cobra flete (por peso Y volumen), o el cliente lo pone (no se cobra flete)
- [x] **Condiciones de pago por cliente:**
  - [x] Días de tramitación específicos del cliente (ej: solo paga los martes)
  - [x] Ciclo de cobro: mes vencido (default) · quincenal · al cierre de obra
  - [x] Notas especiales de facturación por cliente (portal, contacto, horarios)
- [x] **Proforma antes de factura** — se especifica al cliente qué se le va a cobrar antes de emitir la factura oficial
- [x] **Modalidad de factura configurable por cliente:**
  - [x] Por remisión (una factura por contratista)
  - [x] Consolidada (todo el período en una sola factura)
  - [x] Por valor ("lo que quepa" — el usuario define el monto)
  - [x] Transporte siempre en factura separada
- [x] **Cortes mensuales por cliente** — el sistema agrupa todos los pedidos del período según la modalidad configurada
- [x] Generación de factura con cálculo de m² y días de alquiler (desde pedido completo)
- [x] **Centros de costo automáticos: 13 (alquiler) · 14 (venta y reposición)** — no se mezclan en una misma factura
- [x] Retenciones por tipo de concepto: distintas para alquiler, transporte, venta/reposición
- [x] **Integración Siigo → DIAN (no directa):**
  - [x] La factura se envía a Siigo; Siigo transmite a la DIAN
  - [x] El estado de Siigo puede ser incorrecto — Facturación valida en el portal DIAN directamente
  - [x] Seguimiento telefónico al cliente para confirmar recepción y procesamiento
  - [x] CUFE generado por Siigo al transmitir — evidencia oficial de envío ante la DIAN
- [x] **Estados en Radian (portal DIAN):** Sin enviar · Enviada (CUFE) · Aceptada (triple check) · Rechazada · Sin confirmar (dominio público)
- [x] Registro de pagos con validación contable
- [x] PDF de factura electrónica

---

## ✅ Módulo de Cartera (módulo independiente)

- [x] **Cartera es un módulo completamente separado de Facturación**
- [x] Gestión de mora: seguimiento, días vencidos, monto pendiente
- [x] **Estrategia de cobro por tipo de dominio:**
  - [x] Corporativo → triple check automático en DIAN
  - [x] Público (Gmail/Hotmail/Yahoo) → llamada telefónica + CUFE como evidencia
- [x] Estados de gestión: Nueva · En Gestión · Acuerdo de Pago · Demanda · Castigada · Recuperada
- [x] Cobro jurídico (cuando aplica)

---

## ✅ Módulo de Reportería

- [x] **Módulo de Reportería independiente** — genera informes a partir de todos los módulos del sistema
- [x] Informes incluidos: Kardex por período · Facturas emitidas vs. pagadas · Cartera por antigüedad · Rotación de equipos · Conductores y trayectos · Cotizaciones por estado
- [x] Filtros: fecha, cliente, obra, línea de negocio, sucursal
- [x] Exportación en Excel y PDF

---

## ✅ Módulo de Auditoría

- [x] Log inmutable con: Quién · Cuándo (fecha + hora) · Qué acción
- [x] Filtro de log por usuario y por módulo
- [x] **Vista de rechazos con motivos detallados** — acceso CEO/Ingeniero
- [x] Rastreo de aprobaciones y conceptos de cada área

---

## ✅ Módulo de Notificaciones

- [x] **Módulo de Notificaciones separado** — configuración de eventos del sistema
- [x] El SuperAdmin configura qué eventos disparan qué alertas
- [x] Alertas por: aprobación pendiente, contrato sin firmar, recogida próxima, factura vencida, cronograma actualizado
- [x] Canales: sistema, email, WhatsApp

---

## ✅ Configuración y Seguridad

- [x] Control de acceso basado en roles (RBAC) — **11 roles:**
  - [x] SuperAdmin (configuración global — separado de Admin)
  - [x] Admin
  - [x] CEO / Ingeniero
  - [x] Comercial
  - [x] Dibujante
  - [x] Contabilidad
  - [x] Facturación (rol separado de Contabilidad)
  - [x] Jurídica
  - [x] Almacén
  - [x] Conductor
  - [x] Despachador
  - [x] Recepción
- [x] Catálogo configurable de productos y precios por línea de negocio
- [x] Gestión de usuarios desde el panel de administración
- [x] **Firma electrónica vía Ooku** (API keys configurables)
- [x] Alertas y notificaciones configurables (Email + WhatsApp)
- [x] **Parámetros de trayecto configurables** — tarifa/km, combustible, capacidad por tipo de camión

---

## 📌 Pendientes

- [ ] Formatos de Kardex — pendiente de redacción en sesión
- [ ] Catálogo actual de productos (Excel/TXT) por parte del cliente — para migración
- [ ] Listado de empresas, clientes y obras (~180 registros) — para migración
- [ ] Correos del personal de cada área para accesos y feedback
- [ ] Evaluación de acortar cronograma de inception para iniciar desarrollo
- [ ] Plan de migración y respaldos (fallo crítico del servidor actual — prioridad alta)
- [ ] Definir regla exacta de km/combustible para conductores (configurable por SuperAdmin)
- [ ] Confirmar si el módulo de Proforma requiere firma o confirmación simple del cliente
