"""
Unit Tests: Machine System

Runs against the REAL Machine class — pygame is mocked so no display is required.

Requirements covered:
  Req14 - Machine placed when purchased and counter space available     [NEEDS CODE - SKIPPED]
  Req15 - Brewing starts when ingredient inserted and start pressed
  Req16 - Brewing progress and machine state tracked during brewing
  Req17 - Output added to cup contents when collected from machine      [PARTIAL - remove_output only]
"""

import unittest
from unittest.mock import MagicMock
import sys

# Mock pygame before importing anything that depends on it
mock_pygame = MagicMock()
mock_pygame.sprite.Sprite = object  # must be a real type so class bodies can inherit from it
sys.modules['pygame'] = mock_pygame

# Populate IMAGE_LIBRARY with test keys before importing machines
import constants
constants.IMAGE_LIBRARY.update({
    'empty_key':   MagicMock(),
    'running_key': MagicMock(),
    'ready_key':   MagicMock(),
})

from machines import Machine


MINI_GAME_KEYS    = ['empty_key', 'running_key', 'ready_key']
START_BUTTON_INFO = [400, 400, 100, 50]
MACHINE_INPUT     = 'coffee_beans'
OUTPUTS           = ['espresso', 'lungo']


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
        start_button_info=START_BUTTON_INFO,
    )
    m.state = state
    return m


