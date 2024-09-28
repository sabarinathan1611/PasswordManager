
# PasswordManager

This project is a Flask-based web application designed to handle user authentication, form submissions, and secure data management. The application utilizes encryption for sensitive data such as user credentials and email, with plans for secure file storage in the future.


## Features

- User Authentication: Supports user login, registration, and session management.
- AES and RSA Hybrid Encryption: Secure password and email storage using a combination of AES for data encryption and RSA for encrypting the AES keys.
- CSRF Protection: Ensures protection against CSRF (Cross-Site Request Forgery) attacks.
- Secure File Upload: The application is configured to handle file uploads, with file storage functionality coming soon.


## Project Structure




```bash
PasswordManager/
├── app
├── auth.py
│   ├── auth.py
│   ├── .env
│   ├── config.py
│   ├── Converter.py
│   ├── dataencryption.py
│   ├── DeleteTask.py
│   ├── demo.py
│   ├── fileencryption.py
│   ├── forms.py
│   ├── functions.py
│   ├── __init__.py
│   ├── Log
│   │   └── Log.py
│   ├── models.py
│   ├── requirements.txt
│   ├── static
│   │   ├── asset
│   │   │   ├── icons
│   │   │   │   ├── icon_1 (1).png
│   │   │   │   ├── icon_2 (1).png
│   │   │   │   ├── icon_3 (1).png
│   │   │   │   └── icon_4 (1).png
│   │   │   ├── images
│   │   │   │   ├── all-in-one.jpg
│   │   │   │   ├── authentication.png
│   │   │   │   ├── background.avif
│   │   │   │   ├── business-password-manager.webp
│   │   │   │   ├── file-manager.png
│   │   │   │   ├── hand-drawn-construction-background_23-2147734520.avif
│   │   │   │   ├── image-manager.png
│   │   │   │   ├── logo.avif
│   │   │   │   ├── logo-sc.png
│   │   │   │   ├── main-background.avif
│   │   │   │   ├── main-image.png
│   │   │   │   ├── password-manager.png
│   │   │   │   └── password-managers.webp
│   │   │   └── logos
│   │   │       ├── logo.png
│   │   │       ├── settings.png
│   │   │       └── title-logo.png
│   │   ├── css
│   │   │   ├── about.css
│   │   │   ├── home.css
│   │   │   ├── login.css
│   │   │   ├── nav.css
│   │   │   ├── showpassword.css
│   │   │   └── style.css
│   │   ├── images
│   │   │   ├── 6538623-removebg-preview.png
│   │   │   ├── add.png
│   │   │   ├── avatar.jfif
│   │   │   ├── close_FILL0_wght400_GRAD0_opsz24.svg
│   │   │   ├── menu_FILL0_wght400_GRAD0_opsz24.svg
│   │   │   └── refresh.png
│   │   ├── js
│   │   │   ├── getform.js
│   │   │   ├── home.js
│   │   │   ├── login.js
│   │   │   ├── passwords.js
│   │   │   ├── request.js
│   │   │   ├── script.js
│   │   │   ├── scroll.js
│   │   │   └── validateForm.js
│   │   ├── key
│   │   │   ├── private_key
│   │   │   └── public_key
│   │   └── uploads
│   ├── sysinfo.py
│   ├── templates
│   │   ├── About.html
│   │   ├── admin.html
│   │   ├── base.html
│   │   ├── changepass.html
│   │   ├── decrypted_file.html
│   │   ├── email.html
│   │   ├── home.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── passwords.html
│   │   ├── POST 1.1.txt
│   │   ├── profile.html
│   │   ├── Signup.html
│   │   └── uploadfile.html
│   ├── testpass.py
│   ├── TextEncryption.py
│   └── view.py
├── app.py
├── Cloud.sql
├── Dockerfile
├── instance
│   └── database.db
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── test
    ├── config.ini
    ├── decrypted_file.png
    ├── encrpytfile.py
    ├── encrypted_file.bin
    ├── main.py
    ├── private_key.der
    ├── private_key.pem
    ├── public_key.der
    ├── public_key.pem
    ├── req.txt
    ├── sysinfo.py
    ├── Test.png
    ├── test.py
    └── textencryption.py


```
    
## Environment Variables(Optional)

To run this project, you will need to add the following environment variables to your .env file

`KEY`

`IV`


## Encryption Logic
 
The application secures sensitive data, such as user passwords and email addresses, using a hybrid encryption approach.

- AES (Advanced Encryption Standard) is used for encrypting the actual data.
- RSA (Rivest–Shamir–Adleman) is used to encrypt the AES session key.
- This method ensures that sensitive data is both secure and efficiently encrypted.

#### Here’s a simplified view of how encryption is handled:

- A random AES session key is generated and used to encrypt the data.
- The AES session key is then encrypted with the RSA public key.
- Both the encrypted session key and the encrypted data are stored.
In the future, file storage will also be secured using this encryption approach.


## Getting Started

### Prerequisites

#### Ensure you have the following installed on your machine:

- Python 3.8+
- Flask
- Flask-WTF (for CSRF protection)
- Flask-SQLAlchemy (for database management)
- Flask-Login (for user session management)
- Flask-Mail (for email verification)
- Flask-CORS (for cross-origin requests)
- Flask-Migrate (for database migrations)






## Installation
1. Clone the repository:
    
    ```bash
    git clone https://github.com/sabarinathan1611/PasswordManager.git
    cd PasswordManager
    
    ```
2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate

    ```
3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    ```bash
    flask db upgrade
    ```
## Running the Application
Start the Flask development server:

    flask run
Visit http://127.0.0.1:5000 in your browser.

## Security Measures


####  CSRF Protection
The application uses Flask-WTF to protect against CSRF attacks. This ensures that every form and API request is accompanied by a valid CSRF token, which is validated on the server-side before processing the request.

#### Session Management
User sessions are managed securely using Flask-Login. Sessions are configured to be permanent and have a short lifespan (e.g., 1 minute) to reduce the risk of session hijacking.

#### Future Enhancements
- File Storage: Secure and encrypted file storage will be added in the future to handle user uploads securely.
- Enhanced Security: More advanced features such as two-factor authentication (2FA) will be considered for further protection.



## License



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Contributing
Feel free to submit issues and feature requests via GitHub Issues. Pull requests are welcome!