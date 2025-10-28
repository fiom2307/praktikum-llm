class User:
    def __init__(self, username: str, pizza_count: int = 0):
        self.username = username
        self.pizza_count = pizza_count

    def to_dict(self):
        return {
            "username": self.username,
            "pizzaCount": self.pizza_count
        }
    
    def from_dict(data: dict):
        return User(
            username=data.get("username", ""),
            pizza_count=data.get("pizzaCount", 0)
        )