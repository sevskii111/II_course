import pydot


def draw(graph, parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)


def visit(graph, node, parent=None):
    for _, v in enumerate(node.items()):
        k, v = v
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent is not None:
                draw(graph, parent, k)
            visit(graph, v, k)
        else:
            if parent is not None:
                draw(graph, parent, k)
            # drawing the label using a distinct name
            if k is not None and v is not None:
                draw(graph, k, str(k)+str(v))
