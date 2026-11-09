"""Request limits per client."""
import time


class FixedWindowLimiter:
    """Allows `limit` requests per client in each `window` seconds."""

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.counts = {}

    def check(self, key):
        now = time.time()
        start, count = self.counts.get(key, (now, 0))
        if now - start >= self.window:
            start, count = now, 0
        if count >= self.limit:
            return False
        self.counts[key] = (start, count + 1)
        return True
