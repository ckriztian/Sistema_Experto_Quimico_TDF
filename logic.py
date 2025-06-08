import json
from typing import Dict, List, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
import os

class SistemaExpertoQuimico:
    def __init__(self):
        self.cargar_datos()
        self.historial_file = 'historial.json'
        self.inicializar_historial()

    def cargar_datos(self):
        with open('compuestos.json', 'r', encoding='utf-8') as f:
            self.compuestos = json.load(f)['compuestos']

        with open('regulaciones_tdf.json', 'r', encoding='utf-8') as f:
            self.regulaciones = json.load(f)

    def inicializar_historial(self):
        if not os.path.exists(self.historial_file):
            with open(self.historial_file, 'w') as f:
                json.dump({"consultas": []}, f)

    def combinar_compuestos(self, ids: List[int]) -> Dict:
        seleccionados = [c for c in self.compuestos if c['id'] in ids]
        phs = [c['pH'] for c in seleccionados if c['pH'] is not None]
        ph_promedio = sum(phs)/len(phs) if phs else None

        return {
            "nombres": [c['nombre'] for c in seleccionados],
            "categorias": list(set(c['categoria'] for c in seleccionados)),
            "pH": ph_promedio,
            "inflamable": any(c['inflamable'] for c in seleccionados),
            "reactivo": any(c['reactivo'] for c in seleccionados),
            "volatil": any(c['volatil'] for c in seleccionados),
            "metales_pesados": any(c['metales_pesados'] for c in seleccionados),
            "explosivo": any(c.get('explosivo', False) for c in seleccionados),
            "radiactivo": any(c.get('radiactivo', False) for c in seleccionados)
        }

    def evaluar_toxicidad(self, respuestas: Dict) -> Tuple[str, str]:
        toxicidad = 0
        if respuestas['pH'] == 'si':
            toxicidad += 2
        elif respuestas['pH'] == 'desconocido':
            toxicidad += 1.5

        propiedades = {
            'inflamable': 1,
            'reactivo': 1,
            'metales_pesados': 3,
            'volatil': 1,
            'explosivo': 4,
            'radiactivo': 5
        }

        for prop, puntos in propiedades.items():
            if respuestas.get(prop) == 'si':
                toxicidad += puntos
            elif respuestas.get(prop) == 'desconocido':
                toxicidad += puntos * 0.5

        if toxicidad >= 5:
            return "Extremadamente tóxica", "Nivel 4 (Alta certeza)"
        elif toxicidad >= 4:
            return "Altamente tóxica", "Nivel 3 (Probable)"
        elif toxicidad >= 2.5:
            return "Moderadamente tóxica", "Nivel 2 (Incertidumbre)"
        elif toxicidad >= 1.5:
            return "Potencialmente peligrosa", "Nivel 1 (Alta incertidumbre)"
        return "Baja toxicidad", "Nivel 0 (Riesgo mínimo)"

    def generar_recomendaciones(self, sustancia: Dict, nivel: str) -> str:
        recomendaciones = []
        categorias = sustancia.get('categorias', [])
        regulaciones = self.regulaciones.get('regulaciones', {})

        if not categorias:
            recomendaciones.append("⚠️ Categoría desconocida. Aplicar precauciones generales.")
        else:
            prioridades = {
                'radiactivo': 6,
                'explosivo': 5,
                'tóxico': 4,
                'oxidante': 3,
                'corrosivo': 2,
                'inflamable': 1
            }
            cat_mas_peligrosa = max(categorias, key=lambda c: prioridades.get(c, 0))
            reg = regulaciones.get(cat_mas_peligrosa, regulaciones.get('default'))
            recomendaciones.append(
                f"\n📌 {cat_mas_peligrosa.upper()}:\n"
                f"- DESCARTE: {reg['descarte']}\n"
                f"- REQUISITOS: {reg['requisitos']}\n"
                f"- AUTORIDAD: {reg['autoridad']}"
            )

        contactos = self.regulaciones.get('contactos_emergencia', {})
        recomendaciones.append(
            f"\n🚨 CONTACTOS ({nivel}):\n"
            f"- Bomberos: {contactos.get('bomberos', 'N/D')}\n"
            f"- Ambiente TDF: {contactos.get('ambiente_tdf', 'N/D')}\n"
            f"- Toxicológico: {contactos.get('toxicologico', 'N/D')}\n"
            f"- Materiales peligrosos: {contactos.get('materiales_peligrosos', 'N/D')}\n"
            f"- Nuclear: {contactos.get('nuclear', 'N/D')}\n"
        )

        if sustancia.get('pH') is None:
            recomendaciones.append(
                "\n⚠️ PRECAUCIÓN: pH desconocido\n"
                "- Considerar neutralización completa\n"
                "- Usar equipo de protección completo"
            )

        return '\n'.join(recomendaciones)

    def generar_grafico_riesgo(self, nivel_toxicidad: str) -> plt.Figure:
        niveles = ["Nivel 0", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4"]
        valores = [0, 1.5, 2.5, 4, 5]
        nivel_actual = next((i for i, n in enumerate(niveles) if n in nivel_toxicidad), 0)

        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['green', 'yellowgreen', 'yellow', 'orange', 'red']
        bars = ax.bar(niveles, valores, color=colors)
        bars[nivel_actual].set_edgecolor('black')
        bars[nivel_actual].set_linewidth(2)

        ax.set_title('Niveles de Toxicidad', pad=20)
        ax.set_ylabel('Puntuación de Riesgo')
        ax.set_ylim(0, 5.5)
        ax.axhline(y=2.5, color='red', linestyle='--', alpha=0.3)
        ax.text(4.2, 2.7, 'Límite peligroso', color='red')

        fig.tight_layout()
        return fig

    def registrar_consulta(self, compuestos: List[str], resultado: Tuple[str, str]):
        with open(self.historial_file, 'r+') as f:
            data = json.load(f)
            data['consultas'].append({
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "compuestos": compuestos,
                "nivel_toxicidad": resultado[0],
                "detalle": resultado[1]
            })
            f.seek(0)
            json.dump(data, f, indent=2)

    def obtener_historial(self) -> List[Dict]:
        with open(self.historial_file, 'r') as f:
            return json.load(f)['consultas']
