from Website import create_app

app = create_app()

with app.app_context():
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)