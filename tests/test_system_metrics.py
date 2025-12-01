import unittest
from unittest.mock import patch, MagicMock
from lib.system_metrics import system_metric

class TestSystemMetrics(unittest.TestCase):

    @patch('lib.system_metrics.get_data')
    @patch('lib.system_metrics.health_metric')
    @patch('lib.system_metrics.web_jvm_max_memory_metric')
    @patch('lib.system_metrics.web_jvm_free_memory_metric')
    @patch('lib.system_metrics.web_jvm_heap_commited_metric')
    @patch('lib.system_metrics.web_jvm_heap_init_metric')
    @patch('lib.system_metrics.web_jvm_heap_max_metric')
    @patch('lib.system_metrics.web_jvm_heap_used_metric')
    @patch('lib.system_metrics.web_jvm_non_heap_committed_metric')
    @patch('lib.system_metrics.web_jvm_non_heap_init_metric')
    @patch('lib.system_metrics.web_jvm_non_heap_used_metric')
    @patch('lib.system_metrics.web_jvm_threads_metric')
    @patch('lib.system_metrics.web_pool_active_connection_metric')
    @patch('lib.system_metrics.web_pool_max_connection_metric')
    @patch('lib.system_metrics.web_pool_initial_size_metric')
    @patch('lib.system_metrics.web_pool_idle_connections_metric')
    @patch('lib.system_metrics.web_pool_min_idle_connections_metric')
    @patch('lib.system_metrics.web_pool_max_idle_connections_metric')
    @patch('lib.system_metrics.compute_engine_tasks_pending_metric')
    @patch('lib.system_metrics.compute_engine_tasks_inprogress_metric')
    @patch('lib.system_metrics.compute_engine_tasks_error_progress_metric')
    @patch('lib.system_metrics.compute_engine_tasks_success_progress_metric')
    @patch('lib.system_metrics.compute_engine_tasks_progressing_time_metric')
    @patch('lib.system_metrics.compute_engine_tasks_worker_metric')
    @patch('lib.system_metrics.compute_engine_jvm_state_max_memory_metric')
    @patch('lib.system_metrics.compute_engine_jvm_free_memory_metric')
    @patch('lib.system_metrics.compute_engine_jvm_heap_commited_metric')
    @patch('lib.system_metrics.compute_engine_jvm_heap_init_metric')
    @patch('lib.system_metrics.compute_engine_jvm_heap_max_metric')
    @patch('lib.system_metrics.compute_engine_jvm_heap_used_metric')
    @patch('lib.system_metrics.compute_engine_jvm_non_heap_committed_metric')
    @patch('lib.system_metrics.compute_engine_jvm_non_heap_init_metric')
    @patch('lib.system_metrics.compute_engine_jvm_non_heap_used_metric')
    @patch('lib.system_metrics.compute_engine_jvm_threads_metric')
    @patch('lib.system_metrics.compute_engine_pool_active_connection_metric')
    @patch('lib.system_metrics.compute_engine_pool_max_connection_metric')
    @patch('lib.system_metrics.compute_engine_pool_initial_size_metric')
    @patch('lib.system_metrics.compute_engine_pool_idle_connections_metric')
    @patch('lib.system_metrics.compute_engine_pool_min_idle_connections_metric')
    @patch('lib.system_metrics.compute_engine_pool_max_idle_connections_metric')
    @patch('lib.system_metrics.cpu_usage_metric')
    @patch('lib.system_metrics.disk_available_metric')
    @patch('lib.system_metrics.store_size_metric')
    @patch('lib.system_metrics.translog_size_metric')
    @patch('lib.system_metrics.jvm_heap_used_metric')
    @patch('lib.system_metrics.jvm_heap_max_metric')
    @patch('lib.system_metrics.jvm_non_heap_used_metric')
    @patch('lib.system_metrics.jvm_threads_metric')
    @patch('lib.system_metrics.open_file_descriptors_metric')
    @patch('lib.system_metrics.max_file_descriptors_metric')
    @patch('lib.system_metrics.index_docs_metric')
    @patch('lib.system_metrics.sonarlint_client_metric')
    @patch('lib.system_metrics.total_of_user_metric')
    @patch('lib.system_metrics.total_of_project_metric')
    @patch('lib.system_metrics.total_line_of_code_metric')
    @patch('lib.system_metrics.total_of_plugins_metric')
    @patch('lib.system_metrics.project_count_by_language_metric')
    @patch('lib.system_metrics.ncloc_count_by_language_metric')
    def test_system_metric(self,
                           mock_ncloc_count_by_language_metric,
                           mock_project_count_by_language_metric,
                           mock_total_of_plugins_metric,
                           mock_total_line_of_code_metric,
                           mock_total_of_project_metric,
                           mock_total_of_user_metric,
                           mock_sonarlint_client_metric,
                           mock_index_docs_metric,
                           mock_max_file_descriptors_metric,
                           mock_open_file_descriptors_metric,
                           mock_jvm_threads_metric,
                           mock_jvm_non_heap_used_metric,
                           mock_jvm_heap_max_metric,
                           mock_jvm_heap_used_metric,
                           mock_translog_size_metric,
                           mock_store_size_metric,
                           mock_disk_available_metric,
                           mock_cpu_usage_metric,
                           mock_compute_engine_pool_max_idle_connections_metric,
                           mock_compute_engine_pool_min_idle_connections_metric,
                           mock_compute_engine_pool_idle_connections_metric,
                           mock_compute_engine_pool_initial_size_metric,
                           mock_compute_engine_pool_max_connection_metric,
                           mock_compute_engine_pool_active_connection_metric,
                           mock_compute_engine_jvm_threads_metric,
                           mock_compute_engine_jvm_non_heap_used_metric,
                           mock_compute_engine_jvm_non_heap_init_metric,
                           mock_compute_engine_jvm_non_heap_committed_metric,
                           mock_compute_engine_jvm_heap_used_metric,
                           mock_compute_engine_jvm_heap_max_metric,
                           mock_compute_engine_jvm_heap_init_metric,
                           mock_compute_engine_jvm_heap_commited_metric,
                           mock_compute_engine_jvm_free_memory_metric,
                           mock_compute_engine_jvm_state_max_memory_metric,
                           mock_compute_engine_tasks_worker_metric,
                           mock_compute_engine_tasks_progressing_time_metric,
                           mock_compute_engine_tasks_success_progress_metric,
                           mock_compute_engine_tasks_error_progress_metric,
                           mock_compute_engine_tasks_inprogress_metric,
                           mock_compute_engine_tasks_pending_metric,
                           mock_web_pool_max_idle_connections_metric,
                           mock_web_pool_min_idle_connections_metric,
                           mock_web_pool_idle_connections_metric,
                           mock_web_pool_initial_size_metric,
                           mock_web_pool_max_connection_metric,
                           mock_web_pool_active_connection_metric,
                           mock_web_jvm_threads_metric,
                           mock_web_jvm_non_heap_used_metric,
                           mock_web_jvm_non_heap_init_metric,
                           mock_web_jvm_non_heap_committed_metric,
                           mock_web_jvm_heap_used_metric,
                           mock_web_jvm_heap_max_metric,
                           mock_web_jvm_heap_init_metric,
                           mock_web_jvm_heap_commited_metric,
                           mock_web_jvm_free_memory_metric,
                           mock_web_jvm_max_memory_metric,
                           mock_health_metric,
                           mock_get_data):

        # Mock data return
        mock_data = {
            'Health': 'GREEN',
            'Web JVM State': {
                'Max Memory (MB)': 1000,
                'Free Memory (MB)': 500,
                'Heap Committed (MB)': 600,
                'Heap Init (MB)': 200,
                'Heap Max (MB)': 1000,
                'Heap Used (MB)': 500,
                'Non Heap Committed (MB)': 100,
                'Non Heap Init (MB)': 50,
                'Non Heap Used (MB)': 80,
                'Threads': 20
            },
            'Web Database Connection': {
                'Pool Active Connections': 5,
                'Pool Max Connections': 50,
                'Pool Initial Size': 10,
                'Pool Idle Connections': 45,
                'Pool Min Idle Connections': 10,
                'Pool Max Idle Connections': 40
            },
            'Compute Engine Tasks': {
                'Pending': 2,
                'In Progress': 1,
                'Processed With Error': 0,
                'Processed With Success': 10,
                'Processing Time (ms)': 500,
                'Worker Count': 2
            },
            'Compute Engine JVM State': {
                'Worker Count': 2,
                'Free Memory (MB)': 300,
                'Heap Committed (MB)': 400,
                'Heap Init (MB)': 100,
                'Heap Max (MB)': 800,
                'Heap Used (MB)': 300,
                'Non Heap Committed (MB)': 80,
                'Non Heap Init (MB)': 40,
                'Non Heap Used (MB)': 60,
                'Threads': 10
            },
            'Compute Engine Database Connection': {
                'Pool Active Connections': 2,
                'Pool Max Connections': 20,
                'Pool Initial Size': 5,
                'Pool Idle Connections': 18,
                'Pool Min Idle Connections': 5,
                'Pool Max Idle Connections': 15
            },
            'Search State': {
                'CPU Usage (%)': 10,
                'Disk Available': '10GB',
                'Store Size': '500MB',
                'Translog Size': '50MB',
                'JVM Heap Used': '200MB',
                'JVM Heap Max': '1GB',
                'JVM Non Heap Used': '100MB',
                'JVM Threads': 15,
                'Open File Descriptors': 100,
                'Max File Descriptors': 1000
            },
            'Search Indexes': {
                'Index components - Docs': 5000
            },
            'Server Push Connections': {
                'SonarLint Connected Clients': 5
            },
            'Statistics': {
                'userCount': 50,
                'projectCount': 10,
                'ncloc': 100000,
                'plugins': ['java', 'python'],
                'projectCountByLanguage': [{'language': 'java', 'count': 5}],
                'nclocByLanguage': [{'language': 'java', 'ncloc': 50000}]
            }
        }
        mock_get_data.return_value = mock_data

        # Call function
        system_metric('http://localhost', 'token')

        # Assert calls
        mock_health_metric.info.assert_called_with({'health': 'GREEN'})
        mock_web_jvm_max_memory_metric.set.assert_called_with(1000)
        # Add more assertions if needed, but this covers the execution path.
        mock_cpu_usage_metric.set.assert_called_with(10)
        mock_total_of_plugins_metric.set.assert_called_with(2)
        mock_project_count_by_language_metric.labels.assert_called_with(language='java')
