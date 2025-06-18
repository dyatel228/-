import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.count = 1


class Tree:
    def __init__(self):
        self.root = Node(0)

    def insert(self, node, data, path, index=0):
        if index == len(path):
            if node.data == data:
                node.count += 1
            elif node.data != 0:
                raise ValueError(f"число {data} не помещается по пути {path}")
            else:
                node.data = data
            return

        direction = path[index]

        if direction == '0':
            if node.left is None:
                node.left = Node(0)
            self.insert(node.left, data, path, index + 1)
        elif direction == '1':
            if node.right is None:
                node.right = Node(0)
            self.insert(node.right, data, path, index + 1)

    def check_missing_nodes(self, data):
        paths = [path for _, path in data]
        # Сортировка без sort()
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                if paths[i] > paths[j]:
                    paths[i], paths[j] = paths[j], paths[i]

        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                path1 = paths[i]
                path2 = paths[j]
                if len(path2) >= len(path1) and path2[:len(path1)] == path1 and len(path2) > len(path1):
                    missing_path = path2[:len(path1) + 1]
                    if missing_path not in paths:
                        raise ValueError(f"не хватает узла '{missing_path}'")
        return True


def read_excel_data(file_path):
    try:
        df = pd.read_excel(file_path, header=None, dtype={0: str, 1: str})
    except Exception as e:
        raise ValueError(f"не получилось прочитать файл: {e}")

    data = []
    for index, row in df.iterrows():
        num_str = str(row[0]).strip()
        path = str(row[1]).strip()

        try:
            number = int(num_str)
        except (ValueError, TypeError):
            raise ValueError(f"в строке {index + 1}: '{num_str}' - это не целое число")

        if num_str.startswith('0') and len(num_str) > 1:

            raise ValueError(f"в строке {index + 1}: в числе '{num_str}' есть ведущие нули")

        if not all(c in ('0', '1') for c in path):
            raise ValueError(f"в строке {index + 1}: в пути '{path}' есть что-то кроме 0 и 1")

        data.append((number, path))

    return data


def visualize_tree(root):
    G = nx.Graph()
    pos = {}
    labels = {}
    queue = [(root, (0, 0))]
    level_height = 2

    while queue:
        node, (x, y) = queue.pop(0)
        label = f"{node.data}" + (f" (x{node.count})" if node.count > 1 else "")
        labels[node] = label
        pos[node] = (x, -y)

        if node.left:
            G.add_edge(node, node.left)
            left_x = x - 1 / (2 * (y / level_height + 1))
            queue.append((node.left, (left_x, y + level_height)))

        if node.right:
            G.add_edge(node, node.right)
            right_x = x + 1 / (2 * (y / level_height + 1))
            queue.append((node.right, (right_x, y + level_height)))

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000,
            node_color='skyblue', font_size=10, font_weight='bold')
    plt.title("Бинарное дерево", size=15)
    plt.show()


try:
    data = read_excel_data("tree_data.xlsx")

    tree = Tree()

    if tree.check_missing_nodes(data):
        for number, path in data:
            tree.insert(tree.root, number, path)

        print("Дерево построено!")
        visualize_tree(tree.root)

except FileNotFoundError:
    print("файл 'tree_data.xlsx' не найден")
except ValueError as e:
    print(f"Ошибка: {e}")