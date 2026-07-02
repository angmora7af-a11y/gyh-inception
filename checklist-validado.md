# Checklist Validado — G&H Sistema de Gestión
**Sesión 2026-06-16 + Ajustes Feedback 2026-06-24**

---

## ✅ Módulo de Clientes y Aprobación

- [x] Formulario FT-AC-001 v2.0 — 9 secciones digitalizadas en el sistema
- [x] Checklist documental: RUT, Cámara de Comercio, Cédula Rep. Legal, EEFF, Autorización Centrales de Riesgo, Carta de Presentación
- [x] Aprobación simultánea de 3 áreas: Comercial, Jurídica, Contabilidad
- [x] **Notas por especialidad obligatorias** — cada área registra justificación textual al dar concepto
- [x] **Rol CEO/Ingeniero** — perfil de consulta con acceso a motivos de rechazo detallados
- [x] **Aprobación forzada por CEO** — regla de negocio: el CEO tiene la última palabra bajo su responsabilidad
- [x] Notificación automática a todas las áreas para agilizar proceso de aprobación

---

## ✅ Módulo de Cotizaciones

- [x] Carga de planos en DWG, DXF, PDF desde el sistema
- [x] Importación de Excel de materiales exportado desde AutoCAD
- [x] Consulta automática del catálogo de precios y asignación de valores
- [x] **Catálogo subdividido por unidades de negocio:**
  - [x] Formaleta Metálica
  - [x] Multidireccional
  - [x] Transporte
  - [x] Formaleta Plástica
  - [x] Formaleta Tradicional
- [x] Tipos de negocio: Venta, Alquiler, Transporte, Reposición
- [x] Validación de retenciones: Rte. Fuente, Rte. ICA, IVA
- [x] Generación de PDF oficial con logo y datos completos
- [x] Envío de PDF directamente al cliente desde el sistema

---

## ✅ Módulo de Contratos

- [x] Generación de Orden de Compra a partir de cotización aprobada
- [x] Firma electrónica vía DocuSign / Okc
- [x] Seguimiento del estado del contrato (Pendiente → Firmado → Activo)
- [x] Activación automática de operaciones al completar la firma

---

## ✅ Módulo de Inventarios y Logística

- [x] Kardex con remisiones de salida y entrada
- [x] **Stock total (Momento Cero): Bodega + Equipos en Clientes + Equipos en Producción**
- [x] Agenda de transporte: conductor, vehículo, placa, hora, dirección
- [x] Cálculo de días de alquiler: fecha remisión salida → fecha remisión entrada
- [x] Inspección de equipos devueltos: Buen Estado / Dañado / Faltante
- [x] Reposición automática por faltante (cobro al cliente)
- [x] **Alertas proactivas de recogidas pendientes** — triggers para optimizar rutas de transporte
- [x] **Registro de fecha y hora en todas las transacciones** (campos globales)
- [ ] *(Fase 3)* Evidencias de entrega: firma digital + fotografías por conductores

---

## ✅ Módulo de Facturación

- [x] Generación de factura con cálculo de m² y días de alquiler
- [x] Retenciones: Rte. Fuente, ICA, IVA según configuración del cliente
- [x] Registro de pagos con validación contable
- [x] Gestión de cartera: seguimiento, mora y cobro jurídico

---

## ✅ Módulo de Auditoría

- [x] Log inmutable con: Quién · Cuándo (fecha + hora) · Qué acción
- [x] Filtro de log por usuario y por módulo
- [x] **Vista de rechazos con motivos detallados** — acceso CEO/Ingeniero
- [x] Rastreo de aprobaciones y conceptos de cada área

---

## ✅ Configuración y Seguridad

- [x] Control de acceso basado en roles (RBAC) — 8 roles
- [x] Catálogo configurable de productos y precios por unidad de negocio
- [x] Gestión de usuarios desde el panel de administración
- [x] Integración de firma electrónica (API keys configurables)
- [x] Alertas y notificaciones configurables (Email + WhatsApp)

---

## 📌 Pendientes (Próxima Sesión)

- [ ] Detalle del módulo de Logística, Inventarios y Órdenes de Compra
- [ ] Envío de catálogo de productos actual (Excel/TXT) por parte del cliente
- [ ] Listado de empresas, clientes y obras para migración (~180 registros)
- [ ] Correos del personal de cada área para habilitar accesos y feedback
- [ ] Evaluación de acortar cronograma de inception para iniciar desarrollo
- [ ] Plan de migración y respaldos (fallo crítico del servidor actual — prioridad alta)
