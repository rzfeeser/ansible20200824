#!/usr/bin/python3
"""RZFeeser | Alta3 Research
Ansible Runner is a tool and python library that helps when interfacing with Ansible directly or as part of another system whether that be through a container image interface, as a standalone tool, or as a Python module that can be imported. The goal is to provide a stable and consistent interface abstraction to Ansible.
"""

# python3 -m pip install ansible_runner
import ansible_runner

# run() takes inputs (either provided as direct inputs to the function or from the Runner Input Directory Hierarchy), and executes Ansible
# returns runner object
r = ansible_runner.run(private_data_dir='/home/student/ans/', playbook='playbook-copy.yml')

# explore some of the returned data
print("playbook run breakdown")

#Status: successful
#RunCode: 0
print(f"Status: {r.status}\nRunCode: {r.rc}")


for each_host_event in r.events:
    print(each_host_event) # print out the dictionary of events
                           # includes data such as
                           # name of the playbook
                           # json returned by the task

print("Exit Stats")
print(r.stats) # breakdown of how the playbook ran

