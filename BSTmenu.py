from myqueue import MENU

class BSTNode:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        self.left = None
        self.right = None

class BSTMenuManager:
    def __init__(self):
        self.roots = {} 
        self.categories_map = {
            "Drinks": ["Brewed Coffee", "Iced Coffee", "Milk Tea (Bubble Tea)", "Fresh Lemonade", "Fruit Shake (Banana)", "Canned Soda / Bottled Water"],
            "Street Food": ["French Fries", "Siomai (Steamed)", "Kwek-Kwek", "Fish Balls / Kikiam", "Pork BBQ Stick", "Grilled Hotdog", "Turon"],
            "Simple Meals": ["Tapsilog", "Lugaw / Congee (with toppings)", "Pasta (Simple sauce)", "Grilled Cheese Sandwich", "Basic Burger", "Pancit Canton (Stir-fry)"],
            "Baked Goods": ["Chocolate Chip Cookie", "Brownie Square", "Cheese Pandesal", "Banana Cue", "Leche Flan (Small)", "Halo-Halo (Basic)"]
        }
        self._load_data_categorized_balanced()

    def _load_data_categorized_balanced(self):
        for category in self.categories_map:
            self.reset_tree_with_root(category, None)

    def get_items_in_category(self, category):
        return self.categories_map.get(category, [])

    def reset_tree_with_root(self, category, chosen_root_name):
        self.roots[category] = None
        item_names = self.categories_map.get(category, [])
        items_data = []

        for name in item_names:
            if name in MENU:
                items_data.append({"name": name, "price": MENU[name]['price']})
        
        if not items_data: return

        root_data = None
        if chosen_root_name:
            for item in items_data:
                if item['name'] == chosen_root_name:
                    root_data = item
                    break
        else:
            items_data.sort(key=lambda x: x['price'])
            root_data = items_data[len(items_data) // 2]

        if root_data:
            self.insert(root_data['name'], root_data['price'], category)
            for item in items_data:
                if item['name'] != root_data['name']:
                    self.insert(item['name'], item['price'], category)

    def insert(self, name, price, category):
        """Internal use only for building trees."""
        current_root = self.roots.get(category)
        if current_root is None:
            self.roots[category] = BSTNode(name, price, category)
        else:
            self._insert_recursive(current_root, name, price, category)

    def _insert_recursive(self, current, name, price, category):
        if name.lower() == current.name.lower():
            return 

        if price < current.price:
            if current.left is None:
                current.left = BSTNode(name, price, category)
                return 
            self._insert_recursive(current.left, name, price, category)
        elif price > current.price:
            if current.right is None:
                current.right = BSTNode(name, price, category)
                return 
            self._insert_recursive(current.right, name, price, category)
        else:
            if name.lower() < current.name.lower():
                if current.left is None:
                    current.left = BSTNode(name, price, category)
                    return 
                self._insert_recursive(current.left, name, price, category)
            else:
                if current.right is None:
                    current.right = BSTNode(name, price, category)
                    return 
                self._insert_recursive(current.right, name, price, category)

    def get_category_root(self, category):
        return self.roots.get(category)
    
    def get_categories(self):
        return sorted(list(self.categories_map.keys()))

    def search_by_name(self, root, name):
        if not root: return None
        if root.name.lower() == name.lower(): return f"{root.name} (P{root.price})"
        res = self.search_by_name(root.left, name)
        if res: return res
        return self.search_by_name(root.right, name)

    # --- HTML GENERATOR ---
    def get_tree_html(self, node):
        if not node: return ""
        return f"<ul>{self._build_tree_recursive(node)}</ul>"

    def _build_tree_recursive(self, node):
        if not node: return ""
        
        html = f"<li>{self._node_link(node)}"
        
        if node.left or node.right:
            html += "<ul>"
            if node.left:
                html += self._build_tree_recursive(node.left)
            else:
                html += "<li class='ghost-node'><span>.</span></li>"
            
            if node.right:
                html += self._build_tree_recursive(node.right)
            else:
                html += "<li class='ghost-node'><span>.</span></li>"
            html += "</ul>"
            
        html += "</li>"
        return html

    def _node_link(self, node):
        return f"<a href='#'><span><b>{node.name}</b><br>P{node.price}</span></a>"

    # --- Stats ---
    def inorder(self, node, res=None):
        if res is None: res = []
        if not node: return res
        self.inorder(node.left, res)
        res.append(node.name)
        self.inorder(node.right, res)
        return res

    def preorder(self, node, res=None):
        if res is None: res = []
        if not node: return res
        res.append(node.name)
        self.preorder(node.left, res)
        self.preorder(node.right, res)
        return res

    def postorder(self, node, res=None):
        if res is None: res = []
        if not node: return res
        self.postorder(node.left, res)
        self.postorder(node.right, res)
        res.append(node.name)
        return res
    
    def get_height(self, node):
        if not node: return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def get_min(self, node):
        if not node: return "None"
        curr = node
        while curr.left: curr = curr.left
        return curr.name
    
    def get_max(self, node):
        if not node: return "None"
        curr = node
        while curr.right: curr = curr.right
        return curr.name