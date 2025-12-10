from flask import Flask, render_template, request
from myqueue import Queue
from binaryTree import BinaryTree, Node

app = Flask(__name__)

# --- Queue setup ---
order_queue = Queue()

# --- Global course trees ---
courses = {
    "Learn how to sew": BinaryTree("Sewing"),
    "Learn how to draw": BinaryTree("Drawing"),
}

default_course = "Learn how to sew"

# Track last selected course
last_selected_course = {"course": default_course}

# --- Helper functions ---
def tree_to_dict(node):
    if node is None:
        return None
    return {
        "value": node.value,
        "completed": getattr(node, "completed", False),
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right)
    }

def gather_nodes_with_available_sides(node, path=None, out=None):
    """
    Returns a list of tuples: (node value, path, allowed_sides)
    allowed_sides = list of "L" and/or "R" where insertion is possible
    """
    if out is None:
        out = []
    if path is None:
        path = []
    if node is None:
        return out

    allowed_sides = []
    if node.left is None:
        allowed_sides.append("L")
    if node.right is None:
        allowed_sides.append("R")

    # Only include nodes that have at least one available side
    if allowed_sides:
        out.append((node.value, "".join(path), allowed_sides))

    if node.left:
        gather_nodes_with_available_sides(node.left, path + ["L"], out)
    if node.right:
        gather_nodes_with_available_sides(node.right, path + ["R"], out)
    return out

def convert_tree_to_html(node):
    """Recursively convert BinaryTree nodes to HTML list items."""
    if node is None:
        return ""
    children = ""
    # Only show existing children
    if node.left or node.right:
        children += "<ul>"
        if node.left:
            children += "<li><a href='#'><span>{}</span></a>{}</li>".format(
                node.left.value, convert_tree_to_html(node.left)
            )
        if node.right:
            children += "<li><a href='#'><span>{}</span></a>{}</li>".format(
                node.right.value, convert_tree_to_html(node.right)
            )
        children += "</ul>"
    return children

def generate_html_tree(tree):
    if not tree or not tree.root:
        return ""
    return "<ul><li><a href='#'><span>{}</span></a>{}</li></ul>".format(
        tree.root.value, convert_tree_to_html(tree.root)
    )

# --- Flask routes ---
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

@app.route("/tree", methods=["GET", "POST"])
def tree_page():
    result = ""
    selected_course = last_selected_course["course"]
    tree = courses.get(selected_course)
    show_custom_panel = False
    tree_html = ""

    if request.method == "POST":
        # --- DELETE COURSE ---
        delete_course = request.form.get("delete_course")
        if delete_course and delete_course in courses:
            courses.pop(delete_course)
            result = f"Course '{delete_course}' deleted successfully."
            selected_course = next(iter(courses.keys()), None)
            tree = courses.get(selected_course)
            last_selected_course["course"] = selected_course

        # --- Course selection ---
        clicked_course = request.form.get("course")
        if clicked_course and clicked_course in courses:
            selected_course = clicked_course
            tree = courses[selected_course]
            last_selected_course["course"] = selected_course

        # --- Show custom panel ---
        if "create_custom" in request.form:
            show_custom_panel = True

        # --- Save custom tree ---
        if "save_custom_tree" in request.form:
            root_goal = request.form.get("root_goal", "").strip()
            if root_goal:
                new_tree = BinaryTree(root_goal)
                courses[root_goal] = new_tree
                selected_course = root_goal
                tree = new_tree
                last_selected_course["course"] = root_goal
                show_custom_panel = True
                result = f"Custom course '{root_goal}' created successfully."

        # --- Insert node under existing node ---
        parent_path = request.form.get("parent_path")
        new_value = request.form.get("new_value", "").strip()
        side = request.form.get("side")
        if parent_path is not None and new_value and tree:
            parent_node = tree.find_by_path(list(parent_path))
            if parent_node:
                if (side == "L" and parent_node.left is None) or (side == "R" and parent_node.right is None):
                    if side == "L":
                        tree.insert_left(parent_node, new_value)
                    else:
                        tree.insert_right(parent_node, new_value)
                    result = f"Added '{new_value}' under '{parent_node.value}' on {side} side."
                else:
                    result = f"Cannot insert on {side} side. Node already has a child there."
                show_custom_panel = True

        # --- DONE button ---
        if "finish_custom" in request.form:
            tree_html = generate_html_tree(tree)
            show_custom_panel = False
            result = f"Custom course '{tree.root.value}' is done."

    # Display tree_html for previously done trees
    if not tree_html and selected_course not in ["Learn how to sew", "Learn how to draw"]:
        tree_html = generate_html_tree(tree)

    nodes_with_paths = gather_nodes_with_available_sides(tree.root) if tree else []

    return render_template(
        "tree.html",
        result=result,
        courses=list(courses.keys()),
        selected_course=selected_course,
        show_custom_panel=show_custom_panel,
        nodes_with_paths=nodes_with_paths,
        tree_html=tree_html
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
