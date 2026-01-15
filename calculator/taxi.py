from model.commute_profile import CommuteProfile
from model.vehicle import TaxiSpec


class TaxiCommuteCostCalculator:
    def calculate_single_trip_cost(self, vehicle: TaxiSpec, commute: CommuteProfile) -> float:
        base_cost = (
            commute.one_way_distance_km * vehicle.price_per_km_aed
            + vehicle.flagfall_aed
            + vehicle.waiting_fee_per_min_aed * commute.waiting_minutes_per_trip
        )
        if commute.call_car:
            base_cost += vehicle.call_fee_aed
        return base_cost

    def calculate_monthly_cost(self, vehicle: TaxiSpec, commute: CommuteProfile) -> float:
        per_trip_cost = self.calculate_single_trip_cost(vehicle, commute)
        return (
            per_trip_cost
            * commute.round_trips_per_day
            * commute.workdays_per_week
            * commute.weeks_per_year
            / commute.months_per_year
        )
