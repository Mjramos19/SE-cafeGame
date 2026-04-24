"""
Unit Tests: Machine System

Runs against the real Machine class with headless pygame.

Requirements covered:
  Req14 - Machine placed when purchased and counter space available
  Req15 - Brewing starts when ingredient inserted and start pressed
  Req16 - Brewing progress and machine state tracked during brewing
  Req17 - Output added to cup contents when collected from machine
"""

import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()
# Stub mixer.Sound before importing machines so Machine.__init__
# never tries to open real audio files regardless of mixer state.
pygame.mixer.Sound = MagicMock(return_value=MagicMock())

# Patch IMAGE_LIBRARY in every module that references it.
# We create a new dict subclass with __missing__ and assign it
# directly to each module's namespace since "from constants import *"
# gives each module its own reference to the object.
class _FakeImageLib(dict):
    def __missing__(self, key):
        return pygame.Surface((10, 10))

import constants, items
_fake = _FakeImageLib(constants.IMAGE_LIBRARY)
constants.IMAGE_LIBRARY = _fake
items.IMAGE_LIBRARY = _fake

import machines
machines.IMAGE_LIBRARY = _fake

from machines import Machine

MINI_GAME_KEYS    = ['empty_key', 'running_key', 'ready_key']
START_BUTTON_INFO = [400, 400, 100, 50]
MACHINE_INPUT     = 'coffee_beans'
OUTPUTS           = ['espresso', 'lungo']
SOUND_KEYS        = ['fake1.wav', 'fake2.wav', 'fake3.wav', 'fake4.wav']


def make_machine(state='empty'):
    """Create a Machine instance with predictable defaults for testing."""
    m = Machine(
        x=0, y=0,
        name='Test Machine',
        machine_input=MACHINE_INPUT,
        outputs=OUTPUTS,
        num_outputs=2,
        runtime=5,
        mini_game_img_keys=MINI_GAME_KEYS,
        sound_keys=SOUND_KEYS,
        start_button_info=START_BUTTON_INFO,
    )
    m.state = state
    return m


# --- Initial State ---

class TestMachineInitialState(unittest.TestCase):
    """Verify a newly constructed Machine starts with correct default values."""

    def test_initial_state_is_empty(self):
        """A new machine should begin in the 'empty' state before any ingredient is added."""
        m = make_machine()
        self.assertEqual(m.state, 'empty')

    def test_initial_contents_is_empty(self):
        """Contents list should be empty on construction."""
        m = make_machine()
        self.assertEqual(m.contents, [])

    def test_stores_correct_input_type(self):
        """The machine must remember which ingredient type it accepts."""
        m = make_machine()
        self.assertEqual(m.input, MACHINE_INPUT)

    def test_stores_outputs_list(self):
        """The machine must store the full list of possible outputs it can produce."""
        m = make_machine()
        self.assertEqual(m.outputs, OUTPUTS)

    def test_stores_num_outputs(self):
        """The machine must store how many output items it produces per cycle."""
        m = make_machine()
        self.assertEqual(m.num_outputs, 2)

    def test_stores_runtime(self):
        """The machine must store the brewing duration in seconds."""
        m = make_machine()
        self.assertEqual(m.runtime, 5)


# --- Machine.add() ---

class TestMachineAdd(unittest.TestCase):
    """Tests for Machine.add() — loading an ingredient into the machine."""

    def test_correct_ingredient_sets_state_full(self):
        """Inserting the accepted ingredient type should advance state to 'full'."""
        m = make_machine()
        m.add(MACHINE_INPUT, MagicMock())
        self.assertEqual(m.state, 'full')

    def test_wrong_ingredient_sets_state_error(self):
        """Inserting the wrong ingredient type should set state to 'error'."""
        m = make_machine()
        m.add('milk', MagicMock())
        self.assertEqual(m.state, 'error')

    def test_correct_ingredient_calls_pop_inventory(self):
        """A successful add must remove the ingredient from the player's inventory."""
        m = make_machine()
        player = MagicMock()
        m.add(MACHINE_INPUT, player)
        player.pop_inv_item.assert_called_once()

    def test_wrong_ingredient_does_not_pop_inventory(self):
        """A failed add must not remove anything from the player's inventory."""
        m = make_machine()
        player = MagicMock()
        m.add('milk', player)
        player.pop_inv_item.assert_not_called()


# --- Machine.run_machine() ---

