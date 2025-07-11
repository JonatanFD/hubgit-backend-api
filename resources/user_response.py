



class UserResource:
    def __init__(self, user_id: str, email: str, username: str, platform_role: str):
        self.response = {
            "user_id": user_id,
            "email": email,
            "username": username,
            "platform_role": platform_role
        }
