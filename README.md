# Ejercicio

Crear una API, que recibira credenciales de validacion, (user / pass), llame via
scraping a la URL https://www.disco.com.ar/electro/informatica y devuelva un
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

1. beatifulsoup4
2. selenium

## Problema

Existen páginas donde la información es estática que son las más fáciles para scraping. 
El problema surge con las páginas dinámicas. Por ejemplo donde la informacion html es creada dinamicamente como es el caso del paginado de los artículos.

En dicho caso beatibulsoup no tiene ocntrol de la carga de los scripts, ni del flujo dinámico desencadenado por un evento. Por lo q no puede obtener **toda** la imformación html.

Aqui es donde entra selenium al rescate.

## Selenium

Selenium nos permite mediante código manejar las acciones realizadas por los usuarios en los browsers ejemplo: registrarse, hacer click en botones, enlaces, etc. 

Una vez que tengamos el contenido cargado, podemos extraer la información con **beatifulsoup**

## Selenium grid

Correremos un servidor de selenium grid, en el cual podremos tener instanciados mas de un navegador web con diferentes sessiones. Para nuestro ejemplo solo crearemos uh hub de chrome con una sola sesión.

## Beatifulsoup

Beautiful Soup es una biblioteca de Python para analizar documentos HTML (incluyendo los que tienen un marcado incorrecto). Esta biblioteca crea un árbol con todos los elementos del documento y puede ser utilizado para extraer información.

## Webservice con flask
Flask es un framework minimalista escrito en Python que permite crear aplicaciones web rápidamente y con un mínimo número de líneas de código.

Crearemos el servidor para la aplicacion corriendo por el puerto **5000** y un servidor de **selenium grid** corriendo por el puerto **4444**.


##  Instalación

### Método 1:

Instalaremos selenium-grid con docker:

```
docker run --network postgres_local --name selenium -d -p 4444:4444 -e SE_VNC_NO_PASSWORD=1 -e SE_NODE_SESSION_TIMEOUT=3600 --shm-size="2g" selenium/standalone-chrome:latest
```



