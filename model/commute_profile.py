from pydantic import BaseModel


class CommuteProfile(BaseModel):
    one_way_distance_km: float
    leisure_daily_distance_km: float = 0.0
    workdays_per_week: int = 5
    weeks_per_year: int = 52
    months_per_year: int = 12
    round_trips_per_day: int = 2
    working_days_per_month: int = 22
    waiting_minutes_per_trip: float = 5.0
    call_car: bool = False

    def monthly_commute_distance_km(self) -> float:
        return (
            ((self.one_way_distance_km * self.round_trips_per_day) + self.leisure_daily_distance_km)
            * self.workdays_per_week
            * self.weeks_per_year
            / self.months_per_year
        )
