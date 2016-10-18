'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
import time
from deltapy.core import DeltaObject, DeltaException
import deltapy.logging.services as logging
import deltapy.security.session.services as session_services
import deltapy.security.services as security_services  
from deltapy.security.manager import UserNotFoundException
import deltapy.config.services as config_services
from deltapy.caching.decorators import cache

#Constants
IP_ADDRESS_OPTION_KEY = '__IP_ADDRESS__'

class AuthenticationException(DeltaException):
    '''
    '''

class UserIsInactiveException(AuthenticationException):
    '''
    '''
    
class UserIsExpiredException(AuthenticationException):
    '''
    '''

class BaseAuthenticator(DeltaObject):
    '''
    '''
    INCORRECT_PASSWORD_DELAY = 2
    logger = logging.get_logger(name = "authentication")
    
    def _check_password_(self, password, user, **options):
        '''
        Checks user password and return True if password is correct.
         
        @param password: given password
        @param user: user information
        @param **options: 
        
        @return: bool
        '''
        raise NotImplementedError()
    
    def _validate_user_(self, user_name, user, **options):
        '''
        Validates the user.
        
        @param user: user
        '''

        if not security_services.is_active(user.id):
            BaseAuthenticator.logger.error('User [{user_name}] is inactive.'.format(user_name = user_name))
            raise UserIsInactiveException(_('User [{user_name}] is inactive.').format(user_name = user_name))
            
        if security_services.is_expired(user.id):
            BaseAuthenticator.logger.error('User [{user_name}] is expired.'.format(user_name = user_name))
            raise UserIsExpiredException(_('User [{user_name}] is expired.').format(user_name = user_name))

    def internal_login(self, user_name, **options):
        '''
        Logins internally and returns security ticket
        
        @param user_name: user name
        @param **options:  
        
        @return: object
        '''

        user = None
        try:
            user = security_services.get_user(user_name)
        except:
            force = options.get('force', False)
            if force:
                user = security_services.create_internal_user(user_name)
            else:
                BaseAuthenticator.logger.error('User[%s] not found.' % user_name)
                message = 'User[{user_name}] not found.'
                raise AuthenticationException(message.format(user_name = user_name))
        
        session = session_services.create_internal_session(user)
        return session.get_ticket()

    def login(self, user_name, password, **options):
        '''
        Logins and returns security ticket
        
        @param user_name: user name
        @param password: user password
        @param **options:  
        
        @return: object
        '''

        try:
            user = security_services.get_user(user_name)

            if user is None:
                BaseAuthenticator.logger.error('User[{user_name}] not found.'.format(user_name = user_name))
                raise AuthenticationException(_('User or password is invalid.'))

            if not self._check_password_(password, user, **options):
                message = 'User[{user_name}] entered invalid password[{password}].'
                BaseAuthenticator.logger.error(message.format(user_name=user_name,
                                                              password=password))
                #Delay to prevent brute force.
                time.sleep(BaseAuthenticator.INCORRECT_PASSWORD_DELAY)
                raise AuthenticationException(_('User or password is invalid.'))

            #Checking the ip address received in options.
            self._check_recievied_ip_address(user_name, options)

            self._validate_user_(user_name, user, **options)

            session = \
                session_services.create_session(user,
                                                options.get('client_ip'),
                                                lifetime=options.get('lifetime'))

            message = '[{user_name}@{client_ip}] logged in.'
            BaseAuthenticator.logger.info(message.format(user_name = user_name, 
                                                         client_ip = options.get('client_ip')))
            return session.get_ticket()
        except UserNotFoundException:
            BaseAuthenticator.logger.error('User[{user_name}] not found.'.format(user_name = user_name))
            time.sleep(BaseAuthenticator.INCORRECT_PASSWORD_DELAY)
            raise AuthenticationException(_('User or password is invalid.'))
        except Exception, error:
            BaseAuthenticator.logger.exception('Exception : {error}'.format(error = error))
            raise AuthenticationException(str(error))
            

    def authenticate(self, ticket, user_name, **options):
        '''
        Authenticates user and ticket.
        
        @param ticket: security ticket
        @param user_name: user name
        @param **options:  
        
        @return: Session
        '''

        try:        
            session = session_services.get_session(ticket)

            # Checking session expiration
            session_services.check_expiration(session)

            user = session.get_user()
            client_ip = options.get('client_ip')

            if user.id != user_name:
                message = '[{user_name}], [{ip}] sent invalid ticket[{ticket}]'
                BaseAuthenticator.logger.error(message.format(user_name=user_name,
                                                              ip=client_ip,
                                                              ticket=ticket))
                raise AuthenticationException(_('The user or ticket is invalid'))

            # Checking the ip address received in options.
            self._check_recievied_ip_address(user_name, options)

            # Checking if ip of session is equal to ip of client.
            ip_in_session = session.get_client_ip()
            if client_ip != ip_in_session:
                if client_ip not in self.get_trusted_ips():
                    message = '[{user_name}], ticket [{ticket}], came from wrong ip. Session ip [{session_ip}], received ip [{received_ip}].'
                    BaseAuthenticator.logger.error(message.format(user_name=user_name,
                                                                  ticket=ticket,
                                                                  session_ip=ip_in_session,
                                                                  received_ip=client_ip))
                    raise AuthenticationException(_('The user or ticket is invalid'))
                else:
                    message = ('User [{user}] Ticket [{ticket}]'
                               ' Received IP [{trusted_ip}] Session IP [{session_ip}],'
                               ' trusted.')
                    BaseAuthenticator.logger.info(message.format(trusted_ip=client_ip,
                                                                 user=user_name,
                                                                 ticket=ticket,
                                                                 session_ip=ip_in_session))

            return session
        except Exception:
            # Delay to prevent brute force.
            time.sleep(BaseAuthenticator.INCORRECT_PASSWORD_DELAY)
            raise

    def logout(self, ticket, user_name, **options):
        '''
        Logs off given user.
        
        @param ticket: ticket
        @param user_name: user name
        @param **options:  

        '''
        
        try:
            message = 'User [{user_name}@{client_ip}] logged off.'
            BaseAuthenticator.logger.info(message.format(user_name = user_name, 
                                                         client_ip = options.get('client_ip')))
            session = self.authenticate(ticket, user_name, **options)
            session.close()
        except:
            import traceback
            BaseAuthenticator.logger.error(traceback.format_exc())
            raise

    @cache
    def get_trusted_ips(self):
        '''
        Returns a list of IPs that can be trusted.
        
        @return: List of trusted IPs.
        @rtype: list(str)
        '''
        result = set()
        configs = config_services.get_app_config_store()
        if configs.has_key('security', 'trusted_ips'):
            option_str = configs.get('security', 'trusted_ips')
            for trusted_ip in option_str.split(','):
                result.add(trusted_ip.strip())

        return result

    def _check_recievied_ip_address(self, user_name, options):
        '''
        Checks if the ip_address option passed from client is valid.
        If so, replaces the original ip with the received one in the options.
        '''
        client_ip = options.get('client_ip')
        if IP_ADDRESS_OPTION_KEY in options:
            if client_ip not in self.get_trusted_ips():
                message = 'User [{user_name}] with ip [{client_ip}], sends another ip [{ip_address}], but was not trusted.'
                BaseAuthenticator.logger.error(message.format(user_name=user_name,
                                                              client_ip=client_ip,
                                                              ip_address=options.get(IP_ADDRESS_OPTION_KEY)))
                raise AuthenticationException(_("User IP address is invalied."))

            message = 'User [{user}] came from trusted ip [{trusted_ip}]. True IP: [{true_ip}].'
            BaseAuthenticator.logger.info(message.format(user=user_name,
                                                         trusted_ip=client_ip,
                                                         true_ip=options.get(IP_ADDRESS_OPTION_KEY)))
            options.update(client_ip=options.pop(IP_ADDRESS_OPTION_KEY))
