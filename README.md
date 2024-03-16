# Upload to Google Drive

Upload a file to Google Drive using Python.

## Dependencies

- **Python 3**
- **Requests** project
```
python3 -m pip install requests
```

## Installation

Download Python source files or clone this repository.

Navigate to https://console.cloud.google.com/ and create a new project.

Find and enable **Google Drive API**.

Click on **Create Credentials**.
Select **Google Drive API**.
You will be accessing **User data**.

Add scope **https://www.googleapis.com/auth/drive.file**.
Select **Desktop app** as an **Application type**.

Save your credentials with name **client_secret.json** in the directory of the source files.

## Authentication

Run **auth.py**:
```
python3 auth.py
```

Open the printed URL in a browser and follow the instructions.

## Usage

Run **upload.py**:
```
python3 upload.py [-v] FILE FOLDER_ID
```
where `FILE` is the file to be uploaded
and `FOLDER_ID` is the target folder id in Google Drive.
