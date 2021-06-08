from forest import generate_noise_2d
from visual_diagnostics.base import Diagnostic
import cv2


class DiagnoseFeatureSize(Diagnostic):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        shape = (200, 200)
        seed = 1
        for i in range(1, 7):
            feature_size = 2 ** i
            frame = generate_noise_2d(shape, seed=seed, feature_size=feature_size)
            cv2.putText(
                frame,
                f"{feature_size}",
                (0, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (1, 1, 1),
                2,
            )
            self.frames.append(frame)
