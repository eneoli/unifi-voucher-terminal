from app import App

# Config

ENDPOINT_URL = "https://eneoli.de/demo.php"
API_TOKEN = "TEST"
TERMINAL_ID = "Demo-Terminal 01"
TERMINAL_LOCATION = "Demoroom"
BUTTON_PIN = 20

if __name__ == '__main__':
    app = App(ENDPOINT_URL, API_TOKEN, TERMINAL_ID, TERMINAL_LOCATION, BUTTON_PIN)
    app.run()
