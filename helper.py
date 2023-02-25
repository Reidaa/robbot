from datetime import datetime, timedelta
from typing import Dict, Callable


def cooldown(duration: float):
    last_called: Dict[Callable, datetime] = {}

    def decorator(wrapped: Callable):
        async def wrapper(*args, **kwargs):
            # Check when the function was last called
            now = datetime.now()
            if (wrapped in last_called) and (now - last_called[wrapped] < timedelta(seconds=duration)):
                return  # Do nothing

            # Call the wrapped function and update the last called time
            result = await wrapped(*args, **kwargs)
            last_called[wrapped] = now
            return result

        return wrapper

    return decorator
