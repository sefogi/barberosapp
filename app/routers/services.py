# app/routers/services.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.databases import get_database
from app.models import Service
from app.schemas import ServiceCreate
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Service)
async def create_service(service: ServiceCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_service = Service(**service.model_dump(), date=datetime.now())
    result = await db.services.insert_one(new_service.dict())
    created_service = await db.services.find_one({"_id": result.inserted_id})
    return Service(**created_service)

@router.get("/", response_model=List[Service])
async def read_services(db: AsyncIOMotorDatabase = Depends(get_database)):
    services = []
    async for service in db.services.find():
        services.append(Service(**service))
    return services

@router.get("/{service_id}", response_model=Service)
async def read_service(service_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    service = await db.services.find_one({"_id": service_id})
    if service:
        return Service(**service)
    else:
        raise HTTPException(status_code=404, detail="Service not found")
    
    

@router.put("/{service_id}/rate/", response_model=Service)
async def rate_service(
    service_id: str,
    rating: float = Query(..., description="Service rating"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    service = await db.services.find_one({"_id": service_id})
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    updated_service = await db.services.find_one_and_update(
        {"_id": service_id},
        {"$set": {"rating": rating}},
        return_document=True,
    )

    # Actualizar la calificación del barbero
    barber = await db.barbers.find_one({"_id": updated_service["barber_id"]})
    if barber:
        new_rating = (barber["rating"] + rating) / 2 # aqui deberia ir una logica que promedie con todas las calificaciones.
        await db.barbers.find_one_and_update(
            {"_id": updated_service["barber_id"]},
            {"$set": {"rating": new_rating}},
        )

    return Service(**updated_service)

# Implementa las rutas para actualizar y eliminar servicios aquí