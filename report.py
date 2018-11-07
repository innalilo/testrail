# Test Raile report for users - how many tsts they worked on

from base64 import b64encode
from datetime import datetime
from json import loads
from time import gmtime, mktime, strftime, time
from urllib2 import urlopen, URLError

from pprint import pprint

from testrail import APIClient, APIError


def main():
    server = "http://SERVER.COM"
    login = "USERNAME"
    password = "PASSWORD"

    START_DATE = "01/08/2018"
    END_DATE = "31/08/2018"

    TESTERS = ['USER1EMAIL', 'USER2EMAIL']

    start_date = mktime(datetime.strptime(START_DATE, "%d/%m/%Y").timetuple())
    end_date = mktime(datetime.strptime(END_DATE, "%d/%m/%Y").timetuple())

    client = APIClient(server)
    client.user = login
    client.password = password

    print "Getting testers... "
    testers = {}
    for tester_email in TESTERS:
        try:
            tester = client.send_get('get_user_by_email&email={}'.format(tester_email))
            testers.update({
                tester["id"]: {
                    'email': tester_email,
                    'created': 0,
                    'updated': 0
                }
            })
        except APIError:
            print "Tester's email is not valid", tester_email

    projects = client.send_get('get_projects/')
    for project in projects:
        print "=" * 80
        print "PROJECT", project["id"]

        project_id = project["id"]
        project_suites = client.send_get('get_suites/{}'.format(project_id))

        for suite in project_suites:
            print "-" * 80
            print "SUITE", suite["id"]

            suite_id = suite["id"]

            created = client.send_get(
                'get_cases/{0}&suite_id={1}&created_after={2}&created_before={3}'.format(
                    project_id, suite_id, int(start_date), int(end_date)))

            updated = client.send_get(
                'get_cases/{0}&suite_id={1}&updated_after={2}&updated_before={3}'.format(
                    project_id, suite_id, int(start_date), int(end_date)))

            for c in created:
                tid = c['created_by']
                if tid in testers:
                    testers[tid]['created'] += 1
                # import pdb; pdb.set_trace()

            for c in updated:
                tid = c['updated_by']
                if tid in testers:
                    testers[tid]['updated'] += 1

    # ------------------------------------------------------------------------

    print "=" * 80
    pprint(testers)


if __name__ == "__main__":
    main()
