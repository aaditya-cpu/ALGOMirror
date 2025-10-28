# app.py

# =================================================================
# 1. IMPORTS
# =================================================================
# Standard Flask imports and utilities
from flask import Flask, render_template, jsonify, request
import random

# For generating random words for Trie/String structures (if implemented)
from wonderwords import RandomWord

# Import all algorithm step-generation functions from the 'algorithms' package
from algorithms.searching import linear_search, binary_search
from algorithms.sorting import bubble_sort, selection_sort
from algorithms.trees import bst_build_steps
from algorithms.graphs import bfs, dfs
from algorithms.other_algorithms import (
    fib_dp_steps, knapsack_01_steps, fractional_knapsack_steps,
    hanoi_steps, bitwise_swap_steps, count_set_bits_steps
)

# Import the descriptive content (pseudocode, complexity, etc.) from content.py
from content import ALGORITHM_CONTENT, DATA_STRUCTURE_INFO

# =================================================================
# 2. FLASK APP INITIALIZATION
# =================================================================
app = Flask(__name__)
r = RandomWord() # Initialize the random word generator

# =================================================================
# 3. ALGORITHM TO FUNCTION MAPPING
# =================================================================
# This dictionary is the core of the backend logic. It maps the string identifier for an algorithm
# (used by the frontend and in content.py) to the actual Python function that
# generates the animation steps. To add a new algorithm, you must implement its
# logic in the /algorithms package and add its entry here.
ALGORITHM_FUNCTIONS = {
    # Searching
    'linear_search': linear_search,
    'binary_search': binary_search,
    # Sorting
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    # Trees
    'bst_build': bst_build_steps,
    # Graphs
    'bfs': bfs,
    'dfs': dfs,
    # Dynamic Programming
    'fib_dp': fib_dp_steps,
    'knapsack_01': knapsack_01_steps,
    # Greedy
    'fractional_knapsack': fractional_knapsack_steps,
    # Recursion
    'hanoi': hanoi_steps,
    # Bitwise
    'bitwise_swap': bitwise_swap_steps,
    'count_set_bits': count_set_bits_steps,
}

# =================================================================
# 4. API ROUTES / ENDPOINTS
# =================================================================

@app.route('/')
def index():
    """Serves the main single-page application file (index.html)."""
    return render_template('index.html')

@app.route('/get_content')
def get_content():
    """Provides the frontend with all descriptive content for algorithms and data structures."""
    return jsonify({
        "algorithms": ALGORITHM_CONTENT,
        "data_structures": DATA_STRUCTURE_INFO
    })

@app.route('/generate_data', methods=['POST'])
def generate_data():
    """Generates initial data structures based on requests from the frontend."""
    data = request.get_json()
    size = int(data.get('size', 10))
    dtype = data.get('dtype', 'array')
    is_sorted = data.get('sorted', False)

    if dtype == 'array':
        arr = [random.randint(1, 100) for _ in range(size)]
        if is_sorted:
            arr.sort()
        return jsonify(arr)

    elif dtype == 'tree':
        # For BSTs, unique values are best. random.sample ensures this.
        arr = random.sample(range(1, 100), k=min(size, 99))
        return jsonify(arr)

    elif dtype == 'graph':
        # Generate a dynamic, weighted graph
        num_nodes = min(size, 26) # Limit to 26 nodes (A-Z)
        nodes = {}
        node_ids = [chr(65 + i) for i in range(num_nodes)] # A, B, C...

        # Position nodes randomly in a circle for a clean layout
        width, height = 700, 350
        center_x, center_y = width / 2, height / 2
        radius = min(center_x, center_y) * 0.8
        for i, node_id in enumerate(node_ids):
            angle = (2 * math.pi / num_nodes) * i
            nodes[node_id] = {
                "x": center_x + radius * math.cos(angle),
                "y": center_y + radius * math.sin(angle)
            }

        adjacency_list = {node_id: [] for node_id in node_ids}
        num_edges = int(num_nodes * 1.5) # Create a reasonable number of edges

        for _ in range(num_edges):
            u, v = random.sample(node_ids, 2)
            # Ensure no duplicate edges
            if not any(neighbor['node'] == v for neighbor in adjacency_list[u]):
                weight = random.randint(1, 10)
                adjacency_list[u].append({"node": v, "weight": weight})
                adjacency_list[v].append({"node": u, "weight": weight}) # Undirected graph

        graph = {"nodes": nodes, "adjacency_list": adjacency_list}
        return jsonify(graph)
    return jsonify([])

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    """
    The main endpoint for executing an algorithm. It receives the algorithm key and required
    parameters, calls the corresponding function, and returns the generated animation steps.
    """
    data = request.get_json()
    algorithm_key = data.get('algorithm')

    if not algorithm_key or algorithm_key not in ALGORITHM_FUNCTIONS:
        return jsonify({'error': f"Algorithm '{algorithm_key}' not found or is not implemented."}), 400

    func = ALGORITHM_FUNCTIONS[algorithm_key]

    try:
        # This block determines which parameters to pass to the function based on the algorithm key.
        if "search" in algorithm_key:
            steps = func(data.get('input_data'), int(data.get('target')))
        elif algorithm_key in ['bfs', 'dfs']:
            steps = func(data.get('input_data'), data.get('start_node'))
        elif algorithm_key == 'fib_dp':
            steps = func(int(data.get('n', 5))) # Default to 5 if not provided
        elif algorithm_key == 'knapsack_01' or algorithm_key == 'fractional_knapsack':
            # Assumes frontend sends capacity and items for knapsack problems
            steps = func(int(data.get('capacity')), data.get('items'))
        elif algorithm_key == 'hanoi':
            steps = func(int(data.get('n_disks', 3)))
        elif algorithm_key == 'bitwise_swap':
            steps = func(int(data.get('a')), int(data.get('b')))
        elif algorithm_key == 'count_set_bits':
            steps = func(int(data.get('n')))
        else:
            # Default case for algorithms that only need the main data structure
            # (e.g., sorting, bst_build)
            steps = func(data.get('input_data'))
        
        return jsonify({'steps': steps})

    except Exception as e:
        # A robust catch-all for any unexpected errors during algorithm execution.
        print(f"Error running algorithm '{algorithm_key}': {e}") # Log the full error for debugging
        return jsonify({'error': 'An unexpected error occurred on the server while running the algorithm.'}), 500

# =================================================================
# 5. SERVER EXECUTION
# =================================================================
if __name__ == '__main__':
    """
    Allows the script to be run directly using 'python app.py'.
    debug=True enables features like auto-reloading, which is very helpful for development.
    """
    app.run(debug=True)