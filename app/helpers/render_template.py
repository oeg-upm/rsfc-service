from jinja2 import Environment, FileSystemLoader
import json
import uuid

def render_benchmark_score(score, log, checks):
    
    data = dict()
    env = Environment(loader=FileSystemLoader("app/templates/"))
    
    data['score'] = score
    data['log'] = log
    data['urn_score'] = f"urn:rsfc:{uuid.uuid4()}"
    data['urn_results'] = f"urn:rsfc:{uuid.uuid4()}"
    data['checks'] = checks

    template = env.get_template("benchmark_score_template.json.j2")

    rendered = template.render(**data)

    return json.loads(rendered)
