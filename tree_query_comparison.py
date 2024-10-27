"""
tree_query_comparison.py

Author: Yinxuan Wu
Department: Electrical and Computer Engineering (ECE)
University: UMass Amherst
Email: yinxuan.wu.eng@gmail.com

Description:
This script compares the execution times of multiple solutions for processing tree-related queries
in binary trees. The solutions are based on the problem "2458. Height of Binary Tree After Subtree
Removal Queries" from Leetcode:
https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/description/.

In this problem, you are given the root of a binary tree and an array of queries. Each query removes
a subtree rooted at a given node, and you must return the height of the tree after performing each
query. The solutions compared here calculate the height of the tree after excluding the subtree
for each query independently.

Key Features:
- Multiple tree sizes and query counts are tested.
- Solutions benchmarked include various depth-first search (DFS)-based algorithms.
- Execution times are plotted with options for logarithmic or linear scales.
- Results are visualized using line plots, box plots, and bar charts for comparison.

Usage:
Run the script and follow the prompts to choose between multiprocessing and y-axis scale options.
"""



import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict, deque
from typing import List, Optional
from multiprocessing import Pool, Manager
import os


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Solution 1 (benchmark)
class Solution1:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        def find_parents_and_depths(node, parent, depth):
            if node:
                parent_map[node.val] = parent
                depth_map[node.val] = depth
                find_parents_and_depths(node.left, node, depth + 1)
                find_parents_and_depths(node.right, node, depth + 1)

        def find_heights(node):
            if node is None:
                return 0
            left_height = find_heights(node.left)
            right_height = find_heights(node.right)
            heights[node.val] = 1 + max(left_height, right_height)
            return heights[node.val]

        def calculate_new_height(exclude_val):
            queue = deque([(root, 0)])
            max_depth = 0
            while queue:
                current, depth = queue.popleft()
                if current.val == exclude_val:
                    continue
                max_depth = max(max_depth, depth)
                if current.left:
                    queue.append((current.left, depth + 1))
                if current.right:
                    queue.append((current.right, depth + 1))
            return max_depth

        parent_map = {}
        depth_map = {}
        heights = defaultdict(int)
        find_parents_and_depths(root, None, 0)
        find_heights(root)

        results = []
        for query in queries:
            result = calculate_new_height(query)
            results.append(result)

        return results


class Solution2:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        depth_map = {}  # Stores the depth of each node
        height_map = {}  # Stores the height of each node
        subtree_height = defaultdict(list)  # Stores heights of subtrees at each depth

        # Helper function to find depth and height of each node
        def dfs(node, depth):
            if not node:
                return -1
            depth_map[node.val] = depth
            left_height = dfs(node.left, depth + 1)
            right_height = dfs(node.right, depth + 1)
            height = 1 + max(left_height, right_height)
            height_map[node.val] = height
            subtree_height[depth].append(height)
            return height

        # Run DFS to populate depth_map, height_map, and subtree_height
        dfs(root, 0)

        # Results list to store the height of the tree after each query
        results = []

        # Process each query
        for query in queries:
            original_depth = depth_map[query]
            original_height = height_map[query]

            # Find the maximum height excluding the queried subtree
            heights_at_depth = subtree_height[original_depth]

            # Remove the current node's height from the list to calculate the new height
            heights_at_depth.remove(original_height)

            if heights_at_depth:
                max_height = max(heights_at_depth)
                new_height = max_height + original_depth
            else:
                # If no other subtree at this depth, calculate new height without this subtree
                new_height = original_depth - 1

            # Add back the original height to keep the data consistent for future queries
            heights_at_depth.append(original_height)

            results.append(new_height)

        return results


# Solution 3
class Solution3:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        depth_map = {}
        height_map = {}
        max_heights = defaultdict(lambda: [-1, -1])

        def dfs(node, depth):
            if not node:
                return -1
            depth_map[node.val] = depth
            left_height = dfs(node.left, depth + 1)
            right_height = dfs(node.right, depth + 1)
            height = 1 + max(left_height, right_height)
            height_map[node.val] = height

            if height > max_heights[depth][0]:
                max_heights[depth][1] = max_heights[depth][0]
                max_heights[depth][0] = height
            elif height > max_heights[depth][1]:
                max_heights[depth][1] = height

            return height

        dfs(root, 0)
        results = []

        for query in queries:
            original_depth = depth_map[query]
            original_height = height_map[query]

            max1, max2 = max_heights[original_depth]
            if original_height == max1:
                new_height = max2 + original_depth
            else:
                new_height = max1 + original_depth

            results.append(new_height)

        return results


