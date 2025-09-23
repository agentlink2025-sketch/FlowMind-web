#!/bin/bash

# 检查虚拟环境是否存在
if [ ! -d "myprojectenv1" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myprojectenv1
fi

# 激活虚拟环境
source myprojectenv1/bin/activate

# 安装依赖
#pip install -r requirements.txt
pip install -r requirements.txt -i https://pypi.org/simple --timeout 180 --retries 10


# 运行应用
python3 app.py
#python test_kimi_search.py
#python test_kimi_stream_search.py