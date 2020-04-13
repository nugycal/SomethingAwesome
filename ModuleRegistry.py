from Module import Module

class ModuleRegistry:
    def __init__(self):
        self.raw_data = []
        self.names = {}

    def length(self):
        return len(self.raw_data)

    def get(self, index):
        if index >= 0 and index < len(self.raw_data):
            return self.raw_data[index]
        else:
            return None

    def register(self, module):
        if isinstance(module, Module):
            self.names[module.getName()] = len(self.raw_data)
            self.raw_data.append(module)
