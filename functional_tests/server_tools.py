from fabric import Connection

c = Connection(host='localhost', user='krutsch', connect_kwargs={'key_filename': '/home/krutsch/.ssh/id_rsa'})

def _get_manage_py(host: str) -> str:
    return f'/home/krutsch/sites/{host}/virtualenv/bin/python /home/krutsch/sites/{host}/source/manage.py'

def reset_database() -> None:
    manage_py = _get_manage_py(host=c.host)
    c.run(f'{manage_py} flush --noinput')

def create_session_on_server(email: str) -> None:
    manage_py = _get_manage_py(host=c.host)
    session_key = c.run(f'{manage_py} create_session {email}')
    return session_key.stdout.strip()