from locust import HttpLocust, TaskSet, task
from random import random
import base64

PERCENT_SEARCH = 0.9  # Previous study: 0.99

title_num = 0


class Scenario(TaskSet):
    auth = "Basic " + base64.b64encode("testAdmin1:password")

    def get_req(self, url):
        self.client.request(method="GET",
                            url=url,
                            headers={"Authorization": Scenario.auth},
                            verify=False),

    def hud(self):
        Scenario.get_req(self, "/marketplace/api/profile/self/notification")
        Scenario.get_req(self, "/marketplace/api/profile/self/library")
        Scenario.get_req(self, "/marketplace/api/profile/self")

    def center(self):
        Scenario.get_req(self, "/marketplace/api/metadata/")
        Scenario.get_req(self, "/marketplace/api/profile/self")
        Scenario.get_req(self, "/marketplace/api/storefront")
        Scenario.get_req(self, "/marketplace/api/profile/self/notification")
        Scenario.get_req(self, "/marketplace/api/listing/counts")
        Scenario.get_req(self, "/marketplace/api/profile/self/library")

    def search(self):
        Scenario.get_req(self, "/marketplace/api/listing/search?queryString=box*&offset=0")
        # Or "browse by ..."

    def new_listing(self):
        auth = "Basic " + base64.b64encode("testAdmin1:password")

        global title_num
        title_num = title_num + 1

        post_data = '''{"title":<title_num>,"contacts":[],"tags":[],"type":"Web Application","owners":[{"createdDate":"2015-11-06T13:07:51.000+0000","email":"testAdmin1@nowhere.com","bio":"","lastLogin":"2015-11-12T16:46:21.000+0000","highestRole":"ADMIN","launchInWebtop":false,"organizations":[],"stewardedOrganizations":[],"displayName":"Test Admin 1","username":"testAdmin1","id":2,"_links":{"curies":{"href":"http://ozoneplatform.org/docs/rels/{rel}","name":"ozp","templated":true},"ozp:application-library":{"href":"https://ci-latest.amlng.di2e.net:7799/marketplace/api/profile/2/library"},"ozp:user-data":{"href":"https://ci-latest.amlng.di2e.net:7799/marketplace/api/profile/2/data"},"self":{"href":"https://ci-latest.amlng.di2e.net:7799/marketplace/api/profile/2"}}}],"categories":[],"intents":[],"docUrls":[],"changeLogs":[],"screenshots":[]}'''

        post_data = post_data.replace("<title_num>", str(title_num))

        resp = self.client.request(method="POST",
                                   url="/marketplace/api/listing",
                                   headers={"Authorization": auth,
                                            "Content-Type": "application/json"},
                                   verify=False,
                                   data=post_data)
        print resp.status_code
        print resp.text.id
        # Call activity endpoint with listing num (id) after POST

    @task(1)
    def run_scenario(self):
        Scenario.hud(self)
        Scenario.center(self)
        if random() < PERCENT_SEARCH:
            Scenario.search(self)
        else:
            Scenario.new_listing(self)



class WebsiteUser(HttpLocust):
    task_set = Scenario
    min_wait = 1000
    max_wait = 9000
    host = "https://ci-latest.amlng.di2e.net:7799"
