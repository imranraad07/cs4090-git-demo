import streamlit as st
import time

st.set_page_config(page_title="Builder Pattern Demo", page_icon="🧱")
st.title("Builder Pattern")


# --- Product ---
class Computer:
    def __init__(self, category):
        self.category = category
        self.cpu = None
        self.gpu = None
        self.ram = None
        self.storage = None
        self.os = None
        self.price = 0

    def __str__(self):
        return (
            f"Category: {self.category}\n"
            f"CPU: {self.cpu}\n"
            f"GPU: {self.gpu}\n"
            f"RAM: {self.ram}\n"
            f"Storage: {self.storage}\n"
            f"Operating System: {self.os}\n"
            f"Total Price: ${self.price:,.2f}\n"
        )


# --- Builder Base Class ---
class ComputerBuilder:
    def __init__(self, category):
        self.computer = Computer(category)

    def set_cpu(self, cpu, price):
        self.computer.cpu = cpu
        self.computer.price += price
        return self

    def set_gpu(self, gpu, price):
        if gpu and gpu != "None":
            self.computer.gpu = gpu
            self.computer.price += price
        return self

    def set_ram(self, ram, price):
        self.computer.ram = ram
        self.computer.price += price
        return self

    def set_storage(self, storage, price):
        if storage and storage != "None":
            self.computer.storage = storage
            self.computer.price += price
        return self

    def set_os(self, os, price):
        if os and os != "None":
            self.computer.os = os
            self.computer.price += price
        return self

    def build(self):
        # validation: required fields
        if not self.computer.cpu or not self.computer.ram:
            raise ValueError("CPU and RAM are required to build a computer.")
        return self.computer


# --- Concrete Builders ---
class DesktopBuilder(ComputerBuilder):
    def __init__(self):
        super().__init__("Desktop PC")


class LaptopBuilder(ComputerBuilder):
    def __init__(self):
        super().__init__("Laptop")


# --- Director ---
class ComputerDirector:
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder

    def build_custom_pc(self, components, progress_callback):
        for i, (name, (value, price)) in enumerate(components.items(), 1):
            if name == "CPU":
                self.builder.set_cpu(value, price)
            elif name == "GPU":
                self.builder.set_gpu(value, price)
            elif name == "RAM":
                self.builder.set_ram(value, price)
            elif name == "Storage":
                self.builder.set_storage(value, price)
            elif name == "OS":
                self.builder.set_os(value, price)
            progress_callback(i / len(components), f"Installing {name}...")
            time.sleep(0.4)
        return self.builder.build()


# --- Pricing Dictionary ---
PRICE_LIST = {
    "CPU": {
        "Intel Core i5": 300,
        "Intel Core i7": 400,
        "AMD Ryzen 7": 450,
        "Apple M3": 500,
    },
    "GPU": {
        "None": 0,
        "Integrated": 0,
        "NVIDIA RTX 4070": 900,
        "NVIDIA RTX 4090": 1600,
        "AMD Radeon RX 7800": 750,
    },
    "RAM": {
        "8GB DDR4": 60,
        "16GB DDR4": 120,
        "32GB DDR5": 250,
    },
    "Storage": {
        "None": 0,
        "512GB SSD": 100,
        "1TB SSD": 150,
        "2TB NVMe SSD": 300,
    },
    "OS": {
        "None": 0,
        "Windows 10": 150,
        "Windows 11": 200,
        "Linux": 0,
        "macOS": 250,
    },
}


# --- Streamlit UI ---
st.header("🖥️ Custom Build Your PC")

device_type = st.radio("Device Type:", ["Desktop", "Laptop"])
builder = DesktopBuilder() if device_type == "Desktop" else LaptopBuilder()
director = ComputerDirector(builder)

progress_bar = st.progress(0, text="Idle...")

# --- Progress callback function ---
def update_progress(value, text):
    progress_bar.progress(value, text=text)

# --- Custom Build Options ---
st.subheader("🧩 Select Components")

# Required fields (no None option)
cpu = st.selectbox("CPU (Required)", list(PRICE_LIST["CPU"].keys()))
ram = st.selectbox("RAM (Required)", list(PRICE_LIST["RAM"].keys()))

# Optional fields
gpu = st.selectbox("GPU (Optional)", list(PRICE_LIST["GPU"].keys()))
storage = st.selectbox("Storage (Optional)", list(PRICE_LIST["Storage"].keys()))
os = st.selectbox("Operating System (Optional)", list(PRICE_LIST["OS"].keys()))

computer = None

if st.button("🛠️ Build Custom PC"):
    components = {
        "CPU": (cpu, PRICE_LIST["CPU"][cpu]),
        "GPU": (gpu, PRICE_LIST["GPU"][gpu]),
        "RAM": (ram, PRICE_LIST["RAM"][ram]),
        "Storage": (storage, PRICE_LIST["Storage"][storage]),
        "OS": (os, PRICE_LIST["OS"][os]),
    }
    try:
        computer = director.build_custom_pc(components, update_progress)
        st.success("✅ Custom PC Built Successfully!")
    except ValueError as e:
        st.error(str(e))

# --- Display Final Product ---
if computer:
    st.subheader("🧾 Final Build Summary")
    st.text(str(computer))
    st.json({
        "Category": computer.category,
        "CPU": computer.cpu,
        "GPU": computer.gpu,
        "RAM": computer.ram,
        "Storage": computer.storage,
        "OS": computer.os,
        "Total Price": f"${computer.price:,.2f}"
    })

st.caption("""
This Builder Pattern demo enforces **required components** (CPU, RAM)  
and allows **optional parts** (GPU, Storage, OS) to be skipped using `"None"`.  
The pattern cleanly separates construction steps while preserving flexibility.
""")
