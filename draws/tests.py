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

    def test_clear_all_removes_every_call(self):
        services.add_number(self.event, "125")
        services.add_number(self.event, "044")
        services.clear_all(self.event)
        self.assertEqual(self.event.called_count, 0)


class WinnerLogicTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name="Test Draw", prize_interval=3)

    def test_no_prize_interval_never_auto_wins(self):
        event = Event.objects.create(name="No prizes")
        self.assertFalse(services.is_auto_winner(event, 1))
        self.assertFalse(services.is_auto_winner(event, 3))

    def test_auto_winner_starts_at_first_call(self):
        self.assertTrue(services.is_auto_winner(self.event, 1))
        self.assertFalse(services.is_auto_winner(self.event, 2))
        self.assertFalse(services.is_auto_winner(self.event, 3))
        self.assertTrue(services.is_auto_winner(self.event, 4))
        self.assertTrue(services.is_auto_winner(self.event, 7))

    def test_effective_winner_falls_back_to_auto_rule(self):
        call = services.add_number(self.event, "001")
        self.assertTrue(services.effective_winner(self.event, call))
        call2 = services.add_number(self.event, "002")
        self.assertFalse(services.effective_winner(self.event, call2))

    def test_toggle_winner_overrides_auto_rule(self):
        services.add_number(self.event, "001")
        call = services.add_number(self.event, "002")
        self.assertFalse(services.effective_winner(self.event, call))
        services.toggle_winner(self.event, call)
        self.assertTrue(services.effective_winner(self.event, call))
        services.toggle_winner(self.event, call)
        self.assertFalse(services.effective_winner(self.event, call))
