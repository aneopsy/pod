CAS_SERVER_URL = 'https://cas.upf.pf/'
CAS_VERSION = '3'

# LDAP
AUTH_LDAP_SERVER_URI = 'ldap://ldap.upf.pf'
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_SCOPE = 'ONELEVEL'
# ('ldap', 'parameters')
AUTH_LDAP_USER_SEARCH = ('ou=people,dc=upf,dc=pf', "(uid=%(uid)s)")
AUTH_LDAP_UID_TEST = ""

AUTH_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mailLocalAddress',
    'affiliation': 'eduPersonPrimaryAffiliation'
}
AFFILIATION_STAFF = ('employee', 'faculty')
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'core.populatedCASbackend.PopulatedCASBackend'
)
