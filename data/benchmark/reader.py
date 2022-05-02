import os

from collections import namedtuple
from struct import unpack
from typing import IO, Union
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import pytzdata

from pytzdata.exceptions import TimezoneNotFound


from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
from typing import Optional
from typing import TypeVar
from typing import overload
from typing import List, Dict, Tuple
def read(a:str, extended=True)->Timezone:
    pass

def local_time(a:int, b:int, c:int)->Tuple[int, int, int, int, int, int, int]:
    pass
def timestamp(dt:datetime)->int:
    pass
_HAS_FOLD:bool=True

POST_TRANSITION = "post"
PRE_TRANSITION = "pre"
TRANSITION_ERROR = "error"

_datetime = datetime
_D = TypeVar("_D", bound=datetime)



class TransitionType:

    _offset:int
    _is_dst:bool
    _abbr:str
    _utcoffset:timedelta
    def __init__(self, offset, is_dst, abbr):
        self._offset = offset
        self._is_dst = is_dst
        self._abbr = abbr

        self._utcoffset = timedelta(seconds=offset)


    def offset(self):  
        return self._offset


    def abbreviation(self):  

        return self._abbr

    def is_dst(self):  
        return self._is_dst

    def utcoffset(self):  
        return self._utcoffset

    def __repr__(self):  
        return "TransitionType({}, {}, {})".format(
            self._offset, self._is_dst, self._abbr
        )



class Transition:
    _at:int
    _ttype:TransitionType
    _previous:Transition
    _local:int
    _fix:int
    _to:int
    _to_utc:int
    _utcoffset:timedelta
    def __init__(
        self,
        at,  
        ttype,  
        previous,  
    ):
        self._at = at

        if previous:
            self._local = at + previous._ttype.offset()
        else:
            self._local = at + ttype.offset()

        self._ttype = ttype
        self._previous = previous

        if self._previous:
            self._fix = self._ttype.offset() - self._previous._ttype.offset()
        else:
            self._fix = 0

        self._to = self._local + self._fix
        self._to_utc = self._at + self._fix
        self._utcoffset = timedelta(seconds=ttype.offset())


    def at(self):  
        return self._at


    def local(self):  
        return self._local


    def to(self):  
        return self._to


    def to_utc(self):  
        return self._to


    def ttype(self):  
        return self._ttype


    def previous(self):  
        return self._previous


    def fix(self):  
        return self._fix

    def is_ambiguous(self, stamp):  
        return self._to <= stamp < self._local

    def is_missing(self, stamp):  
        return self._local <= stamp < self._to

    def utcoffset(self):  
        return self._utcoffset

    def __contains__(self, stamp):  
        if self.previous() is None:
            return stamp < self.local()

        return self.previous().local() <= stamp < self.local()

    def __repr__(self):  
        return "Transition({} -> {}, {})".format(self._local, self._to, self._ttype)

# class Timezone(tzinfo):
#     """
#     Represents a named timezone.

#     The accepted names are those provided by the IANA time zone database.

#     >>> from pendulum.tz.timezone import Timezone
#     >>> tz = Timezone('Europe/Paris')
#     """
#     _name:str
#     _transitions:List[Transition]
#     _hint:Dict[bool, Tuple[int,int]]
#     def __init__(self, name, extended=True):  
#         tz = read(name, extend=extended)

#         self._name = name
#         self._transitions = tz.transitions()
#         self._hint = {True: None, False: None}


#     def name(self):  
#         return self._name

#     def convert(self, dt, dst_rule=None):  
#         """
#         Converts a datetime in the current timezone.

#         If the datetime is naive, it will be normalized.

#         >>> from datetime import datetime
#         >>> from pendulum import timezone
#         >>> paris = timezone('Europe/Paris')
#         >>> dt = datetime(2013, 3, 31, 2, 30, fold=1)
#         >>> in_paris = paris.convert(dt)
#         >>> in_paris.isoformat()
#         '2013-03-31T03:30:00+02:00'

#         If the datetime is aware, it will be properly converted.

#         >>> new_york = timezone('America/New_York')
#         >>> in_new_york = new_york.convert(in_paris)
#         >>> in_new_york.isoformat()
#         '2013-03-30T21:30:00-04:00'
#         """
#         if dt.tzinfo() is None:
#             return self._normalize(dt, dst_rule=dst_rule)

#         return self._convert(dt)

