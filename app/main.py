# app/main.py
from fastapi import FastAPI
from app.routers import barbers, clients, services, payments

app = FastAPI()

app.title = "Barbers API"
app.version = "0.1.0"
app.description = "API for barbers and clients to manage appointments and payments"

app.include_router(barbers.router, prefix="/barbers", tags=["barbers"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])