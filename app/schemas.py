from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BarberCreate(BaseModel):
    name: str = "Barber"
    location: str = "barcelona"
    neighborhood: str = "poble sec"
    # latitude: float
    # longitude: float
    services: List[str] = ["haircut"]

class BarberUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[float] = None
    membership: Optional[bool] = None

class ClientCreate(BaseModel):
    name: str = "sara"
    location: str = "barcelona"
    neighborhood: str = "poble sec"
    # latitude: float
    # longitude: float
    payment_methods: List[str] = ["cash"]

class ServiceCreate(BaseModel):
    barber_id: str = "1"
    client_id: str = "1"
    service_type: str = "haircut"

class PaymentCreate(BaseModel):
    service_id: str = "1"
    amount: float = 10.0
    payment_method: str = "cash"