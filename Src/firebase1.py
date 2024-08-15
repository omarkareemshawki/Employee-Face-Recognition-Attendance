import pyrebase

firebaseConfig={
  'apiKey': "AIzaSyBZJutbXtz8VSvzUax2HSTzlzgGy0MHFjw",
  'authDomain': "attendance-system-64e54.firebaseapp.com",
  'projectId': "attendance-system-64e54",
  'storageBucket': "attendance-system-64e54.appspot.com",
  'messagingSenderId': "664436338546",
  'appId': "1:664436338546:web:d7810818bb738d4f16f7eb",
  'measurementId': "G-08WGRCPCGX"
}

firebase=pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
print(storage.child('trainingImg').get_url(None))
db = firebase.database()
