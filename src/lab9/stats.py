"""Statistics: M2 judge calibration, M4 paired bootstrap, M6 pass@k."""

from __future__ import annotations

from collections.abc import Sequence
from math import comb

import numpy as np

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    tp = fp = fn = tn = 0
    for h, j in zip(human, judge):
        if h == POS and j == POS:
            tp += 1
        elif h != POS and j == POS:
            fp += 1
        elif h == POS and j != POS:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    c = confusion(human, judge)
    p = c["tp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else 0.0
    r = c["tp"] / (c["tp"] + c["fn"]) if (c["tp"] + c["fn"]) else 0.0
    return p, r


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    n = len(human)
    p_o = sum(h == j for h, j in zip(human, judge)) / n
    labels = set(human) | set(judge)
    p_e = sum((sum(h == l for h in human) / n) * (sum(j == l for j in judge) / n) for l in labels)
    if p_e == 1:
        raise ValueError("kappa undefined: p_e == 1")
    return (p_o - p_e) / (1 - p_e)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    denom = sensitivity + specificity - 1
    if denom == 0:
        raise ValueError("judge has no signal: sens + spec == 1")
    return min(1.0, max(0.0, (observed_rate + specificity - 1) / denom))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    from scipy.stats import bootstrap
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.array_equal(a, b):
        return (0.0, 0.0, 0.0)
    res = bootstrap((a, b), lambda x, y, axis: np.mean(x - y, axis=axis),
                    paired=True, vectorized=True, n_resamples=n_resamples,
                    confidence_level=confidence, method="percentile",
                    rng=np.random.default_rng(rng))
    ci = res.confidence_interval
    return (float(a.mean() - b.mean()), float(ci.low), float(ci.high))


def pass_at_k(n: int, c: int, k: int) -> float:
    if k > n:
        raise ValueError("k > n")
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float:
    if k > n:
        raise ValueError("k > n")
    return comb(c, k) / comb(n, k)