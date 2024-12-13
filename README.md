# SmartPaddy API Documentation

## Overview

The SmartPaddy API provides endpoints to manage user authentication, perform image-based predictions, and retrieve historical user data. This guide outlines the available routes, their expected inputs, and outputs.

## How to Run

### Prerequisites

1. Ensure you have Python installed (version 3.8 or later).
2. Install `pip` (Python package manager).
3. Clone this repository to your local machine.
4. Set up a virtual environment for dependency management (recommended).

### Steps to Run

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:

   - Create a `.env` file in the root directory.
   - Add the necessary environment variables such as:
     ```env
     MODEL_URL=your_secret_key
     ```

5. **Run the Flask Application**:

   ```bash
   python run.py
   ```

6. **Access the API**:
   Open your browser or API client (e.g., Postman) and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Deploy API With GitHub Repository In Cloud Run

### Step 1: Fork the Repository
**Fork the Repository**:
   - Go to the original GitHub repository containing the API code.
   - Click the **Fork** button to create a copy of the repository in your GitHub account.
     
---

### Step 2: Set Up Google Cloud Run

1. **Go to Google Cloud Console**:
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/).

2. **Enable Cloud Run**:
   - Ensure the **Cloud Run API** is enabled for your project. If not, enable it by searching for "Cloud Run" in the **APIs & Services** section.

3. **Create a New Cloud Run Service**:
   - In the **Cloud Run** section, click on **Create Service**.

4. **Select Deployment Source**:
   - Choose **Deploy from Source Repository**.
   - Click **Set up with Cloud Build** if prompted.

---

### Step 3: Link Your GitHub Repository

1. **Connect Your GitHub Account**:
   - During setup, authorize Google Cloud to access your GitHub account.

2. **Select Your Repository**:
   - Select the forked repository from your GitHub account from the list of repositories.

3. **Pick the Branch**:
   - Choose the branch you want to deploy (e.g.,`cc-main`).

---

### Step 4: Configure Build and Deployment

1. **Set Build Options**:
   - Ensure your repository contains a `Dockerfile` configuration file. Google Cloud will automatically detect these files.

2. **Specify Runtime Settings**:
   - Configure settings such as the service name, region, and secret variable.
   - Adjust CPU allocation and memory limits based on the API requirements.

3. **Enable Continuous Deployment**:
   - Check the option for **Continuous Deployment** to automatically redeploy the service whenever new changes are pushed to the selected branch.

---

### Step 5: Deploy the API

1. **Review and Deploy**:
   - Review your configuration and click **Deploy**.
   - Google Cloud Run will build the container from your GitHub repository, deploy it, and provide you with a public URL.

2. **Monitor Deployment**:
   - Use the **Cloud Build** section in Google Cloud Console to monitor the build and deployment process.

---

### Step 6: Test the Deployed API
**Access the API**:
   - Copy the URL provided by Cloud Run and use it to test the API.
   - Use tools like **Postman** or `curl` to verify the endpoints.

---

## Endpoints

### 1. **User Registration**

**Route:** `/register`  
**Method:** `POST`

**Description:**  
Registers a new user. The `regis_user_handler` function processes the request.

#### Expected Input:

- **Name**: A name of User.
- **Email**: A email number of User.
- **Password**: A password for User

#### Expected Outputs:

1. **Case 1: Successful Register**  
   **HTTP Status Code:** 200

```json
{
  "message": "String",
  "status": "success",
  "user": {
    "email": "String",
    "name": "String",
    "token": "String"
  }
}
```

2. **Case 2: Email already registered**  
   **HTTP Status Code:** 400

```json
{
  "message": "Email sudah terdaftar",
  "status": "fail"
}
```

3. **Case 3: No data input**  
   **HTTP Status Code:** 400

```json
{
  "message": "Mohon isi seluruh data",
  "status": "fail"
}
```

---

### 2. **User Login**

**Route:** `/login`  
**Method:** `POST`

**Description:**  
Authenticates an existing user. The `login_user_handler` function processes the request.

#### Expected Input:

