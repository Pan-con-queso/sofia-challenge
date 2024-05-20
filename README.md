# Parte 1: Data Engineering

Para hacer la parte de data engineering, se divide en 4 partes, las cuales se describen una a una

1. Descarga del archivo
2. Extracción de datos desde el archivo descargado
3. Creación de archivo .csv
4. Guardado de base de datos en SQLite

También se proponen mejoras a este modelo que no se desarrollan por tiempo.

## Descarga desde google drive

El script de descarga es gdrive_downloader.py

Para poder descargar el archivo, se opta por el camino de usar la API de google drive, en particular el código se basa en el [quickstart](https://github.com/googleworkspace/python-samples/blob/main/drive/quickstart/quickstart.py) para poder usar la API. 

Para poder usar la API hay que seguir las [instrucciones](https://developers.google.com/drive/api/quickstart/python?hl=es-419) de la API de google registrarse en Google Developer
- Habilitar la API
- Configurar consentimiento de oAuth credenciales
- Agregar mi correo personal como usuario test de la aplicación para la cual voy a ocupar la API
- Crear un cliente de oAuth 2.0

Las credenciales se guardan en un archivo credentials.json que no he incluido en este repo porque es información sensible.

Las diferencias con el código de ejemplo es que la requests llama a una ruta explícita que es la que nos dieron en el Challenge con el archivo .zip.

## Descomprimir archivo

Para esta parte se utiliza la librería zipFile. el código está en zip_extractor.py y es una aplicación inmediata de la librería.

## Creación de csv

Este código está incluido en build_dataset.py.

Para esto recorremos la carpeta usando pathlib e iterando sobre las carpetas.

Los archivos JSON no son planos puesto que hay llaves cuyos values son otros diccionarios. Se crea una función auxiliar para transformar el json a un diccionario `{columna: valor}` y así poder insertarlo a nuestra base de datos de forma inmediata. 

Para revisar los archivos manipulados por Ziggy, ocupamos `jmespath` para revisar si la llave `name` está presente. Si la busqueda devuelve `None` quiere decir que pertenece a un Perro y no a un humano jeje.

Se usa la librería `tqdm` para poder tener una barra de progreso del recorrido por las carpetas

Para tener un fallback en caso de que falle el programa mientras se ejecuta, se agrega un archivo con extensión .DONE, de tal modo que si se vuelve a ejecutar el código no se ejecuta ningún archivo con esa extensión debido a que ya se procesó.

La función que te devuelve las filas a agregar es un iterador que devuelve una lista ya sea con las columnas o con los valores de las columnas, La función main se ejecuta mientrs este iterador tenga alguna fila por procesar.

## Guardado en base de datos SQLite

Este código está incluido en build_dataset.py junto con la creación del CSV. La Base de datos se guarda en vo2_max_data.db

Se usa la librería sqlite3 para Python y se crea la tabla y se insertan las filas una por una definiendo las queries de forma explícita en texto plano, definiendo el esquema de forma implicita. 

Algunas modificaciones que tuve que hacer fueron:
- Cambiar todos los caracteres especiales de los títulos de las columnas por guiones bajos
- Cambiar los titulos de las columnas que parten con un número debido a que sqlite no las admite.
- Para los valores que son strings, se agregan las comillas explicitamente al crear la consulta de SQLite.

Los valores de las filas que provienen de la iteración se agrupan en un string grande usando un join de python que itera sobre el arreglo. 

Se explicita que la tabla se crea solo si no existe. De modo de evitar que se caiga el código si es que ya habías creado la tabla con anterioridad.

## Evaluación de desempeño

Escribir el csv y la base de datos toma aproximadamente 28 minutos, lo que es un tiempo muy grande para la cantidad de datos. Pero se guardan los 25000 datos perfectamente.

## Posibles mejoras

Podemos ver de inmediato que no tenemos un solo script que englobe todo, sino que tenemos tres. Una mejora sería un programa de python que llame a las 3 funciones secuencialmente para así solo ejecutar un script.

Otras mejoras es que el el esquema de la tabla de SQLite se puede definir de forma explicita y definir llaves primarias y únicas para ver que no se repitan datos, que es un chequeo que no estamos haciendo al momento de insertar datos en la base de datos.

Se pueden evaluar formas de batch inserting para escribir varias lineas a la vez o de forma simultanea para poder ahorrar tiempo, o paralelizar la iteración por las carpetas.

Actualmente el código escribe el archivo .csv desde cero cada vez que se ejecuta, cuando nos gustaría que las lineas nuevas se ejecuten desde el punto en que quedó la iteración por las carpetas. Esto en una segunda iteración hay que arreglarlo porque no queremos perder datos. 

# Parte 2 y 3: Data Modelling

En el jupyter notebook `predictive_modelling.ipynb` se detalla paso a paso el procedimiento seguido para el análisis

# Parte 4: Bonus

Se programan los siguientes scripts:
1. `full_data_divider.py` para dividir la data completa en 25 csvs de 1000 filas cada uno
2. `api.py` API en FastAPI que recibe un csv y devuelve el score logrado 
3. `model.py` Modelo de predicción (Regresión lineal) y lógica para poder reentrenar el modelo
4. `api_test.py` archivo para poder hacer tests de la API

Además, se programa un Dockerfile para poder correr la API en una imagen Docker, y así por ejemplo, subirla a alguna nube de nuestra preferencia como GCP o AWS.