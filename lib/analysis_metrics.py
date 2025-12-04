# Importing the functions from the lib.util file and the prometheus_client file.
import logging
from lib.util import get_json, sr_to_json
from prometheus_client import Enum, Gauge, Info

logger = logging.getLogger(__name__)

def get_stat(metrics):
    stats = []
# Creating a list of metrics that are supported by prometheus.
    for metric in metrics:
        if metric['type'] in ['INT', 'FLOAT', 'PERCENT', 'MILLISEC', 'RATING', 'WORK_DUR']:
            g = Gauge(metric['key'], metric['name'], ['project_key', 'domain'])
        elif metric['key'] == 'alert_status':
            g = Enum(metric['key'], metric['name'], ['project_key', 'domain'], states=['ERROR', 'OK'])
        elif metric.get('type') in ['BOOL', 'DATA', 'STRING']:
            continue
        else:
            logger.debug('Metric type %s for key %s is not supported', metric.get('type'), metric.get('key'))
            continue
        stats.append({'stat':g, 'metric':metric})
    return stats
    
def get_value(measures):
# Getting the value of the metric.
    logger.debug(f"Getting value from measures: {measures}")
    if not measures:
        logger.debug("Measures list is empty.")
        return 0

    if not isinstance(measures[0], dict):
         logger.debug(f"First element of measures is not a dict: {type(measures[0])}. Skipping.")
         return 0

    if 'value' in measures[0]:
        try:
            value = measures[0]['value']
        except (KeyError, IndexError, NameError) as error:
            logger.error(f"Error extracting value: {error}")
            raise error
    elif 'periods' in measures[0]:
        try:
            value = measures[0]['periods'][0]['value']
        except (KeyError, IndexError, NameError) as error:
             logger.error(f"Error extracting period value: {error}")
             raise error
    else:
        logger.debug("Neither 'value' nor 'periods' found in measures.")
        value = 0
    return value

def set_metrics(sonar_issue_key, sonar_issue_domain, sonar_issue_type, value, prom_metric, project_key):
# This is a function that is setting the metrics in prometheus.
    logger.debug(f"Setting metric {sonar_issue_key} for project {project_key} with value {value}")
    if sonar_issue_type in ['INT', 'FLOAT', 'PERCENT', 'MILLISEC', 'RATING', 'WORK_DUR']:
        prom_metric.labels(
            project_key=project_key, 
            domain=sonar_issue_domain,
        ).set(value)
    elif sonar_issue_key == 'alert_status':
        prom_metric.labels(
            project_key=project_key, 
            domain=sonar_issue_domain,
        ).state(value)
    elif sonar_issue_type in ['BOOL', 'DATA', 'STRING']:
        return
    else:
        logger.debug('Metric type %s for key %s is not supported', sonar_issue_type, sonar_issue_key)

def common_metrics(projects, sonar, stats):
# Getting the metrics from sonarqube and setting the metrics in prometheus.
    prom_metric = stats['stat']
    sonar_metric = stats['metric']
    for p in projects:
        project_key = p['key']
        sonar_issue_key = sonar_metric['key']
        sonar_issue_domain = sonar_metric['domain']
        sonar_issue_type = sonar_metric['type']

        logger.debug(f"Processing common metric {sonar_issue_key} for project {project_key}")

        try:
            component = sonar.measures.get_component_with_specified_measures(component=project_key, fields="metrics", metricKeys=sonar_issue_key)
            if 'component' in component and 'measures' in component['component']:
                measures = component['component']['measures']
                if len(measures) > 0:
                    value = get_value(measures)
                    set_metrics(sonar_issue_key, sonar_issue_domain, sonar_issue_type, value, prom_metric, project_key)
                else:
                    logger.debug(f'Component {project_key} doesnt have metric {sonar_issue_key}')
            else:
                 logger.debug(f"Invalid component response for {project_key}")
        except Exception as e:
            logger.error(f"Error in common_metrics for {project_key}: {e}")

stat_rule = Gauge('stat_rule', 'Frequency of rule', ['project_key', 'rule'])
def rule_metrics(projects, sonar):
# Getting the rules from sonarqube and setting the metrics in prometheus.
    for p in projects:
        project_key = p['key']
        logger.debug(f"Processing rule metrics for {project_key}")
        try:
            issues1 = list(sonar.issues.search_issues(componentKeys=project_key))
            rules = []
            for i in issues1:
                rules.append(i['rule'])
            j_data = sr_to_json(rules)
            for key, value in j_data.items():
                stat_rule.labels(
                    project_key=project_key,
                    rule=key,
                ).set(value)
        except Exception as e:
            logger.error(f"Error in rule_metrics for {project_key}: {e}")

stat_event = Info('project_analyses_and_events', 'Description of project analyses', ['project_key'])
def event_metrics(projects, sonar):
# Getting the events from sonarqube and setting the metrics in prometheus.
    for p in projects:
        project_key = p['key']
        logger.debug(f"Processing event metrics for {project_key}")
        try:
            project_analyses_and_events = list(sonar.project_analyses.search_project_analyses_and_events(project=project_key))
            for event in project_analyses_and_events:
                event_id = get_json("key", event)
                date = get_json("date", event)
                project_version = get_json("projectVersion", event)
                value = {'event_id': event_id, 'date': date, 'project_version': project_version}
                stat_event.labels(
                    project_key=project_key,
                ).info(value)
        except Exception as e:
            logger.error(f"Error in event_metrics for {project_key}: {e}")
