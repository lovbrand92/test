import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import time
while True:
    print('hi')
    time.sleep(3)
cred = credentials.Certificate("fireb-722bb-2b80a512daf0.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "fireb-722bb.appspot.com"
})

db = firestore.client()


def sign_up_set_src():
    user_corp = str(sign_up())
    src = input('링크를 입력하시오(링크만): ')

    db.collection(u'Companies').document(u'{}'.format(user_corp)).set({'src': str(src)})


def sign_up():
    user_email = input('email을 입력하시오: ')
    password = input('비밀번호를 입력하시오: ')
    user = auth.create_user(
        email=str(user_email),
        email_verified=False,
        password=str(password),
        disabled=False)

    user_corp = input('회사명을 입력하시오: ')

    db.collection(u'Users').document(u'{}'.format(user_email)).set({'company': u'{}'.format(user_corp)})
    return user_corp


def set_src():
    user_corp = input('회사명을 입력하시오: ')
    src = input('링크를 입력하시오(링크만): ')

    db.collection(u'Companies').document(u'{}'.format(user_corp)).set({'src': str(src)})


coms = db.collection(u'Companies').stream()
print('-------현재 회사 목록------')
for com in coms:
    try:
        print('name:', com.id, ', src:', com.to_dict()['src'])
    except KeyError:
        print('name:', com.id, ', src 미입력 상태')
print('-------------------------')
print(
    "1: 신규 기업 회원가입(링크 추가 포함)"
    "\n2: 기존 기업 계정 추가(링크 추가 미포함)"
    "\n3: 기존 기업 링크 수정"
    "\n4: 나가기"
)
a = input('무엇을 할거요(숫자만 입력하시오): ')

if a == "1":
    sign_up_set_src()

elif a == "2":
    sign_up()

elif a == "3":
    set_src()
elif a == "4":
    exit()
else:
    print('다시해')
