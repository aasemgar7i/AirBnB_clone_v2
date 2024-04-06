#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy.
"""

from fabric.api import env, put, run
from os.path import exists
from os import makedirs
from datetime import datetime

env.hosts = ['<100.26.238.68>', '<100.25.190.136>']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): The path to the archive to be distributed.

    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the folder /data/web_static/releases/<archive_no_ext>
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_no_ext))

        # Uncompress the archive to the folder
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_no_ext))

        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False


if __name__ == "__main__":
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    print(do_deploy(archive_path))