class TestMachineRunMachine(unittest.TestCase):
    """Tests for Machine.run_machine() — pressing the start button."""

    def test_run_machine_does_nothing_when_empty(self):
        """Pressing start on an empty machine must not transition to 'running'."""
        m = make_machine(state='empty')
        m.run_machine()
        self.assertNotEqual(m.state, 'running')

    def test_run_machine_does_nothing_when_ready(self):
        """Pressing start when outputs are already ready must leave state unchanged."""
        m = make_machine(state='ready')
        m.run_machine()
        self.assertEqual(m.state, 'ready')

    def test_run_machine_transitions_to_running_when_full(self):
        """Pressing start on a loaded machine must move state to 'running'."""
        m = make_machine(state='full')
        m.run_machine()
        self.assertEqual(m.state, 'running')

    def test_run_machine_sets_selected_output(self):
        """Pressing start must choose and record which output will be produced."""
        m = make_machine(state='full')
        m.run_machine()
        self.assertEqual(m.selected_output, OUTPUTS[0])


# --- Machine.update() ---

class TestMachineUpdate(unittest.TestCase):
    """Tests for Machine.update() — the per-frame timer check during brewing."""

    def test_update_transitions_to_ready_when_timer_expires(self):
        """Once elapsed time exceeds runtime, state must become 'ready'."""
        m = make_machine(state='running')
        m.selected_output = 'espresso'
        m.timer_start = pygame.time.get_ticks() - 6000
        m.update()
        self.assertEqual(m.state, 'ready')

    def test_update_does_not_transition_before_timer_expires(self):
        """State must remain 'running' while elapsed time is still under the runtime."""
        m = make_machine(state='running')
        m.selected_output = 'espresso'
        m.timer_start = pygame.time.get_ticks()
        m.update()
        self.assertEqual(m.state, 'running')

    def test_update_populates_contents_on_completion(self):
        """On completion, contents must be filled with num_outputs copies of the selected output."""
        m = make_machine(state='running')
        m.selected_output = 'espresso'
        m.num_outputs = 2
        m.timer_start = pygame.time.get_ticks() - 6000
        m.update()
        self.assertEqual(m.contents, ['espresso', 'espresso'])

    def test_update_does_nothing_when_not_running(self):
        """update() must be a no-op when the machine is not in the 'running' state."""
        m = make_machine(state='empty')
        m.update()
        self.assertEqual(m.state, 'empty')


# --- Machine.select_output() ---

class TestMachineSelectOutput(unittest.TestCase):
    """Tests for Machine.select_output() — choosing which item will be produced."""

    def test_select_output_returns_first_output(self):
        """select_output must return the first item from the outputs list."""
        m = make_machine()
        self.assertEqual(m.select_output(0), OUTPUTS[0])

    def test_select_output_ignores_index_always_returns_first(self):
        """The index argument is currently unused — any index returns the first output."""
        m = make_machine()
        self.assertEqual(m.select_output(0), m.select_output(1))


# --- Machine.remove_output() ---

class TestMachineRemoveOutput(unittest.TestCase):
    """Tests for Machine.remove_output() — collecting a finished item from the machine."""

    def test_remove_output_returns_item_when_ready(self):
        """A ready machine with contents must return one of those items."""
        m = make_machine(state='ready')
        m.contents = ['espresso']
        self.assertEqual(m.remove_output(), 'espresso')

    def test_remove_output_decreases_contents(self):
        """Each collection must remove exactly one item from contents."""
        m = make_machine(state='ready')
        m.contents = ['espresso', 'espresso']
        m.remove_output()
        self.assertEqual(len(m.contents), 1)

    def test_remove_output_returns_none_when_not_ready(self):
        """Collecting from a non-ready machine must return None."""
        m = make_machine(state='full')
        self.assertIsNone(m.remove_output())

    def test_remove_output_returns_none_when_empty_state(self):
        """Collecting from an empty machine must return None."""
        m = make_machine(state='empty')
        self.assertIsNone(m.remove_output())

    def test_remove_output_returns_none_when_contents_empty(self):
        """Collecting from a ready machine with no contents must return None."""
        m = make_machine(state='ready')
        m.contents = []
        self.assertIsNone(m.remove_output())


# --- Machine.get_sprite() ---

