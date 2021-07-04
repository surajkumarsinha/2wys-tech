import os
from rest_framework.exceptions import ValidationError
from ..fileSystem.models import FilesModel
from ..authentication.models import User, Account
from .notif import zip_guid
import datetime
import zipfile

def check_cred(user, acc):
    if not User.objects.filter(EmailId=user) or not Account.objects.filter(
            AccountName=acc):
        raise ValidationError("No Such User or Account")


def sign_filter(data, TypeFilter):
    if TypeFilter == "Unsigned":
        return data.filter(IsSigned=False)

    elif TypeFilter == "Signed":
        return data.filter(IsSigned=True)
    else:
        return data


def date_filter(queryset_type_date, start_date, end_date):
    if end_date:
        end_date_arr = date_format(end_date)
        queryset_type_date = queryset_type_date.filter(Date__lte=datetime.date(end_date_arr[2],
                                                                               end_date_arr[1],
                                                                               end_date_arr[0]))

    if start_date:
        start_date_arr = date_format(start_date)
        queryset_type_date = queryset_type_date.filter(Date__gte=datetime.date(start_date_arr[2],
                                                                               start_date_arr[1],
                                                                               start_date_arr[0]))


    # print(l)
    return queryset_type_date


def date_format(date):
    date = date.split('/')
    date = [int(numeric_string) for numeric_string in date]
    return date


def user_filter(acc_id, user):
    if not user:
        return FilesModel.objects.filter(Account=acc_id)
    else:
        user_id = User.objects.get(EmailId=user).id
        return FilesModel.objects.filter(User=user_id,
                                         Account=acc_id
                                         )

def create_zip(queryset, is_guid, name, user):
    filenames = []
    
    for i in range(len(queryset)):
        if not is_guid:
            fid = queryset[i]
            fname = FilesModel.objects.get(pk=str(fid)).File 
        else:       
            fname = queryset[i].File

        filenames.append('media/'+ str(fname))

    zip_subdir = ""
    if is_guid:
        guid = zip_guid.make_token(user)
        zip_filename = "media/zipfiles/"+ name + "_" + str(guid) +".zip"
    
    else:
        zip_filename = "media/zipfiles/"+ name + ".zip"

    zf = zipfile.ZipFile( zip_filename, "w", compression=zipfile.ZIP_DEFLATED)

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()

    return zip_filename

def check_dir_path(dir, subdir):
    if not os.path.isdir(dir + "/" + subdir):
        parent_dir = os.path.abspath(dir) 
        pth = os.path.join(parent_dir, subdir)
        os.mkdir(pth)