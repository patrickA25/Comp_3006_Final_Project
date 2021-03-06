import numpy as np
import unittest
from Channel_Squareroot2_Weather import *
from dotenv import load_dotenv

#Getting API Key from .env file
load_dotenv()
API_KEY_NOAA = os.getenv("API_KEY_NOAA")
API_URL_CURIOSITY = os.getenv("CURIOSITY_API")

class TestNOAAAPI(unittest.TestCase):
    
    def test_returndata(self):
        a1 = NOAA_Data(2017,"USW00003167","Spring",False)
        self.assertEqual(200,a1.api_return_value())
        
    #testing the return value for Fall 2017 in DN
    def test_returndates(self):
        a1 = NOAA_Data(2017,"USC00052223","Fall",False)
        comp_value = np.array([88,90,100,94,73,85,82,85,89,91,91,87,95,85,
                                79,70,72,82,90,82,95,78,58,50,55,63,58,65,
                                48,64,73,69,67,83,66,38,62,72,82,68,59,65,
                                78,83,81,77,82,60,69,64,66,87,55,43,60,76,
                                36,54,73,52,58,71,54,41,34,62,45,59,60,58,
                                74,70,57,74,56,50,66,71,54,70,73,70,63,76,
                                80,50])
        self.assertTrue((comp_value==a1.output_max_array()).all())

    #testing the returnv value for Sping 2019 in NY
    def test_returnvalues_min(self):
        a1= NOAA_Data(2019,"USW00094789","Summer",False)
        comp_vlaue = np.array([61,62,57,55,62,64,61,60,57,56,65,57,57,59,55,65,67,66,
                                65,66,66,63,64,63,69,69,69,69,71,69,65,67,72,70,72,75,
                                70,68,68,70,71,73,71,73,69,70,73,71,71,78,80,73,67,65,
                                67,67,70,71,72,75,72,71,72,70,70,70,71,70,69,70,66,64,
                                67,73,70,68,67,73,73,72,74,74,69,66,63,62,60,60,65,67,64,66])
        self.assertTrue((comp_vlaue==a1.output_min_array()).all())
        
    #testing all API is able to connect to each weather stations
    def test_weather_station_LA(self):
        a1 = NOAA_Data(2017,"USW00003167","Spring",False)
        self.assertEquals(a1.api_return_value(), 200)
    
    def test_weather_station_TX(self):
        a1 = NOAA_Data(2019,"USW00013958","Spring",False)
        self.assertEquals(a1.api_return_value(), 200)

    def test_weather_station_FL(self):
        a1 = NOAA_Data(2020,"USW00012815","Spring",False)
        self.assertEquals(a1.api_return_value(), 200)
        
    #Testing that we can pull data from each season
    def test_weather_station_LA_Spring(self):
        a1 = NOAA_Data(2017,"USW00003167","Spring",False)
        self.assertTrue(len(a1.output_date_array())>0)

        
    def test_weather_station_TX_Summer(self):
        a1 = NOAA_Data(2019,"USW00013958","Summer",False)
        self.assertTrue(len(a1.output_date_array())>0)

class TestCuriosity(unittest.TestCase):
    def test_init(self):
        c1 = Curiosity_Data(2012, 'Summer', False) # Test lower limit of the API
        self.assertTrue(len(c1.curiosity_data) > 0)

        c2 = Curiosity_Data(2012, 'Spring', False)
        self.assertFalse(len(c2.curiosity_data) > 0)

        c3 = Curiosity_Data(2021, 'Summer', False) # Test upper limit of the API
        self.assertTrue(len(c3.curiosity_data) > 0)

        c4 = Curiosity_Data(2021, 'Winter', False)
        self.assertFalse(len(c4.curiosity_data) > 0)

        c5 = Curiosity_Data(2020, 'Fall', False) # Test Fall input
        self.assertTrue(len(c5.curiosity_data) > 0)

    @unittest.expectedFailure
    def test_init_season(self):
        c1 = Curiosity_Data(2012, 'Autumn', False) # Testing an invalid season
        self.assertIsInstance(c1)

    @unittest.expectedFailure
    def test_root2report_fail(self):
        m1 = [1, 'a', 2.0] # Arbitrary Mars array
        e1 = [datetime.date(2019, 12, 2), 1, 2, 3, 'a'] # Arbitary Earth array
        m2 = Curiosity_Data(2020, 'Summer', False)
        e2 = NOAA_Data(2020,'USW00003167','Summer')

        # Invalid inputs
        r1 = Root_Two_Report(e1, m1, False, False)
        self.assertIsInstance(r1)

        r2 = Root_Two_Report(e1, m2, False, False)
        self.assertIsInstance(r2)

        r3 = Root_Two_Report(e2, m1, False, False)
        self.assertIsInstance(r3)

        # Valid inputs, but invalid order (Mars, Earth) not (Earth, Mars)
        r4 = Root_Two_Report(m2, e2, False, False)
        self.assertIsInstance(r4)
        
        
if __name__=='__main__':
    unittest.main()