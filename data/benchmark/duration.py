from __future__ import absolute_import
from __future__ import division
from typing import Any, Dict, List, Type, Union
from datetime import timedelta
import operator

from datetime import date
from datetime import datetime
from datetime import timedelta
from sqlite3 import Date
from typing import Type
import calendar
import math


from .constants import SECONDS_PER_DAY
from .constants import SECONDS_PER_HOUR
from .constants import SECONDS_PER_MINUTE
from .constants import US_PER_SECOND, MONTHS_PER_YEAR
from .constants import FRIDAY
from .constants import MONDAY
from .constants import MONTHS_PER_YEAR
from .constants import SATURDAY
from .constants import SUNDAY
from .constants import THURSDAY
from .constants import TUESDAY
from .constants import WEDNESDAY
from .constants import YEARS_PER_CENTURY
from .constants import YEARS_PER_DECADE

class PreciseDiff():
    years:int
    months:int
    days:int
    hours:int
    minutes:int
    seconds:int
    microseconds:int
    def __repr__(self):
        return (
            "{years} years "
            "{months} months "
            "{days} days "
            "{hours} hours "
            "{minutes} minutes "
            "{seconds} seconds "
            "{microseconds} microseconds"
        ).format(
            years=self.years(),
            months=self.months(),
            days=self.days(),
            hours=self.hours(),
            minutes=self.minutes(),
            seconds=self.seconds(),
            microseconds=self.microseconds(),
        )
def precise_diff(
    d1, d2
):  
    """
    Calculate a precise difference between two datetimes.

    :param d1: The first datetime
    :type d1: datetime.datetime or datetime.date

    :param d2: The second datetime
    :type d2: datetime.datetime or datetime.date

    :rtype: PreciseDiff
    """
    sign = 1

    if d1 == d2:
        return PreciseDiff(0, 0, 0, 0, 0, 0, 0, 0)
def _divide_and_round(a, b):
    """divide a by b and round result to the nearest integer

    When the ratio is exactly half-way between two integers,
    the even integer is returned.
    """
    # Based on the reference implementation for divmod_near
    # in Objects/longobject.c.
    q, r = divmod(a, b)
    # round up if either r / b > 0.5, or r / b == 0.5 and q is odd.
    # The expression r / b > 0.5 is equivalent to 2 * r > b if b is
    # positive, 2 * r < b if b negative.
    r *= 2
    greater_than_half = r > b if b > 0 else r < b
    if greater_than_half or r == b and q % 2 == 1:
        q += 1

    return q


class Duration(timedelta):
    """
    Replacement for the standard timedelta class.

    Provides several improvements over the base class.
    """

    _y:int = None
    _m:int = None
    _w:int = None
    _d:int = None
    _h:int = None
    _i:int = None
    _s:int = None
    _invert:int = None

    _total:int
    _microseconds:int
    _seconds:int
    _days:int 
    _remaining_days:int
    _weeks:int
    _months:int
    _years:int

    min:Duration
    max:Duration
    resolution:Duration
    def __new__(
        cls:Type[Duration],
        days:int=0,
        seconds:int=0,
        microseconds:int=0,
        milliseconds:int=0,
        minutes:int=0,
        hours:int=0,
        weeks:int=0,
        years:int=0,
        months:int=0,
    )->Duration:
        if not isinstance(years, int) or not isinstance(months, int):
            raise ValueError("Float year and months are not supported")

        self = timedelta.__new__(
            cls,
            days + years * 365 + months * 30,
            seconds,
            microseconds,
            milliseconds,
            minutes,
            hours,
            weeks,
        )

        # Intuitive normalization
        total = self.total_seconds() - (years * 365 + months * 30) * SECONDS_PER_DAY
        self._total = total

        m = 1
        if total < 0:
            m = -1

        self._microseconds = round(total % m * 1e6)
        self._seconds = abs(int(total)) % SECONDS_PER_DAY * m

        _days = abs(int(total)) // SECONDS_PER_DAY * m
        self._days = _days
        self._remaining_days = abs(_days) % 7 * m
        self._weeks = abs(_days) // 7 * m
        self._months = months
        self._years = years

        return self

    def total_minutes(self):
        return self.total_seconds() / SECONDS_PER_MINUTE

    def total_hours(self):
        return self.total_seconds() / SECONDS_PER_HOUR

    def total_days(self):
        return self.total_seconds() / SECONDS_PER_DAY

    def total_weeks(self):
        return self.total_days() / 7


    def total_seconds(self):
        days = 0

        if hasattr(self, "_years"):
            days += self._years * 365

        if hasattr(self, "_months"):
            days += self._months * 30

        if hasattr(self, "_remaining_days"):
            days += self._weeks * 7 + self._remaining_days
        else:
            days += self._days

        return int((
            (days * SECONDS_PER_DAY + self._seconds) * US_PER_SECOND
            + self._microseconds
        ) / US_PER_SECOND)


    def years(self):
        return self._years


    def months(self):
        return self._months


    def weeks(self):
        return self._weeks


    
    def days(self):
        return self._years * 365 + self._months * 30 + self._days


    def remaining_days(self):
        return self._remaining_days


    def hours(self):
        if self._h is None:
            seconds = self._seconds
            self._h = 0
            if abs(seconds) >= 3600:
                self._h = (abs(seconds) // 3600 % 24) * self._sign(seconds)

        return self._h


    def minutes(self):
        if self._i is None:
            seconds = self._seconds
            self._i = 0
            if abs(seconds) >= 60:
                self._i = (abs(seconds) // 60 % 60) * self._sign(seconds)

        return self._i


    def seconds(self):
        return self._seconds


    def remaining_seconds(self):
        if self._s is None:
            self._s = self._seconds
            self._s = abs(self._s) % 60 * self._sign(self._s)

        return self._s


    def microseconds(self):
        return self._microseconds


    def invert(self):
        if self._invert is None:
            self._invert = self.total_seconds() < 0

        return self._invert

    def in_weeks(self):
        return int(self.total_weeks())

    def in_days(self):
        return int(self.total_days())

    def in_hours(self):
        return int(self.total_hours())

    def in_minutes(self):
        return int(self.total_minutes())

    def in_seconds(self):
        return int(self.total_seconds())


 

    def _sign(self, value):
        if value < 0:
            return -1

        return 1

    def as_timedelta(self):
        """
        Return the interval as a native timedelta.

        :rtype: timedelta
        """
        return timedelta(seconds=self.total_seconds())

    # def __str__(self):
    #     return self.in_words()

    def __repr__(self):
        rep = "{}(".format(self.__class__.__name__)

        if self._years:
            rep += "years={}, ".format(self._years)

        if self._months:
            rep += "months={}, ".format(self._months)

        if self._weeks:
            rep += "weeks={}, ".format(self._weeks)

        if self._days:
            rep += "days={}, ".format(self._remaining_days)

        if self.hours:
            rep += "hours={}, ".format(self.hours)

        if self.minutes:
            rep += "minutes={}, ".format(self.minutes)

        if self.remaining_seconds:
            rep += "seconds={}, ".format(self.remaining_seconds)

        if self.microseconds:
            rep += "microseconds={}, ".format(self.microseconds)

        rep += ")"

        return rep.replace(", )", ")")

    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.total_seconds() + other.total_seconds())

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.total_seconds() - other.total_seconds())

        return NotImplemented

    def __neg__(self):
        return self.__class__(
            years=-self._years,
            months=-self._months,
            weeks=-self._weeks,
            days=-self._remaining_days,
            seconds=-self._seconds,
            microseconds=-self._microseconds,
        )

    def _to_microseconds(self):
        return (self._days * (24 * 3600) + self._seconds) * 1000000 + self._microseconds

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(
                years=self._years * other,
                months=self._months * other,
                seconds=self._total * other,
            )

        if isinstance(other, float):
            usec = self._to_microseconds()
            a, b = other.as_integer_ratio()

            return self.__class__(0, 0, _divide_and_round(usec * a, b))

        return NotImplemented

    __rmul__ = __mul__

    def __floordiv__(self, other):
        if not isinstance(other, (int, timedelta)):
            return NotImplemented
        
        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec // other._to_microseconds()

        if isinstance(other, int):
            return self.__class__(
                0,
                0,
                usec // other,
                years=self._years // other,
                months=self._months // other,
            )

    def __truediv__(self, other):
        if not isinstance(other, (int, float, timedelta)):
            return NotImplemented

        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec / other._to_microseconds()

        if isinstance(other, int):
            return self.__class__(
                0,
                0,
                _divide_and_round(usec, other),
                years=_divide_and_round(self._years, other),
                months=_divide_and_round(self._months, other),
            )

        if isinstance(other, float):
            a, b = other.as_integer_ratio()

            return self.__class__(
                0,
                0,
                _divide_and_round(b * usec, a),
                years=_divide_and_round(self._years * b, a),
                months=_divide_and_round(self._months, other),
            )

    __div__ = __floordiv__

    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = self._to_microseconds() % other._to_microseconds()

            return self.__class__(0, 0, r)

        return NotImplemented

    # def __divmod__(self, other):
    #     if isinstance(other, timedelta):
    #         q, r = divmod(self._to_microseconds(), other._to_microseconds())

    #         return q, self.__class__(0, 0, r)

    #     return NotImplemented



