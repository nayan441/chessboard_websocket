



class HelloWorldUser(HttpUser):

    @task
    def login_post(self):
        for i in user_dict:
            print(i)
            data = {
                "username":i['username'] , 
                "password":"Qwerty@12345" 
            }
            headers = {
                "Content-type": "application/json"
            }
            x=self.client.post("/", json=data, headers=headers)
            print(x.text)