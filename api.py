from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from logic import SistemaExpertoQuimico

app = FastAPI(title="Sistema Experto Químico")

# Permitir acceso desde el navegador/web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sistema = SistemaExpertoQuimico()

class EvaluacionRequest(BaseModel):
    ids: List[int]
    respuestas: Dict[str, str]

@app.get("/")
def read_root():
    return {"mensaje": "API del Sistema Experto Químico ONLINE"}

@app.get("/compuestos")
def get_compuestos():
    return sistema.compuestos

@app.post("/evaluar")
def evaluar_mezcla(request: EvaluacionRequest):
    try:
        sustancia = sistema.combinar_compuestos(request.ids)
        nivel, detalle = sistema.evaluar_toxicidad(request.respuestas)
        recomendaciones = sistema.generar_recomendaciones(sustancia, nivel)
        sistema.registrar_consulta(sustancia['nombres'], (nivel, detalle))

        return {
            "compuestos": sustancia['nombres'],
            "nivel_toxicidad": nivel,
            "detalle": detalle,
            "recomendaciones": recomendaciones
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historial")
def get_historial():
    return sistema.obtener_historial()

