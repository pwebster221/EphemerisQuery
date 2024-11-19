# app.py
from webhook_receiver import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000)