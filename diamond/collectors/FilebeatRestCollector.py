import diamond.collector
import socket
import requests

class FilebeatRestCollector(diamond.collector.Collector):
    session = requests.Session()
    def get_default_config_help(self):
        config_help = super(FilebeatRestCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        config = super(FilebeatRestCollector, self).get_default_config()
        config.update({
            'hostname':socket.gethostbyname(socket.gethostname()),
            'port':'8081',
            'metrics':[''],
            'stats_base_name':'monitoring.metric',
            'base_stats':'stats'
        })
        return config
        
    def collect(self):
        data = self.get_stats('stats')
        flat_data = self.flatten_json(data)
        desired_stats = self.config.get('metrics')
        for stat in desired_stats:
            self.publish_stats(flat_data[stat])
    
    def get_stats(self, path):
        base_url='http://{}:{}/{}'.format(
            self.config.get('hostname'),
            self.config.get('port'),
            self.config.get('path'),
            )
        response = self.session.get(base_url)
        data = response.json()['data']
        return data
    
    def flatten_json(self, data, prev_key = '', flat_data = {}, delim='.'):
        for key in data:
            if isinstance(data[key], dict):
                flatten_json(data[key],prev_key = prev_key + key + delim ,flat_data = flat_data)
            else:
                flat_data[prev_key+key]=data[key]
        return flat_data