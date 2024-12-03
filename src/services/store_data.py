from google.cloud import firestore

async def store_user_data(user):
    db = firestore.Client()
    
    user_collection = db.collection('users')
    
    await user_collection.document(user['email']).set(user)


async def store_prediction_data(id, data):
    db = firestore.AsyncClient()

    predict_collection = db.collection('predictions')

    await predict_collection.document(id).set(data)