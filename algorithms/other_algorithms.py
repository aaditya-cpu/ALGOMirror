# algorithms/other_algorithms.py

# =================================================================
# DYNAMIC PROGRAMMING ALGORITHMS
# =================================================================

def fib_dp_steps(n):
    """
    Generates steps to visualize Fibonacci calculation using memoization (Dynamic Programming).
    This visualization focuses on the recursion tree and the memoization table.
    """
    if n > 12: # Limit input to prevent extremely long animations
        return [{'action': 'error', 'message': 'Input is too large for animation. Please choose a number <= 12.'}]

    steps = []
    memo = {}
    call_id_counter = 0

    def _fib_recursive(num, parent_id):
        nonlocal call_id_counter
        current_id = call_id_counter
        call_id_counter += 1

        steps.append({'action': 'call', 'id': current_id, 'parent_id': parent_id, 'n': num, 'message': f'Calling fib({num}).'})
        steps.append({'action': 'check_memo', 'id': current_id, 'n': num, 'memo_state': dict(memo), 'message': f'Is fib({num}) in memo table?'})
        
        if num in memo:
            steps.append({'action': 'memo_hit', 'id': current_id, 'n': num, 'value': memo[num], 'message': f'Yes! fib({num}) = {memo[num]}. Returning stored value.'})
            return memo[num]
        
        if num <= 1:
            steps.append({'action': 'base_case', 'id': current_id, 'n': num, 'value': num, 'message': f'Base case reached. fib({num}) = {num}.'})
            memo[num] = num
            steps.append({'action': 'store_memo', 'id': current_id, 'n': num, 'value': num, 'memo_state': dict(memo), 'message': f'Storing result fib({num}) = {num} in memo.'})
            return num

        res1 = _fib_recursive(num - 1, current_id)
        res2 = _fib_recursive(num - 2, current_id)
        result = res1 + res2
        
        steps.append({'action': 'calculate', 'id': current_id, 'n': num, 'val1': res1, 'val2': res2, 'result': result, 'message': f'Calculating fib({num}) = {res1} + {res2} = {result}.'})
        memo[num] = result
        steps.append({'action': 'store_memo', 'id': current_id, 'n': num, 'value': result, 'memo_state': dict(memo), 'message': f'Storing result fib({num}) = {result} in memo.'})
        return result

    final_result = _fib_recursive(n, parent_id=None)
    steps.append({'action': 'complete', 'result': final_result, 'message': f'Final result for fib({n}) is {final_result}.'})
    return steps

def knapsack_01_steps(capacity, items):
    """
    Generates steps for the 0/1 Knapsack problem using Dynamic Programming.
    `items` is a list of dicts: [{'weight': w, 'value': v}]
    """
    weights = [item['weight'] for item in items]
    values = [item['value'] for item in items]
    steps = []
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    steps.append({'action': 'init_table', 'rows': n + 1, 'cols': capacity + 1, 'weights': weights, 'values': values, 'message': 'Initializing DP table for Knapsack problem.'})

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            item_index = i - 1
            item_weight = weights[item_index]
            item_value = values[item_index]

            steps.append({'action': 'highlight_cell', 'cell': (i, w), 'message': f'Calculating value for item {i} (w:{item_weight}, v:{item_value}) at capacity {w}.'})

            if item_weight > w:
                dp[i][w] = dp[i-1][w]
                steps.append({'action': 'copy_above', 'from_cell': (i-1, w), 'to_cell': (i, w), 'value': dp[i][w], 'message': f'Item {i} is too heavy. Value is same as above: {dp[i][w]}.'})
            else:
                value_without_item = dp[i-1][w]
                value_with_item = item_value + dp[i-1][w - item_weight]
                dp[i][w] = max(value_with_item, value_without_item)
                
                steps.append({'action': 'compare_options', 'cell': (i, w), 'option_without': {'cell': (i-1, w), 'value': value_without_item}, 'option_with': {'cell': (i-1, w - item_weight), 'value': value_with_item, 'item_value': item_value}, 'result': dp[i][w], 'message': f'Choose max between excluding ({value_without_item}) and including ({value_with_item}). Max is {dp[i][w]}.'})

    final_value = dp[n][capacity]
    steps.append({'action': 'complete', 'result': final_value, 'final_cell': (n, capacity), 'message': f'Knapsack calculation complete. Maximum value is {final_value}.'})
    return steps


# =================================================================
# GREEDY ALGORITHMS
# =================================================================

def fractional_knapsack_steps(capacity, items):
    """
    Generates steps for the Fractional Knapsack problem using a Greedy approach.
    `items` is a list of dicts: [{'weight': w, 'value': v, 'id': i}]
    """
    steps = []
    
    # Step 1: Calculate value-to-weight ratio for each item
    for item in items:
        item['ratio'] = item['value'] / item['weight']
    steps.append({'action': 'calculate_ratios', 'items': list(items), 'message': 'Calculated value-to-weight ratio for each item.'})
    
    # Step 2: Sort items by ratio in descending order
    items.sort(key=lambda x: x['ratio'], reverse=True)
    steps.append({'action': 'sort_items', 'items': list(items), 'message': 'Sorted items by ratio in descending order.'})
    
    total_value = 0
    current_capacity = capacity
    
    for item in items:
        steps.append({'action': 'select_item', 'item_id': item['id'], 'message': f"Considering item {item['id']} (w:{item['weight']}, v:{item['value']})"})
        
        if current_capacity == 0:
            steps.append({'action': 'knapsack_full', 'item_id': item['id'], 'message': 'Knapsack is full. Cannot add more items.'})
            break
            
        if item['weight'] <= current_capacity:
            # Take the whole item
            current_capacity -= item['weight']
            total_value += item['value']
            steps.append({'action': 'take_whole', 'item_id': item['id'], 'capacity_left': current_capacity, 'total_value': total_value, 'message': f"Took all of item {item['id']}. Capacity left: {current_capacity:.2f}."})
        else:
            # Take a fraction of the item
            fraction = current_capacity / item['weight']
            value_taken = item['value'] * fraction
            total_value += value_taken
            current_capacity = 0
            steps.append({'action': 'take_fraction', 'item_id': item['id'], 'fraction': fraction, 'capacity_left': 0, 'total_value': total_value, 'message': f"Took {fraction*100:.1f}% of item {item['id']}. Knapsack is now full."})

    steps.append({'action': 'complete', 'result': total_value, 'message': f'Greedy knapsack complete. Total value is {total_value:.2f}.'})
    return steps


