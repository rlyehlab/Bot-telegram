# Bot de Telegram para recordatorios de donaciones

Bot de Telegram en desarrollo para ayudar a recordar donaciones mensuales. El objetivo es que cada usuario pueda elegir un día del mes y recibir un mensaje de recordatorio automáticamente.

> **Estado:** prototipo inicial. Los comandos disponibles son básicos; la configuración de recordatorios y el envío programado todavía no están implementados. La persistencia que se está intentando usar es SQLite, aunque el diseño previsto del proyecto requiere PostgreSQL.

## Lineamientos generales

- Mantener separadas las responsabilidades de comandos, lógica de aplicación, reglas del dominio y acceso a datos.
- Guardar tokens y credenciales en variables de entorno. No incluirlos en el código ni subir archivos `.env` al repositorio.
- Validar los datos recibidos antes de guardarlos o usarlos.
- Usar consultas parametrizadas al trabajar con bases de datos.
- Registrar errores de forma que ayuden a diagnosticar problemas sin exponer secretos.
- Añadir pruebas para cambios de lógica, persistencia y notificaciones.
- La zona horaria prevista es `America/Argentina/Buenos_Aires`. La regla anotada para la selección de días es del 1 al 27 de cada mes; ambas deben implementarse y probarse.
- La estructura y el estado detallado del proyecto están descritos en [document.md](document.md).

## Requisitos

- Python 3.
- Una cuenta/bot de Telegram y su token, creado mediante [@BotFather](https://t.me/BotFather).
- Para ejecutar los comandos de Docker: Docker Desktop (Windows/macOS) o Docker Engine y el complemento Docker Compose.

## Comandos

Estos son los comandos registrados actualmente por `bot.py`:

| Comando | Qué realiza actualmente |
| --- | --- |
| `/start` | Responde `Helloworld.`. No registra al usuario ni configura recordatorios todavía. |
| `/ayuda` | Muestra una lista de los comandos del bot. |
| `/tuinfo` | Responde con el ID de Telegram, nombre y nombre de usuario del usuario que lo invoca. |
| `/guardaruser` | Añade el ID del usuario a una lista en memoria. La lista se pierde al reiniciar el bot. |
| `/mostrarusuarios` | Muestra los IDs añadidos a esa lista en memoria, o informa que está vacía. |
| `/escribirAtodos` | Recorre la lista en memoria e intenta enviar un mensaje a cada ID. Actualmente manda el texto fijo `example`; no utiliza el texto que se pase al comando. |

Los comandos de gestión de usuarios no constituyen todavía un sistema de suscripciones ni una función de difusión lista para producción.

## Entorno virtual e instalación

Desde PowerShell, abre la carpeta del repositorio y crea el entorno virtual:

```powershell
py -m venv .venv
```

Actívalo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell informa que la ejecución de scripts está deshabilitada, permite la activación solo en la ventana actual y vuelve a ejecutar el comando:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias declaradas:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```






## Configuración y ejecución del bot

1. Crea un archivo `.env` en la carpeta raíz del proyecto (junto a `bot.py`) con el token de tu bot:

   ```dotenv
   TOKEN=pega_aqui_el_token_de_telegram
   ```

2. No compartas ni subas el archivo `.env`. El `.gitignore` del proyecto ya lo excluye.
3. Activa el entorno virtual e instala las dependencias siguiendo la sección anterior.
4. Desde la raíz del repositorio, ejecuta:

   ```powershell
   python bot.py
   ```

   Detén el proceso con `Ctrl+C`.

> **Limitación conocida:** en el estado actual, la ejecución puede fallar antes de iniciar. `bot.py` importa módulos como `database.db` y `handlers.commands`, pero esos módulos están dentro de `src`; además, la sentencia SQL de inicialización de SQLite tiene errores. Es necesario corregir estos problemas y declarar `python-dotenv` en `requirements.txt` para que el arranque sea reproducible.

## Docker

El repositorio todavía no está listo para ejecutar el bot con Docker: no hay un `Dockerfile` y `docker-compose.yaml` está vacío. Además, el arranque del bot tiene los problemas descritos arriba. Primero hay que crear y probar la imagen y configurar el servicio (y PostgreSQL cuando se implemente esa integración).

Una vez que exista un `Dockerfile` válido en la raíz, se podrá construir y ejecutar la imagen con:

```powershell
docker build -t bot-telegram .
docker run --rm --env-file .env bot-telegram
```

Cuando `docker-compose.yaml` esté configurado con el servicio del bot, se podrá iniciar en segundo plano con:

```powershell
docker compose up --build -d
```

Comandos útiles para ese despliegue:

```powershell
docker compose logs -f
docker compose down
```

`docker compose down` detiene y elimina los contenedores del proyecto. Si se agrega una base de datos con volumen persistente, evita usar `docker compose down -v` salvo que quieras eliminar también los datos almacenados.

No incluyas el token en el `Dockerfile` ni en el archivo Compose. Pásalo mediante variables de entorno o un archivo `.env` local excluido del control de versiones.

## Convenciones de commits

Usar el formato **Conventional Commits**:

```text
<tipo>(<alcance opcional>): <resumen en imperativo>
```

Tipos recomendados:

- `feat`: una funcionalidad nueva.
- `fix`: corrección de un error.
- `docs`: cambios en documentación.
- `refactor`: reestructuración sin cambiar el comportamiento esperado.
- `test`: incorporación o modificación de pruebas.
- `chore`: mantenimiento, dependencias o tareas auxiliares.

Ejemplos:

```text
feat(comandos): agregar configuración del día de recordatorio
fix(database): corregir inicialización de la tabla de usuarios
docs(readme): documentar instalación y comandos
test(recordatorios): cubrir el cálculo de la próxima fecha
```

Escribir resúmenes breves y concretos; un commit debe representar un cambio coherente. No incluir tokens, contraseñas ni otros secretos en un commit.