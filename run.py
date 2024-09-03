from foodfinder.__init__ import create_app

if __name__ == "__main__":
    #debug=True: to be able to make/see html changes in real time
    app, db = create_app()
    app.run(debug=True)

