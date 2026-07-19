# Matriz de Roles y Permisos — G&H Sistema

**13 roles · Control de acceso basado en roles (RBAC)**

> ✓ = Acceso completo · ◎ = Solo lectura / parcial · — = Sin acceso

---

## Módulo Clientes y Prospectos

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Ver lista de clientes/prospectos | ✓ | ✓ | ✓ | ✓ | ◎ | ✓ | ◎ | ✓ | ◎ | — | ◎ | — | **✓** |
| Crear / editar cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **✓** |
| Subir documentos del cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **✓** |
| Dar concepto favorable/no favorable | — | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — | — | — | — | **—** |
| Ver todos los conceptos de aprobación | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — | — | — | — | **—** |
| Aprobar cliente (si los 3 dan favorable) | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | **—** |
| **Ver motivos de rechazo detallados** | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | **—** |
| **Forzar aprobación (última palabra CEO)** | ✓ | — | — | — | — | — | — | — | — | — | — | — | **—** |
| **Editar datos para facturación (caso fiducia)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |

---

## Módulo Cotizaciones

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Ver cotizaciones asignadas | — | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | **◎** |
| Cargar planos y archivos | — | ✓ | ✓ | — | ✓ | — | — | — | — | — | — | — | **—** |
| Crear cotización técnica (materiales) | — | ✓ | ✓ | — | ✓ | — | — | — | — | — | — | — | **—** |
| Agregar valores comerciales | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| Generar PDF y enviar al cliente | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| Ver todas las cotizaciones | ◎ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| **Gestionar precios especiales por cliente** | — | ✓ | ✓ | ✓ | — | — | — | ◎ | — | — | — | — | **—** |
| **Acceder a cotización autogestionada (web pública)** | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **✓** |

---

## Módulo Contratos

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Crear orden de compra | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| Enviar contrato a firma electrónica (Ooku) | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| Confirmar firma del contrato | — | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | **—** |
| **Ver contratos de clientes registrados** | — | — | — | — | — | — | — | — | — | — | — | — | **◎** |

---

## Módulo Almacén / Gestión de Conductores

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Ver stock / Kardex (Bodega + Clientes + Producción) | ◎ | ✓ | ✓ | — | — | — | ◎ | — | ✓ | — | ◎ | ◎ | **—** |
| Generar remisión de salida | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| Programar agenda de transporte | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| Asignar conductor y vehículo | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| Confirmar entrega / recepción en obra | — | ✓ | ✓ | — | — | — | — | — | ✓ | ✓ | — | — | **—** |
| Ver agenda de despacho asignada | — | — | — | — | — | — | — | — | — | ✓ | — | — | **—** |
| Alertas de recogidas pendientes | ◎ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | ✓ | **—** |
| **Ver pedidos relacionados a clientes registrados** | — | — | — | — | — | — | — | — | — | — | — | — | **◎** |
| **Autorizar despacho de pedido** | — | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | **—** |
| **Clasificar estado de equipo devuelto (OK/Daño/Mant/Baja/Faltante/Ajeno)** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | ✓ | — | **—** |
| **Enviar cronograma diario de recogidas** | — | ✓ | ✓ | — | — | — | — | — | — | — | — | ✓ | **—** |
| **Registrar y gestionar equipo ajeno** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | ✓ | — | **—** |
| **Registrar indisponibilidad de conductor** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| **Verificar y cargar camiones (despachador)** | — | ✓ | ✓ | — | — | — | — | — | — | — | ✓ | — | **—** |
| **Ver y registrar movimientos de Kardex Consumibles** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | ✓ | — | **—** |
| **Alerta de stock mínimo de consumibles** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| **Evaluar criterios de liquidación conductor por viaje** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |

---

## Módulo Facturación

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Generar proforma | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| Generar factura | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Acceder a Pre-Facturación con Kardex detallado** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Ver Proforma con detalle discriminado** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| Gestionar modalidad de factura por cliente | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| Registrar pagos | — | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | **—** |
| Ver facturas propias del área | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — | **—** |
| **Enviar factura a Siigo / Validar envío DIAN** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Validar DIAN/Radian (automática y manual)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Gestionar centros de costo (13 Alquiler / 14 Venta)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Editar datos de cliente para facturación (fiducia)** | — | ✓ | ✓ | — | — | — | ✓ | — | — | — | — | — | **—** |
| **Configurar condiciones de pago por cliente** | — | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | **—** |

---

## Módulo Cartera

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Ver cartera y facturas vencidas | ◎ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — | **—** |
| Registrar gestión de cobro (notas) | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — | **—** |
| Cambiar estado de cartera | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — | **—** |
| Demanda / Cobro jurídico | — | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | **—** |

---

## Módulo Inventarios

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| **Consultar inventarios por bodega (no restrictivo)** | ◎ | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | ✓ | — | **✓** |
| **Ver disponibilidad en tiempo real (4 bodegas)** | ◎ | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | ✓ | — | **✓** |
| **Recibir alertas de stock bajo (no bloqueantes)** | — | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | **—** |
| **Filtrar por bodega según rol** | — | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | ✓ | — | **✓** |

---

## Auditoría y Configuración

