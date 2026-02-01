from pathlib import Path

import dash
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

from calculator import CarCommuteCostCalculator, CarOwnershipCostCalculator
from model import CommuteProfile, load_car_specs

CAR_SPECS_PATH = Path(__file__).resolve().parent / "data" / "cars.json"
cars = load_car_specs(CAR_SPECS_PATH)
commute_calculator = CarCommuteCostCalculator()
ownership_calculator = CarOwnershipCostCalculator()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Cost Of Driving Calculator"),
        html.Label("Select you car"),
        dcc.Dropdown(
            id="car-selection",
            options=[{"label": key, "value": key} for key in cars.keys()],
            value=list(cars.keys())[0],
        ),
        html.Label("One-way commute distance (km)"),
        dcc.Input(id="commute-distance", type="number", value=30),
        html.Label("Extra leisure travling distance per day (km)"),
        dcc.Input(id="leisure-distance", type="number", value=5),
        html.Label("Down payment rate (%)"),
        dcc.Input(id="dp-rate", type="number", value=20, step=1),
        html.Label("Interest Rate (%)"),
        dcc.Input(id="interest-rate", type="number", value=3, step=0.1),
        html.Label("Loan term"),
        dcc.Input(id="loan-term", type="number", value=5),
        html.Button("Calculate", id="calculate-btn", n_clicks=0),
        html.H2("Monthly cost of driving by selected car"),
        html.Div(id="monthly-cost-output"),
        html.H2("Monthly Cost Chart"),
        dcc.Graph(id="cost-chart"),
    ]
)


@app.callback(
    [Output("monthly-cost-output", "children"), Output("cost-chart", "figure")],
    [Input("calculate-btn", "n_clicks")],
    [
        State("car-selection", "value"),
        State("commute-distance", "value"),
        State("leisure-distance", "value"),
        State("dp-rate", "value"),
        State("interest-rate", "value"),
        State("loan-term", "value"),
    ],
)
def update_car_cost(
    n_clicks,
    car_model,
    commute_distance,
    leisure_distance,
    dp_rate,
    interest_rate,
    loan_term,
):
    car = cars[car_model]
    commute = CommuteProfile(
        one_way_distance_km=commute_distance,
        leisure_daily_distance_km=leisure_distance,
    )
    monthly_cost = commute_calculator.calculate_monthly_cost(car, commute)
    total_m_p, expected_life_time = ownership_calculator.calculate_monthly_cost_series(
        car,
        commute,
        down_payment_rate=dp_rate,
        interest_rate=interest_rate,
        loan_term_years=loan_term,
    )

    fig = px.bar(
        x=[x for x in range(1, expected_life_time + 2)],
        y=total_m_p,
        labels={"x": "Month", "y": "Price in AED"},
        title=f"Real monthly cost of {car.brand} {car.model} {car.energy_type} by month",
    )

    return f"Averaged monthly cost: {monthly_cost:.2f} AED", fig


if __name__ == "__main__":
    app.run(debug=True)
