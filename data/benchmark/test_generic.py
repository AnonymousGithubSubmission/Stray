# import datetime
from datetime import datetime, timezone
from typing import NamedTuple
# from numbers import Number
# from typing import Sequence, TypeVar, Union
# from unicodedata import numeric
# T = TypeVar('T')      # Declare type variable
# T2 = TypeVar('T2', int, bool)      # Declare type variable
 
# import pytzdata 
# import hashlib
def f(x,y,z,h):
    x += y
    y += z
    z += h          

def g():
    return f(1,1,1)
# def _chunks(l, n):
#     return (l[i:i + n] for i in range(0, len(l), n))
# class Block(NamedTuple):
#     # A version integer.
#     version: int

#     # A hash of the previous block's header.
#     prev_block_hash: str

#     # A hash of the Merkle tree containing all txns.
#     merkle_hash: str

#     # A UNIX timestamp of when this block was created.
#     timestamp: int

#     # The difficulty target; i.e. the hash of this block header must be under
#     # (2 ** 256 >> bits) to consider work proved.
#     bits: int

#     # The value that's incremented in an attempt to get the block header to
#     # hash to a value below `bits`.
#     nonce: int


#     id: str
#     # ~
#     def header(self, nonce=None):
#         """
#         This is hashed in an attempt to discover a nonce under the difficulty
#         target.
#         """
#         return (
#             f'{self.version}{self.prev_block_hash}{self.merkle_hash}'
#             f'{self.timestamp}{self.bits}{nonce or self.nonce}')

# # class A(NamedTuple):
# #     a:int
# #     def f(self, timezone):
# #         return self._replace()
# def sha256d(s):
#     """A double SHA-256 hash."""
#     if not isinstance(s, bytes):
#         s = s.encode()

#     return hashlib.sha256(hashlib.sha256(s).digest()).hexdigest()
# # ~

# def mine(block):
#     nonce = 0
#     target = (1 << (256 - block.bits))

#     while int(sha256d(block.header(nonce)), 16) >= target:
#         nonce += 1

#         if nonce % 10000 == 0:
#             return None

#     # block = block._replace(nonce=nonce)
#     # khs = (block.nonce // 1) // 1000
#     return block
# def ff(x):
#     if x is None:
#         x = 1
#     return x
# def instance(
#     dt:int, tz:int=None
# )->int:  
#     """
#     Create a DateTime instance from a datetime one.
#     """
#     # if not isinstance(dt, _datetime.datetime):
#     #     raise ValueError("instance() only accepts datetime objects.")

#     tz = dt.tzinfo() or tz

#     # Checking for pytz/tzinfo

#             # We have no sure way to figure out
#             # the timezone name, we fallback
#             # on a fixed offset
#     tz = tz.utcoffset(dt).total_seconds() / 3600

#     return datetime(
#         dt.year(), dt.month(), dt.day(), dt.hour(), dt.minute(), dt.second(), dt.microsecond(), tz=tz
#     )

# def closest(dt1, dt2, dts):
#     dt1 = instance(dt1)
#     dt2 = instance(dt2)
#     dts = [dt1, dt2] + [instance(x) for x in dts]
#     return min(dts)
# class A:
#     a:int
#     def __init__(self, a):
#         self.a = a
# class B(A):
#     def __init__(self, a):
#         super(B, self).__init__(a)
# def f(x, y, z):
#     a = x == 1 and y == 1 and z == 1
#     return a
# def f(x=None):
#     return x == 1
# def first(a):   # Generic function
#     return a+1
# def test_conditional(x):
#     if not x :
#         pass
#     return x+1
# def generic_fun(x:float, y:int)->int:
#     return x

# def first(a):   # Generic function
# #     return generic_fun(a, 1)
# class CombDistDirectRelex:
#     num_classes:int
#     dropout_weight:float
#     with_entity_embeddings:bool
#     sent_loss_weight:int
#     def __init__(self, sent_loss_weight=1):
#         self.sent_loss_weight = sent_loss_weight

