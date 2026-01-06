from graphviz import Digraph

def generate_flowchart(summary_text, output_name="flowchart"):
    """
    Converts summary text into a simple vertical flowchart
    """
    # Split summary into steps
    steps = [s.strip() for s in summary_text.split(".") if len(s.strip()) > 10]

    dot = Digraph(format="png")
    dot.attr(rankdir="TB", size="8,10")

    for i, step in enumerate(steps):
        dot.node(str(i), step)
        if i > 0:
            dot.edge(str(i - 1), str(i))

    dot.render(output_name)
    return f"{output_name}.png"
