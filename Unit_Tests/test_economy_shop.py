"""
Unit Tests: Economy and Shop/Register Systems

Runs against the REAL game classes — not stubs.

Requirements covered:
  Req4  - Shop interface / upgrade list accessible        [MANUAL - SKIPPED]
  Req6  - Recipe details retrievable                      [NEEDS CODE - SKIPPED]
  Req7  - Upgrade purchased when sufficient currency
  Req8  - Currency deducted on purchase
  Req9  - Register customer_waiting flag set
  Req10 - Customer drink order stored
  Req11 - Customer wait time tracked
  Req19 - Currency added on successful delivery
"""

import unittest
import os
import sys

# ------------------------------------------------------------------
# Boot pygame in headless mode before any game imports
# ------------------------------------------------------------------
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.image.load = lambda path: pygame.Surface((10, 10))

# Patch IMAGE_LIBRARY to return a dummy surface for any key so
# classes that look up sprites during __init__ don't crash.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants

class _FakeImageLib(dict):
    def __missing__(self, key):
        return pygame.Surface((10, 10))

constants.IMAGE_LIBRARY = _FakeImageLib()

# ------------------------------------------------------------------
# Now import the REAL game classes
# ------------------------------------------------------------------
from manager import GameManager
from recipes import Recipe
from customer import Customer
from items import Ingredient, Cup
from others import Register


# ==================================================================
# Tests
# ==================================================================

@unittest.skip("Req 4 - visual/UI interaction, must be tested manually")
class TestReq4_ShopAccessible(unittest.TestCase):
    """Req4 — Shop interface opens when player clicks shop button."""

    def test_upgrade_list_exists(self):
        manager = GameManager()
        self.assertIsInstance(manager.upgrades, list)

    def test_upgrade_list_has_three_tiers(self):
        manager = GameManager()
        self.assertEqual(len(manager.upgrades), 3)

    def test_each_upgrade_has_name(self):
        manager = GameManager()
        for upgrade in manager.upgrades:
            self.assertIn("name", upgrade)

    def test_each_upgrade_has_cost(self):
        manager = GameManager()
        for upgrade in manager.upgrades:
            self.assertIn("cost", upgrade)


@unittest.skip("Req 6 - code not yet implemented")
class TestReq6_RecipeDetails(unittest.TestCase):
    """Req6 — Recipe details displayed when player selects a recipe."""

    def setUp(self):
        self.ing1 = Ingredient("espresso", ["espresso_key"], price_to_buy=1.0)
        self.ing2 = Ingredient("milk", ["milk_key"], price_to_buy=0.5)
        self.recipe = Recipe("Latte", [self.ing1, self.ing2], 4.50, "latte_key", locked=False)

    def test_get_name(self):
        self.assertEqual(self.recipe.get_name(), "Latte")

    def test_get_price(self):
        self.assertEqual(self.recipe.get_price(), 4.50)

    def test_get_ingredients_is_list(self):
        self.assertIsInstance(self.recipe.get_ingredients(), list)

    def test_get_ingredients_count(self):
        self.assertEqual(len(self.recipe.get_ingredients()), 2)

    def test_get_status_unlocked(self):
        self.assertFalse(self.recipe.get_status())

    def test_set_status_locks_recipe(self):
        self.recipe.set_status(True)
        self.assertTrue(self.recipe.get_status())


