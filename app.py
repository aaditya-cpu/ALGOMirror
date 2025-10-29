# app.py (FINAL, CLEANED, AND CORRECTED)

import random
import math
from flask import Flask, render_template, jsonify, request

# Import all necessary algorithm functions
from algorithms.searching import linear_search, binary_search, jump_search, interpolation_search
from algorithms.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort
from algorithms.trees import bst_build_steps
from algorithms.graphs import bfs, dfs, dijkstra_steps
from algorithms.other_algorithms import fib_dp_steps

# Import the validated content dictionaries
from content import ALGORITHM_CONTENT, DATA_STRUCTURE_INFO

app = Flask(__name__)

# This dictionary maps algorithm keys to their implementation functions
ALGORITHM_FUNCTIONS = {
    'linear_search': linear_search, 'binary_search': binary_search, 'jump_search': jump_search, 'interpolation_search': interpolation_search,
    'bubble_sort': bubble_sort, 'selection_sort': selection_sort, 'insertion_sort': insertion_sort, 'merge_sort': merge_sort, 'quick_sort': quick_sort,
    'bst_build': bst_build_steps,
    'bfs': bfs, 'dfs': dfs, 'dijkstra': dijkstra_steps,
    'fib_dp': fib_dp_steps,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_content')
def get_content():
    return jsonify({"algorithms": ALGORITHM_CONTENT, "data_structures": DATA_STRUCTURE_INFO})

@app.route('/generate_data', methods=['POST'])
def generate_data():
    data = request.get_json()
    size = int(data.get('size', 12))
    dtype = data.get('dtype', 'array')
    if dtype == 'array':
        is_sorted = data.get('sorted', False)
        arr = [random.randint(1, 100) for _ in range(size)]
        if is_sorted: arr.sort()
        return jsonify(arr)
    elif dtype == 'tree':
        return jsonify(random.sample(range(1, 100), k=min(size, 99)))
    elif dtype == 'graph':
        num_nodes = min(size, 26)
        nodes, node_ids = {}, [chr(65 + i) for i in range(num_nodes)]
        width, height, center_x, center_y = 700, 350, 350, 175
        radius = min(center_x, center_y) * 0.8
        for i, node_id in enumerate(node_ids):
            angle = (2 * math.pi / num_nodes) * i
            nodes[node_id] = {"x": center_x + radius * math.cos(angle), "y": center_y + radius * math.sin(angle)}
        adj_list = {node_id: [] for node_id in node_ids}
        num_edges = int(num_nodes * 1.5)
        # Use a set to prevent trying to add duplicate edges
        existing_edges = set()
        for _ in range(num_edges * 5): # More attempts to connect graph
             u, v = random.sample(node_ids, 2)
             edge = tuple(sorted((u,v)))
             if u != v and edge not in existing_edges:
                weight = random.randint(1, 10)
                adj_list[u].append({"node": v, "weight": weight})
                adj_list[v].append({"node": u, "weight": weight})
                existing_edges.add(edge)
        return jsonify({"nodes": nodes, "adjacency_list": adj_list})
    return jsonify([])

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.get_json()
    key = data.get('algorithm')
    if not key or key not in ALGORITHM_FUNCTIONS:
        return jsonify({'error': f"Algorithm '{key}' not found or is not implemented."}), 400
    
    func = ALGORITHM_FUNCTIONS[key]
    try:
        # Use the robust 'category' and 'ds' keys from content.py for routing
        algo_info = ALGORITHM_CONTENT[key]
        if algo_info['category'] == 'Searching':
            return jsonify({'steps': func(data.get('input_data'), int(data.get('target')))})
        elif key == 'dijkstra':
            return jsonify({'steps': func(data.get('input_data'), data.get('start_node'), data.get('end_node'))})
        elif algo_info['category'] in ['Graph Traversal', 'Shortest Path']:
            return jsonify({'steps': func(data.get('input_data'), data.get('start_node'))})
        elif algo_info['ds'] == 'conceptual':
            return jsonify({'steps': func(int(data.get('n', 5)))})
        else: # Covers all other cases like sorting, bst_build
            return jsonify({'steps': func(data.get('input_data'))})
    except Exception as e:
        print(f"ERROR executing {key}: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__': jsonify({'error': 'Server error during algorithm execution.'}), 500

if __name__ == '__main__':
    app.run(debug=True)