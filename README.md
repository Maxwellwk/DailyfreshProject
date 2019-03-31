### B2C电商平台
本项目基于 Python的Django框架开发，用到的技术有mysql双机热备、celery异步通信、非关系数据库redis、fastDFS分布式文件系统、uwsgi+nginx、whoosh+haystack+jieba全文检索、事务回滚、并发访问控制、负载均衡集群、对接第三方(支付宝)支付等。
#### 如何部署
##### 1.先将项目clone到本地 
git clone https://github.com/Maxwellwk/DailyfreshProject.git
##### 2.进入自己创建的python3.7虚拟环境（传送门：如何创建虚拟环境https://blog.csdn.net/qq_26870933/article/details/81502484）， 执行pip install -r requirements.txt
pip install -r requirements.txt
##### 3.配置mysql主从同步（传送门：https://blog.csdn.net/qq_26870933/article/details/85041432）， 并更改setting中DATABASES里面的HOST（本机），安装mysql并创建对应的数据库。
...<br>
DATABASES = {<br>
    'default': {<br>
        'ENGINE': 'django.db.backends.mysql',<br>
        'HOST': '10.*.*.101',<br>
        'PORT': 3306,<br>
        'USER': 'root',<br>
        'PASSWORD': 'root',<br>
        'NAME': 'dailyfresh'<br>
    },<br>
    'slave': {<br>
        'ENGINE': 'django.db.backends.mysql',<br>
        'HOST': '10.*.*.102',<br>
        'PORT': 3306,<br>
        'USER': 'root',<br>
        'PASSWORD': 'root',<br>
        'NAME': 'dailyfresh'<br>
    }<br>
}<br>
#读写分离路由器<br>
DATABASE_ROUTERS = ["utils.db_router.MasterSlaveDBRouter"]<br>
...<br>
##### 4.在settings.py中将邮箱更改为你自己的邮箱地址
#Email<br>
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'<br>
EMAIL_HOST = 'smtp.126.com'<br>
EMAIL_PORT = 25<br>
EMAIL_HOST_USER = 'ma########@163.com'<br>
EMAIL_HOST_PASSWORD = 'w#########3'<br>
EMAIL_FROM = '天天生鲜<ma#########@163.com>'<br>
##### 5.在settings.py中将CACHES中的redis地址换成自己本机的地址
#缓存<br>
CACHES = {<br>
    "default": {<br>
        "BACKEND": "django_redis.cache.RedisCache",<br>
        "LOCATION": "redis://10.*.*.101:6379/5",<br>
        "OPTIONS": {<br>
            "CLIENT_CLASS": "django_redis.client.DefaultClient",<br>
        }<br>
    }<br>
}<br>
##### 6.在settings.py中将fastdfs的地址更换
#FastDFS使用的配置信息<br>
FASTDFS_CLIENT = os.path.join(BASE_DIR, "utils/fastdfs/client.conf")<br>
FASTDFS_URL = "http://10.*.*.101:8888/"<br>
##### 7.在settings.py中更改ALIPAY_APPID和ALIPAY_URL（传送门：https://blog.csdn.net/qq_41664526/article/details/80571743）
ALIPAY_APPID = "20160#########1638"<br>
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"<br>
##### 8.在celery_tasks/tasks.py中更改broker的IP地址
app = Celery("celery_tasks.tasks", broker="redis://10.*.*.101/4")
##### 9.在utils/fastdfs/client.conf中更改tracker_server，base_path（fastdfs日志存放位置）
base_path=/Users/自定义日志文件路径/fastdfs_log<br>
tracker_server=10.*.*.101:22122<br>
##### 10.使用uwsgi+ngin部署项目（传送门：https://blog.csdn.net/qq_26870933/article/details/86699083）， 更改uwsgi.ini中的IP，项目地址，虚拟环境地址
[uwsgi]<br>
#使用nginx连接时使用<br>
socket=10.*.*.101:8000<br>
#直接做web服务器使用<br>
#http=10.*.*.101:8000<br>
#项目目录<br>
chdir=/Users/项目地址/dailyfresh<br>
#项目中wsgi.py文件的目录，相对于项目目<br>
wsgi-file=dailyfresh/wsgi.py<br>
processes=4<br>
threads=2<br>
master=True<br>
pidfile=uwsgi.pid<br>
#在后台运行,信息保存的日志文件<br>
daemonize=uwsgi.log<br>
#虚拟环境目录<br>
virtualenv=/Users/虚拟环境地址/b2cenv<br>
##### 11.开启项目，在项目目录下，先执行数据库迁移命令，再分别开启uwsgi,celery,nginx
#生成迁移文件<br>
python manage.py makemigrations<br>
#执行迁移<br>
python manage.py migrate<br>
#开启uwsgi<br>
uwsgi --ini uwsgi.ini<br>
#收集所有静态文件到static_root指定目录<br>
python manage.py collectstatic<br>
#初始化索引数据<br>
python manage.py rebuild_index<br>
#开启redis<br>
sudo service redis start<br>
#开启worker<br>
celery -A dailyfresh worker -l info<br>
#开启nginx<br>
sudo sbin/nginx<br>
### ⚠️ 本人省略了whoosh,fastdfs,nginx,mysql,redis的详细安装过程，因为网上有大量的安装教程，大家动动手搜一搜即可配置成功，我这里就不再赘述了，祝君成功！





