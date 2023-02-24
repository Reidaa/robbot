from datetime import datetime, timedelta


def cooldown(duration):
    last_called = {}

    def decorator(wrapped):
        async def wrapper(*args, **kwargs):
            # Check when the function was last called
            now = datetime.now()
            if wrapped in last_called and now - last_called[wrapped] < timedelta(seconds=duration):
                return  # Do nothing

            # Call the wrapped function and update the last called time
            result = await wrapped(*args, **kwargs)
            last_called[wrapped] = now
            return result

        return wrapper

    return decorator
