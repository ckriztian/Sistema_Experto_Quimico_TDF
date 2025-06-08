![Sistema_Experto_TDF](https://raw.githubusercontent.com/ckriztian/Energia_Electrica_TDF/refs/heads/main/reports/figures/banner_flat1.jpg)

### Arquitectura del Sistema Experto

### 1. Extracción y Organización del Conocimiento

El conocimiento de este sistema fue extraído del conocimiento técnico de una **experta en química, procesos químicos y regularizaciones locales**. A su vez, se sistematizó utilizando fuentes confiables como protocolos de manejo de sustancias peligrosas y las **normativas ambientales específicas de la provincia de Tierra del Fuego** (`regulaciones_tdf.json`).

Este conocimiento se organiza en tres componentes fundamentales:

### a. Base de Hechos (`compuestos.json`)
Contiene información detallada de más de 40 compuestos químicos con sus propiedades fisicoquímicas:

- pH
- Inflamabilidad
- Reactividad
- Volatilidad
- Presencia de metales pesados
- Explosividad
- Radiactividad
- Categoría principal (ej. inflamable, tóxico, corrosivo, etc.)

### b. Base de Conocimiento (`regulaciones_tdf.json`)
Incluye las **reglas y recomendaciones asociadas a cada categoría de riesgo químico**, indicando:

- Métodos de descarte.
- Requisitos de almacenamiento.
- Autoridad competente.
- Contactos de emergencia específicos.

### c. Motor de Inferencia (`logic.py`)
Aplica reglas lógicas para evaluar el nivel de toxicidad y generar recomendaciones, simulando el razonamiento de un experto humano.

### 2. Reglas, Criterios y Estructuras de Decisión

### a. Reglas tipo IF-THEN (Reglas de Producción)
```python
if respuestas['inflamable'] == 'si':
    toxicidad += 1

if respuestas['explosivo'] == 'si':
    toxicidad += 4

if respuestas['pH'] == 'si':
    toxicidad += 2
```

Estas reglas también consideran valores "desconocido", penalizándolos con la mitad del puntaje:

```python
if respuestas.get('radiactivo') == 'desconocido':
    toxicidad += 2.5
```

### b. Árbol de Decisión Implícito por Puntajes

| Puntaje total | Nivel de Toxicidad         | Grado de Certeza             |
|---------------|----------------------------|------------------------------|
| ≥ 5           | Extremadamente tóxica      | Nivel 4 (Alta certeza)       |
| ≥ 4           | Altamente tóxica           | Nivel 3 (Probable)           |
| ≥ 2.5         | Moderadamente tóxica       | Nivel 2 (Incertidumbre)      |
| ≥ 1.5         | Potencialmente peligrosa   | Nivel 1 (Alta incertidumbre) |
| < 1.5         | Baja toxicidad             | Nivel 0 (Riesgo mínimo)      |

### c. Reglas Jerárquicas por Categoría

```python
prioridades = {
    'radiactivo': 6,
    'explosivo': 5,
    'tóxico': 4,
    'oxidante': 3,
    'corrosivo': 2,
    'inflamable': 1
}
```

### 3. Métodos de Inferencia Aplicados

- **Inferencia Directa**: Basada en respuestas explícitas del usuario.
- **Inferencia Aproximada**: Penaliza respuestas "desconocidas".
- **Inferencia Jerárquica**: Elige la categoría más peligrosa.
- **Inferencia Integrada**: Deduce propiedades desde la combinación de compuestos.

### 4. Lógica de Organización del Conocimiento

| Nivel             | Descripción                                                                 |
|------------------|------------------------------------------------------------------------------|
| **Base química** | Información factual de compuestos (`compuestos.json`)                        |
| **Base normativa**| Reglas por categoría química (`regulaciones_tdf.json`)                      |
| **Motor lógico**  | Inferencia, evaluación y recomendaciones (`logic.py`)                        |

### 5. Justificación de la Organización

- **Facilidad de mantenimiento**
- **Separación clara de dominios**
- **Extensibilidad geográfica y normativa**
- **Razonamiento explicable**

___

### Para más detalles del Sistema Experto:
---
### [Descripción del Proyecto del Sistema Experto](https://github.com/ckriztian/Sistema_Experto_Quimico_TDF/blob/main/docs/Entrega%201.pdf)
### [Organización del Conocimiento en el Sistema Experto](https://github.com/ckriztian/Sistema_Experto_Quimico_TDF/blob/main/docs/Entrega%202.pdf)
---
### [Link del video - presentación](https://wwww.youtube.com)
---
 ### Estructura del Repositorio:

```
├── docs/                         # Documentación del proyecto
│   └── Entrega 1                 # Informe descriptivo del proyecto
│   └── Entrega 2                 # Informe de la arquitectura del proyecto
├── README.md                     # Descripción general del sistema
├── api.py                        # API REST desarrollada con FastAPI
├── compuestos.json               # Base de hechos: compuestos químicos y propiedades
├── historial.json                # Historial de consultas (se crea automáticamente si no existe)
├── index.html                    # Interfaz web del sistema experto
├── logic.py                      # Motor de inferencia y lógica del sistema
├── regulaciones_tdf.json         # Reglas de seguridad y regulaciones ambientales locales
```

