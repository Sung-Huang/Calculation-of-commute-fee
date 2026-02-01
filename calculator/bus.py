from model import BusSpec, CommuteProfile


class BusCommuteCostCalculator:
    def calculate_single_trip_cost(self, vehicle: BusSpec, commute: CommuteProfile) -> float:
        return vehicle.boarding_fee_aed + vehicle.price_per_km_aed * commute.one_way_distance_km

    def calculate_monthly_cost(self, vehicle: BusSpec, commute: CommuteProfile) -> float:
        per_trip_cost = self.calculate_single_trip_cost(vehicle, commute)
        return (
            per_trip_cost
            * commute.round_trips_per_day
            * commute.workdays_per_week
            * commute.weeks_per_year
            / commute.months_per_year
        )
