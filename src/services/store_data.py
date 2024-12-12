from google.cloud import firestore

db = firestore.Client()
USER_COLLECTION = "users"
PREDICTION_COLLECTION = "predictions"

def store_user_data(user):
    try:
        db.collection(USER_COLLECTION).document(user['email'].lower()).set(user)
    except Exception as e:
        print(f"Error storing user data: {e}")

def fetch_user_by_email(email):
    try:
        user_doc = db.collection(USER_COLLECTION).document(email).get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

def store_prediction_data(predict_id, data):
    try:
        db.collection(PREDICTION_COLLECTION).document(predict_id).set(data)
    except Exception as e:
        print(f"Error storing prediction data: {e}")
        raise ValueError("Failed to store prediction data.") from e

def get_prediction_data(predict_id):
    try:
        doc = db.collection(PREDICTION_COLLECTION).document(predict_id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Error fetching prediction data: {e}")
        return None
