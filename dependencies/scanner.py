from pathlib import Path
from stdlib_list import stdlib_list
import platform

with open("generated_requirements.txt", "w") as requirements:
    seen_reqs = set()
    python_version = platform.python_version().split(".")
    python_version = ".".join(python_version[:2])
    stdlib = set(stdlib_list(python_version))
    for path in Path("./tests/test-repo/.").rglob("*.py"):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                reqs = []
                line = line.strip()

                if line.startswith("from "):
                    reqs = line.removeprefix("from ").split(" import ")[0]
                    reqs = [r.strip() for r in reqs.split(",")] # for modules like sklearn.cluster, we just want sklearn

                elif line.startswith("import "):  # import x,y,z vs. import x
                    reqs = line.removeprefix("import ")
                    reqs = reqs.split(",")
                    
                if reqs:
                    for req in reqs:
                        base_req = req.split(".")[0]
                        if base_req not in seen_reqs and base_req not in stdlib:
                            requirements.write(base_req + "\n")
                            seen_reqs.add(base_req)