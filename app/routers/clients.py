# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException
from app.databases import get_database
from app.models import Client
from app.schemas import ClientCreate
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter()

@router.post("/", response_model=Client)
async def create_client(client: ClientCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_client = Client(**client.model_dump())
    result = await db.clients.insert_one(new_client.model_dump())
    created_client = await db.clients.find_one({"_id": result.inserted_id})
    return Client(**created_client)

@router.get("/", response_model=List[Client])
async def read_clients(db: AsyncIOMotorDatabase = Depends(get_database)):
    clients = []
    async for client in db.clients.find():
        clients.append(Client(**client))
    return clients

@router.get("/{name}", response_model=Client)
async def read_client(name: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    client = await db.clients.find_one({"name": name})
    if client:
        return Client(**client)
    else:
        raise HTTPException(status_code=404, detail="Client not found")

# Implementa las rutas para actualizar y eliminar clientes aquí