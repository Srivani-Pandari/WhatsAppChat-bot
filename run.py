import app from app

from flask import session

if __name__ == "__main__":
    app.run(debug=True)
    print('---')
    
    if session.get('status_index'):
        session.pop('status_index')
    if session.get('date'):
        session.pop('date')
    if session.get('orderPosition'):
        session.pop('orderPosition')

    print(session.get('status_index'))

