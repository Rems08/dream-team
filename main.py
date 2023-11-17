import matplotlib.pyplot as plt
from garden import Garden

def plot_garden_evolution(garden):
    weeks = list(range(len(garden.rabbit_count)))
    plt.figure(figsize=(10, 6))

    # Plotting rabbits and carrots over time
    plt.plot(weeks, garden.rabbit_count, label='Rabbits')
    plt.plot(weeks, garden.carrot_count, label='Carrots')
    
    # Optionally, plot reproduction events
    plt.plot(weeks, garden.reproduction_count, label='Reproduction Events')

    plt.xlabel('Weeks')
    plt.ylabel('Count')
    plt.title('Garden Evolution Over Time')
    plt.legend()
    plt.show()

# Run the simulation
garden = Garden()
for week in range(6 * 52):
    garden.weekly_update()

# Plot the results
plot_garden_evolution(garden)
