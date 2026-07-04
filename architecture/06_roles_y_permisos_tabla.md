# Matriz de Roles y Permisos — G&H Sistema

**12 roles · Control de acceso basado en roles (RBAC)**

> ✓ = Acceso completo · ◎ = Solo lectura / parcial · — = Sin acceso

---

## Módulo Clientes y Prospectos

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Ver lista de clientes/prospectos | ✓ | ✓ | ✓ | ✓ | ◎ | ✓ | ◎ | ✓ | ◎ | — | ◎ | — |
| Crear / editar cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Subir documentos del cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Dar concepto favorable/no favorable | — | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — | — | — | — |
| Ver todos los conceptos de aprobación | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — | — | — | — |
| Aprobar cliente (si los 3 dan favorable) | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| **Ver motivos de rechazo detallados** | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| **Forzar aprobación (última palabra CEO)** | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| **Editar datos para facturación (caso fiducia)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |

---

## Módulo Cotizaciones

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Ver cotizaciones asignadas | — | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — |
| Cargar planos y archivos | — | ✓ | ✓ | — | ✓ | — | — | — | — | — | — | — |
| Crear cotización técnica (materiales) | — | ✓ | ✓ | — | ✓ | — | — | — | — | — | — | — |
| Agregar valores comerciales | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Generar PDF y enviar al cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Ver todas las cotizaciones | ◎ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| **Gestionar precios especiales por cliente** | — | ✓ | ✓ | ✓ | — | — | — | ◎ | — | — | — | — |

---

## Módulo Contratos

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Crear orden de compra | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Enviar contrato a firma electrónica (Ooku) | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Confirmar firma del contrato | — | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — |

---

## Módulo Almacén / Gestión de Conductores

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Ver stock / Kardex (Bodega + Clientes + Producción) | ◎ | ✓ | ✓ | — | — | — | ◎ | — | ✓ | — | ◎ | ◎ |
| Generar remisión de salida | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — |
| Programar agenda de transporte | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — |
| Asignar conductor y vehículo | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — |
| Confirmar entrega / recepción en obra | — | ✓ | ✓ | — | — | — | — | — | ✓ | ✓ | — | — |
| Ver agenda de despacho asignada | — | — | — | — | — | — | — | — | — | ✓ | — | — |
| Alertas de recogidas pendientes | ◎ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | ✓ |
| **Autorizar despacho de pedido** | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — |
| **Clasificar estado de equipo devuelto (OK/Daño/Mant/Baja/Faltante/Ajeno)** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | ✓ | — |
| **Enviar cronograma diario de recogidas** | — | ✓ | ✓ | — | — | — | — | — | — | — | — | ✓ |
| **Registrar y gestionar equipo ajeno** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | ✓ | — |
| **Registrar indisponibilidad de conductor** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — |
| **Verificar y cargar camiones (despachador)** | — | ✓ | ✓ | — | — | — | — | — | — | — | ✓ | — |

---

## Módulo Facturación

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Generar proforma | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| Generar factura | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| Gestionar modalidad de factura por cliente | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| Registrar pagos | — | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — |
| Ver facturas propias del área | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — |
| **Enviar factura a Siigo / Validar envío DIAN** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| **Gestionar centros de costo (13 Alquiler / 14 Venta)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| **Editar datos de cliente para facturación (fiducia)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — |
| **Configurar condiciones de pago por cliente** | — | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — |

---

## Módulo Cartera

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Ver cartera y facturas vencidas | ◎ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — |
| Registrar gestión de cobro (notas) | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — |
| Cambiar estado de cartera | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — |
| Demanda / Cobro jurídico | — | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — |

---

## Auditoría y Configuración

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|
| Ver log completo de auditoría | ✓ | ✓ | ✓ | — | — | ✓ | ◎ | — | — | — | — | — |
| Gestionar usuarios y roles | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Configurar catálogo de productos | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Configurar unidades de negocio | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| **Configurar parámetros globales del sistema** | — | ✓ | — | — | — | — | — | — | — | — | — | — |
| **Configurar reglas conductores (km · combustible · peso/volumen)** | — | ✓ | — | — | — | — | — | — | — | — | — | — |
| **Configurar valor de km y reglas de trayecto** | — | ✓ | — | — | — | — | — | — | — | — | — | — |

---

## Catálogo de Productos — Líneas de Negocio

