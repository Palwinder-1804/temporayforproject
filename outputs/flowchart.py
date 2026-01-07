from graphviz import Digraph

def generate_flowchart(summary):
    dot = Digraph(format="png")
    dot.attr(rankdir="TB")

    points = summary.split(".")[:5]

    for i, point in enumerate(points):
        dot.node(str(i), point.strip())
        if i > 0:
            dot.edge(str(i - 1), str(i))

    return dot
