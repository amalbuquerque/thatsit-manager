from datetime import datetime

def hello1():
    """ simple page without template """

    return "Hello World! Movies: " + settings.movies_path

def create1():
    xpto_spot = get_or_create(db.spot, filename=request.vars.name, \
            description="", time=30, position=2, uploader="admin", \
            timestamp = datetime.now())

    return "I think I've created something: {0}-{1} by {2} @ {3}".format( \
            xpto_spot.id, xpto_spot.filename, xpto_spot.uploader, xpto_spot.timestamp)

def check1():
    xpto_spot = get(db.spot, filename=request.vars.name)
    if (xpto_spot == None):
        return "Sorry. Nothing"
    return "I think I've found something: {0}-{1} by {2} @ {3}".format( \
            xpto_spot.id, xpto_spot.filename, xpto_spot.uploader, xpto_spot.timestamp)

def log_test():
    logger.debug("DEBUG WELL")
    logger.warning("WARNING WELL")

def upload():
    """
    Action utilizada inicialmente para apresentar
    o Form, e onde este vem bater depois de submetido.
    (seja operação de INSERT ou DELETE)
    """
    # record = db.spot(request.args(0)) or redirect(URL('index'))
    # tenta obter o spot com id passado por querystring: /id
    # se nao existir, fica como None e o SQLFORM sera um INSERT
    # form, se existir sera um UPDATE form
    logger.debug("UPLOAD CALLED")
    record = db.spot(request.args(0))
    form = SQLFORM(db.spot, record, deletable=False, upload=URL('download'),\
            submit_button='Gravar',\
            # campos que queremos que sejam apresentados
            fields=['description', 'time', 'position', 'movie', 'uploader'])

    # record == None entao nao existia anteriormente
    # na BD
    if request.vars.movie != None and record == None:
        logger.debug("Uploaded a file *{}* with {} bytes"\
                .format(request.vars.movie.filename,\
                len(request.vars.movie.value)))
        # filename e preenchido pela action
        form.vars.filename = request.vars.movie.filename
        form.vars.timestamp = datetime.now()

    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def download():
    return response.download(request, db)

def upload_example_old():
    """
    Renomeei em 2013/1/14 para old, para utilizar
    o SQLFORM disponibilizado out-of-the-box pelo
    web2py (permite nao guardar imediatamente na
    BD, pelo que podemos em vez disso fazer o
    upload via WebService para o cliente -
    realizado nas actions upload_first() e upload_new()
    """
    response.files.append(URL(r=request, c='static/js', f='fileuploader.js'))
    response.files.append(URL(r=request, c='static/css', f='fileuploader.css'))
    response.files.append(URL(r=request, c='static/js/thatsit/global', f='use_fileuploader.js'))

    form = FORM(TABLE(
        TR('Filename:', INPUT(_type='text', _name='arg_filename',
           requires=IS_NOT_EMPTY())),
        TR('Description:', TEXTAREA(_name='arg_description',
           value='write something here')),
        TR('Time (in secs):', INPUT(_type='int', _name='arg_time',
           requires=IS_NOT_EMPTY(), value=20)),
        TR('Position:', INPUT(_type='int', _name='arg_position',
           requires=IS_NOT_EMPTY(), value=0)),
        TR('Your email:', INPUT(_type='text', _name='email',
           requires=IS_EMAIL())),
        TR('Admin', INPUT(_type='checkbox', _name='admin')),
        TR('Sure?', SELECT('yes', 'no', _name='sure',
           requires=IS_IN_SET(['yes', 'no']))),
        TR('Profile', TEXTAREA(_name='profile',
           value='write something here')),
        TR('', INPUT(_type='submit', _value='SUBMIT')),
        ))

    return dict(message = "test message from controller", form=form)

def upload_old():
    """
    Permite utilizador fazer o upload de um spot e de
    criar a BE correspondente na BD. Sera implementado
    do lado do manager.
    1. Guarda ficheiro nos uploads
    2. Converte o movie para .swf
    3. Invoca o WebService do Cliente para fazer o upload
       do filme
    """
    try:
        for r in request.vars:
            if r=="qqfile":
                filename = request.vars.qqfile
                # process the file here
                gen_filename = db.spot.file.store(request.body, filename)
                logger.debug("Wrote {} bytes to {}"\
                        .format(len(request.body), filename))
                logger.warning("*Warning*Wrote {} bytes to {}"\
                        .format(len(request.body), filename))
                # db.document.insert(file=db.spot.file.store(request.body,filename))
                return response.json({'success': 'true',\
                        'upl_file' : filename,\
                        'new_file' : gen_filename})
    except:
        return response.json({'success': 'false'})
