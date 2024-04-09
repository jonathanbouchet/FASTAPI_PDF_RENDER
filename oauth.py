from fastapi import status, Depends, HTTPException
from fastapi.security import APIKeyHeader

oauth2_scheme = APIKeyHeader(name="X-API-Key") 
X_API_KEY = "1234"

def api_auth_key(api_key: str = Depends(oauth2_scheme)):
    """
    Takes the X-API-Key header and validate it with the X-API-Key in the database/environment
    solution: https://stackoverflow.com/questions/48218065/objects-created-in-a-thread-can-only-be-used-in-that-same-thread
    :param api_key:
    :return:
    """
    print(f"in api_auth_key")
    if api_key != X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header."
        )