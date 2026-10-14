"""Warehouse maintenance system module."""

import logging
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


class MaintenanceManager:
    """Manages maintenance inventory and asset levels."""

    def __init__(self) -> None:
        """Initialize the manager with an empty inventory dictionary."""
        self.inventory: Dict[str, Dict[str, Any]] = {}

    def add_item(
        self, item_name: str, quantity: int, tags: Optional[List[str]] = None
    ) -> bool:
        """Add an item with a specified quantity and optional tags."""
        if tags is None:
            tags = []

        if not isinstance(item_name, str) or not item_name.strip():
            LOGGER.error("Invalid item name provided.")
            return False

        if quantity < 0:
            LOGGER.error("Quantity cannot be negative for item: %s", item_name)
            return False

        if item_name in self.inventory:
            self.inventory[item_name]["quantity"] += quantity
            for tag in tags:
                if tag not in self.inventory[item_name]["tags"]:
                    self.inventory[item_name]["tags"].append(tag)
        else:
            self.inventory[item_name] = {"quantity": quantity, "tags": tags}

        LOGGER.info("Successfully added %d of %s", quantity, item_name)
        return True

    def get_stock(self, item_name: str) -> int:
        """Retrieve the stock quantity of a specific maintenance item."""
        try:
            item_data = self.inventory.get(item_name)
            if item_data and isinstance(item_data, dict):
                return int(item_data.get("quantity", 0))
            return 0
        except (KeyError, TypeError, ValueError) as err:
            LOGGER.error("Error retrieving stock for %s: %s", item_name, err)
            return 0


def main() -> None:
    """Run the main application demonstration."""
    manager = MaintenanceManager()
    manager.add_item("Widgets", 50, ["electronics", "fragile"])
    manager.add_item("Gadgets", 120, ["hardware"])

    LOGGER.info("Widget stock: %d", manager.get_stock("Widgets"))
    LOGGER.info("Gadget stock: %d", manager.get_stock("Gadgets"))


if __name__ == "__main__":
    main()
