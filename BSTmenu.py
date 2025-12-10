from BST import BinarySearchTree
from typing import List, Optional

class MenuItem:
    def __init__(self, name: str, price: int, category: str, popularity: int = 0):
        self.name = name
        self.price = price
        self.category = category
        self.popularity = popularity

    def __repr__(self):
        return f"{self.name} (₱{self.price} | ⭐{self.popularity})"

    def __str__(self):
        return self.name

class ComparableItem:
    def __init__(self, item: MenuItem, mode: str = "price", idx: int = 0):
        self.item = item
        self.mode = mode
        self.idx = idx

    def key(self):
        if self.mode == "price":
            return (self.item.price, self.item.name.lower(), self.idx)
        if self.mode == "name":
            return (self.item.name.lower(), self.item.price, self.idx)
        if self.mode == "popularity":
            return (-self.item.popularity, self.item.name.lower(), self.idx)
        return (self.item.price, self.item.name.lower(), self.idx)

    def __lt__(self, other):
        if not isinstance(other, ComparableItem):
            return NotImplemented
        return self.key() < other.key()

    def __gt__(self, other):
        if not isinstance(other, ComparableItem):
            return NotImplemented
        return self.key() > other.key()

    def __eq__(self, other):
        if not isinstance(other, ComparableItem):
            return NotImplemented
        return self.key() == other.key()

    def __str__(self):
        return self.item.name.replace(" ", "_")

    def __repr__(self):
        return f"{self.item.name}({self.mode})"

# ----- MENU_DATA -----
MENU_DATA = {
    "Brewed Coffee": {"price": 80, "category": "Drinks", "popularity": 4},
    "Iced Coffee": {"price": 125, "category": "Drinks", "popularity": 4},
    "Milk Tea (Bubble Tea)": {"price": 110, "category": "Drinks", "popularity": 5},
    "Fresh Lemonade": {"price": 65, "category": "Drinks", "popularity": 3},
    "Fruit Shake (Banana)": {"price": 125, "category": "Drinks", "popularity": 4},
    "Canned Soda / Bottled Water": {"price": 50, "category": "Drinks", "popularity": 3},
    "French Fries": {"price": 70, "category": "Street Food", "popularity": 4},
    "Siomai (Steamed)": {"price": 40, "category": "Street Food", "popularity": 4},
    "Kwek-Kwek": {"price": 18, "category": "Street Food", "popularity": 3},
    "Fish Balls / Kikiam": {"price": 40, "category": "Street Food", "popularity": 4},
    "Pork BBQ Stick": {"price": 32, "category": "Street Food", "popularity": 4},
    "Grilled Hotdog": {"price": 30, "category": "Street Food", "popularity": 3},
    "Turon": {"price": 28, "category": "Street Food", "popularity": 3},
    "Tapsilog": {"price": 140, "category": "Simple Meals", "popularity": 5},
    "Lugaw / Congee (with toppings)": {"price": 70, "category": "Simple Meals", "popularity": 3},
    "Pasta (Simple sauce)": {"price": 185, "category": "Simple Meals", "popularity": 4},
    "Grilled Cheese Sandwich": {"price": 125, "category": "Simple Meals", "popularity": 4},
    "Basic Burger": {"price": 125, "category": "Simple Meals", "popularity": 4},
    "Pancit Canton (Stir-fry)": {"price": 100, "category": "Simple Meals", "popularity": 4},
    "Chocolate Chip Cookie": {"price": 55, "category": "Baked Goods", "popularity": 4},
    "Brownie Square": {"price": 65, "category": "Baked Goods", "popularity": 4},
    "Cheese Pandesal": {"price": 20, "category": "Baked Goods", "popularity": 3},
    "Banana Cue": {"price": 28, "category": "Baked Goods", "popularity": 3},
    "Leche Flan (Small)": {"price": 80, "category": "Baked Goods", "popularity": 4},
    "Halo-Halo (Basic)": {"price": 105, "category": "Baked Goods", "popularity": 5},
}

