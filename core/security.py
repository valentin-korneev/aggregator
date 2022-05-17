from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request
from pydantic import ValidationError
from core.config import config
from jose import JWTError, jwt
from core.constants import BEARER
from utils.localization import _
from core.schemas.tokens import TokenUser, TokenData
from fastapi.security.oauth2 import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from typing import Optional, Dict, Any
from fastapi.security.utils import get_authorization_scheme_param


class CredentialException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        authenticate_value: str = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': authenticate_value}
        )


class ForbiddenException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        authenticate_value: str = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={'WWW-Authenticate': authenticate_value} if authenticate_value else dict()
        )


class OAuth2PasswordBearer(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        refreshUrl: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={'tokenUrl': tokenUrl, 'scopes': scopes, 'refreshUrl': refreshUrl})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != BEARER.lower():
            if self.auto_error:
                raise CredentialException(
                    _(request, 'errors.auth.not_authenticated'),
                    authenticate_value=BEARER
                )
            else:
                return None
        return param


def parseJWT(r: Request, token: str) -> TokenData:
    credential_exception = CredentialException(
        _(r, 'errors.auth.compromised_credential'),
        authenticate_value=BEARER
    )
    try:
        # exp проверяется автоматически
        payload = jwt.decode(
            token,
            config.security.KEY.get_secret_value(),
            algorithms=[config.security.ALGORITHM]
        )
        user: str = TokenUser(**payload.get('user'))
        if not user:
            raise credential_exception
    except (JWTError, ValidationError):
        raise credential_exception
    return TokenData(user=user, scopes=payload.get('scopes', []))


def createJWT(data: TokenData, ttl: int = config.security.ACCESS_TOKEN_TTL) -> Any:
    return jwt.encode(
        data.dict() | {'exp': datetime.utcnow() + timedelta(minutes=ttl)},
        config.security.KEY.get_secret_value(),
        algorithm=config.security.ALGORITHM
    )


def verify_password(plain_password, hashed_password):
    return config.security.PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
    return config.security.PWD_CONTEXT.hash(password)