class TestMachineInitialState(unittest.TestCase):
    """Verify that a newly constructed Machine starts with the correct default values."""

    def test_initial_state_is_empty(self):
        """A new machine should begin in the 'empty' state before any ingredient is added."""
        m = make_machine()
        self.assertEqual(m.state, 'empty')

    def test_initial_contents_is_empty(self):
        """Contents list should be empty on construction — no outputs exist yet."""
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
        """The machine must store the brewing duration (in seconds) for timer calculations."""
        m = make_machine()
        self.assertEqual(m.runtime, 5)


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
        player.popInventoryItem.assert_called_once()

    def test_wrong_ingredient_does_not_pop_inventory(self):
        """A failed add must not remove anything from the player's inventory."""
        m = make_machine()
        player = MagicMock()
        m.add('milk', player)
        player.popInventoryItem.assert_not_called()


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
        mock_pygame.time.get_ticks.return_value = 1000
        m.run_machine()
        self.assertEqual(m.state, 'running')

    def test_run_machine_sets_selected_output(self):
        """Pressing start must choose and record which output will be produced."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 1000
        m.run_machine()
        self.assertEqual(m.selected_output, OUTPUTS[0])


class TestMachineUpdate(unittest.TestCase):
    """Tests for Machine.update() — the per-frame timer check during brewing."""

    def test_update_transitions_to_ready_when_timer_expires(self):
        """Once elapsed time exceeds runtime, state must become 'ready'."""
        m = make_machine(state='running')
        m.selected_output = 'espresso'
        m.timer_start = 0
        mock_pygame.time.get_ticks.return_value = 6000  # 6s > 5s runtime
        m.update()
        self.assertEqual(m.state, 'ready')

    def test_update_does_not_transition_before_timer_expires(self):
        """State must remain 'running' while elapsed time is still under the runtime."""
        m = make_machine(state='running')
        m.timer_start = 0
        mock_pygame.time.get_ticks.return_value = 3000  # 3s < 5s runtime
        m.update()
        self.assertEqual(m.state, 'running')

    def test_update_populates_contents_on_completion(self):
        """On completion, contents must be filled with num_outputs copies of the selected output."""
        m = make_machine(state='running')
        m.selected_output = 'espresso'
        m.timer_start = 0
        m.num_outputs = 2
        mock_pygame.time.get_ticks.return_value = 6000
        m.update()
        self.assertEqual(m.contents, ['espresso', 'espresso'])

    def test_update_does_nothing_when_not_running(self):
        """update() must be a no-op when the machine is not in the 'running' state."""
        m = make_machine(state='empty')
        m.update()
        self.assertEqual(m.state, 'empty')


class TestMachineSelectOutput(unittest.TestCase):
    """Tests for Machine.select_output() — choosing which item will be produced."""

    def test_select_output_returns_first_output(self):
        """select_output must return the first item from the outputs list."""
        m = make_machine()
        result = m.select_output(0)
        self.assertEqual(result, OUTPUTS[0])

    def test_select_output_ignores_index_always_returns_first(self):
        """The index argument is currently unused — any index returns the first output."""
        m = make_machine()
        self.assertEqual(m.select_output(0), m.select_output(1))


class TestMachineRemoveOutput(unittest.TestCase):
    """Tests for Machine.remove_output() — collecting a finished item from the machine."""

    def test_remove_output_returns_item_when_ready(self):
        """A ready machine with contents must return one of those items."""
        m = make_machine(state='ready')
        m.contents = ['espresso', 'espresso']
        result = m.remove_output()
        self.assertEqual(result, 'espresso')

    def test_remove_output_decreases_contents(self):
        """Each collection must remove exactly one item from contents."""
        m = make_machine(state='ready')
        m.contents = ['espresso', 'espresso']
        m.remove_output()
        self.assertEqual(len(m.contents), 1)

    def test_remove_output_returns_none_when_not_ready(self):
        """Collecting from a non-ready machine must return None."""
        m = make_machine(state='full')
        result = m.remove_output()
        self.assertIsNone(result)

    def test_remove_output_returns_none_when_empty_state(self):
        """Collecting from an empty machine must return None."""
        m = make_machine(state='empty')
        result = m.remove_output()
        self.assertIsNone(result)

    def test_remove_output_returns_none_when_contents_empty(self):
        """Collecting from a ready machine with no contents must return None."""
        m = make_machine(state='ready')
        m.contents = []
        result = m.remove_output()
        self.assertIsNone(result)


class TestMachineGetSprite(unittest.TestCase):
    """Tests for Machine.get_sprite() — selecting the correct visual based on state."""

    def test_get_sprite_uses_empty_key_when_empty(self):
        """An empty machine must use the first sprite key (empty state image)."""
        m = make_machine(state='empty')
        m.get_sprite()
        self.assertEqual(m.sprite, 'empty_key')

    def test_get_sprite_uses_running_key_when_running(self):
        """A running machine must use the second sprite key (in-progress image)."""
        m = make_machine(state='running')
        m.get_sprite()
        self.assertEqual(m.sprite, 'running_key')

    def test_get_sprite_uses_ready_key_when_ready(self):
        """A ready machine must use the third sprite key (done image)."""
        m = make_machine(state='ready')
        m.get_sprite()
        self.assertEqual(m.sprite, 'ready_key')

    def test_get_sprite_uses_empty_key_when_full(self):
        """A full (loaded but not started) machine must use the empty sprite key."""
        m = make_machine(state='full')
        m.get_sprite()
        self.assertEqual(m.sprite, 'empty_key')


class TestMachineIsPlayerNearby(unittest.TestCase):
    """Tests for Machine.is_player_nearby() — proximity detection for interaction."""

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


class TestMachineSetupMinigame(unittest.TestCase):
    """Tests for Machine.setup_minigame() — preparing the ingredient for the minigame UI."""

    def test_sets_ingredient_from_list(self):
        """The last item in the list must be assigned as the machine's active ingredient."""
        m = make_machine()
        ingredient = MagicMock()
        m.setup_minigame([ingredient])
        self.assertEqual(m.ingredient, ingredient)

    def test_sets_none_when_list_is_empty(self):
        """An empty list must result in ingredient being set to None."""
        m = make_machine()
        m.setup_minigame([])
        self.assertIsNone(m.ingredient)

    def test_sets_ingredient_position(self):
        """The ingredient must be repositioned to the fixed minigame display coordinates."""
        m = make_machine()
        ingredient = MagicMock()
        m.setup_minigame([ingredient])
        self.assertEqual(ingredient.x, 20)
        self.assertEqual(ingredient.y, 500)

    def test_does_not_modify_original_list(self):
        """setup_minigame must work on a copy and leave the caller's list intact."""
        m = make_machine()
        ingredient = MagicMock()
        original = [ingredient]
        m.setup_minigame(original)
        self.assertEqual(len(original), 1)


