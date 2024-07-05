# 来源：https://blog.rappit.site/2024/04/22/obfuscated-shell-scripts/

import os
import uuid
import base64

# 读取你的脚本
with open('script.sh', 'r') as f:
    script = f.read()

# 使用 base64 对你的脚本进行编码
encoded_script = base64.b64encode(script.encode()).decode()

# 定义每个字符串段的大小
chunk_size = 4

# 将编码后的脚本分割成多个小段
chunks = [encoded_script[i:i+chunk_size]
          for i in range(0, len(encoded_script), chunk_size)]

# 创建一个新的文件来存储最终的脚本
with open('final_script.sh', 'w') as f:
    # 输出每个变量赋值语句
    variable_names = []
    for chunk in chunks:
        while True:
            var_name = str(uuid.uuid4()).replace('-', '')  # 生成一个 UUID 作为变量名
            if not var_name.startswith('0') and not var_name.startswith('1') and not var_name.startswith('2') and not var_name.startswith('3') and not var_name.startswith('4') and not var_name.startswith('5') and not var_name.startswith('6') and not var_name.startswith('7') and not var_name.startswith('8') and not var_name.startswith('9'):
                break
        variable_names.append(var_name)
        f.write(f'{var_name}=\'{chunk}\'\n')

    # 输出连接所有变量的语句
    f.write('eval "$(echo -n "')
    for var_name in variable_names:
        f.write(f'${var_name}')
    f.write('" | base64 --decode)"')

# 修改文件权限，使其可执行
os.chmod('final_script.sh', 0o755)
