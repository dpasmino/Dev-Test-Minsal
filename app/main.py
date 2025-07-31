from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler
from app.schemas import UserCreate, UserOut
from app.crud import create_user, get_user_by_email
from app.auth import create_access_token
from app.validation import is_valid_email, is_valid_password
from datetime import datetime
from passlib.context import CryptContext
import uuid

#bcrypt context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize FastAPI app
app = FastAPI()

# Custom exception handler for validation errors, which provides detailed error messages for missing fields and type errors
@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []
    type_errors = []

    for error in exc.errors():
        field = error["loc"][-1]
        if error["type"] == "value_error.missing":
            missing_fields.append(field)
        else:
            type_errors.append((field, error["msg"]))

    messages = []
    if missing_fields:
        messages.append(f"Missing required fields: {', '.join(missing_fields)}")
    if type_errors:
        for field, msg in type_errors:
            messages.append(f"Invalid value for '{field}': {msg}")

    return JSONResponse(
        status_code=400,
        content={"detail": messages}
    )

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Post endpoint to register a new user
@app.post("/users", response_model=UserOut)
async def register_user(user: UserCreate):

    # Check if the email is already registered
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    # Check if the email and password are valid
    valid_email = is_valid_email(user.email)
    if not valid_email:
        raise HTTPException(status_code=400, detail="El correo no es válido.")
    
    valid_password = is_valid_password(user.password)
    if not valid_password:
        raise HTTPException(status_code=400, detail="La contraseña no es válida, debe incluir al menos una letra mayúscula, una letra minúscula, y dos números.")
    
    # Create a unique user ID with UUID4, hash the password, get the current time, create a token usng JWT, and set the user as active
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user.password)
    current_time = datetime.now().isoformat()
    user_token = create_access_token(data={"sub": user.email})
    user_isactive = True
    
    # Create a user dictionary
    hashed_user = {
        "username": user.username,
        "email": user.email,
        "user_id": user_id,
        "phones": [dict(phone) for phone in user.phones],
        "created": current_time,
        "modified": current_time,
        "last_login": current_time,
        "token": user_token,
        "isactive": user_isactive,
        "password": hashed_password,
    }
    # Insert the user dictionary into the database and return the user id (UUID4)
    user_id = await create_user(hashed_user)
    
    # Return the user data in the UserOut schema format
    return UserOut(username=user.username, email=user.email, id=user_id, created=current_time, modified=current_time,
                   last_login=current_time, token=user_token, isactive=user_isactive)