import random
from animals import Rabbit, Gender, Fox, Hunter


class WindowConfig:
    def __init__(self, width, height, margin_x, margin_y):
        self.width = width
        self.height = height
        self.margin_x = margin_x
        self.margin_y = margin_y


# Carrot Class
class Carrot:
    def __init__(self, count):
        self.count = count
        self.positions = []  # Ajouter une liste pour stocker les positions des carottes

    def consume(self):
        """ Consumes a carrot, if available, and removes its position. """
        if self.count > 0 and self.positions:
            self.count -= 1
            return self.positions.pop()  # Retire et renvoie la position de la carotte consommée
        return None

    def harvest(self, additional_count, config: WindowConfig):
        """ Adds carrots to the garden and generates their positions. """
        self.count += additional_count
        for _ in range(additional_count):
            pos_x = random.randint(config.margin_x, config.width - config.margin_x)
            pos_y = random.randint(config.margin_y, config.height - config.margin_y)
            self.positions.append((pos_x, pos_y))


class GardenConfig:
    def __init__(self, window_config: WindowConfig, carrot_count: int, fox_count: int, hunter_count: int):
        self.window_config = window_config
        self.carrot_count = carrot_count
        self.fox_count = fox_count
        self.hunter_count = hunter_count


def create_garden(config: GardenConfig):
    carrots = Carrot(config.carrot_count)
    rabbits = [Rabbit(Gender.MALE), Rabbit(Gender.FEMALE)]
    foxes = [Fox('img/fox.png') for _ in range(config.fox_count)]
    hunters = [Hunter('img/hunter.png') for _ in range(config.hunter_count)]

    garden = Garden(config.window_config, carrots, rabbits, foxes, hunters)
    return garden


# Garden Class
class Garden:
    WEEKS_PER_YEAR = 52

    def __init__(self, window_config: WindowConfig, carrots: Carrot, rabbits, foxes, hunters):
        self.window_config = window_config

        self.carrots = carrots
        self.rabbits = rabbits
        self.foxes = foxes
        self.hunters = hunters

        self.current_week = 9
        self.last_planting_year = 0
        self.carrots.harvest(200, window_config)

        self.rabbits_killed_count = 0
        self.foxes_killed_count = 0

    def has_carrots(self):
        """ Checks if there are any carrots in the garden. """
        return self.carrots.count > 0

    def consume_carrot(self):
        """ Consumes a carrot from the garden. """
        return self.carrots.consume()

    def weekly_update(self):
        """ Updates the garden status every week. """
        self.current_week += 1
        current_year = self.current_week // self.WEEKS_PER_YEAR
        week_of_year = self.current_week % self.WEEKS_PER_YEAR

        # Planting and harvesting logic
        if week_of_year == 9 and current_year != self.last_planting_year:
            self.carrots.harvest(200, self.window_config)
            self.last_planting_year = current_year

        rabbit_population = len(self.rabbits)
        epidemic_risk = 0.05

        # Update each rabbit in the garden
        for rabbit in list(self.rabbits):
            rabbit.age_one_week()
            rabbit.eat(self)
            if rabbit.is_dead(epidemic_risk, self.current_week, rabbit_population):
                self.rabbits.remove(rabbit)

        self.handle_reproduction()
        self.handle_hunters()

    def handle_reproduction(self):
        """ Handles the reproduction of rabbits in the garden. """
        week_of_year = self.current_week % self.WEEKS_PER_YEAR
        if week_of_year in range(14, 18) or week_of_year in range(27, 31):
            potential_mothers = [rabbit for rabbit in self.rabbits if rabbit.can_reproduce(self.current_week)]
            for mother in potential_mothers:
                fathers = [rabbit for rabbit in self.rabbits if
                           rabbit.gender == Gender.MALE and rabbit.can_reproduce(self.current_week)]
                if fathers:
                    father = random.choice(fathers)
                    litter_size = random.randint(1, 6)
                    for _ in range(litter_size):
                        self.rabbits.append(Rabbit(gender=random.choice([Gender.MALE, Gender.FEMALE])))
                    mother.last_reproduction_week = self.current_week // self.WEEKS_PER_YEAR
                    father.last_reproduction_week = self.current_week // self.WEEKS_PER_YEAR

    def handle_hunters(self):
        print("Hunt is starting...")

        print("Foxes are hunting...")
        before_hunt_rabbit_count = len(self.rabbits)

        for fox in self.foxes:
            fox.hunt(self.current_week, self.rabbits)

        after_hunt_rabbit_count = len(self.rabbits)
        self.rabbits_killed_count += before_hunt_rabbit_count - after_hunt_rabbit_count
        print("Foxes killed {} rabbits".format(before_hunt_rabbit_count - after_hunt_rabbit_count))

        print("Hunters are hunting...")
        before_hunt_fox_count = len(self.foxes)

        remaining_foxes = self.__find_remaining_foxes()

        for hunter in self.hunters:
            print("Hunter is hunting...")
            hunter.hunt(self.current_week, remaining_foxes)

        self.foxes = remaining_foxes

        after_hunt_fox_count = len(self.foxes)
        self.foxes_killed_count += before_hunt_fox_count - after_hunt_fox_count
        print("Hunters killed {} foxes".format(before_hunt_fox_count - after_hunt_fox_count))

    def __find_remaining_foxes(self):
        return [fox for fox in self.foxes if fox.is_alive]
