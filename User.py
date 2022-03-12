class User():
    def __init__(self, id, public_id, username, password):
        self.id=id
        self.public_id=public_id
        self.username=username
        self.password=password

    def __repr__(self):
        return f'Customer(id="{self.id}", public_id="{self.public_id}", city="{self.username}", password="{self.password}")'

    def __str__(self):
        return f'Customer(id="{self.id}", public_id="{self.public_id}", city="{self.username}", password="{self.password}")'