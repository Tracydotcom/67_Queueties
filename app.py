from flask import Flask, render_template, request, redirect, url_for
from myqueue import Queue
from binaryTree import BinaryTree, Node
from BSTmenu import BSTMenuManager

app = Flask(__name__)

# --- Queue setup ---
order_queue = Queue()

# --- Global course trees ---
# (existing binaryTree initialization unchanged)
sewing_tree = BinaryTree("Learn how to sew")
sewing_tree.root.left = Node("Sew a dress")
sewing_tree.root.right = Node("Sew a pocket")
sewing_tree.root.left.left = Node("Alter a shirt")
sewing_tree.root.left.left.left = Node("Learn basic stitches")
sewing_tree.root.left.left.right = Node("Learn basic fabric types")
sewing_tree.root.right.left = Node("Use a sewing machine")
sewing_tree.root.right.right = Node("Learn draping techniques")

drawing_tree = BinaryTree("Learn how to draw")
drawing_tree.root.left = Node("Perspective drawing")
drawing_tree.root.left.left = Node("One-point perspective")
drawing_tree.root.left.left.left = Node("Sketch basic shapes")
drawing_tree.root.left.left.left.left = Node("Circles & Squares")
drawing_tree.root.left.left.left.right = Node("Own Shapes")
drawing_tree.root.left.right = Node("Two-point perspective")
drawing_tree.root.left.right.left = Node("Sketch basic forms")
drawing_tree.root.left.right.left.left = Node("Cylinder & Cone")
drawing_tree.root.left.right.left.right = Node("Pyramid & Cube")

courses = {
    "Learn how to sew": sewing_tree,
    "Learn how to draw": drawing_tree,
}

default_course = "Learn how to sew"
last_selected_course = {"course": default_course}

# --- Helper functions (unchanged) ---
def tree_to_dict(node):
    if node is None:
        return None
    return {
        "value": node.value,
        "completed": getattr(node, "completed", False),
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right)
    }

def gather_nodes_with_available_slots(node, path=None, out=None):
    if out is None:
        out = []
    if path is None:
        path = []
    if node is None:
        return out
    available_sides = []
    if not node.left:
        available_sides.append("L")
    if not node.right:
        available_sides.append("R")
    if available_sides:
        out.append((node.value, "".join(path), available_sides))
    if node.left:
        gather_nodes_with_available_slots(node.left, path + ["L"], out)
    if node.right:
        gather_nodes_with_available_slots(node.right, path + ["R"], out)
    return out

def convert_tree_to_html(node, current_path=""):
    if node is None:
        return ""
    completed_class = "completed-node" if node.completed else ""
    children = ""
    if node.left or node.right:
        children += "<ul>"
        if node.left:
            left_path = current_path + "L"
            left_children_html = convert_tree_to_html(node.left, left_path)
            children += f"""<li><a href='#' class='{completed_class}' onclick='toggleGoal("{node.left.value}", "{left_path}"); return false;'><span>{node.left.value}</span></a>{left_children_html}</li>"""
        if node.right:
            right_path = current_path + "R"
            right_children_html = convert_tree_to_html(node.right, right_path)
            children += f"""<li><a href='#' class='{completed_class}' onclick='toggleGoal("{node.right.value}", "{right_path}"); return false;'><span>{node.right.value}</span></a>{right_children_html}</li>"""
        children += "</ul>"
    return children

def generate_html_tree(tree):
    if not tree or not tree.root:
        return ""
    root_node = tree.root
    root_completed_class = "completed-node" if getattr(root_node, "completed", False) else ""
    root_children_html = convert_tree_to_html(root_node, "")
    return f"""<ul><li><a href='#' class='{root_completed_class}' onclick='toggleGoal("{root_node.value}", ""); return false;'><span>{root_node.value}</span></a>{root_children_html}</li></ul>"""

# --- Flask routes (unchanged earlier ones) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    if request.method == 'POST':
        operation = request.form.get('operation')
    return render_template('works.html', result=result)

@app.route('/queue', methods=['GET', 'POST'])
def queue_page():
    result = None
    if request.method == 'POST':
        if 'enterOrder' in request.form:
            selected_items = {}
            for item_name in order_queue.MENU.keys():
                quantity = request.form.get(item_name, 0, type=int)
                if quantity > 0:
                    selected_items[item_name] = quantity
            if selected_items:
                order_details = order_queue.enqueue(selected_items)
                wait_mins, wait_secs = divmod(order_details['wait'], 60)
                result = f"Order {order_details['code']} added! Total: P{order_details['total']:.2f}. Est. wait: {int(wait_mins)}m {int(wait_secs)}s"
            else:
                result = "Please select at least one item."
        elif 'finishOrder' in request.form:
            served = order_queue.dequeue()
            if served:
                result = f"Served order {served['code']}"
            else:
                result = "Queue is empty!"
    return render_template(
        'queue.html',
        queue=order_queue.display(),
        result=result,
        menu=order_queue.MENU
    )

@app.route("/toggle_goal/<course_name>/<path:node_path>", methods=["POST"])
@app.route("/toggle_goal/<course_name>/", methods=["POST"])
def toggle_goal(course_name, node_path=""):
    path_list = list(node_path) if node_path else []
    tree = courses.get(course_name)
    if not tree:
        return redirect(url_for('tree_page', result="Error: Course not found."))
    node_to_toggle = tree.find_by_path(path_list)
    if not node_to_toggle:
        return redirect(url_for('tree_page', result="Error: Node not found."))
    result_message = tree.toggle_node(node_to_toggle)
    last_selected_course["course"] = course_name
    return redirect(url_for('btree_page', result=result_message))

