# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def main():
    # 创建根节点
    root = TreeNode(1)

    # 创建其他节点并连接
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    # 前序遍历
    def pre_order_traversal(node):
        if node:
            print(node.val, end=' ')  # 访问根节点
            pre_order_traversal(node.left)  # 访问左子树
            pre_order_traversal(node.right)  # 访问右子树
    print(f"Pre-order")
    pre_order_traversal(root)

    # 中序遍历
    def in_order_traversal(node):
        if node:
            in_order_traversal(node.left)  # 访问左子树
            print(node.val, end=' ')  # 访问根节点
            in_order_traversal(node.right)  # 访问右子树
    print(f"\nIn-order")
    in_order_traversal(root)

    # 后序遍历
    def post_order_traversal(node):
        if node:
            post_order_traversal(node.left)  # 访问左子树
            post_order_traversal(node.right)  # 访问右子树
            print(node.val, end=' ')  # 访问根节点

    print(f"\nPost-order")
    post_order_traversal(root)
    print(f"\n")

    depth0_tree = TreeNode(1)

    def tree_depth(node):
        if not node:
            return 0
        left_depth = tree_depth(node.left)
        right_depth = tree_depth(node.right)
        return 1 + max(left_depth, right_depth)

    print(tree_depth(depth0_tree))


if __name__ == "__main__":
    main()
