# Backend simulacion uso de monedas

## Descripción:

Servicio Realizado con flask/flask-restplus y base de datos SQLLite para la realizacion de la API Rest del sistema, enteramente documentado con swagger.
### DEMO de la API [instancia de AWS EC2](http://54.94.217.113/api/doc)

Usuarios de prueba:
* nacosta
* fcorvalan
* fdiaz
* admin

La contraseña de todos los usuarios es `1234`

Tanbién se puede realizar el log in desde swagger para probar las apis, haciendo click en Authorize.

## Levantar servicios para desarrollo local con docker compose:
Clonar repo: 
```bash
$ cd project-back

$ git clone https://github.com/eneacosta/project-back.git
```
Levantar servicios:
```bash
$ sudo docker-compose up -f docker-compose.develpment.yml
```

El servicio deberia estar corriendo en el puerto 8000 de [localhost](http://localhost:8000), la [documentacion de la api](http://localhost:8000/doc) en /doc.

## Levantar servicios para desarrollo local:

Clonar repo: 
```bash
$ git clone https://github.com/eneacosta/project-back.git
```
Setear entorno virtual: 
```bash
$ cd project-back

$ python venv env

$ source env/Script/activate
# o
$ source env/bin/activate
# dependiendo del SO
```
Instalar librerias: 
```bash
$ pip install -r requirements.txt
```
Correr instancia de desarrollo de flask con refresco automatico: 
```bash
$ python app.py
```

El servicio deberia estar corriendo en el puerto 5000 de [localhost](http://localhost:5000), la [documentacion de la api](http://localhost:5000/doc) en /doc.

