import unittest
from SolarCalc.model import SolarDataProcessor

class TestSolarDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = SolarDataProcessor()
    
    def testInitialClassState(self):
        self.assertIsInstance(self.processor, SolarDataProcessor)

if __name__ == '__main__':
    unittest.main()

