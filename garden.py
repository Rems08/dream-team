from animals import Rabbit, Carrot
import random
from datetime import datetime, timedelta

class Garden:
    def __init__(self):
        self.rabbits = [Rabbit('male'), Rabbit('female')]
        self.carrots = [Carrot() for _ in range(200)]
        self.current_date = datetime(2023, 1, 1)  # Starting date

    def harvest_carrot(self):
        if self.carrots:
            self.carrots.pop()
            return True
        return False

    def weekly_update(self):
        self.current_date += timedelta(weeks=1)

        # Aging and eating
        for rabbit in self.rabbits:
            rabbit.age_one_week()
            rabbit.eat(self)

        # Handle reproduction
        self.handle_reproduction()

        # Remove dead rabbits
        self.rabbits = [rabbit for rabbit in self.rabbits if not rabbit.is_dead()]

        # Handle carrot growth
        self.handle_carrot_growth()

    def handle_reproduction(self):
        potential_mothers = [rabbit for rabbit in self.rabbits if rabbit.can_reproduce(self.current_date)]
        for mother in potential_mothers:
            father = random.choice([rabbit for rabbit in self.rabbits if rabbit.gender == 'male' and rabbit != mother.last_mate])
            if father:
                litter_size = random.randint(1, 6)
                for _ in range(litter_size):
                    self.rabbits.append(Rabbit(gender=random.choice(['male', 'female'])))
                mother.last_mate = father

    def handle_carrot_growth(self):
        if self.current_date.month == 3:  # Sowing in March
            self.carrots = [Carrot() for _ in range(200)]
        elif self.current_date.month == 6:  # Harvest in June
            self.carrots = []

    def __str__(self):
        return f"Garden on {self.current_date.strftime('%Y-%m-%d')} with {len(self.rabbits)} rabbits and {len(self.carrots)} carrots"
