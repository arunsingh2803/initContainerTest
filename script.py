import sys
import time
import requests


def check_for_go_ahead(version, appname):
    url = "http://127.0.0.1:5000/go_ahead"
    querystring = {"appname": appname, "version": version}
    response = requests.request("GET", url, params=querystring)
    return response.text


def run_db_schema_change(deploying_version, app):
    print("Running DB schema change for app {0} and DB schema version {1}".format(app, deploying_version))
    time.sleep(10) # Replace this with actual DB schema change job
    job_status = "Success" # change to Failed if job_status fails
    unlock_deployment(app, job_status, deploying_version)
    return job_status


def unlock_deployment(appname, job_status, deploying_version):
    url = "http://127.0.0.1:5000/unlock_depl"
    querystring = {"appname": appname, "job_status": job_status, "deploying_version": deploying_version}
    response = requests.request("GET", url, params=querystring)
    return response.text


def analyse_decision(decision, deploying_version, app):
    if decision == "wait":
        sleep_time = 10
        while sleep_time < 300:
            print("Waiting for goahead from controller, sleeping for 10 sec")
            time.sleep(sleep_time)
            decision = check_for_go_ahead(deploying_version, app)
            if decision != "wait":
                break
            sleep_time += 10
        else:
            print("Wait time exceeded")
            sys.exit(1)
    elif decision == "run":
        status = run_db_schema_change(deploying_version, app)
        print("DB schema change job finished with status: {0}".format(status))
    elif decision == "noneed":
        print("No need to run DB Schema changes")


if __name__ == "__main__":
    deploying_version = sys.argv[1]
    app = sys.argv[2]
    decision = check_for_go_ahead(deploying_version, app)
    analyse_decision(decision, deploying_version, app)
