
for x in range(9):
    for y in range(9):
        print("For index (", x, ", ", y, ")")
        print("Printing Box Constriaints: ")
        for i in range(x-(x%3), x + (3-(x%3)), 1):
            for j in range(y-(y%3), y + (3-(y%3)), 1):
                if i != x or j != y: #If not current node
                    print("[(" + str(x) + ", " + str(y) + ") != (" + str(i) + ", " + str(j) + ")]", end='')
                
                if i == (x + (3-(x%3)))-1 and j == (y + (3-(y%3)))-1:
                    print('')
                elif not (i == x and j == y):
                    print(", ", end='')

        print("Printing Column Constriaints: ")
        for i in range(9):
            if i != x:#If not current node
                print("[(" + str(x) + ", " + str(y) + ") != (" + str(x) + ", " + str(i) + ")]", end='')
            
            if i != 8 and i != x:
                print(", ", end='')
            elif i == 8:
                print('')

        print("Printing Row Constriaints: ")
        for i in range(9):
            if i != y:#If not current node
                print("[(" + str(x) + ", " + str(y) + ") != (" + str(i) + ", " + str(y) + ")]", end='')
            
            if i != 8 and i != y:
                print(", ", end='')
            elif i == 8:
                print('')
        print('')