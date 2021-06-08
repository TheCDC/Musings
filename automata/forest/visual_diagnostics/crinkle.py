from forest import NoiseMapArgs, generate_noise_2d_crinkly
import random
from typing import List
from visual_diagnostics.base import Diagnostic
import cv2
import numpy


class DiagnoseCrinkle(Diagnostic):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        seed = 1
        shape = (200, 200)
        for i in range(7):
            crinkle_scalar = 2**i
            frame = generate_noise_2d_crinkly(
                    shape,
                    seed=seed,
                    noise_map=NoiseMapArgs(
                        x0=0,
                        y0=0,
                        octaves=2,
                        feature_size=64,
                        seed=seed*2,
                    ),
                    crinkle_map=NoiseMapArgs(
                        x0=0,
                        y0=0,
                        octaves=2 ** 2,
                        feature_size=8,
                        seed=seed*2,
                    ),
                    crinkle_scalar=crinkle_scalar,
                )
            cv2.putText(frame, f"{crinkle_scalar}", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (1,1,1), 2)
            self.frames.append(
                frame
            )