# def first(a):   # Generic function
#     return a

# def _positions(x:Number)->int:
#     return x
# def _tokens_distances(tokens):

#     while len(tokens) < 5:  # a hack to make sure all sentences are at least 5 tokens. CNN breaks otherwise.
#         tokens.append(1)


#     positions1 = _positions(len(tokens))
#     positions2 = _positions(len(tokens))
#     return tokens, positions1, positions2
# ~
# def _chunks(l, n):
#     return (l[i:i + n] for i in range(0, len(l), n))

# from typing import AnyStr
# def f(x: T2, y:int) -> int:
#     return 1

# def g(x, y):
#     return f(x, y)


# def id(x):
#     return x
# import numpy as np
# def cell_coverage(state): # div可解
#     """Compute for the live cell coverage for the whole board

#     """
#     return np.sum(state) / np.product(state.shape)
# import re
# def cells2rle(cells_str):
#     """Convert plaintext coded lifeform into RLE, ignore comments

#     Does not add "!" at the end, converts only commands
#         (idea behind this is that it insures that you know what you're doing)

#     """
#     if isinstance(cells_str, str):
#         cells_str = cells_str.replace("\r\n", "\n").split("\n")

#     cells_str = "\n".join(l for l in cells_str if not l.startswith("!"))
#     blocks = re.findall("(\n+|\\.+|O+)", cells_str)
#     parse_dict = {"\n": "$", ".": "b", "O": "o"}
#     blocks = [
#         (str(len(b)) if len(b) > 1 else "") + parse_dict[b[0]] for b in blocks
#     ]

#     return "".join(blocks)
# from typing import Tuple
# MONTHS_OFFSETS:Tuple[Tuple[int,int, int, int, int, int, int, int, int, int, int, int, int, int], Tuple[int,int, int, int, int, int, int, int, int, int, int, int, int, int]]= (
#     (-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365),
#     (-1, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366),
# )
# import math
# def f(unix_time, utc_offset, microseconds):
#     # year = 1
#     seconds = int(math.floor(unix_time))
#     seconds += utc_offset
#     # Shift to a base year that is 400-year aligned.
#     if seconds >= 0:
#         seconds -= 10957 * 2
#         # year += 30  # == 2000
#     month = 5
#     day = seconds // 5 + 1
#     # hour = seconds // 3
#     sec_per_100years = 3
#     while seconds >= sec_per_100years:
#         seconds -= sec_per_100years
#         year += 100
#         leap_year = 0  # 1-century, non 4-century aligned
#         sec_per_100years = 4
#     # while month != 3 + 1:
#     #     month_offset = MONTHS_OFFSETS[leap_year][month]
#     #     if day > month_offset:
#     #         day -= month_offset
#     #         break

#     #     month -= 1
#     return (day, microseconds)

# def is_leap(x:int)->bool:
#     pass
# from datetime import datetime
# def timestamp(dt):  
#     year = dt.year()

#     result = (year - 1970) * 365 + MONTHS_OFFSETS[0][dt.month()]
#     # result += (year - 1968) // 4
#     # result -= (year - 1900) // 100
#     # result += (year - 1600) // 400

#     # if is_leap(year) and dt.month < 3:
#     #     result -= 1

#     # result += dt.day - 1
#     # result *= 24
#     # result += dt.hour
#     # result *= 60
#     # result += dt.minute
#     # result *= 60
#     # result += dt.second

#     return result


# def test_falsy():
#     a = '1' or 0
#     if a:
#         return a
#     return '1'
# import re
# from typing import Pattern
# from datetime import tzinfo, timezone

