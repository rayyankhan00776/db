from fastapi import HTTPException, Header
import jwt

def auth_middleware(x_auth_token = Header()):
    try:
        if not x_auth_token:
            raise HTTPException(401, "No auth token provided")
        
        # Decode JWT token
        verified_token = jwt.decode(x_auth_token, 'password_key', algorithms=["HS256"])
        uid = verified_token.get('id')

        if not uid:
            raise HTTPException(401, "Token invalid, authorization denied")

        return {'uid': uid, 'token': x_auth_token}

    except jwt.PyJWTError:
        raise HTTPException(401, "Token is not valid, authorization failed")