from datetime import datetime, timedelta
from jose import JWTError, jwt

# Secret key for JWT encoding and decoding
# In a real application, this should be kept secret and not hardcoded
SECRET_KEY = "super-secret-key"
# Algorithm used for JWT encoding
ALGORITHM = "HS256"
# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt