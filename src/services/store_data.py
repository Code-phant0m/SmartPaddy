from google.cloud import firestore

async def store_user_data(user):
    db = firestore.Client()
    
    user_collection = db.collection('users')
    
    await user_collection.document(user['email']).set(user)


async def store_prediction_data(predictIds, predictData):
    db = firestore.Client()

    predict_collection = db.collection('predictions')

    await predict_collection.document(predictIds).set(predictData)