A continuación, se presenta la estructura completa y detallada del documento `DESIGN_SYSTEM.md` basada en la extracción minuciosa de tokens de diseño, selectores, variables nativas, comportamiento adaptativo y componentes analizados a partir del código fuente y los scripts de configuración provistos.

---

# DESIGN_SYSTEM.md

## 1. Fundamentos de Identidad y Marca

### 1.1 Logotipo e Iconografía Base

* **Logotipo Principal:** Archivo en formato WebP con dimensiones optimizadas de `800x425` px. (`https://gyhbogota.com/wp-content/uploads/2024/06/logo-800x425.webp`).
* **Favicon e Identificadores de Dispositivo:**
* 32x32 px: `cropped-logo-32x32.webp`
* 192x192 px: `cropped-logo-192x192.webp`
* Apple Touch Icon (180x180 px): `cropped-logo-180x180.webp`
* MS Application Tile (270x270 px): `cropped-logo-270x270.webp`



---

## 2. Paleta de Colores y Gradientes (`Design Tokens`)

### 2.1 Colores Sólidos (Core CSS Variables)

```css
:root {
    --wp--preset--color--black: #000000;
    --wp--preset--color--white: #ffffff;
    --wp--preset--color--cyan-bluish-gray: #abb8c3;
    --wp--preset--color--pale-pink: #f78da7;
    --wp--preset--color--vivid-red: #cf2e2e;
    --wp--preset--color--luminous-vivid-orange: #ff6900;
    --wp--preset--color--luminous-vivid-amber: #fcb900;
    --wp--preset--color--light-green-cyan: #7bdcb5;
    --wp--preset--color--vivid-green-cyan: #00d084;
    --wp--preset--color--pale-cyan-blue: #8ed1fc;
    --wp--preset--color--vivid-cyan-blue: #0693e3;
    --wp--preset--color--vivid-purple: #9b51e0;
}

```

### 2.2 Colores Semánticos e Identidad de Plantilla

* **Color de Acentuación Primario (`.mil-accent` / Custom CSS):** `#bcff00` (Verde Limón / Neón brillante).
* **Color de Acentuación Secundario (Iconos/Enlaces Form):** `#769d08` / `#459c34` / `#459c34`.
* **Fondo de Botones WooCommerce (Éxito):** `#4CAF50` (Hover: `#45a049`).
* **Fondo de Botones Estándar / Bloques:** `#32373c`.
* **Color del Texto de Precios (WooCommerce):** `#FF5722` (Naranja vibrante).
* **Color de Fondo de WhatsApp Corporativo:** `#25D366` (Hover: `#00d34d`).

### 2.3 Gradientes Preestablecidos (`Gradients`)

* **Vivid Cyan Blue to Vivid Purple:** `linear-gradient(135deg, rgb(6, 147, 227) 0%, rgb(155, 81, 224) 100%)`
* **Light Green Cyan to Vivid Green Cyan:** `linear-gradient(135deg, rgb(122, 220, 180) 0%, rgb(0, 208, 130) 100%)`
* **Luminous Vivid Amber to Luminous Vivid Orange:** `linear-gradient(135deg, rgb(252, 185, 0) 0%, rgb(255, 105, 0) 100%)`
* **Luminous Vivid Orange to Vivid Red:** `linear-gradient(135deg, rgb(255, 105, 0) 0%, rgb(207, 46, 46) 100%)`
* **Very Light Gray to Cyan Bluish Gray:** `linear-gradient(135deg, rgb(238, 238, 238) 0%, rgb(169, 184, 195) 100%)`
* **Cool to Warm Spectrum:** `linear-gradient(135deg, rgb(74, 234, 220) 0%, rgb(151, 120, 209) 20%, rgb(207, 42, 186) 40%, rgb(238, 44, 130) 60%, rgb(251, 105, 98) 80%, rgb(254, 248, 76) 100%)`
* **Blush Light Purple:** `linear-gradient(135deg, rgb(255, 206, 236) 0%, rgb(152, 150, 240) 100%)`
* **Blush Bordeaux:** `linear-gradient(135deg, rgb(254, 205, 165) 0%, rgb(254, 45, 45) 50%, rgb(107, 0, 62) 100%)`
* **Luminous Dusk:** `linear-gradient(135deg, rgb(255, 203, 112) 0%, rgb(199, 81, 192) 50%, rgb(65, 88, 208) 100%)`
* **Pale Ocean:** `linear-gradient(135deg, rgb(255, 245, 203) 0%, rgb(182, 227, 212) 50%, rgb(51, 167, 181) 100%)`
* **Electric Grass:** `linear-gradient(135deg, rgb(202, 248, 128) 0%, rgb(113, 206, 126) 100%)`
* **Midnight:** `linear-gradient(135deg, rgb(2, 3, 129) 0%, rgb(40, 116, 252) 100%)`

