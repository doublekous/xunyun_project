# xunyun_project

## 主要使用线程池来实现批量检测ip是否异常，检测方式为通过requests库，使用代理池的方式来请求腾讯电脑管家检测ip手段来实现ip检测功能
- 使用方法
### git clone https://github.com/doublekous/xunyun_project.git
### cd ip_is_bd
### 删除掉venv文件夹，自行创建环境文件夹
### pip install -r requirements.txt
### 在settings中配置数据库
```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ip_is_bad',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}
```
### python manage.py runserver 0.0.0.0:8000