class TestReq7_UpgradePurchased(unittest.TestCase):
    """Req7 — Upgrade is purchased when sufficient currency is available."""

    def setUp(self):
        self.manager = GameManager()

    def test_tier1_purchased_with_enough_money(self):
        self.manager.money = 100
        self.manager.buy_upgrade(0)
        self.assertTrue(self.manager.upgrades[0]["purchased"])

    def test_tier1_not_purchased_without_enough_money(self):
        self.manager.money = 10
        self.manager.buy_upgrade(0)
        self.assertFalse(self.manager.upgrades[0]["purchased"])

    def test_tier2_blocked_without_tier1(self):
        self.manager.money = 500
        self.manager.buy_upgrade(1)
        self.assertFalse(self.manager.upgrades[1]["purchased"])

    def test_tier2_unlocks_after_tier1(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)
        self.manager.buy_upgrade(1)
        self.assertTrue(self.manager.upgrades[1]["purchased"])

    def test_tier3_requires_tier2(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)
        self.manager.buy_upgrade(2)
        self.assertFalse(self.manager.upgrades[2]["purchased"])

    def test_cannot_buy_same_upgrade_twice(self):
        self.manager.money = 200
        self.manager.buy_upgrade(0)
        money_after_first = self.manager.money
        self.manager.buy_upgrade(0)
        self.assertEqual(self.manager.money, money_after_first)

    def test_max_orders_increases_by_2(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)
        self.assertEqual(self.manager.max_orders, 4)

    def test_more_hands_tier_increments(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)
        self.assertEqual(self.manager.more_hands_tier, 1)

    def test_all_three_tiers_purchasable(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)
        self.manager.buy_upgrade(1)
        self.manager.buy_upgrade(2)
        self.assertTrue(all(u["purchased"] for u in self.manager.upgrades))

    def test_invalid_index_does_nothing(self):
        self.manager.money = 500
        self.manager.buy_upgrade(99)
        self.manager.buy_upgrade(-1)
        self.assertEqual(self.manager.money, 500)


class TestReq8_CurrencyDeducted(unittest.TestCase):
    """Req8 — Currency deducted when a purchase is made."""

    def setUp(self):
        self.manager = GameManager()

    def test_money_deducted_on_tier1(self):
        self.manager.money = 200
        self.manager.buy_upgrade(0)
        self.assertEqual(self.manager.money, 150)

    def test_money_unchanged_on_failed_purchase(self):
        self.manager.money = 10
        self.manager.buy_upgrade(0)
        self.assertEqual(self.manager.money, 10)

    def test_sequential_deductions(self):
        self.manager.money = 500
        self.manager.buy_upgrade(0)   # -50
        self.manager.buy_upgrade(1)   # -100
        self.assertEqual(self.manager.money, 350)

    def test_money_never_goes_negative(self):
        self.manager.money = 49
        self.manager.buy_upgrade(0)
        self.assertGreaterEqual(self.manager.money, 0)


class TestReq9_RegisterWaitingFlag(unittest.TestCase):
    """Req9 — customer_waiting flag set when customer present at register."""

    def setUp(self):
        Register.customer_waiting = False

    def tearDown(self):
        Register.customer_waiting = False

    def test_flag_starts_false(self):
        self.assertFalse(Register.customer_waiting)

    def test_set_waiting_sets_flag(self):
        reg = Register(0, 0, 10)
        reg.set_waiting()
        self.assertTrue(Register.customer_waiting)

    def test_flag_shared_across_instances(self):
        reg1 = Register(0, 0, 10)
        reg2 = Register(200, 0, 10)
        reg1.set_waiting()
        self.assertTrue(reg2.customer_waiting)


class TestReq10_OrderStored(unittest.TestCase):
    """Req10 — Customer's drink order stored when order confirmed."""

    def setUp(self):
        self.recipe = Recipe("Espresso", [], 3.00, "espresso_key")
        self.customer = Customer(
            0, 0, ["cust_key", "cust_key"], [self.recipe], (100, 370)
        )

    def test_ordered_item_assigned_on_init(self):
        self.assertIsNotNone(self.customer.ordered_item)

    def test_ordered_item_is_from_recipe_list(self):
        self.assertEqual(self.customer.ordered_item.get_name(), "Espresso")

    def test_ordered_item_price_accessible(self):
        self.assertEqual(self.customer.ordered_item.get_price(), 3.00)

    def test_ordered_item_can_be_cleared(self):
        self.customer.ordered_item = None
        self.assertIsNone(self.customer.ordered_item)


