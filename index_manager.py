from globus.auth import get_authorizer
import globus_sdk
import requests
import json


def get_input(prompt):
    try:
        s = input(prompt)
    except KeyboardInterrupt:
        print()
        exit(0)
    return s

def announcement(message):
    annoucement_width = 80
    pound_signs = (annoucement_width - len(message) - 2) // 2
    s = pound_signs * '#' + ' ' + message + ' ' + pound_signs * '#'
    if len(s) < annoucement_width:
        s += '#'
    print(s)

def get_indices(authorizer):
    url = 'https://search.api.globus.org/v1/index_list'
    headers = {
        'Authorization': authorizer.get_authorization_header()
    }
    r = requests.get(url, headers=headers)
    indices = []
    for index in r.json()['index_list']:
        indices.append(index)
    return indices

def print_index(d):
    if d['status'] == 'delete-pending':
        print('PENDING DELETION')
    print(f"id: {d['id']}")
    print(f"name: {d['display_name']}")
    print(f"subjects: {d['num_subjects']}")

def get_choice(prompt, num_choices):
    while True:
        try:
            choice = int(get_input(prompt))
            if choice < 0 or choice >= num_choices:
                print('Please enter a valid integer.')
            else:
                break
        except ValueError:
            print('Please enter an integer.')
    return choice

def create_index(sc, name, description):
    try:
        r = sc.create_index(name, description)
        return json.loads(str(r))
    except Exception as e:
        print('Error while creating index: ' + str(e))
        exit(1)

def new_index_activity(sc):
    name = get_input('Enter a name for the new index: ')
    description = get_input('Enter a description for the new index: ')
    new_index = create_index(sc, name, description)
    announcement('New index details')
    print(json.dumps(new_index, indent=4))

def do_command_activity(index, index_data, sc):
    cmds = ['info', 'clear', 'delete']
    prompt = 'Select a command: ' + ', '.join([f'{i}:{cmd}' for i, cmd in enumerate(cmds)])
    choice = get_choice(prompt, len(cmds))
    cmd = cmds[choice]
    if cmd == 'info':
        print(json.dumps(index_data, indent=4))
    elif cmd == 'clear':
        announcement(f'Clear index {index}?')
        prompt = f'Are you sure you want to clear this index? (y/n): '
        yn = get_input(prompt)
        if yn.lower() != 'y':
            print('Aborting.')
        else:
            sc.delete_by_query(index_data['id'], { 'q': '*' })
            print(f"Deleted all {index_data['num_subjects']} subjects from index.")
    elif cmd == 'delete':
        # confirm deletion
        announcement(f'Delete index {index}?')
        print_index(index_data)
        prompt = f'Are you sure you want to delete this index? (y/n): '
        yn = get_input(prompt)
        if yn.lower() != 'y':
            print('Aborting.')
        else:
            sc.delete_index(index_data['id'])
            print('Index marked for deletion.')

if __name__ == '__main__':
    authorizer = get_authorizer('urn:globus:auth:scope:search.api.globus.org:all')    
    search_client = globus_sdk.SearchClient(authorizer=authorizer)
    indices = get_indices(authorizer)
    # if no indices, create one and exit
    if len(indices) == 0:
        prompt =  f'No indices found. Create new index? (y/n): '
        yn = get_input(prompt)
        if yn.lower() == 'y':
            new_index_activity(search_client)
            exit(0)
    # print details for each index
    for i, index_data in enumerate(indices, start=1):
        announcement(f'Index {i}')
        print_index(index_data)
    # choose index or create new one
    announcement('How to proceed?')
    if len(indices) > 1:
        choice = get_choice('Enter 0 to create a new index, or select an index to examine: ', len(indices)+1)
    else: # only one index
        choice = get_choice('Create new index (enter 0), or examine index 1 (enter 1): ', 2)
    if choice == 0:
        new_index_activity(search_client)
        exit(0)
    else:
        index = choice
    # perform action on index
    announcement(f'Selected index {index}')
    do_command_activity(index, indices[index-1], search_client)