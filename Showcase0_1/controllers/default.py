"""
def call():
    exposes all registered services, including XML-RPC
    return service()
"""

@auth.requires_login()
def profile():
    projects = get_projects()
    last_project = projects.first()
    project_count = len(projects)
    this_bio = auth.user.bio
    this_picture = auth.user.profilepic
    #project_title ="title"
    #project_body = "body"
    print "project_count: %s" % project_count
    return dict(picture=this_picture,bio=this_bio,last_project=last_project,project_count = project_count)

def get_projects():
    """get posts, in reverse chronological order"""
    return db(db.project).select().sort(lambda p: p.created_on, reverse=True)

def feed():
    feed = db(db.document).select(orderby=~db.document.created_on)
    comments = db(db.post).select(orderby=~db.post.created_on)
    form = SQLFORM(db.post)
    following = db(db.following.user_id == auth.user_id).select()
    return dict(feed=feed, comments=comments, form=form, following=following)
    """feed = db(db.project).select(orderby=~db.project.created_on, limitby=(0, 10))
    return dict(feed=feed)"""

#shows projects
def index1():
    projects = get_projects
    #return dict(people=people)
    projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    return dict(projects=projects)

#make smartgrid show users and link projects
def index():
    """default_sort_order = [db.project.id]
    fields = (db.project.title,  db.auth_user.first_name)
    headers = {
        'project.title': 'Title',
        ' db.auth_user.first_name': 'Body'
    }


    grid = SQLFORM.grid(db.project,
                        fields=fields,
                        headers=headers,
                        orderby=default_sort_order,
                        create=False,
                        csv=False,
                        deletable=False,
                        editable=False,
                        details=False,
                        links = [lambda row: A('View Post',_href=URL("default","show",args=[row.id]))],
                        paginate=50)"""
    feed = db(db.project).select(orderby=~db.project.created_on)
    return dict(feed=feed)


#create a new person
#def createPerson():
#form = SQLFORM(db.person).process(next=URL('index'))
#return dict(form=form)

#create a project
def createProject():
    form = SQLFORM(db.project,
                 labels= {'project_title': "Title", 'project_body': "Body"},
                 submit_button = 'Make a project!',
                  )
    if form.process(keepvalues=True).accepted:
        response.flash = 'Project made!'
    else:
        response.flash = 'errors, please check with administrator'
    return dict(form=form)

def projects():
    this_project = db.project(request.args(0, cast=int))
    projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    return dict(project=this_project, projects=projects)

#this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
#db.post.project_id.default = this_project.id
#projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
#return dict(projects=projects)

#show the project and comments
def show():
    comments = db(db.post).select(orderby=~db.post.created_on)
    this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    db.document.project_id.default = this_project.id
    form = SQLFORM(db.document)#.process() #if auth.user else None
    if form.process(keepvalues=True).accepted:
       response.flash = 'post accepted'
    elif form.errors:
       response.flash = 'please complete your post'
    projectposts = db(db.document.project_id == this_project.id).select()
    projectcollaborators = db(db.collaborators.project_id == this_project.id).select()
    return dict(project=this_project, posts=projectposts, comments=comments, form=form, collaborators=projectcollaborators)
    """this_project = db.project(request.args(0, cast=int)) or redirect(URL('index'))
    db.document.project_id.default = this_project.id
    form = SQLFORM(db.post).process() if auth.user else None
    projectcomments = db(db.document.project_id == this_project.id).select()
    projectcollaborators = db(db.collaborators.project_id == this_project.id).select()
    return dict(project=this_project, comments=projectcomments, form=form, collaborators=projectcollaborators)"""

@auth.requires_login()
def add_collaborator():
    newform = SQLFORM(db.collaborators)
    if newform.process(keepvalues=True).accepted:
        response.flash = 'Collaborator added!'
    else:
        response.flash = 'errors, please check with administrator'
    return dict(newform=newform)

@auth.requires_login()
def following():
    newnewform = SQLFORM(db.following)
    if newnewform.process(keepvalues=True).accepted:
        response.flash = 'followed'
    else:
        response.flash = 'errors, please check with administrator'
    return dict(newnewform=newnewform)

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
