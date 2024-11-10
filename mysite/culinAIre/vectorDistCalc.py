import numpy as np

def vectorDistCalc(menuVec,userData,responseString):
    #calculating the euclidean distance between the user's input and the stored average metrics.

    #converting vectors to numpy arrays
    menuVec = np.array(menuVec)
    userData = np.array(userData)

    # Calculate the Euclidean distance
    distances = np.linalg.norm(menuVec - userData, axis=1)

    # Get the indices that would sort the distances in ascending order
    sortedIndices = np.argsort(distances)

    # Sort distances and responseString according to these indices
    sortedDists = distances[sortedIndices]
    sortedDishes = [responseString[i] for i in sortedIndices]

    return sortedDishes[0]