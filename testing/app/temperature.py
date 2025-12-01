class Temperature:
    def __init__(self, value, unit="C"):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric")
        if unit not in ("C","F"):
            raise ValueError("Invalid unit")
        self.value=float(value); self.unit=unit
    def to_fahrenheit(self):
        return self.value if self.unit=="F" else (self.value*9/5)+32
    def to_celsius(self):
        return self.value if self.unit=="C" else (self.value-32)*5/9
    def __add__(self, other):
        if not isinstance(other, Temperature): raise TypeError
        if self.unit!=other.unit: raise ValueError
        return Temperature(self.value+other.value, self.unit)
