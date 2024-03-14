import random


def generate_random_grid(width, height):
    # Utwórz siatkę wypełnioną wartościami 0
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # Ustaw wartości 1 na krawędziach
    for i in range(width):
        grid[0][i] = 1
        grid[height - 1][i] = 1

    for i in range(height):
        grid[i][0] = 1
        grid[i][width - 1] = 1

    # Wybierz losowo miejsca do wstawienia 1
    for row in range(2, height - 2):
        for col in range(2, width - 2):
            chance_to_place_ground = random.random() < 0.6
            is_space_above = all(grid[i][col] == 0 for i in range(row - 3, row))  # Zwiększ wymagane odstępy
            is_space_below = all(grid[i][col] == 0 for i in range(row + 1, row + 1))  # Zwiększ wymagane odstępy
            is_neighbour_ground = grid[row][col - 1] == 1 or grid[row][col + 1] == 1  # Sprawdź tylko sąsiednie kafelki po lewej i prawej stronie
            is_neighbour_space = (
                grid[row][col - 1] == 0 and grid[row][col + 1] == 0
            )  # Sprawdź, czy sąsiednie kafelki po lewej i prawej stronie są puste

            if is_neighbour_ground:
                chance_to_place_ground *= 10
            elif is_neighbour_space:
                chance_to_place_ground *= 0.03  # Zmniejsz szansę na umieszczenie ground, jeśli sąsiednie kafelki po lewej i prawej stronie są puste

            if chance_to_place_ground and is_space_above and is_space_below:
                grid[row][col] = 1

    return grid


# Test the function
for row in generate_random_grid(38, 10):
    print(row)
