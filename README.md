# CertExtractor 🛠️🔐

Extractor automático de certificados y claves desde archivos
**.pfx/.p12**, compatible incluso con certificados antiguos cifrados con
algoritmos como **RC2-40-CBC**. Diseñado para despliegues industriales y
sistemas ALPR (TattileSender, VaxALPR On Camera, integraciones SOAP,
etc.).

## 📘 Descripción general

**CertExtractor** es una herramienta en Python que automatiza la
extracción de:

-   **Clave privada cifrada** (`cert-priv.pem`)
-   **Clave privada sin cifrar** (`key.pem`)
-   **Clave pública** (`key-pub.pem`)
-   **Certificado completo** (`privpub.pem`)

a partir de un archivo **.pfx / .p12**, usando exclusivamente
**OpenSSL** mediante `subprocess.run`.\
No valida vigencia ni confianza del certificado: su propósito es
**extraer** y **convertir**.

## ⚠️ Disclaimer IMPORTANTE

Para que el script funcione correctamente en Windows:

**El instalador de OpenSSL (`Win64OpenSSL_Full-3_0_16.exe`) debe estar obligatoriamente dentro de la carpeta `installers/` ubicada en el directorio raíz del proyecto.**

CertExtractor intentará ejecutar este instalador automáticamente si OpenSSL no está disponible en el sistema.  
Si el archivo no está en la ruta correcta, la auto-instalación fallará.

## 🚀 Características

✔ Compatible con certificados antiguos (RC2-40-CBC, TripleDES, etc.)\
✔ Extrae claves y certificados en formato PEM\
✔ Interfaz sencilla por consola (sin flags)\
✔ Sin dependencias externas de Python (solo stdlib + OpenSSL)\
✔ Requiere OpenSSL 3.x con `legacy provider`\
✔ Auto-instalación de OpenSSL en Windows mediante instalador incluido\
✔ Enfoque práctico para entornos ALPR y sistemas empresariales

## 📦 Archivos generados

El script crea una carpeta `cert_output/` junto al archivo de entrada.
Dentro encontrarás:

  Archivo           Descripción
  ----------------- -------------------------------------
  `cert-priv.pem`   Clave privada cifrada
  `key.pem`         Clave privada sin cifrar
  `key-pub.pem`     Clave pública extraída
  `privpub.pem`     Certificado completo en formato PEM

## 🛠️ Requisitos

### Python

-   Python **3.8+**

### OpenSSL

-   OpenSSL **3.x**
-   Debe incluirse el proveedor heredado (`legacy`) para soportar
    cifrados como RC2-40-CBC.

### Windows

Si no existe OpenSSL en el sistema, el script intenta ejecutar el
instalador incluido:

    installers/Win64OpenSSL_Full-3_0_16.exe

## ▶️ Uso

Ejecutar desde consola:

``` bash
python CertExtractor.py
```

El programa solicitará:

1.  Ruta del archivo `.pfx` / `.p12`
2.  Contraseña del certificado

Al finalizar, se mostrará un resumen con los archivos generados y la
ruta de salida (`cert_output/`).

## 📁 Estructura del repositorio

    certExtractor/
    │
    ├─ CertExtractor.py          # Script principal
    ├─ installers/               # Instalador de OpenSSL para Windows
    │   └─ Win64OpenSSL_Full-3_0_16.exe
    └─ README.md

## ❗ Limitaciones actuales

-   No valida fechas de vigencia, cadena de confianza ni emisores.
-   No acepta argumentos tipo `--input` o `--password` (solo interacción
    por consola).
-   No genera logs externos (solo salida por consola).
-   No exporta a otros formatos más allá de PEM.

## 🏭 Casos de uso recomendados

CertExtractor se utiliza en contextos como:

-   Configurar cámaras ALPR (Tattile, Axis, Vaxtor, etc.).
-   Integraciones con Mossos vía WS-Security.
-   Conversión de certificados municipales para enviadores SOAP.
-   Preparación de certificados para sistemas como **TattileSender**.
-   Procesos empresariales donde se reciben certificados heredados o
    cifrados.

## 🧭 Roadmap

-   [ ] Añadir CLI completo con flags (`--input`, `--output`,
    `--password`).
-   [ ] Validación opcional del certificado (vigencia, emisor, cadena).
-   [ ] Exportación a DER, CRT y PKCS8.
-   [ ] Sistema de logs estructurados.
-   [ ] Modo silencioso para automatizaciones CI/CD.

## 📝 Licencia

Distribuido bajo licencia **MIT**.

## 👤 Autor

**Lázaro Beltrán García (Lasarikoo)**\
Automatización ALPR · Backend Python · Integraciones SOAP/REST
