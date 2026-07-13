from arq.connections import RedisSettings
from app.core.config import settings

async def sample_background_task(ctx, message: str):
    print(f"Background task received: {message}")
    return f"Processed: {message}"

class WorkerSettings:
    functions = [sample_background_task]
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