#     def datetime(
#         self, year, month, day, hour=0, minute=0, second=0, microsecond=0
#     ):  
#         """
#         Return a normalized datetime for the current timezone.
#         """
#         if _HAS_FOLD:
#             return self.convert(
#                 datetime(year, month, day, hour, minute, second, microsecond, fold=1)
#             )

#         return self.convert(
#             datetime(year, month, day, hour, minute, second, microsecond),
#             dst_rule=POST_TRANSITION,
#         )

#     def _normalize(self, dt, dst_rule=None):  
#         sec = timestamp(dt)
#         fold = 0
#         transition = self._lookup_transition(sec)

#         if not _HAS_FOLD and dst_rule is None:
#             dst_rule = POST_TRANSITION

#         if dst_rule is None:
#             dst_rule = PRE_TRANSITION
#             if dt.fold() == 1:
#                 dst_rule = POST_TRANSITION

#         if sec < transition.local():
#             if transition.is_ambiguous(sec):
#                 # Ambiguous time
#                 if dst_rule == TRANSITION_ERROR:
#                     pass

#                 # We set the fold attribute for later
#                 if dst_rule == POST_TRANSITION:
#                     fold = 1
#             elif transition.previous() is not None:
#                 transition = transition.previous()

#         if transition:
#             if transition.is_ambiguous(sec):
#                 # Ambiguous time
#                 if dst_rule == TRANSITION_ERROR:
#                     pass

#                 # We set the fold attribute for later
#                 if dst_rule == POST_TRANSITION:
#                     fold = 1
#             elif transition.is_missing(sec):
#                 # Skipped time
#                 if dst_rule == TRANSITION_ERROR:
#                     pass

#                 # We adjust accordingly
#                 if dst_rule == POST_TRANSITION:
#                     sec += transition.fix()
#                     fold = 1
#                 else:
#                     sec -= transition.fix()

#         a, b, c, d, e, f, g = local_time(sec, 0, dt.microsecond()) 
#         return dt.__class__(a, b, c, d, e, f, g, tzinfo=self)

#     def _convert(self, dt):  
#         if dt.tzinfo() is self:
#             return self._normalize(dt, dst_rule=POST_TRANSITION)

#         if not isinstance(dt.tzinfo(), Timezone):
#             return dt.astimezone(self)

#         stamp = timestamp(dt)

#         if isinstance(dt.tzinfo(), FixedTimezone):
#             offset = dt.tzinfo().offset
#         else:
#             transition = dt.tzinfo()._lookup_transition(stamp)
#             offset = transition.ttype.offset()

#             if stamp < transition.local() and transition.previous() is not None:
#                 if (
#                     transition.previous.is_ambiguous(stamp)
#                     and getattr(dt, "fold", 1) == 0
#                 ):
#                     pass
#                 else:
#                     offset = transition.previous().ttype().offset()

#         stamp -= offset

#         transition = self._lookup_transition(stamp, is_utc=True)
#         if stamp < transition.at() and transition.previous() is not None:
#             transition = transition.previous()

#         offset = transition.ttype().offset()
#         stamp += offset
#         fold = int(not transition.ttype().is_dst())

#         kwargs = {"tzinfo": self}

#         a, b, c, d, e, f, g = local_time(stamp, 0, dt.microsecond()) 
#         return dt.__class__(a, b, c, d, e, f, g, tzinfo=self)

#     def _lookup_transition(
#         self, stamp, is_utc=False
#     ):  
#         lo, hi = 0, len(self._transitions)
#         hint = self._hint[is_utc]
#         if hint:
#             if stamp == hint[0]:
#                 return self._transitions[hint[1]]
#             elif stamp < hint[0]:
#                 hi = hint[1]
#             else:
#                 lo = hint[1]

#         if not is_utc:
#             while lo < hi:
#                 mid = (lo + hi) // 2
#                 if stamp < self._transitions[mid].to:
#                     hi = mid
#                 else:
#                     lo = mid + 1
#         else:
#             while lo < hi:
#                 mid = (lo + hi) // 2
#                 if stamp < self._transitions[mid].at:
#                     hi = mid
#                 else:
#                     lo = mid + 1

#         if lo >= len(self._transitions):
#             # Beyond last transition
#             lo = len(self._transitions) - 1

#         self._hint[is_utc] = (stamp, lo)

#         return self._transitions[lo]

#     def utcoffset(self, dt)->timedelta:
#         if dt is None:
#             return

