#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: issriders.py

short_description: This is my test module

version_added: "2.9"

description:
    - "This is my longer description explaining my test module"

options:
    path:
        description:
            - This is path to save out the astros last names to. If no path is supplied, then no file is produced. File is always saved YYYY-MO-DDissriders.txt
        required: false

author:
    - RZFeeser (@rzfeeser)
'''

EXAMPLES = '''
# Grab last names of riders on http://api.open-notify.org/astros.json
- name: Pull in last names save to tmp
  issriders:
    path: /tmp/

# Grab last names of riders on http://api.open-notify.org/astros.json
- name: Pull in last names and register
  issriders:
  register: results

- name: Show the results
  debug:
      var: results

# easter egg - force a failure
- name: force the module to fail
  issrider:
    path: fail me
'''

RETURN = '''
fulljson:
    description: entire json avail on  http://api.open-notify.org/astros.json. None if operation fails.
    returned: always
lastnames:
    description: list of last names. None if operation fails.
    type: list
    returned: always
statuscode:
    description: HTTP status code of operation
    type: int
    returned: always
'''
import requests
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        fulljson='',
        lastnames='',
        statuscode=0
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    astros = requests.get("http://api.open-notify.org/astros.json")

    result['statuscode'] = astros.status_code

    if astros.status_code != 200:
        module.fail_json(msg=f'Huston, we have a problem! Status code returned by the lookup was {astros.status_code}', **result)

    result['fulljson'] = astros.json()

    lastnamelist = []
    for astro in astros.json()["people"]:
        lastnamelist.append(astro['name'].split()[-1])

    result['lastnames'] = lastnamelist

    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['path'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    if module.params['path']:
        with open(f"{module.params['path']}YYYY-MM-DDissriders.txt", "w") as af:
            for ln in lastnamelist:
                af.write(f"{ln}\n")

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
