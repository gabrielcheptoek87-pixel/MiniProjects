"""Fish stock models: logistic growth with harvesting, plus the Fibonacci baseline."""

DEFAULT_R = 0.4
DEFAULT_K = 10_000.0
DEFAULT_N0 = 4_000.0


def fibonacci(n):
    """Old baseline 'stock' series (kept only for comparison in the write-up)."""
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def msy_benchmarks(r=DEFAULT_R, K=DEFAULT_K):
    """Return (MSY in tonnes/week, harvest fraction achieving MSY at steady state)."""
    return r * K / 4, r / 2


class FishStock:
    """N(t+1) = N(t) + r*N(t)*(1 - N(t)/K) - h*N(t)"""

    def __init__(self, r=DEFAULT_R, K=DEFAULT_K, N0=DEFAULT_N0):
        self.r = r
        self.K = K
        self.N = N0
        self.history = [N0]

    def step(self, h):
        harvest_tonnes = h * self.N
        growth = self.r * self.N * (1 - self.N / self.K)
        self.N = max(self.N + growth - harvest_tonnes, 0.0)
        self.history.append(self.N)
        return harvest_tonnes

    def simulate(self, weeks, h, closed_weeks_per_year=0):
        """Return weekly harvest (tonnes). Harvest is zero for the first
        `closed_weeks_per_year` weeks of every 52-week block (closed season)."""
        harvests = []
        for t in range(weeks):
            h_t = 0.0 if (t % 52) < closed_weeks_per_year else h
            harvests.append(self.step(h_t))
        return harvests