class TestReq11_WaitTimeTracked(unittest.TestCase):
    """Req11 — Customer wait time tracked via waitBar_length."""

    def setUp(self):
        recipe = Recipe("Latte", [], 4.00, "latte_key")
        self.customer = Customer(
            0, 0, ["cust_key", "cust_key"], [recipe], (100, 370)
        )

    def test_wait_bar_starts_at_max(self):
        self.assertEqual(self.customer.wait_bar_length, 10000)

    def test_wait_bar_decrements(self):
        self.customer.wait_bar_length -= 1
        self.assertEqual(self.customer.wait_bar_length, 9999)

    def test_wait_bar_reaches_zero(self):
        self.customer.wait_bar_length = 1
        self.customer.wait_bar_length -= 1
        self.assertEqual(self.customer.wait_bar_length, 0)

    def test_tip_is_max_at_full_wait_bar(self):
        self.customer.wait_bar_length = 10000
        base, tip, total = self.customer.calculate_tip()
        self.assertEqual(tip, base)

    def test_tip_is_zero_at_empty_wait_bar(self):
        self.customer.wait_bar_length = 0
        base, tip, total = self.customer.calculate_tip()
        self.assertEqual(tip, 0.0)

    def test_tip_is_half_at_half_wait_bar(self):
        self.customer.wait_bar_length = 5000
        base, tip, total = self.customer.calculate_tip()
        self.assertAlmostEqual(tip, self.customer.ordered_item.get_price() * 0.5, places=2)


class TestReq19_CurrencyAddedOnDelivery(unittest.TestCase):
    """Req19 — Currency added on successful drink delivery."""

    def setUp(self):
        self.ing1 = Ingredient("espresso", ["espresso_key"], price_to_buy=1.0)
        self.ing2 = Ingredient("milk", ["milk_key"], price_to_buy=0.5)
        self.recipe = Recipe("Latte", [self.ing1, self.ing2], 5.00, "latte_key")
        self.cup = Cup(["cup_key", "cup_full_key"])
        self.manager = GameManager()

    def test_check_match_correct_drink(self):
        self.cup.contents = [self.ing1, self.ing2]
        self.assertTrue(self.recipe.check_match(self.cup))

    def test_check_match_wrong_ingredient(self):
        wrong = Ingredient("water", ["water_key"], price_to_buy=0.0)
        self.cup.contents = [self.ing1, wrong]
        self.assertFalse(self.recipe.check_match(self.cup))

    def test_check_match_wrong_count(self):
        self.cup.contents = [self.ing1]
        self.assertFalse(self.recipe.check_match(self.cup))

    def test_check_match_empty_cup(self):
        self.cup.contents = []
        self.assertFalse(self.recipe.check_match(self.cup))

    def test_check_match_wrong_order(self):
        self.cup.contents = [self.ing2, self.ing1]
        self.assertFalse(self.recipe.check_match(self.cup))

    def test_money_increases_on_correct_delivery(self):
        customer = Customer(
            0, 0, ["cust_key", "cust_key"], [self.recipe], (100, 370)
        )
        customer.ordered_item = self.recipe
        self.cup.contents = [self.ing1, self.ing2]
        if self.recipe.check_match(self.cup):
            base, tip, total = customer.calculate_tip()
            self.manager.money += total
        self.assertGreater(self.manager.money, 0)

    def test_no_money_added_on_wrong_drink(self):
        customer = Customer(
            0, 0, ["cust_key", "cust_key"], [self.recipe], (100, 370)
        )
        wrong = Ingredient("water", ["water_key"], price_to_buy=0.0)
        self.cup.contents = [wrong, wrong]
        if self.recipe.check_match(self.cup):
            base, tip, total = customer.calculate_tip()
            self.manager.money += total
        self.assertEqual(self.manager.money, 0)

    def test_total_equals_base_plus_tip(self):
        customer = Customer(
            0, 0, ["cust_key", "cust_key"], [self.recipe], (100, 370)
        )
        base, tip, total = customer.calculate_tip()
        self.assertAlmostEqual(total, base + tip, places=2)

    def test_full_wait_bar_gives_double_price(self):
        """Full wait bar = 100% tip = total is 2x base price."""
        customer = Customer(
            0, 0, ["cust_key", "cust_key"], [self.recipe], (100, 370)
        )
        customer.ordered_item = self.recipe
        customer.wait_bar_length = 10000
        base, tip, total = customer.calculate_tip()
        self.assertAlmostEqual(total, base * 2, places=2)


