# Matriz de Roles y Permisos — G&H Sistema

**8 roles · Control de acceso basado en roles (RBAC)**

> ✓ = Acceso completo · ◎ = Solo lectura / parcial · — = Sin acceso

---

## Módulo Clientes y Prospectos

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Ver lista de clientes/prospectos | ✓ | ✓ | ✓ | ◎ | ✓ | ✓ | ◎ | — |
| Crear / editar cliente | — | ✓ | ✓ | — | — | — | — | — |
| Subir documentos del cliente | — | ✓ | ✓ | — | — | — | — | — |
| Dar concepto favorable/no favorable | — | ✓ | ✓ | — | ✓ | ✓ | — | — |
| Ver todos los conceptos de aprobación | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — |
| Aprobar cliente (si los 3 dan favorable) | — | ✓ | — | — | — | — | — | — |
| **Ver motivos de rechazo detallados** | ✓ | ✓ | — | — | — | — | — | — |
| **Forzar aprobación (última palabra CEO)** | ✓ | — | — | — | — | — | — | — |

---

## Módulo Cotizaciones

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Ver cotizaciones asignadas | — | ✓ | ✓ | ✓ | — | — | — | — |
| Cargar planos y archivos | — | ✓ | — | ✓ | — | — | — | — |
| Crear cotización técnica (materiales) | — | ✓ | — | ✓ | — | — | — | — |
| Agregar valores comerciales | — | ✓ | ✓ | — | — | — | — | — |
| Generar PDF y enviar al cliente | — | ✓ | ✓ | — | — | — | — | — |
| Ver todas las cotizaciones | ◎ | ✓ | ✓ | — | — | — | — | — |

---

## Módulo Contratos

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Crear orden de compra | — | ✓ | ✓ | — | — | — | — | — |
| Enviar contrato a firma electrónica | — | ✓ | ✓ | — | — | — | — | — |
| Confirmar firma del contrato | — | ✓ | — | — | — | ✓ | — | — |

---

## Módulo Inventarios y Logística

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Ver stock / Kardex (Bodega + Clientes + Producción) | ◎ | ✓ | — | — | — | — | ✓ | — |
| Generar remisión de salida | — | ✓ | — | — | — | — | ✓ | — |
| Programar agenda de transporte | — | ✓ | — | — | — | — | ✓ | — |
| Asignar conductor y vehículo | — | ✓ | — | — | — | — | ✓ | — |
| Confirmar entrega / recepción en obra | — | ✓ | — | — | — | — | ✓ | ✓ |
| Ver agenda de despacho asignada | — | — | — | — | — | — | — | ✓ |
| Alertas de recogidas pendientes | ◎ | ✓ | — | — | — | — | ✓ | — |

---

## Módulo Facturación

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Generar factura | — | ✓ | — | — | ✓ | — | — | — |
| Registrar pagos | — | ✓ | — | — | ✓ | — | — | — |
| Gestionar cartera | — | ✓ | — | — | ✓ | ✓ | — | — |
| Ver facturas propias del área | — | ✓ | — | — | ✓ | ✓ | — | — |

---

## Auditoría y Configuración

| Acción | CEO | Admin | Comercial | Dibujante | Contabilidad | Jurídica | Almacén | Conductor |
|--------|:---:|:-----:|:---------:|:---------:|:------------:|:--------:|:-------:|:---------:|
| Ver log completo de auditoría | ✓ | ✓ | — | — | ✓ | — | — | — |
| Gestionar usuarios y roles | — | ✓ | — | — | — | — | — | — |
| Configurar catálogo de productos | — | ✓ | — | — | — | — | — | — |
| Configurar unidades de negocio (catálogo) | — | ✓ | — | — | — | — | — | — |

---

## Catálogo de Productos — Unidades de Negocio

El catálogo de precios e inventario se subdivide por unidad de negocio para filtrar disponibilidad y precios:

| Unidad de Negocio | Descripción |
|-------------------|-------------|
| **Formaleta Metálica** | Sistemas de encofrado metálico para estructuras |
| **Multidireccional** | Andamios y sistemas multidireccionales |
| **Transporte** | Fletes, servicios de transporte y logística |
| **Formaleta Plástica** | Encofrados en material plástico |
| **Formaleta Tradicional** | Sistemas de encofrado en madera/tradicional |
