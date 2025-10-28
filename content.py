# content.py

ALGORITHM_CONTENT = {
    # =================================================================
    # 1. SEARCHING ALGORITHMS
    # =================================================================
    "linear_search": {
        "name": "Linear Search",
        "category": "Searching",
        "ds": "array",
        "idea": "Check each element one by one from the beginning until the target is found or the list ends. The simplest, most direct approach.",
        "pseudocode": """
function linearSearch(array, target):
    for i from 0 to length(array) - 1:
        if array[i] == target:
            return i  // Found
    return -1 // Not found
        """,
        "complexity": {
            "time_best": "O(1)", "time_avg": "O(n)", "time_worst": "O(n)", "space": "O(1)"
        }
    },
    "binary_search": {
        "name": "Binary Search",
        "category": "Searching",
        "ds": "array",
        "idea": "Efficiently find an item in a **sorted** array by repeatedly dividing the search interval in half. It compares the target value to the middle element of the array.",
        "pseudocode": """
function binarySearch(array, target):
    low = 0
    high = length(array) - 1
    while low <= high:
        mid = floor((low + high) / 2)
        if array[mid] == target:
            return mid
        else if array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
        """,
        "complexity": {
            "time_best": "O(1)", "time_avg": "O(log n)", "time_worst": "O(log n)", "space": "O(1)"
        }
    },
    "jump_search": {
        "name": "Jump Search",
        "category": "Searching",
        "ds": "array",
        "idea": "An improvement over linear search for large arrays. It works on a sorted array by jumping ahead in fixed steps, then performing a linear search in the identified block.",
        "pseudocode": """
function jumpSearch(array, target):
    n = length(array)
    step = floor(√n)
    prev = 0
    while array[min(step, n) - 1] < target:
        prev = step
        step += floor(√n)
        if prev >= n:
            return -1
    
    while array[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1
            
    if array[prev] == target:
        return prev
    return -1
        """,
        "complexity": {
            "time_best": "O(1)", "time_avg": "O(√n)", "time_worst": "O(√n)", "space": "O(1)"
        }
    },
    "interpolation_search": {
        "name": "Interpolation Search",
        "category": "Searching",
        "ds": "array",
        "idea": "An improvement over Binary Search for uniformly distributed data. It estimates the position of the target value based on the values at the ends of the search interval.",
        "pseudocode": """
function interpolationSearch(array, target):
    low = 0
    high = length(array) - 1
    while low <= high and target >= array[low] and target <= array[high]:
        // Estimate position
        pos = low + ((target - array[low]) * (high - low)) / (array[high] - array[low])
        
        if array[pos] == target:
            return pos
        if array[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1
        """,
        "complexity": {
            "time_best": "O(1)", "time_avg": "O(log log n)", "time_worst": "O(n)", "space": "O(1)"
        }
    },
    # =================================================================
    # 2. SORTING ALGORITHMS
    # =================================================================
    "bubble_sort": {
        "name": "Bubble Sort",
        "category": "Sorting",
        "ds": "array",
        "idea": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The largest elements 'bubble' to the end.",
        "pseudocode": """
function bubbleSort(array):
    n = length(array)
    for i from 0 to n-1:
        swapped = false
        for j from 0 to n-i-2:
            if array[j] > array[j+1]:
                swap(array[j], array[j+1])
                swapped = true
        if not swapped:
            break
        """,
        "complexity": {
            "time_best": "O(n)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)"
        }
    },
    "selection_sort": {
        "name": "Selection Sort",
        "category": "Sorting",
        "ds": "array",
        "idea": "Repeatedly finds the minimum element from the unsorted part of the array and puts it at the beginning of the sorted part.",
        "pseudocode": """
function selectionSort(array):
    n = length(array)
    for i from 0 to n-1:
        minIndex = i
        for j from i+1 to n-1:
            if array[j] < array[minIndex]:
                minIndex = j
        swap(array[i], array[minIndex])
        """,
        "complexity": {
            "time_best": "O(n^2)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)"
        }
    },
    "insertion_sort": {
        "name": "Insertion Sort",
        "category": "Sorting",
        "ds": "array",
        "idea": "Builds the final sorted array one item at a time. It iterates through an input array and removes one element per iteration, finds the place it belongs in the sorted part, and inserts it there.",
        "pseudocode": """
function insertionSort(array):
    for i from 1 to length(array)-1:
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j+1] = array[j]
            j = j - 1
        array[j+1] = key
        """,
        "complexity": {
            "time_best": "O(n)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)"
        }
    },
    "merge_sort": {
        "name": "Merge Sort",
        "category": "Sorting",
        "ds": "array",
        "idea": "A 'Divide and Conquer' algorithm. It divides the array into two halves, recursively sorts them, and then merges the two sorted halves.",
        "pseudocode": """
function mergeSort(array):
    if length(array) > 1:
        mid = length(array) // 2
        Left = array[:mid]
        Right = array[mid:]

        mergeSort(Left)
        mergeSort(Right)
        
        merge(array, Left, Right)
        """,
        "complexity": {
            "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n log n)", "space": "O(n)"
        }
    },
    "quick_sort": {
        "name": "Quick Sort",
        "category": "Sorting",
        "ds": "array",
        "idea": "A 'Divide and Conquer' algorithm. It picks an element as a 'pivot' and partitions the given array around the picked pivot. All smaller elements go before the pivot, and all greater elements go after.",
        "pseudocode": """
function quickSort(array, low, high):
    if low < high:
        pivotIndex = partition(array, low, high)
        quickSort(array, low, pivotIndex - 1)
        quickSort(array, pivotIndex + 1, high)
        """,
        "complexity": {
            "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n^2)", "space": "O(log n)"
        }
    },
    # =================================================================
    # 3. GRAPH ALGORITHMS
    # =================================================================
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "category": "Graph Traversal",
        "ds": "graph",
        "idea": "Explore a graph level by level. It starts at a selected node and explores all of its neighbors at the present depth prior to moving on to the nodes at the next depth level.",
        "pseudocode": """
function BFS(graph, start):
    queue = [start]
    visited = {start}
    while queue is not empty:
        node = queue.dequeue()
        process(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
        """,
        "complexity": {
            "time_best": "O(V + E)", "time_avg": "O(V + E)", "time_worst": "O(V + E)", "space": "O(V)"
        }
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "category": "Graph Traversal",
        "ds": "graph",
        "idea": "Explore a graph by going as deep as possible along each branch before backtracking. It uses a stack (or recursion) to keep track of the path.",
        "pseudocode": """
function DFS(graph, start):
    stack = [start]
    visited = {}
    while stack is not empty:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            process(node)
            for neighbor in reversed(graph[node]):
                stack.push(neighbor)
        """,
        "complexity": {
            "time_best": "O(V + E)", "time_avg": "O(V + E)", "time_worst": "O(V + E)", "space": "O(V)"
        }
    },
    "dijkstra": {
        "name": "Dijkstra's Algorithm",
        "category": "Shortest Path",
        "ds": "graph",
        "idea": "Finds the shortest path between nodes in a weighted graph with non-negative edge weights. It works by maintaining a set of visited nodes and progressively finding the closest unvisited node.",
        "pseudocode": """
function dijkstra(graph, source):
    dist = map of {vertex: infinity}
    dist[source] = 0
    pq = priorityQueue with all vertices
    
    while pq is not empty:
        u = pq.extract_min()
        for each neighbor v of u:
            alt = dist[u] + weight(u, v)
            if alt < dist[v]:
                dist[v] = alt
                pq.decrease_priority(v, alt)
    return dist
        """,
        "complexity": {
            "time_best": "O(E + V log V)", "time_avg": "O(E + V log V)", "time_worst": "O(E + V log V)", "space": "O(V)"
        }
    },
    # =================================================================
    # 4. TREE ALGORITHMS
    # =================================================================
     "bst_build": {
        "name": "BST Build",
        "category": "Tree Operations",
        "ds": "tree",
        "idea": "Build a Binary Search Tree by inserting elements one by one. For each new element, traverse from the root to find its correct position based on comparisons.",
        "pseudocode": """
function buildBST(values):
    tree = new Tree()
    for value in values:
        tree.insert(value)

function insert(node, value):
    if value < node.value:
        if node.left is null:
            node.left = new Node(value)
        else:
            insert(node.left, value)
    else:
        if node.right is null:
            node.right = new Node(value)
        else:
            insert(node.right, value)
        """,
        "complexity": {
            "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n^2)", "space": "O(n)"
        }
    },
    # =================================================================
    # 5. DYNAMIC PROGRAMMING
    # =================================================================
    "fib_dp": {
        "name": "Fibonacci (Dynamic Prog.)",
        "category": "Dynamic Programming",
        "ds": "conceptual",
        "idea": "Calculates Fibonacci numbers efficiently by storing the results of subproblems (memoization) to avoid redundant calculations, transforming an exponential problem into a linear one.",
        "pseudocode": """
memo = {}
function fib(n):
    if n in memo: return memo[n]
    if n <= 1: return n
    
    result = fib(n-1) + fib(n-2)
    memo[n] = result
    return result
        """,
        "complexity": {
            "time_best": "O(n)", "time_avg": "O(n)", "time_worst": "O(n)", "space": "O(n)"
        }
    },
    "knapsack_01": {
        "name": "0/1 Knapsack",
        "category": "Dynamic Programming",
        "ds": "conceptual",
        "idea": "Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible. Items are indivisible.",
        "pseudocode": """
function knapsack(W, weights, values, n):
    dp = 2D array of size (n+1) x (W+1)
    for i from 0 to n:
        for w from 0 to W:
            if i==0 or w==0:
                dp[i][w] = 0
            else if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w-weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]
        """,
        "complexity": {
            "time_best": "O(n*W)", "time_avg": "O(n*W)", "time_worst": "O(n*W)", "space": "O(n*W)"
        }
    }
}

