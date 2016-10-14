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

    class UserProductionTypeEnum(DeltaEnum):
        CONSUMER = DeltaEnumValue(0, "Consumer")
        PRODUCER = DeltaEnumValue(1, "Producer")

    user_id = Unicode("USERID")
    user_full_name = Unicode("USERNAME")
    user_password = Unicode("USERPSWD")
    user_status = Int("USERSTATE")
    user_last_login_date = DateTime("USERLASTLOGIN")
    user_type = Int("USERTYPE")
    user_mobile = Unicode("USERMOBILE")
    user_phone = Unicode("USERPHONE")
    user_email = Unicode("USEREMAIL")
    user_address = Unicode("USERADDRESS")
    user_work_address = Unicode("USERWORKADDRESS")
    user_national_code = Int("USERNATIONALCODE")
    user_production_type = Int('USERPRODUCTIONTYPE')


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
    user_history_date = DateTime("USHISTDATE")
    user_history_client_ip = Unicode("USHISTCLNTIP")
    user_history_status = Int("USHISTSTATUS")
    user_history_message = Unicode("USHISTMSG")

    user = Reference(("UserHistoryEntity.user_id"), ("UserEntity.id"))


class UserActionBaseEntity(Storm):
    """
    This class defines spuseractions table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spuseractions"
    __storm_primary__ = "id"

    id = Unicode("ID")

    def __eq__(self, other):
        if isinstance(other, UserActionBaseEntity):
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


class UserActionEntity(UserActionBaseEntity):
    """
    This class defines spuseractions table.
    *Created automatically by ExtractorEngine*
    """

    class UserActionStatusEnum(DeltaEnum):
        ACTION_CREATED = DeltaEnumValue(0, "Action Created")
        ACTION_EXPIRED = DeltaEnumValue(1, "Action Expired")
        ACTION_FAILED = DeltaEnumValue(2, "Action Failed")
        ACTION_COMPLETED = DeltaEnumValue(3, "Action Completed")

    class UserActionEnum(DeltaEnum):
        ACTIVATE_USER = DeltaEnumValue(0, "Activate User")
        CHANGE_USER_PASSWORD = DeltaEnumValue(1, "Change User Password")

    user_id = Unicode("USERID")
    user_action = Int("USERACTION")
    user_action_date = DateTime("ACTIONDATE")
    user_action_status = Int("ACTIONSTATE")
    user_action_data = Unicode("ACTIONDATA")


class ProductsBaseEntity(Storm):
    """
    This class defines spproducts table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spproducts"
    __storm_primary__ = "product_id"

    product_id = Unicode("PRODUCTID")

    def __eq__(self, other):
        if isinstance(other, ProductsBaseEntity):
            return self.product_id == other.product_id
        return False

    def __hash__(self):
        return hash(self.product_id)

    def __repr__(self):
        return '<%s.%s [ %s ] >' % (self.__module__,
                                    self.__class__.__name__,
                                    str(self.product_id))

    def __str__(self):
        return self.__storm_primary__.__str__()


class ProductsEntity(ProductsBaseEntity):
    """
    This class defines spproducts table.
    *Created automatically by ExtractorEngine*
    """

    class ProductCategoryEnum(DeltaEnum):
        BODY_BUILDING_POWER_LIFTING = DeltaEnumValue(0, 'Body Building & Power Lifting')
        CLOTHING_WEAR = DeltaEnumValue(1, "Clothing & Wear")
        SPORT_CLOTHING_PRINT = DeltaEnumValue(2, "Sport Clothing Print")
        SNEAKERS = DeltaEnumValue(3, "Sneakers")
        MARTIAL_ARTS = DeltaEnumValue(4, "Martial Arts")
        DISTRIBUTION = DeltaEnumValue(5, "Distribution")
        SPORTS_BAG_BACKPACK = DeltaEnumValue(6, "Sports Bag & Backpack")
        ELECTRONICS = DeltaEnumValue(7, "Electronics")
        ARTIFICIAL_GRASS = DeltaEnumValue(8, "Artificial Grass")
        SPORT_FLOOR_COVER = DeltaEnumValue(9, "Sports Floor Cover")
        INSTALLATION_ESTABLISHMENT = DeltaEnumValue(10, "Installation & Establishment")
        SKATE_SKI = DeltaEnumValue(11, "Skate & Ski")
        CLIMBING_BOULDERING = DeltaEnumValue(12, "Mountaineering & Bouldering & Climbing")
        POOL_ROCKET = DeltaEnumValue(13, "Pool & Rocket")
        BALL_NET = DeltaEnumValue(14, "Ball & Net")
        SWIMMING_TOOLS = DeltaEnumValue(15, "Swimming Tools")
        BICYCLING_TOOLS = DeltaEnumValue(16, "Bicycling Tools")
        HUNTING_TOOLS = DeltaEnumValue(17, "Hunting Tools")
        BOW_ARROW = DeltaEnumValue(18, "Bow & Arrow")
        GYMNASTICS_TOOLS = DeltaEnumValue(19, "Gymnastics Tools")

    class ProductStatusEnum(DeltaEnum):
        OUT_OF_STOCK = DeltaEnum(0, "Out of Stock")
        IN_STOCK = DeltaEnum(1, "In Stock")

    product_name = Unicode("PRODUCTNAME")
    product_price = Decimal('PRODUCTPRICE')
    product_category = Int('PRODUCTCATEGORY')
    product_image = RawStr('PRODUCTIMAGE')
    product_status = Int('PRODUCTSTATE')
    product_unique_name = Unicode("PRODUCTUNIQNAME")
    product_producer_user_id = Unicode("PRODUCTPRODUCERID")
    product_creation_date = DateTime("PRODUCTCREATIONDATE")


