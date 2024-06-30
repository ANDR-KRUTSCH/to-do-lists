import random
from fabric import Connection

c = Connection(host='localhost', user='krutsch', connect_kwargs={'key_filename': '/home/krutsch/.ssh/id_rsa'})

REPO_URL = 'https://github.com/ANDR-KRUTSCH/to-do-lists.git'

def _create_directory_structure_if_necessary(site_folder: str) -> None:
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder: str) -> None:
    result = c.run(f'ls -a -m {source_folder}')
    if '.git' in result.stdout:
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone {REPO_URL} {source_folder}')
    current_commit = c.run(f'cd {source_folder} && git log -n 1 --format=%H')
    c.run(f'cd {source_folder} && git reset --hard {current_commit.stdout}')

def _update_settings(source_folder: str) -> None:
    settings_path = source_folder + '/superlists/settings.py'
    c.get(remote=f'{settings_path}', local=f'/home/{c.user}/Desktop/superlists/superlists/deploy_tools/')
    with open(file='/home/krutsch/Desktop/superlists/superlists/deploy_tools/settings.py') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if 'DEBUG = ' in lines[i]:
                lines[i] = 'DEBUG = False\n'
            elif 'ALLOWED_HOSTS = ' in lines[i]:
                lines[i] = f'ALLOWED_HOSTS = [\'{c.host}\']\n'
            elif 'SECRET_KEY = ' in lines[i]:
                lines[i] = 'from .secret_key import SECRET_KEY\n'
    secret_key_file = source_folder + '/superlists'
    result = c.run(f'ls -a -m {secret_key_file}')
    if 'secret_key.py' not in result.stdout:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        c.run(f'echo \'SECRET_KEY = "{key}"\' > {secret_key_file}/secret_key.py')
    with open(file='/home/krutsch/Desktop/superlists/settings.py', mode='w') as file:
        file.writelines(lines)
    c.run(f'cd {source_folder}/superlists && rm settings.py')
    c.put(local=f'/home/{c.user}/Desktop/superlists/settings.py', remote=f'{source_folder}/superlists/')

def _update_virtualenv(source_folder: str) -> None:
    result = c.run(f'ls -a -m {source_folder}/../virtualenv')
    if 'bin' not in result.stdout:
        c.run(f'cd {source_folder}/../ && python3 -m venv virtualenv')
    c.run(f'{source_folder}/../virtualenv/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder: str) -> None:
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database(source_folder: str) -> None:
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')

def deploy() -> None:
    if c.host == 'localhost':
        host = 'www.staging.to-do-lists.com'
    else:
        host = 'www.live.to-do-lists.com'

    site_folder = f'/home/{c.user}/sites/{host}'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

deploy()