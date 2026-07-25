from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import cv2
from deepface import DeepFace


BASE_DIR = Path(__file__).resolve().parent
USUARIOS_DIR = BASE_DIR / "usuarios"
REGISTROS_DIR = BASE_DIR / "registros"
TEMPORALES_DIR = BASE_DIR / "capturas_temporales"
REGISTRO_CSV = REGISTROS_DIR / "accesos.csv"

MODELO_FACIAL = "VGG-Face"
DETECTOR_FACIAL = "retinaface"

def preparar_directorios() -> None:
    """Crea las carpetas necesarias y el archivo de registros."""
    USUARIOS_DIR.mkdir(exist_ok=True)
    REGISTROS_DIR.mkdir(exist_ok=True)
    TEMPORALES_DIR.mkdir(exist_ok=True)

    if not REGISTRO_CSV.exists():
        with REGISTRO_CSV.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                "fecha_hora",
                "usuario",
                "accion",
                "resultado",
                "distancia",
                "umbral",
            ])


def limpiar_usuario(nombre: str) -> str:
    """Convierte el nombre en un valor seguro para usar como archivo."""
    nombre_limpio = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        nombre.strip()
    )

    if not nombre_limpio:
        raise ValueError("El nombre del usuario no es válido.")

    return nombre_limpio


def guardar_registro(
    usuario: str,
    accion: str,
    resultado: str,
    distancia: float | None = None,
    umbral: float | None = None,
) -> None:
    """Guarda cada registro o intento de acceso en un archivo CSV."""
    with REGISTRO_CSV.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            datetime.now().isoformat(timespec="seconds"),
            usuario,
            accion,
            resultado,
            "" if distancia is None else round(distancia, 6),
            "" if umbral is None else round(umbral, 6),
        ])


def validar_imagen(ruta: Path) -> None:
    """Verifica que el archivo exista y que OpenCV pueda leerlo."""
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta}"
        )

    imagen = cv2.imread(str(ruta))

    if imagen is None:
        raise ValueError(
            f"El archivo no contiene una imagen válida: {ruta}"
        )


def capturar_fotografia(ruta_salida: Path) -> None:
    """Captura una fotografía mediante la cámara del equipo."""
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        raise RuntimeError(
            "No fue posible abrir la cámara."
        )

    print("Presione C para capturar la fotografía.")
    print("Presione Q para cancelar.")

    try:
        while True:
            disponible, frame = camara.read()

            if not disponible:
                raise RuntimeError(
                    "No fue posible obtener una imagen de la cámara."
                )

            cv2.putText(
                frame,
                "C: capturar | Q: cancelar",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "Sistema de verificacion facial",
                frame
            )

            tecla = cv2.waitKey(1) & 0xFF

            if tecla in (ord("c"), ord("C")):
                cv2.imwrite(str(ruta_salida), frame)
                print(
                    f"Fotografía guardada en: {ruta_salida}"
                )
                break

            if tecla in (ord("q"), ord("Q")):
                raise KeyboardInterrupt(
                    "Captura cancelada por el usuario."
                )

    finally:
        camara.release()
        cv2.destroyAllWindows()


def obtener_imagen(
    ruta_imagen: str | None,
    usar_camara: bool,
    ruta_temporal: Path,
) -> tuple[Path, bool]:
    """Obtiene una imagen desde archivo o mediante cámara."""
    if usar_camara:
        capturar_fotografia(ruta_temporal)
        return ruta_temporal, True

    if ruta_imagen:
        ruta = Path(ruta_imagen).expanduser().resolve()
        validar_imagen(ruta)
        return ruta, False

    raise ValueError(
        "Debes proporcionar --imagen o utilizar --camara."
    )


