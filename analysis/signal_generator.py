# Signal generation
import numpy as np


def generate_signal(vectors):
    scores = vectors.mean(axis=1)
    confidence = np.std(scores)
    return scores, confidence