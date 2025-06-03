![Energía_Eléctrica_TDF](https://raw.githubusercontent.com/ckriztian/Energia_Electrica_TDF/refs/heads/main/reports/figures/banner_flat1.jpg)

### 📘 Sistema Experto para la Evaluación de Sustancias Químicas y Gestión de Riesgos en la Provincia de Tierra del Fuego, Argentina.

Este documento describe la estructura, lógica y organización del conocimiento utilizada en el desarrollo del **Sistema Experto para Evaluación de Mezclas Químicas** conforme a regulaciones de Tierra del Fuego.

---

### 1. 🧠 Introducción

El sistema tiene como objetivo asistir a técnicos o usuarios no expertos en la **evaluación de mezclas químicas**, determinación de niveles de **toxicidad** y **generación de recomendaciones** de gestión, de acuerdo a parámetros físico-químicos y normativas locales.

---

### 2. 🧬 Organización del Conocimiento

### 2.1 📦 Estructura de Datos

- `compuestos.json`: contiene la lista de sustancias individuales con sus propiedades clave:
  - `pH`
  - `inflamable`
  - `reactivo`
  - `volatil`
  - `explosivo`
  - `radiactivo`
  - `metales_pesados`
  - `categoria`

- `regulaciones_tdf.json`: contiene la normativa local, categorizada por tipo de riesgo, incluyendo:
  - medidas de descarte
  - condiciones de transporte
  - autoridades de intervención

### 2.2 🧪 Evaluación de Mezclas

Cuando el usuario selecciona varios compuestos, se calculan propiedades agregadas como:

- Promedio de pH
- Suma o presencia de características de riesgo (radiactividad, inflamabilidad, etc.)

---

### 3. ⚙️ Reglas y Métodos de Inferencia

El sistema aplica **reglas de producción tipo `IF-THEN`**, codificadas en el archivo `logic.py`. Estas reglas suman una puntuación de **toxicidad total**, que luego es interpretada.

### 📖 Ejemplo de reglas:

```python
if pH < 4 or pH > 10:
    toxicidad += 2
if inflamable:
    toxicidad += 1
if radiactivo:
    toxicidad += 5
```

🧮 Método de Inferencia:
- Basado en lógica de puntuación acumulativa
- Evaluación secuencial de reglas
- Categorización automática de nivel de riesgo: bajo, moderado o alto

---

### 4. 🧱 Jerarquía de Riesgos
El sistema prioriza las características de mayor peligrosidad. Las categorías están ordenadas de la siguiente forma:

| Nivel |	Característica |
|-------|--------------- |
| 🔴 1 |	Radiactivo |
| 🟠 2 |	Explosivo |
| 🟡 3 |	Tóxico | 
| 🟡 4 |	Oxidante |
| 🟢 5 |	Corrosivo |
| 🟢 6 |	Inflamable |

Esto permite decidir automáticamente cuál es la regulación dominante a aplicar.

---

### 5. 📤 Generación de Recomendaciones
Con base en la categoría principal y la toxicidad total, se extrae la normativa correspondiente desde `regulaciones_tdf.json` y se genera:
- Recomendación en texto natural
- Instrucciones para manejo y descarte
- Datos de contacto de autoridades locales

---

### 6. 📊 Visualización del Conocimiento
El sistema también muestra **gráficos de barras** de toxicidad total usando *matplotlib*, facilitando la comprensión visual de la mezcla evaluada.

---

### 7. ♻️ Retroalimentación y Seguimiento
Cada análisis queda registrado para posibles mejoras futuras, permitiendo:
- Análisis estadístico de casos frecuentes
- Entrenamiento de futuros sistemas más complejos (ej. basados en IA)

---

### 8. ✅ Conclusión
La arquitectura del conocimiento combina:
- Datos estructurados (compuestos y regulaciones)
- Reglas tipo experto if-then
- Jerarquías de peligrosidad
- Interpretación y recomendación automatizada

Este diseño permite un sistema robusto, explicable y alineado con normativas específicas de Tierra del Fuego.

---

### ⚙️ Estructura de organización
```
sistema_experto_quimico_tdf/
├── .github/
│   └── workflows/          # Opcional: Para GitHub Actions (CI/CD)
├── data/
│   ├── compuestos.json
│   ├── regulaciones_tdf.json
│   └── historial.json
├── docs/
│   └── Cristian Vera - Entrega 1.pdf
├── src/
│   ├── __init__.py         # Hace que 'src' sea un paquete
│   ├── logic.py
│   └── main_gui.py
├── tests/                  # Opcional: Para pruebas unitarias
│   └── __init__.py
│   └── test_logic.py       # Opcional: Ejemplo de archivo de prueba
├── .gitignore
├── LICENSE                 # Opcional: Añade un archivo de licencia (ej. MIT, GPL)
└── README.md
```