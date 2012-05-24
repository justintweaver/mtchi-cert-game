#!/usr/bin/python

"""Invocation:  scripts/initialize_instance 

Useful for initial configuration of a makahiki instance, and for re-configuration after
pulling changes from the repository.   

Performs the following:
  * Updates and/or installation of any modules in requirements.txt
  * Syncs the database.
  * Migrates the database schemas.
  * Loads the default configuration of data (via scripts/load_data)
  * Reinitializes the test users and sets up test data.
  * Deals with static media locations. 
  
  """

import os


def main():
    """main function."""

    os.system("pip install -r ../requirements.txt")
    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py migrate")
    os.system("python scripts/load_data.py")
    os.system("python manage.py setup_test_data all")
    os.system("python manage.py collectstatic --noinput")
    os.system("cp -r media site_media")
    # if use S3, need to upload the media directory to S3 bucket

if __name__ == '__main__':
    main()
