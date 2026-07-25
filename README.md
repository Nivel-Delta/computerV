# Sistema de inicio de sesión con verificación facial

Proyecto educativo de visión por computadora desarrollado con Python, OpenCV, TensorFlow y DeepFace.

El programa permite registrar la fotografía facial de un usuario y verificar posteriormente su identidad utilizando una nueva captura de cámara o una imagen existente.

## Funcionalidades

- Registro de usuarios mediante cámara web.
- Registro mediante archivos de imagen.
- Detección facial con RetinaFace.
- Verificación facial mediante VGG-Face.
- Autorización o denegación del acceso.
- Registro local de cada intento en un archivo CSV.
- Consulta de usuarios registrados.
- Protección de fotografías y registros mediante `.gitignore`.

## Requisitos

Para reproducir el entorno utilizado durante el desarrollo se recomienda:

- Windows 10 u 11 de 64 bits.
- Python 3.13 de 64 bits.
- Cámara web.
- Conexión a Internet durante la primera ejecución.
- Aproximadamente 2 GB de espacio disponible.

Durante la primera ejecución, DeepFace descargará los pesos de RetinaFace y VGG-Face. Las ejecuciones posteriores utilizarán los modelos almacenados localmente.

## 1. Clonar el repositorio

Abrir PowerShell y ejecutar:

```powershell
git clone https://github.com/Nivel-Delta/computerV.git
cd computerV
```

## 2. Crear un entorno virtual

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Al activarse correctamente, la terminal mostrará algo similar a:

```text
(.venv) PS C:\ruta\computerV>
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar las dependencias

Con el entorno virtual activado:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La instalación puede tardar varios minutos debido al tamaño de TensorFlow.

Comprobar que no existen dependencias incompatibles:

```powershell
python -m pip check
```

## 4. Comprobar el programa

Ejecutar:

```powershell
python main.py --help
```

Debe aparecer:

```text
usage: main.py [-h] {registrar,verificar,listar} ...

Sistema educativo de inicio de sesión con verificación facial.

positional arguments:
  {registrar,verificar,listar}
    registrar
    verificar
    listar
```

También puede comprobar que el programa inicia mediante:

```powershell
python main.py listar
```

En una instalación nueva mostrará:

```text
No hay usuarios registrados.
```

## 5. Registrar un usuario con la cámara

Ejecutar:

```powershell
python main.py registrar --usuario usuario_prueba --camara
```

Se abrirá una ventana con la cámara.

- Presionar `C` para capturar la fotografía.
- Presionar `Q` para cancelar.

El resultado esperado es:

```text
Fotografía guardada en: ...\capturas_temporales\registro_usuario_prueba.jpg
Usuario registrado: usuario_prueba
Imagen de referencia: ...\usuarios\usuario_prueba.jpg
```

La primera ejecución puede tardar porque RetinaFace descargará sus pesos.

Para obtener mejores resultados:

- Mirar de frente a la cámara.
- Mantener el rostro completamente visible.
- Utilizar buena iluminación.
- Evitar que aparezcan varias personas en la fotografía.
- No cubrir el rostro con objetos.

## 6. Listar usuarios registrados

Ejecutar:

```powershell
python main.py listar
```

Resultado esperado:

```text
Usuarios registrados:
 - usuario_prueba
```

## 7. Verificar el inicio de sesión

Ejecutar:

```powershell
python main.py verificar --usuario usuario_prueba --camara
```

Cuando se abra la cámara, presionar `C` para tomar una nueva fotografía.

Cuando el rostro coincida, aparecerá:

```text
ACCESO AUTORIZADO
Bienvenido, usuario_prueba.
Distancia facial: 0.xxxx
Umbral del modelo: 0.xxxx
```

Cuando el rostro no coincida, aparecerá:

```text
ACCESO DENEGADO
El rostro no coincide con el usuario.
Distancia facial: 0.xxxx
Umbral del modelo: 0.xxxx
```

La distancia facial exacta puede variar según la iluminación, el ángulo, la cámara y la calidad de la imagen.

## 8. Utilizar imágenes existentes

También se puede registrar un usuario con una fotografía existente:

```powershell
python main.py registrar `
    --usuario usuario_imagen `
    --imagen "C:\ruta\real\foto_registro.jpg"
```

La ruta debe corresponder a un archivo que exista realmente. No debe escribirse literalmente `ruta\foto.jpg`.

Verificar con otra fotografía:

```powershell
python main.py verificar `
    --usuario usuario_imagen `
    --imagen "C:\ruta\real\foto_verificacion.jpg"
```

Formatos recomendados:

- JPG
- JPEG
- PNG

## 9. Registros del sistema

Cada registro o intento de acceso queda almacenado localmente en:

```text
registros/accesos.csv
```

El archivo incluye:

- Fecha y hora.
- Usuario.
- Acción realizada.
- Resultado.
- Distancia facial.
- Umbral del modelo.

Las fotografías y los registros no se publican en GitHub porque están protegidos mediante `.gitignore`.

## Estructura del proyecto

```text
computerV/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── usuarios/
│   └── .gitkeep
├── registros/
│   └── .gitkeep
└── capturas_temporales/
    └── .gitkeep
```

## Comandos disponibles

### Ayuda

```powershell
python main.py --help
```

### Registrar con cámara

```powershell
python main.py registrar --usuario nombre --camara
```

### Registrar con imagen

```powershell
python main.py registrar --usuario nombre --imagen "C:\ruta\foto.jpg"
```

### Verificar con cámara

```powershell
python main.py verificar --usuario nombre --camara
```

### Verificar con imagen

```powershell
python main.py verificar --usuario nombre --imagen "C:\ruta\otra_foto.jpg"
```

### Listar usuarios

```powershell
python main.py listar
```

## Solución de problemas

### La cámara no se abre

Cerrar programas que puedan estar utilizando la cámara, como Zoom, Teams, OBS o la aplicación Cámara de Windows, y ejecutar nuevamente el comando.

### No se encontró la imagen

Confirmar que la ruta sea real y esté escrita entre comillas:

```powershell
Test-Path "C:\ruta\real\foto.jpg"
```

El resultado debe ser:

```text
True
```

### DeepFace no encuentra un rostro

Tomar otra fotografía con mejor iluminación, mirar de frente y asegurarse de que el rostro ocupe una parte suficiente de la imagen.

### La primera ejecución tarda demasiado

La primera ejecución descarga los modelos de RetinaFace y VGG-Face. No cerrar la terminal mientras se realiza la descarga.

### Aparecen advertencias de TensorFlow

Los mensajes relacionados con oneDNN o funciones obsoletas son advertencias informativas. El programa puede continuar mientras no aparezca una excepción que detenga la ejecución.

## Privacidad

Las imágenes faciales constituyen información biométrica sensible.

El repositorio no incluye fotografías reales ni registros de acceso. Cada persona que ejecute el proyecto deberá registrar localmente una imagen propia o una fotografía utilizada con autorización.

## Limitaciones de seguridad

Este proyecto fue desarrollado con fines educativos.

No incluye:

- Detección de vida.
- Protección contra fotografías impresas o mostradas en una pantalla.
- Cifrado de plantillas biométricas.
- Autenticación multifactor.
- Administración de usuarios.
- Protección para ambientes productivos.

No debe utilizarse como único mecanismo para proteger información sensible, instalaciones críticas o sistemas reales de alto riesgo.

## Tecnologías utilizadas

- Python
- DeepFace
- TensorFlow
- TF-Keras
- RetinaFace
- VGG-Face
- OpenCV