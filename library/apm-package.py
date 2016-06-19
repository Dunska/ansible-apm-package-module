#!/usr/bin/python

import subprocess
import json

from ansible.module_utils.basic import *

def tryInstall(name, upgrade):

    apmList = subprocess.check_output(['apm', 'list', '--bare', '--installed',]).strip().split('\n')

    for line in apmList:
        if line:
            if line.split('@')[0] == name:
                if upgrade:
                    return tryUpgrade(name)
                else: return False

    return install(name);

def install(name):
    subprocess.check_output(['apm', 'install', name,])
    return True

def tryUpgrade(name):
    result = subprocess.check_output(['apm', 'upgrade', '--list', '--json', name,])
    if json.loads(result):
        return upgrade(name)
    else: return False

def upgrade(name):
    subprocess.check_output(['apm', 'upgrade', '--no-confirm', name,])
    return True

def main():

    fields = {
        "name": {"required": True, "type":"str"},
        "upgrade": {"default": False, "type":"bool"}
    }

    module = AnsibleModule(argument_spec=fields)
    result = tryInstall(module.params['name'], module.params['upgrade'])
    module.exit_json(changed=result)

if __name__ == '__main__':
    main()
