import json
import os

class AuthManager:
    def __init__(self, users):
        self.users = users

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        return user if user and user['password'] == password else None

    def get_user_projects(self, username):
        return self.users.get(username, {}).get('projects', [])

def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在。")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
