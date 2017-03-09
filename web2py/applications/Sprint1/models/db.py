#OMG THIS IS A COMMMENT

db = DAL('sqlite://storage.sqlite')

#auth
from gluon.tools import *
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('profile',
                Field('profilepic', 'upload'),
                )

#database for projects
db.define_table('project',
                Field('person_id', 'reference person'),
                Field('title'),
                Field('body', 'text'),
                Field('image', 'upload'),
                Field('category'),
                Field('Youtube_Embed_Link'),
                Field('Vimeo_Embed_Link'),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', 'reference auth_user', default=auth.user_id),
                format='%(title)s')

#db for documents on each project
db.define_table('document',
                Field('project_id', 'reference project'),
                Field('name'),
                Field('file', 'upload'),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', 'reference auth_user', default=auth.user_id),
                format='%(name)s')

#db for posts on each project
db.define_table('post',
                Field('project_id', 'reference project'),
                Field('body', 'text'),
                Field('created_on', 'datetime', default=request.now),
                Field('created_by', 'reference auth_user', default=auth.user_id))

#Person validators
db.person.name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.person.name)]
db.person.email.requires = [IS_NOT_EMPTY(), IS_EMAIL(error_message='Please enter a valid email!')]
db.person.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='Please enter in form 1-123-456-7899')
#db.person.following_id.readable = db.person.person_id.writable = False
#db.person.project_id.readable = db.person.project_id.writable = False


db.project.title.requires = IS_NOT_IN_DB(db, 'project.title')
db.project.body.requires = IS_NOT_EMPTY()
db.project.person_id.readable = db.project.person_id.writable = False
db.project.created_by.readable = db.project.created_by.writable = False
db.project.created_on.readable = db.project.created_on.writable = False
db.project.category.requires =  IS_IN_SET(["Software", "hardware", "Music","Video", "Game", "Product", "Event", "Misc."])

db.post.body.requires = IS_NOT_EMPTY()
db.post.project_id.readable = db.post.project_id.writable = False
db.post.created_by.readable = db.post.created_by.writable = False
db.post.created_on.readable = db.post.created_on.writable = False

db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.project_id.readable = db.document.project_id.writable = False
db.document.created_by.readable = db.document.created_by.writable = False
db.document.created_on.readable = db.document.created_on.writable = False
