"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import uuid
import datetime

from storm.expr import Select, And, In

from deltapy.core import DynamicObject, DeltaException
from deltapy.utils.storm_aux import entity_to_dic
from deltapy.transaction.decorators import transactional
from deltapy.security.manager import BaseSecurityManager
from deltapy.transaction.services import get_current_transaction_store

import deltapy.unique_id.services as unique_id_services

from server.model import UserEntity, UserActionEntity
from server.utils.encryption import encrypt_sha512, verify_sha512, encrypt_aes, decrypt_aes

import server.utils.email.services as email_services


class UserSecurityException(DeltaException):
    '''
    Is raised when user manipulation encounters an error.
    '''


class UserNotFoundException(UserSecurityException):
    '''
    Is raised when user not found.
    '''

    def __init__(self, user_id):
        super(UserNotFoundException, self).__init__("User [{0}] not found.".format(user_id))


class SecurityManager(BaseSecurityManager):
    """
    Security Manager
    """

    def _check_invalid_user_names(self, user_id):
        '''
        Checks invalid user names.
        '''

        if user_id in ('admin', 'root', 'support'):
            raise UserSecurityException("User name is not valid.")

    def _get(self, id):
        '''
        Returns user entity:
        '''

        store = get_current_transaction_store()
        return store.get(UserEntity, id)

    def create_user(self, id, password, fullname, **options):
        """
        Creates a new user.

        @param id: user ID
        @param password: password
        @param fullname: full name
        """

        if id is None or id.strip() == "":
            raise UserSecurityException("Use id can not be nothing.")

        if password is None or password.strip() == "":
            raise UserSecurityException("Use password can not be nothing.")

        if fullname is None or fullname.strip() == "":
            raise UserSecurityException("Use name can not be nothing.")

        self._check_invalid_user_names(id)

        user = UserEntity()
        user.id = unicode(unique_id_services.get_id('uuid'))
        user.user_id = id
        user.user_full_name = fullname
        user.user_password = unicode(encrypt_sha512(password))

        status = options.get('status')
        if status is None:
            status = UserEntity.UserStatusEnum.USER_REGISTERED
        user.user_status = status

        type = options.get('type')
        if type is None:
            type = UserEntity.UserTypeEnum.NORMAL_USER
        user.user_type = type

        mobile = options.get('mobile')
        if mobile is None:
            mobile = ""
        user.user_mobile = unicode(mobile)

        phone = options.get('phone')
        if phone is None:
            phone = ""
        user.user_phone = unicode(phone)

        email = options.get('email')
        if email is None:
            raise UserSecurityException("User email can not be nothing.")
        user.user_email = unicode(email)

        address = options.get('address')
        if address is None:
            address = ""
        user.user_address = unicode(address)

        work_address = options.get('work_address')
        if work_address is None:
            work_address = ""
        user.user_work_address = unicode(work_address)

        national_code = options.get('national_code')
        if national_code is None:
            national_code = "0"
        user.user_national_code = unicode(national_code)

        production_type = options.get('production_type')
        if production_type is None:
            production_type = UserEntity.UserProductionTypeEnum.CONSUMER
        user.user_production_type = production_type

        production_package = options.get('production_package')
        if production_package is None:
            production_type = UserEntity.UserProductionPackageEnum.FREE
        if production_type == UserEntity.UserProductionTypeEnum.PRODUCER:
            user.user_production_package = production_package

        user.user_last_login_date = datetime.datetime(datetime.MINYEAR, 1, 1, 0, 0, 0, 0)

        store = get_current_transaction_store()
        store.add(user)

        self.activate_user(user.user_id, True)

        return DynamicObject(entity_to_dic(user))

    def remove_user(self, id):
        """
        Removes the given user.

        @param id: user name
        """

        user = self.get_user_by_id(id)
        if user.user_status != UserEntity.UserStatusEnum.USER_REGISTERED:
            raise UserSecurityException("Only registered user can be removed.")

        store = get_current_transaction_store()
        user_entity = self._get(user.id)
        store.remove(user_entity)

    def update_user(self, id, **params):
        """
        Updates specified user with given parameters.

        @param id: user name
        @param **options:
        """

        user = self.get_user_by_id(id)
        if user is None:
            raise UserNotFoundException(id)

        user_entity = self._get(user.id)

        full_name = params.get('full_name')
        if full_name is not None and full_name.strip() != "":
            user_entity.user_full_name = unicode(full_name)

        password = params.get('password')
        if password is not None and password.strip() != "":
            user_entity.user_password = unicode(encrypt_sha512(password))

        address = params.get('address')
        if address is not None and address.strip() != "":
            user_entity.user_address = unicode(address)

        mobile = params.get('mobile')
        if mobile is not None and mobile.strip() != "":
            user_entity.user_mobile = unicode(mobile)

    def activate_user(self, id, flag, **options):
        """
        Active or inactive specified user.

        @param id: user ID
        @param flag: activation flag(True or False)
        """

        user = self.get_user_by_id(id)
        if user is None:
            raise UserNotFoundException(id)

        self._check_invalid_user_names(id)

        store = get_current_transaction_store()
        activation_data = options.get('activation_data')

        statement = \
            Select(columns=[UserActionEntity.id,
                            UserActionEntity.user_action_data,
                            UserActionEntity.user_action_date],
                   where=And(UserActionEntity.user_id == user.id,
                             UserActionEntity.user_action == UserActionEntity.UserActionEnum.ACTIVATE_USER,
                             UserActionEntity.user_action_status == UserActionEntity.UserActionStatusEnum.ACTION_CREATED),
                   tables=[UserActionEntity])
        result = store.execute(statement).get_one()

        if self.is_active(user.id):
            raise UserSecurityException("User is already activated.")
        else:
            if activation_data is None or activation_data.strip() == "":
                if result is None:
                    now_date = datetime.datetime.now()
                    activation_date = datetime.datetime(now_date.year, now_date.month, now_date.day,
                                                        now_date.hour, now_date.minute, now_date.second)
                    activation_data = self._generate_activation_data(user, activation_date)
                    activation_data = encrypt_aes("{0}${1}".format(user.user_id, activation_data))

                    action_entity = UserActionEntity()
                    action_entity.id = unicode(unique_id_services.get_id('uuid'))
                    action_entity.user_action = UserActionEntity.UserActionEnum.ACTIVATE_USER
                    action_entity.user_action_data = unicode(activation_data)
                    action_entity.user_action_date = activation_date
                    action_entity.user_id = user.id
                    action_entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_CREATED
                    store.add(action_entity)

                    email_services.send_activation_email(user.user_full_name, user.user_email,
                                                         "http://{0}:{1}/activate/{2}".format("185.94.99.134",
                                                                                              "5001",
                                                                                              activation_data))

                    return activation_data
                else:
                    actions_id, user_action_data, user_action_date = result
                    email_services.send_activation_email(user.user_full_name, user.user_email,
                                                         "http://{0}:{1}/activate/{2}".format("185.94.99.134",
                                                                                              "5001",
                                                                                              user_action_data))
                    return user_action_data

        if result is None:
            raise UserSecurityException("User Activation Error")

        actions_id, user_action_data, user_action_date = result
        if (user_action_data != activation_data or
            not self._verify_activation_data(user, user_action_date, activation_data)):
            action_entity = store.get(UserActionEntity, actions_id)
            action_entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_FAILED
            raise UserSecurityException("User Activation Error")

        if (datetime.datetime.now() - user_action_date).total_seconds() > 24*3600:
            action_entity = store.get(UserActionEntity, actions_id)
            action_entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_EXPIRED
            raise UserSecurityException("User Activation Expired")

        user_entity = self._get(user.id)
        user_entity.user_status = UserEntity.UserStatusEnum.USER_ACTIVATED

        action_entity = store.get(UserActionEntity, actions_id)
        action_entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_COMPLETED

    def _generate_activation_data(self, user, activation_date):
        '''
        Generates activation/change password data.
        '''

        to_be_encrypted = \
            "{0}]*[{1}]*[{2}".format(user.user_id, activation_date, user.user_password)

        return encrypt_sha512(to_be_encrypted)

    def _verify_activation_data(self, user, activation_date, activation_data):
        '''
        Generates activation/change password data.
        '''

        decrypted = decrypt_aes(activation_data)
        user_id, data = decrypted.split('$')

        new_data = \
            "{0}]*[{1}]*[{2}".format(user.user_id, activation_date, user.user_password)

        return verify_sha512(new_data, data)

    def is_active(self, user_id):
        """
        Returns True if user is active.

        @param user_id: user ID

        @return: bool
        """

        user = self.get_user(user_id)
        if user is None:
            raise UserNotFoundException(user_id)

        return user.user_status not in (UserEntity.UserStatusEnum.USER_REGISTERED,
                                        UserEntity.UserStatusEnum.USER_DEACTIVATED)

    def is_expired(self, user_id):
        """
        Returns True if user is expired.

        @param user_id: user ID

        @return: bool
        """

        return False

    @transactional
    def get_user(self, id, **options):
        """
        Returns user information by specified name

        @param id: user name

        @return: user data as DynamicObject
        """

        store = get_current_transaction_store()
        user = store.find(UserEntity, And(UserEntity.id == id)).one()

        if user is None:
            return None

        return DynamicObject(entity_to_dic(user))

    @transactional
    def get_user_by_id(self, user_id, **options):
        """
        Returns user information by specified name

        @param user_id: user ID

        @return: user data as DynamicObject
        """

        store = get_current_transaction_store()
        user = store.find(UserEntity, And(UserEntity.user_id == unicode(user_id))).one()

        if user is None:
            return None

        return DynamicObject(entity_to_dic(user))

    def is_superuser(self, id):
        """
        Returns True if specified user is supper user else returns False

        @param id: user name

        @return: bool
        """

        user = self.get_user_by_id(id)
        if user is None:
            raise UserNotFoundException(id)

        return user.user_type in (UserEntity.UserTypeEnum.ADMIN_USER, UserEntity.UserTypeEnum.SUPPORT_USER)

    def get_users(self, **options):
        """
        Returns users using given options.

        @return: [DynamicObject<user info...>]
        """

        expressions = []

        statuses = options.get('statuses')
        if statuses is not None and len(statuses) > 0:
            expressions.append(In(UserEntity.user_status, statuses))

        types = options.get('types')
        if types is not None and len(types) > 0:
            expressions.append(In(UserEntity.user_type, types))

        store = get_current_transaction_store()
        entities = store.find(UserEntity,
                              And(*expressions))

        results = []
        for user in entities:
            if user.user_id not in ('admin', 'root', 'support'):
                results.append(DynamicObject(entity_to_dic(user)))

        return results

    def reset_password(self, user_id, new_password):
        """
        Resets password of the given user to new password.

        @param user_id: user ID
        @param new_password: user new password
        """

        self._check_invalid_user_names(user_id)
        self.update_user(user_id, password=new_password)

    def change_password(self, user_id, current_password, new_password, **options):
        """
        Changes password of current user.

        @param current_password: user current password
        @param new_password: user new password
        """

        self._check_invalid_user_names(user_id)

        user = self.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)

        if not self.is_active(user.id):
            raise UserSecurityException("User is not activated.")

        store = get_current_transaction_store()
        activation_data = options.get('activation_data')

        statement = \
            Select(columns=[UserActionEntity.id,
                            UserActionEntity.user_action_data,
                            UserActionEntity.user_action_date],
                   where=And(UserActionEntity.user_id == user.id,
                             UserActionEntity.user_action == UserActionEntity.UserActionEnum.CHANGE_USER_PASSWORD,
                             UserActionEntity.user_action_status == UserActionEntity.UserActionStatusEnum.ACTION_CREATED),
                   tables=[UserActionEntity])
        result = store.execute(statement).get_one()

        if result is None:
            if activation_data not in (None, ""):
                return

            newly_generated_data = str(uuid.uuid4())[:8]
            entity = UserActionEntity()
            entity.id = unicode(unique_id_services.get_id('uuid'))
            entity.user_action = UserActionEntity.UserActionEnum.CHANGE_USER_PASSWORD
            entity.user_action_data = unicode(newly_generated_data)
            entity.user_action_date = datetime.datetime.now()
            entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_CREATED
            entity.user_id = user.id

            store.add(entity)

            email_services.send_change_password_email(user.user_full_name, user.user_email, newly_generated_data)
            return newly_generated_data
        else:
            entity_id, user_action_data, user_action_date = result
            if user_action_date < datetime.datetime.now() - datetime.timedelta(days=1):
                entity = store.get(UserActionEntity, entity_id)
                entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_EXPIRED
                return

            if unicode(user_action_data) != unicode(activation_data):
                raise UserSecurityException("Security change code is wrong.")

            if new_password in (None, "") or new_password.strip() == "":
                raise UserSecurityException("Password is not valid.")

            self.update_user(user_id, password=new_password)
            entity = store.get(UserActionEntity, entity_id)
            entity.user_action_status = UserActionEntity.UserActionStatusEnum.ACTION_COMPLETED

    def create_role(self, name, **options):
        """
        Creates a new role.

        @param id: role ID
        @param name: role name
        @param **options: Other options.
        """

        raise NotImplementedError()

    def find_role(self, **options):
        """
        Finds role according to given options.

        @param **options: Filters of find.

        @return: List of DynamicObject
        """

        raise NotImplementedError()

    def add_or_update_role(self, id, **options):
        """
        Adds or updates role.

        @param id: role ID
        @param **options:
        """

        raise NotImplementedError()

    def remove_role(self, id):
        """
        Removes specified role.

        @param id: role ID
        """

        raise NotImplementedError()

    def update_role(self, id, **params):
        """
        Removes specified role.

        @param id: role ID
        @param **params:
        """

        raise NotImplementedError()

    def get_role(self, id, **options):
        """
        Returns role information by given role ID.

        @param role_id: role ID
        @param **options: Other options.
        """

        raise NotImplementedError()

    def get_roles(self, **options):
        """
        Returns roles considering given options.

        @return: [DynamicObject<...>]
        """

        raise NotImplementedError()

    def assign_role(self, user_id, role_ids):
        """
        Assigns given roles to specified user.

        @param user_id: user ID
        @param role_ids: list role ID
        """

        raise NotImplementedError()

    def unassign_role(self, user_id, role_ids):
        """
        Unassigns given roles from specified user.

        @param user_id: user ID
        @param role_ids: list role ID
        """

        raise NotImplementedError()

    def create_permission(self, id, name, **options):
        """
        Creates a new permission.
        @param id: permission ID
        @param name: permission name
        @param **options:
        """

        raise NotImplementedError()

    def add_or_update_permission(self, id, **options):
        """
        Adds new permission or updates existed permission.
        @param id: permission ID
        """

        raise NotImplementedError()

    def remove_permission(self, id):
        """
        Removes specified permission.

        @param id: permission ID
        """

        raise NotImplementedError()

    def update_permission(self, id, **params):
        """
        Updates specified permission using given parameters.
        @param id: permission ID
        @param **params:
        """

        raise NotImplementedError()

    def get_permission(self, id):
        """
        Returns specified permission information.
        @param id:
        """

        raise NotImplementedError()

    def get_permissions(self, **options):
        """
        Returns a list of permission considering given options.
        """

        raise NotImplementedError()

    def grant_permission(self, role_id, permission_ids):
        """
        Grants given permissions.

        @param role_id: role ID
        @param permission_ids: list of permission ID
        """

        raise NotImplementedError()

    def deny_permission(self, role_id, permission_ids):
        """
        Denies given permissions.

        @param role_id: role ID
        @param permission_ids: list of permission ID
        """

        raise NotImplementedError()

    def get_user_roles(self, user_id, **options):
        """
        Returns all roles which are assigned to specified user.

        @param user_id: user ID
        @param **options:

        @return: [role as DynamicObject]
        """

        return []

    def get_role_permissions(self, role_id, **options):
        """
        Returns all permissions which are granted to specified role.

        @param role_id: role ID

        @return: [permission as DynamciObject]
        """

        return []

    def get_user_permissions(self, id):
        """
        Returns all permissions of specified user.

        @param id: user ID

        @return: [permission info as DynamicObject]
        """

        permissions = []
        for r in self.get_roles(user_id = id):
            permissions += self.get_permissions(role_id=r.id)
        return permissions

    def get_role_users(self, role_id, **options):
        """
        Returns all user which is assigned to specified role.

        @param role_id: role ID

        @return: [user as DynamicObject]
        """

        return []

    def get_permission_roles(self, permission_id, **options):
        """
        Returns all roles which are including specified permission.

        @param permission_id: permission ID

        @return: [role as DynamicObject]
        """

        return []
