# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *

import os.path

CONF_ROOT = os.path.dirname(__file__)

DEBUG = {{ sentry_debug }}
SENTRY_TESTING = {{ sentry_testing }}

CELERYD_CONCURRENCY = {{ sentry_celeryd_concurrency }}

DATABASES = {
    'default': {
        'ENGINE': '{{ sentry_db_engine }}',
        'NAME': '{{ sentry_db_name }}',
        'USER': '{{ sentry_db_user }}',
        'PASSWORD': '{{ sentry_db_password }}',
        'HOST': '{{ sentry_db_host }}',
        'PORT': '{{ sentry_db_port }}',
        {% if sentry_db_engine  == "sentry.db.postgres" %}
        'AUTOCOMMIT': {{ sentry_db_postgre_autocommit }},
        'ATOMIC_REQUESTS': {{ sentry_db_postgre_atomicreq }}
        {% endif %}
    }
}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True
SENTRY_OPTIONS['system.secret-key']= '{{ sentry_secret_key }}'


# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = False

#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

#SENTRY_REDIS_OPTIONS = {
#    'hosts': {
#        0: {
#            'host': '{{ sentry_redis_host }}',
#            'port': {{ sentry_redis_port }},
#        }
#    }
#}

#########
# Cache #
#########

# Sentry currently utilizes two separate mechanisms. While CACHES is not a
# requirement, it will optimize several high throughput patterns.

# If you wish to use memcached, install the dependencies and adjust the config
# as shown:
#
#   pip install python-memcached
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': ['127.0.0.1:11211'],
#     }
# }

# A primary cache is required for things such as processing events
SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

################
# File storage #
################

# Any Django storage backend is compatible with Sentry. For more solutions see
# the django-storages package: https://django-storages.readthedocs.io/en/latest/

SENTRY_OPTIONS['filestore.backend'] = 'django.core.files.storage.FileSystemStorage'
SENTRY_OPTIONS['filestore.options'] = {
          'location': '/tmp/sentry-files',
}
##############
# Web Server #
##############

# If you're using a reverse SSL proxy, you should enable the X-Forwarded-Proto
# header and uncomment the following settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# If you're not hosting at the root of your web server,
# you need to uncomment and set it to the path where Sentry is hosted.
# FORCE_SCRIPT_NAME = '/sentry'

SENTRY_WEB_HOST = '{{ sentry_ip }}'
SENTRY_WEB_PORT = {{ sentry_port }}
SENTRY_WEB_OPTIONS = {
     'workers': 6,  # the number of web workers
    # 'protocol': 'uwsgi',  # Enable uwsgi protocol instead of http
}

#SENTRY_ALLOW_REGISTRATION = False
SENTRY_FEATURES["auth:register"]=False

{% if sentry_ad_auth | bool %}

######################
## django-auth-ldap ##
######################

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTH_LDAP_SERVER_URI = '{{ sentry_auth_ldap_server_uri }}'
AUTH_LDAP_BIND_DN = "{{ sentry_auth_ldap_bind_dn }}"
AUTH_LDAP_BIND_PASSWORD = "{{ sentry_auth_ldap_bind_password }}"


AUTH_LDAP_USER_SEARCH = LDAPSearch(
'{{ sentry_auth_ldap_user_search }}',
ldap.SCOPE_SUBTREE,
'(name=%(user)s)',
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
'{{ sentry_auth_ldap_group_search }}',
ldap.SCOPE_SUBTREE,
'(objectClass=group)'
)

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')
AUTH_LDAP_REQUIRE_GROUP = '{{ sentry_auth_ldap_group_search }}'
AUTH_LDAP_USER_ATTR_MAP = {
'name': 'displayName',
'email': 'mail'
}

AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_DEFAULT_SENTRY_ORGANIZATION = u'{{ sentry_auth_ldap_default_sentry_org }}'
AUTH_LDAP_SENTRY_ORGANIZATION_ROLE_TYPE = 'member'
AUTH_LDAP_SENTRY_ORGANIZATION_GLOBAL_ACCESS = True
AUTH_LDAP_SENTRY_SUBSCRIBE_BY_DEFAULT = True

#First backend is the ldap backendl, second one is a "local" backend based on
#data gathered in the database
AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
  'sentry_ldap_auth.backend.SentryLdapBackend',
  'django.contrib.auth.backends.ModelBackend',
)
#Require domain cert
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
{% endif %}
