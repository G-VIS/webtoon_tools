from .separate import SeparateHighlight

import os
import subprocess
import sys

def install_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if os.path.isfile(requirements_path):
        print(f'requirements.txt が見つかりました: {requirements_path}')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        except subprocess.CalledProcessError as e:
            print(f'requirements.txt のインストールに失敗しました: {e}')
    else:
        print('requirements.txt が見つかりません。必要なパッケージは手動でインストールしてください。')

# パッケージのインストールを実行
install_requirements()


NODE_CLASS_MAPPINGS = {
    "SeparateHighlight": SeparateHighlight
}