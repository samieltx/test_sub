# tienda-amiga-exams
El proyecto consiste en un ETL que consume datos de noticias mediante la libreria de `GoogleNews`. 

Recordar clonarse el repositorio de la branch `data-eng-exams`

## Requisitos para ejecutar el proyecto.
1. Tener instalado Docker
2. Tener python >=3.8 y <3.10.
3. Tener instalado Poetry para instalar el python environment de este proyecto. Recomendamos una versión >=1.3 y <1.4.

## Configuracion local del repositorio
1. Tener instalado Poetry >=1.3 y <1.4.
2. Ejecutar:
```
poetry install
```
3. Al hacer `poetry shell` podremos acceder a nuestro python environment con nuestras dependencias definidas en `pyproject.toml`.

## Como reproducir el proyecto
1. Ir a la carpeta `docker` el cual contiene los archivos de configuracion de los servicios a desplegar (Airflow y postgres).
2. Para levantar los servicios ejecutar:
```
docker compose --env-file ../.env up
```

Esto debería buildear una imagen de docker llamada `tienda-amiga-playground_base` (ver `Dockerfile`) por ser la primera vez y luego se levantaran los servicios definidos en `docker-compose.yaml`.

3. Una vez levantados los servicios es posible ingresar a los containers con el comando `docker exec` o a los distintos servicios mediante el puerto definido de salida.
En el caso de postgres dejaremos un comando útil de referencia para poder acceder a la consola de Postgres de forma remota.
Para acceder a la UI de Airflow directamente ingresar a http://localhost:2023/ para ver el DAG de ejemplo para este proyecto.

## Consignas

Para el desarrollo del examen se pide:
1. Armar otro ETL con alguna keyword de interés (por ejemplo `bitcoin`).
2. En la función de transformacion, limpiar los campos innecesarios, transformar otros para dejar sólo información relevante, etc. El resultado final debería ser un dataset mucho más limpio que el extraído inicialmente por `extract.py`
3. Agregar como columna el tiempo de procesamiento del DAG en el dataframe (hint: se puede usar el context de Airflow es posible obtener el campo `logical_date`).
4. Insertar el dataset final (incluido este nuevo campo) a la base de datos destino (`load.py`).
5. Actualmente los DAGs no tienen un `schedule` definido, agregarle una periodicidad para que corra cada 3 horas todos los dias menos los Domingos (hint: usar https://crontab.guru/).
6. Crear un DAG que se ejecute todos los dias a las 4AM UTC y que realice un logging (tipo print) de las palabras más usadas en cada keyword buscada para las ultimas 12 horas de búsqueda.

## Consejos útiles
Algunos comandos/consejos útiles:

1. Para poder acceder a la base de datos de forma remota
```bash
docker exec -it ta-playground-airflow-scheduler poetry run pgcli -h postgres-db -U tiendaamiga -d tiendaamiga_db
```

Puede ser útil para tirar queries tipo `SELECT` o para droppear alguna tabla en caso de ser necesario.

2. Se dispone de un notebook de ejemplo en la carpeta `notebooks` para poder interactuar con la API de Google News de forma interactiva.
3. Recomendamos el siguiente workflow:
   1. Crear una branch `ta-exam` en el repositorio. 
   2. Ir subiendo cambios a esa branch. Una vez subido el primer cambio, crear un Pull Request.
   3. En caso de querer agregar o modificar un DAG, recomendamos usar el notebook para prototipar por ejemplo las transformaciones sobre el dataframe de pandas e insertar los cambios en el codigo fuente en este proyecto. Todos los DAGs son parseados desde la carpeta `tienda_amiga/dags`.
4. En caso de necesitar agregar una libreria o algun archivo binario recomendamos:
   1. Tener instalado el environment de Poetry ejecutando `poetry install`. 
   2. Ejecutar `poetry add <libreria_a_agregar>`.
   3. Ir a la carpeta `docker` y ejecutar `docker compose --env-file ../.env build` y luego `docker-compose --env-file ../.env up`
5. Ante cualquier inconveniente de setup local con Poetry es posible acceder a algun container de Airflow para probar scripts de Python dentro del container haciendo:
```bash
docker exec -it ta-playground-airflow-scheduler /bin/bash
```
