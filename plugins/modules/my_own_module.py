#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Создает текстовый файл с заданным содержимым
version_added: "1.0.0"
description:
    - Этот модуль создает или обновляет текстовый файл по указанному пути.
    - Если файл уже существует с тем же содержимым, изменений не происходит.
options:
    path:
        description:
            - Путь к файлу, который нужно создать или обновить.
        required: true
        type: str
    content:
        description:
            - Содержимое файла.
        required: false
        type: str
        default: ''
author:
    - Andrew (@ваш_github)
'''

EXAMPLES = r'''
# Создать файл с содержимым
- name: Create a file with content
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/hello.txt
    content: "Hello World!"

# Создать пустой файл
- name: Create empty file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/empty.txt

# Обновить существующий файл
- name: Update file content
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/config.txt
    content: |
      server_name: example.com
      port: 8080
'''

RETURN = r'''
path:
    description: Путь к файлу
    type: str
    returned: always
    sample: '/tmp/hello.txt'
changed:
    description: Был ли файл изменен
    type: bool
    returned: always
    sample: true
file_exists:
    description: Существовал ли файл до выполнения
    type: bool
    returned: always
    sample: false
'''

import os
from ansible.module_utils.basic import AnsibleModule
import traceback

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='')
    )
    
    result = dict(
        changed=False,
        path='',
        file_exists=False
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    path = module.params['path']
    content = module.params['content']
    
    result['path'] = path
    
    # Проверяем, существует ли файл
    file_exists = os.path.exists(path)
    result['file_exists'] = file_exists
    
    if file_exists:
        # Читаем текущее содержимое
        try:
            with open(path, 'r', encoding='utf-8') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg=f"Не удалось прочитать файл: {str(e)}", **result)
        
        # Сравниваем содержимое
        if current_content == content:
            # Содержимое одинаковое - ничего не меняем
            module.exit_json(**result)
    
    # Если мы здесь, значит нужно изменить файл
    result['changed'] = True
    
    if module.check_mode:
        # В режиме проверки только сообщаем о намерении
        module.exit_json(**result)
    
    # Реально записываем файл
    try:
        # Создаем директорию, если её нет
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        module.fail_json(msg=f"Не удалось записать файл: {str(e)}", **result)
    
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()