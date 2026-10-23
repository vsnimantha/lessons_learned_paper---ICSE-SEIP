"""Shared loaders. Pure standard library; Python 3.8+."""
import csv, os, collections, statistics, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def is_noise(rec):
    """DEBUG and O0 records are never labelled; they are not comparisons."""
    return rec["variant"] in ("DEBUG", "O0")


def comparisons(records):
    return [r for r in records if not is_noise(r)]


def rank(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5


def spearman(x, y):
    return pearson(rank(x), rank(y))


def spearman_perm_p(x, y, n_perm=200000, seed=1):
    """Two-sided permutation p-value (deterministic seed)."""
    rng = random.Random(seed)
    obs = abs(spearman(x, y))
    rx = rank(x)
    ry = rank(y)
    hits = 0
    ry2 = ry[:]
    for _ in range(n_perm):
        rng.shuffle(ry2)
        if abs(pearson(rx, ry2)) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (n_perm + 1)
