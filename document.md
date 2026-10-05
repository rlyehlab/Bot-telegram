 # Bot de Telegram para recordatorios de donaciones

## Propósito

Desarrollar un bot de Telegram que permita a cada usuario elegir el día del mes en que desea recibir un recordatorio para realizar sus donaciones. El bot guardará las preferencias en PostgreSQL y enviará avisos de forma automática.

## Estado actual

El proyecto cuenta con un prototipo de bot con algunos comandos básicos. La configuración del día de recordatorio, la persistencia funcional y el envío programado aún no están implementados. La inicialización actual de SQLite contiene errores de sintaxis SQL que impiden el arranque normal.


## Requerimientos funcionales

1. **Inicio y registro:** al recibir `/start`, identificar al usuario por su ID de Telegram y crear su registro si aún no existe.
2. **Configuración interactiva:** preguntar qué día del mes desea recibir el aviso. Ofrecer botones o una entrada validada, además de opciones para cambiar la fecha y cancelar.
3. **Persistencia:** almacenar en PostgreSQL el ID de Telegram, el día seleccionado, el próximo aviso, el estado de suscripción y las marcas de creación y actualización.
4. **Envío programado:** localizar los recordatorios vencidos, enviar el mensaje y calcular y guardar el siguiente aviso.
5. **Fechas límite:** para días que no existen en un mes, como el 31 de febrero, enviar el aviso el último día de ese mes. Definir la zona horaria de operación; guardar instantes en UTC y convertir según una zona configurada.
6. **Gestión de suscripción:** permitir consultar o modificar la preferencia y dejar de recibir avisos.
7. **Errores y reintentos:** manejar errores temporales de Telegram y PostgreSQL sin perder avisos ni enviarlos repetidamente.

## Requerimientos no funcionales

- Python con módulos y responsabilidades separadas, manejo explícito de errores y registro de eventos.
- Configuración mediante variables de entorno. No guardar tokens ni contraseñas en el código o en el repositorio.
- Consultas parametrizadas o un ORM; nunca concatenar directamente datos del usuario en SQL.
- Pruebas para validación, cálculo de fechas, persistencia y flujo de notificaciones.
- Envíos idempotentes y acceso seguro a avisos vencidos, incluso si más de una instancia procesa tareas.

## Arquitectura propuesta

- **Presentación:** comandos, mensajes y botones de Telegram.
- **Aplicación:** casos de uso para registrar usuarios, configurar preferencias, cancelar suscripción y procesar recordatorios.
- **Dominio:** reglas de validación y cálculo de fechas, sin depender de Telegram o PostgreSQL.
- **Infraestructura:** adaptador de Telegram, repositorio PostgreSQL, migraciones y planificador.

La solicitud menciona una estructura «C5», pero no define ese estándar. Conviene aclarar su significado para el proyecto. Si se refiere a documentación arquitectónica, C4 (contexto, contenedores, componentes y código) es una opción; no determina por sí mismo la estructura de carpetas. Mantener dependencias dirigidas hacia el dominio y separar las responsabilidades.

## Modelo de datos inicial

Tabla `users` propuesta:

- `id`: clave primaria interna.
- `telegram_id`: identificador único de Telegram, obligatorio.
- `reminder_day`: día solicitado, entre 1 y 31.
- `next_reminder_at`: instante del siguiente recordatorio.
- `is_subscribed`: indica si se deben enviar mensajes.
- `created_at` y `updated_at`: marcas de tiempo.

Crear un índice que permita buscar usuarios suscritos con avisos vencidos. Si se requiere auditoría de entregas, añadir una tabla de envíos con estado e identificador de idempotencia.

## PostgreSQL y migraciones

- Centralizar la configuración y el ciclo de vida de conexiones o sesiones, con tiempos de espera y reintentos limitados.
- Usar una herramienta de migraciones, por ejemplo Alembic si se elige SQLAlchemy.
- Crear una migración inicial con la tabla, restricciones e índices.
- Ejecutar las migraciones explícitamente durante el despliegue antes de iniciar el bot; no depender de la creación automática de tablas al arrancar.

## Docker y Docker Compose

