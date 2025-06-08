# 🚀 Instrucciones para Ejecutar la API del Sistema Experto Químico

## 🔧 Requisitos Previos

1. **Python 3.8 o superior**  
   Verificá con:
   ```bash
   python --version
   ```

2. **Instalar dependencias**  
   Se recomienda usar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate     # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   O instalarlas manualmente:
   ```bash
   pip install fastapi uvicorn pydantic matplotlib
   ```

## ▶️ Ejecutar el Servidor

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. Iniciar el servidor:
   ```bash
   uvicorn api:app --reload
   ```

3. Acceder a la documentación interactiva (Swagger UI):  
   👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 📦 Archivos importantes

- `api.py`: API REST con FastAPI.
- `logic.py`: Lógica del sistema experto.
- `compuestos.json`: Base de hechos (compuestos químicos).
- `regulaciones_tdf.json`: Reglas y regulaciones locales.
- `index.html`: Interfaz web (abrir en navegador).

> `historial.json` se genera automáticamente si no existe.