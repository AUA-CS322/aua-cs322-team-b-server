import unittest
from src.data.organization_chart import OrganizationChart


class TestGetChart(unittest.TestCase):

    organization_chart = OrganizationChart()
    chart = organization_chart.get_chart()

    def test_get_chart_fields(self):
        NORMALIZED_FIELDS = ['nodeId', 'parentNodeId', 'fullName', 'position', 'photoUrl']
        self.assertEqual(list(TestGetChart.chart[0].keys()), NORMALIZED_FIELDS, 'A field is missing')

    def test_get_chart_length(self):
        self.assertEqual(len(TestGetChart.chart), len(TestGetChart.organization_chart._chart),
                         "the lengths do not match")

    def test_get_chart_id_root(self):
        self.assertIsNone(TestGetChart.chart[0]['parentNodeId'], "The parent of root is not None")


if __name__ == '__main__':
    unittest.main()

