#https://gist.githubusercontent.com/ajxchapman/443c1673e0948f92e59452e3b5951c99/raw/50c99be5bdbb5ee46e567d930ef96c90c71ddb85/burp_scopes.py
import json
import re
import sys

scopes = []
f = sys.stdin
if len(sys.argv) == 2:
    f = open(sys.argv[1])
scopes_defs = [x.strip().lower() for x in f.readlines() if len(x.strip())]

for scope_def in scopes_defs:
    scope = {
        "enabled" : True,
        "host" : scope_def,
        "protocol" : "any"
    }

    if scope["host"].startswith("http://") or scope["host"].startswith("https://"):
        scope["protocol"], scope["host"] = scope["host"].split("//", 1)
        scope["protocol"] = scope["protocol"].rstrip(":")

    if scope["host"].startswith("*"):
        scope["host"] = ".*{}$".format(re.escape(scope["host"].lstrip("*")))

    if "/" in scope["host"]:
        scope["host"], scope["file"] = scope["host"].split("/", 1)
        if not len(scope["file"]):
            del scope["file"]
        else:
            scope["file"] = "^/{}.*".format(re.escape(scope["file"].rstrip("*")))
    
    if ":" in scope["host"]:
        scope["host"], scope["port"] = scope["host"].split(":", 1)

    scopes.append(scope)

print(json.dumps({
    "target": {
        "scope": {
            "advanced_mode": True,
            "exclude": [],
            "include": scopes
        }
    }
}, indent=4))
