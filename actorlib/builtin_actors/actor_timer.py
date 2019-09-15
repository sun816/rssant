import asyncio
import time
import logging

from actorlib.actor import actor
from actorlib.message import ActorMessage
from actorlib.context import ActorContext

from .base import BuiltinActorBase
from .name import ACTOR_TIMER


LOG = logging.getLogger(__name__)


@actor(ACTOR_TIMER)
class ActorTimer(BuiltinActorBase):

    def _load_timers(self):
        timers = []
        now = time.time()
        for x in self.app.timers.values():
            d = x.timer.total_seconds()
            timers.append(dict(name=x.name, seconds=d, deadline=now + d))
        return timers

    def _op_inbox(self, ctx, dst, expire_at=None):
        node_name = self.app.registery.current_node.name
        message = ActorMessage(
            dst=dst,
            dst_node=node_name,
            src=ACTOR_TIMER,
            expire_at=expire_at,
            priority=0,
            require_ack=False,
        )
        message = self.app.registery.complete_message(message)
        self.app.queue.op_inbox(message)

    async def _schedule_timers(self, ctx: ActorContext, timers):
        now = time.time()
        tasks = []
        for timer in timers:
            if now >= timer['deadline']:
                expire_at = now + 2 * timer['seconds']
                tasks.append(dict(dst=timer['name'], expire_at=expire_at))
                timer['deadline'] = now + timer['seconds']
        for task in tasks:
            try:
                self._op_inbox(ctx, **task)
            except Exception as ex:
                LOG.exception(ex)
        now = time.time()
        wait_seconds = 1
        for timer in timers:
            wait_seconds = min(wait_seconds, timer['deadline'] - now)
        await asyncio.sleep(max(0, wait_seconds))

    async def __call__(self, ctx: ActorContext):
        timers = self._load_timers()
        if not timers:
            LOG.info('no timers to schedule')
            return
        for timer in timers:
            LOG.info("schedule timer {} every {} seconds".format(timer['name'], timer['seconds']))
        while True:
            try:
                await self._schedule_timers(ctx, timers)
            except Exception as ex:
                LOG.exception(ex)
