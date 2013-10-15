import csv
import StringIO
import time
import sys
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProximityListener(FileSystemEventHandler):
    """A proximity listener"""
    def __init__(self, listener_id, ssid, csv_file, data_handler):
        super(ProximityListener, self).__init__()
        self.ssid = ssid
        self.csv_file = csv_file
        self.data_handler = data_handler
        self.listener_id = listener_id
    
    def getSignalStrengths(self):
        (access_points, clients) = self.parseCSV()
        filtered_access_points = self.filterAccessPoints(access_points)
        filtered_clients = self.filterClients(clients, map(lambda x: x['BSSID'], filtered_access_points))
        signal_strengths = {}
        for client in filtered_clients:
            signal_strengths[client['Station MAC']] = client['Power']
        return signal_strengths
        
    def parseCSV(self):
        accesspoints = []
        clients = []
        target = accesspoints
        csvfile =  open(self.csv_file, 'r')
        for line in csvfile.readlines():
            if line[:7] == 'Station':
                target = clients
            if len(line)<3:
                continue
            target.append(line)
        access_point_string = ''.join(accesspoints)
        client_string = ''.join(clients)
        
        access_point_reader = csv.DictReader(StringIO.StringIO(access_point_string), delimiter=',')
        client_reader = csv.DictReader(StringIO.StringIO(client_string), delimiter=',')
        access_points = []
        clients = []
        for row in access_point_reader:
            access_points.append(row)
        for row in client_reader:
            clients.append(row)
        access_points = self.cleanDictList(access_points)
        clients = self.cleanDictList(clients)
        return (access_points, clients)
        
    def cleanDictList(self, l):
        new_list = []
        for d in l:
            if None in d.keys():
                d.pop(None, None)
            new_list.append({k.lstrip():v.lstrip() for k, v in d.iteritems()})
        return new_list
            
    def filterAccessPoints(self, access_points):
        new_list = []
        for access_point in access_points:
            if access_point['ESSID'] == self.ssid:
                new_list.append(access_point)
        return new_list
        
    def filterClients(self, clients, BSSIDs):
        new_list = []
        for client in clients:
            if client['BSSID'] in BSSIDs:
                new_list.append(client)
        return new_list
        
    def on_modified(self, event):
        signal_strengths = self.getSignalStrengths()
        to_send = {'listenerId': self.listener_id, 'proximityData': signal_strengths}
        self.data_handler.handle_data(to_send)
        
class JSONPoster(object):
    """Simple class for posting data"""
    def __init__(self, url):
        super(JSONPoster, self).__init__()
        self.url = url
        
    def handle_data(self, data):
        url = self.url
        data = data
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "Usage: python proximity_listener.py <listener id> <ssid> <csv-file> <server-url>"
        exit(0)
    event_handler = ProximityListener(sys.argv[1], sys.argv[2], sys.argv[3], JSONPoster(sys.argv[4]))
    observer = Observer()
    path = '/'.join(sys.argv[2].split('/')[:len(sys.argv[2].split('/'))-1])
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()