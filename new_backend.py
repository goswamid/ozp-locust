from locust import HttpLocust, TaskSet, task
import base64


class Scenario(TaskSet):
    auth = "Basic " + base64.b64encode("bigbrother:password")

    def get_req(self, url):
        self.client.request(method="GET",
                            url=url,
                            headers={"Authorization": Scenario.auth},
                            verify=False)

    @task(1)
    def hud(self):
        Scenario.get_req(self, "/api/self/notification/")
        Scenario.get_req(self, "/api/self/library/")
        Scenario.get_req(self, "/api/self/profile/")

    @task(1)
    def center(self):
        Scenario.get_req(self, "/api/metadata/")
        Scenario.get_req(self, "/api/self/profile/")
        Scenario.get_req(self, "/api/storefront/")
        Scenario.get_req(self, "/api/self/notification/")
        Scenario.get_req(self, "/api/self/library/")


class WebsiteUser(HttpLocust):
    task_set = Scenario
    min_wait = 1000
    max_wait = 9000
    host = "http://ci-prototype.amlng.di2e.net"