| Acción | CEO | SuperAdmin | Admin | Comercial | Dibujante | Contabilidad | Facturación | Jurídica | Almacén | Conductor | Despachador | Recepción | **Soporte Atención** |
|--------|:---:|:----------:|:-----:|:---------:|:---------:|:------------:|:-----------:|:--------:|:-------:|:---------:|:-----------:|:---------:|:--------------------:|
| Ver log completo de auditoría | ✓ | ✓ | ✓ | — | — | ✓ | ◎ | — | — | — | — | — | **—** |
| Gestionar usuarios y roles | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | **—** |
| Configurar catálogo de productos | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | **—** |
| Configurar unidades de negocio | — | ✓ | ✓ | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar parámetros globales del sistema** | — | ✓ | — | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar reglas conductores (km · combustible · peso/volumen)** | — | ✓ | — | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar valor de km y reglas de trayecto** | — | ✓ | — | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar tarifas de transporte por zona (Bogotá/Fuera)** | — | ✓ | — | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar criterios de liquidación conductor (MP/RTE/SER/CL/PP)** | — | ✓ | — | — | — | — | — | — | — | — | — | — | **—** |
| **Configurar pesos por equipo del catálogo (FT/FM/AMD/ALFOR)** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |
| **Gestionar catálogo de consumibles** | — | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | **—** |

---

## Catálogo de Productos — Líneas de Negocio

| Línea de Negocio | Código Sistema | Prefijo Remisión | Ítems Aprox. | Descripción |
|------------------|:--------------:|:----------------:|:------------:|-------------|
| **Formaleta Tradicional** | `formaleta_tradicional` | `FT` | ~18 | Parales enano/corto/largo/extralargo, cerchas, crucetas corta/larga, andamio tubular, andamio colgante, escalera, saca corbatas |
| **Formaleta Metálica** | `formaleta_metalica` | `FM` | ~154 | Tableros múltiples dimensiones (0.6×1.2, 0.5×1.2, …), rinconeras, ángulos, corbatas, muretes |
| **Multidireccional AMD** | `multidireccional` | `AMD` | ~202 | Verticales con/sin espigo (0.5m, 1m, 2m), horizontales (0.7m, 1.4m, 2m, 3m), diagonales, tornillo nivelador |
| **Sistema ALFOR** | `andamio_alfor` | `ALFOR` | ~443 | Abrazaderas fija/giratoria, alineadores (múltiples longitudes), bases, cruces, plataformas — referencia ALFOR/ALFOREQUIPOS |
| **Transporte** | `transporte` | `TRP` | N/A | Fletes G&H — precio por peso Y volumen (el mayor); Bogotá $2.500/ton, Fuera $4.500/ton |
| **Consumibles (Bodega)** | `consumible` | N/A | ~6 cat. | Pintura anticorrosivo, disolvente/thinner, soldadura 6013, soldadura MIG 0.35, tornillos, gases — NO se alquilan; kardex separado |
| **Accesorios** | `accesorio` | N/A | Variable | Accesorios complementarios de cualquier línea |

> **Pesos por equipo**: Registrados en la BD con campo `peso_kg_unitario` en `catalogo_productos`. Fuente de verdad: `PESO-EQUIPOS-GYH-ACTUAL.xlsx` (hojas PESO FT, PESO FM, PESOS EQUI-ALFOR, PESO FT — mantenida por Almacén).

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
| **Tarifa por tonelada** | SuperAdmin | Bogotá: $2.500/ton · Fuera de Bogotá: $4.500/ton (configurable en `config_tarifas_transporte`) |
| **Liquidación viaje** | Sistema | Calculada automáticamente: f(km, toneladas, volumen, combustible, criterios) |

### Criterios de acceso al pago por toneladas (fuente: PESO-EQUIPOS-GYH.xlsx — hoja CONSOLIDADO)

El conductor accede al pago por toneladas **solo si cumple los 5 criterios**. El incumplimiento descuenta esa remisión de la liquidación:

| Código | Nombre | Descripción |
|:------:|--------|-------------|
| **MP** | Mantenimiento Preventivo | El carro debe salir en perfecto estado. El conductor debe avisar al mecánico o su jefe directo con anticipación — no el mismo día |
| **RTE** | Recoger Totalidad del Equipo | Indicar al almacenista si se recogió la totalidad o quedó parcial. Debe quedar anotado en la remisión |
| **SER** | Sale con Equipo · Regresa con Equipo | Carro que sale con equipo para entregar debe regresar con equipo recogido y con sus remisiones |
| **CL** | Entrega el Mismo Día | Carro que sale con equipo lo debe entregar el mismo día. Si no ocurre, esa remisión no se paga |
| **PP** | Presentación Personal | Buena presentación personal, tanto en la empresa como en las obras. Los sábados: carros lavados, tanqueados y en garaje |

> **Evaluación**: Por viaje (`agenda_transporte`). Registrada en `evaluacion_criterios_conductor`. El sistema bloquea el pago de la remisión cuando `CL=false` (no entregó el mismo día) — regla automática.

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
| **Soporte Atención** | Registra nuevos clientes con documentación completa; consulta inventarios para informar disponibilidad; ve estado de pedidos y cotizaciones de clientes registrados (solo lectura); NO aprueba clientes ni ve información financiera |
