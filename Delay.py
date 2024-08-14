class Delay:
    def __init__(self, name: str, delayPercent: str, target, reqBroken: bool, stackable: bool):
        self.name = name
        self.delayPercent = delayPercent
        self.target = target
        self.reqBroken = reqBroken
        self.stackable = stackable