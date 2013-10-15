import unittest
from proximity_listener import ProximityListener

class ProximityListenerTest(unittest.TestCase):
    
    def setUp(self):
        self.proximityListener = ProximityListener('AU-Gadget', 'tests/test_data/test_data.csv')
    
    def test_correct_mac_in_signal_strengths(self):
        signalStrengths = self.proximityListener.getSignalStrengths()
        assert '74:E5:0B:40:E1:A2' in signalStrengths
        
    def test_another_correct_mac_in_signal_strengths(self):
        signalStrengths = self.proximityListener.getSignalStrengths()
        assert '58:1F:AA:31:C0:91' in signalStrengths
            
    def test_mac_on_different_network_not_in_signal_strengths(self):
        signalStrengths = self.proximityListener.getSignalStrengths()
        assert 'A0:0B:BA:C4:AD:EF' not in signalStrengths
        
    def test_mac_on_unknown_network_not_in_signal_strengths(self):
        signalStrengths = self.proximityListener.getSignalStrengths()
        assert 'E4:25:E7:01:28:F0' not in signalStrengths
        
    def test_parse_csv_file(self):
        (accesspoints, clients) = self.proximityListener.parseCSV()
        assert accesspoints is not None
        assert clients is not None

    def test_filter_access_points(self):
        (accesspoints, clients) = self.proximityListener.parseCSV()
        filtered_access_points = self.proximityListener.filterAccessPoints(accesspoints)
        assert len(filtered_access_points) == 3
        assert filtered_access_points[0]['ESSID'] == 'AU-Gadget'
        assert filtered_access_points[1]['ESSID'] == 'AU-Gadget'
        assert filtered_access_points[2]['ESSID'] == 'AU-Gadget'
        
    def test_filter_clients(self):
        (accesspoints, clients) = self.proximityListener.parseCSV()
        filtered_access_points = self.proximityListener.filterAccessPoints(accesspoints)
        bssids = map(lambda x: x['BSSID'], filtered_access_points)
        filtered_clients = self.proximityListener.filterClients(clients, bssids)
        print (len(filtered_clients))
        assert len(filtered_clients) == 13