class Period(Duration):
    """
    Duration class that is aware of the datetimes that generated the
    time difference.
    """
    _invert:bool
    _absolute:bool
    _start:Union[date, datetime]
    _end:Union[date, datetime]
    _delta:PreciseDiff
    @classmethod
    def __new__(cls:Type[Period], start:Union[date, datetime], end:Union[date, datetime], absolute:bool=False)->Period:
        if isinstance(start, datetime) and isinstance(end, datetime):
            if (
                start.tzinfo is None
                and end.tzinfo is not None
                or start.tzinfo is not None
                and end.tzinfo is None
            ):
                raise TypeError("can't compare offset-naive and offset-aware datetimes")

        if absolute and start > end:
            end, start = start, end

        _start = start
        _end = end
        if isinstance(start, datetime):

            _start = datetime(
                start.year(),
                start.month(),
                start.day(),
                start.hour(),
                start.minute(),
                start.second(),
                start.microsecond(),
                tzinfo=start.tzinfo(),
            )
        elif isinstance(start, Date):
            _start = date(start.year(), start.month(), start.day)

        if isinstance(end, datetime):
            _end = datetime(
                end.year(),
                end.month(),
                end.day(),
                end.hour(),
                end.minute(),
                end.second(),
                end.microsecond(),
                tzinfo=end.tzinfo(),
            )
        elif isinstance(end, Date):
            _end = date(end.year(), end.month(), end.day)

        # Fixing issues with datetime.__sub__()
        # not handling offsets if the tzinfo is the same
        if (
            isinstance(_start, datetime)
            and isinstance(_end, datetime)
            and _start.tzinfo is _end.tzinfo
        ):
            if _start.tzinfo is not None:
                _start = (_start - start.utcoffset()).replace(tzinfo=None)

            if isinstance(end, datetime) and _end.tzinfo is not None:
                _end = (_end - end.utcoffset()).replace(tzinfo=None)

        delta = _end - _start

        return super(Period, cls).__new__(cls, seconds=delta.total_seconds())

    def __init__(self, start, end, absolute=False):
        super(Period, self).__init__()


        # if isinstance(start, datetime):
        #     _start = datetime(
        #         start.year(),
        #         start.month(),
        #         start.day(),
        #         start.hour(),
        #         start.minute(),
        #         start.second(),
        #         start.microsecond(),
        #         tzinfo=start.tzinfo(),
        #     )
        # else:
        _start = date(start.year(), start.month(), start.day())


        # if isinstance(end, datetime):
        #     _end = datetime(
        #         end.year(),
        #         end.month(),
        #         end.day(),
        #         end.hour(),
        #         end.minute(),
        #         end.second(),
        #         end.microsecond(),
        #         tzinfo=end.tzinfo(),
        #     )
        # else:
        _end = date(end.year(), end.month(), end.day())

        self._invert = False
        # if start > end:
        #     self._invert = True

            # if absolute:
            #     end, start = start, end
            #     _end, _start = _start, _end

        self._absolute = absolute
        self._start = start
        self._end = end
        self._delta = precise_diff(_start, _end)


    def years(self):
        return self._delta.years


    def months(self):
        return self._delta.months


    def weeks(self):
        return abs(self._delta.days) // 7 * self._sign(self._delta.days)


    def days(self):
        return self._days


    def remaining_days(self):
        return abs(self._delta.days) % 7 * self._sign(self._days)


    def hours(self):
        return self._delta.hours


    def minutes(self):
        return self._delta.minutes


    def start(self):
        return self._start


    def end(self):
        return self._end

    def in_years(self):
        """
        Gives the duration of the Period in full years.

        :rtype: int
        """
        return self.years()

    def in_months(self):
        """
        Gives the duration of the Period in full months.

        :rtype: int
        """
        return self.years() * MONTHS_PER_YEAR + self.months()

    def in_weeks(self):
        days = self.in_days()
        sign = 1

        if days < 0:
            sign = -1

        return sign * (abs(days) // 7)

    def in_days(self):
        return self._delta.days

    def in_words(self, locale=None, separator=" "):
        """
        Get the current interval in words in the current locale.

        Ex: 6 jours 23 heures 58 minutes

        :param locale: The locale to use. Defaults to current locale.
        :type locale: str

        :param separator: The separator to use between each unit
        :type separator: str

        :rtype: str
        """
        periods = [
            ("year", self.years()),
            ("month", self.months()),
            ("week", self.weeks()),
            ("day", self.remaining_days()),
            ("hour", self.hours()),
            ("minute", self.minutes()),
            ("second", self.remaining_seconds()),
        ]


        parts = []
        for period in periods:
            unit, count = period
            if abs(count) > 0:
                translation = locale.translation(
                    "units.{}.{}".format(unit, locale.plural(abs(count)))
                )
                parts.append(translation.format(count))

        if not parts:
            if abs(self.microseconds) > 0:
                unit = "units.second.{}".format(locale.plural(1))
                count = "{:.2f}".format(abs(self.microseconds) / 1e6)
            else:
                unit = "units.microsecond.{}".format(locale.plural(0))
                count = 0
            translation = locale.translation(unit)
            parts.append(translation.format(count))

        return parts

    def range(self, unit, amount=1):
        method = "add"
        op = operator.le
        if not self._absolute and self.invert:
            method = "subtract"
            op = operator.ge

        start, end = self.start, self.end

        i = amount
        while op(start, end):
            yield start

            start = getattr(self.start, method)(**{unit: i})

            i += amount

    def as_interval(self):
        """
        Return the Period as an Duration.

        :rtype: Duration
        """
        return Duration(seconds=self.total_seconds())

    def __iter__(self):
        return self.range("days")

    def __contains__(self, item):
        return self.start() <= item <= self.end()

    def __add__(self, other):
        return self.as_interval().__add__(other)

    __radd__ = __add__

    def __sub__(self, other):
        return self.as_interval().__sub__(other)

    def __neg__(self):
        return self.__class__(self.end(), self.start(), self._absolute)

    def __mul__(self, other):
        return self.as_interval().__mul__(other)

    __rmul__ = __mul__

    def __floordiv__(self, other):
        return self.as_interval().__floordiv__(other)

    def __truediv__(self, other):
        return self.as_interval().__truediv__(other)

    __div__ = __floordiv__

    def __mod__(self, other):
        return self.as_interval().__mod__(other)

    def __divmod__(self, other):
        return self.as_interval().__divmod__(other)

    def __abs__(self):
        return self.__class__(self.start(), self.end(), True)

    def __repr__(self):
        return "<Period [{} -> {}]>".format(self._start, self._end)

    def __str__(self):
        return self.__repr__()

    def _cmp(self, other):
        # Only needed for PyPy
        # assert isinstance(other, timedelta)

        if isinstance(other, Period):
            other = other.as_timedelta()

        td = self.as_timedelta()

        return 0 if td == other else 1 if td > other else -1

    def _getstate(self, protocol=3):
        start, end = self.start(), self.end()

        if self._invert and self._absolute:
            end, start = start, end

        return (start, end, self._absolute)

    def __reduce__(self):
        return self.__reduce_ex__(2)

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)

    def __hash__(self):
        return hash((self.start(), self.end(), self._absolute))

    def __eq__(self, other):
        if isinstance(other, Period):
            return (self.start(), self.end(), self._absolute) == (
                other.start(),
                other.end(),
                other._absolute,
            )
        else:
            return self.as_interval() == other