# ---------------------------------------------------------------------------
# Req15 – Brewing starts when ingredient inserted AND start button pressed
# ---------------------------------------------------------------------------

class TestReq15BrewingStart(unittest.TestCase):
    """
    Covers Req15: the system shall start brewing only when BOTH conditions are met —
    the correct ingredient has been inserted AND the start button has been pressed.
    """

    def test_inserting_ingredient_then_pressing_start_begins_brewing(self):
        """Combined flow: correct ingredient added then start pressed → state is 'running'."""
        m = make_machine(state='empty')
        player = MagicMock()
        mock_pygame.time.get_ticks.return_value = 1000

        m.add(MACHINE_INPUT, player)  # player inserts ingredient
        m.run_machine()               # player presses start button

        self.assertEqual(m.state, 'running')

    def test_inserting_ingredient_alone_does_not_start_brewing(self):
        """Start button is required — inserting ingredient alone must not begin brewing."""
        m = make_machine(state='empty')
        player = MagicMock()

        m.add(MACHINE_INPUT, player)  # ingredient inserted, start NOT pressed

        self.assertNotEqual(m.state, 'running')

    def test_pressing_start_without_ingredient_does_not_start_brewing(self):
        """Ingredient is required — pressing start on an empty machine must not begin brewing."""
        m = make_machine(state='empty')

        m.run_machine()  # start pressed, ingredient NOT inserted

        self.assertNotEqual(m.state, 'running')


# ---------------------------------------------------------------------------
# Req16 – Brewing progress and machine state are tracked once brewing begins
# ---------------------------------------------------------------------------

class TestReq16BrewingTracking(unittest.TestCase):
    """
    Covers Req16: once brewing begins the system must record a timer start point,
    maintain 'running' state throughout, and transition to 'ready' with correct
    contents when the runtime elapses.
    """

    def test_timer_start_is_captured_when_brewing_begins(self):
        """timer_start must be set to the current tick so elapsed time can be calculated."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 3000

        m.run_machine()

        self.assertEqual(m.timer_start, 3000)

    def test_state_is_running_immediately_after_start(self):
        """Machine state must be 'running' right after the start button is pressed."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 1000

        m.run_machine()

        self.assertEqual(m.state, 'running')

    def test_state_remains_running_while_timer_has_not_expired(self):
        """Machine must stay in 'running' state while elapsed time is less than runtime."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 1000
        m.run_machine()

        mock_pygame.time.get_ticks.return_value = 3000  # 2s elapsed < 5s runtime
        m.update()

        self.assertEqual(m.state, 'running')

    def test_state_transitions_to_ready_when_timer_expires(self):
        """Machine must move to 'ready' once elapsed time reaches or exceeds runtime."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 1000
        m.run_machine()

        mock_pygame.time.get_ticks.return_value = 7000  # 6s elapsed > 5s runtime
        m.selected_output = OUTPUTS[0]
        m.update()

        self.assertEqual(m.state, 'ready')

    def test_contents_populated_with_correct_output_on_completion(self):
        """On completion, contents must hold num_outputs copies of the selected output."""
        m = make_machine(state='full')
        mock_pygame.time.get_ticks.return_value = 1000
        m.run_machine()

        mock_pygame.time.get_ticks.return_value = 7000
        m.update()

        self.assertEqual(m.contents, [OUTPUTS[0]] * m.num_outputs)


if __name__ == '__main__':
    unittest.main()
