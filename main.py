import json
import math
import os
from pathlib import Path

INP = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
Z = [-1.645, -0.674, 0, 0.674, 1.645]
TAU = (0.05, 0.25, 0.5, 0.75, 0.95)


def r2(x):
    v = math.floor(x * 100 + 0.5) / 100
    return int(v) if v == int(v) else v


def pct(xs, t):
    if len(xs) == 1:
        return xs[0]
    i = t * (len(xs) - 1)
    lo = int(i)
    hi = min(lo + 1, len(xs) - 1)
    f = i - lo
    return xs[lo] * (1 - f) + xs[hi] * f


def curves(case):
    out = []
    for c in case.get("comparables") or []:
        hr = c.get("hourly") or []
        ds = c.get("day_start")
        idx = None
        for i, p in enumerate(hr):
            if p.get("from") == ds:
                idx = i
                break
        if idx is None or idx + 24 > len(hr):
            continue
        v1 = hr[idx].get("viewers") or 0
        if v1 <= 0:
            continue
        rs = []
        ok = True
        for h in range(1, 24):
            v = hr[idx + h].get("viewers") or 0
            if v <= 0:
                ok = False
                break
            rs.append(math.log(v / v1))
        if ok:
            out.append((v1, rs))
    return out


def forecast(case):
    p1 = 1
    for k in case.get("known") or []:
        if k.get("hour") == 1:
            p1 = max(1, k.get("viewers") or 1)
    hrs = [r.get("hour") for r in case.get("forecast") or []]
    if hrs != list(range(2, 25)):
        hrs = list(range(2, 25))
    cs = curves(case)
    near = [rs for v1, rs in cs if abs(math.log(v1) - math.log(p1)) <= math.log(20)]
    if len(near) >= 5:
        cs = near
    else:
        cs = [rs for _, rs in cs]
    rows = []
    for j, h in enumerate(hrs):
        col = sorted(c[j] for c in cs) if cs else []
        if len(col) >= 5:
            qs = [p1 * math.exp(pct(col, t)) for t in TAU]
        else:
            s = 0.15 * math.sqrt(h - 1)
            qs = [p1 * math.exp(z * s) for z in Z]
        qs = [min(1e9, max(0.01, r2(q))) for q in qs]
        for i in range(1, 5):
            if qs[i] < qs[i - 1]:
                qs[i] = qs[i - 1]
        rows.append({"hour": h, "q": qs})
    return {"hours": rows}


def fallback():
    rows = []
    for h in range(2, 25):
        s = 0.15 * math.sqrt(h - 1)
        rows.append({"hour": h, "q": [max(0.01, r2(math.exp(z * s))) for z in Z]})
    return {"hours": rows}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(INP.glob("*.in")):
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            fc = forecast(case)
        except Exception:
            fc = fallback()
        (OUT / f"{path.stem}.out").write_text(
            json.dumps(fc, separators=(",", ":")) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
