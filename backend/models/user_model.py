class User:
    #
    def __init__(self, username: str, pizza_count: int = 0, password: str = None):
        self.username = username
        self.pizza_count = pizza_count
        self.password = password  

    def to_dict(self):
        return {
            "username": self.username,
            "pizzaCount": self.pizza_count
        }
    
    @classmethod
    def from_dict(cls, data: dict): 
        return cls(
            username=data.get("username", ""),
            pizza_count=data.get("pizzaCount", 0),
            password=data.get("password")  
        )