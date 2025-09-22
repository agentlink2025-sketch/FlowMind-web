from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# 创建 Flask 应用
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    daily_queries = db.Column(db.Integer, default=0)
    last_query_date = db.Column(db.Date, default=datetime.now().date())

# 定义聊天记录模型
class ChatRecord(db.Model):
    __tablename__ = 'chat_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_time = db.Column(db.DateTime, default=datetime.now)
    intent_result = db.Column(db.Text)
    model_response = db.Column(db.Text)
    file_id = db.Column(db.String(36))

def read_user_data():
    """读取用户数据"""
    try:
        with app.app_context():
            users = User.query.all()
            print("\n=== 用户数据 ===")
            for user in users:
                print(f"ID: {user.id}")
                print(f"手机号: {user.phone}")
                print(f"每日查询次数: {user.daily_queries}")
                print(f"最后查询日期: {user.last_query_date}")
                print("-" * 30)
    except Exception as e:
        print(f"读取用户数据时出错: {str(e)}")

def read_chat_records():
    """读取聊天记录"""
    try:
        with app.app_context():
            chat_records = ChatRecord.query.all()
            print("\n=== 聊天记录 ===")
            for record in chat_records:
                print(f"记录ID: {record.id}")
                print(f"用户ID: {record.user_id}")
                print(f"问题: {record.question}")
                print(f"提问时间: {record.question_time}")
                print(f"意图结果: {record.intent_result}")
                print(f"模型响应: {record.model_response[:100]}..." if record.model_response else "无响应")
                print(f"文件ID: {record.file_id}")
                print("-" * 30)
    except Exception as e:
        print(f"读取聊天记录时出错: {str(e)}")

def get_user_chat_history(user_id):
    """获取特定用户的聊天历史"""
    try:
        with app.app_context():
            user = User.query.get(user_id)
            if not user:
                print(f"未找到ID为 {user_id} 的用户")
                return

            print(f"\n=== 用户 {user.phone} 的聊天历史 ===")
            chat_records = ChatRecord.query.filter_by(user_id=user_id).all()
            
            for record in chat_records:
                print(f"时间: {record.question_time}")
                print(f"问题: {record.question}")
                print(f"意图: {record.intent_result}")
                print(f"响应: {record.model_response[:100]}..." if record.model_response else "无响应")
                print("-" * 30)
    except Exception as e:
        print(f"获取用户聊天历史时出错: {str(e)}")

if __name__ == '__main__':
    # 读取所有用户数据
    read_user_data()
    
    # 读取所有聊天记录
    read_chat_records()
    
    # 获取特定用户的聊天历史（替换为实际的用户ID）
    # get_user_chat_history(1) 