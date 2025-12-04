import time
from collections import deque
from threading import Lock

class RateLimiter:
    def __init__(self, max_calls: int, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.timestamps = deque()
        self.lock = Lock()

    def wait(self):
        with self.lock:
            while True:
                now = time.time()
                while self.timestamps and now - self.timestamps[0] > self.period:
                    self.timestamps.popleft()

                if len(self.timestamps) < self.max_calls:
                    self.timestamps.append(now)
                    return
                
                sleep_time = self.timestamps[0] + self.period - now
                if sleep_time > 0:
                    time.sleep(sleep_time + 0.1)