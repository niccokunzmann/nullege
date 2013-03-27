try:
    from nullege.test.test import *
except ImportError:
    from test import *

from nullege.find import Samples
import nullege.find


class TestSamples(Samples):
    def _nullege_json(self, name):
        return samples_bytearray

class SamplesTest(unittest.TestCase):
    sample_name = 'bytearray'
    def setUp(self):
        self.samples = TestSamples(self.sample_name)

    def test_access_one_sample(self):
        sample = self.samples[0]
        self.assertEqual(sample.index, 0)
        self.assertEqual(sample.name, self.sample_name)
        self.assertEqual(sample.file, samples_bytearray['samples'][0]['file'])

    def test_iterate_over_samples(self):
        length = len(samples_bytearray['samples'])
        for i, sample in enumerate(self.samples):
            if i + 1 == length:
                self.assertEqual(len(self.samples), length)
                return 
        self.fail('does not load more samples at %i' % i)

    def test_unknown_length_is_None(self):
        self.assertEqual(len(self.samples), 0)
        
if __name__ == '__main__':
    unittest.main(exit = False)


