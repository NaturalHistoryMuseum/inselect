import unittest
from pathlib import Path

from inselect.lib.document import InselectDocument
from inselect.lib.sort_document_items import sort_document_items


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSortBoxes(unittest.TestCase):
    def test_order_by_rows(self):
        doc = InselectDocument.load(TESTDATA / 'shapes.inselect')

        items = sort_document_items(doc.items, by_columns=False)
        self.assertEqual(
            ['1', '2', '3', '4', '5'],
            [item['fields']['catalogNumber'] for item in items]
        )

    def test_order_by_columns(self):
        doc = InselectDocument.load(TESTDATA / 'shapes.inselect')
        items = sort_document_items(doc.items, by_columns=True)
        self.assertEqual(
            ['1', '4', '3', '2', '5'],
            [item['fields']['catalogNumber'] for item in items]
        )


if __name__ == '__main__':
    unittest.main()
