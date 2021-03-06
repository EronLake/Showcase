def call():
    """exposes all registered services, including XML-RPC"""
    return service()

@auth.requires_login()
def edit_profile():
    profiles = db.profile[request.args(0)]
    if(profiles and profiles.user_id == auth.user_id):
        form = SQLFORM(db.profile, profile,
                 showid= False,
                 deletable= True,
                 submit_button = 'Update your Profile'

                  )

        if form.process(keepvalues=True).accepted:
           response.flash = 'listing accepted'
           redirect(URL('index'))
        elif form.errors:
           response.flash = 'please complete your post'
        else:
           response.flash = 'please edit your comment'

        return dict(form=form)
def create_profile():
    form = SQLFORM(db.profile, 
                 labels= {'Listing_Descript': "Description", 'seller': "Seller"},
                 submit_button = 'Submit your listing',
                 
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'comment accepted'
       
    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please post your listing'

    return dict(form=form)
def feed():
    feed = db(db.project).select(orderby=~db.project.created_on, limitby=(0, 10))
    return dict(feed=feed)

#shows projects
def index1():
    projects = get_projects
    #return dict(people=people)
    projects = db().select(db.project.id, db.project.title, orderby=db.project.title)
    return dict(projects=projects)

#make smartgrid show users and link projects
def index():
    default_sort_order = [db.project.id]
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
                        deletable=False,
                        editable=False,
                        details=False,
                        links = [lambda row: A('View Post',_href=URL("default","show",args=[row.id]))],
                        paginate=50)
    return dict(grid=grid)


def get_projects():
    """get posts, in reverse chronological order"""
    return db(db.project).select().sort(lambda p: p.updated_on, reverse=True)
#create a new person
#def createPerson():
#form = SQLFORM(db.person).process(next=URL('index'))
#return dict(form=form)

#create a project
def createProject():
    form = SQLFORM(db.project).process(next=URL('projects'))
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
@auth.requires_login()
def profile():
    this_bio = auth.user.bio
    this_picture = auth.user.profilepic
    return dict(picture=this_picture,bio=this_bio)
