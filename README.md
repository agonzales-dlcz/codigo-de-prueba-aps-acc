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

---

## I - PRERREQUISITOS

### 0.1 - Instalar Python

**Si ya se tiene python instalado saltarse este paso, verificar con el paso [0.2]**

Descargar Python de preferencia una version estable como la (Version 3.12.9) [https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe](https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe)

> En la instalación, marcar ambos check **"Use admin privileges when installing py.exe"** (instala python para todo el sistema no solo para el usuario, evita problemas de permisos al intalar dependencias como `pip`) y **"Add Python to PATH"** (agrega python a las variables de entorno del sistema) antes de hacer clic en **Install Now**. Si no se hizo se puede volver a instalar y añadir el check.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/python_instalar.png" alt="instalador de python" width="600" />
</p>

> Por último, en **"Disable path length limit"** (si se tiene un nombre de usuario muy largo).

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/instalador_python_path_length_limit.png" alt="instalador de python" width="600" />
</p>

### 0.2 - Verificar las variables de entorno

Abrir una terminal nueva y ejecutar -> Win + R -> `cmd` -> Enter:

```cmd
python --version
pip --version
```

> Si el comando no se reconoce, cerrar y volveer a abrir la terminal —> los cambios al PATH no se aplican a sesiones ya abiertas.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/version_python.png" alt="cmd_version" width="600" />
</p>

### 0.3 - Instalar dependencias
1. Abrir la **consola de windows** -> Win + R -> `cmd` -> Enter
2. Para para este caso es necesario tener dotenv

```bash
pip install python-dotenv
```
<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/dotenvinstall.png" alt="cmd_version" width="600" />
</p>

3. Si se necesitara otra dependencia el proceso es el mismo

```bash
pip install reemplazar-por-nombre-de-dependencia
```
---

## II - INFRAESTRUCTURA AUTODESK

## PASO 1 - Obtener una cuenta con suscripción activa

En caso de no tener una suscripcion, se puede obtener una temporal (30 días) con un correo personal o un nuevo correo temporal

### 1.1 - Crear cuenta Autodesk personal

