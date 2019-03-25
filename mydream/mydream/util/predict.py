import lightgbm as lgb
import numpy as np
import os

from .__init__ import __ROOT__


# TODO(@LEO_MOON) send output to web server
# mode >> 0 : pdf, 1 : doc/docs, 2 : hwp
def predict(feature, mode=0, th=0.5):
    if mode == 0:
        bst = lgb.Booster(model_file=os.path.join(__ROOT__, "dream_pdf.model"))
    elif mode == 1:
        bst = lgb.Booster(model_file=os.path.join(__ROOT__, "dream_doc.model"))
    elif mode == 2:
        bst = lgb.Booster(model_file=os.path.join(__ROOT__, "dream_hwp.model"))

    feature = np.array(feature)
    output = bst.predict(feature, num_iteration=bst.best_iteration)

    for i in range(len(output)):
        if output[i] >= th:
            output[i] = 1
        else:
            output[i] = 0

    return output