- **Email**: An email for authentication.
- **Password**: A password for authentication.

#### Expected Outputs:

1. **Case 1: Successful Login**  
   **HTTP Status Code:** 200

```json
{
  "message": "String",
  "email": "String",
  "name": "String",
  "status": "success",
  "token": "String"
}
```

2. **Case 2: Wrong email or wrong password**  
   **HTTP Status Code:** 401

```json
{
  "message": "email atau password salah",
  "status": "fail"
}
```

3. **Case 3: No data input or No email or No password**  
   **HTTP Status Code:** 400

```json
{
  "message": "Mohon isi email dan password",
  "status": "fail"
}
```

---

### 3. **Scan Paddy Image**

**Route:** `/scan`  
**Method:** `POST`

**Description:**  
Processes an image of paddy plants to make predictions.

#### Expected Input:

- **imageUri**: A `.png` or `.jpg` file.
- **userIds**: A string used for authentication.
- **imagePath**: A string used for saving the image path.

#### Expected Outputs:

1. **Case 1: Successful Prediction**  
   **HTTP Status Code:** 200

```json
{
    "data": {
        "created_at": DATE,
        "image_url": "String",
        "predict_id": "String",
        "result": {
            "c_menangani": "String",
            "gejala": "String",
            "penjelasan": "String",
            "predicted_class": "String",
            "predicted_prob": Float
        },
        "user_id": "String"
    },
    "status": "success"
}
```

2. **Case 2: Low Accuracy but Valid Prediction**  
   **HTTP Status Code:** 200

```json
{
    "data": {
        "created_at": DATE,
        "image_url": "String",
        "predict_id": "String",
        "result": {
            "c_menangani": "String",
            "gejala": "String",
            "message": "Under the model Accuracy",
            "penjelasan": "String",
            "predicted_class": "String",
            "predicted_prob": Float
        },
        "user_id": "String"
    },
    "status": "success"
}
```

3. **Case 3: Image Not Provided**  
   **HTTP Status Code:** 400

```json
{
  "message": "Image file is required",
  "status": "fail"
}
```

4. **Case 4: User ID Not Provided**  
   **HTTP Status Code:** 400

```json
{
  "message": "User ID is required",
  "status": "fail"
}
```

5. **Case 5: Invalid or Unrecognizable Image**  
   **HTTP Status Code:** 415

```json
{
  "message": "Image is not recognizable. Please use a better Image!",
  "status": "fail"
}
```

---

### 4. **Get Post Details**

**Route:** `/post/<string:predict_id>`  
**Method:** `GET`

**Description:**  
Retrieves details of a specific post by its `predict_id`. The `get_post_detail` function processes the request.

#### Expected Input:

- **predict_id**: The ID of the data.

#### Expected Outputs:

1. **Case 1: Successful Get Details**  
   **HTTP Status Code:** 200

```json
{
    "data": {
        "result": {
            "c_menangani": "String",
            "gejala": "String",
            "penjelasan": "String",
            "predicted_class": "String",
            "predicted_prob": Float
        }
    },
    "status": "success"
}
```

2. **Case 2: Data not found**
   **HTTP Status Code:** 404

```json
{
  "message": "Data tidak ditemukan",
  "status": "fail"
}
```

---

### 5. **User History**

**Route:** `/history/<string:user_id>`  
**Method:** `GET`

**Description:**  
Retrieves the historical data associated with a user.

#### Expected Input:

- **user_id**: The ID of the user.

#### Expected Outputs:

1. **Case 1: Data Retrieved Successfully**  
   **HTTP Status Code:** 200

```json
{
    "data": [
        {
            "created_at": DATE,
            "image_url": "String",
            "predict_id": "String",
            "result": {
                "c_menangani": "String",
                "gejala": "String",
                "penjelasan": "String",
                "predicted_class": "String",
                "predicted_prob": Float
            }
        }
    ],
    "status": "success"
}
```

2. **Case 2: User Not Found or Invalid ID**  
   **HTTP Status Code:** 404

```json
{
  "message": "History tidak ditemukan",
  "status": "fail"
}
```

---
