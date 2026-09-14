from django.test import TestCase

from . import services
from .models import Event


class LoserBoardTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name="Test Draw")

    def test_add_number_sets_position(self):
        call = services.add_number(self.event, "125")
        self.assertEqual(call.number, "125")
        self.assertEqual(call.position, 1)

    def test_add_number_increments_position(self):
        services.add_number(self.event, "125")
        second = services.add_number(self.event, "044")
        self.assertEqual(second.position, 2)

    def test_add_number_strips_whitespace(self):
        call = services.add_number(self.event, "  125  ")
        self.assertEqual(call.number, "125")

    def test_add_blank_number_raises(self):
        with self.assertRaises(ValueError):
            services.add_number(self.event, "   ")

    def test_add_duplicate_number_raises(self):
        services.add_number(self.event, "125")
        with self.assertRaises(ValueError):
            services.add_number(self.event, "125")

    def test_undo_last_removes_most_recent_call(self):
        services.add_number(self.event, "125")
        services.add_number(self.event, "044")
        undone = services.undo_last(self.event)
        self.assertEqual(undone.number, "044")
        self.assertEqual(self.event.called_count, 1)

    def test_undo_last_with_no_calls_raises(self):
        with self.assertRaises(ValueError):
            services.undo_last(self.event)

    def test_undo_then_reenter_same_number(self):
        services.add_number(self.event, "125")
        services.undo_last(self.event)
        call = services.add_number(self.event, "125")
        self.assertEqual(call.position, 1)
