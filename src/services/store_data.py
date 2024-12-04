from google.cloud import firestore

def store_user_data(user):
    db = firestore.Client()
    
    user_collection = db.collection('users')
    
    user_collection.document(user['email']).set(user)


def store_prediction_data(predict_id, predict_data):
    db = firestore.Client()

    predict_collection = db.collection('predictions')

    predict_collection.document(predict_id).set(predict_data)


def get_prediction_data(predict_id):
    db = firestore.Client()
    doc_ref = db.collection('predictions').document(predict_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None