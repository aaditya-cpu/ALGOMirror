/algorithmic-mirror
├── app.py                  # Main Flask application
├── content.py              # The complete content database (provided below)
├── /algorithms
│   ├── __init__.py         # Makes the folder a Python package
│   ├── searching.py        # Logic for Linear, Binary, Jump search etc.
│   ├── sorting.py          # Logic for Bubble, Quick, Merge sort etc.
│   ├── trees.py            # Logic for BST, traversals etc.
│   ├── graphs.py           # Logic for BFS, DFS, Dijkstra etc.
│   └── (other_algorithms.py) # For DP, Greedy, etc. if needed
├── /static
│   ├── /css
│   │   └── style.css       # All the styling
│   └── /js
│       ├── main.js         # Core frontend logic, event handling, API calls
│       └── animator.js     # Handles the animation loop and visual changes
└── /templates
    └── index.html          # The single HTML page for the application