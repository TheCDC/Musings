import cv2
import numpy
from visual_diagnostics import ALL_DIAGNOSTICS

ims = []
for d in ALL_DIAGNOSTICS:
    diag = d()
    diag.run()
    diag.show()
    ims.append(diag.get_image())
# cv2.imshow('all',numpy.vstack(ims))
while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        break
