import random

UNIQUE_LENGTH = 5


class Random(random.Random):
    def __init__(self, use_static_seed=True):
        super().__init__()
        if use_static_seed:
            self.seed(0xDEADBEEF)

    def get_unique_id(self, length=UNIQUE_LENGTH):
        return str(self.getrandbits(16 * 8))[0:length]
