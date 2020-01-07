# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'



# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

PHOTO_URL_PREFIX = "/{}/static/capture/vehicles".format(request.application)


db.define_table('tunnel', 
                Field('uniqueID', length=128, unique=True),
                Field('displayName', length=128, required=False),
                Field('textDescription', 'text', required=False),
                format='%(displayName)s [%(uniqueID)s]'
                )


db.define_table('pole',
                Field('uniqueID', 'string', length=128, required=True, unique=True),
                Field('displayName', 'string', length=128, required=False),
                Field('textDescription', 'text', required=False),
                Field('tunnelID', 'reference tunnel', required=False),
                format='%(displayName)s [%(uniqueID)s]'
                )


db.define_table('camera',
                Field('uniqueID', 'string', length=128, required=True, unique=True),
                Field('displayName', 'string', length=128, required=True),
                Field('textDescription', 'text', required=False),
                Field('poleID', 'reference pole', required=False),
                format='%(displayName)s [%(uniqueID)s]'
                )


db.define_table('tunnelInfo',
                Field('tunnelID', 'reference tunnel', required=True),
                )


db.define_table('poleInfo',
                Field('poleID', 'reference pole', required=True),
                )


db.define_table('cameraInfo',
                Field('cameraID', 'reference camera', required=True),
                Field('IPaddress', 'string', length=64, required=True),
                Field('resW', 'integer', required=False, default=1920),
                Field('resH', 'integer', required=False, default=1080),
                Field('config', 'text', required=True)
                )


db.define_table('vehicle_records',
                Field('uniqueID', 'string', length=128, required=True, unique=True),
                Field('cameraID', 'reference camera', required=True),
                Field('laneNumber', 'integer', required=True),
                Field('direction', 'integer', required=False),
                Field('checkPointTime', 'integer', required=True),
                Field('vehicleClassConfidence', 'integer', required=True),
                Field('vehicleClassId', 'integer', required=True),
                Field('speedKmh', 'double', required=False, default=0),
                Field('plateConfidence', 'integer', required=True, default=0),
                Field('plateType', 'string', length=128, required=False),
                Field('plateColor', 'string', length=128, required=False),
                Field('license', 'string', length=128, required=False)
                )


db.define_table('photo',
                Field('name', 'string', required=True),
                Field('record_id', 'reference vehicle_records', required=True),
                Field('upload_time', 'datetime', default=request.now)
                )

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