---

## 3. Tipografía y Jerarquía Visual

### 3.1 Familias Tipográficas Preestablecidas

* **Inter (Sans-serif):** Cargada localmente a través de variables de WooCommerce. Rango de peso: `300 a 900`. Usada para bloques y elementos de interfaz de lectura continua. (`--wp--preset--font-family--inter`).
* **Cardo (Serif):** Peso `400`. Usada para bloques tradicionales elegantes. (`--wp--preset--font-family--cardo`).
* **Sora (Sans-serif):** Pesos `100;200;300;400;500;600;700;800`. Utilizada en elementos de UI personalizados como leyendas e imágenes (`figcaption`).
* **Syne:** Pesos `400;500;600;700;800`.
* **Caveat & Satisfy:** Fuentes de acentuación caligráfica / tipografía secundaria de la plantilla *Ruizarch*.

### 3.2 Escala de Tamaños (`Font Sizes`)

* `--wp--preset--font-size--small`: `13px`
* `--wp--preset--font-size--medium`: `20px`
* `--wp--preset--font-size--large`: `36px`
* `--wp--preset--font-size--x-large`: `42px`

### 3.3 Reglas de Transformación Textual

```css
h1, .mil-h1 {
    text-transform: uppercase;
}
h2, .mil-h2, h3, .mil-h3, h4, .mil-h4, h5, .mil-h5, h6, .mil-h6 {
    text-transform: unset;
}
figcaption {
    font-family: "Sora", sans-serif;
    font-weight: 600;
    font-size: 16px !important;
    text-transform: uppercase !important;
    color: rgb(0,0,0);
}

```

---

## 4. Estructura de Espaciados y Sombras

### 4.1 Grid y Layout Espaciado (`Spacing Tokens`)

* `--wp--preset--spacing--20`: `0.44rem`
* `--wp--preset--spacing--30`: `0.67rem`
* `--wp--preset--spacing--40`: `1rem`
* `--wp--preset--spacing--50`: `1.5rem`
* `--wp--preset--spacing--60`: `2.25rem`
* `--wp--preset--spacing--70`: `3.38rem`
* `--wp--preset--spacing--80`: `5.06rem`

### 4.2 Sombras de Elevación (`Elevation Box Shadows`)

* **Natural:** `6px 6px 9px rgba(0, 0, 0, 0.2)`
* **Deep:** `12px 12px 50px rgba(0, 0, 0, 0.4)`
* **Sharp:** `6px 6px 0px rgba(0, 0, 0, 0.2)`
* **Outlined:** `6px 6px 0px -3px rgb(255, 255, 255), 6px 6px rgb(0, 0, 0)`
* **Crisp:** `6px 6px 0px rgb(0, 0, 0)`
* **Light Soft (Productos Grid):** `0 2px 5px rgba(0, 0, 0, 0.1)` (Hover: `0 5px 15px rgba(0, 0, 0, 0.2)`)

---

## 5. Layout Adaptativo y Puntos de Interrupción (`Breakpoints`)

De acuerdo con el archivo de configuración interna de Elementor (`elementorFrontendConfig`), la matriz de breakpoints estipulada es la siguiente:

| Breakpoint Key | Label | Value (px) | Direction | Estado |
| --- | --- | --- | --- | --- |
| **xs** | Extra Small | 0 | min | Por defecto |
| **sm** | Small | 480 | min | Por defecto |
| **md** | Medium | 768 | min | Activo |
| **mobile** | Móvil vertical | 767 | max | Activo |
| **mobile_extra** | Móvil horizontal | 880 | max | Deshabilitado |
| **tablet** | Tableta vertical | 1024 | max | Activo |
| **tablet_extra** | Tableta horizontal | 1200 | max | Deshabilitado |
| **lg / laptop** | Portátil | 1025 / 1366 | max | Deshabilitado |
| **xl** | Extra Large | 1440 | min | Por defecto |
| **xxl / widescreen** | Pantalla grande | 1600 / 2400 | min / max | Deshabilitado |

---

## 6. Componentes del Sistema (`UI Components`)

### 6.1 Botones (`Buttons`)

#### Botón de Bloque Clásico (`.wp-block-button__link`)

* **Propiedades:** Fondo `#32373c`, texto `#fff`, bordes totalmente redondeados (`border-radius: 9999px`), padding balanceado de `calc(.667em + 2px) calc(1.333em + 2px)`, tamaño de fuente `1.125em`. Sin decoración de texto ni sombras por defecto.

