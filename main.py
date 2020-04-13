#!/usr/bin/env python3

from ModuleRegistry import ModuleRegistry
import os
import string
import importlib

module_registry = ModuleRegistry()

def valid_filename(file):
    valid = string.ascii_letters + "._-+, " + "0123456789"
    for i in file:
        if i not in valid:
            return False
    return True

__globals = globals()
for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    if file[:4] == "mod_":

        if valid_filename(file) == False:
            print(f"Unable to load module '{file}' - invalid characters in filename")
        else:
            mod_name = file[4:][:-3]
            module_registry.register(exec('from mod_{} import modules; temp = [module_registry.register(module) for module in modules];'.format(mod_name)))

def options():
    last = 0
    steps = []
    while last != "q":
        print("====================")
        print("       Options      ")
        print("====================")
        print("q: Process existing selection and move on")
        print("!: Remove previous step")

        for index in range(module_registry.length()):
            module = module_registry.get(index)
            print(f"{index}. {module.getName()}")

        last = input("Option: ")
        if last in "q!" or int(last) >= 0 and int(last) < module_registry.length():
            if last == "q":
                break
            elif last == "!":
                if len(steps) == 0:
                    print("You haven't added any steps yet!")
                    continue
                else:
                    steps.pop()
                    continue
            last = int(last)
            if last >= 0 and last < module_registry.length():
                if len(module_registry.get(last).hasOptions()) != 0:
                    options = []
                    for option in module_registry.get(last).hasOptions():
                        user = ""
                        while user == "":
                            user = input("Enter " + option + ": ")
                            if "required" in option.lower() and user.strip() == "":
                                print(f"{option} is required.")
                            else:
                                continue
                        if user.strip() == "":
                            continue
                        else:
                            options.append(user)
                    steps.append((last, options))
                else:
                    steps.append([last])
            else:
                steps.append([last])
    return steps

flag = ""
while flag == "":
    flag = input("Enter a Flag: ")
    if flag == "":
        print("Invalid Flag!")
    elif len(flag) >= 65535:
        print("Invalid Flag!")
        flag = ""
steps = options()
print("=== Original Flag ===")
data = flag
for step in steps:
    for char in str(step[0]):
        if char not in "0123456789":
            flag = True
    if flag == True:
        continue
    try:
        int_step = int(step[0])
    except TypeError as e:
        print(f"error parsing step index '{step}'.")
    except ValueError as e:
        print(f"error parsing step index '{step}'.")

    if int_step < 0 or int_step > module_registry.length():
        continue
    print(data)
    print(f"=== {module_registry.get(int_step).getName()} ===")
    if len(step) == 2:
        options = step[1]
        data = module_registry.get(int_step).processD(data, options)
    else:
        data = module_registry.get(int_step).process(data)

print(data)