"""User business object class"""


class User: # pylint: disable=too-few-public-methods
    """User business object"""

    def __init__(self, username, password, created_at, last_login_at):
        self.username = username
        self.hashed_password = password
        self.created_at = created_at
        self.last_login_at = last_login_at

    def dict(self):
        """Render as dictionary"""
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "last_login_at": self.last_login_at,
        }
