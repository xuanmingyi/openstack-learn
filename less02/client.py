from oslo_config import cfg
import oslo_messaging as messaging

transport = messaging.get_transport(cfg.CONF)
target = messaging.Target(topic='test', version='2.0')
client = messaging.RPCClient(transport, target)
client.call(ctxt, 'test', arg=arg)
