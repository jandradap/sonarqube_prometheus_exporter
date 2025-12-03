import unittest
from unittest.mock import patch, MagicMock
from lib.analysis_metrics import get_stat, get_value, set_metrics, common_metrics, rule_metrics, event_metrics

class TestAnalysisMetrics(unittest.TestCase):

    def test_get_stat(self):
        metrics = [
            {'key': 'metric1', 'name': 'Metric 1', 'type': 'INT', 'domain': 'domain1'},
            {'key': 'alert_status', 'name': 'Alert Status', 'type': 'LEVEL', 'domain': 'domain2'},
            {'key': 'metric3', 'name': 'Metric 3', 'type': 'UNKNOWN', 'domain': 'domain3'}
        ]
        stats = list(get_stat(metrics))
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0]['metric']['key'], 'metric1')
        self.assertEqual(stats[1]['metric']['key'], 'alert_status')

    def test_get_value(self):
        # Case 1: 'value' in measures
        measures = [{'value': 10}]
        self.assertEqual(get_value(measures), 10)

        # Case 2: 'periods' in measures
        measures_period = [{'periods': [{'value': 20}]}]
        self.assertEqual(get_value(measures_period), 20)

        # Case 3: Error handling - should return 0 now
        measures_error = [{'other': 30}]
        self.assertEqual(get_value(measures_error), 0)

    def test_set_metrics(self):
        mock_prom_metric = MagicMock()

        # Case 1: INT type
        set_metrics('metric1', 'domain1', 'INT', 10, mock_prom_metric, 'project1')
        mock_prom_metric.labels.assert_called_with(project_key='project1', domain='domain1')
        mock_prom_metric.labels().set.assert_called_with(10)

        # Case 2: alert_status
        set_metrics('alert_status', 'domain2', 'LEVEL', 'OK', mock_prom_metric, 'project2')
        mock_prom_metric.labels.assert_called_with(project_key='project2', domain='domain2')
        mock_prom_metric.labels().state.assert_called_with('OK')

        # Case 3: Unsupported
        # Just ensure it doesn't crash
        set_metrics('unknown', 'domain3', 'UNKNOWN', 0, mock_prom_metric, 'project3')

    @patch('lib.analysis_metrics.get_value')
    @patch('lib.analysis_metrics.set_metrics')
    def test_common_metrics(self, mock_set_metrics, mock_get_value):
        mock_sonar = MagicMock()
        stats = {'stat': MagicMock(), 'metric': {'key': 'metric1', 'domain': 'domain1', 'type': 'INT'}}
        projects = [{'key': 'project1'}]

        # Mock sonar response
        mock_sonar.measures.get_component_with_specified_measures.return_value = {
            'component': {'measures': [{'value': 100}]}
        }
        mock_get_value.return_value = 100

        common_metrics(projects, mock_sonar, stats)

        mock_get_value.assert_called()
        mock_set_metrics.assert_called_with('metric1', 'domain1', 'INT', 100, stats['stat'], 'project1')

        # Case where no measures
        mock_sonar.measures.get_component_with_specified_measures.return_value = {
            'component': {'measures': []}
        }
        common_metrics(projects, mock_sonar, stats)
        # Should just print and continue

    @patch('lib.analysis_metrics.stat_rule')
    @patch('lib.analysis_metrics.sr_to_json')
    def test_rule_metrics(self, mock_sr_to_json, mock_stat_rule):
        mock_sonar = MagicMock()
        projects = [{'key': 'project1'}]

        mock_sonar.issues.search_issues.return_value = [
            {'rule': 'rule1'}, {'rule': 'rule2'}, {'rule': 'rule1'}
        ]

        mock_sr_to_json.return_value = {'rule1': 2, 'rule2': 1}

        rule_metrics(projects, mock_sonar)

        mock_stat_rule.labels.assert_any_call(project_key='project1', rule='rule1')
        mock_stat_rule.labels().set.assert_any_call(2)

    @patch('lib.analysis_metrics.stat_event')
    @patch('lib.analysis_metrics.get_json')
    def test_event_metrics(self, mock_get_json, mock_stat_event):
        mock_sonar = MagicMock()
        projects = [{'key': 'project1'}]

        mock_sonar.project_analyses.search_project_analyses_and_events.return_value = [
            {'key': 'event1', 'date': '2023-01-01', 'projectVersion': '1.0'}
        ]

        # Mock get_json to return the value passed as key if it exists in the dict
        # Actually get_json(element, json_data) returns json_data[element]
        def side_effect(element, json_data):
            return json_data.get(element)
        mock_get_json.side_effect = side_effect

        event_metrics(projects, mock_sonar)

        mock_stat_event.labels.assert_called_with(project_key='project1')
        mock_stat_event.labels().info.assert_called_with({
            'event_id': 'event1', 'date': '2023-01-01', 'project_version': '1.0'
        })
