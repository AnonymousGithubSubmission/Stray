# class A:
#     _x:int
#     @property
#     def x(self):
#         return self._x

#     @x.setter
#     def x(self,val):
#         self._x = val

#     def g(self):
#         return self.x + 1

# def f(x):
#     if x is None:
#         x = 1
#     return x

from datetime import date,datetime, timedelta
from math import copysign
from typing import Tuple
DAYS_PER_MONTHS:Tuple[Tuple[int,int, int, int, int, int, int, int, int, int, int, int, int], Tuple[int,int, int, int, int, int, int, int, int, int, int, int, int]]= (
    (-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
    (-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
)


def is_leap(year):  
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
def _sign(x):
    return int(copysign(1, x))

def add_duration(
    dt,
    years=0,
    months=0,
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    microseconds=0,
):
    """
    Adds a duration to a date/datetime instance.
    """
    days += weeks * 7

    if (
        isinstance(dt, date)
        and not isinstance(dt, datetime)
        and any([hours])
    ):
        raise RuntimeError("Time elements cannot be added to a date instance.")

    # Normalizing
    if abs(microseconds) > 999999:
        s = _sign(microseconds)
        div, mod = divmod(microseconds * s, 1000000)
        microseconds = mod * s
        seconds += div * s

    if abs(seconds) > 59:
        s = _sign(seconds)
        div, mod = divmod(seconds * s, 60)
        seconds = mod * s
        minutes += div * s

    if abs(minutes) > 59:
        s = _sign(minutes)
        div, mod = divmod(minutes * s, 60)
        minutes = mod * s
        hours += div * s

    if abs(hours) > 23:
        s = _sign(hours)
        div, mod = divmod(hours * s, 24)
        hours = mod * s
        days += div * s

    if abs(months) > 11:
        s = _sign(months)
        div, mod = divmod(months * s, 12)
        months = mod * s
        years += div * s

    year = dt.year() + years
    month = dt.month()

    if months:
        month += months
        if month > 12:
            year += 1
            month -= 12
        elif month < 1:
            year -= 1
            month += 12

    day = min(DAYS_PER_MONTHS[int(is_leap(year))][month], dt.day())

    dt = dt.replace(year=year, month=month, day=day)

    return dt + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )

