import pandas as pd

# Set up basic assumption

class TAXI:
        
    def calculate_single_fee(self, distance):
        callcar=False
        flagfall=5
        price_per_km=1.82
        waiting_fee=0.5
        price = distance * price_per_km + flagfall + waiting_fee * 5
        if callcar:
            return price+4
        else:
            return price
    def calculate_monthly_fee(self, distance):
        callcar=False
        num_week=52
        num_month=12
        flagfall=5
        price_per_km=1.82
        waiting_fee=0.5
        monthly_price = (distance * price_per_km + flagfall + waiting_fee * 5)*2*5*num_week/num_month
        monthly_call_price = (distance * price_per_km + flagfall + waiting_fee * 5 + 4 )*2*5*num_week/num_month
        if callcar:
            return monthly_call_price
        else:
            return monthly_price
    
class BUS:
    def calculate_single_fee(self, distance):
        boarding_fee=2
        price_per_km=0.05
        price=boarding_fee+price_per_km*distance
        return price
    def calculate_montly_fee(self, distance):
        num_week=52
        num_month=12
        boarding_fee=2
        price_per_km=0.05
        total_price=(boarding_fee+price_per_km*distance)*5*2*num_week/num_month
        return total_price
        
    
taxi_total=TAXI()
taxi_half=TAXI()
bus_total=BUS()
bus_half=BUS()

print(f'計程車全程直接到NMDC單程價格是{taxi_total.calculate_single_fee(38.5):.2f} AED')
print(f'MBZ出發到NMDC計程車單程價格是{taxi_half.calculate_single_fee(8.5)} AED')
print(f'計程車全程來回每月價格是{taxi_total.calculate_monthly_fee(38.5):.2f} AED')
print(f'搭公車到MBZ單程價格是{bus_half.calculate_single_fee(30)} AED')
print(f'搭公車到MBZ轉計程車到NMDC每月價格是{taxi_half.calculate_monthly_fee(8.5)+bus_half.calculate_montly_fee(30):.2f} AED')

class Car:
    def __init__(self, brand, model, energy_type, fuel_economy, price, maintenance, mileage = 0):
        self.brand=brand
        self.model=model
        self.energy_type=energy_type
        self.fuel_economy=fuel_economy #[km/L]
        self.price=price #[AED]
        self.maintenance=maintenance #[AED/km]
        self.mileage = mileage

    def calculate_averaged_monthly_price(self, commute_single_distance, leisure_daily_additional_distance):
        used_mileage = self.mileage
        annual_insurrance=3000
        annual_fix_parking=4500
        expected_life_mileage=275000 - used_mileage
        average_oil_price=2.7
        num_month=12
        num_week=52
        averaged_monthly_mileage=(commute_single_distance*2+leisure_daily_additional_distance)*5*num_week/num_month
        monthly_fuel_cost=averaged_monthly_mileage/self.fuel_economy*average_oil_price
        depreciation=self.price/expected_life_mileage*averaged_monthly_mileage
        monthly_maintenance_fee=self.maintenance*averaged_monthly_mileage
        monthly_insurrance_fee=annual_insurrance/num_month
        monthly_parking_fix_fee=annual_fix_parking/num_month
        Total_monthly_cost=monthly_fuel_cost+depreciation+monthly_maintenance_fee+monthly_insurrance_fee+monthly_parking_fix_fee
        return Total_monthly_cost

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
print(f'{car_a.brand} {car_a.model} 每月養車價格是{car_a.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_b.brand} {car_b.model} 每月養車價格是{car_b.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_c.brand} {car_c.model} 每月養車價格是{car_c.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_d.brand} {car_d.model} 每月養車價格是{car_d.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_e.brand} {car_e.model} 每月養車價格是{car_e.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_f.brand} {car_f.model} 每月養車價格是{car_f.calculate_averaged_monthly_price(38, 6):.2f} AED')
print(f'{car_h.brand} {car_h.model} averaged monthly cost during the whole lifetime is {car_h.calculate_averaged_monthly_price(25, 6):.2f} AED')
print(f'{car_g.brand} {car_g.model} used car manufactured in year {car_g.manufacture_year}每月養車價格是{car_g.calculate_averaged_monthly_price(38, 6):.2f} AED')


# Add a comment test

    


