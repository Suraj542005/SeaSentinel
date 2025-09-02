import os
import time
import json
import requests
import jwt
from jwt import algorithms

CLERK_ISSUER = os.getenv("CLERK_ISSUER")
CLERK_AUDIENCE = os.getenv("CLERK_AUDIENCE")
JWKS_URL = f"{CLERK_ISSUER}/.well-known/jwks.json"
JWKS_CACHE_TTL = 60 * 60  # 1 hour cache

_jwks = None
_jwks_last = 0

def get_jwks():
    global _jwks, _jwks_last
    if _jwks is None or time.time() - _jwks_last > JWKS_CACHE_TTL:
        res = requests.get(JWKS_URL)
        res.raise_for_status()
        _jwks = res.json()
        _jwks_last = time.time()
    return _jwks

def verify_clerk_token(token: str):
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    if not kid:
        raise Exception("No 'kid' found in token header")

    jwks = get_jwks()
    key_jwk = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if not key_jwk:
        raise Exception("Public key not found in JWKS")

    public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(key_jwk))

    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=CLERK_AUDIENCE,
        issuer=CLERK_ISSUER,
    )
    return payload
