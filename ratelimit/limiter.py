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

    def remaining(self, key):
        """How many more requests `key` can make in the current window."""
        start, count = self.counts.get(key, (time.time(), 0))
        if time.time() - start >= self.window:
            return self.limit
        return max(self.limit - count, 0)
