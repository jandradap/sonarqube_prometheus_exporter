import unittest
from unittest.mock import patch, MagicMock
from lib.analysis_metrics import get_stat

class TestAnalysisMetrics(unittest.TestCase):
    def test_get_stat(self):

        metric1 = {'key': 'metric1', 'name': 'Metric 1', 'type': 'INT', 'domain': 'domain1'}
        metric2 = {'key': 'metric2', 'name': 'Metric 2', 'type': 'UNKNOWN', 'domain': 'domain2'}

        metrics = [metric1, metric2]

        # Test the function
        stats = list(get_stat(metrics))
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['metric']['key'], 'metric1')
