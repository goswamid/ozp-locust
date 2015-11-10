from locust import HttpLocust, TaskSet, task
import base64


class OldBackend(TaskSet):

    @task(1)
    def listing(self):
        auth = "Basic " + base64.b64encode("testAdmin1:password")
        self.client.request(method="GET",
                            url="/marketplace/api/profile/self/listing",
                            headers={"Authorization": auth},
                            verify=False)

    @task(2)
    def storefront(self):
        auth = "Basic " + base64.b64encode("testAdmin1:password")
        self.client.request(method="GET",
                            url="/marketplace/api/storefront",
                            headers={"Authorization": auth},
                            verify=False)


class NewBackend(TaskSet):

    @task(1)
    def listing(self):
        auth = "Basic " + base64.b64encode("bigbrother:password")
        self.client.request(method="GET",
                            url="/api/self/listing/",
                            headers={"Authorization": auth},
                            verify=False)

    @task(1)
    def storefront(self):
        auth = "Basic " + base64.b64encode("bigbrother:password")
        self.client.request(method="GET",
                            url="/api/storefront/",
                            headers={"Authorization": auth},
                            verify=False)


title_num = 0


class NbScenario(TaskSet):

    @task
    def storefront(self):
        auth = "Basic " + base64.b64encode("bigbrother:password")
        self.client.request(method="GET",
                            url="/api/storefront/",
                            headers={"Authorization": auth},
                            verify=False)

        self.client.request(method="GET",
                            url="/api/self/library/",
                            headers={"Authorization": auth},
                            verify=False)


    @task
    class SubScenario(TaskSet):

        @task(1)
        def create_new_listing(self):
            auth = "Basic " + base64.b64encode("bigbrother:password")

            global title_num
            title_num = title_num + 1

            post_data = '''{"title":<title_num>,"screenshots":[],"contacts":[],"tags":[],"owners":[{"display_name":"Winston Smith","id":1,"user":{"username":"wsmith"}}],"agency":{},"categories":[],"intents":[],"doc_urls":[],"listing_type":{"title":"web application"},"last_activity":{"action":"APPROVED"},"is_private":false,"required_listings":null,"access_control":{"title":"UNCLASSIFIED"}}'''

            post_data = post_data.replace("<title_num>", str(title_num))

            self.client.request(method="POST",
                                url="/api/listing/",
                                headers={"Authorization": auth,
                                         "Content-Type": "application/json"},
                                verify=False,
                                data=post_data)
            self.interrupt()

        @task(1)
        def search(self):
            auth = "Basic " + base64.b64encode("bigbrother:password")
            self.client.request(method="GET",
                                url="/api/listings/search/?search=air&offset=0&limit=24",
                                headers={"Authorization": auth},
                                verify=False)
            self.interrupt()


class WebsiteUser(HttpLocust):
    #task_set = NbScenario
    #task_set = NewBackend
    task_set = OldBackend
    min_wait = 1000
    max_wait = 9000
    #host = "http://ci-prototype.amlng.di2e.net"
    #host = "http://localhost:8181"
    host = "https://ci-latest.amlng.di2e.net:7799"

# locust --host=https://ci-latest.amlng.di2e.net:7799
# locust --host=http://ci-prototype.amlng.di2e.net
