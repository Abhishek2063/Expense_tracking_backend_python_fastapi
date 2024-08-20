from fastapi import FastAPI, status,Request
from seedings.seed import seed_data
from utils.message import VALIDATION_ERROR, WELCOME_MESSAGE
from utils.response import create_response
from routes.user_routes import router as user_router
seed_data()
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []

    for error in errors:
        formatted_errors.append({"field": error["loc"][-1], "message": error["msg"]})

    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "success": False,
            "message": VALIDATION_ERROR,
            "errors": formatted_errors,
        },
    )
    
app.include_router(user_router)


@app.get("/")
def read_root():
    return create_response(status.HTTP_200_OK, True, WELCOME_MESSAGE)
