import json
import logging
import uuid
from typing import Optional, Tuple
from datetime import datetime
import redis # type: ignore

from brasiltransporta.infrastructure.config.settings import AppSettings
from brasiltransporta.domain.errors.errors import SecurityAlertError

logger = logging.getLogger(__name__)

class RefreshTokenService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.settings = AppSettings()
        self.namespace = self.settings.redis.refresh_token_namespace
        self.ttl = self.settings.redis.refresh_token_ttl

    def _get_key(self, user_id: str, token_family: str = None) -> str:
        """Generate Redis key for refresh token storage"""
        if token_family:
            return f"{self.namespace}:{user_id}:{token_family}"
        return f"{self.namespace}:{user_id}"

    def store_refresh_token(self, user_id: str, refresh_token: str, token_family: str = None) -> bool:
        """Store refresh token with token family in Redis"""
        try:
            # Generate token family if not provided
            if not token_family:
                token_family = str(uuid.uuid4())
            
            key = self._get_key(user_id, token_family)
            token_data = {
                "token": refresh_token,
                "created_at": datetime.utcnow().isoformat(),
                "used": False,
                "token_family": token_family
            }
            
            # Store with TTL
            result = self.redis.setex(
                key,
                self.ttl,
                json.dumps(token_data)
            )
            
            if result:
                logger.debug(f"Stored refresh token for user {user_id}, family {token_family}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error storing refresh token for user {user_id}: {e}")
            return False

    def verify_and_rotate(self, user_id: str, old_refresh_token: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Verify refresh token and rotate if valid
        """
        try:
            # Find all token families for this user
            pattern = self._get_key(user_id, "*")
            keys = self.redis.keys(pattern)
            
            for key in keys:  # ← Já é string por causa do decode_responses=True
                # key já é string, não precisa decode()
                token_data_str = self.redis.get(key)
                if not token_data_str:
                    continue
                    
                token_data = json.loads(token_data_str)
                
                # Check if this is the token we're looking for
                if (token_data["token"] == old_refresh_token and 
                    not token_data.get("used", False)):
                    
                    # Mark as used (single-use token)
                    token_data["used"] = True
                    token_data["used_at"] = datetime.utcnow().isoformat()
                    self.redis.setex(key, self.ttl, json.dumps(token_data))
                    
                    # Return token family for rotation
                    token_family = token_data.get("token_family")
                    
                    logger.info(f"Refresh token verified and marked as used for user {user_id}")
                    return True, token_family, None
            
                # Security alert: token reuse detected
                elif (token_data["token"] == old_refresh_token and 
                    token_data.get("used", False)):
                    logger.warning(f"Refresh token reuse detected for user {user_id} - possible security breach")
                    raise SecurityAlertError("Refresh token reuse detected - possible security breach")
        
            logger.warning(f"Invalid refresh token for user {user_id}")
            return False, None, "Invalid refresh token"
        
        except SecurityAlertError:
            raise
        except Exception as e:
            logger.error(f"Error verifying refresh token for user {user_id}: {e}")
            return False, None, str(e)

    def revoke_all_tokens(self, user_id: str) -> bool:
        """Revoke all refresh tokens for a user"""
        try:
            pattern = self._get_key(user_id, "*")
            keys = self.redis.keys(pattern)
            
            deleted_count = 0
            for key in keys:
                if self.redis.delete(key):
                    deleted_count += 1
            
            logger.info(f"Revoked {deleted_count} refresh tokens for user {user_id}")
            return deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error revoking tokens for user {user_id}: {e}")
            return False

    def get_active_sessions(self, user_id: str) -> list:
        """Get all active refresh token sessions for a user"""
        try:
            pattern = self._get_key(user_id, "*")
            keys = self.redis.keys(pattern)
            
            sessions = []
            for key_bytes in keys:
                key = key_bytes.decode('utf-8')
                token_data_str = self.redis.get(key)
                if token_data_str:
                    token_data = json.loads(token_data_str)
                    sessions.append({
                        "token_family": token_data.get("token_family"),
                        "created_at": token_data.get("created_at"),
                        "used": token_data.get("used", False),
                        "used_at": token_data.get("used_at"),
                        "key": key
                    })
            
            return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting active sessions for user {user_id}: {e}")
            return []

    def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens (Redis TTL should handle this, but this is a backup)"""
        # Redis automatically expires keys based on TTL
        # This method is just for manual cleanup if needed
        return 0