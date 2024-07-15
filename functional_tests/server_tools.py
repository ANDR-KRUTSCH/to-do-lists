from fabric import Connection

def _get_manage_py(host: str) -> str:
    return f'/home/krutsch/sites/{host}/virtualenv/bin/python /home/krutsch/sites/{host}/source/manage.py'

def reset_database(host: str) -> None:
    c = Connection(host=host, user='krutsch', connect_kwargs={'key_filename': '/home/krutsch/.ssh/id_rsa'})
    if c.host == 'localhost':
        host = 'www.staging.to-do-lists.com'
    manage_py = _get_manage_py(host=host)
    c.run(f'{manage_py} flush --noinput')
    c.close()

def create_session_on_server(host: str, email: str) -> str:
    c = Connection(host=host, user='krutsch', connect_kwargs={'key_filename': '/home/krutsch/.ssh/id_rsa'})
    if c.host == 'localhost':
        host = 'www.staging.to-do-lists.com'
    manage_py = _get_manage_py(host=host)
    session_key = c.run(f'{manage_py} create_session {email}')
    return session_key.stdout.strip()