import diamond.collector
import socket
import requests

class FilebeatRestCollector(diamond.collector.Collector):

    METRICS_KEYS = {
    #CPU
    'cpu_tics':'beat.cpu.system.ticks',
    'cpu_time':'beat.cpu.system.time.ms',
    'cpu__total_tics':'beat.cpu.total.ticks',
    'cpu__total_time':'beat.cpu.total.time.ms',
    'cpu_total_value':'beat.cpu.total.value',
    'cpu_user_tics':'beat.cpu.user.ticks',
    'cpu_user_time':'beat.cpu.user.time.ms',
    #LOAD
    'load_1':'system.load.1',
    'load_15':'system.load.15',
    'load_5':'system.load.5',
    'load_norm_1':'system.load.norm.1',
    'load_norm_15':'system.load.norm.15',
    'load_norm_5':'system.load.norm.5',
    #MEMORY
    'mem_alloc':'beat.memstats.memory_alloc',
    'mem_total':'beat.memstats.memory_total',
    'gc_next':'beat.memstats.gc_next',
    }

    def __init__(self, *args, **kwargs):
        super(FilebeatRestCollector, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    def get_default_config_help(self):
        config_help = super(FilebeatRestCollector, self).get_default_config_help()
        config_help.update({
            'host':'machine hostname',
            'port':'Filebeat HTTP port default:5066',
            'metrics':'list of metrics to be published',
            'path':'stats endpoint'
        })
        return config_help

    def get_default_config(self):
        config = super(FilebeatRestCollector, self).get_default_config()
        config.update({
            'host':socket.gethostbyname(socket.gethostname()),
            'port':'8081',
            'metrics':[],
            'path':'stats'
        })
        return config
        
    def collect(self):
        data = self.get_stats(self.config.get('path'))
        metrics = self.config.get('metrics')

        for metric in metrics:
            self.publish_stats(
                data[self.METRICS_KEY[metric]],self.METRICS_KEY[metric]
                )

    def get_stats(self, path):
        url='http://%s:%s/%s' % (
            self.config.get('hostname'),
            self.config.get('port'),
            self.config.get('path'),
            )
        try:
            response = self.session.get(url)
            data = response.json()['data']
        except requests.exceptions.RequestException as e:
            self.log.error("Can't open url %s. %s", url, e)
        return data

    def flatten_json(self, data, prev_key = '', flat_data = {}, delim='.'):
        for key in data:
            if isinstance(data[key], dict):
                self.flatten_json(data[key], prev_key = prev_key + key + delim, flat_data = flat_data)
            else:
                flat_data[prev_key+key]=data[key]
        return flat_data