from app import create_app

app = create_app(mode='development')

if __name__ == '__main__':
    app.run(debug=True)