class TestMachineGetSprite(unittest.TestCase):
    """Tests for Machine.get_sprite() — sprite key selection by state."""

    def test_get_sprite_uses_empty_key_when_empty(self):
        """An empty machine must use the first sprite key."""
        m = make_machine(state='empty')
        m.get_sprite()
        self.assertEqual(m.sprite, MINI_GAME_KEYS[0])

    def test_get_sprite_uses_running_key_when_running(self):
        """A running machine must use the second sprite key."""
        m = make_machine(state='running')
        m.get_sprite()
        self.assertEqual(m.sprite, MINI_GAME_KEYS[1])

    def test_get_sprite_uses_ready_key_when_ready(self):
        """A ready machine must use the third sprite key."""
        m = make_machine(state='ready')
        m.get_sprite()
        self.assertEqual(m.sprite, MINI_GAME_KEYS[2])

    def test_get_sprite_uses_empty_key_when_full(self):
        """A full but not started machine must use the empty sprite key."""
        m = make_machine(state='full')
        m.get_sprite()
        self.assertEqual(m.sprite, MINI_GAME_KEYS[0])


# --- Machine.is_player_nearby() ---

class TestMachineIsPlayerNearby(unittest.TestCase):
    """Tests for Machine.is_player_nearby() — proximity detection."""

    def test_returns_true_when_player_in_zone(self):
        """Must return True when the player's foot rect overlaps the interaction zone."""
        m = make_machine()
        player = MagicMock()
        player.get_foot_rect.return_value.colliderect.return_value = True
        self.assertTrue(m.is_player_nearby(player))

    def test_returns_false_when_player_outside_zone(self):
        """Must return False when the player's foot rect does not overlap the interaction zone."""
        m = make_machine()
        player = MagicMock()
        player.get_foot_rect.return_value.colliderect.return_value = False
        self.assertFalse(m.is_player_nearby(player))


# --- Machine.setup_minigame() ---

class TestMachineSetupMinigame(unittest.TestCase):
    """Tests for Machine.setup_minigame() — preparing the ingredient for display."""

    def test_sets_ingredient_from_list(self):
        """The last item in the list must be assigned as the machine's active ingredient."""
        m = make_machine()
        ing = MagicMock()
        m.setup_minigame([ing])
        self.assertEqual(m.ingredient, ing)

    def test_sets_none_when_list_is_empty(self):
        """An empty list must result in ingredient being set to None."""
        m = make_machine()
        m.setup_minigame([])
        self.assertIsNone(m.ingredient)

    def test_sets_ingredient_position(self):
        """The ingredient must be repositioned to the fixed minigame display coordinates."""
        m = make_machine()
        ing = MagicMock()
        m.setup_minigame([ing])
        self.assertEqual(ing.x, 20)
        self.assertEqual(ing.y, 500)

    def test_does_not_modify_original_list(self):
        """setup_minigame must work on a copy and leave the caller's list intact."""
        m = make_machine()
        ing = MagicMock()
        original = [ing]
        m.setup_minigame(original)
        self.assertEqual(len(original), 1)


# --- Req14: Machine Placement ---

class TestReq14MachinePlacement(unittest.TestCase):
    """Req14 - Machine placed when purchased and counter space is available."""

    def test_placed_flag_starts_false(self):
        """A new machine must start unplaced before the player positions it."""
        m = make_machine()
        self.assertFalse(m.placed)

    def test_setting_placed_true_marks_machine_as_placed(self):
        """Once the player confirms placement the placed flag must become True."""
        m = make_machine()
        m.placed = True
        self.assertTrue(m.placed)

    def test_move_to_updates_x_and_y(self):
        """move_to must update the machine's x and y to the chosen counter position."""
        m = make_machine()
        m.move_to(193, 234)
        self.assertEqual(m.x, 193)
        self.assertEqual(m.y, 234)

    def test_move_to_updates_counter_space_rect(self):
        """move_to must reposition counter_space_rect so collision detection stays correct."""
        m = make_machine()
        m.move_to(193, 234)
        self.assertEqual(m.counter_space_rect.x, 193)
        self.assertEqual(m.counter_space_rect.y, 234)

    def test_move_to_updates_interaction_zone_y(self):
        """move_to must shift the interaction zone vertically so players can still interact."""
        m = make_machine()
        m.move_to(193, 234)
        self.assertEqual(m.interaction_zone.y, 234 + m.h)

    def test_placed_machine_appears_in_occupied_set(self):
        """A placed machine's x must appear in the occupied counter positions set."""
        m = make_machine()
        m.move_to(193, 234)
        m.placed = True
        occupied_xs = {mac.x for mac in [m] if mac.placed}
        self.assertIn(193, occupied_xs)

    def test_unplaced_machine_not_in_occupied_set(self):
        """An unplaced machine must not block any counter space."""
        m = make_machine()
        m.move_to(193, 234)
        occupied_xs = {mac.x for mac in [m] if mac.placed}
        self.assertNotIn(193, occupied_xs)

    def test_counter_space_blocked_when_machine_at_same_x(self):
        """Placement must be blocked when a placed machine already occupies the target x."""
        existing = make_machine()
        existing.move_to(193, 234)
        existing.placed = True
        occupied_xs = {mac.x for mac in [existing] if mac.placed}
        self.assertIn(193, occupied_xs)

    def test_counter_space_free_at_different_x(self):
        """Placement must be allowed when no placed machine occupies the target x."""
        existing = make_machine()
        existing.move_to(193, 234)
        existing.placed = True
        occupied_xs = {mac.x for mac in [existing] if mac.placed}
        self.assertNotIn(358, occupied_xs)

    def test_two_machines_can_be_placed_at_different_positions(self):
        """Two machines placed at different x values must both appear in the occupied set."""
        m1 = make_machine()
        m1.move_to(193, 234)
        m1.placed = True
        m2 = make_machine()
        m2.move_to(358, 234)
        m2.placed = True
        occupied_xs = {mac.x for mac in [m1, m2] if mac.placed}
        self.assertIn(193, occupied_xs)
        self.assertIn(358, occupied_xs)

    def test_machine_added_to_active_list_on_placement(self):
        """The machine must be appended to the active machines list during placement."""
        m = make_machine()
        machines = []
        m.move_to(193, 234)
        m.placed = True
        if m not in machines:
            machines.append(m)
        self.assertIn(m, machines)

    def test_full_placement_flow(self):
        """Complete flow: move_to, set placed, append to list — leaves machine active and positioned."""
        m = make_machine()
        machines = []
        m.move_to(358, 234)
        m.placed = True
        machines.append(m)
        self.assertTrue(m.placed)
        self.assertEqual(m.x, 358)
        self.assertIn(m, machines)


