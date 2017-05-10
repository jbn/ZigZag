import numpy as np
import zigzag

from unittest import TestCase
from numpy.testing.utils import assert_array_equal, assert_array_almost_equal
from zigzag import PEAK, VALLEY


class TestIdentifyInitialPivot(TestCase):
    def test_strictly_increasing(self):
        data = np.linspace(1, 2., 10)
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         VALLEY)

    def test_increasing_kinked(self):
        data = np.array([1.0, 0.99, 1.1])
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         PEAK)

    def test_strictly_increasing_under_threshold(self):
        data = np.linspace(1, 1.01, 10)
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         VALLEY)

    def test_increasing_under_threshold_kinked(self):
        data = np.array([1.0, 0.99, 1.02])
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         VALLEY)

    def test_strictly_decreasing(self):
        data = np.linspace(1, 0.5, 10)
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         PEAK)

    def test_decreasing_kinked(self):
        data = np.array([1.0, 1.01, 0.9])
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         VALLEY)

    def test_strictly_decreasing_under_threshold(self):
        data = np.linspace(1, 0.99, 10)
        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         PEAK)

    def test_decreasing_under_threshold_kinked(self):
        data = np.array([1.0, 1.01, 0.99])

        self.assertEqual(zigzag.identify_initial_pivot(data, 0.1, -0.1),
                         PEAK)


class TestPeakValleyPivots(TestCase):
    def test_guard_against_common_threshold_value_mistake(self):
        data = np.array([1.0, 2.0, 3.0])
        self.assertRaises(ValueError, zigzag.peak_valley_pivots,
                          data, 0.1, 0.1)

    def test_strictly_increasing(self):
        data = np.linspace(1, 10, 10)
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.zeros_like(data)
        expected_result[0], expected_result[-1] = VALLEY, PEAK

        assert_array_equal(result, expected_result)

    def test_strictly_increasing_but_less_than_threshold(self):
        data = np.linspace(1.0, 1.05, 10)
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.zeros_like(data)
        expected_result[0], expected_result[-1] = VALLEY, PEAK

        self.assertTrue(data[0] < data[len(data)-1])
        assert_array_equal(result, expected_result)

    def test_strictly_decreasing(self):
        data = np.linspace(10, 0, 10)
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.zeros_like(data)
        expected_result[0], expected_result[-1] = PEAK, VALLEY

        assert_array_equal(result, expected_result)

    def test_strictly_decreasing_but_less_than_threshold(self):
        data = np.linspace(1.05, 1.0, 10)
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.zeros_like(data)
        expected_result[0], expected_result[-1] = PEAK, VALLEY

        assert_array_equal(result, expected_result)

    def test_single_peaked(self):
        data = np.array([1.0, 1.2, 1.05])
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.array([VALLEY, PEAK, VALLEY])

        assert_array_equal(result, expected_result)

    def test_single_valleyed(self):
        data = np.array([1.0, 0.9, 1.2])
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.array([PEAK, VALLEY, PEAK])

        assert_array_equal(result, expected_result)

    def test_increasing_kinked(self):
        data = np.array([1.0, 0.99, 1.1])
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.array([PEAK, VALLEY, PEAK])

        assert_array_equal(result, expected_result)

    def test_decreasing_kinked(self):
        data = np.array([1.0, 1.01, 0.9])
        result = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        expected_result = np.array([VALLEY, PEAK, VALLEY])

        assert_array_equal(result, expected_result)


class TestSegmentReturn(TestCase):
    def test_strictly_increasing(self):
        data = np.linspace(1.0, 100.0, 10)
        pivots = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        assert_array_almost_equal(zigzag.compute_segment_returns(data, pivots),
                                  np.array([99.0]))

    def test_strictly_decreasing(self):
        data = np.linspace(100.0, 1.0, 10)
        pivots = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        assert_array_almost_equal(zigzag.compute_segment_returns(data, pivots),
                                  np.array([-0.99]))

    def test_rise_fall_rise(self):
        data = np.array([1.0, 1.05, 1.1, 1.0, 0.9, 1.5])
        pivots = zigzag.peak_valley_pivots(data, 0.1, -0.1)
        assert_array_almost_equal(zigzag.compute_segment_returns(data, pivots),
                                  np.array([0.1, -0.181818, 0.6666666]))


class TestMaxDrawdown(TestCase):
    def test_strictly_increasing(self):
        data = np.linspace(1.0, 100.0, 10)
        self.assertEquals(zigzag.max_drawdown(data), 0.0)

    def test_strictly_decreasing(self):
        data = np.linspace(100.0, 1.0, 10)
        self.assertEquals(zigzag.max_drawdown(data), 0.99)

    def test_rise_fall_rise_drawdown(self):
        data = np.array([1.0, 1.05, 1.1, 1.0, 0.9, 1.5])
        self.assertAlmostEqual(zigzag.max_drawdown(data), 0.18181818181818188)


class TestPivotsToModes(TestCase):
    def test_pivots_to_modes(self):
        data = np.array([1, 0, 0, 0, -1, 0, 0, 1, -1, 0, 1])
        result = zigzag.pivots_to_modes(data)
        expected_result = np.array([1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1])

        assert_array_equal(result, expected_result)
