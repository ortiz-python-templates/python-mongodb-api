import ast
import os

BASE_PATH = "src/controllers"

def get_routes_from_file(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and hasattr(decorator.func, "attr"):
                    if decorator.func.attr in ["get", "post", "put", "delete"]:
                        routes.append(node.name)
    return routes


def main():
    feature_flags = []

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".py"):
                module = file.replace("_controller.py", "").replace(".py", "")
                file_path = os.path.join(root, file)
                
                routes = get_routes_from_file(file_path)
                
                for route in routes:
                    flag = f"flag.{module}.{route.replace('_', '-')}"
                    feature_flags.append(flag)

    print("\n=== GENERATED FEATURE FLAGS ===")
    for flag in feature_flags:
        print(flag)

    print(f"\nTotal: {len(feature_flags)} feature flags\n")


if __name__ == "__main__":
    main()