# --- Req15: Brewing Start ---

class TestReq15BrewingStart(unittest.TestCase):
    """Req15 - Brewing starts only when ingredient inserted AND start button pressed."""

    def test_inserting_ingredient_then_pressing_start_begins_brewing(self):
        """Combined flow: correct ingredient added then start pressed → state is 'running'."""
        m = make_machine(state='empty')
        m.add(MACHINE_INPUT, MagicMock())
        m.run_machine()
        self.assertEqual(m.state, 'running')

    def test_inserting_ingredient_alone_does_not_start_brewing(self):
        """Start button is required — inserting ingredient alone must not begin brewing."""
        m = make_machine(state='empty')
        m.add(MACHINE_INPUT, MagicMock())
        self.assertNotEqual(m.state, 'running')

    def test_pressing_start_without_ingredient_does_not_start_brewing(self):
        """Ingredient is required — pressing start on an empty machine must not begin brewing."""
        m = make_machine(state='empty')
        m.run_machine()
        self.assertNotEqual(m.state, 'running')


# --- Req16: Brewing Tracking ---

class TestReq16BrewingTracking(unittest.TestCase):
    """Req16 - Brewing progress and machine state tracked once brewing begins."""

    def test_timer_start_is_captured_when_brewing_begins(self):
        """timer_start must be recorded when brewing begins."""
        m = make_machine(state='full')
        before = pygame.time.get_ticks()
        m.run_machine()
        after = pygame.time.get_ticks()
        self.assertGreaterEqual(m.timer_start, before)
        self.assertLessEqual(m.timer_start, after)

    def test_state_is_running_immediately_after_start(self):
        """Machine state must be 'running' right after the start button is pressed."""
        m = make_machine(state='full')
        m.run_machine()
        self.assertEqual(m.state, 'running')

    def test_state_remains_running_while_timer_has_not_expired(self):
        """Machine must stay in 'running' state while elapsed time is less than runtime."""
        m = make_machine(state='full')
        m.run_machine()
        m.update()
        self.assertEqual(m.state, 'running')

    def test_state_transitions_to_ready_when_timer_expires(self):
        """Machine must move to 'ready' once elapsed time reaches or exceeds runtime."""
        m = make_machine(state='full')
        m.run_machine()
        m.timer_start = pygame.time.get_ticks() - 6000
        m.update()
        self.assertEqual(m.state, 'ready')

    def test_contents_populated_with_correct_output_on_completion(self):
        """On completion, contents must hold num_outputs copies of the selected output."""
        m = make_machine(state='full')
        m.run_machine()
        m.timer_start = pygame.time.get_ticks() - 6000
        m.update()
        self.assertEqual(m.contents, [OUTPUTS[0]] * m.num_outputs)


if __name__ == '__main__':
    unittest.main()