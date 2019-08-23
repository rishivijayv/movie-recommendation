# Prompts the User to enter a movie and then suggests movies that have similar:
# (1) Plotline/Overview, or
# (2) Genre/Director/Case

from PythonFiles.recmovies import recommend, overview_matrix, meta_matrix

print("--------------------- RECOMMEND A MOVIE --------------------- \n")
quit_app = 0
while quit_app != 'y':
    movie = input("What movie did you watch recently? ")
    movie = str.lower(movie.replace(" ", ""))
    print("Do you want movies that have similar: \n")
    print("1. Plot Line\n")
    print("2. Genre, Director, Cast\n")
    choice = 0
    while choice != 1 and choice != 2:
        choice = int(input("Enter (1) or (2): "))
    try:
        if choice == 1:
            print(recommend(movie, overview_matrix))
        else:
            print(recommend(movie, meta_matrix))
    except KeyError as ke:
        print("Sorry, we don't have \"" + movie + "\" in our database currently.")

    print("-------------------------------")
    quit_app = input("Enter y to quit or anything else to continue: ")