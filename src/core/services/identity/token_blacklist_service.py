from datetime import datetime, timezone, timezone
from jose import jwt, JWTError
from src.common.config.env_config import EnvConfig
from src.common.config.redis_client import RedisClient

class TokenBlackListService:

    @classmethod
    async def add_token(cls, token: str):
        try:
            payload = jwt.decode(token, EnvConfig.JWT_SECRET_KEY, algorithms=[EnvConfig.JWT_ALGORITHM])
            exp = payload.get("exp")
            if exp:
                now = int(datetime.now(tz=timezone.utc).timestamp())
                ttl = exp - now
                if ttl > 0:
                    await RedisClient.setex(f"blacklist:{token}", ttl, "1")
        except JWTError:
            pass 


    @classmethod
    async def is_blacklisted(cls, token: str) -> bool:
        return await RedisClient.exists(f"blacklist:{token}")
