#约自习平台
#模板文件(.html)放在templates中
#在templates同级建立static文件夹，并将css,js 图片等放在static中
#请先配置config.py中的SQLALCHEMY_DATABASE_URI 和邮箱的配置
#tmp文件用来放日志
## Virtual Environment
    $pip install virtualenv
    $ virtualenv --no-site-packages venv
    $ source venv/bin/activate

## Install Extensions

    $ pip install -r requirment.txt
## Run
    $ python run.py



