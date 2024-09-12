import unittest
import pandas as pd
import numpy as np
from UserProfile import process_data, generate_age_groups, calculate_percentile_bounds

class TestUserPortrait(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Sample data for testing
        cls.df = pd.DataFrame({
            'Predicted Age': [22, 35, 44, 55, 28, np.nan, 42],
            'Predicted Zodiac Sign': ['Aries', 'Leo', 'Virgo', 'Cancer', 'Aries', 'Gemini', np.nan],
            'Predicted MBTI': ['INTJ', 'ENTP', np.nan, 'ENFP', 'INTP', 'ISFJ', 'ENTP'],
            'Last 7-day Cat1 Purchase Amount': [120, 340, 560, 80, 300, 400, 150]
        })

    def test_generate_age_groups(self):
        # Assuming generate_age_groups is a function that assigns age groups
        age_bins = [18, 25, 35, 45, 55, 65, 75, 90]
        age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-90']
        result = generate_age_groups(self.df['Predicted Age'], age_bins, age_labels)
        
        # Check if the age groups are generated correctly
        expected_groups = pd.Categorical(['18-25', '36-45', '46-55', '56-65', '26-35', np.nan, '36-45'])
        pd.testing.assert_series_equal(result, expected_groups, check_names=False)

    def test_handle_null_mbti(self):
        # Test how null MBTI values are handled
        null_percentage = self.df['Predicted MBTI'].isna().mean() * 100
        self.assertAlmostEqual(null_percentage, 14.29, places=2)

    def test_calculate_percentile_bounds(self):
        # Test the boundary calculation (5th and 95th percentile)
        lower_bound, upper_bound = calculate_percentile_bounds(self.df['Last 7-day Cat1 Purchase Amount'], 5, 95)
        self.assertEqual(lower_bound, 93)  # The 5th percentile value
        self.assertEqual(upper_bound, 526)  # The 95th percentile value

    def test_zodiac_distribution(self):
        # Test the Zodiac Sign distribution
        zodiac_counts = self.df['Predicted Zodiac Sign'].value_counts(dropna=False)
        expected_counts = pd.Series({'Aries': 2, 'Leo': 1, 'Virgo': 1, 'Cancer': 1, 'Gemini': 1, np.nan: 1})
        pd.testing.assert_series_equal(zodiac_counts, expected_counts)

    def test_plot_functions(self):
        # You can also test if a plot is generated without raising errors
        try:
            process_data(self.df)
        except Exception as e:
            self.fail(f"Plotting function raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
