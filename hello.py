#!/usr/bin/env python3

def say_hello(name: str) -> None:
    print(f"Hello from {name}")

if __name__ == "__main__":
    # change the name below or uncomment the input line to prompt at runtime
    # name = input("Enter your name: ")
    name = "Matthew Schepers"
    say_hello(name)
