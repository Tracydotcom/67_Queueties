from flask import Flask, render_template, request, redirect, url_for
from myqueue import Queue
from binaryTree import BinaryTree, Node

app = Flask(__name__)

# --- Queue setup ---
order_queue = Queue()

# --- Global course trees ---
# Initialize Sewing Tree manually so it matches the old hardcoded HTML
sewing_tree = BinaryTree("Learn how to sew")
# Root: Learn how to sew
# L: Sew a dress, R: Sew a pocket
sewing_tree.root.left = Node("Sew a dress")
sewing_tree.root.right = Node("Sew a pocket")
# L->L: Alter a shirt
sewing_tree.root.left.left = Node("Alter a shirt")
# L->L->L: Basic stitches, L->L->R: Basic fabric
sewing_tree.root.left.left.left = Node("Learn basic stitches")
sewing_tree.root.left.left.right = Node("Learn basic fabric types")
# R->L: Sewing machine, R->R: Draping
sewing_tree.root.right.left = Node("Use a sewing machine")
sewing_tree.root.right.right = Node("Learn draping techniques")

# Initialize Drawing Tree
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

def gather_nodes_with_paths(node, path=None, out=None):
    if out is None:
        out = []
    if path is None:
        path = []
    if node is None:
        return out
    out.append((node.value, "".join(path)))
    if node.left:
        gather_nodes_with_paths(node.left, path + ["L"], out=out)
    if node.right:
        gather_nodes_with_paths(node.right, path + ["R"], out=out)
    return out

def convert_tree_to_html(node, current_path=""):
    """Recursively convert BinaryTree nodes to HTML list items with path and status."""
    if node is None:
        return ""
    
    # Determine the CSS class for completed status
    completed_class = "completed-node" if node.completed else ""

    children = ""
    if node.left or node.right:
        children += "<ul>"
        
        # LEFT CHILD
        if node.left:
            left_path = current_path + "L"
            left_children_html = convert_tree_to_html(node.left, left_path)
            # The <a> tag now uses the toggle_goal function via onclick
            children += f"""<li><a href='#' class='{completed_class}' onclick='toggleGoal("{node.left.value}", "{left_path}"); return false;'><span>{node.left.value}</span></a>{left_children_html}</li>"""

        # RIGHT CHILD
        if node.right:
            right_path = current_path + "R"
            right_children_html = convert_tree_to_html(node.right, right_path)
            # The <a> tag now uses the toggle_goal function via onclick
            children += f"""<li><a href='#' class='{completed_class}' onclick='toggleGoal("{node.right.value}", "{right_path}"); return false;'><span>{node.right.value}</span></a>{right_children_html}</li>"""
            
        children += "</ul>"
    return children

def generate_html_tree(tree):
    if not tree or not tree.root:
        return ""

    root_node = tree.root
    root_completed_class = "completed-node" if root_node.completed else ""
    
    # Path for root is empty string ""
    root_children_html = convert_tree_to_html(root_node, "")

    # Root node also gets the click handler. Path is empty string.
    return f"""<ul><li><a href='#' class='{root_completed_class}' onclick='toggleGoal("{root_node.value}", ""); return false;'><span>{root_node.value}</span></a>{root_children_html}</li></ul>"""

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

# --- NEW ROUTE FOR TOGGLING GOALS ---
@app.route("/toggle_goal/<course_name>/<path:node_path>", methods=["POST"])
@app.route("/toggle_goal/<course_name>/", methods=["POST"]) # Handle root (empty path)
def toggle_goal(course_name, node_path=""):
    # node_path comes in as a string of 'L's and 'R's
    path_list = list(node_path) if node_path else []
    
    # Use the course name stored in the dictionary keys
    tree = courses.get(course_name) 

    if not tree:
        return redirect(url_for('tree_page', result="Error: Course not found."))

    # Find the node using the path
    node_to_toggle = tree.find_by_path(path_list)

    if not node_to_toggle:
        return redirect(url_for('tree_page', result="Error: Node not found."))

    # Apply the logic from binaryTree.py
    result_message = tree.toggle_node(node_to_toggle)
    
    # Update last selected so we stay on this page
    last_selected_course["course"] = course_name
    
    return redirect(url_for('tree_page', result=result_message))


@app.route("/tree", methods=["GET", "POST"])
def tree_page():
    result = request.args.get('result', "") # Get result from redirect if exists
    selected_course = last_selected_course["course"]
    
    # Safety check if selected course was deleted
    if selected_course not in courses and courses:
        selected_course = next(iter(courses.keys()))
        last_selected_course["course"] = selected_course
    
    tree = courses.get(selected_course)
    show_custom_panel = False
    
    if request.method == "POST":
        # --- DELETE COURSE ---
        delete_course = request.form.get("delete_course")
        if delete_course and delete_course in courses:
            courses.pop(delete_course)
            result = f"Course '{delete_course}' deleted successfully."
            # Pick another course if available
            if courses:
                selected_course = next(iter(courses.keys()))
                last_selected_course["course"] = selected_course
                tree = courses.get(selected_course)
            else:
                selected_course = None
                tree = None

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

        # --- Insert node under existing node ---
        parent_path = request.form.get("parent_path")
        new_value = request.form.get("new_value", "").strip()
        side = request.form.get("side")
        
        if parent_path is not None and new_value and tree:
            # Handle empty string for root path
            path_list = list(parent_path) if parent_path else []
            parent_node = tree.find_by_path(path_list)
            
            if parent_node:
                if side == "L":
                    tree.insert_left(parent_node, new_value)
                else:
                    tree.insert_right(parent_node, new_value)
                result = f"Added '{new_value}' under '{parent_node.value}' on {side} side."
                show_custom_panel = True

        # --- DONE button ---
        if "finish_custom" in request.form:
            show_custom_panel = False
            result = f"Custom course '{tree.root.value}' is done."

    # Generate HTML for WHATEVER tree is selected (no more hardcoding)
    tree_html = generate_html_tree(tree) if tree else ""
    nodes_with_paths = gather_nodes_with_paths(tree.root) if tree else []

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
