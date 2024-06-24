import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

# # Increase the recursion limit
# sys.setrecursionlimit(1500)

def create_min_heap():
    """Create and manipulate a min heap"""
    min_heap = []
    # Push elements into the min heap
    heapq.heappush(min_heap, 10)
    heapq.heappush(min_heap, 4)
    heapq.heappush(min_heap, 7)
    heapq.heappush(min_heap, 1)

    print("Min heap:", min_heap)  # Output the min heap

    smallest = heapq.heappop(min_heap)
    print("Popped smallest element:", smallest)
    print("Heap structure:", min_heap)


def create_max_heap():
    """Create and manipulate a max heap"""
    max_heap = []
    # Push elements into the max heap (store negative values)
    heapq.heappush(max_heap, -10)
    heapq.heappush(max_heap, -4)
    heapq.heappush(max_heap, -7)
    heapq.heappush(max_heap, -1)
    print("Max heap (stored as negative values):", max_heap)
    largest = -heapq.heappop(max_heap)
    print("Popped largest element:", largest)
    print("Heap structure (stored as negative values):", max_heap)
    # Convert back to positive for display purposes
    display_heap = [-x for x in max_heap]
    print("Max heap (stored as negative values):", display_heap)
    largest = -heapq.heappop(max_heap)
    print("Popped largest element:", largest)
    display_heap = [-x for x in max_heap]
    print("Heap structure (stored as negative values):",
          display_heap)


def draw_heap(heap, title="Heap Visualization"):
    """Draws a binary heap using matplotlib and networkx"""
    G = nx.DiGraph()
    labels = {}
    for i, val in enumerate(heap):
        G.add_node(i, label=val)
        labels[i] = val
        if i != 0:
            G.add_edge((i - 1) // 2, i)

    pos = hierarchy_pos(G, 0)
    nx.draw(G, pos, with_labels=False,
            node_size=700, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, labels,
                            font_size=12, font_color="black")
    plt.title(title)
    plt.show()


def hierarchy_pos(G, root,
                  width: float = 1.,
                  vert_gap: float = 0.2, vert_loc: float = 0,
                  xcenter: float = 0.5):
    '''
    If there is a cycle that is reachable from root,
        then this will see infinite recursion.
    G: the graph (must be a tree)
    root: the root node of the current branch
    width: horizontal space allocated for this branch
        - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    '''
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc,
                         xcenter)
    return pos


def _hierarchy_pos(G, root,
                   width: float = 1.,
                   vert_gap: float = 0.2, vert_loc: float = 0,
                   xcenter=0.5,
                   pos: dict = None, parent: int = None,
                   parsed: list = None):
    if parsed is None:
        parsed = []
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)

    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child,
                                 width=dx,
                                 vert_gap=vert_gap,
                                 vert_loc=vert_loc - vert_gap,
                                 xcenter=nextx,
                                 pos=pos, parent=root,
                                 parsed=parsed)
    return pos


def visualize_heap(num_elements=10, fixed_seed=False):
    """Example to create a heap and visualize it"""
    # Set a fixed random seed for reproducibility
    if fixed_seed:
        random.seed(42)
    # Create a heap with random values
    heap = [random.randint(1, 100) for _ in range(num_elements)]
    heapq.heapify(heap)  # Transform the list into a heap
    print("Heap before visualization:", heap)
    draw_heap(heap)


def main():
    create_min_heap()
    create_max_heap()
    # Allow user to choose whether to fix the random seed
    user_choice = input(
        "Do you want to fix the random seed "
        "for heap visualization? (yes/no): ").strip().lower()
    fixed_seed = user_choice == 'yes'
    visualize_heap(num_elements=400, fixed_seed=fixed_seed)


if __name__ == "__main__":
    main()