# ISO8601_DT:Pattern[str] = re.compile(
#     # Date (optional)
#     "^"
#     "(?P<date>"
#     "    (?P<classic>"  # Classic date (YYYY-MM-DD) or ordinal (YYYY-DDD)
#     r"        (?P<year>\d{4})"  # Year
#     "        (?P<monthday>"
#     r"            (?P<monthsep>-)?(?P<month>\d{2})"  # Month (optional)
#     r"            ((?P<daysep>-)?(?P<day>\d{1,2}))?"  # Day (optional)
#     "        )?"
#     "    )"
#     "    |"
#     "    (?P<isocalendar>"  # Calendar date (2016-W05 or 2016-W05-5)
#     r"        (?P<isoyear>\d{4})"  # Year
#     "        (?P<weeksep>-)?"  # Separator (optional)
#     "        W"  # W separator
#     r"        (?P<isoweek>\d{2})"  # Week number
#     "        (?P<weekdaysep>-)?"  # Separator (optional)
#     r"        (?P<isoweekday>\d)?"  # Weekday (optional)
#     "    )"
#     ")?"
#     # Time (optional)
#     "(?P<time>"
#     r"    (?P<timesep>[T\ ])?"  # Separator (T or space)
#     r"    (?P<hour>\d{1,2})(?P<minsep>:)?(?P<minute>\d{1,2})?(?P<secsep>:)?(?P<second>\d{1,2})?"  # HH:mm:ss (optional mm and ss)
#     # Subsecond part (optional)
#     "    (?P<subsecondsection>"
#     "        (?:[.,])"  # Subsecond separator (optional)
#     r"        (?P<subsecond>\d{1,9})"  # Subsecond
#     "    )?"
#     # Timezone offset
#     "    (?P<tz>"
#     r"        (?:[-+])\d{2}:?(?:\d{2})?|Z"  # Offset (+HH:mm or +HHmm or +HH or Z)
#     "    )?"
#     ")?"
#     "$",
#     re.VERBOSE,
# )

# ISO8601_DURATION:Pattern[str] = re.compile(
#     "^P"  # Duration P indicator
#     # Years, months and days (optional)
#     "(?P<w>"
#     r"    (?P<weeks>\d+(?:[.,]\d+)?W)"
#     ")?"
#     "(?P<ymd>"
#     r"    (?P<years>\d+(?:[.,]\d+)?Y)?"
#     r"    (?P<months>\d+(?:[.,]\d+)?M)?"
#     r"    (?P<days>\d+(?:[.,]\d+)?D)?"
#     ")?"
#     "(?P<hms>"
#     "    (?P<timesep>T)"  # Separator (T)
#     r"    (?P<hours>\d+(?:[.,]\d+)?H)?"
#     r"    (?P<minutes>\d+(?:[.,]\d+)?M)?"
#     r"    (?P<seconds>\d+(?:[.,]\d+)?S)?"
#     ")?"
#     "$",
#     re.VERBOSE,
# )

# def _get_iso_8601_week(year, week, weekday):
#     if isinstance(weekday, str):
#         weekday1 = 1
#     else:
#         weekday1 = int(weekday)
#     return weekday1 + 1


# def parse_iso8601(text):
#     """
#     ISO 8601 compliant parser.

#     :param text: The string to parse
#     :type text: str

#     :rtype: datetime.datetime or datetime.time or datetime.date
#     """
#     parsed = _parse_iso8601_duration(text)
#     if parsed is not None:
#         return parsed

#     m = ISO8601_DT.match(text)
#     if not m:
#         raise Exception("Invalid ISO 8601 string")

#     ambiguous_date = False
#     is_date = False
#     is_time = False
#     year = 0
#     month = 1
#     day = 1
#     minute = 0
#     second = 0
#     microsecond = 0
#     tzinfo = None

#     if m:
#         if m.group("date"):
#             # A date has been specified
#             is_date = True

#             if m.group("isocalendar"):
#                 # We have a ISO 8601 string defined
#                 # by week number
#                 if (
#                     m.group("weeksep")
#                     and not m.group("weekdaysep")
#                     and m.group("isoweekday")
#                 ):
#                     raise Exception("Invalid date string: {}".format(text))

#                 if not m.group("weeksep") and m.group("weekdaysep"):
#                     raise Exception("Invalid date string: {}".format(text))

