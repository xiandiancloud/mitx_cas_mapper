"""Django CAS 1.0/2.0 authentication backend"""

from django.conf import settings

__all__ = []

_DEFAULTS = {
    'CAS_ADMIN_PREFIX': None,
    'CAS_EXTRA_LOGIN_PARAMS': None,
    'CAS_IGNORE_REFERER': False,
    'CAS_LOGOUT_COMPLETELY': True,
    'CAS_REDIRECT_URL': '/',
    'CAS_RETRY_LOGIN': False,
    'CAS_PROXY_CALLBACK': None,
    'CAS_SERVER_URL': None,
    'CAS_VERSION': '2',
}
CAS_URI = 'http://192.168.2.103:8081/cas'
NSMAP = {'cas': CAS_URI}
CAS = '{%s}' % CAS_URI

for key,value in _DEFAULTS.iteritems():
    try:
        getattr(settings,key)
    except AttributeError:
        setattr(settings,key,value)
    except ImportError:
        pass

def populate_user(user, authentication_response):
    if authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP) is not None:
        attr = authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP)

        if attr.find(CAS + 'is_staff', NSMAP) is not None:
            user.is_staff = attr.find(CAS + 'is_staff', NSMAP).text.upper() == 'TRUE'

        if attr.find(CAS + 'is_superuser', NSMAP) is not None:
            user.is_superuser = attr.find(CAS + 'is_superuser', NSMAP).text.upper() == 'TRUE'

        if attr.find(CAS + 'givenName', NSMAP) is not None:
            user.first_name = attr.find(CAS + 'givenName', NSMAP).text

        if attr.find(CAS + 'sn', NSMAP) is not None:
            user.last_name = attr.find(CAS + 'sn', NSMAP).text

        if attr.find(CAS + 'email', NSMAP) is not None:
            user.email = attr.find(CAS + 'email', NSMAP).text
    pass

