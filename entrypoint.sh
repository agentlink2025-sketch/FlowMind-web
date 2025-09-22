#!/bin/bash

# 检查虚拟环境是否存在
if [ ! -d "myprojectenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myprojectenv
fi

# 激活虚拟环境
source myprojectenv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python3 app.py
#python test_kimi_search.py
#python test_kimi_stream_search.py