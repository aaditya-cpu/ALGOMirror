# content.py (FINAL, COMPLETE, AND VALIDATED)

ALGORITHM_CONTENT = {
    # 1. SEARCHING ALGORITHMS
    "linear_search": {
        "name": "Linear Search", "category": "Searching", "ds": "array",
        "idea": "Check each element one by one from the beginning.",
        "pseudocode": """function linearSearch(array, target):
    for i from 0 to length(array) - 1:
        if array[i] == target:
            return i
    return -1""",
        "complexity": { "time_best": "O(1)", "time_avg": "O(n)", "time_worst": "O(n)", "space": "O(1)" }
    },
    "binary_search": {
        "name": "Binary Search", "category": "Searching", "ds": "array",
        "idea": "Efficiently find an item in a sorted array by repeatedly dividing the search interval in half.",
        "pseudocode": """function binarySearch(array, target):
    low = 0
    high = length(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if array[mid] == target:
            return mid
        else if array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1""",
        "complexity": { "time_best": "O(1)", "time_avg": "O(log n)", "time_worst": "O(log n)", "space": "O(1)" }
    },
    "jump_search": {
        "name": "Jump Search", "category": "Searching", "ds": "array",
        "idea": "Hop through a sorted array in fixed steps, then perform a linear search in the identified block.",
        "pseudocode": """function jumpSearch(array, target):
    step = √(length(array))
    prev = 0
    while array[min(step, length(array)) - 1] < target:
        prev = step
        step += √(length(array))
        if prev >= length(array):
            return -1
    for i from prev to min(step, length(array)):
        if array[i] == target:
            return i
    return -1""",
        "complexity": { "time_best": "O(1)", "time_avg": "O(√n)", "time_worst": "O(√n)", "space": "O(1)" }
    },
    "interpolation_search": {
        "name": "Interpolation Search", "category": "Searching", "ds": "array",
        "idea": "An improvement over Binary Search for uniformly distributed data by probing positions.",
        "pseudocode": """function interpolationSearch(array, target):
    low = 0
    high = length(array) - 1
    while low <= high and target >= array[low] and target <= array[high]:
        pos = low + ((target - array[low]) * (high - low)) / (array[high] - array[low])
        if array[pos] == target:
            return pos
        if array[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1""",
        "complexity": { "time_best": "O(1)", "time_avg": "O(log log n)", "time_worst": "O(n)", "space": "O(1)" }
    },
    
    # 2. SORTING ALGORITHMS
    "bubble_sort": {
        "name": "Bubble Sort", "category": "Sorting", "ds": "array",
        "idea": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
        "pseudocode": """function bubbleSort(array):
    for i from 0 to length(array)-1:
        for j from 0 to length(array)-i-1:
            if array[j] > array[j+1]:
                swap(array[j], array[j+1])""",
        "complexity": { "time_best": "O(n)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)" }
    },
    "selection_sort": {
        "name": "Selection Sort", "category": "Sorting", "ds": "array",
        "idea": "Repeatedly finds the minimum element from the unsorted part and puts it at the beginning.",
        "pseudocode": """function selectionSort(array):
    for i from 0 to length(array)-1:
        minIndex = i
        for j from i+1 to length(array):
            if array[j] < array[minIndex]:
                minIndex = j
        swap(array[i], array[minIndex])""",
        "complexity": { "time_best": "O(n^2)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)" }
    },
    "insertion_sort": {
        "name": "Insertion Sort", "category": "Sorting", "ds": "array",
        "idea": "Builds the final sorted array one item at a time by inserting each element into its proper place.",
        "pseudocode": """function insertionSort(array):
    for i from 1 to length(array)-1:
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j+1] = array[j]
            j = j - 1
        array[j+1] = key""",
        "complexity": { "time_best": "O(n)", "time_avg": "O(n^2)", "time_worst": "O(n^2)", "space": "O(1)" }
    },
    "merge_sort": {
        "name": "Merge Sort", "category": "Sorting", "ds": "array",
        "idea": "A 'Divide and Conquer' algorithm. It divides the array into halves, recursively sorts them, and then merges them.",
        "pseudocode": """function mergeSort(array):
    if length(array) > 1:
        mid = length(array)//2
        left = array[0:mid]
        right = array[mid:]

        mergeSort(left)
        mergeSort(right)

        merge(array, left, right)""",
        "complexity": { "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n log n)", "space": "O(n)" }
    },
    "quick_sort": {
        "name": "Quick Sort", "category": "Sorting", "ds": "array",
        "idea": "A 'Divide and Conquer' algorithm that picks a 'pivot' and partitions the array around it.",
        "pseudocode": """function quickSort(array, low, high):
    if low < high:
        pivotIndex = partition(array, low, high)
        quickSort(array, low, pivotIndex - 1)
        quickSort(array, pivotIndex + 1, high)""",
        "complexity": { "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n^2)", "space": "O(log n)" }
    },
    
    # 3. GRAPH ALGORITHMS
    "bfs": {
        "name": "Breadth-First Search (BFS)", "category": "Graph Traversal", "ds": "graph",
        "idea": "Explore a graph level by level using a queue.",
        "pseudocode": """function BFS(graph, start):
    queue = [start]
    visited = {start}
    while queue not empty:
        node = dequeue(queue)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                enqueue(queue, neighbor)""",
        "complexity": { "time_best": "O(V+E)", "time_avg": "O(V+E)", "time_worst": "O(V+E)", "space": "O(V)" }
    },
    "dfs": {
        "name": "Depth-First Search (DFS)", "category": "Graph Traversal", "ds": "graph",
        "idea": "Explore a graph by going as deep as possible along each branch before backtracking, using a stack.",
        "pseudocode": """function DFS(graph, start, visited):
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            DFS(graph, neighbor, visited)""",
        "complexity": { "time_best": "O(V+E)", "time_avg": "O(V+E)", "time_worst": "O(V+E)", "space": "O(V)" }
    },
    "dijkstra": {
        "name": "Dijkstra's Algorithm", "category": "Shortest Path", "ds": "graph",
        "idea": "Finds the shortest path in a weighted graph with non-negative edge weights.",
        "pseudocode": """function dijkstra(graph, source):
    dist[source] = 0
    for vertex in graph:
        dist[vertex] = ∞
    pq = priorityQueue()
    pq.push((0, source))

    while pq not empty:
        (distance, u) = pq.pop()
        for (v, weight) in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pq.push((dist[v], v))""",
        "complexity": { "time_best": "O(E + V log V)", "time_avg": "O(E + V log V)", "time_worst": "O(E + V log V)", "space": "O(V)" }
    },

    # 4. TREE ALGORITHMS
    "bst_build": {
        "name": "BST Build", "category": "Tree Operations", "ds": "tree",
        "idea": "Build a Binary Search Tree by inserting elements one by one.",
        "pseudocode": """function insert(node, value):
    if value < node.value:
        if node.left is null:
            node.left = new Node(value)
        else:
            insert(node.left, value)
    else:
        if node.right is null:
            node.right = new Node(value)
        else:
            insert(node.right, value)""",
        "complexity": { "time_best": "O(n log n)", "time_avg": "O(n log n)", "time_worst": "O(n^2)", "space": "O(n)" }
    },

    # 5. CONCEPTUAL ALGORITHMS
    "fib_dp": {
        "name": "Fibonacci (DP)", "category": "Dynamic Programming", "ds": "conceptual",
        "idea": "Calculates Fibonacci numbers efficiently by storing results of subproblems (memoization).",
        "pseudocode": """function fib(n, memo):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]""",
        "complexity": { "time_best": "O(n)", "time_avg": "O(n)", "time_worst": "O(n)", "space": "O(n)" }
    }
}

DATA_STRUCTURE_INFO = {
    "array": { "name": "Array", "description": "A collection of items stored at contiguous memory locations." },
    "tree": { "name": "Tree (BST)", "description": "A hierarchical data structure with a root node and child nodes." },
    "graph": { "name": "Graph", "description": "A collection of nodes (vertices) connected by edges." },
    "conceptual": { "name": "Conceptual", "description": "Algorithms that demonstrate a concept like recursion or dynamic programming." }
}