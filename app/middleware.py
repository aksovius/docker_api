from fastapi import  Request
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import jwt

class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path == "/graphql":
            auth_header = request.headers.get("Authorization")
            if auth_header:
                token = auth_header.split(" ")[-1]  # Extract the token from the header
                decoded = jwt.decode(token, 'secret key for jwt token generation and verification', algorithms=['HS256']) # Validate the token
                access = decoded['access']
                if access == "admin" or access == "teacher": 
                    response = await call_next(request)  # Continue to the next middleware or route
                    return response
                else:
                    print("Unauthorized")
                    return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)
            else:     
                print("Unauthorized")
                return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)
        else:
            return await call_next(request)