def registrar_usuario(
    nombre: str,
    ruta_imagen: str | None,
    usar_camara: bool,
) -> None:
    """Registra una fotografía facial de referencia."""
    usuario = limpiar_usuario(nombre)
    destino = USUARIOS_DIR / f"{usuario}.jpg"
    temporal = TEMPORALES_DIR / f"registro_{usuario}.jpg"

    origen, es_temporal = obtener_imagen(
        ruta_imagen,
        usar_camara,
        temporal,
    )

    try:
        validar_imagen(origen)

        DeepFace.extract_faces(
            img_path=str(origen),
            detector_backend=DETECTOR_FACIAL,
            enforce_detection=True,
        )

        shutil.copy2(origen, destino)

        guardar_registro(
            usuario,
            "registro",
            "usuario_registrado",
        )

        print(f"Usuario registrado: {usuario}")
        print(f"Imagen de referencia: {destino}")

    finally:
        if es_temporal and temporal.exists():
            temporal.unlink()


def verificar_usuario(
    nombre: str,
    ruta_imagen: str | None,
    usar_camara: bool,
) -> None:
    """Compara el rostro presentado con el usuario registrado."""
    usuario = limpiar_usuario(nombre)
    referencia = USUARIOS_DIR / f"{usuario}.jpg"
    temporal = TEMPORALES_DIR / f"verificacion_{usuario}.jpg"

    if not referencia.exists():
        raise FileNotFoundError(
            f"El usuario '{usuario}' no está registrado."
        )

    candidata, es_temporal = obtener_imagen(
        ruta_imagen,
        usar_camara,
        temporal,
    )

    try:
        resultado = DeepFace.verify(
            img1_path=str(referencia),
            img2_path=str(candidata),
            model_name=MODELO_FACIAL,
            detector_backend=DETECTOR_FACIAL,
            enforce_detection=True,
        )

        verificado = bool(resultado.get("verified", False))
        distancia = float(resultado.get("distance", 0))
        umbral = float(resultado.get("threshold", 0))

        if verificado:
            estado = "acceso_autorizado"
            print("\nACCESO AUTORIZADO")
            print(f"Bienvenido, {usuario}.")
        else:
            estado = "acceso_denegado"
            print("\nACCESO DENEGADO")
            print("El rostro no coincide con el usuario.")

        print(f"Distancia facial: {distancia:.4f}")
        print(f"Umbral del modelo: {umbral:.4f}")

        guardar_registro(
            usuario,
            "verificacion",
            estado,
            distancia,
            umbral,
        )

    finally:
        if es_temporal and temporal.exists():
            temporal.unlink()


def listar_usuarios() -> None:
    """Muestra los usuarios registrados localmente."""
    usuarios = sorted(
        archivo.stem
        for archivo in USUARIOS_DIR.glob("*.jpg")
    )

    if not usuarios:
        print("No hay usuarios registrados.")
        return

    print("Usuarios registrados:")

    for usuario in usuarios:
        print(f" - {usuario}")


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Sistema educativo de inicio de sesión "
            "con verificación facial."
        )
    )

    subparsers = parser.add_subparsers(
        dest="comando",
        required=True
    )

    registrar = subparsers.add_parser(
        "registrar",
        help="Registrar un usuario."
    )
    registrar.add_argument(
        "--usuario",
        required=True
    )
    registrar.add_argument("--imagen")
    registrar.add_argument(
        "--camara",
        action="store_true"
    )

    verificar = subparsers.add_parser(
        "verificar",
        help="Verificar la identidad de un usuario."
    )
    verificar.add_argument(
        "--usuario",
        required=True
    )
    verificar.add_argument("--imagen")
    verificar.add_argument(
        "--camara",
        action="store_true"
    )

    subparsers.add_parser(
        "listar",
        help="Mostrar usuarios registrados."
    )

    return parser


def main() -> int:
    preparar_directorios()
    parser = crear_parser()
    argumentos = parser.parse_args()

    try:
        if argumentos.comando == "registrar":
            registrar_usuario(
                argumentos.usuario,
                argumentos.imagen,
                argumentos.camara,
            )

        elif argumentos.comando == "verificar":
            verificar_usuario(
                argumentos.usuario,
                argumentos.imagen,
                argumentos.camara,
            )

        elif argumentos.comando == "listar":
            listar_usuarios()

        return 0

    except KeyboardInterrupt as error:
        print(f"\nOperación cancelada: {error}")
        return 1

    except Exception as error:
        print(f"\nError: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())