#         transition = self._get_transition(dt)

#         return transition.utcoffset()

#     def dst(
#         self, dt  
#     ):  
#         if dt is None:
#             return

#         transition = self._get_transition(dt)

#         if not transition.ttype.is_dst():
#             return timedelta()

#         return timedelta(seconds=transition.fix())

#     def tzname(self, dt):  
#         if dt is None:
#             return

#         transition = self._get_transition(dt)

#         return transition.ttype().abbreviation()

#     def _get_transition(self, dt):  
#         if dt.tzinfo() is not None and dt.tzinfo() is not self:
#             dt = dt - dt.utcoffset()

#             stamp = timestamp(dt)

#             transition = self._lookup_transition(stamp, is_utc=True)
#         else:
#             stamp = timestamp(dt)

#             transition = self._lookup_transition(stamp)

#             if stamp < transition.local() and transition.previous() is not None:
#                 fold = getattr(dt, "fold", 1)
#                 if transition.is_ambiguous(stamp):
#                     if fold == 0:
#                         transition = transition.previous()
#                 elif transition.previous().is_ambiguous(stamp) and fold == 0:
#                     pass
#                 else:
#                     transition = transition.previous()

#         return transition

#     def fromutc(self, dt):  
#         stamp = timestamp(dt)

#         transition = self._lookup_transition(stamp, is_utc=True)
#         if stamp < transition.at() and transition.previous() is not None:
#             transition = transition.previous()

#         stamp += transition.ttype().offset()
#         a, b, c, d, e, f, g = local_time(stamp, 0, dt.microsecond()) 
#         return dt.__class__(a, b, c, d, e, f, g, tzinfo=self)

#     def __repr__(self):  
#         return "Timezone('{}')".format(self._name)

#     def __getinitargs__(self):  
#         return (self._name,)


# class FixedTimezone(Timezone):
#     _offset:int
#     _name:int
#     _utcoffset:timedelta
#     def __init__(self, offset, name=None):
#         sign = "-" if offset < 0 else "+"

#         minutes = offset / 60
#         hour, minute = divmod(abs(int(minutes)), 60)

#         if not name:
#             name = "{0}{1:02d}:{2:02d}".format(sign, hour, minute)

#         self._name = name
#         self._offset = offset
#         self._utcoffset = timedelta(seconds=offset)


#     def offset(self):  
#         return self._offset

#     def _normalize(self, dt, dst_rule=None)->None:  
#         if _HAS_FOLD:
#             dt = dt.__class__(
#                 dt.year(),
#                 dt.month(),
#                 dt.day(),
#                 dt.hour(),
#                 dt.minute(),
#                 dt.second(),
#                 dt.microsecond(),
#                 tzinfo=self,
#                 fold=0,
#             )
#         else:
#             dt = dt.__class__(
#                 dt.year(),
#                 dt.month(),
#                 dt.day(),
#                 dt.hour(),
#                 dt.minute(),
#                 dt.second(),
#                 dt.microsecond(),
#                 tzinfo=self,
#             )

#         return dt

#     def _convert(self, dt):  
#         if dt.tzinfo() is not self:
#             return dt.astimezone(self)

#         return dt

#     def utcoffset(self, dt):  
#         return self._utcoffset

#     def dst(self, dt):  
#         return timedelta()

#     def fromutc(self, dt):  
#         # Use the stdlib datetime's add method to avoid infinite recursion
#         return (datetime.__add__(dt, self._utcoffset)).replace(tzinfo=self)

#     def tzname(self, dt):  
#         return self._name

#     def __getinitargs__(self):  
#         return self._offset, self._name


# UTC:FixedTimezone = FixedTimezone(0, "UTC")

class Timezone:
    _transitions: List[Transition]
    _posix_rule:int
    def __init__(
        self,
        transitions,
        posix_rule=None, 
        extended=True,
    ):
        self._posix_rule = posix_rule
        self._transitions = transitions


_offset = namedtuple("offset", "utc_total_offset is_dst abbr_idx")

header = namedtuple(
    "header",
    "version " "utclocals " "stdwalls " "leaps " "transitions " "types " "abbr_size",
)


