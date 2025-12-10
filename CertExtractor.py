import os
import subprocess
import shutil
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración obligatoria para OpenSSL con legacy provider
OPENSSL_CONF_PATH = os.path.join(BASE_DIR, "openssl_legacy.cnf")
OPENSSL_MODULES_PATH = os.path.join(BASE_DIR, "installers", "legacy", "lib", "ossl-modules")
os.environ["OPENSSL_CONF"] = OPENSSL_CONF_PATH
os.environ["OPENSSL_MODULES"] = OPENSSL_MODULES_PATH

INSTALLER_PATH = os.path.join(BASE_DIR, "installers", "Win64OpenSSL_Full-3_0_16.exe")


def show_banner():
    print(r"""
╔════════════════════════════════════════════════════════════╗
║            🛡️  Extractor de Certificados PFX  🛡️            ║
║      Autor: Lázaro Beltrán García | Alphanet Solutions      ║
╚════════════════════════════════════════════════════════════╝
""")

def try_manual_openssl_path():
    paths = [
        r"C:\Program Files\OpenSSL-Win64\bin",
        r"C:\OpenSSL-Win64\bin",
        os.path.join(BASE_DIR, "installers", "legacy", "bin")
    ]
    for path in paths:
        candidate = os.path.join(path, "openssl.exe")
        if os.path.isfile(candidate):
            os.environ["PATH"] += os.pathsep + path
            return True
    return False

def check_openssl():
    if not os.path.isdir(OPENSSL_MODULES_PATH):
        print("⚠️ Ruta del provider legacy no encontrada:", OPENSSL_MODULES_PATH)
        print("   Verifica que el instalador 'installers/legacy' está completo y vuelve a ejecutar.")

    openssl_path = shutil.which("openssl")
    if openssl_path:
        try:
            result = subprocess.run(["openssl", "version"], capture_output=True, text=True)
            version = result.stdout.strip()
            print(f"🔍 OpenSSL detectado: {version}")
            return True
        except Exception as e:
            print("❌ Error al ejecutar OpenSSL:", e)
            return False

    print("❌ OpenSSL no está instalado.")
    if os.path.isfile(INSTALLER_PATH):
        print("🔧 Instalador encontrado, ejecutando instalación silenciosa...")
        try:
            subprocess.run([
                INSTALLER_PATH,
                "/silent", "/sp-", "/suppressmsgboxes", "/norestart"
            ], check=True)

            print("✅ Instalación completada. Esperando que el sistema reconozca OpenSSL...")
            time.sleep(5)

            if shutil.which("openssl") or try_manual_openssl_path():
                print("✅ OpenSSL detectado manualmente tras instalación.")
                return True

            print("❌ OpenSSL sigue sin estar disponible tras la instalación.")
            return False
        except subprocess.CalledProcessError as e:
            print("❌ Falló la instalación de OpenSSL:", e)
            return False
    else:
        print(f"❌ No se encontró el instalador en {INSTALLER_PATH}")
        return False

def run_openssl(args, description):
    print(f"✨ {description} en progreso...")
    try:
        subprocess.run(args, check=True)
        print(f"✅ {description} completada")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en '{description}': {e}")
        return False

def extract_cert():
    show_banner()
    print("🚀 Preparando el viaje para liberar tus certificados...")

    if not check_openssl():
        return

    while True:
        pfx_path = input("Ruta del archivo .pfx: ").strip().strip('"')
        if os.path.isfile(pfx_path):
            break
        print("❌ El archivo no existe. Por favor, introduce una ruta válida.")

    pfx_dir = os.path.dirname(pfx_path)
    pfx_pass = input("Introduce el PIN del certificado (contraseña): ").strip()
    output_dir = os.path.join(pfx_dir, "cert_output")
    os.makedirs(output_dir, exist_ok=True)

    print("📂 Los certificados se guardarán en:", output_dir)
    print("🎵 Abriendo la caja fuerte digital y separando las piezas...")

    # Usamos directamente openssl con -legacy y -passin
    print("🧩 Separando la clave privada para que puedas firmar con estilo...")
    run_openssl([
        "openssl", "pkcs12", "-legacy", "-in", pfx_path,
        "-nocerts", "-out", os.path.join(output_dir, "cert-priv.pem"),
        "-nodes", "-passin", f"pass:{pfx_pass}"
    ], "Clave privada (cert-priv.pem)")

    print("📜 Preparando el certificado completo, como un pergamino digital...")
    run_openssl([
        "openssl", "pkcs12", "-legacy", "-in", pfx_path,
        "-out", os.path.join(output_dir, "privpub.pem"),
        "-passin", f"pass:{pfx_pass}",
        "-passout", f"pass:{pfx_pass}"
    ], "Certificado completo (privpub.pem)")

    print("🔑 Forjando la clave pública para compartir sin revelar secretos...")
    run_openssl([
        "openssl", "x509", "-inform", "pem", "-in",
        os.path.join(output_dir, "privpub.pem"),
        "-pubkey", "-out", os.path.join(output_dir, "key-pub.pem"),
        "-outform", "pem", "-passin", f"pass:{pfx_pass}"
    ], "Clave pública (key-pub.pem)")

    print("🛡️ Generando una copia de la clave sin cifrar para integraciones especiales...")
    run_openssl([
        "openssl", "pkcs12", "-legacy", "-in", pfx_path,
        "-nocerts", "-out", os.path.join(output_dir, "key.pem"),
        "-nodes", "-passin", f"pass:{pfx_pass}"
    ], "Clave sin cifrar (key.pem)")

    print(f"\n✅ Certificados extraídos en la carpeta: {output_dir}")
    for file in os.listdir(output_dir):
        print(" -", file)

    abrir = input("\n¿Quieres abrir la carpeta ahora? (s/n): ").strip().lower()
    if abrir == "s":
        subprocess.run(["explorer", output_dir], shell=True)

if __name__ == "__main__":
    extract_cert()
