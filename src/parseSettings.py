import sys
import json
args = sys.argv[1:]

# "Source" the provided settings file
with open(args[0], "r") as f:
    exec(f.read())
    
sourced_globals = dict(globals())

# Store the global variables in a dictionary
diff = {
    k: sourced_globals[k] 
        for k in list(sourced_globals.keys()) 
        if 
            not k.startswith("__")
            and
            k not in ["sys", "json", "args", "sourced_globals", "f"]    
    }

# Print the difference as JSON
print(json.dumps(diff, indent=4))