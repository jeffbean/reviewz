from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
import ldap
from reviewproject import settings


class ActiveDirectoryGroupMembershipSSLBackend(object):
    def __init__(self):
        self.debug = settings.DEBUG

    def authenticate(self, username=None, password=None, **kwargs):
        """
            - This authenticate is a JBean special. This first trys to login to the local instance
            and then trys to authenticate with your Configured LDAP server.

        :param username: default username field
        :param password: password field from login
        :param kwargs:
        :return: user object that authenticates
        """
        try:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.CERT_FILE)
            l = ldap.initialize(settings.AD_LDAP_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            binddn = "%s@%s" % (username, settings.AD_NT4_DOMAIN)
            l.simple_bind_s(binddn, password)
            l.unbind_s()
            return self.get_or_create_user(username, password, **kwargs)
        except ldap.INVALID_CREDENTIALS:
            pass


    @staticmethod
    def __create_user(username, password):
        """

        :param username: username that is in AD that does not exist in the local DB
        :param password: password from AD that will be pu in the Local Auth DB
        :return: The newly created user object
        """
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.AD_CERT_FILE)
        ldap.set_option(ldap.OPT_REFERRALS, 0) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!

        # initialize
        ldap_connection = ldap.initialize(settings.AD_LDAP_URL)
        ldap_connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)

        # bind
        bind_domain_name = "%s@%s" % (username, settings.AD_NT4_DOMAIN)
        ldap_connection.bind_s(bind_domain_name, password)

        # search for the user on LDAP server
        result = ldap_connection.search_ext_s(settings.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, "sAMAccountName=%s" % username, settings.AD_SEARCH_FIELDS)[0][1]

        # Validate that they are a member of review board group
        if 'memberOf' in result:
            membership = result['memberOf']
        else:
            membership = None

        # Make sure user is part of one of the required AD groups

        user_valid = False
        for req_group in settings.AD_MEMBERSHIP_REQ:
            for group in membership:
                group_str = "CN=%s," % req_group
                if group.find(group_str) >= 0:
                    user_valid = True
                    break

        if not user_valid:

            return None

        # get email
        if 'mail' in result:
            mail = result['mail'][0]
        else:
            mail = None

        # get surname
        if 'sn' in result:
            last_name = result['sn'][0]
        else:
            last_name = None

        # get display name
        if 'givenName' in result:
            first_name = result['givenName'][0]
        else:
            first_name = None

        ldap_connection.unbind_s()

        return User(username=username, first_name=first_name, last_name=last_name, email=mail)

    def get_or_create_user(self, username, password, **kwargs):
        """
        - This method will return either the user found in the Sites Django DB
            or create a new User in the Database based on the information in Active Directory

        :param username: username passed into login form
        :param password: password passed into login form
        """
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            try:
                return UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass

        try:
            new_user = ActiveDirectoryGroupMembershipSSLBackend.__create_user(username, password)
        except Exception, e:
            messages.error('Server Error: {0}'.format(e))
            return None

        new_user.is_staff = True
        new_user.is_superuser = False
        new_user.set_password('ldap authenticated')
        new_user.save()

        # add user to default group
        group = Group.objects.get(pk=15)
        new_user.groups.add(group)
        new_user.save()
        messages.success(request=1, message='Created new User from LDAP: {0}'.format(new_user))
        return new_user

    def get_user(self, user_id):
        try:
            user_model = get_user_model()
            return user_model._default_manager.get(pk=user_id)
        except user_model.DoesNotExist:
            return None