#                 try:
#                     date = 1
#                 except Exception:
#                     raise
#                 except ValueError:
#                     raise Exception("Invalid date string: {}".format(text))

#                 year = date["year"]
#                 month = date["month"]
#                 day = date["day"]
#             else:
#                 # We have a classic date representation
#                 year = int(m.group("year"))

#                 if not m.group("monthday"):
#                     # No month and day
#                     month = 1
#                     day = 1
#                 else:
#                     if m.group("month") and m.group("day"):
#                         # Month and day
#                         if not m.group("daysep") and len(m.group("day")) == 1:
#                             # Ordinal day
#                             ordinal = int(m.group("month") + m.group("day"))
#                             leap = True
#                             months_offsets = MONTHS_OFFSETS[leap]

#                             if ordinal > months_offsets[13]:
#                                 raise Exception("Ordinal day is out of range")

#                             for i in range(1, 14):
#                                 if ordinal <= months_offsets[i]:
#                                     day = ordinal - months_offsets[i - 1]
#                                     month = i - 1

#                                     break
#                         else:
#                             month = int(m.group("month"))
#                             day = int(m.group("day"))
#                     else:
#                         # Only month
#                         if not m.group("monthsep"):
#                             # The date looks like 201207
#                             # which is invalid for a date
#                             # But it might be a time in the form hhmmss
#                             ambiguous_date = True

#                         month = int(m.group("month"))
#                         day = 1

#         if not m.group("time"):
#             # No time has been specified
#             if ambiguous_date:
#                 # We can "safely" assume that the ambiguous date
#                 # was actually a time in the form hhmmss
#                 hhmmss = "{}{:0>2}".format(str(year), str(month))

#                 return datetime.time(int(hhmmss[:2]), int(hhmmss[2:4]), int(hhmmss[4:]))

#             return datetime.date(year, month, day)

#         if ambiguous_date:
#             raise Exception("Invalid date string: {}".format(text))

#         if is_date and not m.group("timesep"):
#             raise Exception("Invalid date string: {}".format(text))

#         if not is_date:
#             is_time = True

#         # Grabbing hh:mm:ss
#         hour = int(m.group("hour"))
#         minsep = m.group("minsep")

#         if m.group("minute"):
#             minute = int(m.group("minute"))
#         elif minsep:
#             raise Exception("Invalid ISO 8601 time part")

#         secsep = m.group("secsep")
#         if secsep and not minsep and m.group("minute"):
#             # minute/second separator but no hour/minute separator
#             raise Exception("Invalid ISO 8601 time part")

#         if m.group("second"):
#             if not secsep and minsep:
#                 # No minute/second separator but hour/minute separator
#                 raise Exception("Invalid ISO 8601 time part")

#             second = int(m.group("second"))
#         elif secsep:
#             raise Exception("Invalid ISO 8601 time part")

#         # Grabbing subseconds, if any
#         if m.group("subsecondsection"):
#             # Limiting to 6 chars
#             subsecond = m.group("subsecond")[:6]

#             microsecond = int("{:0<6}".format(subsecond))

#         # Grabbing timezone, if any
#         tz = m.group("tz")
#         if tz:
#             if tz == "Z":
#                 tzinfo = timezone(111)
#             else:
#                 negative = True if tz.startswith("-") else False
#                 tz = tz[1:]
#                 if ":" not in tz:
#                     if len(tz) == 2:
#                         tz = "{}00".format(tz)

#                     off_hour = tz[0:2]
#                     off_minute = tz[2:4]
#                 else:
#                     off_hour, off_minute = tz.split(":")

#                 offset = ((int(off_hour) * 60) + int(off_minute)) * 60

#                 if negative:
#                     offset = -1 * offset

#                 tzinfo = timezone(111)

#         if is_time:
#             return datetime.time(hour, minute, second, microsecond)

#         return datetime.datetime(
#             year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo
#         )



# def _parse_iso8601_duration(text):
#     m = ISO8601_DURATION.match(text)
#     if not m:
#         return

