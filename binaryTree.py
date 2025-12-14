
import random
import string

class Node:
    """A node in a binary tree."""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.completed = False  # checkbox state

class BinaryTree:
    """A binary tree data structure."""
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def insert_left(self, current_node, value):
        """Insert a node as the left child ONLY if empty."""
        if current_node.left is None:
            current_node.left = Node(value)
            return True  # Success
        else:
            return False # Failed: Spot occupied

    def insert_right(self, current_node, value):
        """Insert a node as the right child ONLY if empty."""
        if current_node.right is None:
            current_node.right = Node(value)
            return True  # Success
        else:
            return False # Failed: Spot occupied

    # traversal methods unchanged
    def preorder_traversal(self, start, traversal=""):
        if start:
            traversal += str(start.value) + " "
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal.strip()

    def inorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += str(start.value) + " "
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal.strip()

    def postorder_traversal(self, start, traversal=""):
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += str(start.value) + " "
        return traversal.strip()

    def search(self, root, key):
        """Return True if node exists, False otherwise."""
        nodes = self.inorder_traversal(root).split()
        return key in nodes

    def delete(self, root, key):
        """Delete a node using BFS (level-order delete). Return message."""
        if root is None:
            return "No tree exists."

        if root.value == key and root.left is None and root.right is None:
            self.root = None
            return f"Node '{key}' deleted. Tree is now empty."

        queue = [(root, None)]
        key_node = None
        deep = None
        deep_parent = None

        while queue:
            current, parent = queue.pop(0)
            deep = current
            deep_parent = parent

            if current.value == key:
                key_node = current

            if current.left:
                queue.append((current.left, current))
            if current.right:
                queue.append((current.right, current))

        if key_node is None:
            return f"Node '{key}' not found."

        key_node.value = deep.value

        if deep_parent:
            if deep_parent.left == deep:
                deep_parent.left = None
            else:
                deep_parent.right = None

        return f"Node '{key}' deleted."

    # -------------------------
    # New helpers for web UI
    # -------------------------
    def find_by_path(self, path):
        """
        Path is a list of 'L' and 'R' steps from root.
        Example: ['L','R','L'] -> root.left.right.left
        """
        node = self.root
        if node is None:
            return None
        for step in path:
            if step == 'L':
                node = node.left
            elif step == 'R':
                node = node.right
            else:
                return None
            if node is None:
                return None
        return node

    def _generate_coupon(self):
        """Generate a random 8-character promo code."""
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"TIKTOK-{code}"

    def toggle_node(self, node):
        """
        Toggle node.completed only if allowed.
        Logic: A node can only be completed if all its existing children are completed.
        """
        if node is None:
            return "Node not found."

        # If already completed, allow un-checking (reverting) without strict checks
        if node.completed:
            node.completed = False
            return f"Reverted '{node.value}' to incomplete."

        # Check if children are ready (either None or Completed)
        left_ready = node.left is None or node.left.completed
        right_ready = node.right is None or node.right.completed

        if left_ready and right_ready:
            node.completed = True
            coupon = self._generate_coupon()
            return f"Goal '{node.value}' COMPLETED! Reward Coupon: {coupon}"
        else:
            return f"Locked: You must complete the smaller tasks below '{node.value}' first!"
