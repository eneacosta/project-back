import jwt
import datetime

SECRET_KEY = "SOY_UNA_CLAVE_SECRETA"

def encode_auth_token(user_id, minutes=60):
    """
    Genera el token JWT
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodifica el token y devuelve solo el ID del usuario
    :param auth_token:
    :return: integer|string
    """
    try:
        if not auth_token: raise HTTPException("Token invalido", status_code=401)
        auth_token = auth_token.split(" ")[1]
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException("Token expirado", status_code=401)
    except jwt.InvalidTokenError:
        raise HTTPException("Token invalido", status_code=401)



class HTTPException(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        body =  {
            "message":self.message,   
        }
        if self.payload:
            body["payload"] = self.payload
        return body
    
    def response(self):
        return self.to_dict(), self.status_code, {'ContentType':'application/json'} 
    
    @staticmethod
    def unespected(message):
        return {'message':f'Error inesperado: {message}'}, 500, {'ContentType':'application/json'} 

    @staticmethod
    def simple_message(message):
        return {'message':f'{message}'}, 500, {'ContentType':'application/json'} 