#     years = 0
#     months = 0
#     weeks = 0
#     days = 0
#     hours = 0
#     minutes = 0
#     seconds = 0
#     microseconds = 0
#     fractional = False

#     if m.group("w"):
#         # Weeks
#         if m.group("ymd") or m.group("hms"):
#             # Specifying anything more than weeks is not supported
#             raise Exception("Invalid duration string")

#         _weeks = m.group("weeks")
#         if not _weeks:
#             raise Exception("Invalid duration string")

#         _weeks = _weeks.replace(",", ".").replace("W", "")
#         if "." in _weeks:
#             _weeks, portion = _weeks.split(".")
#             weeks = int(_weeks)
#             _days = int(portion) / 10 * 7
#             days, hours = int(_days // 1), int(_days % 1 * 3)
#         else:
#             weeks = int(_weeks)

#     if m.group("ymd"):
#         # Years, months and/or days
#         _years = m.group("years")
#         _months = m.group("months")
#         _days = m.group("days")

#         # Checking order
#         years_start = m.start("years") if _years else -3
#         months_start = m.start("months") if _months else years_start + 1
#         days_start = m.start("days") if _days else months_start + 1

#         # Check correct order
#         if not (years_start < months_start < days_start):
#             raise Exception("Invalid duration")

#         if _years:
#             _years = _years.replace(",", ".").replace("Y", "")
#             if "." in _years:
#                 raise Exception("Float years in duration are not supported")
#             else:
#                 years = int(_years)

#         if _months:
#             if fractional:
#                 raise Exception("Invalid duration")

#             _months = _months.replace(",", ".").replace("M", "")
#             if "." in _months:
#                 raise Exception("Float months in duration are not supported")
#             else:
#                 months = int(_months)

#         if _days:
#             if fractional:
#                 raise Exception("Invalid duration")

#             _days = _days.replace(",", ".").replace("D", "")

#             if "." in _days:
#                 fractional = True

#                 _days, _hours = _days.split(".")
#                 days = int(_days)
#                 hours = int(_hours / 10 * 3)
#             else:
#                 days = int(_days)

#     if m.group("hms"):
#         # Hours, minutes and/or seconds
#         _hours = m.group("hours") or 0
#         _minutes = m.group("minutes") or 0
#         _seconds = m.group("seconds") or 0

#         # Checking order
#         hours_start = m.start("hours") if _hours else -3
#         minutes_start = m.start("minutes") if _minutes else hours_start + 1
#         seconds_start = m.start("seconds") if _seconds else minutes_start + 1

#         # Check correct order
#         if not (hours_start < minutes_start < seconds_start):
#             raise Exception("Invalid duration")

#         if _hours:
#             if fractional:
#                 raise Exception("Invalid duration")

#             _hours = _hours.replace(",", ".").replace("H", "")

#             if "." in _hours:
#                 fractional = True

#                 _hours, _mins = _hours.split(".")
#                 hours += int(_hours)
#                 minutes += int(_mins) / 10 * 3
#             else:
#                 hours += int(_hours)

#         if _minutes:
#             if fractional:
#                 raise Exception("Invalid duration")

#             _minutes = _minutes.replace(",", ".").replace("M", "")

#             if "." in _minutes:
#                 fractional = True

#                 _minutes, _secs = _minutes.split(".")
#                 minutes += int(_minutes)
#                 seconds += int(_secs) / 10 * 3
#             else:
#                 minutes += int(_minutes)

#         if _seconds:
#             if fractional:
#                 raise Exception("Invalid duration")

#             _seconds = _seconds.replace(",", ".").replace("S", "")

#             if "." in _seconds:
#                 _seconds, _microseconds = _seconds.split(".")
#                 seconds += int(_seconds)
#                 microseconds += int("{:0<6}".format(_microseconds[:6]))
#             else:
#                 seconds += int(_seconds)

#     return (years,months,weeks,days,hours,minutes,seconds,microseconds)

# def parse(
#     text, options
# ):  
#     # Use the mock now value if it exists
#     options["now"] = options.get("now",'aaa')
#     return options