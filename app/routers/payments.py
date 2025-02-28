# app/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException
from app.databases import get_database
from app.models import Payment
from app.schemas import PaymentCreate
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter()

@router.post("/", response_model=Payment)
async def create_payment(payment: PaymentCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_payment = Payment(**payment.model_dump())
    result = await db.payments.insert_one(new_payment.model_dump())
    created_payment = await db.payments.find_one({"_id": result.inserted_id})
    return Payment(**created_payment)

@router.get("/", response_model=List[Payment])
async def read_payments(db: AsyncIOMotorDatabase = Depends(get_database)):
    payments = []
    async for payment in db.payments.find():
        payments.append(Payment(**payment))
    return payments

@router.get("/{payment_id}", response_model=Payment)
async def read_payment(payment_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    payment = await db.payments.find_one({"_id": payment_id})
    if payment:
        return Payment(**payment)
    else:
        raise HTTPException(status_code=404, detail="Payment not found")

# Implementa las rutas para actualizar y eliminar pagos aquí