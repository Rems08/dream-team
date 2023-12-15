import random

from gender import Gender
from rabbit import Rabbit


class Carrot:
    """A class representing a quantity of carrots in the garden."""

    def __init__(self, count):
        self.count = count

    def consume(self):
        """Consumes a carrot, if available."""
        if self.count > 0:
            self.count -= 1
            return True
        return False

    def harvest(self, additional_count):
        """Adds carrots to the garden."""
        self.count += additional_count


class Garden:
    """A class representing a garden containing rabbits and carrots."""

    WEEKS_PER_YEAR = 52
    PLANTING_WEEK = 9
    ADDITIONAL_HARVEST_WEEK = 22
    REPRODUCTION_WEEKS = list(range(14, 18)) + list(range(27, 31))

    def __init__(self):
        self.rabbits = [Rabbit(Gender.MALE), Rabbit(Gender.FEMALE)]
        self.carrots = Carrot(200)
        self.current_week = 9
        self.last_planting_year = 0

    def has_carrots(self):
        """Checks if there are any carrots in the garden."""
        return self.carrots.count > 0

    def consume_carrot(self):
        """Consumes a carrot from the garden."""
        return self.carrots.consume()

    def weekly_update(self):
        """Updates the garden status every week."""
        self.current_week += 1
        self._handle_planting_and_harvesting()
        self._update_rabbits()
        self._handle_reproduction()

    def _handle_planting_and_harvesting(self):
        """Handles the planting and harvesting of carrots."""
        current_year = self.current_week // self.WEEKS_PER_YEAR
        week_of_year = self.current_week % self.WEEKS_PER_YEAR

        if week_of_year == self.PLANTING_WEEK and current_year != self.last_planting_year:
            self.carrots.harvest(200)
            self.last_planting_year = current_year

        if week_of_year == self.ADDITIONAL_HARVEST_WEEK:
            self.carrots.harvest(200)

    def _update_rabbits(self):
        """Updates the status of each rabbit in the garden."""
        rabbit_population = len(self.rabbits)
        epidemic_risk = 0.05

        for rabbit in list(self.rabbits):
            rabbit.age_by_a_week()
            rabbit.eat(self)
            if rabbit.is_dead(epidemic_risk, rabbit_population):
                self.rabbits.remove(rabbit)

    def _handle_reproduction(self):
        """Handles the reproduction of rabbits in the garden."""
        week_of_year = self.current_week % self.WEEKS_PER_YEAR
        if week_of_year in self.REPRODUCTION_WEEKS:
            self._reproduce_rabbits()

    def _reproduce_rabbits(self):
        """Manages the reproduction process of rabbits."""
        potential_mothers = [r for r in self.rabbits if r.can_reproduce(self.current_week)]
        for mother in potential_mothers:
            fathers = [r for r in self.rabbits if r.gender == Gender.MALE and r.can_reproduce(self.current_week)]
            if fathers:
                father = random.choice(fathers)
                litter_size = random.randint(1, 6)
                for _ in range(litter_size):
                    self.rabbits.append(Rabbit(gender=random.choice([Gender.MALE, Gender.FEMALE])))
                mother.last_reproduction_week = self.current_week // self.WEEKS_PER_YEAR
                father.last_reproduction_week = self.current_week // self.WEEKS_PER_YEAR
