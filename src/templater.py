import sys
import json
import ast

class TemplateTransformer(ast.NodeTransformer):
    def __init__(self, bindings):
        self.bindings = bindings

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "t":
            # We found the template expression
            template_node = node.args[0]
            if isinstance(template_node, ast.Str):
                template = template_node.s
            elif isinstance(template_node, ast.JoinedStr):
                template = "".join([
                    value.s if isinstance(value, ast.Constant) 
                        else 
                    self.bindings[value.value.id] for value in template_node.values])
            else:
                raise ValueError("Unsupported template node type")
            
            new_node = getattr(ast.parse(template).body[0], 'value', ast.parse(template).body[0])
            return new_node
        return node

def template_ast(tree, bindings):
    """
        Template the AST tree with the given bindings.
        The template expression is a call to the function t() with a single argument - JoinedStr (f"Template string {variable}")
            This is to be replaced with the string itself, with the bindings applied.
    """
    transformer = TemplateTransformer(bindings)
    for node in ast.walk(tree):
        transformer.visit(node)

    return tree

[in_path, bindings, out_path] = sys.argv[1:]
with open(in_path, "r") as f:
    tree = ast.parse(f.read())

    bindings = json.loads(bindings)
    tree = template_ast(tree, bindings)

    with open(out_path, "w") as f:
        f.write(ast.unparse(tree))
    