class DateTime(datetime.datetime, Date):


    _EPOCH:datetime = datetime.datetime(1970, 1, 1)

    _MODIFIERS_VALID_UNITS:List[str] = [
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "year",
        "decade",
        "century",
    ]

    _fold:int
    def __new__(
        cls,
        year,
        month,
        day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
        fold=0,
    ):
        self = datetime.datetime.__new__(
            cls, year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo
        )

        self._fold = fold

        return self

    
    # def now(cls, tz=None):  
    #     """
    #     Get a DateTime instance for the current date and time.
    #     """
    #     return pendulum.now(tz)

    
    # def utcnow(cls):  
    #     """
    #     Get a DateTime instance for the current date and time in UTC.
    #     """
    #     return pendulum.now(UTC)

    
    # def today(cls):  
    #     return pendulum.now()

    
    # def strptime(cls, time, fmt):  
    #     return pendulum.instance(datetime.datetime.strptime(time, fmt))

    # Getters/Setters

    def set(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        tz=None,
    ):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tz is None:
            tz = self.tz

        return Datetime(
            year, month, day, hour, minute, second, microsecond, tz=tz
        )


    
    def fold(self):
        return self._fold

    def timestamp(self):
        if self.tzinfo() is None:
            s = timestamp(self)

            return s + self.microsecond / 1e6
        else:
            kwargs = {"tzinfo": self.tzinfo}

            dt = datetime.datetime(
                self.year(),
                self.month(),
                self.day(),
                self.hour(),
                self.minute(),
                self.second(),
                self.microsecond(),
                **kwargs
            )
            return (dt - self._EPOCH).total_seconds()


    def float_timestamp(self):
        return self.timestamp()


    def int_timestamp(self):
        # Workaround needed to avoid inaccuracy
        # for far into the future datetimes
        kwargs = {"tzinfo": self.tzinfo}

        dt = datetime.datetime(
            self.year(),
            self.month(),
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
            self.microsecond(),
            **kwargs
        )

        delta = dt - self._EPOCH

        return delta.days * SECONDS_PER_DAY + delta.seconds


    def offset(self):
        return self.get_offset()


    def offset_hours(self):
        return self.get_offset() / SECONDS_PER_MINUTE / MINUTES_PER_HOUR


    def timezone(self):  
        if not isinstance(self.tzinfo(), Timezone):
            return

        return self.tzinfo


    def tz(self):  
        return self.timezone


    def timezone_name(self):  
        tz = self.timezone

        if tz is None:
            return None

        return tz.name


    def age(self):
        return self.date().diff(self.now(self.tz).date(), abs=False).in_years()

    def is_local(self):
        return self.offset == self.in_timezone(pendulum.local_timezone()).offset

    def is_utc(self):
        return self.offset == UTC.offset

    def is_dst(self):
        return self.dst() != datetime.timedelta()

    def get_offset(self):
        return int(self.utcoffset().total_seconds())

    def date(self):
        return Date(self.year(), self.month(), self.day)

    def time(self):
        return Time(self.hour(), self.minute(), self.second(), self.microsecond)

    def naive(self):  
        """
        Return the DateTime without timezone information.
        """
        return self.__class__(
            self.year(),
            self.month(),
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
            self.microsecond(),
        )

    def on(self, year, month, day):
        """
        Returns a new instance with the current date set to a different date.

        :param year: The year
        :type year: int

        :param month: The month
        :type month: int

        :param day: The day
        :type day: int

        :rtype: DateTime
        """
        return self.set(year=int(year), month=int(month), day=int(day))

    def at(self, hour, minute=0, second=0, microsecond=0):
        """
        Returns a new instance with the current time to a different time.

        :param hour: The hour
        :type hour: int

        :param minute: The minute
        :type minute: int

        :param second: The second
        :type second: int

        :param microsecond: The microsecond
        :type microsecond: int

        :rtype: DateTime
        """
        return self.set(
            hour=hour, minute=minute, second=second, microsecond=microsecond
        )

    def in_timezone(self, tz):  
        """
        Set the instance's timezone from a string or object.
        """
        tz = pendulum._safe_timezone(tz)

        return tz.convert(self, dst_rule=pendulum.POST_TRANSITION)

    def in_tz(self, tz):  
        """
        Set the instance's timezone from a string or object.
        """
        return self.in_timezone(tz)

    # STRING FORMATTING




    def __str__(self):
        return self.isoformat("T")

    def __repr__(self):
        us = ""
        if self.microsecond:
            us = ", {}".format(self.microsecond)

        repr_ = "{klass}(" "{year}, {month}, {day}, " "{hour}, {minute}, {second}{us}"

        if self.tzinfo is not None:
            repr_ += ", tzinfo={tzinfo}"

        repr_ += ")"

        return repr_.format(
            klass=self.__class__.__name__,
            year=self.year(),
            month=self.month(),
            day=self.day(),
            hour=self.hour(),
            minute=self.minute(),
            second=self.second(),
            us=us,
            tzinfo=self.tzinfo(),
        )

    # Comparisons
    def closest(self, dt1, dt2, *dts):
        """
        Get the farthest date from the instance.

        :type dt1: datetime.datetime
        :type dt2: datetime.datetime
        :type dts: list[datetime.datetime,]

        :rtype: DateTime
        """
        dt1 = pendulum.instance(dt1)
        dt2 = pendulum.instance(dt2)
        dts = [dt1, dt2] + [pendulum.instance(x) for x in dts]
        dts = [(abs(self - dt), dt) for dt in dts]

        return min(dts)[1]

    def farthest(self, dt1, dt2, *dts):
        """
        Get the farthest date from the instance.

        :type dt1: datetime.datetime
        :type dt2: datetime.datetime
        :type dts: list[datetime.datetime,]

        :rtype: DateTime
        """
        dt1 = pendulum.instance(dt1)
        dt2 = pendulum.instance(dt2)

        dts = [dt1, dt2] + [pendulum.instance(x) for x in dts]
        dts = [(abs(self - dt), dt) for dt in dts]

        return max(dts)[1]

    def is_future(self):
        """
        Determines if the instance is in the future, ie. greater than now.

        :rtype: bool
        """
        return self > self.now(self.timezone)

    def is_past(self):
        """
        Determines if the instance is in the past, ie. less than now.

        :rtype: bool
        """
        return self < self.now(self.timezone)

    def is_long_year(self):
        """
        Determines if the instance is a long year

        See link `https://en.wikipedia.org/wiki/ISO_8601#Week_dates`_

        :rtype: bool
        """
        return (
            Datetime(self.year(), 12, 28, 0, 0, 0, tz=self.tz).isocalendar()[1]
            == 53
        )

    def is_same_day(self, dt):
        """
        Checks if the passed in date is the same day
        as the instance current day.

        :type dt: DateTime or datetime or str or int

        :rtype: bool
        """
        dt = pendulum.instance(dt)

        return self.to_date_string() == dt.to_date_string()

    def is_anniversary(self, dt=None):
        """
        Check if its the anniversary.
        Compares the date/month values of the two dates.

        :rtype: bool
        """
        if dt is None:
            dt = self.now(self.tz)

        instance = pendulum.instance(dt)

        return (self.month(), self.day) == (instance.month(), instance.day)

    # the additional method for checking if today is the anniversary day
    # the alias is provided to start using a new name and keep the backward compatibility
    # the old name can be completely replaced with the new in one of the future versions
    is_birthday = is_anniversary

    # ADDITIONS AND SUBSTRACTIONS

    def add(
        self,
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
        Add a duration to the instance.

        If we're adding units of variable length (i.e., years, months),
        move forward from curren time,
        otherwise move forward from utc, for accuracy
        when moving across DST boundaries.
        """
        units_of_variable_length = any([years, months, weeks, days])

        current_dt = datetime.datetime(
            self.year(),
            self.month(),
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
            self.microsecond(),
        )
        if not units_of_variable_length:
            offset = self.utcoffset()
            if offset:
                current_dt = current_dt - offset

        dt = add_duration(
            current_dt,
            years=years,
            months=months,
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds,
        )

        if units_of_variable_length or self.tzinfo is None:
            return Datetime(
                dt.year(),
                dt.month(),
                dt.day(),
                dt.hour(),
                dt.minute(),
                dt.second(),
                dt.microsecond(),
                tz=self.tz,
            )

        dt = self.__class__(
            dt.year(),
            dt.month(),
            dt.day(),
            dt.hour(),
            dt.minute(),
            dt.second(),
            dt.microsecond(),
            tzinfo=UTC,
        )

        dt = self.tz.convert(dt)

        return self.__class__(
            dt.year(),
            dt.month(),
            dt.day(),
            dt.hour(),
            dt.minute(),
            dt.second(),
            dt.microsecond(),
            tzinfo=self.tz,
            fold=dt.fold,
        )

    def subtract(
        self,
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
        Remove duration from the instance.

        :param years: The number of years
        :type years: int

        :param months: The number of months
        :type months: int

        :param weeks: The number of weeks
        :type weeks: int

        :param days: The number of days
        :type days: int

        :param hours: The number of hours
        :type hours: int

        :param minutes: The number of minutes
        :type minutes: int

        :param seconds: The number of seconds
        :type seconds: int

        :param microseconds: The number of microseconds
        :type microseconds: int

        :rtype: DateTime
        """
        return self.add(
            years=-years,
            months=-months,
            weeks=-weeks,
            days=-days,
            hours=-hours,
            minutes=-minutes,
            seconds=-seconds,
            microseconds=-microseconds,
        )

    # Adding a final underscore to the method name
    # to avoid errors for PyPy which already defines
    # a _add_timedelta method
    def _add_timedelta_(self, delta):
        """
        Add timedelta duration to the instance.

        :param delta: The timedelta instance
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: DateTime
        """
        if isinstance(delta, pendulum.Period):
            return self.add(
                years=delta.years,
                months=delta.months,
                weeks=delta.weeks,
                days=delta.remaining_days,
                hours=delta.hours,
                minutes=delta.minutes,
                seconds=delta.remaining_seconds,
                microseconds=delta.microseconds,
            )
        elif isinstance(delta, pendulum.Duration):
            return self.add(
                years=delta.years, months=delta.months, seconds=delta._total
            )

        return self.add(seconds=delta.total_seconds())

    def _subtract_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: DateTime
        """
        if isinstance(delta, pendulum.Duration):
            return self.subtract(
                years=delta.years, months=delta.months, seconds=delta._total
            )

        return self.subtract(seconds=delta.total_seconds())

    # DIFFERENCES

    def diff(self, dt=None, abs=True):
        """
        Returns the difference between two DateTime objects represented as a Duration.

        :type dt: DateTime or None

        :param abs: Whether to return an absolute interval or not
        :type abs: bool

        :rtype: Period
        """
        if dt is None:
            dt = self.now(self.tz)

        return Period(self, dt, absolute=abs)

    def diff_for_humans(
        self,
        other=None,  
        absolute=False,  
        locale=None,  
    ):  
        """
        Get the difference in a human readable format in the current locale.

        When comparing a value in the past to default now:
        1 day ago
        5 months ago

        When comparing a value in the future to default now:
        1 day from now
        5 months from now

        When comparing a value in the past to another value:
        1 day before
        5 months before

        When comparing a value in the future to another value:
        1 day after
        5 months after
        """
        is_now = other is None

        if is_now:
            other = self.now()

        diff = self.diff(other)

        return pendulum.format_diff(diff, is_now, absolute, locale)

    # Modifiers
    def start_of(self, unit):
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * second: microsecond set to 0
        * minute: second and microsecond set to 0
        * hour: minute, second and microsecond set to 0
        * day: time to 00:00:00
        * week: date to first day of the week and time to 00:00:00
        * month: date to first day of the month and time to 00:00:00
        * year: date to first day of the year and time to 00:00:00
        * decade: date to first day of the decade and time to 00:00:00
        * century: date to first day of century and time to 00:00:00

        :param unit: The unit to reset to
        :type unit: str

        :rtype: DateTime
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "{}" for start_of()'.format(unit))

        return getattr(self, "_start_of_{}".format(unit))()

    def end_of(self, unit):
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * second: microsecond set to 999999
        * minute: second set to 59 and microsecond set to 999999
        * hour: minute and second set to 59 and microsecond set to 999999
        * day: time to 23:59:59.999999
        * week: date to last day of the week and time to 23:59:59.999999
        * month: date to last day of the month and time to 23:59:59.999999
        * year: date to last day of the year and time to 23:59:59.999999
        * decade: date to last day of the decade and time to 23:59:59.999999
        * century: date to last day of century and time to 23:59:59.999999

        :param unit: The unit to reset to
        :type unit: str

        :rtype: DateTime
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "%s" for end_of()' % unit)

        return getattr(self, "_end_of_%s" % unit)()

    def _start_of_second(self):
        """
        Reset microseconds to 0.

        :rtype: DateTime
        """
        return self.set(microsecond=0)

    def _end_of_second(self):
        """
        Set microseconds to 999999.

        :rtype: DateTime
        """
        return self.set(microsecond=999999)

    def _start_of_minute(self):
        """
        Reset seconds and microseconds to 0.

        :rtype: DateTime
        """
        return self.set(second=0, microsecond=0)

    def _end_of_minute(self):
        """
        Set seconds to 59 and microseconds to 999999.

        :rtype: DateTime
        """
        return self.set(second=59, microsecond=999999)

    def _start_of_hour(self):
        """
        Reset minutes, seconds and microseconds to 0.

        :rtype: DateTime
        """
        return self.set(minute=0, second=0, microsecond=0)

    def _end_of_hour(self):
        """
        Set minutes and seconds to 59 and microseconds to 999999.

        :rtype: DateTime
        """
        return self.set(minute=59, second=59, microsecond=999999)

    def _start_of_day(self):
        """
        Reset the time to 00:00:00

        :rtype: DateTime
        """
        return self.at(0, 0, 0, 0)

    def _end_of_day(self):
        """
        Reset the time to 23:59:59.999999

        :rtype: DateTime
        """
        return self.at(23, 59, 59, 999999)

    def _start_of_month(self):
        """
        Reset the date to the first day of the month and the time to 00:00:00.

        :rtype: DateTime
        """
        return self.set(self.year(), self.month(), 1, 0, 0, 0, 0)

    def _end_of_month(self):
        """
        Reset the date to the last day of the month
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        return self.set(self.year(), self.month(), self.days_in_month, 23, 59, 59, 999999)

    def _start_of_year(self):
        """
        Reset the date to the first day of the year and the time to 00:00:00.

        :rtype: DateTime
        """
        return self.set(self.year(), 1, 1, 0, 0, 0, 0)

    def _end_of_year(self):
        """
        Reset the date to the last day of the year
        and the time to 23:59:59.999999

        :rtype: DateTime
        """
        return self.set(self.year(), 12, 31, 23, 59, 59, 999999)

    def _start_of_decade(self):
        """
        Reset the date to the first day of the decade
        and the time to 00:00:00.

        :rtype: DateTime
        """
        year = self.year - self.year % YEARS_PER_DECADE
        return self.set(year, 1, 1, 0, 0, 0, 0)

    def _end_of_decade(self):
        """
        Reset the date to the last day of the decade
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        year = self.year - self.year % YEARS_PER_DECADE + YEARS_PER_DECADE - 1

        return self.set(year, 12, 31, 23, 59, 59, 999999)

    def _start_of_century(self):
        """
        Reset the date to the first day of the century
        and the time to 00:00:00.

        :rtype: DateTime
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + 1

        return self.set(year, 1, 1, 0, 0, 0, 0)

    def _end_of_century(self):
        """
        Reset the date to the last day of the century
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + YEARS_PER_CENTURY

        return self.set(year, 12, 31, 23, 59, 59, 999999)

    def _start_of_week(self):
        """
        Reset the date to the first day of the week
        and the time to 00:00:00.

        :rtype: DateTime
        """
        dt = self

        if self.day_of_week != pendulum._WEEK_STARTS_AT:
            dt = self.previous(pendulum._WEEK_STARTS_AT)

        return dt.start_of("day")

    def _end_of_week(self):
        """
        Reset the date to the last day of the week
        and the time to 23:59:59.

        :rtype: DateTime
        """
        dt = self

        if self.day_of_week != pendulum._WEEK_ENDS_AT:
            dt = self.next(pendulum._WEEK_ENDS_AT)

        return dt.end_of("day")

    def next(self, day_of_week=None, keep_time=False):
        """
        Modify to the next occurrence of a given day of the week.
        If no day_of_week is provided, modify to the next occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :param day_of_week: The next day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: DateTime
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError("Invalid day of week")

        if keep_time:
            dt = self
        else:
            dt = self.start_of("day")

        dt = dt.add(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.add(days=1)

        return dt

    def previous(self, day_of_week=None, keep_time=False):
        """
        Modify to the previous occurrence of a given day of the week.
        If no day_of_week is provided, modify to the previous occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :param day_of_week: The previous day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: DateTime
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError("Invalid day of week")

        if keep_time:
            dt = self
        else:
            dt = self.start_of("day")

        dt = dt.subtract(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.subtract(days=1)

        return dt

    def first_of(self, unit, day_of_week=None):
        """
        Returns an instance set to the first occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the first day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, "_first_of_{}".format(unit))(day_of_week)

    def last_of(self, unit, day_of_week=None):
        """
        Returns an instance set to the last occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the last day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, "_last_of_{}".format(unit))(day_of_week)

    def nth_of(self, unit, nth, day_of_week):
        """
        Returns a new instance set to the given occurrence
        of a given day of the week in the current unit.
        If the calculated occurrence is outside the scope of the current unit,
        then raise an error. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        dt = getattr(self, "_nth_of_{}".format(unit))(nth, day_of_week)
        if dt is False:
            raise PendulumException(
                "Unable to find occurence {} of {} in {}".format(
                    nth, self._days[day_of_week], unit
                )
            )

        return dt

    def _first_of_month(self, day_of_week):
        """
        Modify to the first occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the first day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int

        :rtype: DateTime
        """
        dt = self.start_of("day")

        if day_of_week is None:
            return dt.set(day=1)

        month = calendar.monthcalendar(dt.year(), dt.month)

        calendar_day = (day_of_week - 1) % 7

        if month[0][calendar_day] > 0:
            day_of_month = month[0][calendar_day]
        else:
            day_of_month = month[1][calendar_day]

        return dt.set(day=day_of_month)

    def _last_of_month(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the last day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        dt = self.start_of("day")

        if day_of_week is None:
            return dt.set(day=self.days_in_month)

        month = calendar.monthcalendar(dt.year(), dt.month)

        calendar_day = (day_of_week - 1) % 7

        if month[-1][calendar_day] > 0:
            day_of_month = month[-1][calendar_day]
        else:
            day_of_month = month[-2][calendar_day]

        return dt.set(day=day_of_month)

    def _nth_of_month(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current month. If the calculated occurrence is outside,
        the scope of the current month, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if nth == 1:
            return self.first_of("month", day_of_week)

        dt = self.first_of("month")
        check = dt.format("%Y-%M")
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if dt.format("%Y-%M") == check:
            return self.set(day=dt.day).start_of("day")

        return False

    def _first_of_quarter(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the first day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.on(self.year(), self.quarter * 3 - 2, 1).first_of(
            "month", day_of_week
        )

    def _last_of_quarter(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the last day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.on(self.year(), self.quarter * 3, 1).last_of("month", day_of_week)

    def _nth_of_quarter(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current quarter. If the calculated occurrence is outside,
        the scope of the current quarter, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if nth == 1:
            return self.first_of("quarter", day_of_week)

        dt = self.set(day=1, month=self.quarter * 3)
        last_month = dt.month
        year = dt.year
        dt = dt.first_of("quarter")
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if last_month < dt.month or year != dt.year:
            return False

        return self.on(self.year(), dt.month(), dt.day).start_of("day")

    def _first_of_year(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the first day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.set(month=1).first_of("month", day_of_week)

    def _last_of_year(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the last day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.set(month=MONTHS_PER_YEAR).last_of("month", day_of_week)

    def _nth_of_year(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current year. If the calculated occurrence is outside,
        the scope of the current year, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if nth == 1:
            return self.first_of("year", day_of_week)

        dt = self.first_of("year")
        year = dt.year
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if year != dt.year:
            return False

        return self.on(self.year(), dt.month(), dt.day).start_of("day")

    def average(self, dt=None):
        """
        Modify the current instance to the average
        of a given instance (default now) and the current instance.

        :type dt: DateTime or datetime

        :rtype: DateTime
        """
        if dt is None:
            dt = self.now(self.tz)

        diff = self.diff(dt, False)
        return self.add(
            microseconds=(diff.in_seconds() * 1000000 + diff.microseconds) // 2
        )

    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            return self._subtract_timedelta(other)

        if not isinstance(other, datetime.datetime):
            return NotImplemented

        if not isinstance(other, self.__class__):
            if other.tzinfo is None:
                other = pendulum.naive(
                    other.year(),
                    other.month(),
                    other.day(),
                    other.hour(),
                    other.minute(),
                    other.second(),
                    other.microsecond(),
                )
            else:
                other = pendulum.instance(other)

        return other.diff(self, False)

    def __rsub__(self, other):
        if not isinstance(other, datetime.datetime):
            return NotImplemented

        if not isinstance(other, self.__class__):
            if other.tzinfo is None:
                other = pendulum.naive(
                    other.year(),
                    other.month(),
                    other.day(),
                    other.hour(),
                    other.minute(),
                    other.second(),
                    other.microsecond(),
                )
            else:
                other = pendulum.instance(other)

        return self.diff(other, False)

    def __add__(self, other):
        if not isinstance(other, datetime.timedelta):
            return NotImplemented

        return self._add_timedelta_(other)

    def __radd__(self, other):
        return self.__add__(other)

    # Native methods override

    
    def fromtimestamp(cls, t, tz=None):
        return pendulum.instance(datetime.datetime.fromtimestamp(t, tz=tz), tz=tz)

    
    def utcfromtimestamp(cls, t):
        return pendulum.instance(datetime.datetime.utcfromtimestamp(t), tz=None)

    
    def fromordinal(cls, n):
        return pendulum.instance(datetime.datetime.fromordinal(n), tz=None)

    
    def combine(cls, date, time):
        return pendulum.instance(datetime.datetime.combine(date, time), tz=None)

    def astimezone(self, tz=None):
        return pendulum.instance(super(DateTime, self).astimezone(tz))

    def replace(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        tzinfo=True,
        fold=None,
    ):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        if fold is None:
            fold = self.fold

        transition_rule = pendulum.POST_TRANSITION
        if fold is not None:
            transition_rule = pendulum.PRE_TRANSITION
            if fold:
                transition_rule = pendulum.POST_TRANSITION

        return Datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond,
            tz=tzinfo,
            dst_rule=transition_rule,
        )

    def __getnewargs__(self):
        return (self,)

    def _getstate(self, protocol=3):
        return (
            self.year(),
            self.month(),
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
            self.microsecond(),
            self.tzinfo(),
        )

    def __reduce__(self):
        return self.__reduce_ex__(2)

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)

    def _cmp(self, other, **kwargs):
        # Fix for pypy which compares using this method
        # which would lead to infinite recursion if we didn't override
        kwargs = {"tzinfo": self.tz}


        dt = datetime.datetime(
            self.year(),
            self.month(),
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
            self.microsecond(),
            **kwargs
        )

        return 0 if dt == other else 1 if dt > other else -1

class Date(date):

    # Names of days of the week
    _days:Dict[int,str] = {
        SUNDAY: "Sunday",
        MONDAY: "Monday",
        TUESDAY: "Tuesday",
        WEDNESDAY: "Wednesday",
        THURSDAY: "Thursday",
        FRIDAY: "Friday",
        SATURDAY: "Saturday",
    }

    _MODIFIERS_VALID_UNITS:List[str] = ["day", "week", "month", "year", "decade", "century"]

    # Getters/Setters

    def set(self, year=None, month=None, day=None):
        return self.replace(year=year, month=month, day=day)


    def day_of_week(self):
        """
        Returns the day of the week (0-6).

        :rtype: int
        """
        return self.isoweekday() % 7


    def day_of_year(self):
        """
        Returns the day of the year (1-366).

        :rtype: int
        """
        k = 1 if self.is_leap_year() else 2

        return (275 * self.month()) // 9 - k * ((self.month() + 9) // 12) + self.day() - 30


    def week_of_year(self):
        return self.isocalendar()[1]


    def days_in_month(self):
        return calendar.monthrange(self.year(), self.month())[1]


    def week_of_month(self):
        first_day_of_month = self.replace(day=1)

        return self.week_of_year() - first_day_of_month.week_of_year() + 1


    def age(self):
        return self.diff(abs=False).in_years()


    def quarter(self):
        return int(math.ceil(self.month() / 3))

    # String Formatting

    def to_date_string(self):
        """
        Format the instance as date.

        :rtype: str
        """
        return self.strftime("%Y-%m-%d")

    def to_formatted_date_string(self):
        """
        Format the instance as a readable date.

        :rtype: str
        """
        return self.strftime("%b %d, %Y")

    def __repr__(self):
        return (
            "{klass}("
            "{year}, {month}, {day}"
            ")".format(
                klass=self.__class__.__name__,
                year=self.year(),
                month=self.month(),
                day=self.day(),
            )
        )

    # COMPARISONS

    def closest(self, dt1, dt2):
        """
        Get the closest date from the instance.

        :type dt1: Date or date
        :type dt2: Date or date

        :rtype: Date
        """
        dt1 = self.__class__(dt1.year(), dt1.month(), dt1.day())
        dt2 = self.__class__(dt2.year(), dt2.month(), dt2.day())

        if self.diff(dt1).in_seconds() < self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def farthest(self, dt1, dt2):
        """
        Get the farthest date from the instance.

        :type dt1: Date or date
        :type dt2: Date or date

        :rtype: Date
        """
        dt1 = self.__class__(dt1.year(), dt1.month(), dt1.day())
        dt2 = self.__class__(dt2.year(), dt2.month(), dt2.day())

        if self.diff(dt1).in_seconds() > self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def is_future(self):
        """
        Determines if the instance is in the future, ie. greater than now.

        :rtype: bool
        """
        return self > self.today()

    def is_past(self):
        """
        Determines if the instance is in the past, ie. less than now.

        :rtype: bool
        """
        return self < self.today()

    def is_leap_year(self):
        """
        Determines if the instance is a leap year.

        :rtype: bool
        """
        return calendar.isleap(self.year())

    def is_long_year(self):
        """
        Determines if the instance is a long year

        See link `<https://en.wikipedia.org/wiki/ISO_8601#Week_dates>`_

        :rtype: bool
        """
        return Date(self.year(), 12, 28).isocalendar()[1] == 53

    def is_same_day(self, dt):
        """
        Checks if the passed in date is the same day as the instance current day.

        :type dt: Date or date

        :rtype: bool
        """
        return self == dt

    def is_anniversary(self, dt=None):
        """
        Check if its the anniversary.

        Compares the date/month values of the two dates.

        :rtype: bool
        """
        if dt is None:
            dt = Date.today()

        instance = self.__class__(dt.year(), dt.month(), dt.day())

        return (self.month(), self.day()) == (instance.month(), instance.day)

    # the additional method for checking if today is the anniversary day
    # the alias is provided to start using a new name and keep the backward compatibility
    # the old name can be completely replaced with the new in one of the future versions
    is_birthday = is_anniversary

    # ADDITIONS AND SUBSTRACTIONS

    def add(self, years=0, months=0, weeks=0, days=0):
        """
        Add duration to the instance.

        :param years: The number of years
        :type years: int

        :param months: The number of months
        :type months: int

        :param weeks: The number of weeks
        :type weeks: int

        :param days: The number of days
        :type days: int

        :rtype: Date
        """
        # dt = add_duration(
        #     date(self.year(), self.month(), self.day()),
        #     years=years,
        #     months=months,
        #     weeks=weeks,
        #     days=days,
        # )

        return self.__class__(years, months, days)

    def subtract(self, years=0, months=0, weeks=0, days=0):
        """
        Remove duration from the instance.

        :param years: The number of years
        :type years: int

        :param months: The number of months
        :type months: int

        :param weeks: The number of weeks
        :type weeks: int

        :param days: The number of days
        :type days: int

        :rtype: Date
        """
        return self.add(years=-years, months=-months, weeks=-weeks, days=-days)

    def _add_timedelta(self, delta):
        """
        Add timedelta duration to the instance.

        :param delta: The timedelta instance
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: Date
        """
        # if isinstance(delta, pendulum.Duration):
        #     return self.add(
        #         years=delta.years,
        #         months=delta.months,
        #         weeks=delta.weeks,
        #         days=delta.remaining_days,
        #     )

        return self.add(days=delta.days)

    def _subtract_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: Date
        """
        # if isinstance(delta, pendulum.Duration):
        #     return self.subtract(
        #         years=delta.years,
        #         months=delta.months,
        #         weeks=delta.weeks,
        #         days=delta.remaining_days,
        #     )

        return self.subtract(days=delta.days)

    def __add__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented

        return self._add_timedelta(other)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self._subtract_timedelta(other)

        if not isinstance(other, date):
            return NotImplemented

        dt = self.__class__(other.year(), other.month(), other.day)

        return dt.diff(self, False)

    # DIFFERENCES

    def diff(self, dt=None, abs=True):
        """
        Returns the difference between two Date objects as a Period.

        :type dt: Date or None

        :param abs: Whether to return an absolute interval or not
        :type abs: bool

        :rtype: Period
        """
        if dt is None:
            dt = self.today()

        return Period(self, dt, absolute=abs)

    def diff_for_humans(self, other=None, absolute=False, locale=None):
        """
        Get the difference in a human readable format in the current locale.

        When comparing a value in the past to default now:
        1 day ago
        5 months ago

        When comparing a value in the future to default now:
        1 day from now
        5 months from now

        When comparing a value in the past to another value:
        1 day before
        5 months before

        When comparing a value in the future to another value:
        1 day after
        5 months after

        :type other: Date

        :param absolute: removes time difference modifiers ago, after, etc
        :type absolute: bool

        :param locale: The locale to use for localization
        :type locale: str

        :rtype: str
        """
        is_now = other is None

        if is_now:
            other = self.today()

        diff = self.diff(other)

        return diff

    # MODIFIERS

    def start_of(self, unit:str)->Date:
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * day: time to 00:00:00
        * week: date to first day of the week and time to 00:00:00
        * month: date to first day of the month and time to 00:00:00
        * year: date to first day of the year and time to 00:00:00
        * decade: date to first day of the decade and time to 00:00:00
        * century: date to first day of century and time to 00:00:00

        :param unit: The unit to reset to
        :type unit: str

        :rtype: Date
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "{}" for start_of()'.format(unit))

        return getattr(self, "_start_of_{}".format(unit))()

    def end_of(self, unit:str)->Date:
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * week: date to last day of the week
        * month: date to last day of the month
        * year: date to last day of the year
        * decade: date to last day of the decade
        * century: date to last day of century

        :param unit: The unit to reset to
        :type unit: str

        :rtype: Date
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "%s" for end_of()' % unit)

        return getattr(self, "_end_of_%s" % unit)()

    def _start_of_day(self):
        """
        Compatibility method.

        :rtype: Date
        """
        return self

    def _end_of_day(self):
        """
        Compatibility method

        :rtype: Date
        """
        return self

    def _start_of_month(self):
        """
        Reset the date to the first day of the month.

        :rtype: Date
        """
        return self.set(self.year(), self.month(), 1)

    def _end_of_month(self):
        """
        Reset the date to the last day of the month.

        :rtype: Date
        """
        return self.set(self.year(), self.month(), self.days_in_month())

    def _start_of_year(self):
        """
        Reset the date to the first day of the year.

        :rtype: Date
        """
        return self.set(self.year(), 1, 1)

    def _end_of_year(self):
        """
        Reset the date to the last day of the year.

        :rtype: Date
        """
        return self.set(self.year(), 12, 31)

    def _start_of_decade(self):
        """
        Reset the date to the first day of the decade.

        :rtype: Date
        """
        year = self.year() - self.year() % YEARS_PER_DECADE

        return self.set(year, 1, 1)

    def _end_of_decade(self):
        """
        Reset the date to the last day of the decade.

        :rtype: Date
        """
        year = self.year() - self.year() % YEARS_PER_DECADE + YEARS_PER_DECADE - 1

        return self.set(year, 12, 31)

    def _start_of_century(self):
        """
        Reset the date to the first day of the century.

        :rtype: Date
        """
        year = self.year() - 1 - (self.year() - 1) % YEARS_PER_CENTURY + 1

        return self.set(year, 1, 1)

    def _end_of_century(self):
        """
        Reset the date to the last day of the century.

        :rtype: Date
        """
        year = self.year() - 1 - (self.year() - 1) % YEARS_PER_CENTURY + YEARS_PER_CENTURY

        return self.set(year, 12, 31)

    def _start_of_week(self):
        """
        Reset the date to the first day of the week.

        :rtype: Date
        """
        dt = self

        if self.day_of_week() != 1:
            dt = self.previous(1)

        return dt.start_of("day")

    def _end_of_week(self):
        """
        Reset the date to the last day of the week.

        :rtype: Date
        """
        dt = self

        if self.day_of_week() != 1:
            dt = self.next(1)

        return dt.end_of("day")

    def next(self, day_of_week=None):
        """
        Modify to the next occurrence of a given day of the week.
        If no day_of_week is provided, modify to the next occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :param day_of_week: The next day of week to reset to.
        :type day_of_week: int or None

        :rtype: Date
        """
        if day_of_week is None:
            day_of_week = self.day_of_week()

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError("Invalid day of week")

        dt = self.add(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.add(days=1)

        return dt

    def previous(self, day_of_week=None):
        """
        Modify to the previous occurrence of a given day of the week.
        If no day_of_week is provided, modify to the previous occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :param day_of_week: The previous day of week to reset to.
        :type day_of_week: int or None

        :rtype: Date
        """
        if day_of_week is None:
            day_of_week = self.day_of_week()

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError("Invalid day of week")

        dt = self.subtract(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.subtract(days=1)

        return dt

    def first_of(self, unit:str, day_of_week:int=None)->Date:
        """
        Returns an instance set to the first occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the first day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: Date
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, "_first_of_{}".format(unit))(day_of_week)

    def last_of(self, unit:str, day_of_week:int=None)->Date:
        """
        Returns an instance set to the last occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the last day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: Date
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, "_last_of_{}".format(unit))(day_of_week)

    def nth_of(self, unit:str, nth:int, day_of_week:int)->Date:
        """
        Returns a new instance set to the given occurrence
        of a given day of the week in the current unit.
        If the calculated occurrence is outside the scope of the current unit,
        then raise an error. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type nth: int

        :type day_of_week: int or None

        :rtype: Date
        """
        if unit not in ["month", "quarter", "year"]:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        dt = getattr(self, "_nth_of_{}".format(unit))(nth, day_of_week)
        return dt

    def _first_of_month(self, day_of_week):
        """
        Modify to the first occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the first day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int

        :rtype: Date
        """
        dt = self

        if day_of_week is None:
            return dt.set(day=1)

        month = calendar.monthcalendar(dt.year(), dt.month())

        calendar_day = (day_of_week - 1) % 7

        if month[0][calendar_day] > 0:
            day_of_month = month[0][calendar_day]
        else:
            day_of_month = month[1][calendar_day]

        return dt.set(day=day_of_month)

    def _last_of_month(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the last day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Date
        """
        dt = self

        if day_of_week is None:
            return dt.set(day=self.days_in_month())

        month = calendar.monthcalendar(dt.year(), dt.month())

        calendar_day = (day_of_week - 1) % 7

        if month[-1][calendar_day] > 0:
            day_of_month = month[-1][calendar_day]
        else:
            day_of_month = month[-2][calendar_day]

        return dt.set(day=day_of_month)

    def _nth_of_month(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current month. If the calculated occurrence is outside,
        the scope of the current month, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Date
        """
        if nth == 1:
            return self.first_of("month", day_of_week)

        dt = self.first_of("month")
        check = dt.format("YYYY-MM")
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if dt.format("YYYY-MM") == check:
            return self.set(day=dt.day())

        return False

    def _first_of_quarter(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the first day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Date
        """
        return self.set(self.year(), self.quarter() * 3 - 2, 1).first_of(
            "month", day_of_week
        )

    def _last_of_quarter(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the last day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Date
        """
        return self.set(self.year(), self.quarter * 3, 1).last_of("month", day_of_week)

    def _nth_of_quarter(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current quarter. If the calculated occurrence is outside,
        the scope of the current quarter, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Date
        """
        if nth == 1:
            return self.first_of("quarter", day_of_week)

        dt = self.replace(self.year(), self.quarter() * 3, 1)
        last_month = dt.month()
        year = dt.year()
        dt = dt.first_of("quarter")
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if last_month < dt.month() or year != dt.year():
            return False

        return self.set(self.year(), dt.month(), dt.day())

    def _first_of_year(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the first day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Date
        """
        return self.set(month=1).first_of("month", day_of_week)

    def _last_of_year(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the last day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Date
        """
        return self.set(month=MONTHS_PER_YEAR).last_of("month", day_of_week)

    def _nth_of_year(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current year. If the calculated occurrence is outside,
        the scope of the current year, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Date
        """
        if nth == 1:
            return self.first_of("year", day_of_week)

        dt = self.first_of("year")
        year = dt.year()
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if year != dt.year():
            return False

        return self.set(self.year(), dt.month(), dt.day())

    def average(self, dt=None):
        """
        Modify the current instance to the average
        of a given instance (default now) and the current instance.

        :type dt: Date or date

        :rtype: Date
        """
        if dt is None:
            dt = Date.today()

        return self.add(days=int(self.diff(dt, False).in_days() / 2))

    # Native s override

    # @classmethod
    # def today(cls:Type[Date])->Date:
    #     return pendulum.today().date()

    # @classmethod
    # def fromtimestamp(cls:Type[Date], t:float)->Date:
    #     dt = super(Date, cls).fromtimestamp(t)

    #     return cls(dt.year(), dt.month(), dt.day())

    # @classmethod
    # def fromordinal(cls:Type[Date], n:int)->Date:
    #     dt = super(Date, cls).fromordinal(n)

    #     return cls(dt.year(), dt.month(), dt.day()())

    def replace(self, year=None, month=None, day=None):
        year = year if year is not None else self.year()
        month = month if month is not None else self.month()
        day = day if day is not None else self.day()

        return self.__class__(year, month, day)
