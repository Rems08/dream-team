from garden import Garden

# Simulate over 6 years
garden = Garden()
for week in range(6 * 52):  # 6 years in weeks
    garden.weekly_update()

print(garden)  # Final state of the garden after 6 years
