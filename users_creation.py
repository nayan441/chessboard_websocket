def populate(N=5):
    with open("users.json",'a', encoding = 'utf-8') as f:
        for entry in range(N):
            fakename = fakegen.name()
            username = fakename.replace(" ","")
            fake_name= fakename.split()
            fake_first_name = fake_name[0]
            fake_last_name = fake_name[1]
            fake_email= fakegen.email()
            f.write("{'username':'%s', 'password':'Qwerty@12345', 'email':%s},\n"% (username,fake_email))
            print(fakename, fake_email)
            try:
                user = User.objects.get_or_create(username= username, first_name = fake_last_name,
                                last_name= fake_last_name,email = fake_email, password="Qwerty@12345")[0]
            except:
                pass

if __name__ == '__main__':
    print('populating databases......................')
    populate(2)
    print('populated')