
import sys
import os
import unittest

# Mengatur lokasi folder src
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.insert(0, SRC_DIR)

# Import kedua implementasi SLL
from sll_standard import SinglyLinkedListStandard
from sll_slots import SinglyLinkedListSlots


class SLLTestMixin:
    """
    Kumpulan pengujian yang digunakan oleh
    kedua implementasi Singly Linked List.
    """

    def setUp(self):
        self.sll = self.SLLClass()

    def test_initial_state(self):
        self.assertEqual(len(self.sll), 0)
        self.assertIsNone(self.sll.head)
        self.assertIsNone(self.sll.tail)

    def test_append(self):
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)

        self.assertEqual(len(self.sll), 3)
        self.assertEqual(self.sll.head.data, 10)
        self.assertEqual(self.sll.tail.data, 30)

    def test_prepend(self):
        self.sll.prepend(20)
        self.sll.prepend(10)
        self.sll.prepend(5)

        self.assertEqual(len(self.sll), 3)
        self.assertEqual(self.sll.head.data, 5)
        self.assertEqual(self.sll.tail.data, 20)

    def test_delete_head(self):
        for value in [10, 20, 30]:
            self.sll.append(value)

        result = self.sll.delete_head()

        self.assertEqual(result, 10)
        self.assertEqual(len(self.sll), 2)
        self.assertEqual(self.sll.head.data, 20)

    def test_delete_tail(self):
        for value in [10, 20, 30]:
            self.sll.append(value)

        result = self.sll.delete_tail()

        self.assertEqual(result, 30)
        self.assertEqual(len(self.sll), 2)
        self.assertEqual(self.sll.tail.data, 20)
        self.assertIsNone(self.sll.tail.next)

    def test_delete_at_middle(self):
        for value in [10, 20, 30, 40, 50]:
            self.sll.append(value)

        result = self.sll.delete_at(2)

        self.assertEqual(result, 30)
        self.assertEqual(len(self.sll), 4)
        self.assertTrue(self.sll.search(20))
        self.assertFalse(self.sll.search(30))

    def test_delete_at_head(self):
        for value in [10, 20, 30]:
            self.sll.append(value)

        result = self.sll.delete_at(0)

        self.assertEqual(result, 10)
        self.assertEqual(self.sll.head.data, 20)

    def test_delete_at_tail(self):
        for value in [10, 20, 30]:
            self.sll.append(value)

        result = self.sll.delete_at(2)

        self.assertEqual(result, 30)
        self.assertEqual(self.sll.tail.data, 20)

    def test_delete_single_node(self):
        self.sll.append(10)

        result = self.sll.delete_head()

        self.assertEqual(result, 10)
        self.assertEqual(len(self.sll), 0)
        self.assertIsNone(self.sll.head)
        self.assertIsNone(self.sll.tail)

    def test_delete_tail_single_node(self):
        self.sll.append(10)

        result = self.sll.delete_tail()

        self.assertEqual(result, 10)
        self.assertEqual(len(self.sll), 0)
        self.assertIsNone(self.sll.head)
        self.assertIsNone(self.sll.tail)

    def test_search_found(self):
        self.sll.append(10)
        self.sll.append(20)

        self.assertTrue(self.sll.search(20))

    def test_search_not_found(self):
        self.sll.append(10)
        self.sll.append(20)

        self.assertFalse(self.sll.search(99))

    def test_search_empty(self):
        self.assertFalse(self.sll.search(10))

    def test_delete_head_empty(self):
        with self.assertRaises(IndexError):
            self.sll.delete_head()

    def test_delete_tail_empty(self):
        with self.assertRaises(IndexError):
            self.sll.delete_tail()

    def test_delete_at_empty(self):
        with self.assertRaises(IndexError):
            self.sll.delete_at(0)

    def test_delete_at_negative_index(self):
        self.sll.append(10)

        with self.assertRaises(IndexError):
            self.sll.delete_at(-1)

    def test_delete_at_out_of_range(self):
        self.sll.append(10)

        with self.assertRaises(IndexError):
            self.sll.delete_at(1)

    def test_append_after_emptying(self):
        self.sll.append(10)
        self.sll.delete_head()

        self.sll.append(20)

        self.assertEqual(len(self.sll), 1)
        self.assertEqual(self.sll.head.data, 20)
        self.assertEqual(self.sll.tail.data, 20)

    def test_prepend_after_emptying(self):
        self.sll.append(10)
        self.sll.delete_tail()

        self.sll.prepend(20)

        self.assertEqual(len(self.sll), 1)
        self.assertEqual(self.sll.head.data, 20)
        self.assertEqual(self.sll.tail.data, 20)


class TestSLLStandard(SLLTestMixin, unittest.TestCase):
    """Pengujian untuk NodeStandard."""

    SLLClass = SinglyLinkedListStandard


class TestSLLSlots(SLLTestMixin, unittest.TestCase):
    """Pengujian untuk NodeSlots."""

    SLLClass = SinglyLinkedListSlots


if __name__ == "__main__":
    unittest.main(verbosity=2)
