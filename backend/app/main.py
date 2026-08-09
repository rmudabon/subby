from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import DomainException
from app.api.router import api_router

app = FastAPI(root_path="/api")
app.include_router(api_router)

@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )