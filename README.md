# Ejercicio

Crear una API, que recibira credenciales de validacion, (user / pass), llame via
scraping a la URL [https://www.disco.com.ar/electro/informatica](https://www.disco.com.ar/electro/informatica) y devuelva un
JSON conel siguiente formato con todos los productos encontados:

```
{
    "records": [
        {
            "marca": "Lenovo",
            "descripcion": "Notebook Lenovo 14' Ip 3 I5 8g 256g",
            "precio": "114999"
        },
        {
            "marca": "Samsung",
            "descripcion": "Monitor Samsung 24' Fhd Lf24t350fhlczb",
            "precio": "54599"
        }
    ]
}
```

# Scraping

Para realizar el scraping usamos 2 paquetes de python:

1.  beatifulsoup4
2.  selenium

## Problema

Existen páginas donde la información es estática que son las más fáciles para scraping. 
El problema surge con las páginas dinámicas. Por ejemplo donde la información
html es creada dinámicamente como es el caso del paginado de los artículos.

En dicho caso beatibulsoup no tiene control de la carga de los scripts, ni del 
flujo dinámico desencadenado por un evento. Por lo q no puede obtener **toda**
la imformación html.

Aqui es donde entra selenium al rescate.

## Selenium

Selenium nos permite mediante código manejar las acciones realizadas por los
usuarios en los browsers ejemplo: registrarse, hacer click en botones, enlaces,
etc. En otras palabras nos permite navega ren el browser mediante código.

Para usar selenium necesitas un navegador y los drivers del mismo.
En nuestro caso vamos a usar la imagen de docker **selenium/standalone-chrome**

Que es un servidor con **Selenium Grid**. El cual permite trabajar con
multiples nodos con dferentes navegadores web y multiples sesiones.
Nuestro caso tendremos un solo nodo corriendo chrome con una sola sesión.

Una de las grandes ventajas de **Selenium Grid** es que a medidas que vas
ejecutando el código python puedes visualizar la navegación automática que va
realizando el navegador.

![Selenium-Grid](./src/img/selenium-grid-1.gif)

Una vez que tengamos el contenido cargado, podemos extraer la información con
**beatifulsoup**.

## Beatifulsoup

Beautiful Soup es una biblioteca de Python para analizar documentos 
HTML (incluyendo los que tienen un marcado incorrecto). Esta biblioteca 
crea un árbol con todos los elementos del documento y puede ser utilizado 
para extraer información.

## API con flask
Flask es un framework minimalista escrito en Python que permite crear 
aplicaciones web rápidamente y con un mínimo número de líneas de código.

##  Instalación

> El sistema lo desplegaremos en 2 contenedores dockers, utilizando
doker-compose. Un contenedor con el **webservice** y el otro con **Selenium Grid**

### Instalar docker Ubuntu 20.04

```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
su - ${USER}
```

### Instalando docker-compose Ubuntu 20.04

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Clonando e iniciando los servidores

```
git clone https://github.com/raulfrt/pyapi
cd pyapi
docker-compose up -d
```

## Documentación API con Swagger

[https://app.swaggerhub.com/apis/raulfrt/Scraping/1.0.0](https://app.swaggerhub.com/apis/raulfrt/Scraping/1.0.0)

## Endpoints a consumir

Para la prueba necesitamos realizar el login con usuruaio/contraseña. Eso nos
devolverá un token de acceso con un tiempo de caducidad, le hemos puesto 1
hora. El token es utilizado para poder consultar el resto de los endpoints.

### login

**url**: http://<servername>:<port>/api/login

**method**: POST

**body**: {
    "username": "demo",
    "password": "demo"
}

**descripción**: login del sistema que devuelve un access token para poder acceder
al resto de los endpoints.

**devuelve**: <access_token>

**Ejemplo de petición**

```
curl -X POST \
  http://localhost:5000/api/login \
  -H 'cache-control: ' \
  -H 'content-type: application/json' \
  -d '{
	"username": "demo",
	"password": "demo"
}'
```

### scraping

**url**: http://<servername>:<port>/api/scraping-disco

**method**: GET

**descripción**: realiza scraping de los artículos de la url 
**https://www.disco.com.ar/electro/informatica**

**parámetros**:

1.  **Authorization**: donde pasamos <access_token>
2.  [first_page]: parámetro opcional.

**devuelve**:

```
{
    "records": [
        {
            "marca": "Lenovo",
            "descripcion": "Notebook Lenovo 14' Ip 3 I5 8g 256g",
            "precio": "114999"
        },
        {
            "marca": "Samsung",
            "descripcion": "Monitor Samsung 24' Fhd Lf24t350fhlczb",
            "precio": "54599"
        }
    ]
}
``` 

**Ejemplo de petición**

```
curl -X GET \
  'http://localhost:5000/api/scraping-disco' \
  -H 'first_page: 1' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRlbW8iLCJwYXNzd29yZCI6ImRlbW8iLCJleHAiOjE2NjkzOTEyOTN9.Sc0FgUxgfQlXUmID4UGrvGTST7n0s6_AmBbw-Wq69Ns'
```

> El parámetro opcional first_page se utilizó para devolver solo los artículos
de la primera página. Porque en ociones al navegar por la web no se cargaban 
los artículos. En los siguientes 2 videos se ilustra el problema:

![Navegación por usuario](./src/video/user-navigation.webm)

![Navegación por selenium](./src/video/selenium-navigation.webm)




