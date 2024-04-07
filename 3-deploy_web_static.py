#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers,
using the function deploy.
"""

from fabric.api import env, run
from datetime import datetime
from os.path import exists
from fabric.operations import local
from fabric.api import put

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if the archive has been correctly generated, otherwise None.
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the timestamp for the archive name
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the archive using tar command
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_name))

        # Return the archive path if generated successfully
        return archive_name
    except Exception as e:
        print("Error packing files: {}".format(e))
        return None


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


def deploy():
    """Deploys the web_static content to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