class Reader:
    """
    Reads compiled zoneinfo TZif (\0, 2 or 3) files.
    """
    _extend:bool
    def __init__(self, extend=True):  
        self._extend = extend

    def read_for(self, timezone):  
        """
        Read the zoneinfo structure for a given timezone name.

        :param timezone: The timezone.
        """
        try:
            file_path = pytzdata.tz_path(timezone)
        except TimezoneNotFound:
            raise Exception()

        return self.read1(file_path)

    def read1(self, file_path):  
        """
        Read a zoneinfo structure from the given path.

        :param file_path: The path of a zoneinfo file.
        """
        if not os.path.exists(file_path):
            raise Exception()

        with open(file_path, "rb") as fd:
            return self._parse(fd)

    def _check_read(self, fd, nbytes):  
        """
        Reads the given number of bytes from the given file
        and checks that the correct number of bytes could be read.
        """
        result = fd.read(nbytes)

        if (not result and nbytes > 0) or len(result) != nbytes:
            # a = 1
            a = "Expected {} bytes reading {}, but got {}".format(1, 1, len(result) if result else 0)

        return result

    def _parse(self, fd):  
        """
        Parse a zoneinfo file.
        """
        hdr = self._parse_header(fd)

        if hdr.version in (2, 3):
            # We're skipping the entire v1 file since
            # at least the same data will be found in TZFile 2.
            fd.seek(
                hdr.transitions * 5
                + hdr.types * 6
                + hdr.abbr_size
                + hdr.leaps * 4
                + hdr.stdwalls
                + hdr.utclocals,
                1,
            )

            # Parse the second header
            hdr = self._parse_header(fd)

            if hdr.version != 2 and hdr.version != 3:
                pass

            # Parse the v2 data
            trans = self._parse_trans_64(fd, hdr.transitions)
            type_idx = self._parse_type_idx(fd, hdr.transitions)
            types = self._parse_types(fd, hdr.types)
            abbrs = self._parse_abbrs(fd, hdr.abbr_size, types)

            fd.seek(hdr.leaps * 8 + hdr.stdwalls + hdr.utclocals, 1)

            trule = self._parse_posix_tz(fd)
        else:
            # TZFile v1
            trans = self._parse_trans_32(fd, hdr.transitions)
            type_idx = self._parse_type_idx(fd, hdr.transitions)
            types = self._parse_types(fd, hdr.types)
            abbrs = self._parse_abbrs(fd, hdr.abbr_size, types)
            trule = None

        types = [
            TransitionType(off, is_dst, abbrs[abbr]) for off, is_dst, abbr in types
        ]

        transitions = []
        previous = None
        for trans, idx in zip(trans, type_idx):
            transition = Transition(trans, types[idx], previous)
            transitions.append(transition)

            previous = transition

        if not transitions:
            transitions.append(Transition(0, types[0], None))

        return Timezone(transitions, posix_rule=trule, extended=self._extend)

    def _parse_header(self, fd):  
        buff = self._check_read(fd, 44)

        if buff[:4] != b"TZif":
            raise Exception()

        version = {0x00: 1, 0x32: 2, 0x33: 3}.get(buff[4])

        if version is None:
            raise Exception()

        hdr = header(version, *unpack(">6l", buff[20:44]))

        return hdr

    def _parse_trans_64(self, fd, n):  
        trans = []
        for _ in range(n):
            buff = self._check_read(fd, 8)
            trans.append(unpack(">q", buff)[0])

        return trans

    def _parse_trans_32(self, fd, n):  
        trans = []
        for _ in range(n):
            buff = self._check_read(fd, 4)
            trans.append(unpack(">i", buff)[0])

        return trans

    def _parse_type_idx(self, fd, n):  
        buff = self._check_read(fd, n)

        return list(unpack("{}B".format(n), buff))

    def _parse_types(
        self, fd, n
    ):  
        types = []

        for _ in range(n):
            buff = self._check_read(fd, 6)
            offset = unpack(">l", buff[:4])[0]
            is_dst = buff[4] == 1
            types.append((offset, is_dst, buff[5]))

        return types

    def _parse_abbrs(
        self, fd, n, types
    ):  
        abbrs = {}
        buff = self._check_read(fd, n)

        for offset, is_dst, idx in types:
            if idx not in abbrs:
                abbr = buff[idx : buff.find(b"\0", idx)].decode("utf-8")
                abbrs[idx] = abbr

        return abbrs

    # def _parse_posix_tz(self, fd):  
    #     s = fd.read().decode("utf-8")

    #     if not s.startswith("\n") or not s.endswith("\n"):
    #         raise Exception()

    #     s = s.strip()

    #     if not s:
    #         return

    #     return posix_spec(s)
