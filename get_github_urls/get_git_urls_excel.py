import os
import subprocess
import pandas as pd
from tqdm import tqdm

# 定义一个函数来获取项目的Git URL
def get_git_url(path):
    try:
        # 查找项目的.git文件夹
        git_folder = os.path.join(path, '.git')
        if not os.path.exists(git_folder):
            return None

        # 使用git config命令获取项目的远程URL
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], cwd=path, capture_output=True, text=True)
        if result.returncode != 0:
            return None

        return result.stdout.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# 定义一个函数来遍历文件夹并获取每个项目的Git URL
def get_projects(root_path):
    projects = []
    for dirpath, dirnames, filenames in tqdm(os.walk(root_path), desc="Scanning folders"):
        if '.git' in dirnames:
            # 找到一个项目，获取其Git URL
            git_url = get_git_url(dirpath)
            if git_url is not None:
                projects.append({'Folder': dirpath, 'Git URL': git_url})
    return projects

# 获取当前文件夹的路径
current_path = os.getcwd()

# 获取所有项目的Git URL
projects = get_projects(current_path)

# 将结果保存为Excel文件
df = pd.DataFrame(projects)
df.to_excel('projects.xlsx', index=False)