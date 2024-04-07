#!/usr/bin/python3

from fabric.api import env, put, run
from os.path import exists

env.hosts = ["100.26.238.68", "100.25.190.136"]
env.user = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBuV58INl1/xumSehLJL5XyNwSa8Co55099MC9dS5ZeVCy1ylM1CDEZqBwM99F1svd0ZxuEn1ScdrjxmGMu7QzSqb44OCyoN9ZrBhk621UNTx4X862m/dk8oF+BQczWl8izYfVAXeezuHgZ20EmrtcHcSGFWTi5Pt8GNdDN1eN67ME0w9iA4tK7fRSF4IBDwiuYVPUDSFXSq6eSn0S4mJ2xaYFDpvM4gZPt1CBYI82S+YH+L5j28/w8UstCE60VxvN09CT+HGGxuAzl7RGDJxCB8i/wdg61udZYMLaIDQRXEnSiIALGMqdw3dr2xiCSLmFJiFs0Yzbv6PQUl9d4MNysQVfj3gPi00P6p7wUpLeOXY0f5cukia44H5coc0jRC1FujvSnc7pU36p1z33NQvJua0scGXg8PpdFdf6uFUE6Z6fYwsJzEXNiQOTTmnPVZtX0syGH/vJRx7l0IG66DHR4YzD903dIS5FlVvuVzgiW62PhCLc08pm/9gE/j9h7G0= root@ALX-Students'  # Replace 'your_ssh_username' with your actual SSH username

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

