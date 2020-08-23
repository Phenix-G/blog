# 从仓库拉取 带有 python 3.7 的 Linux 环境
FROM python:3.7.4

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 添加这两行
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code
# 更新 pip
RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
# 将 requirements.txt 复制到容器的 code 目录
# ADD requirements.txt /code/
# 安装库
# RUN pip install pipenv

# 将当前目录复制到容器的 code 目录
ADD . /code/

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