class Solution4:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        from collections import defaultdict, Counter

        depth_map = {}  # Stores the depth of each node
        height_map = {}  # Stores the height of each node
        max_heights = defaultdict(lambda: [-1, -1])  # Stores the two highest heights for each depth
        height_count = defaultdict(Counter)  # Counter to keep track of heights at each depth

        # Helper function to find depth and height of each node
        def dfs(node, depth):
            if not node:
                return -1
            depth_map[node.val] = depth
            left_height = dfs(node.left, depth + 1)
            right_height = dfs(node.right, depth + 1)
            height = 1 + max(left_height, right_height)
            height_map[node.val] = height

            # Update max heights for the current depth
            if height > max_heights[depth][0]:
                max_heights[depth][1] = max_heights[depth][0]
                max_heights[depth][0] = height
            elif height > max_heights[depth][1]:
                max_heights[depth][1] = height

            # Update height counter for the current depth
            height_count[depth][height] += 1

            return height

        # Run DFS to populate depth_map, height_map, max_heights, and height_count
        dfs(root, 0)

        # Results list to store the height of the tree after each query
        results = []

        # Process each query
        for query in queries:
            original_depth = depth_map[query]
            original_height = height_map[query]

            # Determine the new height after removing the subtree rooted at 'query'
            max1, max2 = max_heights[original_depth]

            # Update height counter
            height_count[original_depth][original_height] -= 1
            if height_count[original_depth][original_height] == 0:
                del height_count[original_depth][original_height]

            if original_height == max1:
                # If the height of the removed node was the maximum at this depth
                if height_count[original_depth][max1] > 0:
                    new_height = max1 + original_depth
                else:
                    new_height = max2 + original_depth
            else:
                # If the height of the removed node was not the maximum
                new_height = max1 + original_depth

            # Add back the original height to keep the data consistent for future queries
            height_count[original_depth][original_height] += 1

            results.append(new_height)

        return results


# Function to run a single test case and return execution times for all solutions
def run_test_case(test_case, progress_queue, solutions):
    tree, queries, test_label = test_case
    tree_root = insert_level_order(tree, None, 0, len(tree))

    results = [test_label]
    # Run each solution and record the time
    for solution in solutions:
        start_time = time.time()
        solution.treeQueries(tree_root, queries)
        execution_time = time.time() - start_time
        results.append(execution_time)

    if progress_queue:
        # Send progress update if using multiprocessing
        progress_queue.put(test_label)

    return results


