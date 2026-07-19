# 📚 G&H Obras y Estructuras Metálicas — Documentación Técnica

**Sistema de Gestión Integral · PostgreSQL · React 18**

---

## 📑 Índice de Documentación

### 🏗️ Arquitectura del Sistema

1. **[Flujo Principal GYH](architecture/01_flujo_principal_gyh.mmd)**
   Flujo general del sistema desde prospecto hasta facturación

2. **[Arquitectura del Sistema](architecture/02_arquitectura_sistema.mmd)**
   Diagrama de componentes y capas de la aplicación

3. **[Módulo de Cotizaciones](architecture/03_modulo_cotizacion.mmd)**
   Proceso de cotización técnica + comercial + **cotización autogestionada web**

4. **[Registro y Aprobación de Clientes](architecture/04_registro_aprobacion_cliente.mmd)**
   Flujo de aprobación tripartita (Comercial, Contabilidad, Jurídica)

5. **[Módulo de Inventarios y Logística](architecture/05_modulo_inventarios_logistica.mmd)**
   Gestión de stock, remisiones y agenda de transporte

6. **[Roles y Permisos](architecture/06_roles_y_permisos.mmd)**
   Diagrama de permisos por rol (13 roles incluyendo **Soporte Atención**)

---

### 💰 Facturación e Integración

7. **[Integración Siigo/DIAN](architecture/07_integracion_siigo.mmd)**
   Secuencia de envío a Siigo y validación DIAN (6 fases)

8. **[Módulo Kardex y Facturación](architecture/08_modulo_kardex_facturacion.mmd)**
   Facturación detallada por kardex con devoluciones parciales

9. **[Sistema de Bodegas e Inventarios](architecture/09_bodegas_inventarios.mmd)**
   4 bodegas consultivas (no restrictivas) con visibilidad por rol

10. **[Validación DIAN/Radian](architecture/10_validacion_dian_radian.mmd)**
    Proceso de validación electrónica con automatizaciones

---

### 🔗 Integración Completa

11. **[Flujo Completo de Integración Siigo](architecture/11_flujo_completo_integracion_siigo.mmd)**
    **📌 DIAGRAMA MAESTRO DE INTEGRACIÓN**
    Flujo completo desde cotización hasta pago:
    - **Cotización → Siigo** (opcional)
    - **Pedido → Siigo** (completo/parcial)
    - **Remisión salida/devolución → Siigo**
    - **Facturación → Siigo → DIAN**
    - **Validación DIAN con scraping automático del CUFE**
    - **Sincronización de pagos Siigo → GYH**
    - Especificaciones técnicas de scraping Python/Node
    - API endpoints Siigo documentados
    - Sistema de alertas y monitoreo

---

### 📊 Base de Datos

- **[Schema DBML](database/gyh_schema.dbml)**
  Esquema completo de PostgreSQL v1.1 (SEM-27)
  Incluye: 13 roles, bodegas_inventario, conversión de unidades, validación DIAN

---

### 📝 Especificaciones y Tablas

- **[Matriz de Roles y Permisos](architecture/06_roles_y_permisos_tabla.md)**
  Tabla completa de permisos por módulo (13 roles × 10 módulos)

---

### 🎨 Diseño

- **[Design System v2](DESIGN_SYSTEM_V2.md)**
  Sistema de diseño "The Industrial Ledger"

- **[Design System v1](DESIGN_SYSTEM.md)**
  Versión anterior del sistema de diseño

---

### 📋 Sitemaps

- [Sitemap Principal](sitemaps/sitemap_gyh_app.mmd)
- [Auth y Dashboard](sitemaps/sitemap_01_auth_dashboard.mmd)
- [Clientes](sitemaps/sitemap_02_clientes.mmd)
- [Cotizaciones](sitemaps/sitemap_03_cotizaciones.mmd)
- [Contratos](sitemaps/sitemap_04_contratos.mmd)
- [Inventarios](sitemaps/sitemap_05_inventarios.mmd)
- [Facturación](sitemaps/sitemap_06_facturacion.mmd)
- [Auditoría y Configuración](sitemaps/sitemap_07_auditoria_config.mmd)

