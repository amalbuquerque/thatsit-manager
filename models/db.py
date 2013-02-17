#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################
from gluon.contrib import simplejson as json

response.generic_patterns = ['*']

# use SQLite
db = DAL('sqlite://storage.sqlite')

db.define_table(
    'spot',
    Field('filename', notnull=True, unique=True),
    Field('description'),
    # in seconds
    Field('time', 'integer', notnull=True),
    Field('position', 'integer'),
    Field('movie', 'upload'),
    Field('uploader', notnull=True),
    Field('timestamp', 'datetime', notnull=True),
    # how records of this table should be represented
    # when referenced by another table in forms (dropboxes)
    format = '%(filename)s',
    singular = 'Spot',
    plural = 'Spots',
    )

db.spot.filename.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'spot.filename')]
db.spot.uploader.requires = IS_NOT_EMPTY()
db.spot.time.requires = IS_INT_IN_RANGE(1, 300)

db.define_table(
    'outdoor',
    Field('name', notnull=True, unique=True),
    Field('description'),
    Field('ip', notnull=True),
    Field('port', 'integer', notnull=True),
    Field('liveat', 'datetime'),
    Field('lastspotseen'),
    # how records of this table should be represented
    # when referenced by another table in forms (dropboxes)
    format = '%(name)s',
    singular = 'Outdoor',
    plural = 'Outdoors',
    )

db.outdoor.name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'outdoor.name')]

db.define_table('uploadedto',
                    Field('outdoor', 'reference outdoor'),
                    Field('spot', 'reference spot'),
                    Field('to_delete', 'boolean'),
                    Field('uploaded_at', 'datetime'))

# permite isto:
# for out_spot in outdoors_and_spots(db.outdoor.name=='ericeira1').select():
#       print out_spot.spot.filename
 
outdoors_and_spots = db(
        (db.outdoor.id==db.uploadedto.outdoor) & (db.spot.id==db.uploadedto.spot))

def get(table, **fields):
	"""
	Returns record from table with passed field values.
	'table' is a DAL table reference, such as 'db.spot'
	fields are field=value pairs
    Returns only first row with the given criteria
    Example:
        xpto_spot = get(db.spot, filename="xptoone.swf", \
                description="", time=30, position=2, uploader="admin")
	"""
	return table(**fields)

def get_json(table, **fields):
    to_return = get(table, **fields)
    json_to_return = None
    if(table == db.spot):
        json_to_return = get_json_spot(to_return)

    if(json_to_return != None):
        return json.dumps(json_to_return)

    return to_return

def get_json_spot(to_return):
    if(to_return == None):
        return dict()
    return dict(\
        filename=to_return.filename,\
        description=to_return.description,\
        time=to_return.time,\
        position=to_return.position,\
        uploader=to_return.uploader,\
        timestamp=str(to_return.timestamp))

def get_or_create(table, **fields):
	"""
	Returns record from table with passed field values.
	Creates record if it does not exist.
	'table' is a DAL table reference, such as 'db.spot'
	fields are field=value pairs
    Example:
        xpto_spot = get_or_create(db.spot, filename="xptoone.swf", \
                description="", time=30, position=2, uploader="admin", \
                timestamp = datetime.now())
	"""
	return table(**fields) or table.insert(**fields)

def update_or_create(table, fields, updatefields):
	"""
	Modifies record that matches 'fields' with 'updatefields'.
	If record does not exist then create it.
	
	'table' is a DAL table reference, such as 'db.spot'
	'fields' and 'updatefields' are dictionaries
    Example:
        xpto_spot = update_or_create(db.spot, dict(filename="xptoone.swf"), \
                dict(filename="xpto_new_name.swf"))
	"""
	row = table(**fields)
	if row:
		logger.debug("Row existed. Updating")
		row.update_record(**updatefields)
	else:
		logger.debug("New row. Inserting")
		fields.update(updatefields)
		row = table.insert(**fields)
	return row

def delete(table, **keys_to_search):
    return table.delete(**keys_to_search)
