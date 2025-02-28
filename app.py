import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

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
        toll_fee = 4 * 2 * 22
        averaged_monthly_mileage = (commute_single_distance * 2+ leisure_daily_additional_distance) * 5 * num_week / num_month
        monthly_fuel_cost = averaged_monthly_mileage / self.fuel_economy * average_oil_price
        depreciation = self.price / expected_life_mileage * averaged_monthly_mileage
        monthly_maintenance_fee = self.maintenance * averaged_monthly_mileage
        monthly_insurrance_fee = annual_insurrance / num_month
        monthly_parking_fix_fee = annual_fix_parking / num_month
        Total_monthly_cost = monthly_fuel_cost + depreciation + monthly_maintenance_fee + monthly_insurrance_fee + monthly_parking_fix_fee + toll_fee
        return Total_monthly_cost

    def plot_real_monthly_price(self, commute_single_distance, leisure_daily_additional_distance, DP_rate, interest_rate, loan_term):
        used_mileage = self.mileage
        annual_insurrance = 2000
        annual_fix_parking = 800
        average_oil_price = 2.3
        expected_life_mileage = 300000 - used_mileage
        num_month = 12
        num_week = 52
        averaged_monthly_mileage = (commute_single_distance * 2 + leisure_daily_additional_distance) * 5 * num_week / num_month
        expected_life_time = int(expected_life_mileage / averaged_monthly_mileage)
        monthly_fuel_cost = averaged_monthly_mileage / self.fuel_economy * average_oil_price
        toll_fee = 4 * 2 * 22
        
        monthly_insurrance_fee = annual_insurrance / num_month
        monthly_parking_fix_fee = annual_fix_parking / num_month
        Fixed_monthly_cost = monthly_fuel_cost + monthly_insurrance_fee + monthly_parking_fix_fee + toll_fee

        down_payment = DP_rate / 100 * self.price
        n = loan_term * 12 # loan_term in years
        loan_amount = self.price - down_payment
        r = interest_rate / 100 / 12
        monthly_payment = ((loan_amount * r)*(1 + r) ** n )/((1 + r) ** n - 1)
        m_p = [down_payment] # Real monthly cost 

        for i in range(1, n): 
            m_p.append(monthly_payment)
        for i in range(n, expected_life_time + 1):
            m_p.append(0)
        
        maintenance_1 = 0 # Annual maintenance fee in first year
        maintenance_2_5 = 0 # Annual maintenance fee in 2-5 year
        maintenance_6_10 = 1000 # Annual maintenance fee in 6-10 year

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
        
# 設定可選車款
cars = {
    "TOYOTA YARIS SEDAN 2024 E": Car("TOYOTA", "YARIS SEDAN 2024 E", "Patrol", 20.5, 63900, 0.15),
    "TOYOTA COROLLA 2024 XLI": Car("TOYOTA", "COROLLA 2024 XLI", "Patrol", 18.2, 74900, 0.15),
    "MAZDA 3": Car("MAZDA", "3", "Patrol", 15, 95000, 0.16),
    "TOYOTA Raize 1L": Car("TOYOTA", "Raize 1L", "Patrol", 20.6, 66900, 0.15),
    "NISSAN PATROL XE": Car("NISSAN", "PATROL XE", "Patrol", 8.5, 239900, 0.17),
    "2.5L RAV4 VXR":  Car("TOYOTA", "2.5L RAV4 VXR", "Hybrid", 22.2, 158399, 0.15),
    "Jolion": Car("Haval", "Jolion", "Patrol", 12.3, 49900, 0.18),
    "Dashing 1.5L": Car("Jetour", "Dashing 1.5L", "Patrol", 13.5,  65000, 0.18)
}

# 建立 Dash 應用
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Cost Of Driving Calculator"),
    
    html.Label("Select you car"),
    dcc.Dropdown(id='car-selection', options=[{'label': key, 'value': key} for key in cars.keys()], value=list(cars.keys())[0]),
    
    html.Label("One-way commute distance (km)"),
    dcc.Input(id='commute-distance', type='number', value=30),
    
    html.Label("Extra leisure travling distance per day (km)"),
    dcc.Input(id='leisure-distance', type='number', value=5),
    
    html.Label("Down payment rate (%)"),
    dcc.Input(id='dp-rate', type='number', value=20, step=1),
    
    html.Label("Interest Rate (%)"),
    dcc.Input(id='interest-rate', type='number', value=3, step=0.1),
    
    html.Label("Loan term"),
    dcc.Input(id='loan-term', type='number', value=5),
    
    html.Button("計算", id='calculate-btn', n_clicks=0),
    
    html.H2("Monthly cost of driving by selected car"),
    html.Div(id='monthly-cost-output'),
    
    html.H2("Monthly Cost Chart"),
    html.Img(id='cost-chart')
])

@app.callback(
    [Output('monthly-cost-output', 'children'), Output('cost-chart', 'src')],
    [Input('calculate-btn', 'n_clicks')],
    [dash.dependencies.State('car-selection', 'value'),
     dash.dependencies.State('commute-distance', 'value'),
     dash.dependencies.State('leisure-distance', 'value'),
     dash.dependencies.State('dp-rate', 'value'),
     dash.dependencies.State('interest-rate', 'value'),
     dash.dependencies.State('loan-term', 'value')]
)
def update_car_cost(n_clicks, car_model, commute_distance, leisure_distance, dp_rate, interest_rate, loan_term):
    car = cars[car_model]
    monthly_cost = car.calculate_averaged_monthly_price(commute_distance, leisure_distance)
    
    # 生成成本變化圖
    plt.figure()
    car.plot_real_monthly_price(commute_distance, leisure_distance, dp_rate, interest_rate, loan_term)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.read()).decode('utf-8')
    image_src = "data:image/png;base64,{}".format(encoded_image)
    
    return f"Averaged monthly cost: {monthly_cost:.2f} AED", image_src

if __name__ == '__main__':
    app.run_server(debug=True)
