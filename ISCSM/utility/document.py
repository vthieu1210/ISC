import urllib, os, shutil
from django.core.files.storage import FileSystemStorage
from ISCSM.models import Upload, UploadCategory
from ISC.settings import MEDIA_URL, MEDIA_ROOT

def uploadFile(filename, fs, myfile, path, creator):
    if os.path.exists('/media/'+path+filename):
        return {
            'File' : myfile.name,
            'Status' : 'File existed!'
        }
    else:
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = urllib.unquote(fs.url(filename).encode('utf8'))
        Upload.objects.create(file=uploaded_file_url, filename=filename, category=path, creator=creator)
        return {
            'File' : myfile.name,
            'Status' : 'Upload successfully!!'
        }

def deleteFile(id_file_list):
    for id in id_file_list:
        file = Upload.objects.filter(id=id).get()
        path = os.path.join('/media/', file.file.name.replace('/','',1))
        os.remove(path)
        file.delete()

def createCategory(doctype, path, title):
    if UploadCategory.objects.filter(name=doctype).count() > 0:
        return False
    else:
        os.makedirs(os.path.join(MEDIA_ROOT, path[1:]+doctype))
        UploadCategory.objects.create(name=doctype, path=path, title=title)
        return True

def editCategory(doctype_old, doctype_new, path, title):
    if doctype_old != doctype_new and UploadCategory.objects.filter(name=doctype_new).count() > 0:
        return False
    else:
        path_old = os.path.join(path, doctype_old + "/")
        path_new = os.path.join(path, doctype_new + "/")
        #base_url = '/%s/' % doctype_new
        os.rename(MEDIA_URL+path_old, MEDIA_URL+path_new)

        listsubdoctype = UploadCategory.objects.all()
        for doctype in listsubdoctype:
            if path+doctype_old in doctype.path:
                tmp = doctype.path.replace(path_old, path_new)
                UploadCategory.objects.filter(id=doctype.id).update(path = tmp)

        listfile = Upload.objects.filter(category=path_old)
        for file in listfile:
            uploaded_file_url = path_new+file.filename
            Upload.objects.filter(category=path_old).filter(filename=file.filename).update(file=uploaded_file_url, category=path_new)

        UploadCategory.objects.filter(name=doctype_old).update(name=doctype_new, title=title)
        return True

def deleteCategory(id_category_list):
    for id in id_category_list:
        doctype = UploadCategory.objects.filter(id=id).get()
        files = Upload.objects.all()
        subdoctypes = UploadCategory.objects.all()

        path = doctype.path + doctype.name + '/'
        shutil.rmtree(os.path.join(MEDIA_ROOT, path[1:]))
        doctype.delete()
        for file in files:
            if (path in file.category):
                file.delete()
        for subdoctype in subdoctypes:
            if (path in subdoctype.path):
                subdoctype.delete()

def tracebackCategory(path):
    s = path.split('/')
    del s[-2]
    s = '/'.join(s)
    return s
