from fastapi import FastAPI #se llama la clase Fastapi

app = FastAPI(title = "GestionPaquete",
              description="FastAPI de sistema de gestión de Paquetes",
              version="1.0.1") #() se coloca instacia


@app.get('/')
async def root():
    return 'Accediste a URL del servidor'

@app.get('/envios')
async def get_envios():
    return "Listado de envios realizados"

@app.get('/envios/{id_envio}')
async def get_envios(id_envio:int):
    return ("id_envio: ", id_envio)

@app.post('/envios')
async def save_envio():    
    return "Envio Completado"

@app.put('/envios/{id_envio}')
def update_envio():
    return "Registro Actualizado"


tipopaquete = [
    {"1":"Estandar"},
    {"2":"Tradicional"},
    {"3":"Dimensionado"}
]

@app.get('/tipopaquete/')
async def read_item(skip: int=0, limit: int = 2):
    return tipopaquete[skip : skip + limit]