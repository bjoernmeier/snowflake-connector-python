import logging
from threading import RLock, Lock


class LogLock:
    def __init__(self, name):
        self.name = str(name)
        self.lock = Lock()
        self.logger = logging.getLogger("snowflake")

    def acquire(self, blocking=True, timeout=-1):
        self.logger.debug(f"Trying to acquire {self.name} lock")
        ret = self.lock.acquire(blocking=blocking, timeout=timeout)
        if ret:
            self.logger.debug(f"Acquired {self.name} lock")
        else:
            self.logger.debug(f"Non-blocking or timeout acquire of {1} lock failed, with blocking {blocking} and timeout {timeout}")
        return ret

    def release(self):
        self.logger.debug(f"Releasing {self.name} lock")
        self.lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class LogRLock:
    def __init__(self, name):
        self.name = str(name)
        self.lock = RLock()
        self.logger = logging.getLogger()

    def acquire(self, blocking=True, timeout=-1):
        self.logger.debug(f"Trying to acquire {self.name} lock")
        ret = self.lock.acquire(blocking=blocking, timeout=timeout)
        if ret:
            self.logger.debug(f"Acquired {self.name} lock")
        else:
            self.logger.debug(f"Non-blocking or timeout acquire of {1} lock failed, with blocking {blocking} and timeout {timeout}")
        return ret

    def release(self):
        self.logger.debug(f"Releasing {self.name} lock")
        self.lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
