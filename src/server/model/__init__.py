"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from storm.locals import *


class UserBaseEntity(Storm):
    """
    This class defines spusers table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spusers"
    __storm_primary__ = "id"

    id = Unicode("ID")

    def __eq__(self, other):
        if isinstance(other, UserBaseEntity):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '<%s.%s [ %s ] >' % (self.__module__,
                                    self.__class__.__name__,
                                    str(self.id))

    def __str__(self):
        return self.__storm_primary__.__str__()


class UserEntity (UserBaseEntity):
    """
    This class defines dcusers table.
    *Created automatically by ExtractorEngine*
    """

    user_id = Unicode("USERID")
    user_name = Unicode("USERNAME")
    user_password = Unicode("USERPSWD")