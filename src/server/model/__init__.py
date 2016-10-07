"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.core import DeltaEnum, DeltaEnumValue
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


class UserEntity(UserBaseEntity):
    """
    This class defines spusers table.
    *Created automatically by ExtractorEngine*
    """

    class UserStatusEnum(DeltaEnum):
        USER_REGISTERED = DeltaEnumValue(0, "User Registered")
        USER_ACTIVATED = DeltaEnumValue(1, "User Activated")
        LOGIN_SUCCESSFUL = DeltaEnumValue(2, "Login Successful")
        LOGIN_FAILED = DeltaEnumValue(3, "Login Failed")
        LOGOUT = DeltaEnumValue(4, "Logout")
        USER_DEACTIVATED = DeltaEnumValue(5, "User Deactivated")
        FORGOTTEN_PASSWORD = DeltaEnumValue(6, "Forgotten Password")
        USER_BLOCKED = DeltaEnumValue(7, "Blocked User")

    class UserTypeEnum(DeltaEnum):
        NORMAL_USER = DeltaEnumValue(0, "Normal User")
        SUPPORT_USER = DeltaEnumValue(1, "Support User")
        ADMIN_USER = DeltaEnumValue(2, "Admin User")

    user_id = Unicode("USERID")
    user_name = Unicode("USERNAME")
    user_password = Unicode("USERPSWD")
    user_status = Int("USERSTATE")
    user_last_login_date = Date("USERLASTLOGIN")
    user_type = Int("USERTYPE")

class UserHistoryBaseEntity(Storm):
    """
    This class defines spuserhist table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spuserhist"
    __storm_primary__ = "id"

    id = Unicode("ID")

    def __eq__(self, other):
        if isinstance(other, UserHistoryBaseEntity):
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


class UserHistoryEntity(UserHistoryBaseEntity):
    """
    This class defines spuserhist table.
    *Created automatically by ExtractorEngine*
    """

    class UserHistoryStatusEnum(DeltaEnum):
        USER_REGISTERED = DeltaEnumValue(0, "User Registered")
        USER_ACTIVATED = DeltaEnumValue(1, "User Activated")
        LOGIN_SUCCESSFUL = DeltaEnumValue(2, "Login Successful")
        LOGIN_FAILED = DeltaEnumValue(3, "Login Failed")
        LOGOUT = DeltaEnumValue(4, "Logout")
        USER_DEACTIVATED = DeltaEnumValue(5, "User Deactivated")
        FORGOTTEN_PASSWORD = DeltaEnumValue(6, "Forgotten Password")

    user_id = Unicode("USERID")
    user_history_date = Date("USHISTDATE")
    user_history_client_ip = Unicode("USHISTCLNTIP")
    user_history_status = Int("USHISTSTATUS")
    user_history_message = Unicode("USHISTMSG")

    user = Reference(("UserHistoryEntity.user_id"), ("UserEntity.id"))