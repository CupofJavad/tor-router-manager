# ssh_utils.py — v1.1.0
# SSH connection and SFTP file transfer utilities using paramiko.

import paramiko

def make_client(cfg):
    host = cfg["router"]["host"]
    user = cfg["router"]["user"]
    password = cfg["router"].get("password")
    key_path = cfg["router"].get("key_path")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if key_path:
        pkey = paramiko.RSAKey.from_private_key_file(key_path)
        client.connect(host, username=user, pkey=pkey, timeout=15)
    else:
        client.connect(host, username=user, password=password, timeout=15)

    return client

def run(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode("utf-8", "ignore").strip()
    err = stderr.read().decode("utf-8", "ignore").strip()
    rc = stdout.channel.recv_exit_status()
    return rc, out, err

def sftp_put(client, local_path, remote_path, chmod_700=True):
    sftp = client.open_sftp()
    sftp.put(local_path, remote_path)
    if chmod_700:
        sftp.chmod(remote_path, 0o700)
    sftp.close()