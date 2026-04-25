import numpy as np


class ColorService:

    def random(self):
        return (
            int(np.random.randint(50, 255)),
            int(np.random.randint(50, 255)),
            int(np.random.randint(50, 255)),
            255
        )

    def default(self):
        return (0, 255, 0, 255)