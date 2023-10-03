from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    """
    Class for creating hash of the password and verifying plain password with hash stored
    """
    @classmethod
    def create_hash(cls, password: str) -> str:
        """
        Create passsword hash method
        :param password: Plain password provided as a string
        :return: Hash of the password
        """
        return pwd_context.hash(password)

    @classmethod
    def verify_hash(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password method
        :param plain_password: Plain password received as a string
        :param hashed_password: Hash of the password
        :return: Boolean - True if the verification is successful, otherwise - False
        """
        return pwd_context.verify(plain_password, hashed_password)
