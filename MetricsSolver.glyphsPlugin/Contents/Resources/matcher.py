import re
import unittest

class MetricsSolverMatcher(object):
    pattern = re.compile(r"(\.?[A-Z]+(?:[.\-_][A-Z]+)*)", re.IGNORECASE)

    @classmethod
    def match(cls, metrics_key):
        match = MetricsSolverMatcher.pattern.search(metrics_key)
        if match:
            return match.group(0)
        return None

class MetricsSolverMatcherTest(unittest.TestCase):

    def test_match(self):
        fixtures = [
            ("=A", "A"),
            ("=Lcircumflex", "Lcircumflex"),
            ("=a.sc", "a.sc"),
            ("=200", None),
            ("=A*2", "A"),
            ("=a.sc*2", "a.sc"),
            ("=.notdef", ".notdef"),
            ("=|n", "n"),
            ("=kha-khmer", "kha-khmer"),
            ("=dad-ar.init", "dad-ar.init"),
            ("=f_f_l", "f_f_l"),
            ("==A", "A"),
            ("==180", None),
            ("=O-20", "O")
        ]

        for metric_key, expected in fixtures:
            matched = MetricsSolverMatcher.match(metric_key)
            self.assertEqual(matched, expected)

if __name__ == '__main__':
    unittest.main()
