# -*- coding: utf-8 -*-
import time

from handlers import StandardOutputHandler

STATUS_WORK = 'work'
STATUS_SHORT_REST = 'short'
STATUS_LONG_REST = 'long'


class PomodoroTimer(object):
    def __init__(self, work_duration=4, short_rest=2, long_rest=3,
                 output_handler_cls=StandardOutputHandler):
        self.durations = {
            STATUS_WORK: work_duration,
            STATUS_SHORT_REST: short_rest,
            STATUS_LONG_REST: long_rest
        }
        self.output_handler = output_handler_cls()
        self.session_count = 0
        self.status = STATUS_WORK

    def start(self):
        counter = self._counter()

        while counter > 0:
            self.ticking(counter)
            counter -= 1
            time.sleep(1)

        if self.is_working:
            self.work_completed()
        self._next_status()

    def work_completed(self):
        self.session_count += 1
        self.output_handler.work_completed(self.session_count)

    def ticking(self, counter):
        self.output_handler.ticking(self.status, counter)

    @property
    def is_working(self):
        return self.status == STATUS_WORK

    @property
    def is_short_rest(self):
        return self.status == STATUS_SHORT_REST

    @property
    def is_long_rest(self):
        return self.status == STATUS_LONG_REST

    def _next_status(self):
        if self.status == STATUS_WORK:
            if self.session_count % 4 == 0:
                self.status = STATUS_LONG_REST
            else:
                self.status = STATUS_SHORT_REST
        else:
            self.status = STATUS_WORK

        return self.status

    def _counter(self):
        return self.durations[self.status]
