from logic.HabitatList import HabitatList

if __name__ == '__main__':
    alL_snakes, all_habitat_lists = HabitatList.read_data()
    print()  # printing a blackline
    print("All Snakes:")
    for snake in alL_snakes:
        print(snake)
    print()  # to print blank line
    print("All Habitats:")
    for habitatlist in all_habitat_lists:
        print(habitatlist)