# Function to compare solutions with or without multiprocessing
def compare_solutions(y_scale='log', use_multiprocessing=True, solutions=None):
    if solutions is None:
        solutions = [Solution2(), Solution3(), Solution4()]  # Default solutions for testing
    n_values = [100, 1000, 5000, 10000, 50000, 100000, 500000]  # Different tree sizes
    m_values = [10, 100, 500, 1000, 5000, 10000, 50000]  # Different number of queries
    test_cases = []
    labels = []
    # Generate test cases
    for n in n_values:
        for m in m_values:
            if m > n - 1:
                continue
            # Generate a random test case
            tree, queries = generate_test_case(n, m)
            test_label = f"n={n}, m={m}"
            test_cases.append((tree, queries, test_label))
            labels.append(test_label)
    # Print information about generated test cases
    print("Generated test cases:")
    for idx, test_case in enumerate(test_cases):
        print(
            f"Test case {idx + 1}: "
            f"Tree size = {test_case[2].split(',')[0].split('=')[1]}, "
            f"Queries = {test_case[2].split(',')[1].split('=')[1]}")
    if use_multiprocessing:
        num_test_cases = len(test_cases)
        num_processes = os.cpu_count()
        # Print process-related information
        print(f"\nNumber of available CPU cores: {num_processes}")
        print(f"Total number of test cases to be run: {num_test_cases}")
        print("Test cases will be distributed among the processes as follows:")
        for idx, test_case in enumerate(test_cases):
            print(f"Process {idx % num_processes} will handle test case: {test_case[2]}")
        with Manager() as manager:
            progress_queue = manager.Queue()
            # Start multiprocessing pool
            with Pool(num_processes) as pool:
                async_results = [
                    pool.apply_async(run_test_case, args=(test_case, progress_queue, solutions)) for test_case
                    in test_cases]
                # Track progress
                completed = 0
                while completed < len(test_cases):
                    label = progress_queue.get()
                    completed += 1
                    print(f"Progress: {completed}/{len(test_cases)} test cases completed. Last completed: {label}")
                # Collect results from all workers
                results = [res.get() for res in async_results]
    else:
        # Run sequentially and track progress
        results = []
        total_test_cases = len(test_cases)
        for idx, test_case in enumerate(test_cases):
            # Run the test case
            result = run_test_case(test_case, None, solutions)
            results.append(result)
            # Print progress after each test case
            print(f"Progress: {idx + 1}/{total_test_cases} test cases executed. Last completed: {test_case[2]}")

    # Separate out the results for visualization
    labels, *execution_times = zip(*results)
    # Prepare for visualization
    solution_names = [sol.__class__.__name__ for sol in solutions]

    # Visualization 1: Enhanced Line Plot comparing execution times
    plt.figure(figsize=(12, 6))
    colors = ['blue', 'green', 'red', 'orange']  # Define colors for each solution
    markers = ['o', 's', '^', 'D']  # Define markers for each solution
    line_styles = ['-', '--', '-.', ':']  # Define line styles for each solution
    for idx, times in enumerate(execution_times):
        plt.plot(labels, times, label=f"{solution_names[idx]}",
                 color=colors[idx], marker=markers[idx], linestyle=line_styles[idx])
    plt.xlabel("Test Case (Tree Size, Query Count)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time Comparison (Line Plot)")
    # Allow user to choose y-axis scale (linear or log)
    if y_scale == 'log':
        plt.yscale("log")
    else:
        plt.yscale("linear")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid(True)  # Add grid lines for better readability
    plt.tight_layout()
    plt.show()

    # Visualization 2: Box Plot for execution time spread
    plt.figure(figsize=(10, 6))
    box_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow']
    # Create box plot with custom colors
    boxprops = dict(facecolor='lightgray', color='black', linewidth=2)
    medianprops = dict(color='black', linewidth=2)
    whiskerprops = dict(color='black', linestyle='--')
    boxes = plt.boxplot(execution_times, tick_labels=solution_names, patch_artist=True,
                        boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops)
    # Set individual colors for each box
    for patch, color in zip(boxes['boxes'], box_colors):
        patch.set_facecolor(color)
    # Add a label box explaining the elements
    legend_elements = [
        mpatches.Patch(color='lightgray', label='IQR (Interquartile Range)'),
        plt.Line2D([0], [0], color='black', lw=2, label='Median'),
        plt.Line2D([0], [0], color='black', linestyle='--', label='Whiskers (1.5x IQR)'),
        plt.Line2D(
            [0], [0], color='black', marker='o', markerfacecolor='none',
            linestyle='None', markersize=5, label='Outliers')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time Spread (Box Plot)")
    if y_scale == 'log':
        plt.yscale("log")
    else:
        plt.yscale("linear")
    plt.grid(True)  # Add grid lines
    plt.tight_layout()
    plt.show()

    # Visualization 3: Bar Chart for direct comparison
    plt.figure(figsize=(16, 6))
    width = 0.25  # Width of the bars
    x = range(len(labels))
    for idx, times in enumerate(execution_times):
        plt.bar([p + width * idx for p in x], times, width=width, label=f"{solution_names[idx]}",
                 color=colors[idx], align='center')
    plt.xlabel("Test Case (Tree Size, Query Count)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time Comparison (Bar Chart)")
    if y_scale == 'log':
        plt.yscale("log")
    else:
        plt.yscale("linear")
    plt.xticks([p + width for p in x], labels, rotation=45, ha="right")
    plt.legend()
    plt.grid(True)  # Add grid lines for better readability
    plt.tight_layout()
    plt.show()


# Helper functions for test case generation
def generate_random_tree(n):
    nodes = random.sample(range(1, n + 1), n)
    root = None
    root = insert_level_order(nodes, root, 0, n)
    return root, nodes

def insert_level_order(arr, root, i, n):
    if i < n:
        temp = TreeNode(arr[i])
        root = temp
        root.left = insert_level_order(arr, root.left, 2 * i + 1, n)
        root.right = insert_level_order(arr, root.right, 2 * i + 2, n)
    return root

def generate_test_case(n, m):
    tree_root, node_values = generate_random_tree(n)
    tree_as_list = level_order_traversal(tree_root)
    queries = random.sample(node_values[1:], m)
    return tree_as_list, queries

def level_order_traversal(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val if node else None)
        if node:
            queue.append(node.left)
            queue.append(node.right)
    while result and result[-1] is None:
        result.pop()
    return result


# Run the comparison with or without multiprocessing
if __name__ == "__main__":
    use_multiprocessing = input("Use multiprocessing? (yes/no): ").strip().lower() == 'yes'
    y_scale_choice = input("Choose y-axis scale (log/linear): ").strip().lower()
    compare_solutions(y_scale=y_scale_choice, use_multiprocessing=use_multiprocessing)
