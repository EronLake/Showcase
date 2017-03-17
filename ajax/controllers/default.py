# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    form = SQLFORM(db.child)
    if form.process().accepted:
        response.flash = 'record inserted'
    return dict(form=form)

def tax():
    form = SQLFORM(db.taxpayer)
    if form.process().accepted:
        response.flash = 'record inserted'
    return dict(form=form)

def edit():
    row = db.taxpayer[request.args(0)]
    form = SQLFORM(db.taxpayer, row, deletable=True)
    if form.process().accepted:
        response.flash = 'record updated'
    return dict(form=form)

def ajax1():
    return dict()

def ajax2():
    return dict()

def ajax3():
    return dict()

def echo():
    return request.vars.name

def echo2():
    # return "jQuery('#target').html(%s);" % repr(request.vars.name)
    return "jQuery('#target').html('Albert');" 

def echo3():
    return request.vars.name

def month_input():
    return dict()

def month_selector():
    if not request.vars.month: return ''
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September' ,'October',
              'November', 'December']
    month_start = request.vars.month.capitalize()
    selected = [m for m in months if m.startswith(month_start)]
    return DIV(*[DIV(k,
                     _onclick="jQuery('#month').val('%s')" % k,
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for k in selected])

def formtest():
    return dict()

def new_post():
    form = SQLFORM(db.post)
    if form.accepts(request, formname=None):
        return DIV("Message posted")

    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])

def list_items():
    items = db().select(db.item.ALL, orderby=db.item.votes)
    return dict(items=items)

def download():
    return response.download(request, db)

def vote():
    item = db.item[request.vars.id]
    new_votes = item.votes + 1
    item.update_record(votes=new_votes)
    return str(new_votes)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