#### Botón de Acción de Compra (`.woocommerce button.button`)

* **Propiedades:** Fondo `#4CAF50`, texto `#ffffff`, sin bordes, padding `10px 20px`, `border-radius: 25px`, fuente negrita, tamaño `14px`. Transición suave de color de fondo a `0.3s ease`. Hover cambia a `#45a049`.

#### Botón de Interfaz Temática (`.mil-button.mil-sm`)

* **Propiedades:** Texto transformado a mayúsculas (`.mil-upper`), tamaño pequeño (`.mil-sm`). Estilo embebido por la plantilla para botones interactivos principales ("REGISTRARME COMO CLIENTE").

---

### 6.2 Tarjetas de Producto y Contenedores Grillas (`E-Commerce Layout`)

```css
.woocommerce ul.products li.product {
    float: left;
    margin: 0.5%;
    width: 24% !important; /* Estructura rígida de 4 columnas en desktop */
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
    padding: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.woocommerce ul.products li.product:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

```

---

### 6.3 Tarjetas de Servicios (`.mil-service-card`)

* **Padding:** `15px 40px !important`.
* **Altura mínima unificada:** `309px` (Sobrescribe comportamientos previos de `220px`).
* **Interactividad:** Integra un elemento indicador de navegación (`.mil-go-buton.mil-icon-accent-bg`) que contiene un asset SVG lineal (`arrow-copia.svg`).

---

### 6.4 Acordeones y FAQ (`.mil-accordion-group`)

* **Estructura Visual:** Compuesto por un menú dinámico de control de estado (`.mil-accordion-menu`) y un contenedor expansible de contenido (`.mil-accordion-content`).
* **Indicador de Estado Alternable (`.mil-symbol`):** Alterna la visibilidad entre el signo más (`.mil-plus`) y el signo menos (`.mil-minus`) empleando tipografías delgadas (`.mil-thin`) y colores claros (`.mil-light`).

---

### 6.5 Sistema de Alertas y Retroalimentaciones Semánticas

Utiliza un padding unificado de `15px`, con esquinas redondeadas a `8px`, margen inferior de `20px` y tamaño de fuente de `14px`. Poseen un borde izquierdo destacado de `4px solid`:

* **Mensaje Exitoso (`.woocommerce-message`):** Fondo `#dff0d8`, texto e indicador `#3c763d`.
* **Mensaje de Error (`.woocommerce-error`):** Fondo `#f2dede`, texto e indicador `#a94442`.
* **Mensaje Informativo (`.woocommerce-info`):** Fondo `#d9edf7`, texto e indicador `#31708f`.

---

## 7. Navegación, Cabecera y Menús (`Navigation & Menus`)

### 7.1 Menú Principal (`.mil-navigation`)

* **Efecto de Enlace Activo e Ítem de Menú Actual:**
```css
.mil-navigation nav ul li.mil-has-children ul li.current-menu-item a,
.mil-navigation nav ul li.current-menu-item > a {
    color: #bcff00 !important; /* Verde Neón Corporativo */
    background: #000 !important; /* Contraste en Negro Puro */
}

```


* **Ocultación de Pseudoelementos nativos:** `.mil-navigation nav ul li.mil-has-children > a:before { display: none !important; }`.
* **Ajustes de Margen:** Los elementos de lista (`li`) o sub-menús poseen un `margin-bottom: 15px !important` (reducidos de los `25px` o `30px` por defecto en resoluciones específicas).

---

## 8. Elementos Adicionales de Interfaz Flotante (Widget de Terceros)

### 8.1 Botón Click-To-Chat (WhatsApp Widget)

* **Estructura fija:** Anclado mediante `position: fixed; bottom: 15px; right: 15px; z-index: 99999999;`.
* **Estilos en Estado de Reposo:** Fondo `#25D366`, `border-radius: 25px`, dimensiones del SVG interno de `30x30` px con color de relleno `#ffffff`.
* **Estilos en Hover:**
```css
.ht-ctc .ctc_s_7_1:hover .ctc_s_7_icon_padding,
.ht-ctc .ctc_s_7_1:hover {
    background-color: #00d34d !important;
}
.ht-ctc .ctc_s_7_1:hover .ctc_s_7_1_cta {
    color: #f4f4f4 !important;
}
.ht-ctc .ctc_s_7_1:hover svg g path {
    fill: #f4f4f4 !important;
}

```


* **Parámetros de Integración del Script:** Vinculado al número telefónico de soporte (`573133336813`).

---

*Fin del archivo DESIGN_SYSTEM.md*