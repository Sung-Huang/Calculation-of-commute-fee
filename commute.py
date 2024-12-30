import matplotlib.pyplot as plt
import numpy as np

# Set up basic assumption

class TAXI:
        
    def calculate_single_fee(self, distance):
        callcar = False
        flagfall = 5
        price_per_km = 1.82
        waiting_fee = 0.5
        price = distance * price_per_km + flagfall + waiting_fee * 5
        if callcar:
            return price + 4
        else:
            return price
    def calculate_monthly_fee(self, distance):
        callcar = False
        num_week = 52
        num_month = 12
        flagfall = 5
        price_per_km = 1.82
        waiting_fee = 0.5
        monthly_price = (distance * price_per_km + flagfall + waiting_fee * 5)*2*5*num_week/num_month
        monthly_call_price = (distance * price_per_km + flagfall + waiting_fee * 5 + 4 )*2*5*num_week/num_month
        if callcar:
            return monthly_call_price
        else:
            return monthly_price
    
class BUS:
    def calculate_single_fee(self, distance):
        boarding_fee = 2
        price_per_km = 0.05
        price = boarding_fee + price_per_km * distance
        return price
    def calculate_montly_fee(self, distance):
        num_week = 52
        num_month = 12
        boarding_fee = 2
        price_per_km = 0.05
        total_price = (boarding_fee + price_per_km * distance) * 5 * 2 * num_week / num_month
        return total_price
        
    
taxi_total = TAXI()
taxi_half = TAXI()
bus_total = BUS()
bus_half = BUS()

print(f'計程車全程直接到NMDC單程價格是{taxi_total.calculate_single_fee(38.5):.2f} AED')
print(f'MBZ出發到NMDC計程車單程價格是{taxi_half.calculate_single_fee(8.5)} AED')
print(f'Monthly cost when taking taxi everyday is {taxi_total.calculate_monthly_fee(38.5):.2f} AED')
print(f'搭公車到MBZ單程價格是{bus_half.calculate_single_fee(30)} AED')
print(f'搭公車到MBZ轉計程車到NMDC每月價格是{taxi_half.calculate_monthly_fee(8.5)+bus_half.calculate_montly_fee(30):.2f} AED')

class Car:
    def __init__(self, brand, model, energy_type, fuel_economy, price, maintenance, mileage = 0):
        self.brand = brand
        self.model = model
        self.energy_type = energy_type
        self.fuel_economy = fuel_economy #[km/L]
        self.price = price #[AED]
        self.maintenance = maintenance #[AED/km]
        self.mileage = mileage

    def calculate_averaged_monthly_price(self, commute_single_distance, leisure_daily_additional_distance):
        used_mileage = self.mileage
        annual_insurrance = 3000
        annual_fix_parking = 800
        expected_life_mileage = 275000 - used_mileage
        average_oil_price = 2.3
        num_month = 12
        num_week = 52
        averaged_monthly_mileage = (commute_single_distance * 2+ leisure_daily_additional_distance) * 5 * num_week / num_month
        monthly_fuel_cost = averaged_monthly_mileage / self.fuel_economy * average_oil_price
        depreciation = self.price / expected_life_mileage * averaged_monthly_mileage
        monthly_maintenance_fee = self.maintenance * averaged_monthly_mileage
        monthly_insurrance_fee = annual_insurrance / num_month
        monthly_parking_fix_fee = annual_fix_parking / num_month
        Total_monthly_cost = monthly_fuel_cost + depreciation + monthly_maintenance_fee + monthly_insurrance_fee + monthly_parking_fix_fee
        return Total_monthly_cost

    def plot_real_monthly_price(self, commute_single_distance, leisure_daily_additional_distance, DP_rate, interest_rate, loan_term):
        used_mileage = self.mileage
        annual_insurrance = 5000
        annual_fix_parking = 800
        average_oil_price = 2.3
        expected_life_mileage = 275000 - used_mileage
        num_month = 12
        num_week = 52
        averaged_monthly_mileage = (commute_single_distance * 2 + leisure_daily_additional_distance) * 5 * num_week / num_month
        expected_life_time = int(expected_life_mileage / averaged_monthly_mileage)
        monthly_fuel_cost = averaged_monthly_mileage / self.fuel_economy * average_oil_price
        
        
        monthly_insurrance_fee = annual_insurrance / num_month
        monthly_parking_fix_fee = annual_fix_parking / num_month
        Fixed_monthly_cost = monthly_fuel_cost + monthly_insurrance_fee + monthly_parking_fix_fee

        down_payment = DP_rate * self.price
        n = loan_term * 12 # loan_term in years
        loan_amount = self.price - down_payment
        r = interest_rate / 12
        monthly_payment = ((loan_amount * r)*(1 + r) ** n )/((1 + r) ** n - 1)
        m_p = [down_payment] # Real monthly cost 

        for i in range(1, n): 
            m_p.append(monthly_payment)
        for i in range(n, expected_life_time + 1):
            m_p.append(0)
        
        maintenance_1 = 0 # Annual maintenance fee in first year
        maintenance_2_5 = 900 # Annual maintenance fee in 2-5 year
        maintenance_6_10 = 2500 # Annual maintenance fee in 6-10 year

        for i in range(expected_life_time + 1):
            if i < 12:
                m_p[i] = m_p[i] + (maintenance_1 / 12)
            elif 12 <= i < 60:
                m_p[i] = m_p[i] + (maintenance_2_5 / 12)
            else:
                m_p[i] = m_p[i] + (maintenance_6_10 / 12)
        
        total_m_p = [x + Fixed_monthly_cost for x in m_p]
        
        plt.figure()
        plt.bar([x for x in range(1, expected_life_time + 2)], total_m_p)
        plt.title(f"Real monthly cost of {self.brand} {self.model} {self.energy_type} by month")
        plt.xlabel("Month")
        plt.ylabel("Price in AED")
        
        
        


