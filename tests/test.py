from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


print(bcrypt.generate_password_hash(''.encode('utf-8')).decode('utf-8'))


