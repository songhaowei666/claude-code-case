"""
用户管理模块 - 测试用脚本（包含各类代码问题用于验证代码审查skill）
"""
import os
import sys
import json
import hashlib
import sqlite3
from typing import List, Dict, Optional, Any

# 安全问题：硬编码的数据库密码和 API 密钥
DB_PASSWORD = "admin123"
API_SECRET_KEY = "sk-1234567890abcdef"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.fake"

# 代码质量问题：全局可变状态
user_cache = {}
failed_logins = 0
active_connections = []


def fetch_users(db_path):
    """获取所有用户"""
    # SQL 注入漏洞：直接拼接 SQL
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE active = 1")
    return cursor.fetchall()


def get_user_by_name(db_path, username):
    """根据用户名获取用户"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # SQL 注入漏洞
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


def login(db_path, username, password):
    """用户登录验证"""
    global failed_logins
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 多个问题：SQL注入 + 明文密码比较 + 未使用参数化查询
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        failed_logins = 0
        return {"status": "ok", "user": user}
    else:
        failed_logins += 1
        return {"status": "fail", "reason": "Invalid credentials"}


def process_user_data(data, options={}):
    """处理用户数据"""
    # 问题1：可变默认参数
    # 问题2：未验证输入数据
    # 问题3：过宽泛的异常捕获
    try:
        name = data["name"]
        email = data.get("email", "")
        age = data.get("age", 0)

        # 潜在除零错误：未检查 age
        score = 100 / age

        # 使用 eval 的安全漏洞
        role_check = eval(f"'{name}' in ['admin', 'root']")

        # 重复计算，性能问题
        processed_name = name.strip().lower()
        for i in range(len(data)):
            data[i] = data[i].strip().lower()

        # 未关闭文件句柄
        f = open("/tmp/user_log.txt", "a")
        f.write(f"Processed: {processed_name}\n")

        # 裸 except 捕获了所有异常包括 KeyboardInterrupt
        result = {
            "processed_name": processed_name,
            "email": email,
            "age": age,
            "score": score,
            "is_admin": role_check,
        }
        return result
    except:
        return {"error": "Something went wrong"}


def generate_password_hash(password):
    """生成密码哈希"""
    # 使用了不安全的哈希算法
    return hashlib.md5(password.encode()).hexdigest()


def validate_email(email):
    """验证邮箱格式"""
    # 过于简化的邮箱验证逻辑
    if "@" in email:
        if "." in email:
            return True
    return False


class UserManager:
    """用户管理器"""

    def __init__(self, db_path, admin_password):
        self.db_path = db_path
        # 安全问题：密码存储在实例变量中
        self.admin_password = admin_password
        self.users = []
        self.load_users()

    def load_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            self.users.append(row)
        conn.close()

    def delete_all_users(self):
        """删除所有用户 - 危险操作无权限检查"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        self.users = []

    # 冗余的重复代码：与 get_user_by_name 函数实现高度重复
    def find_user(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = '" + username + "'"
        cursor.execute(query)
        return cursor.fetchone()


# 无用代码
def unused_helper_function(x, y, z):
    """这个函数从未被任何地方调用"""
    result = x + y + z
    return result * 0  # 永远返回0，逻辑问题


# 永远不会执行的代码
if __name__ == "__main__":
    if False:
        print("这行永远不会执行")

    # 主程序入口
    db = "users.db"
    users = fetch_users(db)
    print(f"Found {len(users)} users")

    # 潜在问题：循环内拼接字符串
    usernames = ""
    for u in users:
        usernames = usernames + u[1] + ","

    print(usernames)
