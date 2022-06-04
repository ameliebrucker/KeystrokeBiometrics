import controller.verification as v
from model.sample import Sample
from model.feature import Feature
import unittest

class TestVerification(unittest.TestCase):
    """
    A class for testing functions from verification module

    Attributes (Object)
    modelvalues_for_testing: example modelvalues for test functions
    testvalues_for_testing: example testvalues for test functions
    samples_for_testing: example samples for test functions

    Methods
    setUp(): sets up test values before tests
    test_calculate_euklidean_distance(): tests the calculate_euklidean_distance() function
    test_calculate_euklidean_distance_negative(): tests the calculate_euklidean_distance() function with negative values
    test_create_modelvalues(): tests the create_modelvalues() function
    test_build_vectors_as_list(): tests the build_vectors_as_list() function
    test_build_vectors_as_list_no_match (): tests the build_vectors_as_list() function without a match
    test_create_testvalues_by_nearest_neighbor(): tests the create_testvalues_by_nearest_neighbor() function
    test_create_testvalues_by_nearest_neighbor_no_match(): tests the create_testvalues_by_nearest_neighbor() function without a match    
    test_verify_samples_multiple_testsamples_not_encrypted(): tests the verify_samples() function with multiple testsamples and not encrypted
    test_verify_samples_one_testsample_not_encrypted(): tests the verify_samples() function with one testsample and not encrypted
    test_verify_samples_not_encrypted_no_match(): tests the verify_samples() function not encrypted and with no comparable data
    test_verify_samples_multiple_testsamples_encrypted(): tests the verify_samples() function with multiple testsamples and encrypted
    test_verify_per_threshold_one_testsample_encrypted(): tests the verify_per_threshold() function with one testsample and encrypted
    test_verify_samples_no_learnsamples(): tests the verify_samples() function with empty learnsamples list
    test_verify_samples_no_testsamples(): tests the verify_samples() function with empty testsamples list
    test_get_results_per_threshold(): tests the get_results_per_threshold() function
    test_get_results_per_threshold_no_compared_values(): tests the get_results_per_threshold() function with compared_values = 0
    """

    def setUp(self):
        """
        sets up test values before tests
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
            (Feature.UD, "xy") : [300, 280, 280, 280]},
            {(Feature.DD, "ab") : [160],
            (Feature.M, "y") : [200]})

        self.samples_for_testing = (
            Sample("content", 123456, "username1", self.testvalues_for_testing[1]),
            Sample("content", 123456, "username2", self.testvalues_for_testing[2]),
            Sample("content", 123456, "username3", self.testvalues_for_testing[3]),
            Sample("content", 123456, "username4", self.testvalues_for_testing[4]),
            Sample("content", 123456, "username5", self.testvalues_for_testing[5]))

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

        learnsamples = [self.samples_for_testing[1], self.samples_for_testing[2], self.samples_for_testing[3]]
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
        self.assertEqual(v.build_vectors_as_list(modelvalues, testvalues), [])

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
        self.assertEqual(v.create_testvalues_by_nearest_neighbor(model, testsample), {})
    
    def test_verify_samples_multiple_testsamples_not_encrypted(self):
        """
        tests the verify_samples() function from verification module with multiple testsamples and not encrypted
        """

        learnsamples = [self.samples_for_testing[2]]
        testsamples = [self.samples_for_testing[1], self.samples_for_testing[3]]

        # model: {(Feature.M, "b") : 210, (Feature.M, "c") : 180, (Feature.DD, "ab") : 190, (Feature.DD, "xy") : 310}
        # vector testsample 1: [(190, 220), (190, 200), (210, 80)]
        # vector testsample 2: [(310, 100), (310, 200), (210, 200)]
        # normalized euklidean distance
        # testsample 1: (((190 - 220)^2 + (190 - 200)^2 + (210 - 80)^2) ^ 0.5) / (3 ^ 0.5) = 133.7908816025965 / 1.732050807568877 = 77.24420150837645
        # testsampe 2: (((310 - 100)^2 + (310 - 200)^2 + (210 - 200)^2 ^ 0.5) / (3 ^ 0.5) = 237.2762103541 / 1.732050807568877 = 136.9914839257
        ref = (6, 137, {self.samples_for_testing[1].get_short_identifier() : 77.2442, self.samples_for_testing[3].get_short_identifier() : 136.9915})
        self.assertEqual(v.verify_samples(learnsamples, testsamples, False), ref)
    
    def test_verify_samples_one_testsample_not_encrypted(self):
        """
        tests the verify_samples() function from verification module with one testsample and not encrypted
        """

        learnsamples = [self.samples_for_testing[3]]
        testsamples = [self.samples_for_testing[1]]
        # model: {(Feature.DD, "xy") : 150, (Feature.M, "b") : 200, (Feature.M, "a") : 250, (Feature.UD, "xy") : 285}
        # vector: [(200, 80), (250, 100), (250, 150), (250, 150)]
        # normalized euklidean distance: (((200 - 80)^2 + (250 - 100)^2 + (250 - 150)^2 + (250 - 150)^2) ^ 0.5) / (4 ^ 0.5) = 238.5372088375313 / 2 = 119.2686044187656
        ref = (4, 120, {self.samples_for_testing[1].get_short_identifier() : 119.2686})
        self.assertEqual(v.verify_samples(learnsamples, testsamples, False), ref)
    
    def test_verify_samples_not_encrypted_no_match(self):
        """
        tests the verify_samples() function from verification module not encrypted and with no comparable data
        """

        learnsamples = [self.samples_for_testing[0]]
        testsamples = [self.samples_for_testing[1], self.samples_for_testing[2]]
        self.assertEqual(v.verify_samples(learnsamples, testsamples, False), (0, 0, {}))
    
    def test_verify_samples_multiple_testsamples_encrypted(self):
        """
        tests the verify_samples() function from verification module with multiple testsamples and encrypted
        """

        learnsamples = [self.samples_for_testing[3]]
        testsamples = [self.samples_for_testing[1], self.samples_for_testing[4]]
        # model: {(Feature.DD, "xy") : 150, (Feature.M, "b") : 200, (Feature.M, "a") : 250, (Feature.UD, "xy") : 285}
        # vector testsample 1 encrypted: [(200, 100), (200, 150), (200, 150), (150, 220), (150, 200), (285, 100), (285, 150), (200, 80)]
        # vector testsample 2 encrypted: [(150, 160), (200, 200)]
        # normalized euklidean distance
        # testsample 1: (((200 - 100)^2 + (200 - 150)^2 + (200 - 150)^2 + (150 - 220)^2 + (150 - 200)^2 + (285 - 100)^2 + (285 - 150)^2 + (200 - 80)^2) ^ 0.5) / (8 ^ 0.5) = 298.7473849258 / 2.82842712474619 = 105.6231508731
        # testsample 2: (((150 - 160)^2 + (200 - 200)^2) ^ 0.5) / (2 ^ 0.5) = 7.0710678119
        ref = (10, 106, {self.samples_for_testing[1].get_short_identifier() : 105.6232, self.samples_for_testing[4].get_short_identifier() : 7.0711})        
        self.assertEqual(v.verify_samples(learnsamples, testsamples, True), ref)

    def test_verify_per_threshold_one_testsample_encrypted(self):
        """
        tests the verify_per_threshold() function from verification module with one testsample and encrypted
        """

        learnsamples = [self.samples_for_testing[3]]
        testsamples = [self.samples_for_testing[1]]
        # model: {(Feature.DD, "xy") : 150, (Feature.M, "b") : 200, (Feature.M, "a") : 250, (Feature.UD, "xy") : 285}
        # vector encrypted: [(200, 100), (200, 150), (200, 150), (150, 220), (150, 200), (285, 100), (285, 150), (200, 80)]
        # normalized euklidean distance: (((200 - 100)^2 + (200 - 150)^2 + (200 - 150)^2 + (150 - 220)^2 + (150 - 200)^2 + (285 - 100)^2 + (285 - 150)^2 + (200 - 80)^2) ^ 0.5) / (8 ^ 0.5) = 298.7473849258 / 2.82842712474619 = 105.6231508731
        ref = (8, 106, {self.samples_for_testing[1].get_short_identifier() : 105.6232})
        self.assertEqual(v.verify_samples(learnsamples, testsamples, True), ref)

    def test_verify_samples_no_learnsamples(self):
        """
        tests the verify_samples() function from verification module with empty learnsamples list
        """
        
        testsamples = [self.samples_for_testing[1], self.samples_for_testing[3]]
        self.assertEqual(v.verify_samples([], testsamples, False), (0, 0, {}))

    def test_verify_samples_no_testsamples(self):
        """
        tests the verify_samples() function from verification module with empty testsamples list
        """
        
        learnsamples = [self.samples_for_testing[1], self.samples_for_testing[3]]
        self.assertEqual(v.verify_samples(learnsamples, [], False), (0, 0, {}))

    def test_get_results_per_threshold(self):
        """
        tests the get_results_per_threshold() function from verification module
        """

        #res = (results_as_text, y_acceptance, y_rejection)
        distance_per_sample_for_testing = {self.samples_for_testing[0].get_short_identifier() : 100}
        max_distance = 200
        compared_values = 20
        # thresholds: 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200
        results_as_text = f"Threshold span:\n0 ms (0) - 200 ms (1)\n\nAcceptance:\n\n0.0 (0000 ms) - 0.0 %\n0.1 (0020 ms) - 0.0 %\n0.2 (0040 ms) - 0.0 %\n0.3 (0060 ms) - 0.0 %\n0.4 (0080 ms) - 0.0 %\n0.5 (0100 ms) - 100.0 %\n0.6 (0120 ms) - 100.0 %\n0.7 (0140 ms) - 100.0 %\n0.8 (0160 ms) - 100.0 %\n0.9 (0180 ms) - 100.0 %\n1.0 (0200 ms) - 100.0 %\n\nRejection:\n\n0.0 (0000 ms) - 100.0 %\n0.1 (0020 ms) - 100.0 %\n0.2 (0040 ms) - 100.0 %\n0.3 (0060 ms) - 100.0 %\n0.4 (0080 ms) - 100.0 %\n0.5 (0100 ms) - 0.0 %\n0.6 (0120 ms) - 0.0 %\n0.7 (0140 ms) - 0.0 %\n0.8 (0160 ms) - 0.0 %\n0.9 (0180 ms) - 0.0 %\n1.0 (0200 ms) - 0.0 %\n\nNormalized euklidean distance:\n\n1. Testsample\n\"{self.samples_for_testing[0].get_short_identifier()}\"\nDistance: 100.0000 ms\n\nCompared values in total: {compared_values}"               
        y_acceptance = [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        y_rejection = [100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        res = (results_as_text, y_acceptance, y_rejection)
        self.assertEqual(v.get_results_per_threshold(distance_per_sample_for_testing, compared_values, max_distance), res)

    def test_get_results_per_threshold_no_compared_values(self):
        """
        tests the get_results_per_threshold() function from verification module with compared_values = 0
        """

        self.assertEqual(v.get_results_per_threshold({}, 0, 0), (None, None, None))

if __name__ == '__main__':
    unittest.main()
