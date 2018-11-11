
import jwt
from datetime import datetime,timedelta


SECRECT_KEY='19970806'

def makeToken(telephone,id):
    datetimeInt = datetime.utcnow() + timedelta(hours=5)
    options = {
        'iss': 'lutto.com',
        'exp': datetimeInt,
        'aud': 'webkit',
        'user_id': id,
        'telephone': telephone,
    }
    token = jwt.encode(options, SECRECT_KEY, 'HS256').decode()
    return token

def openToken(token):
    try:
        data=jwt.decode(token, SECRECT_KEY,audience='webkit', algorithms=['HS256'])
        return data
    except Exception as ex:
        print(ex)
        return None


# openToken('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJsdXR0by5jb20iLCJleHAiOjE1Mzk5NDc0NjAsImF1ZCI6IndlYmtpdCIsIm1lc3NhZ2UiOjUxfQ.KWkZa5TwtJuYldi4vswfPGkg_gtIghLgaXtwYc12cJE')
# makeToken(51)
# makeToken('1345')