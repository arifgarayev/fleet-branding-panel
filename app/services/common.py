from config.default import BCRYPT_LOG_ROUNDS
from dependencies import bcrypt


class Utils:
    @staticmethod
    def hash_password(password: str):
        return bcrypt.generate_password_hash(
            password.encode("utf-8"), rounds=BCRYPT_LOG_ROUNDS
        ).decode("utf-8")


if __name__ == "__main__":
    print(Utils.hash_password("348nurmet").decode("UTF-8"))
