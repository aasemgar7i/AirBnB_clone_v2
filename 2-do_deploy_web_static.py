#!/usr/bin/python3

from fabric.api import env, put, run
from os.path import exists

env.hosts = ["100.26.238.68", "100.25.190.136"]
env.user = 'ssh'  # Replace 'your_ssh_username' with your actual SSH username

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path: Path to the archive file to be deployed.

    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not exists(archive_path):
        print("Archive file does not exist.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp')

        # Extract the archive to the /data/web_static/releases/ folder
        archive_filename = archive_path.split('/')[-1]
        archive_name_no_ext = archive_filename.split('.')[0]
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename, archive_name_no_ext))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of your code
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_name_no_ext))

        print("Deployment successful.")
        return True
    except Exception as e:
        print("Error deploying archive: {}".format(e))
        return False

