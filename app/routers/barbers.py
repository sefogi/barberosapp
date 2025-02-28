from fastapi import APIRouter, Depends, HTTPException, Query
from app.databases import get_database
from app.models import Barber
from app.schemas import BarberCreate, BarberUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter()

@router.post("/", response_model=Barber)
async def create_barber(barber: BarberCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_barber = Barber(**barber.model_dump())
    result = await db.barbers.insert_one(new_barber.model_dump())
    created_barber = await db.barbers.find_one({"_id": result.inserted_id})
    return Barber(**created_barber)

@router.get("/", response_model=List[Barber])
async def read_barbers(db: AsyncIOMotorDatabase = Depends(get_database)):
    barbers = []
    async for barber in db.barbers.find():
        barbers.append(Barber(**barber))
    return barbers

@router.put("/{barber_id}", response_model=Barber)
async def update_barber(barber_id: str, barber: BarberUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated_barber = await db.barbers.find_one_and_update(
        {"_id": barber_id},
        {"$set": barber.model_dump(exclude_unset=True)},
        return_document=True
    )
    if updated_barber:
        return Barber(**updated_barber)
    else:
        raise HTTPException(status_code=404, detail="Barber not found")

@router.get("/{barber_id}", response_model=Barber)
async def read_barber(barber_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    barber = await db.barbers.find_one({"_id": barber_id})
    if barber:
        return Barber(**barber)
    else:
        raise HTTPException(status_code=404, detail="Barber not found")
    

@router.get("/search/", response_model=List[Barber])
async def search_barbers(
    neighborhood: str = Query(..., description="Client neighborhood"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    query = {
        "neighborhood": neighborhood
    }
    barbers = []
    async for barber in db.barbers.find(query):
        barbers.append(Barber(**barber))
    return barbers

@router.put("/{barber_id}/membership/", response_model=Barber)
async def update_membership(
    barber_id: str,
    membership: bool = Query(..., description="Membership status"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    updated_barber = await db.barbers.find_one_and_update(
        {"_id": barber_id},
        {"$set": {"membership": membership}},
        return_document=True,
    )
    if updated_barber:
        return Barber(**updated_barber)
    else:
        raise HTTPException(status_code=404, detail="Barber not found")

@router.get("/{barber_id}/membership/", response_model=bool)
async def check_membership(
    barber_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    barber = await db.barbers.find_one({"_id": barber_id})
    if barber:
        return barber["membership"]
    else:
        raise HTTPException(status_code=404, detail="Barber not found")