@app.route("/binarytree", methods=["GET", "POST"])
def btree_page():
    result = request.args.get('result', "")
    selected_course = last_selected_course["course"]
    if selected_course not in courses and courses:
        selected_course = next(iter(courses.keys()))
        last_selected_course["course"] = selected_course
    tree = courses.get(selected_course)
    show_custom_panel = False
    if request.method == "POST":
        delete_course = request.form.get("delete_course")
        if delete_course and delete_course in courses:
            courses.pop(delete_course)
            result = f"Course '{delete_course}' deleted successfully."
            if courses:
                selected_course = next(iter(courses.keys()))
                last_selected_course["course"] = selected_course
                tree = courses.get(selected_course)
            else:
                selected_course = None
                tree = None
        clicked_course = request.form.get("course")
        if clicked_course and clicked_course in courses:
            selected_course = clicked_course
            tree = courses[selected_course]
            last_selected_course["course"] = selected_course
        if "create_custom" in request.form:
            show_custom_panel = True
        if "save_custom_tree" in request.form:
            course_title = request.form.get("root_goal", "").strip()
            root_node_value = request.form.get("child_goal", "").strip()
            if not course_title or not root_node_value:
                result = "Error: Course Title and Top Goal (Root Node) are mandatory."
                show_custom_panel = True
            elif course_title in courses:
                result = f"Error: Course '{course_title}' already exists."
                show_custom_panel = True
            else:
                new_tree = BinaryTree(root_node_value)
                courses[course_title] = new_tree
                selected_course = course_title
                tree = new_tree
                last_selected_course["course"] = course_title
                show_custom_panel = True
                result = f"Custom course '{course_title}' created."
        parent_path = request.form.get("parent_path")
        new_value = request.form.get("new_value", "").strip()
        side = request.form.get("side")
        if parent_path is not None and new_value and tree:
            path_list = list(parent_path) if parent_path else []
            parent_node = tree.find_by_path(path_list)
            if parent_node:
                if side == "L":
                    tree.insert_left(parent_node, new_value)
                else:
                    tree.insert_right(parent_node, new_value)
                result = f"Added '{new_value}' under '{parent_node.value}' on {side} side."
                show_custom_panel = True
        if "finish_custom" in request.form:
            show_custom_panel = False
            result = f"Custom course '{tree.root.value}' is done."
    BinaryTree_html = generate_html_tree(tree) if tree else ""
    nodes_with_paths = gather_nodes_with_available_slots(tree.root) if tree else []
    return render_template(
        "binarytree.html",
        result=result,
        courses=list(courses.keys()),
        selected_course=selected_course,
        show_custom_panel=show_custom_panel,
        nodes_with_paths=nodes_with_paths,
        tree_html=BinaryTree_html
    )

# ----- BST Menu route -----
bst_manager = BSTMenuManager()

@app.route('/BSTmenu', methods=['GET', 'POST'])
def bst_menu():
    message = None
    categories = bst_manager.get_categories()
    selected_category = request.values.get('category') or (categories[0] if categories else '')
    sort_by = request.values.get('sort_by') or 'price'
    root_strategy = request.values.get('root_strategy') or 'oldest'

    # Build the tree using the chosen root strategy
    tree, display_sorted = bst_manager.build_tree_for_category(selected_category, sort_by, root_strategy)

    # initial traversals and stats
    traversals = {
        'inorder': bst_manager.inorder(tree),
        'preorder': bst_manager.preorder(tree),
        'postorder': bst_manager.postorder(tree)
    }
    stats = {
        'min': bst_manager.get_min_item(tree),
        'max': bst_manager.get_max_item(tree),
        'height': bst_manager.get_height(tree)
    }

    if request.method == 'POST':
        # preserve root_strategy from POST form if present
        root_strategy = request.form.get('root_strategy') or root_strategy

        # Search
        if request.form.get('search_name'):
            q = request.form.get('search_name').strip()
            found = bst_manager.search_by_name(tree, q)
            message = f"Found: {found}" if found else f"'{q}' not found."
        # Insert
        elif request.form.get('insert_name'):
            try:
                name = request.form.get('insert_name').strip()
                price = int(request.form.get('insert_price') or 0)
                category_new = request.form.get('insert_category') or selected_category
                popularity = int(request.form.get('insert_popularity') or 0)
                new_item = bst_manager.insert_item(tree, name, price, category_new, popularity, sort_by)
                message = f"Inserted: {new_item}"
                if category_new == selected_category:
                    tree, display_sorted = bst_manager.build_tree_for_category(selected_category, sort_by, root_strategy)
            except Exception as e:
                message = f"Insert error: {e}"
        # Delete
        elif request.form.get('delete_name'):
            name = request.form.get('delete_name').strip()
            deleted = bst_manager.delete_by_name(tree, name)
            if deleted:
                message = f"Deleted: {deleted}"
                tree, display_sorted = bst_manager.build_tree_for_category(selected_category, sort_by, root_strategy)
            else:
                message = f"'{name}' not found to delete."

        # refresh traversals and stats after changes
        traversals = {
            'inorder': bst_manager.inorder(tree),
            'preorder': bst_manager.preorder(tree),
            'postorder': bst_manager.postorder(tree)
        }
        stats = {
            'min': bst_manager.get_min_item(tree),
            'max': bst_manager.get_max_item(tree),
            'height': bst_manager.get_height(tree)
        }

    tree_html = bst_manager.get_tree_html(tree)
    return render_template(
        'BSTmenu.html',
        categories=categories,
        selected_category=selected_category,
        sort_by=sort_by,
        root_strategy=root_strategy,
        display_sorted=display_sorted,
        tree_html=tree_html,
        traversals=traversals,
        stats=stats,
        message=message
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)