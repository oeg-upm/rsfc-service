from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader("app/templates/"))


def render_benchmark_score(benchmark_id, score, log):

    template = env.get_template("benchmark_score_template.json.j2")

    rendered = template.render(benchmark_id=benchmark_id, score=score, log=log)

    return json.loads(rendered)
