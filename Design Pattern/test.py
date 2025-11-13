class Component:
    def render(self):
        raise NotImplementedError()


class BasicElement(Component):
    def __init__(self, text):
        self.text = text
    def render(self):
        return self.text


class Wrapper(Component):
    def __init__(self, target):
        self.target = target


class Highlighted(Wrapper):
    def render(self):
        return "[[" + self.target.render() + "]]"


class ExternalUnit:
    def output(self):
        raise NotImplementedError()


class LegacyUnit:
    def legacy_format(self):
        return "fromLegacy"


class UnifiedAccess(ExternalUnit):
    def __init__(self, unit):
        self.unit = unit
    def output(self):
        return self.unit.legacy_format()


class ElementCreator:
    def create(self, text):
        raise NotImplementedError()


class VariantA(ElementCreator):
    def create(self, text):
        return BasicElement("A:" + text)


class VariantB(ElementCreator):
    def create(self, text):
        return BasicElement("B:" + text)


class Portal:
    _ref = None

    def __init__(self):
        self._notifier = Notifier()
        self._exchange = Exchange()

    @classmethod
    def access(cls):
        if cls._ref is None:
            cls._ref = Portal()
        return cls._ref

    def notifier(self):
        return self._notifier

    def exchange(self):
        return self._exchange


class Listener:
    def update(self, msg):
        raise NotImplementedError()


class Notifier:
    def __init__(self):
        self._listeners = []

    def add(self, l):
        self._listeners.append(l)

    def remove(self, l):
        self._listeners.remove(l)

    def publish(self, data):
        for l in self._listeners:
            l.update(data)


class Exchange:
    def __init__(self):
        self._topics = {}

    def subscribe(self, topic, listener):
        self._topics.setdefault(topic, []).append(listener)

    def distribute(self, topic, msg):
        if topic not in self._topics:
            return
        for l in self._topics[topic]:
            l.update(msg)


class Mode:
    def process(self, s):
        raise NotImplementedError()


class UpperMode(Mode):
    def process(self, s):
        return s.upper()


class ReverseMode(Mode):
    def process(self, s):
        return s[::-1]


class Processor:
    def __init__(self):
        self.mode = None
    def set_mode(self, mode):
        self.mode = mode
    def run(self, text):
        return self.mode.process(text)


class ComplexItem:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    class Builder:
        def __init__(self):
            self.a = None
            self.b = None
            self.c = None

        def part_a(self, val):
            self.a = val
            return self

        def part_b(self, val):
            self.b = val
            return self

        def part_c(self, val):
            self.c = val
            return self

        def build(self):
            return ComplexItem(self.a, self.b, self.c)

    def describe(self):
        return f"{self.a}|{self.b}|{self.c}"


class ConsoleListener(Listener):
    def update(self, msg):
        print("Notify:", msg)


class TopicListener(Listener):
    def update(self, msg):
        print("Topic:", msg)


if __name__ == "__main__":
    ext = UnifiedAccess(LegacyUnit())
    print(ext.output())

    import random
    creator = VariantA() if random.random() > 0.5 else VariantB()
    base = creator.create("test")

    decorated = Highlighted(base)
    print(decorated.render())

    p = Processor()
    p.set_mode(UpperMode())
    print(p.run("alpha"))
    p.set_mode(ReverseMode())
    print(p.run("alpha"))

    item = ComplexItem.Builder().part_a("one").part_b("two").part_c("three").build()
    print(item.describe())

    console = ConsoleListener()
    Portal.access().notifier().add(console)
    Portal.access().notifier().publish("update")

    subscriber = TopicListener()
    Portal.access().exchange().subscribe("events", subscriber)
    Portal.access().exchange().distribute("events", "incoming")
