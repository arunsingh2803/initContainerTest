import os
import sys
from google.cloud import storage
import time


def download_file_from_gcs():
    storage_client = storage.Client("dc-hughes-poc-gke")
    bucket = storage_client.get_bucket("version_check_bucket_echostar")
    blob = bucket.blob("running_version.txt")
    blob.download_to_filename("running_version.txt")


def upload_file_to_gcs():
    storage_client = storage.Client("dc-hughes-poc-gke")
    bucket = storage_client.get_bucket("version_check_bucket_echostar")
    blob = bucket.blob("running_version.txt")
    blob.upload_from_filename("running_version.txt")


def create_pid_file():
    with open('check_version.pid', 'w') as fp:
        pass


def delete_pid_file():
    os.remove("check_version.pid")


def check_version_run_schema_change(version):
    create_pid_file()
    download_file_from_gcs()
    with open('running_version.txt', 'r') as file:
        running_version = file.read().replace('\n', '')

    if running_version < version:
        print("Run DB Scahema changes")
    else:
        print("No need to run DB Schema changes")

    with open('running_version.txt', "w") as file:
        file.write(deploying_version)

    upload_file_to_gcs()
    delete_pid_file()


def main(depl_version):
    path_to_file = "check_version.pid"
    if os.path.exists(path_to_file):
        sleep_time = 10
        while sleep_time < 40:
            print("Waiting for other initContainer request to complete, sleeping for 10 sec")
            time.sleep(sleep_time)
            sleep_time += 10
        else:
            print("Wait time exceeded")
            sys.exit(1)
    else:
        check_version_run_schema_change(depl_version)


if __name__ == "__main__":
    deploying_version = sys.argv[1]
    main(deploying_version)
