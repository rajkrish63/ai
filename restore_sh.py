import sys

path = '/home/rajkrish/.local/lib/python3.10/site-packages/sh.py'
try:
    with open(path, 'r') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: {path} not found")
    sys.exit(1)

# Find the start of env_validator
start_index = -1
for i, line in enumerate(lines):
    if 'def env_validator(passed_kwargs, merged_kwargs):' in line:
        start_index = i
        break

if start_index == -1:
    print("Could not find env_validator")
    sys.exit(1)

# Find the end of our botched patch (which added multiple 'if env is not None' lines)
# and restore it to the original:
#    if passed_kwargs.get("env", None) is None:
#        return invalid

# We know the original ends around where 'if not isinstance(env, Mapping):' or similar starts.
# Actually, the original sh.py env_validator is very simple.

new_content = lines[:start_index+1]
new_content.append('    """ a validator to check that env is a dictionary and that all environment variable\n')
new_content.append('    keys and values are strings. Otherwise, we would exit with a confusing exit code 255. """\n')
new_content.append('    invalid = []\n')
new_content.append('\n')
new_content.append('    if passed_kwargs.get("env", None) is None:\n')
new_content.append('        return invalid\n')
new_content.append('\n')

# Find where the original loop starts: "for k, v in passed_kwargs["env"].items():"
resume_index = -1
for i in range(start_index, len(lines)):
    if 'for k, v in passed_kwargs["env"].items():' in line or 'if not isinstance(passed_kwargs["env"], Mapping):' in lines[i]:
        resume_index = i
        break

if resume_index != -1:
    new_content.extend(lines[resume_index:])
else:
    # Fallback to a safe guess if we can't find it
    print("Warning: Could not find resume point, using fallback")
    new_content.append('    if not isinstance(passed_kwargs["env"], Mapping):\n')
    new_content.append('        invalid.append(("env", "env must be dict-like. Got {!r}".format(passed_kwargs["env"])))\n')
    new_content.append('        return invalid\n')
    new_content.append('\n')
    new_content.append('    for k, v in passed_kwargs["env"].items():\n')
    # ... this is getting complex.

# Let's just do a string replacement of the whole function if possible.
full_content = "".join(lines)
import re
# Regex to match the whole env_validator function
# This is safer if we know the start and the next function starts.
# Next class is "class Command(object):"
func_pattern = re.compile(r'def env_validator\(passed_kwargs, merged_kwargs\):.*?class Command\(object\):', re.DOTALL)
replacement = """def env_validator(passed_kwargs, merged_kwargs):
    \"\"\" a validator to check that env is a dictionary and that all environment variable
    keys and values are strings. Otherwise, we would exit with a confusing exit code 255. \"\"\"
    invalid = []

    if passed_kwargs.get("env", None) is None:
        return invalid

    if not isinstance(passed_kwargs["env"], Mapping):
        invalid.append(("env", "env must be dict-like. Got {!r}".format(passed_kwargs["env"])))
        return invalid

    for k, v in passed_kwargs["env"].items():
        if not isinstance(k, str):
            invalid.append(("env", "env key {!r} must be a str".format(k)))

        elif not isinstance(v, str):
            invalid.append(("env", "value {!r} of env key {!r} must be a str".format(v, k)))

    return invalid


class Command(object):"""

fixed_content = func_pattern.sub(replacement, full_content)
with open(path, 'w') as f:
    f.write(fixed_content)
print("sh.py restored successfully")
