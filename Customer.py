class Customer():
    def __init__(self, id, name, city):
        self.id=id
        self.name=name
        self.city=city

    def __repr__(self):
        return f'Customer(id="{self.id}", name="{self.name}", city="{self.city}")'

    def __str__(self):
        return f'Customer(id="{self.id}", name="{self.name}", city="{self.city}")'