- Crear un `Dockerfile` con una imagen oficial de Python, dependencias fijadas, usuario no privilegiado y comando de inicio documentado.
- Crear `compose.yaml` con servicios para el bot y PostgreSQL, red interna y volumen persistente para la base de datos.
- Configurar token y credenciales mediante entorno o un `.env` excluido del control de versiones; no incluir secretos reales en Compose.
- Añadir healthcheck a PostgreSQL y hacer que el bot espere a que la base esté lista. `depends_on` por sí solo no garantiza que acepte conexiones.
- Documentar construcción, inicio, migraciones, consulta de logs y apagado.

## Código implementado

- `bot.py` carga variables desde `.env`, obtiene `TOKEN`, intenta inicializar la base y registra los comandos `/guardaruser`, `/tuinfo`, `/escribirAtodos`, `/start`, `/ayuda` y `/mostrarusuarios`. Luego inicia el polling.
- `src/handlers/commands.py` contiene respuestas básicas para esos comandos, además de una función `reply` que no está registrada actualmente.
- La lista de usuarios de `guardaruser` y `mostrarusuarios` vive solo en memoria, por lo que se pierde al reiniciar el proceso. `escribirAtodos` recorre esa lista, pero envía el texto fijo `example` en vez del argumento del comando.
- `src/database/db.py` intenta crear una tabla SQLite `usuarios` con datos básicos del usuario. La sentencia usa `IF NOT EXIST` y `UINIQUE`, por lo que falla al ejecutarse; por eso la inicialización llamada desde `bot.py` no es funcional.
- `requirements.txt` incluye `python-telegram-bot==22.8`. El código también importa `dotenv`, pero `python-dotenv` no está declarado en ese archivo.
- Los archivos `src/keyboards/menu.py`, `src/keyboards/botones.py`, `src/handlers/start.py`, `src/handlers/mensajes.py`, `src/handlers/ayuda.py`, `src/handlers/admin.py` y `src/handlers/__init__.py` están vacíos.
- Se anotó como decisión de producto la zona horaria de Buenos Aires y limitar los días elegibles del 1 al 27, pero esas reglas todavía no están aplicadas en el código. Tampoco se definió una política de reintentos.

## Código por implementar

- Corregir la inicialización de base de datos y decidir e implementar la persistencia requerida en PostgreSQL, incluyendo modelo, restricciones y migraciones.
- Implementar el registro persistente desde `/start`, la selección y validación interactiva del día, la modificación de la preferencia y la baja de suscripción.
- Implementar el cálculo del próximo aviso en la zona horaria configurada, el planificador mensual y el envío real del recordatorio.
- Añadir control de reintentos, manejo de errores e idempotencia para evitar perder o duplicar avisos.
- Completar la configuración del proyecto: asegurar que los imports desde `src` funcionen al ejecutar `bot.py` y declarar las dependencias importadas, incluida `python-dotenv`.
- Añadir pruebas unitarias y de integración, y crear y validar `Dockerfile` y `compose.yaml`.
- Documentar configuración, ejecución, despliegue y recuperación ante fallos.

## Tareas por hacer

- [x] Revisar el código y registrar su estado, estructura y dependencias actuales.
- [ ] Elegir y documentar la biblioteca de Telegram, el acceso a datos y la herramienta de migraciones.
    - Biblioteca de Telegram presente: `python-telegram-bot==22.8`.
    - Hay un intento de acceso a SQLite, pero el requisito del proyecto es PostgreSQL; no se eligió ni implementó una herramienta de migraciones.
- [ ] Definir la zona horaria, la regla para días inexistentes y la política de reintentos.
    - Decisiones anotadas: zona horaria de Buenos Aires y días permitidos del 1 al 27 de cada mes.
    - Falta definir la política de reintentos; las decisiones anotadas aún no están implementadas en el código.
- [ ] Implementar registro, configuración interactiva, actualización y baja.
- [ ] Implementar conexión a PostgreSQL, modelo y migración inicial.
- [ ] Implementar planificador mensual y protección frente a avisos duplicados.
- [ ] Añadir pruebas unitarias y de integración.
- [ ] Crear y probar `Dockerfile` y `compose.yaml`, incluida la persistencia y los healthchecks.
- [ ] Documentar configuración, ejecución, despliegue y recuperación ante fallos.
