from fastapi import FastAPI #se llama la clase Fastapi
import os
from fastapi import FastAPI, Body,HTTPException, status 
from fastapi.responses import Response, JSONResponse 
from fastapi.encoders import jsonable_encoder 
from pydantic import BaseModel, Field, EmailStr 
from bson import ObjectId 
from typing import Optional, List 
import motor.motor_asyncio


app = FastAPI(title = "GestionPaquete",
              description="FastAPI de sistema de gestión de Paquetes",
              version="1.0.1") #() se coloca instacia


MONGODB_URL ='mongodb+srv://Paolaandrearodriguez:Paola201095@cluster0.dzdu5vo.mongodb.net/test'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.GestionPaquetes

   

class PyObjectId(ObjectId):
    @classmethod 
    def __get_validators__(cls):
        yield cls.validate 
          
    @classmethod 
    def validate(cls, v): 
        if not ObjectId.is_valid(v): 
            raise ValueError("Invalid objectid") 
        return ObjectId(v)

    @classmethod 
    def __modify_schema__(cls, field_schema): 
        field_schema.update(type="string, i")#modificado


class EnviosModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id") # llama el id de la base de datos al API
    NombreRemitente: str = Field("")
    CedulaRemitente: int = Field("")
    CiudadRemitente: str = Field("")
    DireccionRemitente: str = Field("")
    TelefonoRemitente: int = Field("")
    NombreDestinatario: str = Field("")
    CedulaDestinatario: int = Field("")
    CiudadDestinatario: str = Field("")
    DireccionDestinatario: str = Field("")
    TelefonoDestinatario: int = Field("")
    ValorEnvio: int = Field("")
    FechaEnvio: str = Field("")
    TipoPaquete: str = Field("")#debe ser tipo de seleccion en html
    
 
    
    class Config:
        allow_population_by_field_name = True 
        arbitrary_types_allowed = True 
        json_encoders = {ObjectId: str} #convierte ObjectId en str
        schema_extra = { 
            "example": { 
                "NombreRemitente": "",
                "CedulaRemitente": "",
                "DireccionRemitente": "",
                "TelefonoRemitente": "",
                "CiudadRemitente":"",
                "NombreDestinatario": "",
                "CedulaDestinatario": "",
                "DireccionDestinatario": "",
                "TelefonoDestinatario": "",
                "CiudadDestinatario":"",
                "ValorEnvio": "",
                "FechaEnvio": "",
                "TipoPaquete": ""
            }
        } 

class EnviosUpdateModel(BaseModel):
    NombreRemitente: Optional[str]
    CedulaRemitente: Optional[int]
    CiudadRemitente:  Optional[str]
    DireccionRemitente: Optional[str]
    TelefonoRemitente: Optional[int]
    NombreDestinatario:  Optional[str]
    CedulaDestinatario: Optional[int]
    CiudadDestinatario: Optional[str]
    DireccionDestinatario: Optional[str]
    TelefonoDestinatario: Optional[int]
    ValorEnvio: Optional[int]
    FechaEnvio: Optional[str]
    TipoPaquete: Optional[str]

    class Config:
        allow_population_by_field_name = True 
        arbitrary_types_allowed = True 
        json_encoders = {ObjectId: str} #convierte ObjectId en str
        schema_extra = { 
            "example": { 
                "NombreRemitente": "",
                "CedulaRemitente": "",
                "DireccionRemitente": "",
                "TelefonoRemitente": "",
                "CiudadRemitente":"",
                "NombreDestinatario": "",
                "CedulaDestinatario": "",
                "DireccionDestinatario": "",
                "TelefonoDestinatario": "",
                "CiudadDestinatario":"",
                "ValorEnvio": "",
                "FechaEnvio": "",
                "TipoPaquete": ""
            }
        } 



#en el formulario del paquete, preguntar si desea enviar otro paquete.

@app.get("/", response_description="List all Shipment",response_model=List[EnviosModel] )
async def find_all_Shipment(): 
   shipment = await db["envio"].find().to_list(1000) 
   return shipment

@app.post("/", response_description="Add new Shipmentg",response_model=EnviosModel) 
async def create_Shipment(envio: EnviosModel = Body(...)): 
   envio = jsonable_encoder(envio) 
   new_envio = await db["envio"].insert_one(envio) 
   created_envio = await db["envio"].find_one({"_id": new_envio.inserted_id}) 
   return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_envio)
   

@app.get("/{id}", response_description="Get a single Shipment" ) 
async def show_Shipment(id: str): 
    if (Shipment := await db["envio"].find_one({"_id": id})): 
        return Shipment

    raise HTTPException(status_code=404, detail=f"Shipment {id} not found")

@app.put("/{id}", response_description="Update a Shipment", response_model=EnviosModel) 
async def update_Shipment(id: str, Shipment: EnviosUpdateModel): 
    Shipment = {k: v for k, v in Shipment.dict().items() if v is not None}

    if len(Shipment) >= 1: 
     update_result = await db["envio"].update_one({"_id": id}, {"$set": Shipment})
     
     if update_result.modified_count == 1: 
            if (
                updated_Student := await db["envio"].find_one({"_id": id})
            ) is not None:
                return updated_Student
        
    if (existing_Student := await db["envio"].find_one({"_id": id})) is not None:
         return existing_Student
    
    raise HTTPException(status_code=404, detail=f"Shipment {id} not found")

@app.delete("/{id}", response_description="Delete a Shipment") 
async def delete_Student(id: str): 
    delete_result = await db["envio"].delete_one({"_id": id})    
    if delete_result.deleted_count == 1: 
        return Response(status_code=status.HTTP_204_NO_CONTENT) 
    raise HTTPException(status_code=404, detail=f"Shipment {id} not found")

                          