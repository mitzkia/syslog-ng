|from multiprocessing import Process, Manager

class ThreadPool(object):
    def __init__(self):
        self.process_pool = []

    def __del__(self):
        for process in self.process_pool:
            if process.is_alive:
                process.join()

    def start_process(self, args):
        process = Process(target=target, args=args)
        process.start()
