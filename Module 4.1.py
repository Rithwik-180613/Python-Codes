import requests

def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.status_code == 200:
        joke_data = response.json()
        print(f"Type: {joke_data['type']}\nJoke: {joke_data['setup']} - {joke_data['punchline']}")
    else:
        print(f"Failed to retrieve joke. Status code: {response.status_code}")

def main():
    while True:
        user_input = input("Press Enter to get a random joke or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        get_random_joke()
if __name__ == "__main__":
    main()
      