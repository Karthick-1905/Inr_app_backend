import os
from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI
import uvicorn
from app.database import MongoDB
from app.routes.authRoutes import auth_router
from app.routes.adminRoutes import admin_router
from app.routes.doctorRoutes import doctor_router
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("static/patient_docs", exist_ok=True)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.get("/")
async def heath_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    await MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await MongoDB.disconnect()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router,prefix='/admin',tags=['Admin'])
app.include_router(doctor_router,prefix='/doctor',tags=['Doctor'])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=True)