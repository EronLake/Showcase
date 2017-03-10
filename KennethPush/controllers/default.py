def call():
    """exposes all registered services, including XML-RPC"""
    return service()

#all people
def index():
    people = db().select(db.person.id, db.person.name, orderby=db.person.name)
    return dict(people=people)
    #projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    #return dict(projects=projects)

#This will give us a list of all posts on the site
#ordered from most to least recent
def feed():
    feed = db(db.post).select(orderby=~db.post.created_on, limitby=(0, 10))
    return dict(feed=feed)
    
#create a new person
def createPerson():
    form = SQLFORM(db.person).process(next=URL('index'))
    return dict(form=form)

#create a project
def createProject():
    form = SQLFORM(db.project).process(next=URL('projects'))
    return dict(form=form)

#fix bug to only show projects by person id
def projects():
    this_project = db.project(request.args) 
    projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    return dict(project=this_project, projects=projects)
    
    #this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    #db.post.project_id.default = this_project.id
    #projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    #return dict(projects=projects)

#show the project and comments
def show():
    this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    db.post.project_id.default = this_project.id
    form = SQLFORM(db.post).process() if auth.user else None
    projectcomments = db(db.post.project_id == this_project.id).select()
    return dict(project=this_project, comments=projectcomments, form=form)

@auth.requires_login()
def edit():
    this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.project, this_project).process(
        next = URL('show', args=request.args))
    return dict(form=form)

@auth.requires_login()
def documents():
    project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    db.document.project_id.default = project.id
    db.document.project_id.writable = False
    grid = SQLFORM.grid(db.document.project_id == project.id, args=[project.id])
    return dict(project=project, grid=grid)

def user():
    return dict(form=auth())

#can download docs
def download():
    return response.download(request, db)