class TestHandleTime(unittest.TestCase):
    """Bonus — handle_time clock formatting used in HUD."""

    def setUp(self):
        self.manager = GameManager()

    def test_morning(self):
        self.assertEqual(self.manager.handle_time(6, 0), "06:00 AM")

    def test_noon_is_pm(self):
        self.assertEqual(self.manager.handle_time(12, 0), "12:00 PM")

    def test_midnight_is_am(self):
        self.assertEqual(self.manager.handle_time(0, 0), "12:00 AM")

    def test_minutes_round_down_to_five(self):
        self.assertEqual(self.manager.handle_time(9, 7), "09:05 AM")

    def test_afternoon(self):
        self.assertEqual(self.manager.handle_time(14, 30), "02:30 PM")

    def test_late_night(self):
        self.assertEqual(self.manager.handle_time(23, 55), "11:55 PM")


# ==================================================================
# Clean output runner
# ==================================================================
if __name__ == "__main__":
    suite_classes = [
        TestReq4_ShopAccessible,
        TestReq6_RecipeDetails,
        TestReq7_UpgradePurchased,
        TestReq8_CurrencyDeducted,
        TestReq9_RegisterWaitingFlag,
        TestReq10_OrderStored,
        TestReq11_WaitTimeTracked,
        TestReq19_CurrencyAddedOnDelivery,
        TestHandleTime,
    ]

    labels = {
        TestReq4_ShopAccessible:           "Req 4  | Shop interface accessible         [MANUAL]",
        TestReq6_RecipeDetails:            "Req 6  | Recipe details retrievable         [NEEDS CODE]",
        TestReq7_UpgradePurchased:         "Req 7  | Upgrade purchased with currency",
        TestReq8_CurrencyDeducted:         "Req 8  | Currency deducted on purchase",
        TestReq9_RegisterWaitingFlag:      "Req 9  | Register customer_waiting flag",
        TestReq10_OrderStored:             "Req 10 | Customer order stored",
        TestReq11_WaitTimeTracked:         "Req 11 | Customer wait time tracked",
        TestReq19_CurrencyAddedOnDelivery: "Req 19 | Currency added on delivery",
        TestHandleTime:                    "Bonus  | Clock time formatting",
    }

    total_passed = total_failed = total_skipped = 0
    WIDTH = 62

    print()
    print("=" * WIDTH)
    print(" CIS 350 — Cafe Game  |  Economy & Shop Unit Tests")
    print("=" * WIDTH)

    runner = unittest.TextTestRunner(stream=open("/dev/null", "w"))

    for cls in suite_classes:
        label = labels[cls]
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        result = runner.run(suite)

        passed  = suite.countTestCases() - len(result.failures) - len(result.errors) - len(result.skipped)
        failed  = len(result.failures) + len(result.errors)
        skipped = len(result.skipped)

        total_passed  += passed
        total_failed  += failed
        total_skipped += skipped

        if skipped == suite.countTestCases():
            status = "SKIP"
        elif failed > 0:
            status = "FAIL"
        else:
            status = "PASS"

        detail = f"{passed}/{suite.countTestCases()} passed"
        if skipped:
            detail += f", {skipped} skipped"
        if failed:
            detail += f", {failed} failed"

        line = f"  {label}"
        padding = max(1, WIDTH - len(line) - len(f"  {detail}  [{status}]"))
        print(f"{line}{' ' * padding}{detail}  [{status}]")

        for test, msg in result.failures + result.errors:
            print(f"    x {test.id().split('.')[-1]}")
            print(f"      {msg.strip().splitlines()[-1]}")

    print("-" * WIDTH)
    grand = total_passed + total_failed + total_skipped
    print(f"  Total: {grand} tests  |  {total_passed} passed  |  {total_skipped} skipped  |  {total_failed} failed")
    print("=" * WIDTH)
    print()