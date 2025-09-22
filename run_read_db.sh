#!/bin/bash

# 设置工作目录
cd /home/devbox/project

# 激活 Python 虚拟环境（如果存在）
# 检查虚拟环境是否存在
if [ ! -d "myprojectenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myprojectenv
fi

# 激活虚拟环境
source myprojectenv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 确保数据库文件存在
if [ ! -f "instance/main.db" ]; then
    echo "Error: instance/main.db not found"
    exit 1
fi

# 运行 read_db.py
echo "Starting database reader..."
python3 read_db.py

# 检查运行状态
if [ $? -eq 0 ]; then
    echo "Database reading completed successfully"
else
    echo "Error: Failed to read database"
    exit 1
fi

