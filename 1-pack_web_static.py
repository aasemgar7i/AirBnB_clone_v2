#!/usr/bin/python3

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if the archive has been correctly generated,
        otherwise None.
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the timestamp for the archive name
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the archive using tar command
        archive_name = "web_static_{}.tgz".format(timestamp)
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path if generated successfully
        return "versions/{}".format(archive_name)
    except Exception as e:
        print("Error packing files: {}".format(e))
        return None
