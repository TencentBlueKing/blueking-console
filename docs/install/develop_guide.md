# 本地开发指引

## 准备依赖环境

1. 在本地安装 mysql，并启动 mysql-server

2. 在 mysql 中创建名为 `open_paas` 的数据库
```bash
❯ CREATE DATABASE `open_paas` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

## 准备 Python 开发环境

1. 安装 Python 3.8

可以使用 [pyenv](https://github.com/pyenv/pyenv) 管理本地的 python 环境
- 依照 [相关指引](https://github.com/pyenv/pyenv#getting-pyenv) 安装 pyenv
- 使用 pyenv 安装 Python 3.8

```bash
❯ pyenv install 3.8.13
```

2. 安装项目依赖

本项目使用 [poetry](https://python-poetry.org/) 管理项目依赖。

- 安装 poetry

```bash
❯ pip install poetry
```

- 使用 poetry 安装依赖

```bash
❯ poetry install --no-root
```

完成依赖安装后，便可以使用 poetry 启动项目了，常用命令：
- poetry shell：进入当前的 virtualenv
- poetry run {COMMAND}：使用 virtualenv 执行命令

## 环境配置

配置以下环境变量

```
# 数据库配置
export BK_PAAS_DATABASE_USER='root'
export BK_PAAS_DATABASE_PASSWORD=''
export BK_PAAS_DATABASE_HOST='localhost'
export BK_PAAS_DATABASE_PORT='3306'

export BK_DOMAIN="example.com"
export BK_LOGIN_API_URL="http://example.com/login"
export BK_COMPONENT_API_URL="http://bkapi.example.com"
export BK_IAM_API_URL="http://bkiam-backend.example.com"

export BK_PAAS_PUBLIC_ADDR="devconsole.example.com:8000"  # 本地启动的服务的域名和端口

export BK_PAAS_SECRET_KEY="{应用(bk_paas) 对应的 bk_app_secret}"  # 用于与 ESB 的通信凭证，个人中心修改密码时需要配置该配置项
```

## 启动进程

```bash
❯ python manage.py migrate
❯ python manage.py runserver 8000
```

## 配置本地 hosts  
windows: 在 `C:\Windows\System32\drivers\etc\host` 文件中添加`127.0.0.1 devconsole.example.com:8000`，比如： iam.bking.com。

mac: 执行 `sudo vim /etc/hosts`，添加`127.0.0.1 devconsole.example.com:8000`。

## 访问页面  
使用浏览器开发 `http://devconsole.example.com:8000/` 访问应用。