from src.app import create_app
# Python


app = create_app()
if __name__ == '__main__':

    app.run(debug=True)