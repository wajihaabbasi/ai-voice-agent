import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("voice_crud.middleware")

class CoreExceptionMiddleware(BaseHTTPMiddleware):
    """Catches backend errors gracefully to guarantee service resilience."""
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValueError as val_err:
            logger.warning(f"Intercepted input violation: {str(val_err)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": str(val_err)}
            )
        except Exception as global_err:
            logger.error(f"Uncaught execution exception: {str(global_err)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"status": "error", "message": "An unexpected pipeline failure occurred."}
            )