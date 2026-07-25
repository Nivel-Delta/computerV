# Sistema de inicio de sesión con verificación facial

Proyecto de visión por computadora desarrollado con Python, OpenCV, TensorFlow y DeepFace.

El sistema permite registrar un usuario mediante una fotografía facial y verificar posteriormente su identidad mediante una nueva captura de cámara o una imagen existente.

## Funcionalidades

- Registro de usuarios mediante cámara o archivo de imagen.
- Detección facial con RetinaFace.
- Verificación facial mediante el modelo VGG-Face.
- Autorización o denegación del acceso.
- Registro local de intentos de acceso.
- Consulta de usuarios registrados.
- Protección de fotografías biométricas mediante `.gitignore`.

## Requisitos

- Python 3.13 o compatible.
- Cámara web para realizar capturas en tiempo real.
- Conexión a Internet durante la primera ejecución para descargar los modelos de DeepFace.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Nivel-Delta/computerV.git
cd computerV
