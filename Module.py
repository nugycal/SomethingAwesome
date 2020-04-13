#!/usr/bin/env python3

class Module:
    def __init__(self, name, method, options):
        self.name = name
        self.run = method
        self.hasoptions = options

    def processD(self, data, options):
        return self.run(data, options)

    def process(self, data):
        return self.run(data)

    def getName(self):
        return self.name
    
    def hasOptions(self):
        return self.hasoptions
