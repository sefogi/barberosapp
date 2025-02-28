from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Barber(BaseModel):
    name: str = "Barber"
    
    location: str = "barcelona"
    neighborhood: str = "poble sec"
    # latitude: float = 0.123
    # longitude: float = 0.1234
    status: str = "available"
    rating: float = 5.0
    services: List[str] = ["haircut"]
    membership: bool = True

class Client(BaseModel):
    name: str = "sara"
    location: str = "barcelona"
    neiborhood: str = "poble sec"
    # latitude: float = 0.123
    # longitude: float = 0.1234
    payment_methods: List[str] = ["cash"]

class Service(BaseModel):
    barber_id: str = "1"
    client_id: str = "1"
    service_type: str = "haircut"
    date: datetime = datetime.now()
    status: str = "completed"
    rating: Optional[float] = None # agregar calificacion al servicio.

class Payment(BaseModel):
    service_id: str = "1"
    amount: float = 15.0
    payment_method: str = "cash"
    status: str = "pending"