class UsedCar(Car):
    def __init__(self, brand, model, energy_type, fuel_economy, price, maintenance, mileage, manufacture_year):
        super().__init__(brand, model, energy_type, fuel_economy, price, maintenance, mileage)
        self.manufacture_year = manufacture_year
        self.mileage = mileage

    
# Set up car 
car_a=Car("TOYOTA", "YARIS SEDAN 2024 E", "Patrol", 20.5, 63900, 0.15)
car_b=Car("TOYOTA", "COROLLA 2024 XLI", "Patrol", 18.2, 74900, 0.15)
car_c=Car("MAZDA", "3", "Patrol", 15, 95000, 0.16)
car_d=Car('TOYOTA', "Raize 1L", "Patrol", 20.6, 66900, 0.15)
car_e=Car("NISSAN", "PATROL XE", "Patrol", 8.5, 239900, 0.17)
car_f=Car("TOYOTA", "RUSH 1.5L", "Patrol", 16.3, 71900, 0.15)
car_g=UsedCar("TOYOTA", "RUSH 1.5L", "Patrol", 16.3, 49500, 0.15, 90000, 2022)
car_h=Car("TOYOTA", "2.5L RAV4 VXR", "Hybrid", 19.5, 152900, 0.15)
print(f'{car_a.brand} {car_a.model} {car_a.energy_type}每月養車價格是{car_a.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_b.brand} {car_b.model} {car_b.energy_type}每月養車價格是{car_b.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_c.brand} {car_c.model} {car_c.energy_type}每月養車價格是{car_c.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_d.brand} {car_d.model} {car_d.energy_type}每月養車價格是{car_d.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_e.brand} {car_e.model} {car_e.energy_type}每月養車價格是{car_e.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_f.brand} {car_f.model} {car_f.energy_type}每月養車價格是{car_f.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_h.brand} {car_h.model} {car_h.energy_type}averaged monthly cost during the whole lifetime is {car_h.calculate_averaged_monthly_price(25, 6):.2f} AED')
print(f'{car_g.brand} {car_g.model} {car_g.energy_type}used car manufactured in year {car_g.manufacture_year}每月養車價格是{car_g.calculate_averaged_monthly_price(38, 6):.2f} AED')
car_h.plot_real_monthly_price(25, 6, 0.2, 0.023, 2)
# car_e.plot_real_monthly_price(25, 6, 0.2, 0.023, 2)
# car_d.plot_real_monthly_price(38, 6, 0.2, 0.023, 5)
plt.show()


# Add a comment test

    


