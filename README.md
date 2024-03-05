

## ST0263 TOPICOS ESPEC. EN TELEMATICA
##
## Estudiante(s): Carla Sofía Rendón Baliero, csrendonb@eafit.edu.co
##
## Profesor: Alvaro Enrique Ospina Sanjuan
##


#  P2P - Comunicación entre procesos mediante API REST, RPC
#
# 1. Descripción de la actividad
#
El presente proyecto tiene como objetivo diseñar e implementar un sistema P2P para la comunicación entre procesos, utilizando API REST y gRPC. Cada nodo en la red P2P alberga microservicios que facilitan un sistema de compartición de archivos distribuido.
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor
### Comunicación REST (Flask):
- Se ha implementado un servidor Flask (server.py) que actúa como la interfaz REST para el sistema P2P.
- Los endpoints /login, /logout, y /indexFiles han sido creados para gestionar el inicio de sesión, cierre de sesión, e indexación de archivos respectivamente mediante métodos POST y GET.
- Se utilizan modelos de datos (NodeModel y IndexationModel) para almacenar información sobre los nodos.
### Comunicación gRPC
- Se ha implementado un servicio gRPC Pclient y Pserver, que aprovechan la comunicación gRPC para coordinar las operaciones entre nodos.
### Persistencia de Datos
- Se utiliza SQLAlchemy a través de SQLAlchemy para la persistencia de datos.
- La información sobre los nodos y la indexación de archivos se almacena en la base de datos.

### Sistema P2P
- El sistema P2P permite a los nodos iniciar y cerrar sesión, compartir información sobre archivos a través de la indexación, y buscar recursos en la red.
- La persistencia de datos se logra con una base de datos SQLAlchemy, brindando estabilidad a la información sobre nodos y recursos en la red P2P
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor 
- Despliegue en AWS
- Manejo de algunos errores
- Mejorar el upload y el download


# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
### Arquitectura del Sistema
La arquitectura del sistema es una red P2P no estructurada basada en un servidor de Directorio y Localización. En este modelo, los nodos tienen la capacidad de establecer conexiones directas entre sí, manteniendo así la naturaleza descentralizada característica de las redes P2P. La introducción del servidor central facilita ciertas funciones especializadas, como la búsqueda eficiente de archivos en la red.

Un aspecto importante que refuerza la no estructuración de la red es la implementación del servicio de búsqueda de archivos. Este servicio filtra los nodos que están activos ('up'), selecciona el primero de este conjunto filtrado y realiza la conexión. La elección del nodo se organiza aleatoriamente entre los nodos 'up' disponibles, aportando un elemento de descentralización y variabilidad en la selección de pares. Este enfoque no estructurado permite a los nodos conectarse de manera dinámica y eficiente, adaptándose a la naturaleza cambiante de la red sin depender de una topología predefinida.

La razón principal de usar este tipo de arquitectura no estructurada se debe a lo siguiente:
- **Se espera que la red tenga un número pequeño de usuarios:** El número de usuarios en la red estará limitado por el número de estudiantes que participan en el reto.
- **Los requisitos de seguridad no son altos:** La red no necesita ser altamente segura, ya que solo es un reto inicial.
- **No hay transferencia real de archivos** .

