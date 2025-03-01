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
    result = await db.services.insert_one(new_service.model_dump())
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
    if updated_service:
        barber = await db.barbers.find_one({"_id": updated_service["barber_id"]})
        if barber:
            # Calculate the new average rating
            total_ratings = barber.get("total_ratings", 0) + 1
            new_rating = ((barber["rating"] * barber.get("total_ratings", 0)) + rating) / total_ratings
            await db.barbers.find_one_and_update(
                {"_id": updated_service["barber_id"]},
                {"$set": {"rating": new_rating, "total_ratings": total_ratings}},
            )

        return Service(**updated_service)
    else:
        raise HTTPException(status_code=404, detail="Service not found")

# Implementa las rutas para actualizar y eliminar servicios aquí
@router.put("/{service_id}", response_model=Service)
async  def update_service(service_id: str, service: ServiceCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated_service = await db.services.find_one_and_update(
        {"_id": service_id},
        {"$set": service.model_dump(exclude_unset=True)},
        return_document=True
    )
    if updated_service:
        return Service(**updated_service)
    else:
        raise HTTPException(status_code=404, detail="Service not found")