import os

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = '^yn#++yf-nfzt$qthmxti6l+cdh_v#@z4nw^a0sj+_71=h$p=p'

INTERNAL_IPS = (
    '::1',
    '127.0.0.1',
    '94.142.140.20',
)

ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'dev.gkcck.ru',
    'uor.gkcck.ru',
)

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',

    # 'filebrowser',
    'grappelli',
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    'compressor',
    'sorl.thumbnail',
    # 'mptt',
    'debug_toolbar',

    'captcha',

    'proj',
    'proj.utils',
    'proj.gallery',
    # 'proj.content',
    'proj.postbox',
    # 'proj.callback',

    'apps.news',
    'apps.permits',
    'apps.activities',
    'apps.objects',
]

MIDDLEWARE = (
    'proj.middleware.MultiHostMiddleware',

    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    # 'django.contrib.admindocs.middleware.XViewMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # 'proj.middleware.SetLanguageCookieMiddleware',
    'proj.middleware.MinifyHTMLMiddleware',
)

ROOT_URLCONF = 'www.urls'
HOST_MIDDLEWARE_URLCONF_MAP = {
    'uor.gkcck.ru': 'host.uor.urls',
}
APPEND_SLASH = False

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': 'gkcck.ru_',
            'TIMEOUT': 60 * 60 * 24,
        }
    }
    CACHE_MIDDLEWARE_KEY_PREFIX = 'gkcck.ru_'
    CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 24

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

                'proj.context_processors.yandex',
                'proj.context_processors.google',
                'proj.context_processors.twitter',
            ),
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ) if DEBUG else [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'www.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gkcck--django',
        'USER': 'dev',
        'PASSWORD': 'Dev1234567',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}
DATABASE_ROUTERS = [
    # 'www.CommonDBRouter',
    # 'proj.gallery.GalleryRouter',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGES = (
    ('ru', 'RU'),
)
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_ROOT = os.path.join(ROOT_DIR, 'web', 'assets').replace('\\', '/')
STATIC_URL = '//web.gkcck.ru/assets/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = os.path.join(ROOT_DIR, 'web', 'media').replace('\\', '/')
MEDIA_URL = '//web.gkcck.ru/media/'

SERVER_EMAIL = 'gkcck@yandex.ru'
DEFAULT_FROM_EMAIL = 'default@gkcck.ru'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'default@gkcck.ru'
EMAIL_HOST_PASSWORD = '+1234567'
EMAIL_USE_SSL = True
HOST_MIDDLEWARE_EMAIL_MAP = {
    'gkcck.ru': {
        'EMAIL_SUBJECT_PREFIX': 'ССК',
        'EMAIL_TO': (
            'mail@cckgroup.ru',
            'diaksid@mail.ru',
        ),
    },
    'uor.gkcck.ru': {
        'EMAIL_SUBJECT_PREFIX': 'УОР',
        'EMAIL_TO': (
            'mail@cckgroup.ru',
            'diaksid@mail.ru',
        ),
    },
}

SILENCED_SYSTEM_CHECKS = (
    'urls.W002',
    'admin.E124',
)

# --------------------------------------------------

COMPRESS_ENABLED = not DEBUG
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = (
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.datauri.CssDataUriFilter',
    # 'compressor.filters.cleancss.CleanCSSFilter',
    'compressor.filters.yuglify.YUglifyCSSFilter',
)
COMPRESS_CSS_HASHING_METHOD = None
COMPRESS_CLEAN_CSS_ARGUMENTS = '--s0'
COMPRESS_JS_FILTERS = (
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.yuglify.YUglifyJSFilter',
)
COMPRESS_YUGLIFY_JS_ARGUMENTS = '--beautify --terminal'
COMPRESS_PRECOMPILERS = (
    ('text/scss', 'node-sass --scss'),
    ('text/coffeescript', 'coffee --compile --bare --no-header --stdio'),
    ('text/cjsx', 'cjsx --compile --bare --no-header --stdio'),
)
COMPRESS_REBUILD_TIMEOUT = 60 * 60 * 24 * 7

FILEBROWSER_DIRECTORY = 'uploads/'

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_QUALITY = 80
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_DB = 1

DEBUG_TOOLBAR_PATCH_SETTINGS = False

RECAPTCHA_PUBLIC_KEY = '6Le6eS4UAAAAABr10hIFyeWdz8pGhQoKEB-CCTLj'
RECAPTCHA_PRIVATE_KEY = '6Le6eS4UAAAAAPscU585VRJTkvGnJvasLXTWRb-J'
CAPTCHA_AJAX = False
NOCAPTCHA = True

# --------------------------------------------------

PROJ = dict(
    html=dict(
        minify=not DEBUG,
    ),
)

# --------------------------------------------------

YANDEX = dict(
    ping=True,
    ping_sitemap=True,
    metrika={
        'gkcck.ru': 34428910,
        'uor.gkcck.ru': 35324050,
    },
    search={
        'gkcck.ru': dict(
            searchid=2249469,
            datalist=(
                'строительный контроль',
                'строительный надзор',
            ),
        ),
        'uor.gkcck.ru': dict(
            searchid=2249469,
            datalist=(
                'ремонт квартир',
                'отделка помещений',
            ),
        ),
    },
)

GOOGLE = dict(
    ping=True,
    plus='//plus.google.com/u/0/107952000500022581364',
)

BING = dict(
    ping=True,
)

TWITTER = '//twitter.com/CCKGroup'

# --------------------------------------------------

PERMITS_AFFILIATES = (
    'ООО «ССК»',
    'ООО «ССК-Проект»',
)