DATA_STRUCTURE_INFO = {
    "array": {
        "name": "Array",
        "description": "A collection of items stored at contiguous memory locations. Elements can be accessed randomly using indices. Its size is fixed.",
        "init_complexity": "O(n)",
        "access_complexity": "O(1)",
        "search_complexity": "O(n) (Linear), O(log n) (Binary)",
        "insertion_complexity": "O(n)",
        "deletion_complexity": "O(n)"
    },
    "string": {
        "name": "String",
        "description": "An immutable sequence of characters. It behaves much like an array of characters but cannot be modified in place.",
        "init_complexity": "O(n)",
        "access_complexity": "O(1)",
        "search_complexity": "O(n*m) (Substring search)",
        "insertion_complexity": "O(n) (Creates a new string)",
        "deletion_complexity": "O(n) (Creates a new string)"
    },
    "hashing": {
        "name": "Hash Map / Dictionary",
        "description": "A structure that maps keys to values using a hash function to compute an index into an array of buckets, from which the desired value can be found.",
        "init_complexity": "O(n) (for n items)",
        "access_complexity": "O(1) (Average), O(n) (Worst)",
        "search_complexity": "O(1) (Average), O(n) (Worst)",
        "insertion_complexity": "O(1) (Average), O(n) (Worst)",
        "deletion_complexity": "O(1) (Average), O(n) (Worst)"
    },
    "linked_list": {
        "name": "Linked List",
        "description": "A linear collection of data elements whose order is not given by their physical placement in memory. Instead, each element points to the next.",
        "init_complexity": "O(n) (for n items)",
        "access_complexity": "O(n)",
        "search_complexity": "O(n)",
        "insertion_complexity": "O(1) (at head/tail), O(n) (mid)",
        "deletion_complexity": "O(1) (at head), O(n) (mid/tail)"
    },
    "stack": {
        "name": "Stack",
        "description": "A LIFO (Last-In, First-Out) data structure. The last element added to the stack will be the first one to be removed.",
        "init_complexity": "O(n) (for n items)",
        "access_complexity": "O(n) (to find), O(1) (to peek)",
        "search_complexity": "O(n)",
        "insertion_complexity": "O(1) (Push)",
        "deletion_complexity": "O(1) (Pop)"
    },
    "queue": {
        "name": "Queue",
        "description": "A FIFO (First-In, First-Out) data structure. The first element added to the queue will be the first one to be removed.",
        "init_complexity": "O(n) (for n items)",
        "access_complexity": "O(n) (to find), O(1) (to peek)",
        "search_complexity": "O(n)",
        "insertion_complexity": "O(1) (Enqueue)",
        "deletion_complexity": "O(1) (Dequeue)"
    },
    "tree": {
        "name": "Tree (Binary Search Tree)",
        "description": "A hierarchical data structure with a root node and child nodes. In a BST, all nodes in the left subtree are smaller than the root, and all nodes in the right subtree are larger.",
        "init_complexity": "O(n log n) (Balanced), O(n^2) (Unbalanced)",
        "access_complexity": "O(log n) (Average), O(n) (Worst)",
        "search_complexity": "O(log n) (Average), O(n) (Worst)",
        "insertion_complexity": "O(log n) (Average), O(n) (Worst)",
        "deletion_complexity": "O(log n) (Average), O(n) (Worst)"
    },
    "graph": {
        "name": "Graph",
        "description": "A collection of nodes (vertices) connected by edges. Can be directed or undirected. Used to model networks and relationships.",
        "init_complexity": "O(V + E)",
        "access_complexity": "N/A (No direct access by index)",
        "search_complexity": "O(V + E) (BFS/DFS Traversal)",
        "insertion_complexity": "O(1) (Edge), O(V) (Node) for Adj. List",
        "deletion_complexity": "O(E) (Edge), O(V+E) (Node) for Adj. List"
    },
    "trie": {
        "name": "Trie (Prefix Tree)",
        "description": "A tree-like data structure that stores a dynamic set of strings, where the keys are usually strings. It is used for efficient retrieval of a key in a dataset of strings.",
        "init_complexity": "O(N*L) (N strings, avg length L)",
        "access_complexity": "O(L)",
        "search_complexity": "O(L)",
        "insertion_complexity": "O(L)",
        "deletion_complexity": "O(L)"
    }
}