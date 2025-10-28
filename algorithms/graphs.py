# algorithms/graphs.py
from collections import deque

def bfs(graph_data, start_node):
    """
    Generates animation steps for Breadth-First Search.
    Uses a queue to explore level by level.
    """
    # Validate that the start node exists in the graph
    if start_node not in graph_data['adjacency_list']:
        return [{'action': 'error', 'message': f'Start node "{start_node}" not in graph.'}]

    steps = []
    queue = deque([start_node])
    visited = {start_node}
    
    # Step: Initial state
    steps.append({
        'action': 'enqueue',
        'node': start_node,
        'queue_state': list(queue),
        'message': f'Starting BFS at node {start_node}. Add it to the queue.'
    })

    while queue:
        node = queue.popleft()
        # Step: Dequeue a node to visit it
        steps.append({
            'action': 'dequeue',
            'node': node,
            'queue_state': list(queue),
            'message': f'Dequeueing and visiting node {node}.'
        })
        
        # Explore neighbors of the current node
        for neighbor in sorted(graph_data['adjacency_list'].get(node, [])): # Sorted for consistency
            # Step: Show which edge is being checked
            steps.append({
                'action': 'explore_edge',
                'from': node,
                'to': neighbor,
                'message': f'Exploring edge from {node} to {neighbor}.'
            })
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                # Step: Enqueue an unvisited neighbor
                steps.append({
                    'action': 'enqueue',
                    'node': neighbor,
                    'queue_state': list(queue),
                    'message': f'Node {neighbor} is unvisited. Add to queue.'
                })
            else:
                # Step: Note that the neighbor has already been visited
                 steps.append({
                    'action': 'neighbor_visited',
                    'node': neighbor,
                    'message': f'Node {neighbor} has already been visited. Skipping.'
                 })
    
    steps.append({'action': 'complete', 'message': 'BFS complete. All reachable nodes visited.'})
    return steps


def dfs(graph_data, start_node):
    """
    Generates animation steps for Depth-First Search (iterative version).
    Uses a stack to explore as deep as possible before backtracking.
    """
    if start_node not in graph_data['adjacency_list']:
        return [{'action': 'error', 'message': f'Start node "{start_node}" not in graph.'}]
        
    steps = []
    stack = [start_node]
    visited = set()

    # Step: Initial state
    steps.append({
        'action': 'push',
        'node': start_node,
        'stack_state': list(stack),
        'message': f'Starting DFS at node {start_node}. Push it to the stack.'
    })
    
    while stack:
        node = stack.pop()
        
        # Step: Show the node being popped for consideration
        steps.append({
            'action': 'pop',
            'node': node,
            'stack_state': list(stack),
            'message': f'Popping node {node} from the stack to visit.'
        })
        
        if node in visited:
            # Step: If already visited, skip it
            steps.append({
                'action': 'skip_visited',
                'node': node,
                'message': f'Node {node} already visited. Skipping.'
            })
            continue

        visited.add(node)
        # Step: Mark the node as visited
        steps.append({
            'action': 'visit_node',
            'node': node,
            'message': f'Visiting node {node} for the first time.'
        })
        
        # Add neighbors to the stack. We sort and reverse so they are processed alphabetically.
        neighbors = sorted(graph_data['adjacency_list'].get(node, []), reverse=True)
        for neighbor in neighbors:
            # Step: Explore edge and push unvisited neighbors to the stack
            steps.append({
                'action': 'explore_edge',
                'from': node,
                'to': neighbor,
                'message': f'Checking neighbor {neighbor} of {node}.'
            })
            if neighbor not in visited:
                stack.append(neighbor)
                steps.append({
                    'action': 'push',
                    'node': neighbor,
                    'stack_state': list(stack),
                    'message': f'Pushing unvisited neighbor {neighbor} to stack.'
                })

    steps.append({'action': 'complete', 'message': 'DFS complete. All reachable nodes visited.'})
    return steps