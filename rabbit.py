import logging
from datetime import datetime
from random import random

from gender import Gender


class Rabbit:
    """A class representing a rabbit.

    Attributes:
        gender (Gender): The gender of the rabbit.
        age (float): The age of the rabbit in years.
        has_eaten (bool): Whether the rabbit has eaten recently.
        weeks_without_food (int): Number of weeks the rabbit has gone without food.
        last_reproduction_week (int or None): The last week the rabbit reproduced.
    """

    MAX_UNDER_FEED_AGE = 4
    MAX_HEALTHY_AGE = 6
    WEEKS_PER_YEAR = 52

    def __init__(self, gender: Gender, age=0):
        """Initializes the Rabbit with gender and age.

        Args:
            gender (Gender): The gender of the rabbit.
            age (float): The initial age of the rabbit. Defaults to 0.
        """
        self.gender = gender
        self.age = max(age, 0)
        self.has_eaten = True
        self.weeks_without_food = 0
        self.last_reproduction_week = None

    def age_by_a_week(self):
        """Increases the rabbit's age by one week."""
        self.age += 1 / Rabbit.WEEKS_PER_YEAR

    def eat(self, garden):
        """Attempts to eat a carrot from the garden.

        Args:
            garden (Garden): The garden from which the rabbit tries to eat.
        """
        if garden.has_carrots():
            garden.consume_carrot()
            self.has_eaten = True
            self.weeks_without_food = 0
        else:
            self.has_eaten = False
            self.weeks_without_food += 1

    def can_reproduce(self, current_week: int) -> bool:
        """Determines if the rabbit can reproduce.

        Args:
            current_week (int): The current week number.

        Returns:
            bool: True if the rabbit can reproduce, False otherwise.
        """
        return (
                self.age >= 1 and
                self.last_reproduction_week != current_week // Rabbit.WEEKS_PER_YEAR
        )

    def is_sick(self, epidemic_risk: float, rabbit_population: int) -> bool:
        """Determines if the rabbit is sick based on epidemic risk and population.

        Args:
            epidemic_risk (float): The risk factor of the epidemic.
            rabbit_population (int): The total rabbit population.

        Returns:
            bool: True if the rabbit gets sick, False otherwise.
        """
        base_disease_probability = 0.07
        age_factor = (self.age / Rabbit.MAX_HEALTHY_AGE) ** 2
        population_factor = rabbit_population / 15
        return random() < (
                base_disease_probability + epidemic_risk * population_factor
        ) * age_factor

    def is_dead(self) -> bool:
        """Checks if the rabbit is dead due to starvation or old age.

        Returns:
            bool: True if the rabbit is dead, False otherwise.
        """
        optimal_age_limit = (
            Rabbit.MAX_HEALTHY_AGE if self.has_eaten else Rabbit.MAX_UNDER_FEED_AGE
        )
        death_due_to_starvation = (
                not self.has_eaten and self.age > 2 / Rabbit.WEEKS_PER_YEAR
        )
        death_due_to_old_age = self.age > optimal_age_limit

        if death_due_to_starvation or death_due_to_old_age:
            self.log_death()
            return True
        return False

    def log_death(self):
        """Logs the death of the rabbit."""
        logging.info(f"A rabbit died on {datetime.now().strftime('%Y-%m-%d')}.")
