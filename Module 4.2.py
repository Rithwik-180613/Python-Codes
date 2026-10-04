import requests
url= "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

def get_random_fact():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Did you know? {data['text']}")
    else:
        print("Failed to retrieve a fact.")

while True:
    user_input = input("\nPress Enter to get another fact or type 'exit' to quit.")
    if user_input.lower() == 'exit':
        break   
    get_random_fact()