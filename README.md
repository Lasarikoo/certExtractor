
# 🔐 CertExtractor

CertExtractor es un script en Python que permite **extraer claves públicas, privadas y certificados** desde archivos `.pfx` o `.p12`, incluso si están cifrados con algoritmos antiguos como `RC2-40-CBC`.

---

## ✅ Requisitos

### 1. Python 3.8 o superior
Instálalo desde: https://www.python.org/downloads/

### 2. OpenSSL 3.0.0 o superior (NO usar versiones "Light")
Necesitas una instalación **completa** de OpenSSL que incluya soporte para el **módulo `legacy`**.

Puedes usar el instalador oficial:

🔗 https://slproweb.com/products/Win32OpenSSL.html  
➡️ Descarga: **Win64 OpenSSL v3.0.16 (Full)**

Durante la instalación marca la opción:
```
✅ Add OpenSSL to the system PATH for all users
```

---

## 📁 Estructura del proyecto

```
certExtractor-main
├── CertExtractor.py              ← Script principal
├── openssl_legacy.cnf            ← Config para activar el módulo legacy
├── installers/
│   ├── Win64OpenSSL_Full-3_0_16.exe  ← Instalador (opcional)
│   └── legacy/
│       ├── bin/
│       ├── include/
│       └── lib/
│           └── ossl-modules/
│               └── legacy.dll   ← Módulo legacy requerido por OpenSSL
```

---

## ⚙️ Configuración automática

CertExtractor se encargará de:
- Activar la configuración `openssl_legacy.cnf` automáticamente
- Establecer la ruta al módulo `legacy.dll`
- Ejecutar los comandos de extracción con `openssl -legacy`

---

## 🧪 ¿Cómo saber si todo está bien configurado?

Abre una terminal nueva y escribe:

```bash
openssl version
```

Debe mostrar algo como:

```
OpenSSL 3.0.16 ...
```

Y también asegúrate de que tienes este archivo:

```
installers/legacy/lib/ossl-modules/legacy.dll
```

---

## 🚀 Uso

Ejecuta el script:

```bash
python CertExtractor.py
```

Luego:
1. Introduce la ruta completa del archivo `.pfx`
2. Introduce la contraseña o PIN
3. El script extraerá:
   - `cert-priv.pem` → Clave privada
   - `key.pem` → Clave sin cifrar
   - `key-pub.pem` → Clave pública
   - `privpub.pem` → Certificado combinado
4. Todos los archivos se guardan en una carpeta `cert_output` junto al `.pfx`
5. Al final puedes abrir la carpeta automáticamente

---

## ⚠️ Errores comunes

### ❌ Error: "unsupported algorithm RC2-40-CBC"
➡️ No tienes el proveedor legacy activado o `legacy.dll` no está presente.

### ❌ Error: "unable to load provider legacy"
➡️ Asegúrate de que la variable `OPENSSL_MODULES` apunta correctamente a `ossl-modules`.
   - Si ejecutas el script desde otra carpeta, se usa la ruta relativa al propio script, pero
     necesitas que exista `installers/legacy/lib/ossl-modules/legacy.dll` junto al ejecutable.
   - Si falta ese archivo, vuelve a copiar la carpeta `installers/legacy` completa o reinstala OpenSSL (versión Full).

---

## 📌 Extras

El script también es capaz de instalar automáticamente OpenSSL si se encuentra el instalador dentro de la carpeta `installers`.

---
