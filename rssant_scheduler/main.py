import os
import logging

import django
from actorlib import actor, collect_actors, ActorNode, ActorContext
from rssant_common.helper import pretty_format_json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rssant.settings')
django.setup()

LOG = logging.getLogger(__name__)


@actor('actor.init')
def do_init(ctx: ActorContext):
    ctx.send('scheduler.load_registery')
    ctx.send('scheduler.healthcheck')


@actor('actor.health')
def do_health(ctx):
    nodes = pretty_format_json(ctx.registery.to_spec())
    LOG.info(f'receive healthcheck message {ctx.message}:\n{nodes}')


ACTORS = collect_actors('rssant_scheduler')


app = ActorNode(
    actors=ACTORS,
    port=6790,
    name='scheduler',
    subpath='/api/v1/scheduler',
    networks=[{
        'name': 'local',
        'url': 'http://127.0.0.1:6790/api/v1/scheduler',
    }],
    registery_node_spec={
        'name': 'scheduler',
        'modules': ['scheduler'],
        'networks': [{
            'name': 'local',
            'url': 'http://127.0.0.1:6790/api/v1/scheduler',
        }]
    }
)


if __name__ == "__main__":
    app.run()
