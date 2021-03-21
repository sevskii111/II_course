import pydot


def draw(graph, parent_name, child_name, count):
    parent_node = pydot.Node(" " + parent_name + "?" *
                             (count - len(parent_name)) + " ")
    child_node = pydot.Node(
        " " + child_name + "?" * (count - len(child_name)) + " ")

    label = ""

    if child_name[-1] in ["0", "1"]:
        label = "Leave" if child_name[-1] == '0' else "Take"
        label += " "
        label += str(len(child_name))
    else:
        #last_ind = child_name.index(' ') - 1
        #label = "Leave" if child_name[last_ind] == '0' else "Take"
        label += " "
        #label += str(last_ind + 1)
        if 'S' not in child_name:
            child_node.set('color', 'red')
        else:
            child_node.set('color', 'green')

    graph.add_node(parent_node)
    graph.add_node(child_node)

    edge = pydot.Edge(parent_node, child_node, label=label)
    graph.add_edge(edge)


def visit(graph, node, parent=None, count=0):

    for _, v in enumerate(node.items()):
        k, v = v
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent is not None:
                draw(graph, parent, k, count)
            visit(graph, v, k, count)
        else:
            if parent is not None:
                draw(graph, parent, k, count)
            # drawing the label using a distinct name
            if k is not None and v is not None:
                draw(graph, k, str(k)+str(v), count)
