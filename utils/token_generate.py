from datetime import datetime, timedelta
from jose import jwt
from config.config import settings

def create_access_token(data: dict):
    """
    Generate a JWT access token.

    Args:
        data (dict): The data to encode in the JWT. Typically, this includes information like the user's ID or email.

    Returns:
        str: The encoded JWT token as a string.
    """
    # Create a copy of the data to be encoded into the token
    to_encode = data.copy()

    # Calculate the expiration time for the token
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the data to be encoded
    to_encode.update({"exp": expire})
    
    # Encode the data into a JWT token using the secret key and algorithm defined in the settings
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Return the encoded JWT token
    return encoded_jwt
