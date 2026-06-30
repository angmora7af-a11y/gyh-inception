A continuación, presento el **Checklist Operativo y Técnico** estructurado a partir de los requerimientos de negocio, métricas y flujos que dictaste en los audios, cruzado con las bases del contrato para la Fase de Inception.

---

### 1. Checklist de Datos y Métricas de Migración

Este checklist sirve para validar la estructura de la base de datos relacional (**PostgreSQL**), asegurando que soporte el volumen de datos históricos dictados:

* [ ] **Capacidad de Carga de Clientes:** Soporte para la migración inicial de aproximadamente **180 clientes** en total (130 localizados en Bogotá y 50 distribuidos entre Ibagué y Armenia).
* [ ] **Estructura Geográfica / Sucursales:** Habilitar campos de segmentación por ciudades core (Bogotá, Ibagué, Armenia).
* [ ] **Estructura Multitier de Obras (3 Niveles Jerárquicos):**
* [ ] **Nivel 1 (Cliente):** Registro único con código de revisión automático.
* [ ] **Nivel 2 (Obra):** Capacidad de asociar hasta **50 obras independientes** por cada cliente.
* [ ] **Nivel 3 (Frente de Obra):** Capacidad de desglosar cada obra en **3 o 4 frentes de trabajo** diferentes.


* [ ] **Historial de Prospección:** Registro de hasta **50 clientes nuevos mensualmente** (con trazabilidad de si se concreta o no la venta).

---

### 2. Checklist para el Módulo Comercial y de Cotización

Para el desarrollo de la interfaz en **React** y la lógica en **FastAPI**  respecto al flujo de preventa:

* [ ] **Módulo de Dibujantes (Optimización de Tiempo):** Flujo técnico diseñado para que el proceso de modelamiento actual (que toma de 4 a 6 horas en AutoCAD) se agilice.
* [ ] **Carga y Lectura de Archivos:** Canal de entrada para planos (formatos de diseño) y exportación/importación del desglose de materiales vía Excel.
* [ ] **Integración de Catálogos Oficiales:** Conexión directa con los catálogos de precios del cliente para asignación automática de valores asociados.
* [ ] **Generador de Cotizaciones en PDF:** Exportación del documento final con los valores comerciales e impuestos agregados por el equipo de ventas.
* [ ] **Matriz de Cotización Multimodal:** Habilitar casillas de selección según el tipo de negocio:
* [ ] **Venta:** De productos/materiales existentes en catálogo.
* [ ] **Alquiler:** Equipos y maquinaria temporal.
* [ ] **Transporte:** Costos de logística, trayectos de ida y de venida.
* [ ] **Reposición:** Cobros por pérdida o no devolución de equipos.



---

### 3. Checklist Documental para Registro de Clientes (Flujo de Aprobación)

Este checklist digital reemplazará el formato actual de Excel:

* [ ] **Validación de Roles Simultáneos:** Bloqueo de avance hasta que las tres áreas den su concepto:
* [ ] **Contabilidad** (Validación financiera y de crédito).
* [ ] **Jurídica** (Validación documental y de hojas de vida).
* [ ] **Comercial** (Validación de la oportunidad de negocio).


* [ ] **Conceptos Obligatorios:** Botones de asignación de estado de viabilidad (**Favorable / No Favorable**).
* [ ] **Caja de Anotaciones / Comentarios:** Campo de texto obligatorio para que cada área justifique técnicamente su decisión antes de pasar al contrato.

---

### 4. Checklist para el Módulo de Contratos y Firma

* [ ] **Firma Electrónica:** Módulo de integración técnica (vía API) con plataformas de firma digital externa (tipo DocuSign u Okc) para la oficialización legal del contrato.
* [ ] **Transición a Operaciones:** Automatización para que un contrato firmado dispare de forma inmediata el estado "En Operaciones" y se refleje en el área de inventarios.



---

### 5. Checklist para el Módulo de Inventarios (Logística y Almacén)

* [ ] **Remisiones de Salida:** Generación automática del documento de remisión en el Kardex al momento del despacho de materiales.


* [ ] **Módulo de Agenda y Próximas Recogidas:** Calendario interactivo para el Jefe de Almacén.
* [ ] **Asignación de Conductores:** Formulario para asociar conductores, vehículos, horarios y direcciones específicas de frentes de obra a cada orden de recogida.
* [ ] **Cruce de Devoluciones:** Lógica de entrada de materiales para retornar equipos al Kardex y calcular en tiempo real los días de alquiler transcurridos.



---

### 6. Checklist de Requerimientos Transversales del Sistema

* [ ] **Cálculo por Metro Cuadrado ($/m²):** Lógica matemática en el motor de facturación para procesar cobros basados en área en productos específicos.
* [ ] **Módulo de Auditoría Global (Rastreo General):** Registro inmutable en base de datos de logs: **¿Quién realizó la acción?**, **¿Cuándo se realizó?** (Fecha/Hora) y **¿Qué tipo de cambio se hizo?**
* [ ] **Motor de Notificaciones Integrado:**
* [ ] Alertas automáticas para empujar aprobaciones pendientes entre Contabilidad, Jurídica y Comercial.


* [ ] Alertas logísticas basadas en la agenda de transporte y recolección de maquinaria.