class BSTMenuManager:
    def __init__(self):
        self.items: List[MenuItem] = []
        for name, d in MENU_DATA.items():
            self.items.append(MenuItem(name, d["price"], d["category"], d.get("popularity", 0)))

    def get_menu_data(self):
        return MENU_DATA

    def get_categories(self) -> List[str]:
        return sorted(set(it.category for it in self.items))

    def _key_fn(self, mode: str):
        if mode == "price":
            return lambda it: (it.price, it.name.lower())
        if mode == "name":
            return lambda it: it.name.lower()
        if mode == "popularity":
            return lambda it: (-it.popularity, it.name.lower())
        return lambda it: (it.price, it.name.lower())

    def build_tree_for_category(self, category: str, sort_by: str = "price", root_strategy: str = "oldest"):
        items = [it for it in self.items if it.category == category]
        tree = BinarySearchTree()
        if not items:
            return tree, []

        keyfn = self._key_fn(sort_by)

        # Choose root
        if root_strategy == "median":
            # pick median from sorted list
            sorted_items = sorted(items, key=(keyfn if sort_by != "name" else (lambda x: x.name.lower())))
            mid = len(sorted_items) // 2
            root_item = sorted_items[mid]
        else:
            # oldest (in insertion order)
            root_item = items[0]

        # Create root node
        tree.root = tree.insert(tree.root, ComparableItem(root_item, mode=sort_by, idx=0))

        # Insert remaining items in insertion order (oldest -> newest)
        for idx, it in enumerate(items):
            if it.name == root_item.name:
                continue
            ci = ComparableItem(it, mode=sort_by, idx=idx+1)
            tree.root = tree.insert(tree.root, ci)

        # For display: show insertion order (oldest -> newest)
        display_insertion_order = items[:]
        return tree, display_insertion_order

    # Wrappers for BST functions
    def inorder(self, tree: BinarySearchTree):
        s = tree.inorder_traversal(tree.root, "")
        return [t.replace("_", " ") for t in s.split()] if s else []

    def preorder(self, tree: BinarySearchTree):
        s = tree.preorder_traversal(tree.root, "")
        return [t.replace("_", " ") for t in s.split()] if s else []

    def postorder(self, tree: BinarySearchTree):
        s = tree.postorder_traversal(tree.root, "")
        return [t.replace("_", " ") for t in s.split()] if s else []

    def search_by_name(self, tree: BinarySearchTree, name: str) -> Optional[MenuItem]:
        def _search(n):
            if n is None:
                return None
            left = _search(n.left)
            if left:
                return left
            try:
                if n.value.item.name.lower() == name.lower():
                    return n.value
            except Exception:
                pass
            return _search(n.right)
        found = _search(tree.root)
        return found.item if found else None

    def delete_by_name(self, tree: BinarySearchTree, name: str) -> Optional[MenuItem]:
        target = None
        def _find(n):
            nonlocal target
            if n is None or target is not None:
                return
            _find(n.left)
            if n.value.item.name.lower() == name.lower():
                target = n.value
                return
            _find(n.right)
        _find(tree.root)
        if target:
            tree.root = tree.delete(tree.root, target)
            for i, it in enumerate(self.items):
                if it.name.lower() == name.lower():
                    del self.items[i]
                    break
            return target.item
        return None

    def insert_item(self, tree: BinarySearchTree, name: str, price: int, category: str, popularity: int, sort_by: str):
        new_item = MenuItem(name, int(price), category, int(popularity))
        self.items.append(new_item)
        ci = ComparableItem(new_item, mode=sort_by, idx=len(self.items)-1)
        tree.root = tree.insert(tree.root, ci)
        return new_item

    def get_min_item(self, tree: BinarySearchTree):
        v = tree.get_min_value(tree.root)
        return v.item if v else None

    def get_max_item(self, tree: BinarySearchTree):
        v = tree.get_max_value(tree.root)
        return v.item if v else None

    def get_height(self, tree: BinarySearchTree):
        return tree.find_height(tree.root)

    def get_tree_html(self, tree: BinarySearchTree):
        if not tree or tree.root is None:
            return ""
        return self._node_to_html(tree.root)

    def _node_to_html(self, node):
        if node is None:
            return ""
        ci = node.value
        item = ci.item
        label = f"{item.name}<br/>₱{item.price} | ⭐{item.popularity}"
        children = ""
        if node.left or node.right:
            children += "<ul>"
            if node.left:
                children += f"<li>{self._node_to_html(node.left)}</li>"
            if node.right:
                children += f"<li>{self._node_to_html(node.right)}</li>"
            children += "</ul>"
        return f"<ul><li><a href='#'><span>{label}</span></a>{children}</li></ul>"

    def ascii_tree(self, node, prefix=""):
        if node is None:
            return ""
        lines = []
        item = node.value.item
        lines.append(f"{prefix}{item.name} (₱{item.price} | ⭐{item.popularity})")
        if node.left:
            lines.append(self.ascii_tree(node.left, prefix + "  L-"))
        if node.right:
            lines.append(self.ascii_tree(node.right, prefix + "  R-"))
        return "\n".join(lines)