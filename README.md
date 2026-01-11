# my_own_namespace.yandex_cloud_elk Collection

Custom Ansible collection for file management.

## Installation

```bash
ansible-galaxy collection install my_own_namespace.yandex_cloud_elk

Modules
my_own_module

Creates or updates text files with specified content.

Parameters:

    path (required): Path to the file

    content (optional): File content, defaults to empty string

Example:
yaml

- name: Create configuration file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: "/etc/app/config.txt"
    content: |
      setting1=value1
      setting2=value2

Roles
create_file_role

Role that creates files using my_own_module.

Default variables:

    file_path: /tmp/default_created_file.txt

    file_content: Default content with timestamp

Usage:
yaml

- hosts: servers
  collections:
    - my_own_namespace.yandex_cloud_elk
  roles:
    - create_file_role
  vars:
    file_path: "/opt/myapp/config.cfg"
    file_content: "custom configuration"