class ProductsColorsBaseEntity(Storm):
    """
    This class defines spproductcolors table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spproductcolors"
    __storm_primary__ = "product_color_id"

    product_color_id = Unicode("PRDCTCLRID")

    def __eq__(self, other):
        if isinstance(other, ProductsColorsBaseEntity):
            return self.product_color_id == other.product_color_id
        return False

    def __hash__(self):
        return hash(self.product_color_id)

    def __repr__(self):
        return '<%s.%s [ %s ] >' % (self.__module__,
                                    self.__class__.__name__,
                                    str(self.product_color_id))

    def __str__(self):
        return self.__storm_primary__.__str__()


class ProductsColorsEntity(ProductsColorsBaseEntity):
    """
    This class defines spproductcolors table.
    *Created automatically by ExtractorEngine*
    """

    product_id = Unicode('PRDCTCLRPRODUCTID')
    product_color_hex = Unicode('PRDCTCLRHEX')


class InvoiceBaseEntity(Storm):
    """
    This class defines spinvoices table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spinvoices"
    __storm_primary__ = "invoice_id"

    invoice_id = Unicode("INVOICEID")

    def __eq__(self, other):
        if isinstance(other, InvoiceBaseEntity):
            return self.invoice_id == other.invoice_id
        return False

    def __hash__(self):
        return hash(self.invoice_id)

    def __repr__(self):
        return '<%s.%s [ %s ] >' % (self.__module__,
                                    self.__class__.__name__,
                                    str(self.invoice_id))

    def __str__(self):
        return self.__storm_primary__.__str__()


class InvoiceEntity(InvoiceBaseEntity):
    """
    This class defines spinvoices table.
    *Created automatically by ExtractorEngine*
    """

    class InvoiceStatusEnum(DeltaEnum):
        ORDERED = DeltaEnumValue(0, "Ordered")
        CONFIRMED = DeltaEnumValue(1, "Confirmed")
        REJECTED = DeltaEnumValue(2, "Rejected")
        PAYED = DeltaEnumValue(3, "Payed")
        NOT_PAYED = DeltaEnumValue(4, "Not Payed")
        FAILED = DeltaEnumValue(5, "Failed")
        PROCESSED = DeltaEnumValue(6, "Processed")
        SHIPPED = DeltaEnumValue(7, "Shipped")
        DELIVERED = DeltaEnumValue(8, "Delivered")

    invoice_date = DateTime('INVOICEDATE')
    invoice_status = Int('INVOICESTATE')
    invoice_consumer_user_id = Unicode('INVOICECONSUMERID')


class InvoiceItemBaseEntity(Storm):
    """
    This class defines spinvoiceitems table.
    *Created automatically by ExtractorEngine*
    """
    __version__ = 1.0
    __storm_table__ = "spinvoiceitems"
    __storm_primary__ = "item_id"

    item_id = Unicode("INVITMID")

    def __eq__(self, other):
        if isinstance(other, InvoiceItemBaseEntity):
            return self.item_id == other.item_id
        return False

    def __hash__(self):
        return hash(self.item_id)

    def __repr__(self):
        return '<%s.%s [ %s ] >' % (self.__module__,
                                    self.__class__.__name__,
                                    str(self.item_id))

    def __str__(self):
        return self.__storm_primary__.__str__()


class InvoiceItemEntity(InvoiceItemBaseEntity):
    """
    This class defines spinvoiceitems table.
    *Created automatically by ExtractorEngine*
    """

    invoice_id = Unicode('INVITMINVOICEID')
    item_product_id = Unicode('INVITMPRODUCTID')
    item_price = Decimal('INVITMPRICE')
    item_quantity = Int('INVITMQNTY')
    item_color = Unicode('INVITMCOLOR')