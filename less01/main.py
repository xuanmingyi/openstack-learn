from oslo_config import cfg
from oslo_service import service, loopingcall

from datetime import datetime

CONF = cfg.CONF

# configure
enable_period_tasks = True
interval = 1
initial_delay = 4


def pp(s):
    print "{}: {}".format(datetime.now(), s)


class FooService(service.Service):

    def __init__(self):
        super(FooService, self).__init__()
        self.timers = []


    def start(self):

        if enable_period_tasks:
            # add period tasks
            periodic = loopingcall.FixedIntervalLoopingCall(self.periodic_tasks)
            pp("initial_delay {}".format(initial_delay))
            periodic.start(interval=1, initial_delay=initial_delay)
            self.timers.append(periodic) 


    def wait(self):
        for x in self.timers:
            try:
                x.wait()
            except Exception as e:
                print e
        super(FooService, self).wait()


    def stop(self):
        for x in self.timers:
            try:
                x.stop()
            except Exception as e:
                print e
        super(FooService, self).wait()
    

    def reset(self):
        print "reset"


    def periodic_tasks(self):
        pp("run periold task")


    @classmethod
    def create(cls):
        return cls()

server = FooService.create()


launcher = service.launch(CONF, server)

try:
    launcher.wait()
except KeyboardInterrupt:
    launcher.stop()
