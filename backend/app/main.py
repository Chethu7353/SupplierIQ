from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

app = FastAPI(
    title="SupplierIQ API",
    description="Supply-chain risk analysis and crisis simulation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://refactored-funicular-r4q4jwvvp47rhxrg5-3000.app.github.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Password hashing
# --------------------------------------------------

password_hash = PasswordHash.recommended()

# Temporary storage. Replace with PostgreSQL later.
users_db = {}


# --------------------------------------------------
# Request models
# --------------------------------------------------

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SupplierIQ API is running"
    }


# --------------------------------------------------
# Project information
# --------------------------------------------------

@app.get("/about")
def project_name():
    return {
        "project_name": "SupplierIQ",
        "purpose": "Supply-chain risk analysis and crisis simulation",
        "framework": "FastAPI",
    }


# --------------------------------------------------
# Sample suppliers
# --------------------------------------------------

@app.get("/suppliers")
def get_suppliers():
    return {
        "suppliers": [
            {
                "supplier_id": 1,
                "name": "Supplier A",
                "on_time_delivery_rate": 95.5,
                "defect_rate": 2.1,
            },
            {
                "supplier_id": 2,
                "name": "Supplier B",
                "on_time_delivery_rate": 88.0,
                "defect_rate": 4.5,
            },
        ]
    }


# --------------------------------------------------
# Registration
# --------------------------------------------------

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterRequest):
    email = str(user.email).lower()

    if email in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    users_db[email] = {
        "name": user.name.strip(),
        "email": email,
        "password_hash": password_hash.hash(user.password),
    }

    return {
        "message": "Registration successful",
        "user": {
            "name": user.name.strip(),
            "email": email,
        },
    }


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.post("/login")
def login_user(credentials: LoginRequest):
    email = str(credentials.email).lower()
    user = users_db.get(email)

    if not user or not password_hash.verify(
        credentials.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"],
        },
    }