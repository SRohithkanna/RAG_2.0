import nbformat

def load_notebook_functions(ipynb_path):
    namespace = {}

    with open(ipynb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            exec(cell.source, namespace)

    return namespace
