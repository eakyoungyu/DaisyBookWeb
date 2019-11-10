# 장고 사용법
### 프로젝트 경로
C:\Users\eakyo\workspace\PycharmProjects\webapp
### 앱 추가
> python magnage.py startapp appname\
> manage.py migrate
### 관리자 추가
> manage.py create superuser
### 서버 열기
> manage.py runserver
### model 변경 시
> manage.py makemigrations\
> manage.py migrate
### celery
> celery -A webapp worker -l info -P eventlet