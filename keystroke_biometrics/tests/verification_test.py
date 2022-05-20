import controller.verification as v
import unittest

class TestVerification(unittest.TestCase):

    def test_calculate_euklidean_distance(self):
        # create vector list
        vectors = [(1, 1), (2, 3), (5, 3)]
        self.assertEqual(v.calculate_euklidean_distance (vectors), 6)

    def test_create_modelvalues(self):
        # create learnsamples
        return

    def test_build_vectors_as_list (self):
        # create modelvalues, testvalues
        return

    def test_build_vectors_as_list_no_match (self):
        # create modelvalues, testvalues
        return

    def test_create_testvalues_by_nearest_neighbor(self):
        # create model, testsample
        return
    
    def test_verify_per_threshold_not_encrypted(self):
        # create learnsamples, testsamples
        return
    
    def test_verify_per_threshold_encrypted(self):
        # create learnsamples, testsamples
        return

if __name__ == '__main__':
    unittest.main()
