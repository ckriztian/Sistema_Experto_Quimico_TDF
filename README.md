
# Arquitectura del Conocimiento del Sistema Experto Químico

## 1. Estructura General del Conocimiento

El sistema experto está orientado a diagnosticar la peligrosidad de mezclas químicas y recomendar acciones conforme a regulaciones ambientales específicas de Tierra del Fuego. El conocimiento se estructura en tres fuentes principales:

- **Base de hechos**: Los compuestos químicos con sus propiedades fisicoquímicas (`compuestos.json`).
- **Base de conocimiento**: Las regulaciones locales específicas para cada categoría química (`regulaciones_tdf.json`).
- **Motor de inferencia**: Lógica codificada en `logic.py`, que evalúa la toxicidad y genera recomendaciones mediante reglas.

---

## 2. Representación del Conocimiento

### 2.1. Reglas tipo IF-THEN (reglas de producción)

El sistema utiliza reglas condicionales clásicas:

```python
if respuestas['pH'] == 'si':
    toxicidad += 2

if respuestas.get('explosivo') == 'si':
    toxicidad += 4
```

### 2.2. Árbol implícito de decisión por puntajes

El sistema calcula un puntaje acumulado basado en las propiedades, que determina el nivel de toxicidad:

| Puntaje total | Nivel de Toxicidad         | Confianza                    |
|---------------|----------------------------|------------------------------|
| ≥ 5           | Extremadamente tóxica      | Nivel 4 (Alta certeza)       |
| ≥ 4           | Altamente tóxica           | Nivel 3 (Probable)           |
| ≥ 2.5         | Moderadamente tóxica       | Nivel 2 (Incertidumbre)      |
| ≥ 1.5         | Potencialmente peligrosa   | Nivel 1 (Alta incertidumbre) |
| < 1.5         | Baja toxicidad             | Nivel 0 (Riesgo mínimo)      |

---

## 3. Organización del Conocimiento

### 3.1. Jerarquía de Categorías de Riesgo

Cada compuesto está clasificado en una categoría principal:

- Inflamable
- Corrosivo
- Oxidante
- Tóxico
- Explosivo
- Radiactivo

Estas categorías se jerarquizan por nivel de riesgo para priorizar recomendaciones:

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

### 3.2. Asociación de Reglas y Conceptos

Cada categoría tiene asociadas tres reglas clave extraídas de `regulaciones_tdf.json`:

- **Descarte**: Proceso de disposición final.
- **Requisitos**: Condiciones de almacenamiento y manipulación.
- **Autoridad**: Ente regulador responsable.

**Ejemplo para `tóxico`:**

```json
{
  "descarte": "Prohibido absolutamente el descarte...",
  "requisitos": "Doble contenedor hermético...",
  "autoridad": "Secretaría de Ambiente Nacional"
}
```

---

## 4. Métodos de Inferencia

El sistema combina distintos tipos de inferencia:

- **Inferencia directa**: Basada en respuestas explícitas del usuario.
- **Inferencia aproximada**: Si la propiedad está marcada como “desconocida”, se suma la mitad del puntaje previsto.
- **Inferencia jerárquica**: Se elige la categoría de mayor riesgo entre las presentes y se aplican sus reglas.

---

## 5. Razonamiento del Sistema

El flujo del sistema es el siguiente:

1. **Entrada**: Usuario selecciona compuestos y responde propiedades.
2. **Agrupación**: Se consolidan las propiedades comunes de la mezcla.
3. **Evaluación**: Se calcula un puntaje total de toxicidad.
4. **Clasificación**: Se determina el nivel de riesgo con base en los puntajes.
5. **Recomendación**: Se consulta la regulación más estricta y se muestra al usuario.
6. **Registro**: La consulta se guarda en `historial.json` para trazabilidad.

---

## 6. Conclusión

Esta arquitectura permite mantener una clara separación entre conocimiento, lógica y presentación, haciendo el sistema:

- Extensible a nuevas categorías.
- Adaptable a nuevas reglas o jurisdicciones.
- Comprensible para usuarios y desarrolladores.
