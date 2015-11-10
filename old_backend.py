from locust import HttpLocust, TaskSet, task
import base64


class Scenario(TaskSet):
    auth = "Basic " + base64.b64encode("testAdmin1:password")

    def get_req(self, url):
        self.client.request(method="GET",
                            url=url,
                            headers={"Authorization": Scenario.auth},
                            verify=False)

    @task(1)
    def hud(self):
        Scenario.get_req(self, "/marketplace/api/profile/self/notification")
        Scenario.get_req(self, "/marketplace/api/profile/self/library")
        Scenario.get_req(self, "/marketplace/api/profile/self")

    @task(1)
    def center(self):
        Scenario.get_req(self, "/marketplace/api/metadata/")
        Scenario.get_req(self, "/marketplace/api/profile/self")
        Scenario.get_req(self, "/marketplace/api/storefront")
        Scenario.get_req(self, "/marketplace/api/profile/self/notification")
        Scenario.get_req(self, "/marketplace/api/listing/counts")
        Scenario.get_req(self, "/marketplace/api/profile/self/library")


class WebsiteUser(HttpLocust):
    task_set = Scenario
    min_wait = 1000
    max_wait = 9000
    host = "https://ci-latest.amlng.di2e.net:7799"