1. En [autodesk.com](https://www.autodesk.com) -> En la esquina superior derecha -> **Sign In -> Create Account**
2. Completar los datos personales.

> En el ejemplo se usó un correo temporal de un solo uso (desaparece al cerrar la ventana) pero es mejor usar un correo secundario o crearse un correo como tal para que la sesión se pueda abrir otra vez.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_usurario_autodesk.png" alt="cmd_version" width="1000" />
</p>

4. **Importante** se tiene que usar un correo (gmail, etc) que no tenga una versión de prueba anterior ya caducada esto se activará en los pasos 1.2 y 1.4, si el correo ya se ha usado antes y su licencia temporal ya está caducada no se podrá crear el la application en el paso 4
5. Verificar el correo y completar el registro

> La cuenta Autodesk creada sirve tanto para APS como para el ACC, esto se puede hacer indefinidamente claro que el correo siempre tendrá que ser uno nuevo.

### 1.2 - Activar la versión de prueba del ACC

1. Entrar a [https://construction.autodesk.com/trial/autodesk-build/](https://construction.autodesk.com/trial/autodesk-build/)

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/acc_version_de_prueba.png" alt="cmd_version" width="1000" />
</p>

2. Completar el formulario.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/acc_version_de_prueba_1.png" alt="cmd_version" width="1000" />
</p>

3. Al terminar es redirigido a la cuenta ACC nueva con rol de **Admin Account** (es necesario contar con este rol)

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/acc_version_de_prueba_2.png" alt="cmd_version" width="1000" />
</p>

### 1.3 - Activar la versión de prueba del APS

1. Ir a [aps.autodesk.com/pricing](https://www.autodesk.com/products/autodesk-platform-services/overview#pricing)
2. Seleccionar **Free -> Check Out** completar el registro para esto mejor escojer **(View on local site)**, pide tarjeta, la compra vale 0.00$.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/aps_version_prueba.png" alt="cmd_version" width="1000" />
</p>

3. Luego de completar una dirección válida **Continuar**, en RESUMEN DEL PEDIDO -> **Continuar con el pago**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/aps_version_prueba11.png" alt="cmd_version" width="1000" />
</p>

4. Completar los datos de la tarjeta y dar a **Comprar ahora**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/aps_version_prueba2.png" alt="cmd_version" width="1000" />
</p>

> APS llega a cobrar si se excede el límite mensual de uso de ciertas APIs, sin embargo, eso no es restrictivo para este caso (ver notas del paso 2)

---

## PASO 2 - Crear HUB

El código toma la información de modelos en la nube. Para eso se debe crear un **Hub gratuito** que almacene proyectos y modelos:

1. Ir [manage.autodesk.com](https://manage.autodesk.com) e iniciar sesión, si se acaba de crear la cuenta el link te manda al paso 2.
2. Click en la cinta **Products and Services -> Hubs**
3. Click en **Create Hub -> APS Developer Hub**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/aps_hub.png" alt="cmd_version" width="1000" />
</p>

5. Dar un nombre luego a **Create & Activate**
6. El nuevo Hub aparecerá en la lista inferior

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

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_proyecto_prueba.png" alt="cmd_version" width="1000" />
</p>

4. Completar el formulario -> **Crear Proyecto**
5. Dentro del proyecto ir a **Archivos**
6. Subir los archivos `.rvt` manualmente

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_proyecto_prueba1.png" alt="cmd_version" width="1000" />
</p>
   
> Debido a que se está subiendo manualmente el `.rvt` el ACC no traducirá por su cuenta a `.svf2`, eso lo hará automáticamente el código. Sin embargo, si se abre con revit y se publica desde ahí la traducción se disparará gratis y automáticamente por el ACC. De todas formas, según la fuente del paso anterior por mes se pueden hacer hasta 20 traducciones con código sin costo.

---

## PASO 4 - Crear la app en APS

El script se autentica como una **aplicación APS** usando OAuth2. Necesitas registrar una app para obtener las credenciales.

1. Ir a [aps.autodesk.com](https://aps.autodesk.com) e iniciar sesión con la cuenta de Autodesk
2. Click en **Developer hubs** (costado de la foto de usurio en el encabezado)
3. Click en **Create Application**
4. Dar un nombre (ejemplo -> `aps-application`)
5. Seleccionar **Traditional Web App** luego click en -> **Create**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_applicacion.png" alt="cmd_version" width="600" />
</p>

6. Copiar y guardar el **Client ID** y el **Client Secret**, se necesitarán en el paso 5

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_applicacion1.png" alt="cmd_version" width="1000" />
</p>

7. En **General Settings** -> **Callback URLs** reemplazar la existente por exactamente, tal cual:
   ```
   http://localhost:8080/api/auth/callback
   ```
8. En **API Access** seleccionar las 21 opciones o las que haya para asegurar
9. Click **Save Changes**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/crear_applicacion2.png" alt="cmd_version" width="1000" />
</p>

> El Client Secret no se debe compartir, si se pierde o filtra de ser necesario se puede regenerar. Estas variables van en el archivo `.env`

---

## PASO 5 - Conectar la app al ACC

Para que la app de APS tenga acceso al ACC se tiene que hacer una integración manual desde el panel de administración en el ACC.

1. Ir a [acc.autodesk.com](https://acc.autodesk.com) -> **Hub Admin**
2. En el menú lateral ir a **Integraciones Personalizadas**
3. Click en **Añadir Integración Personalizada**
4. Completar el **Client ID** (el de la app del paso 4 [punto 6]) e ingresar un nombre de la integración -> **Continuar**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/conectar_applicacion.png" alt="cmd_version" width="1000" />
</p>

5. Ante la advertencia de permiso dar a **Continuar De Todos Modos**

---

## III - CÓDIGO

## PASO 6 - Descargar el repositorio

1. Ir a la carpeta donde se descargará la carpeta **codigo-de-prueba-aps-acc** con todos los archivos del repositorio y abrir la **consola de windows**, Win + R, `cmd` desde ahí.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/clonar_repositorio.png" alt="cmd_version" width="1000" />
</p>

2. Para clonar el repositorio, pegar en la consola:

```bash
git clone https://github.com/agonzales-dlcz/codigo-de-prueba-aps-acc.git
```

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/clonar_repositorio1.png" alt="cmd_version" width="1000" />
</p>

---

## PASO 7 - Configuración

1. Dentro de la carpeta **codigo-de-prueba-aps-acc** descargada crear un nuevo archivo documento de text txt pero guardarlo con el nombre **.env** (tal cual) desde donde se leeran las credenciales para la autentificación

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/configurar_app.png" alt="cmd_version" width="1000" />
</p>

2. Editar el contenido con el Client Id y Client Secret Id de la app del paso 4 [punto 6], despues del '=', sin comillas ni espacios:

```env
APS_CLIENT_ID=CLIENT_ID_DE_LA_APP_REEMPLAZAR
APS_CLIENT_SECRET=CLIENT_SECRET_DE_LA_APP_REEMPLAZAR
APS_CALLBACK_URL=http://localhost:8080/api/auth/callback
```

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/configurar_app1.png" alt="cmd_version" width="1000" />
</p>

> Sin las credenciales del cliente, la aplicación no obtendrá el permiso para acceder al ACC

3. En el archivo `extractor.py`, línea 5 -> en la lista, agregar o quitar los parámetros que se quieran exportar.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/configurar_app2.png" alt="cmd_version" width="1000" />
</p>

---

## PASO 8 - Ejecutar

1. En la misma carpeta, abrir nuevamente la **consola de windows**, Win + R, `cmd` (como en el Paso 6 [punto 1].
2. Ejecutar:

```bash
python main.py
```

3. El script abre el login de Autodesk -> iniciar sesión con la **misma cuenta** que tiene acceso al ACC, se mostrarán los permisos solicitados -> Click en **Permitir**

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/main_run.png" alt="cmd_version" width="1000" />
</p>

4. Finalmente, los resultados se exportan y abren automática en un `.csv` en la carpeta `resultados` con el nombre del `extraccion + dia de exportación_hora de exportación + .csv`. Al hacer una tabla de los datos se tienen los valores para compartir.

<p align="center">
  <img src="https://github.com/agonzales-dlcz/icons/blob/main/imagenes/resultados.png" alt="cmd_version" width="1000" />
</p>

---
