from inspect import _empty, getmembers, signature

from lru import TimedLRUCache

docstrings = {}

members = getmembers(TimedLRUCache, callable)
class_name = TimedLRUCache.__name__
class_docstring = TimedLRUCache.__doc__
parent_class_members = TimedLRUCache.__bases__[0]

parent_class_members = {
    name: member for name, member in getmembers(parent_class_members, callable)
}

for name, member in members:
    if name in parent_class_members:
        if parent_class_members[name].__doc__ == member.__doc__:
            continue

    if member.__doc__:
        docstrings[name] = {
            "docstring": member.__doc__,
            "signature": signature(member),
            "arguments": signature(member).parameters,
        }

result = f"{class_name}: {class_docstring.strip()}\n"

for name, docstring in docstrings.items():
    result += (
        f"""\n{name}{docstring["signature"]} -> {docstring["docstring"].strip()}\n\n"""
    )
    for param in docstring["arguments"]:
        if docstring["arguments"][param].annotation != _empty:
            result += f"\t{param}: {docstring['arguments'][param].annotation.__name__} ({docstring['arguments'][param].default})\n"
        else:
            result += f"\t{param}\n"

print(result)
