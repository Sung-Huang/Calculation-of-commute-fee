import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# 父類
class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed  # 單位：km/h

    def display_info(self):
        return f"Vehicle Name: {self.name}\nSpeed: {self.speed} km/h"

# 子類 Car
class Car(Vehicle):
    def __init__(self, name, speed, seats):
        super().__init__(name, speed)
        self.seats = seats

    def display_info(self):
        return super().display_info() + f"\nSeats: {self.seats}"

    def calculate_cost(self):
        # 假設成本公式為：速度 * 座位數 * 0.1
        return self.speed * self.seats * 0.1

# 子類 Truck
class Truck(Vehicle):
    def __init__(self, name, speed, load_capacity):
        super().__init__(name, speed)
        self.load_capacity = load_capacity  # 單位：tons

    def display_info(self):
        return super().display_info() + f"\nLoad Capacity: {self.load_capacity} tons"

    def calculate_cost(self):
        # 假設成本公式為：速度 * 載重能力 * 0.2
        return self.speed * self.load_capacity * 0.2

# GUI 介面
def main():
    # 計算成本的函數
    def calculate_cost():
        vehicle_type = vehicle_type_var.get()
        name = car_model_var.get()
        speed = speed_var.get()

        if not speed.isdigit():
            messagebox.showerror("Input Error", "Speed must be a valid number.")
            return

        speed = float(speed)

        if vehicle_type == "Car":
            seats = seats_var.get()
            if not seats.isdigit():
                messagebox.showerror("Input Error", "Seats must be a valid number.")
                return
            seats = int(seats)
            vehicle = Car(name, speed, seats)
        elif vehicle_type == "Truck":
            load_capacity = load_capacity_var.get()
            if not load_capacity.replace(".", "", 1).isdigit():
                messagebox.showerror("Input Error", "Load capacity must be a valid number.")
                return
            load_capacity = float(load_capacity)
            vehicle = Truck(name, speed, load_capacity)
        else:
            messagebox.showerror("Input Error", "Invalid vehicle type selected.")
            return

        # 顯示結果
        result = vehicle.display_info()
        cost = vehicle.calculate_cost()
        result += f"\nOperating Cost: ${cost:.2f}"
        result_label.config(text=result)

    # 切換輸入框
    def update_inputs(*args):
        if vehicle_type_var.get() == "Car":
            seats_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            seats_entry.grid(row=4, column=1, padx=10, pady=5)
            load_capacity_label.grid_forget()
            load_capacity_entry.grid_forget()
        elif vehicle_type_var.get() == "Truck":
            load_capacity_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            load_capacity_entry.grid(row=4, column=1, padx=10, pady=5)
            seats_label.grid_forget()
            seats_entry.grid_forget()

    # 創建主視窗
    root = tk.Tk()
    root.title("Vehicle Cost Calculator")

    # 車輛類型選擇
    vehicle_type_var = tk.StringVar(value="Car")
    tk.Label(root, text="Select Vehicle Type:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    vehicle_type_menu = ttk.Combobox(root, textvariable=vehicle_type_var, values=["Car", "Truck"], state="readonly")
    vehicle_type_menu.grid(row=0, column=1, padx=10, pady=5)
    vehicle_type_menu.bind("<<ComboboxSelected>>", update_inputs)

    # 車輛品牌選擇
    car_model_var = tk.StringVar(value="Toyota")
    tk.Label(root, text="Select Vehicle Model:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    car_model_menu = ttk.Combobox(root, textvariable=car_model_var, values=["Toyota", "Ford", "Mercedes"], state="readonly")
    car_model_menu.grid(row=1, column=1, padx=10, pady=5)

    # 輸入速度
    speed_var = tk.StringVar()
    tk.Label(root, text="Enter Speed (km/h):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    speed_entry = tk.Entry(root, textvariable=speed_var)
    speed_entry.grid(row=2, column=1, padx=10, pady=5)

    # 輸入座位數（僅適用於 Car）
    seats_var = tk.StringVar()
    seats_label = tk.Label(root, text="Enter Number of Seats:")
    seats_entry = tk.Entry(root, textvariable=seats_var)

    # 輸入載重能力（僅適用於 Truck）
    load_capacity_var = tk.StringVar()
    load_capacity_label = tk.Label(root, text="Enter Load Capacity (tons):")
    load_capacity_entry = tk.Entry(root, textvariable=load_capacity_var)

    # 計算按鈕
    calculate_button = tk.Button(root, text="Calculate Cost", command=calculate_cost)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

    # 結果顯示
    result_label = tk.Label(root, text="", justify="left", anchor="w")
    result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # 初始化輸入框
    update_inputs()

    # 啟動主迴圈
    root.mainloop()

# 執行主程式
if __name__ == "__main__":
    main()
