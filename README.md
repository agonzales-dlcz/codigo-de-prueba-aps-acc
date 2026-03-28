![License](https://img.shields.io/badge/license-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![ACC](https://img.shields.io/badge/ACC-Autodesk_Construction_Cloud-FF6C00?logo=autodesk&logoColor=white)
![ACC Model Properties](https://img.shields.io/badge/ACC-Model_Properties_API-FF6C00?logo=autodesk&logoColor=white)
![APS](https://img.shields.io/badge/APS-Autodesk_Platform_Services-0696D7?logo=autodesk&logoColor=white)
![APS Model Derivative](https://img.shields.io/badge/APS-Model_Derivative_API-0696D7?logo=autodesk&logoColor=white)
![APS OAuth](https://img.shields.io/badge/APS-OAuth_2.0_PKCE-0696D7?logo=autodesk&logoColor=white)
![Data Management API](https://img.shields.io/badge/Data_Management_API-APS-0696D7?logo=autodesk&logoColor=white)
![Data Management Hubs](https://img.shields.io/badge/Data_Management-Hubs_%26_Projects-0696D7?logo=autodesk&logoColor=white)

# Extraer Información de Modelos Del ACC

Si se tiene una cuenta con suscripción activa para APS y ACC saltar al PASO 2

## I - PRERREQUISITOS

### 0.1 - Instalar Python

Descargar directamente el instalador del 3.14 (64-bit) en [Python 3.14.0](https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe).

> [!IMPORTANT]
> En la instalación, marcar el check **"Add Python to PATH"** antes de hacer clic en **Install Now**. Si no se hizo se puede volver a instalar y añadir el check.

### 0.2 - Verificar las variables de entorno

Abrir una terminal nueva y ejecutar -> Win + R -> `cmd` -> Enter:

```cmd
python --version
pip --version
```

> [!TIP]
> Si el comando no se reconoce, cerrar y volveer a abrir la terminal —> los cambios al PATH no se aplican a sesiones ya abiertas.

### 0.3 - Instalar dependencias
1. Abrir la **consola de windows** -> Win + R -> `cmd` -> Enter
2. Para para este caso es necesario tener dotenv

```bash
pip install python-dotenv
```

3. Si se necesitara otra dependencia el proceso es el mismo

```bash
pip install reemplazar-por-nombre-de-dependencia
```
---

## II - INFRAESTRUCTURA AUTODESK

## PASO 1 - Obtener una cuenta con suscripción activa

En caso de no tener una suscripcion, se puede obtener una temporal (30 días) con un correo personal o un nuevo correo temporal

### 1.1 - Crear cuenta Autodesk personal

1. En [autodesk.com](https://www.autodesk.com) -> **Create Account**
2. Completar los datos personales.
3. **Importante** se tiene que usar un correo (gmail, etc) que no tenga una versión de prueba anterior ya caducada esto se activará en los pasos 1.2 y 1.4, si el correo ya se ha usado antes y su licencia temporal ya está caducada no se podrá crear el la application en el paso 4
4. Verificar el correo y completar el registro

> La cuenta Autodesk creada sirve tanto para APS como para el ACC, esto se puede hacer indefinidamente claro que el correo siempre tendrá que ser uno nuevo.

### 1.2 - Activar la versión de prueba del ACC

1. Entrar a [https://construction.autodesk.com/trial/autodesk-build/](https://construction.autodesk.com/trial/autodesk-build/)
2. Completar el formulario, al terminar es redirigido a la cuenta ACC nueva con rol de **Admin Account** (es necesario contar con este rol)

### 1.3 - Activar la versión de prueba del APS

1. Ir a [aps.autodesk.com/pricing](aps.autodesk.com/pricing)
2. Seleccionar **Free** -> completar el registro, pide tarjeta, la compra vale 0.00$.

> APS llega a cobrar si se excede el límite mensual de uso de ciertas APIs, sin embargo, eso no es restrictivo para este caso (ver notas del paso 2)

---

## PASO 2 - Crear HUB

El código toma la información de modelos en la nube. Para eso se debe crear un **Hub gratuito** que almacene proyectos y modelos:

1. Ir [manage.autodesk.com](https://manage.autodesk.com) e iniciar sesión
2. Click en la cinta **Products and Services -> Hubs**
3. Click en **Create Hub -> APS Developer Hub**
4. Dar un nombre luego a **Create & Activate**
5. El nuevo Hub aparecerá en la lista inferior

> Algunas APIs de APS son gratuitas e ilimitadas como:<br><br>
>   **- Authentication API** (3-legged)<br>
>   **- Model Properties API** (propiedades de elementos)<br>
>   **- Webhooks API** (eventos ACC)<br>
>   **- Data Management API** (hubs, proyectos, versiones)<br><br>
> Sin embargo, hay APIs con límite mensual gratuito, pero de pago una vez que se exceda dicho límite como:<br><br>
>   **- Model Derivative API** (traducciones RVT a SVF2, límite -> 20 trabajos complejos, 60 trabajos simples, 300'000 llamadas gratis)<br>
>   (ver [https://www.autodesk.com/products/autodesk-platform-services/product-details](https://www.autodesk.com/products/autodesk-platform-services/product-details))<br><br>

> [!CAUTION]
> **traducir un .rvt a .svf2 es considerado un trabajo complejo, no excederse de 20 al mes**

> [!IMPORTANT]
> **SIN EMBARGO, para cuentas con suscripcion de pago de ACC la traducción es automática (cuando se publica desde ACC Docs o desde el conector de Revit, NO CUANDO SE SUBE MANUALMENTE) y el costo está incluido en la licencia**

---

## PASO 3 - Crear proyecto de prueba en ACC

Luego de haber creado el hub, se necesitará al menos un proyecto con un modelo revit que leer:

1. Entrar a [acc.autodesk.com](https://acc.autodesk.com) e iniciar sesión
2. En la página principal hacer click en **+ Crear Proyecto**
3. Completar el formulario -> **Crear Proyecto**
4. Dentro del proyecto ir a **Archivos**
5. En la raíz (carpeta principal/inicial) -> subir un archivo `.rvt` manualmente
   
> Debido a que se está subiendo manualmente el `.rvt` el ACC no traducirá por su cuenta a `.svf2`, eso lo hará automáticamente el código. Sin embargo, si se abre con revit y se publica desde ahí la traducción se disparará gratis y automáticamente por el ACC. De todas formas, según la fuente del paso anterior por mes se pueden hacer hasta 20 traducciones con código sin costo.

---

## PASO 4 - Crear la app en APS

El script se autentica como una **aplicación APS** usando OAuth2. Necesitas registrar una app para obtener las credenciales.

1. Ir a [aps.autodesk.com](https://aps.autodesk.com) e iniciar sesión con la cuenta de Autodesk
2. Click en **Developer hubs** (costado de la foto de usurio en el encabezado)
3. Click en **Create Application**
4. Dar un nombre (ejemplo -> `aps-application`)
5. Seleccionar **Traditional Web App** luego click en -> **Create**
6. Copiar y guardar el **Client ID** y el **Client Secret**, se necesitarán en el paso 5
7. En **General Settings** -> **Callback URLs** reemplazar la existente por exactamente, tal cual:
   ```
   http://localhost:8080/api/auth/callback
   ```
8. En **API Access** seleccionar las 21 opciones o las que haya para asegurar
9. Click **Save Changes**

> El Client Secret no se debe compartir, si se pierde o filtra de ser necesario se puede regenerar. Estas variables van en el archivo `.env`

---

## PASO 5 - Conectar la app al ACC

Para que la app de APS tenga acceso al ACC se tiene que hacer una integración manual desde el panel de administración en el ACC.

1. Ir a [acc.autodesk.com](https://acc.autodesk.com) -> **Hub Admin**
2. En el menú lateral ir a **Integraciones Personalizadas**
3. Click en **Añadir Integración Personalizada**
4. Completar el **Client ID** (el de la app del paso 4) e ingresar un nombre de la integración -> **Continuar**
5. Ante la advertencia de permiso dar a **Continuar De Todos Modos**
