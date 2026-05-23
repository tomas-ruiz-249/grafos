# Guia de Instalación

## Crear un entorno de Python

Ejecutar el siguiente comando en la terminal en el mismo directorio de **main.py**:

```
python -m venv .venv
```

Luego, activar el entorno:

### Linux (bash)

```
source .venv/bin/activate
```

### Windows (cmd)

```
.venv\Scripts\activate.bat
```

### Windows (powershell)

```
.venv\Scripts\Activate.ps1
```

## Instalar dependencias del programa

```
pip install -r requirements.txt
```

## Ejecutar

```
python main.py
```
