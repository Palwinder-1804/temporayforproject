import re


def _extract_steps(text: str, max_steps: int = 6) -> list[str]:
    """
    Extract logical steps from text.

    Strategy:
    - Split into sentences
    - Keep medium-length, action-oriented sentences
    """

    if not text:
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text)

    steps = []
    for s in sentences:
        s = s.strip()

        # Filter weak or very short sentences
        if len(s.split()) < 6:
            continue

        steps.append(s)

        if len(steps) >= max_steps:
            break

    return steps


def generate_flowchart(text: str) -> str:
    """
    Generate a Mermaid-style flowchart from text.

    Output example:

    graph TD
    A[Step 1] --> B[Step 2]
    B --> C[Step 3]
    """

    steps = _extract_steps(text)

    if not steps:
        return ""

    lines = ["graph TD"]

    for i, step in enumerate(steps):
        node_id = chr(65 + i)  # A, B, C...
        label = step.replace('"', "'")  # Mermaid-safe

        lines.append(f'{node_id}["{label}"]')

        if i > 0:
            prev_id = chr(65 + i - 1)
            lines.append(f"{prev_id} --> {node_id}")

    return "\n".join(lines)
