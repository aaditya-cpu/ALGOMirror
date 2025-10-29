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

def jump_search(data, target):
    """Generates animation steps for Jump Search."""
    steps = []
    n = len(data)
    step = int(math.sqrt(n))
    prev = 0

    if not all(data[i] <= data[i+1] for i in range(len(data)-1)):
        steps.append({'action': 'error', 'message': 'Error: Jump Search requires a sorted array!'})
        return steps

    steps.append({'action': 'message', 'message': f'Block size (step) is √{n} ≈ {step}.'})

    # Jumping ahead in blocks
    while data[min(step, n) - 1] < target:
        steps.append({'action': 'compare_block', 'indices': list(range(prev, min(step, n))), 'message': f'Comparing target with end of block [{prev}...{min(step,n)-1}]. {data[min(step, n) - 1]} < {target}. Jumping.'})
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            steps.append({'action': 'not_found', 'message': 'Target is larger than all elements.'})
            return steps

    steps.append({'action': 'message', 'message': f'Target may be in block [{prev}...{min(step,n)-1}]. Starting linear search.'})

    # Linear search within the identified block
    for i in range(prev, min(step, n)):
        steps.append({'action': 'compare', 'indices': [i], 'message': f'Comparing target ({target}) with array[{i}] ({data[i]})'})
        if data[i] == target:
            steps.append({'action': 'found', 'indices': [i], 'message': f'Target {target} found at index {i}!'})
            return steps

    steps.append({'action': 'not_found', 'message': f'Target {target} not found in the array.'})
    return steps

def interpolation_search(data, target):
    """Generates animation steps for Interpolation Search."""
    steps = []
    low, high = 0, len(data) - 1

    if not all(data[i] <= data[i+1] for i in range(len(data)-1)):
        steps.append({'action': 'error', 'message': 'Error: Interpolation Search requires a sorted array!'})
        return steps

    while low <= high and data[low] <= target <= data[high]:
        if low == high:
            if data[low] == target:
                steps.append({'action': 'found', 'indices': [low], 'message': f'Target found at index {low}.'})
            else:
                steps.append({'action': 'not_found', 'message': 'Target not found.'})
            return steps

        # Probing the position with interpolation formula
        pos = low + int(((float(high - low) / (data[high] - data[low])) * (target - data[low])))
        steps.append({'action': 'probe', 'index': pos, 'message': f'Probing position {pos} based on data distribution.'})
        steps.append({'action': 'compare', 'indices': [pos], 'message': f'Comparing target ({target}) with array[{pos}] ({data[pos]})'})

        if data[pos] == target:
            steps.append({'action': 'found', 'indices': [pos], 'message': f'Target {target} found at index {pos}!'})
            return steps
        if data[pos] < target:
            low = pos + 1
            steps.append({'action': 'eliminate', 'range': (0, pos), 'message': f'Target is larger. New search range is [{low}, {high}].'})
        else:
            high = pos - 1
            steps.append({'action': 'eliminate', 'range': (pos, len(data)-1), 'message': f'Target is smaller. New search range is [{low}, {high}].'})
            
    steps.append({'action': 'not_found', 'message': f'Target {target} not found.'})
    return steps