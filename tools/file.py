import contextlib, json, ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.explicit_start = True

def load_json(path):
    with contextlib.suppress(FileNotFoundError, ImportError):
        with open(path, "r") as f:
            return json.loads(f.read())

def write_yaml(path, data, cloud=False):
    with contextlib.suppress(FileNotFoundError, ImportError):
        with open(path, "w") as f:
            data = json.loads(data, object_pairs_hook=ruamel.yaml.comments.CommentedMap)
            ruamel.yaml.scalarstring.walk_tree(data)
            if cloud:
                f.write("#cloud-config\n")
            yaml.dump(data, f)

def read_file(path):
    with contextlib.suppress(FileNotFoundError, ImportError):
        with open(path, "r") as f:
            return f.read()

def write_file(path, contents):
    with contextlib.suppress(FileNotFoundError, ImportError):
        with open(path, "w") as f:
            return f.write(contents)
