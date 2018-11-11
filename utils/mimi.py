from werkzeug.security import generate_password_hash,check_password_hash


def jiami(password):
    jiami_wd=generate_password_hash(password,method='pbkdf2:sha1:2000',salt_length=8)
    return jiami_wd

def jiemi(pwd,getpwd):
    return check_password_hash(getpwd,pwd)

