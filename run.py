from app import create_app, db

app = create_app()

# Create tables before first request
@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    from app import socketio
    socketio.run(app, debug=True, port=5000)
