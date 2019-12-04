CFDi Blacklist
==============

## Descripción
Script para ayudar a detectar CFDis relacionados con personas que se encuentran en la lista negra del SAT.

*Funciona con Python3*

## Configuración
Instalar las dependencias necesarias de Python:

```python
pip install -r requirements.txt
```

*Es posible que al momento de instalar el archivo de requerimientos haya un error al instalar psycopg2, en ubuntu se puede solucionar así*

```
apt install libpq-dev python3-dev
```

*Opcional*

Crear una variable de entorno con la URI de la Base de Datos que se desea utilizar.

*En caso de no generar la variable de entorno, se generara un archivo data.db con la Base de Datos en SQLite.*

## Uso
### Actualizar listas negras del SAT a la última versión 

Ejecutar con python el script update_database

```
python update_database.py
```

### Buscar problemas con archivos CFDi

Ejecutar con python el script finder.py e introducir la ruta de algun directorio que contenga archivos XML de CFDis.

```
python finder.py
/home/usr/directorio/con/xml
```
