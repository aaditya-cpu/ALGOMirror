# algorithms/searching.py

import math

def linear_search(data, target):
    """
    Generates animation steps for Linear Search.
    Iterates through each element one by one.
    """
    steps = []
    for i, value in enumerate(data):
        # Step: Highlight the element being compared
        steps.append({
            'action': 'compare',
            'indices': [i],
            'message': f'Comparing target ({target}) with array[{i}] which is {value}.'
        })
        if value == target:
            # Step: Highlight the found element and terminate
            steps.append({
                'action': 'found',
                'indices': [i],
                'message': f'Target {target} found at index {i}!'
            })
            return steps # Exit early once found

    # Step: If the loop completes, the target was not found
    steps.append({
        'action': 'not_found',
        'message': f'Target {target} not found in the array.'
    })
    return steps

def binary_search(data, target):
    """
    Generates animation steps for Binary Search.
    Requires the input array to be sorted.
    """
    steps = []
    
    # Pre-computation check: Ensure the array is sorted before starting
    if not all(data[i] <= data[i+1] for i in range(len(data)-1)):
        steps.append({
            'action': 'error',
            'message': 'Error: Binary Search requires a sorted array!'
        })
        return steps

    low, high = 0, len(data) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        # Step: Show the current search boundaries (low, high) and the middle point
        steps.append({
            'action': 'highlight_pointers',
            'pointers': {'low': low, 'high': high, 'mid': mid},
            'message': f'Searching in range [{low}, {high}]. Middle is at index {mid}.'
        })
        
        # Step: Compare the target with the middle element
        steps.append({
            'action': 'compare',
            'indices': [mid],
            'message': f'Comparing target ({target}) with array[{mid}] which is {data[mid]}.'
        })
        
        if data[mid] == target:
            # Step: Target found
            steps.append({
                'action': 'found',
                'indices': [mid],
                'message': f'Target {target} found at index {mid}!'
            })
            return steps
        elif data[mid] < target:
            # Step: Eliminate the left half
            steps.append({
                'action': 'eliminate',
                'range': (low, mid),
                'message': f'Target ({target}) > {data[mid]}. Discarding the left half.'
            })
            low = mid + 1
        else:
            # Step: Eliminate the right half
            steps.append({
                'action': 'eliminate',
                'range': (mid, high),
                'message': f'Target ({target}) < {data[mid]}. Discarding the right half.'
            })
            high = mid - 1
            
    # Step: If the loop finishes, the target was not found
    steps.append({
        'action': 'not_found',
        'message': f'Target {target} not found in the array.'
    })
    return steps