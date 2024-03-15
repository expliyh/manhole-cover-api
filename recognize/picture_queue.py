import queue


class RecognizeTask:
    def __init__(self, pid: int, picture: bytes):
        self.pid = pid
        self.picture = picture


picture_queue = queue.Queue()
