# algorithms/sorting.py

def bubble_sort(data):
    """
    Generates animation steps for Bubble Sort.
    Compares adjacent elements and swaps them if they are in the wrong order.
    """
    steps = []
    n = len(data)
    arr = list(data)  # Create a mutable copy to sort in-place

    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Step: Highlight the two elements being compared
            steps.append({
                'action': 'compare',
                'indices': [j, j + 1],
                'message': f'Comparing {arr[j]} and {arr[j+1]}.'
            })
            if arr[j] > arr[j + 1]:
                # Step: If they need to be swapped, show the swap
                steps.append({
                    'action': 'swap',
                    'indices': [j, j + 1],
                    'message': f'{arr[j]} > {arr[j+1]}. Swapping.'
                })
                # Perform the swap on our local copy
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Step: Mark the last element of this pass as sorted
        steps.append({
            'action': 'sorted_element',
            'indices': [n - 1 - i],
            'message': f'Element {arr[n-1-i]} is now in its final sorted position.'
        })

        # If no swaps occurred in a pass, the array is sorted
        if not swapped:
            # Mark all remaining unsorted elements as sorted
            for k in range(n - i - 1):
                 steps.append({'action': 'sorted_element', 'indices': [k]})
            break
            
    steps.append({'action': 'complete', 'message': 'Array is fully sorted.'})
    return steps

def selection_sort(data):
    """
    Generates animation steps for Selection Sort.
    Finds the minimum element and places it at the beginning.
    """
    steps = []
    n = len(data)
    arr = list(data) # Create a mutable copy

    for i in range(n):
        min_idx = i
        # Step: Highlight the start of the unsorted subarray
        steps.append({
            'action': 'highlight_min',
            'indices': [min_idx],
            'message': f'Finding the minimum in the unsorted part (from index {i}). Current minimum is {arr[min_idx]}.'
        })
        
        # Find the minimum element in the remaining unsorted array
        for j in range(i + 1, n):
            # Step: Compare current element with the current minimum
            steps.append({
                'action': 'compare',
                'indices': [j, min_idx],
                'message': f'Comparing {arr[j]} with current minimum {arr[min_idx]}.'
            })
            if arr[j] < arr[min_idx]:
                # Step: Found a new minimum
                old_min_idx = min_idx
                min_idx = j
                steps.append({
                    'action': 'highlight_min',
                    'indices': [min_idx],
                    'message': f'Found a new minimum: {arr[min_idx]}.'
                })
        
        # Step: Swap the found minimum element with the first element of the unsorted part
        steps.append({
            'action': 'swap',
            'indices': [i, min_idx],
            'message': f'Swapping minimum element {arr[min_idx]} with element at index {i} ({arr[i]}).'
        })
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
        # Step: Mark the element at index i as sorted
        steps.append({
            'action': 'sorted_element',
            'indices': [i],
            'message': f'Element {arr[i]} is now in its final sorted position.'
        })

    steps.append({'action': 'complete', 'message': 'Array is fully sorted.'})
    return steps


def insertion_sort(data):
    """Generates animation steps for Insertion Sort."""
    steps = []
    arr = list(data)
    for i in range(1, len(arr)):
        key = arr[i]
        steps.append({'action': 'highlight_key', 'index': i, 'key': key, 'message': f'Selecting {key} as the key to insert.'})
        j = i - 1
        while j >= 0 and key < arr[j]:
            steps.append({'action': 'compare_shift', 'indices': [j, j+1], 'message': f'{key} < {arr[j]}. Shifting {arr[j]} to the right.'})
            arr[j + 1] = arr[j]
            steps.append({'action': 'shift_right', 'from': j, 'to': j + 1, 'value': arr[j]})
            j -= 1
        arr[j + 1] = key
        steps.append({'action': 'insert_key', 'index': j + 1, 'key': key, 'message': f'Inserting key {key} at position {j+1}.'})

    steps.append({'action': 'complete', 'message': 'Array is fully sorted.'})
    return steps

def merge_sort(data):
    """Generates animation steps for Merge Sort."""
    steps = []
    arr = list(data)

    def _merge_sort_recursive(sub_array, offset):
        if len(sub_array) > 1:
            mid = len(sub_array) // 2
            left_half = sub_array[:mid]
            right_half = sub_array[mid:]
            
            steps.append({'action': 'divide', 'range': (offset, offset + len(sub_array) - 1), 'mid': offset + mid, 'message': f'Dividing array at index {offset+mid}.'})
            
            _merge_sort_recursive(left_half, offset)
            _merge_sort_recursive(right_half, offset + mid)

            i = j = k = 0
            steps.append({'action': 'merge_start', 'range': (offset, offset + len(sub_array) - 1), 'message': f'Merging subarrays.'})
            
            # Merging
            while i < len(left_half) and j < len(right_half):
                steps.append({'action': 'merge_compare', 'left_index': offset + i, 'right_index': offset + mid + j})
                if left_half[i] < right_half[j]:
                    sub_array[k] = left_half[i]
                    i += 1
                else:
                    sub_array[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                sub_array[k] = left_half[i]
                i += 1
                k += 1
            while j < len(right_half):
                sub_array[k] = right_half[j]
                j += 1
                k += 1

            # Update the main array visualization
            steps.append({'action': 'update_range', 'range_start': offset, 'values': sub_array, 'message': 'Subarray sorted and merged.'})

    _merge_sort_recursive(arr, 0)
    steps.append({'action': 'complete', 'message': 'Array is fully sorted.'})
    return steps

def quick_sort(data):
    """Generates animation steps for Quick Sort."""
    steps = []
    arr = list(data)

    def _partition(low, high):
        pivot = arr[high]
        steps.append({'action': 'pivot', 'index': high, 'message': f'Choosing {pivot} as pivot for range [{low}, {high}].'})
        i = low - 1
        for j in range(low, high):
            steps.append({'action': 'compare', 'indices': [j, high], 'message': f'Comparing {arr[j]} with pivot {pivot}.'})
            if arr[j] < pivot:
                i += 1
                steps.append({'action': 'swap', 'indices': [i, j], 'message': f'{arr[j]} < {pivot}. Swapping {arr[i]} and {arr[j]}.'})
                arr[i], arr[j] = arr[j], arr[i]
        
        steps.append({'action': 'swap', 'indices': [i + 1, high], 'message': f'Placing pivot. Swapping {arr[i+1]} and {arr[high]}.'})
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append({'action': 'sorted_element', 'indices': [i + 1]})
        return i + 1

    def _quick_sort_recursive(low, high):
        if low < high:
            pi = _partition(low, high)
            _quick_sort_recursive(low, pi - 1)
            _quick_sort_recursive(pi + 1, high)

    _quick_sort_recursive(0, len(arr) - 1)
    steps.append({'action': 'complete', 'message': 'Array is fully sorted.'})
    return steps