# =================================================================
# RECURSIVE ALGORITHMS
# =================================================================

def hanoi_steps(n_disks):
    """
    Generates steps for solving the Tower of Hanoi puzzle.
    """
    if n_disks > 6: # Limit for animation sanity
        return [{'action': 'error', 'message': 'Too many disks for animation. Please choose 6 or fewer.'}]
        
    steps = []
    # Initial state of the towers
    towers = {'A': list(range(n_disks, 0, -1)), 'B': [], 'C': []}

    def _hanoi_recursive(n, source, target, auxiliary):
        if n > 0:
            # Move n-1 disks from source to auxiliary
            _hanoi_recursive(n - 1, source, auxiliary, target)
            
            # Move the nth disk from source to target
            disk_to_move = towers[source].pop()
            towers[target].append(disk_to_move)
            
            steps.append({
                'action': 'move_disk',
                'disk_id': disk_to_move,
                'from_peg': source,
                'to_peg': target,
                'towers_state': {k: list(v) for k, v in towers.items()}, # Deep copy
                'message': f'Move disk {disk_to_move} from {source} to {target}.'
            })
            
            # Move the n-1 disks from auxiliary to target
            _hanoi_recursive(n - 1, auxiliary, target, source)

    _hanoi_recursive(n_disks, 'A', 'C', 'B')
    steps.append({'action': 'complete', 'message': 'Tower of Hanoi puzzle solved!'})
    return steps


# =================================================================
# BITWISE ALGORITHMS
# =================================================================

def bitwise_swap_steps(a, b):
    """
    Generates steps to visualize swapping two numbers using XOR.
    """
    steps = []
    
    # Helper to format binary strings to a consistent length
    def bin_format(n):
        return format(n, '08b')

    steps.append({'action': 'initial_state', 'a': a, 'b': b, 'bin_a': bin_format(a), 'bin_b': bin_format(b), 'message': 'Initial values.'})
    
    # Step 1: a = a ^ b
    result1 = a ^ b
    steps.append({'action': 'xor_operation', 'var1': 'a', 'val1': a, 'bin1': bin_format(a), 'var2': 'b', 'val2': b, 'bin2': bin_format(b), 'result_var': 'a', 'result_val': result1, 'result_bin': bin_format(result1), 'message': f'Step 1: a = a XOR b ({a} ^ {b}) = {result1}'})
    a = result1
    
    # Step 2: b = a ^ b
    result2 = a ^ b
    steps.append({'action': 'xor_operation', 'var1': 'a', 'val1': a, 'bin1': bin_format(a), 'var2': 'b', 'val2': b, 'bin2': bin_format(b), 'result_var': 'b', 'result_val': result2, 'result_bin': bin_format(result2), 'message': f'Step 2: b = a XOR b ({a} ^ {b}) = {result2}'})
    b = result2

    # Step 3: a = a ^ b
    result3 = a ^ b
    steps.append({'action': 'xor_operation', 'var1': 'a', 'val1': a, 'bin1': bin_format(a), 'var2': 'b', 'val2': b, 'bin2': bin_format(b), 'result_var': 'a', 'result_val': result3, 'result_bin': bin_format(result3), 'message': f'Step 3: a = a XOR b ({a} ^ {b}) = {result3}'})
    a = result3

    steps.append({'action': 'final_state', 'a': a, 'b': b, 'bin_a': bin_format(a), 'bin_b': bin_format(b), 'message': 'Swap complete. Final values.'})
    return steps


def count_set_bits_steps(n):
    """
    Generates steps to visualize counting set bits (1s) in a number's binary representation.
    """
    steps = []
    
    def bin_format(num):
        return format(num, '08b')

    count = 0
    current_n = n

    steps.append({'action': 'initial_state', 'n': n, 'bin_n': bin_format(n), 'count': count, 'message': f'Counting set bits for {n}.'})

    while current_n > 0:
        # Check the last bit
        last_bit = current_n & 1
        steps.append({'action': 'check_last_bit', 'n': current_n, 'bin_n': bin_format(current_n), 'last_bit': last_bit, 'message': f'Checking the last bit of {current_n}. It is {last_bit}.'})
        
        if last_bit == 1:
            count += 1
            steps.append({'action': 'increment_count', 'count': count, 'message': 'Bit is 1. Incrementing count.'})

        # Right shift
        shifted_n = current_n >> 1
        steps.append({'action': 'right_shift', 'n_before': current_n, 'bin_before': bin_format(current_n), 'n_after': shifted_n, 'bin_after': bin_format(shifted_n), 'message': f'Right-shifting {current_n} to get {shifted_n}.'})
        current_n = shifted_n

    steps.append({'action': 'complete', 'result': count, 'n': n, 'message': f'Finished. The number of set bits in {n} is {count}.'})
    return steps