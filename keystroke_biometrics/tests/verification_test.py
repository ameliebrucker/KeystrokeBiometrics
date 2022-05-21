import controller.verification as v
from model.sample import Sample
from model.feature import Feature
import unittest

class TestVerification(unittest.TestCase):

    def setUp(self):
        """
        sets up test values for tests
        """

        self.modelvalues_for_testing = (
            {(Feature.M, "x") : 200,
            (Feature.DD, "xy") : 250,
            (Feature.UD, "xy") : 100,
            (Feature.M, "y") : 150},
            {(Feature.UU, "ab") : 200})

        self.testvalues_for_testing = (
            {(Feature.M, "x") : [180, 210],
            (Feature.DD, "xy") : [220],
            (Feature.UD, "xy") : [80, 300, 220, 250],
            (Feature.DU, "ab") : [100, 150, 250]},
            {(Feature.M, "u") : [280],
            (Feature.DD, "uv") : [400, 450, 320, 120],
            (Feature.UD, "uv") : [110, 320, 280],
            (Feature.DU, "uv") : [100, 150],
            (Feature.M, "v") : [180, 220]},
            {(Feature.M, "a") : [100, 150, 150],
            (Feature.DD, "ab") : [220, 200],
            (Feature.UD, "ab") : [100, 150],
            (Feature.M, "b") : [80]},
            {(Feature.M, "b") : [120, 300],
            (Feature.M, "c") : [180],
            (Feature.DD, "ab") : [180, 200],
            (Feature.DD, "xy") : [300, 320]},
            {(Feature.DD, "xy") : [100, 200],
            (Feature.M, "b") : [200],
            (Feature.M, "a") : [250, 250],
            (Feature.UD, "xy") : [300, 280, 280, 280]})

        self.samples_for_testing = (
            Sample("content", 123456, "username1", self.testvalues_for_testing[1]),
            Sample("content", 123456, "username2", self.testvalues_for_testing[2]),
            Sample("content", 123456, "username3", self.testvalues_for_testing[3]),
            Sample("content", 123456, "username4", self.testvalues_for_testing[4]))

    def test_calculate_euklidean_distance(self):
        """
        tests the calculate_euklidean_distance() function from verification module
        """

        vectors = [(1, 1), (2, 3), (5, 3)]
        # (((1 - 1)^2 + (2 - 3)^2 + (5 - 3)^2) ^ 0.5) / (3 ^ 0.5) = 2.23606797749979 / 1.732050807568877 = 1.290994448735806
        ref = round (1.290994448735806, 4)
        self.assertEqual(v.calculate_euklidean_distance (vectors), ref)

    def test_calculate_euklidean_distance_negative(self):
        """
        tests the calculate_euklidean_distance() function from verification module with negative values
        """

        vectors = [(1, 1), (-2, 3), (5, -3)]
        # (((1 - 1)^2 + (-2 - 3)^2 + (5 + 3)^2) ^ 0.5) / (3 ^ 0.5) = 9.433981132056604 / 1.732050807568877 = 5.446711546122732
        ref = round (5.446711546122732, 4)
        self.assertEqual(v.calculate_euklidean_distance (vectors), ref)

    def test_create_modelvalues(self):
        """
        tests the create_modelvalues() function from verification module
        """

        learnsamples = (self.samples_for_testing[1], self.samples_for_testing[2], self.samples_for_testing[3])
        ref = {
            # (100 + 150 + 150 + 250 + 250) / 5 = 180
            (Feature.M, "a") : 180,
            # (220 + 200 + 180 + 200) / 4 = 200
            (Feature.DD, "ab") : 200,
            # (100 + 150) / 2 = 125
            (Feature.UD, "ab") : 125,
            # (80 + 120 + 300 + 200) / 4 = 175
            (Feature.M, "b") : 175,
            # 180 / 1 = 180
            (Feature.M, "c") : 180,
            # (300 + 320 + 100 + 200) / 4 = 230
            (Feature.DD, "xy") : 230,
            # (300 + 280 + 280 + 280) / 4 = 285
            (Feature.UD, "xy") : 285
        }
        self.assertEqual(v.create_modelvalues(learnsamples).items(), ref.items())

    def test_build_vectors_as_list(self):
        """
        tests the build_vectors_as_list() function from verification module
        """

        modelvalues = self.modelvalues_for_testing[0]
        testvalues = self.testvalues_for_testing[0]
        ref = [
            (200, 180),
            (200, 210),
            (250, 220),
            (100, 80),
            (100, 300),
            (100, 220),
            (100, 250)
        ]
        self.assertEqual(v.build_vectors_as_list(modelvalues, testvalues), ref)

    def test_build_vectors_as_list_no_match (self):
        """
        tests the build_vectors_as_list() function from verification module without a match
        """

        modelvalues = self.modelvalues_for_testing[0]
        testvalues = self.testvalues_for_testing[1]
        ref = []
        self.assertEqual(v.build_vectors_as_list(modelvalues, testvalues), ref)

    def test_create_testvalues_by_nearest_neighbor(self):
        """
        tests the create_testvalues_by_nearest_neighbor() function from verification module
        """

        model = self.modelvalues_for_testing[0]
        testsample = self.samples_for_testing[0]
        ref = {(Feature.M, "x") : [280, 180, 220], (Feature.DD, "xy") : [400, 450, 320, 120], (Feature.UD, "xy") : [110, 320, 280]}
        self.assertEqual(v.create_testvalues_by_nearest_neighbor(model, testsample), ref)

    def test_create_testvalues_by_nearest_neighbor_no_match(self):
        """
        tests the create_testvalues_by_nearest_neighbor() function from verification module without a match
        """

        model = self.modelvalues_for_testing[1]
        testsample = self.samples_for_testing[0]
        ref = {}
        self.assertEqual(v.create_testvalues_by_nearest_neighbor(model, testsample), ref)
    
    def test_verify_per_threshold_multiple_testsamples_not_encrypted(self):
        """
        tests the verify_per_threshold() function from verification module with multiple testsamples and not encrypted
        """

        learnsamples = (self.samples_for_testing[2])
        testsamples = (self.samples_for_testing[1], self.samples_for_testing[3])
        
        """
        # normalized euklidean distance: (((r1 - u1)^2 + ... + (rn - un)^2) ^ 0.5) / (N ^ 0.5)
        # source euklidean distance: F. Monrose, A. D. Rubin: Keystroke dynamics as a biometric for authentication, 2000, http://www1.cs.columbia.edu/~hgs/teaching/security/hw/keystroke.pdf, page 356 (last visit 21/05/2022)
        # testsample 1: (((210 - 80)^2 + (190 - 220)^2 + (190 - 200)^2 + (310 - 100)^2 + (310 - 200)^2) ^ 0.5) / (5 ^ 0.5) = 272.2131517763 / 2.2360679775 = 121.7374223482
        # testsample 2: ((210 - 200)^2) ^ 0.5 = 10

        ref = (6,{
            v.thresholds[0] : 
            })
        """
        return
    
    def test_verify_per_threshold_one_testsample_not_encrypted(self):
        """
        tests the verify_per_threshold() function from verification module with one testsample and not encrypted
        """

        learnsamples = (self.samples_for_testing[2])
        testsamples = (self.samples_for_testing[3])
        
        """
        # normalized euklidean distance: (((r1 - u1)^2 + ... + (rn - un)^2) ^ 0.5) / (N ^ 0.5)
        # source euklidean distance: F. Monrose, A. D. Rubin: Keystroke dynamics as a biometric for authentication, 2000, http://www1.cs.columbia.edu/~hgs/teaching/security/hw/keystroke.pdf, page 356 (last visit 21/05/2022)
        # testsample 1: (((210 - 80)^2 + (190 - 220)^2 + (190 - 200)^2 + (310 - 100)^2 + (310 - 200)^2) ^ 0.5) / (5 ^ 0.5) = 272.2131517763 / 2.2360679775 = 121.7374223482
        # testsample 2: ((210 - 200)^2) ^ 0.5 = 10

        ref = (6,{
            v.thresholds[0] : 
            })
        """
        return
    
    def test_verify_per_threshold_multiple_testsamples_encrypted(self):
        """
        tests the verify_per_threshold() function from verification module with multiple testsamples and encrypted
        """

        return

    def test_verify_per_threshold_one_testsample_encrypted(self):
        """
        tests the verify_per_threshold() function from verification module with one testsample and encrypted
        """

        return

if __name__ == '__main__':
    unittest.main()