---

### 📚 Historias de Usuario

- **[Historias de Usuario](user-stories/historias_usuario.md)**
  User stories por módulo y rol

---

### 📅 Seguimiento y Planes

- **[Plan de Actualización SEM-27](follow/PLAN_ACTUALIZACION_SEM27.md)**
- **[Plan 16 de Julio 2026](follow/PLAN_16JUL.md)**
  Mejoras implementadas: kardex detallado, conversión de unidades, rol soporte, validación DIAN, cotización autogestionada, inventarios consultivos
- **[Checklist Validado](follow/checklist-validado.md)**
- **[Notificaciones](follow/notificaciones.md)**

---

## 🔧 Cómo Usar esta Documentación

### Ver Diagramas .mmd (Mermaid)

Los diagramas `.mmd` se pueden visualizar de varias formas:

#### Opción 1: Visual Studio Code
Instalar extensión: **Mermaid Preview** o **Markdown Preview Mermaid Support**

#### Opción 2: Navegador
1. Copiar contenido del archivo .mmd
2. Ir a: https://mermaid.live/
3. Pegar el código

#### Opción 3: Script Python (Recomendado)
```bash
# Instalar dependencias
pip install mermaid-py

# Convertir .mmd a PNG/SVG
python scripts/render_mermaid.py architecture/11_flujo_completo_integracion_siigo.mmd
```

---

## 📌 Actualizaciones Recientes (Julio 2026)

### ✅ Nuevas Funcionalidades Implementadas

1. **Rol Soporte Atención al Cliente**
   - Registra clientes con documentación
   - Consulta inventarios para informar disponibilidad
   - NO aprueba clientes ni ve información financiera

2. **Facturación por Kardex Detallado**
   - Considera devoluciones parciales automáticamente
   - Genera períodos discriminados
   - Elimina proceso manual de "punteo"

3. **Conversión Automática de Unidades**
   - Productos se registran en UND en kardex
   - Se facturan en M² cuando aplica
   - Conversión automática: cantidad × (largo × ancho)

4. **Validación DIAN/Radian Automatizada**
   - Scraping automático del portal DIAN
   - Validación +1 hora post-envío
   - Revisión nocturna de pendientes
   - Extracción automática de CUFE

5. **Cotización Autogestionada Web**
   - Portal público sin autenticación
   - 5 pasos: productos → cantidades → disponibilidad → resumen → contacto
   - Genera PDF indicativa
   - Notifica a Soporte Atención

6. **Sistema de Inventarios Consultivo**
   - 4 bodegas con visibilidad por rol
   - Alertas de stock bajo (NO bloqueantes)
   - Permite operaciones con stock insuficiente
   - Indicadores visuales de disponibilidad

7. **Alertas de Pedidos Incompletos**
   - Dashboard con KPIs
   - Alertas automáticas para items faltantes
   - Función "Enviar Alerta" a comercial y cliente

8. **Vista de Proforma Discriminada**
   - Detalle por producto con períodos
   - Cálculos expandibles
   - Conversión de unidades visible

---

## 🎯 Próximos Pasos

- [ ] Implementar scraping DIAN en producción
- [ ] Configurar webhooks Siigo
- [ ] Automatizar sincronización de pagos
- [ ] Dashboard de monitoreo de integración
- [ ] Sistema de alertas en tiempo real

---

## 📞 Contacto

**G&H Obras y Estructuras Metálicas S.A.S.**
NIT: 901.218.896-8
Bogotá, Colombia

---

*Documentación actualizada: Julio 2026*
*Versión del sistema: SEM-27 + Mejoras Julio 2026*
