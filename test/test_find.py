try:
    from nullege.test.test import *
except ImportError:
    from test import *

from nullege.find import find, Samples
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
        for i, sample in enumerate(self.samples):
            if i + 1 == len(samples_bytearray['samples']):
                return
        self.fail('does not load more samples at %i' % i)
        
if __name__ == '__main__':
    unittest.main(exit = False)


