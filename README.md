# Sistema de Gestión de Escenarios Deportivos

Aplicación desarrollada en **Python** para gestionar información de escenarios deportivos utilizando **MongoDB**, con funcionalidades CRUD y generación de gráficos a partir de los datos almacenados.

## Descripción

El sistema permite administrar registros de escenarios deportivos mediante una base de datos MongoDB.

Los datos iniciales se cargan desde un archivo CSV y posteriormente pueden ser creados, consultados, actualizados o eliminados desde el menú de la aplicación.

También permite generar visualizaciones para analizar la distribución de los escenarios deportivos según su tipo y ubicación.

## Tecnologías

* Python
* MongoDB
* PyMongo
* Matplotlib
* CSV

## Funcionalidades

* Carga de datos desde archivos CSV hacia MongoDB.
* Creación de nuevos escenarios deportivos.
* Consulta de escenarios almacenados.
* Actualización de registros.
* Eliminación de registros.
* Manejo de coordenadas geográficas.
* Agrupación de datos mediante operaciones de agregación de MongoDB.
* Generación de gráficos con Matplotlib.
* Análisis de escenarios por tipo y ubicación.

## Estructura

* `app.py` — lógica principal de la aplicación, conexión con MongoDB, operaciones CRUD y generación de gráficos.
* `escenarios_deportivos.csv` — conjunto de datos utilizado para cargar los escenarios deportivos.
* `grafico_escenarios.png` — ejemplo de una visualización generada por la aplicación.

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/Gabytoppers/CRUD-con-una-base-de-datos-abiertos.git
cd CRUD-con-una-base-de-datos-abiertos
```

Instala las dependencias:

```bash
pip install pymongo matplotlib
```

Asegúrate de tener **MongoDB ejecutándose localmente** en el puerto `27017`.

Ejecuta la aplicación:

```bash
python app.py
```

Al iniciar, el sistema carga los datos del archivo CSV en MongoDB y posteriormente muestra el menú principal de gestión.
