MONGODB_URL ='mongodb+srv://Paolaandrearodriguez:Paola201095@cluster0.dzdu5vo.mongodb.net/test'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.GestionPaquetes

db.getColletion("envio").agreggate(
    {
        $lookup: {
            from: "Paquetes",
            localField: "Paquetes",
            foreignField: "_id",
            as: "Paquetes"
        }
    }
)