![ImagenArquitectura](https://github.com/csofia1408/csrendonb-st0263/blob/main/Arquitectura.png)

### Patrones
- Patrón MVC "Modelo Vista Controlador":La estructura del código refleja la separación de responsabilidades en términos de modelo (persistencia de datos con SQLAlchemy), vista (interfaz de usuario y servicios REST), y controlador (lógica de negocio y servicios gRPC).
- Patrón DAO "Data Access Object": SQLAlchemy se utiliza para interactuar con la base de datos SQLAlchemy, siguiendo el patrón DAO para separar la lógica de acceso a datos del resto del código.

###  Mejores prácticas utilizadas
- Persistencia de Datos: Se utiliza una base de datos SQLAlchemy para garantizar la persistencia de la información sobre nodos y archivos indexados.
- Menú modular:Permite que los usuarios accedan fácilmente a las funciones del sistema mediante opciones numeradas, no solo mejora la usabilidad del sistema, sino que también proporciona una estructura clara y escalable para futuras expansiones
- Separación de Responsabilidades: El código sigue el principio de separación de responsabilidades, donde cada componente tiene una función clara y específica.
- Comunicación Eficiente:La elección de gRPC como middleware para la comunicación entre nodos permite una transferencia eficiente de mensajes y soporta la concurrencia.
- Manejo de Concurrency:Cada microservicio PServidor debe la concurrencia, permitiendo que más de un proceso remoto se comunique simultáneamente.


# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

### Descripción
El proyecto se desarrolla en Python, utilizando Flask para la implementación del servidor REST y gRPC, y SQLAlchemy para la interacción con la base de datos SQLAlchemy. La versión de Python es la 3.8.5. Además, se emplea gRPC para la comunicación entre nodos, con el archivo de definición de servicio definido en proto3.

## Como se compila y ejecuta.
- P2P Server (Flask):
    - Ejecutar server.py.
    - El servidor se inicia en http://127.0.0.1:5000.

- P2P Client (gRPC):
    - Ejecutar peer.py <username> <port>
    - Se inicia un servidor gRPC en el puerto especificado, y el cliente se presenta con un menú interactivo para acceder a las funciones del sistema.
    - Menu:
        1. Login
        2. Logout
        3. Index files
        4. Search files


## Detalles del desarrollo.
- **Base de Datos (SQLAlchemy):** El código utiliza SQLAlchemy como sistema de gestión de bases de datos. La base de datos contiene el directorio donde esta la información sobre los nodos/peers
`(NodeModel(username=args.username, password=args.  password, state="up", url=args.url)`
- **Métodos del `server.py`:**
    - **`AddNode`:** Este método maneja la creación o actualización de un nodo en la base de datos cuando un peer inicia sesión (`POST /login`). Verifica si el nodo ya existe, y si es así, actualiza su estado a "up". Si no existe, crea un nuevo nodo.
    - **`logoutPeer`:** Gestiona el cierre de sesión de un peer (`POST /logout`). Cambia el estado del nodo a "down" para indicar que el peer se ha desconectado.
    - **`indexFiles`:** Administra la indexación de titulos  de los archivos por parte de un peer (`POST /indexFiles`). Crea o actualiza la información de indexación para un peer dado.

### Métodos en peer.py:

- **`NodeService` (gRPC):** Implementa el servicio gRPC que maneja la comunicación entre nodos. El método `SendMessage` procesa los mensajes enviados desde un peer a otro.
- **`downloading_uploading` (gRPC):** Se conecta a otro peer usando gRPC para enviar un mensaje (`downloading_uploading`). Usado en la descarga y carga de archivos entre peers.
- **`Pclient` (Cliente Peer):**
    - **`run`:** El método principal que inicia la ejecución del cliente peer. Proporciona un menú interactivo para que el usuario (peer) realice acciones como iniciar sesión, cerrar sesión, indexar archivos y buscar archivos.
    - El cliente interactúa con un servidor web (API REST) para realizar operaciones como iniciar sesión, cerrar sesión, indexar archivos y buscar archivos.
    - **`run_submenu`:** Muestra un submenú para opciones adicionales en caso de que el usuario desee expandir funcionalidades en el futuro.
- **`Pserver` (Servidor Peer):**
    - **Inicio del servidor:** Configura y ejecuta el servidor gRPC para manejar las comunicaciones entre peers.
    - La función downloading_uploading utiliza un canal gRPC para comunicarse con otro par (peer).
    - Se instancia un cliente gRPC (NodeServiceStub) y se utiliza para invocar los métodos SendDownload o SendUpload según el parámetro.

### Detalles técnicos
#### Librerías y Paquetes Principales:

- Flask (Versión 2.0.1) para el servidor REST.
- Flask-RESTful (Versión 0.3.9) para facilitar la creación de servicios RESTful.
- Flask-SQLAlchemy (Versión 2.5) para la interacción con la base de datos.
- gRPCio (Versión 1.39.0) para la comunicación gRPC.
- En el archivo requirements.txt, se encuentran todos los paquetes.
    
#### Parámetros del Proyecto:
En peer.py, los parámetros <name> y <port> deben proporcionarse al ejecutar el script. <name> representa el nombre del nodo/peer, y <port> especifica el puerto del servidor gRPC.

#### Configuración de Flask:
El servidor Flask se configura en server.py. Los detalles de configuración, como la dirección IP y el puerto de escucha, se pueden modificar en este archivo.

#### Base de Datos:
La base de datos SQLAlchemy se configura en server.py mediante SQLAlchemy. El archivo database.db contiene la base de datos y se crea automáticamente al ejecutar el servidor.

#### Organización del Código
![teer](https://github.com/csofia1408/csrendonb-st0263/blob/main/OrganizaciónCarpetas.png)

Archivos Significativos:
- server.py: Implementación del servidor Flask y definición de servicios REST.
- peer.py: Implementación del cliente P2P, que incluye la lógica de menú y la inicialización del servidor gRPC.

#### Organización de Carpetas


## una mini guia de como un usuario utilizaría el software o la aplicación

### 1. Iniciar el Servidor de Directorio y Localización :

- Antes de comenzar cualquier interacción, asegúrese de haber ejecutado el servidor peer ejecutando el script server.py
- Este servidor actúa como el punto central para la red P2P y permite la comunicación entre los pares.

### 2. Iniciar el Peer:

- Una vez que el servidor está en funcionamiento, abra un nuevo terminal y ejecute el cliente peer con el script peer.py: python peer.py <UsernameDeLaPeer> <puerto>.

### 3. Menú de Acciones:

Al iniciar el cliente, se presentará un menú interactivo con opciones como:

1. Login: Iniciar sesión en la red P2P.

2. Logout: Cerrar sesión y desconectarse de la red.

3. Index Files: Indexar titulos de archivos locales para compartir información.

4. Search Files: Buscar archivos disponibles en la red.

4. Iniciar Sesión (Login):

- Seleccione la opción '1' en el menú e ingrese su contraseña cuando se le solicite.
- El cliente se conectará a la red P2P ,estado: up.

5. Cerrar Sesión (Logout):

- Seleccione la opción '2' en el menú para cerrar sesión y desconectarse de la red.
- El cliente informará que ha cerrado sesión ,estado : down.

6. Indexar Archivos:

- Seleccione la opción '3' e ingrese una lista de titulos de archivos separados por comas cuando se le solicite.
- El cliente enviará la información de indexación al servidor para compartirla la ubicación con otros pares.

7. Buscar Archivos:

- Seleccione la opción '4' e ingrese el nombre de archivo que desea buscar.
- El cliente consultará a otros pares y mostrará la información de un par disponible que tiene el archivo.
- Se enviará un mensaje a la otra peer con el archivo, solicitando su carga, una vez cargado.
- El archivo se descargará y se agregará al directorio, actualizando la información de archivos de esa peer.

# 5. otra información que considere relevante para esta actividad.
Hay algunas consideraciones adicionales que podrían ser relevantes para mejorar y expandir el proyecto como:
 - Seguridad: Implementar medidas de autenticación y autorización para garantizar el acceso solo a peers autorizados.

- Manejo de Errores: Mejorar la gestión de errores para proporcionar mensajes más descriptivos y manejar situaciones excepcionales de manera más robusta.

- Escalabilidad: Adaptar la implementación para manejar entornos más grandes, abordando cuestiones como la eficiencia de la base de datos y la optimización de operaciones de red

# referencias:
GRPC :https://aws.amazon.com/es/compare/the-difference-between-grpc-and-rest/
Introducción a las redes P2P: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwj8l__ssNyEAxXStYQIHZKNCNcQFnoECDEQAQ&url=https%3A%2F%2Facademy.binance.com%2Fes%2Farticles%2Fpeer-to-peer-networks-explained&usg=AOvVaw1bnPDg4OMuV-Q_MXY9Jqk_&opi=89978449
Tutorial de Flask: https://www.tutorialspoint.com/flask/index.htm
Documentación de gRPC: https://grpc.io/docs/
Tutorial de SQLAlchemy: https://www.tutorialspoint.com/sqlalchemy/index.htm
Python: https://www.python.org/
Flask: https://flask.palletsprojects.com/
Flask-RESTful: https://flask-restful.readthedocs.io/
Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
gRPC: https://grpc.io/
