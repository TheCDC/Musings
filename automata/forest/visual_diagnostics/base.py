from cv2_utils import numpy_to_cv2
from typing import List
import cv2
import numpy


class Diagnostic:
    def __init__(self) -> None:
        self.frames: List[numpy.array] = []

    def run(self):
        raise NotImplementedError()

    def get_image(self) -> numpy.array:
        return numpy.concatenate(self.frames, axis=1)

    def show(self):
        final_image = numpy.concatenate(self.frames, axis=1)

        # final_image = (
        #     cv2.cvtColor(
        #         numpy.concatenate([self.frames], axis=1).astype("float32"),
        #         cv2.COLOR_RGB2BGR,
        #     ),
        # )
        cv2.namedWindow(self.__class__.__name__)
        cv2.imshow(self.__class__.__name__, self.frames[0])
        cv2.imshow(self.__class__.__name__, final_image)
