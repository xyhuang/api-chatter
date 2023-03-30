import json
import yaml

class OpenAPIHelper(object):

    def __init__(self):
        self.openapi_spec = {}
        self.paths = {}
        self.methods = {}
        self.task_descriptions = {}

    def load(self, path):
        if any([path.endswith(suffix) for suffix in [".json", ".JSON"]]):
            with open(path, "r") as f:
                self.openapi_spec = json.load(f)
        elif any([path.endswith(suffix) for suffix in [".yaml", ".YAML", ".yml", ".YML"]]):
            with open(path, "r") as f:
                self.openapi_spec = yaml.safe_load(f)

        task_id = 0
        for path, path_detail in self.openapi_spec.get("paths", {}).items():
            if any([path.startswith(prefix) for prefix in ["/organizations", "/networks", "/devices"]]):
                for method, method_detail in path_detail.items():
                    description = method_detail.get("description", None)
                    if description is not None:
                        self.paths[str(task_id)] = path
                        self.methods[str(task_id)] = method
                        self.task_descriptions[str(task_id)] = description
                        task_id += 1

    def get_task_descriptions(self):
        return self.task_descriptions

    def get_spec_from_task(self, task_id):
        path = self.paths[str(task_id)]
        method = self.methods[str(task_id)]
        new_spec = {k: v for k, v in self.openapi_spec.items() if k != "paths"}
        new_spec["paths"] = {path: {method: self.openapi_spec["paths"][path][method]}}
        return new_spec
