# algorithms/trees.py

def bst_build_steps(values):
    """
    Generates animation steps to build a Binary Search Tree from a list of values.
    The frontend will be responsible for calculating node positions. This function
    only provides the logical steps of comparison and insertion.
    """
    if not values:
        return [{'action': 'error', 'message': 'Cannot build a tree from an empty list.'}]
    
    steps = []
    # Use a dictionary to simulate the tree structure on the backend to track connections
    # Format: {node_value: {'left': child_value, 'right': child_value}}
    tree = {} 
    
    # First value becomes the root
    root_val = values[0]
    steps.append({
        'action': 'insert',
        'value': root_val,
        'parent': None,
        'direction': 'root',
        'message': f'Tree is empty. Inserting {root_val} as the root.'
    })
    tree[root_val] = {'left': None, 'right': None}

    # Insert remaining values
    for val in values[1:]:
        current = root_val
        parent = None
        
        while current is not None:
            parent = current
            # Step: Compare the new value with the current node
            steps.append({
                'action': 'compare',
                'value': current,
                'newValue': val,
                'message': f'Comparing new value {val} with node {current}.'
            })
            if val < current:
                # Go left
                steps.append({'action': 'traverse', 'from': parent, 'direction': 'left', 'message': f'{val} < {current}. Moving left.'})
                current = tree[current]['left']
            elif val > current:
                # Go right
                steps.append({'action': 'traverse', 'from': parent, 'direction': 'right', 'message': f'{val} > {current}. Moving right.'})
                current = tree[current]['right']
            else:
                # Value already exists
                steps.append({'action': 'duplicate', 'value': val, 'message': f'Value {val} already exists. No insertion.'})
                parent = None # Signal that no insertion should happen
                break
        
        if parent is not None:
            direction = 'left' if val < parent else 'right'
            # Step: Insert the new node
            steps.append({
                'action': 'insert',
                'value': val,
                'parent': parent,
                'direction': direction,
                'message': f'Found empty spot. Inserting {val} as the {direction} child of {parent}.'
            })
            # Update our backend tree model
            tree[val] = {'left': None, 'right': None}
            if direction == 'left':
                tree[parent]['left'] = val
            else:
                tree[parent]['right'] = val
                
    steps.append({'action': 'complete', 'message': 'BST build process complete.'})
    return steps