| Línea de Negocio | Descripción | Catálogo |
|------------------|-------------|---------|
| **Formaleta Metálica (FM)** | Sistemas de encofrado metálico (Excel FM) | General anual |
| **Formaleta FP / FT** | Formaleta Plástica y Tradicional (Excel separado) | General anual |
| **Multidireccional** | Andamios y sistemas multidireccionales | General anual |
| **Transporte** | Fletes G&H — precio por peso Y volumen (el mayor) | General anual |
| **Otros / Accesorios** | Accesorios complementarios | General anual |

---

## Tipos de Catálogo de Precios

| Tipo | Responsable | Descripción |
|------|-------------|-------------|
| **General anual** | Recepción | Actualizado cada año por Recepción y distribuido a todas las áreas |
| **Especial por cliente** | Comercial / Admin | Acordado por Comercial; debe notificarse **por escrito** a Facturación |

---

## Centros de Costo — Facturación

El sistema aplica automáticamente el centro de costo según el tipo de concepto. **No se pueden mezclar centros en una misma factura** — Siigo rechazaría el envío a DIAN:

| Centro | Tipo | Impuestos aplicables |
|--------|------|----------------------|
| **13** | Alquileres | Rte. Fuente según tarifa del cliente · Rte. ICA |
| **14** | Ventas y Reposiciones | Rte. Fuente · IVA |
| **Transporte** | Siempre factura separada | Rte. Fuente 1% flete (ReteTransporte) — nunca mezclar con alquiler |

---

## Condiciones de Pago

| Parámetro | Descripción |
|-----------|-------------|
| **Días de tramitación** | Algunos clientes tienen días específicos para tramitar facturas — configurado por cliente |
| **Ciclo de cobro** | Mes vencido (default) — el cobro se hace el mes siguiente al período del servicio |
| **Modalidad** | Por remisión · Consolidada · Por valor ("lo que quepa") — configurable por cliente |
| **Habilitador de pago** | Proforma aprobada u orden de compra válida habilitan la facturación |

---

## Reglas de Liquidación de Conductores

| Parámetro | Quién configura | Descripción |
|-----------|-----------------|-------------|
| **Valor por km** | SuperAdmin | Regla configurable por kilómetro de trayecto |
| **Factor combustible** | SuperAdmin | Valor km × factor de carga por tipo de camión |
| **Capacidad de carga** | SuperAdmin | Peso máximo (toneladas) + volumen por tipo de vehículo |
| **Liquidación viaje** | Sistema | Calculada automáticamente: f(km, toneladas, volumen, combustible) |

---

## Integración DIAN — Flujo Siigo

| Paso | Responsable | Descripción |
|------|-------------|-------------|
| **1. Envío** | Facturación | Envía factura a Siigo |
| **2. Transmisión** | Siigo (automático) | Siigo transmite a la DIAN |
| **3. Validación** | Facturación | Verifica en el portal DIAN (no confiar en el estado de Siigo — puede ser incorrecto) |
| **4. Seguimiento** | Facturación / Cartera | Llamada telefónica al cliente para confirmar recepción y procesamiento |

---

## Descripción de Roles

| Rol | Descripción |
|-----|-------------|
| **CEO / Ingeniero** | Auditoría global, motivos de rechazo y aprobación forzada bajo su responsabilidad |
| **SuperAdmin** | Configuración global del sistema: valor de km, reglas de combustible, capacidad por camión, parámetros sistémicos. Tiene todos los permisos de Admin más la configuración de reglas de negocio globales |
| **Admin** | Administra usuarios, catálogo, precios y operación diaria del sistema |
| **Comercial** | Gestiona prospectos, cotizaciones y relación con el cliente; autoriza despachos |
| **Dibujante** | Modelamiento técnico en AutoCAD, generación de cotizaciones de materiales |
| **Contabilidad** | Validación financiera, conceptos de aprobación de clientes y supervisión de cartera |
| **Facturación** | Genera facturas y proformas, envía a Siigo/DIAN, gestiona centros de costo y cartera |
| **Jurídica** | Validación documental, listas LAFT y confirmación de contratos |
| **Almacén** | Gestiona inventario, pedidos, remisiones, agenda de transporte y devoluciones |
| **Despachador** | Verifica y carga físicamente los camiones antes del despacho; clasifica estado de devoluciones (6 estados) |
| **Conductor** | Ejecuta transporte de equipos a obras; su liquidación se calcula por km, carga y combustible |
| **Recepción** | Genera cronograma diario de recogidas y cortes; recibe reporte de Almacén |
