import sys
from google.cloud import storage


storage_client = storage.Client("<GCP_PROJECT_ID>")
bucket = storage_client.get_bucket("<BUCKET_NAME>")
blob = bucket.blob("running_version.txt")
blob.download_to_filename("running_version.txt")

with open('running_version.txt', 'r') as file:
    running_version = file.read().replace('\n', '')

deploying_version = sys.argv[1]

if running_version < deploying_version:
    print("Run DB Scahema changes")
else:
    print("No need to run DB Schema changes")

with open('running_version.txt', "w") as file:
    file.write(deploying_version)
blob.upload_from_filename("running_version.txt")
