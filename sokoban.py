import random
from copy import deepcopy

class BoxPath:
    def __init__(self, desX, desY, currX, currY, direction):
        self.destinationX = desX
        self.destinationY = desY
        self.currX = currX
        self.currY = currY
        self.direction = direction

def generate(height, width, boxCount):
    # Allocate board and visited, both with dimensions width x height.
    # Each cell in board is set to '.'
    # Each cell in visited is set to 'F'
    board = []
    visited = []
    setGroup = []
    for i in range(height):
        board.append([])
        visited.append([])
        setGroup.append([])
    for i in range(height):
        for j in range(width):
            board[i].append('.')
            visited[i].append('.')
            setGroup[i].append(7)

    # Set all outer boundary cells of board to '@'
    # Set all outer boundary cells of visited to 'T'
    for i in range(height):
        if i == 0 or i == height - 1:
            for j in range(width):
                board[i][j] = '@'
                visited[i][j] = 'T'
        else:
            board[i][0] = '@'
            visited[i][0] = 'T'
            board[i][width - 1] = '@'
            visited[i][width -1] = 'T'

    # Generate boxCount number of boxPaths, each with length two.
    boxPaths = []
    for i in range(boxCount):
        boxX = 0
        boxY = 0
        while board[boxY][boxX] != '.':
            boxX = random.randint(1, width - 2)
            boxY = random.randint(1, height - 2)
        board[boxY][boxX] = 'O'
        visited[boxY][boxX] = 'T'
        valid = False
        invalidLoopCount = 0
        while not valid:
            valid = True
            directionInt = random.randint(0, 3)
            if directionInt == 0 and boxY > 1 and board[boxY - 1][boxX] == '.' and board[boxY - 2][boxX] == '.':
                boxPaths.append(BoxPath(boxX, boxY, boxX, boxY - 2, 0))
                visited[boxY - 1][boxX] = 'T'
                visited[boxY - 2][boxX] = 'T'
            elif directionInt == 1 and boxX < width - 2 and board[boxY][boxX + 1] == '.' and board[boxY][boxX + 2] == '.':
                boxPaths.append(BoxPath(boxX, boxY, boxX + 2, boxY, 1))
                visited[boxY][boxX + 1] = 'T'
                visited[boxY][boxX + 2] = 'T'
            elif directionInt == 2 and boxY < height - 2 and board[boxY + 1][boxX] == '.' and board[boxY + 2][boxX] == '.':
                boxPaths.append(BoxPath(boxX, boxY, boxX, boxY + 2, 2))
                visited[boxY + 1][boxX] = 'T'
                visited[boxY + 2][boxX] = 'T'
            elif directionInt == 3 and boxX > 1 and board[boxY][boxX - 1] == '.' and board[boxY][boxX - 2] == '.':
                boxPaths.append(BoxPath(boxX, boxY, boxX - 2, boxY, 3))
                visited[boxY][boxX - 1] = 'T'
                visited[boxY][boxX - 2] = 'T'
            else:
                valid = False
                invalidLoopCount += 1
    
                if (invalidLoopCount > 50000):
                    return []

    # Elongating each of the paths
    m = ( (height - 2) * (width - 2) ) // 4 * 3 # Maximum amount of active cells
    maxBound = m // boxCount
    minBound = max(0, maxBound - 5)
    numSteps = []
    for i in range(boxCount):
        numSteps.append(random.randint(minBound, maxBound))
    for i in range(0, boxCount):
        steps = numSteps[i]
        stepsTaken = 0
        bottleneck = False
        while stepsTaken < steps and not bottleneck:

            turnInt = random.randint(1, 10000)
            turned = False
            # Lower than 30% chance of turning
            if (turnInt < 3000):
                # 15% chance of turning right and 15% chance of turning left
                turnRight = random.randint(0, 1) % 2 == 0

                currY = boxPaths[i].currY
                currX = boxPaths[i].currX
                bigTurn = random.randint(0, 4) == 4
                
                # Turn right
                if turnRight:
                    newRightDirection = (boxPaths[i].direction + 1) % 4
                    if newRightDirection == 0:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            currY > 1 and \
                            board[currY][currX - 1] != '@' and \
                            board[currY - 1][currX - 1] != '@' and \
                            board[currY - 2][currX - 1] != '@' and \
                            board[currY - 2][currX] != '@' and \
                            board[currY - 2][currX + 1] != '@' and \
                            board[currY - 1][currX + 1] != '@':
                            visited[currY][currX - 1] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            visited[currY - 2][currX - 1] = 'T'
                            visited[currY - 2][currX] = 'T'
                            visited[currY - 2][currX + 1] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 0
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY - 1][currX] != '@' and \
                            board[currY - 1][currX + 1] != '@':
                            visited[currY - 1][currX] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 0
                            stepsTaken += 2
                            turned = True
                    elif newRightDirection == 1:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            width - currX > 1 and \
                            board[currY - 1][currX] != '@' and \
                            board[currY - 1][currX + 1] != '@' and \
                            board[currY - 1][currX + 2] != '@' and \
                            board[currY][currX + 2] != '@' and \
                            board[currY + 1][currX + 2] != '@' and \
                            board[currY + 1][currX + 1] != '@':
                            visited[currY - 1][currX] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            visited[currY - 1][currX + 2] = 'T'
                            visited[currY][currX + 2] = 'T'
                            visited[currY + 1][currX + 2] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 1
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY][currX + 1] != '@' and \
                            board[currY + 1][currX + 1] != '@':
                            visited[currY][currX + 1] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 1
                            stepsTaken += 2
                            turned = True
                    elif newRightDirection == 2:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            height - currY > 1 and \
                            board[currY][currX + 1] != '@' and \
                            board[currY + 1][currX + 1] != '@' and \
                            board[currY + 2][currX + 1] != '@' and \
                            board[currY + 2][currX] != '@' and \
                            board[currY + 2][currX - 1] != '@' and \
                            board[currY + 1][currX - 1] != '@':
                            visited[currY][currX + 1] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            visited[currY + 2][currX + 1] = 'T'
                            visited[currY + 2][currX] = 'T'
                            visited[currY + 2][currX - 1] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 2
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY + 1][currX] != '@' and \
                            board[currY + 1][currX - 1] != '@':
                            visited[currY + 1][currX] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 2
                            stepsTaken += 2
                            turned = True
                    else:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            currX > 1 and \
                            board[currY + 1][currX] != '@' and \
                            board[currY + 1][currX - 1] != '@' and \
                            board[currY + 1][currX - 2] != '@' and \
                            board[currY][currX - 2] != '@' and \
                            board[currY - 1][currX - 2] != '@' and \
                            board[currY - 1][currX - 1] != '@':
                            visited[currY + 1][currX] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            visited[currY + 1][currX - 2] = 'T'
                            visited[currY][currX - 2] = 'T'
                            visited[currY - 1][currX - 2] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 3
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY][currX - 1] != '@' and \
                            board[currY - 1][currX - 1] != '@':
                            visited[currY][currX - 1] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 3
                            stepsTaken += 2
                            turned = True
                # Turn left
                else:
                    newLeftDirection = (boxPaths[i].direction - 1) % 4
                    if newLeftDirection == 0:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            currY > 2 and \
                            board[currY][currX + 1] != '@' and \
                            board[currY - 1][currX + 1] != '@' and \
                            board[currY - 2][currX + 1] != '@' and \
                            board[currY - 2][currX] != '@' and \
                            board[currY - 2][currX - 1] != '@' and \
                            board[currY - 1][currX - 1] != '@':
                            visited[currY][currX + 1] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            visited[currY - 2][currX + 1] = 'T'
                            visited[currY - 2][currX] = 'T'
                            visited[currY - 2][currX - 1] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 0
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY - 1][currX] != '@' and \
                            board[currY - 1][currX - 1] != '@':
                            visited[currY - 1][currX] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 0
                            stepsTaken += 2
                            turned = True

                    elif newLeftDirection == 1:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            width - currX > 1 and \
                            board[currY + 1][currX] != '@' and \
                            board[currY + 1][currX + 1] != '@' and \
                            board[currY + 1][currX + 2] != '@' and \
                            board[currY][currX + 2] != '@' and \
                            board[currY - 1][currX + 2] != '@' and \
                            board[currY - 1][currX + 1] != '@':
                            visited[currY + 1][currX] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            visited[currY + 1][currX + 2] = 'T'
                            visited[currY][currX + 2] = 'T'
                            visited[currY - 1][currX + 2] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 1
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY][currX + 1] != '@' and \
                            board[currY - 1][currX + 1] != '@':
                            visited[currY][currX + 1] = 'T'
                            visited[currY - 1][currX + 1] = 'T'
                            boxPaths[i].currY -= 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 1
                            stepsTaken += 2
                            turned = True
                    elif newLeftDirection == 2:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            height - currY > 1 and \
                            board[currY][currX - 1] != '@' and \
                            board[currY + 1][currX - 1] != '@' and \
                            board[currY + 2][currX - 1] != '@' and \
                            board[currY + 2][currX] != '@' and \
                            board[currY + 2][currX + 1] != '@' and \
                            board[currY + 1][currX + 1] != '@':
                            visited[currY][currX - 1] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            visited[currY + 2][currX - 1] = 'T'
                            visited[currY + 2][currX] = 'T'
                            visited[currY + 2][currX + 1] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 2
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY + 1][currX] != '@' and \
                            board[currY + 1][currX + 1] != '@':
                            visited[currY + 1][currX] = 'T'
                            visited[currY + 1][currX + 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX += 1
                            boxPaths[i].direction = 2
                            stepsTaken += 2
                            turned = True
                    else:
                        if bigTurn and \
                            stepsTaken + 6 <= steps and \
                            height > 1 and \
                            board[currY - 1][currX] != '@' and \
                            board[currY - 1][currX - 1] != '@' and \
                            board[currY - 1][currX - 2] != '@' and \
                            board[currY][currX - 2] != '@' and \
                            board[currY + 1][currX - 2] != '@' and \
                            board[currY + 1][currX - 1] != '@':
                            visited[currY - 1][currX] = 'T'
                            visited[currY - 1][currX - 1] = 'T'
                            visited[currY - 1][currX - 2] = 'T'
                            visited[currY][currX - 2] = 'T'
                            visited[currY + 1][currX - 2] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 3
                            stepsTaken += 6
                            turned = True
                        elif stepsTaken + 2 <= steps and \
                            board[currY][currX - 1] != '@' and \
                            board[currY + 1][currX - 1] != '@':
                            visited[currY][currX - 1] = 'T'
                            visited[currY + 1][currX - 1] = 'T'
                            boxPaths[i].currY += 1
                            boxPaths[i].currX -= 1
                            boxPaths[i].direction = 3
                            stepsTaken += 2
                            turned = True

            # The rest are chances of not turning (approx 70%)
            if not turned:
                currY = boxPaths[i].currY
                currX = boxPaths[i].currX
                direction = boxPaths[i].direction
                stepsTaken += 1
                if direction == 0 and board[currY - 1][currX] != '@':
                    visited[currY - 1][currX] = 'T'
                    boxPaths[i].currY -= 1
                elif direction == 1 and board[currY][currX + 1] != '@':
                    visited[currY][currX + 1] = 'T'
                    boxPaths[i].currX += 1
                elif direction == 2 and board[currY + 1][currX] != '@':
                    visited[currY + 1][currX] = 'T'
                    boxPaths[i].currY += 1
                elif direction == 3 and board[currY][currX - 1] != '@':
                    visited[currY][currX - 1] = 'T'
                    boxPaths[i].currX -= 1
                else:
                    stepsTaken -= 1
                    bottleneck = True

        direction = boxPaths[i].direction
        currX = boxPaths[i].currX
        currY = boxPaths[i].currY


        if direction == 0:
            if board[currY][currX + 1] != '@' and board[currY + 1][currX + 1] != '@' and board[currY + 2][currX + 1] != '@':
                visited[currY][currX + 1] = 'T'
                visited[currY + 1][currX + 1] = 'T'
                visited[currY + 2][currX + 1] = 'T'
            else:
                visited[currY][currX - 1] = 'T'
                visited[currY + 1][currX - 1] = 'T'
                visited[currY + 2][currX - 1] = 'T'
        elif direction == 1:
            if board[currY + 1][currX] != '@' and board[currY + 1][currX - 1] != '@' and board[currY + 1][currX - 2] != '@':
                visited[currY + 1][currX] = 'T'
                visited[currY + 1][currX - 1] = 'T'
                visited[currY + 1][currX - 2] = 'T'
            else:
                visited[currY + 1][currX] = 'T'
                visited[currY + 1][currX - 1] = 'T'
                visited[currY + 1][currX - 2] = 'T'
        elif direction == 2:
            if board[currY][currX - 1] != '@' and board[currY - 1][currX - 1] != '@' and board[currY - 2][currX - 1] != '@':
                visited[currY][currX - 1] = 'T'
                visited[currY - 1][currX - 1] = 'T'
                visited[currY - 2][currX - 1] = 'T'
            else:
                visited[currY][currX + 1] = 'T'
                visited[currY - 1][currX + 1] = 'T'
                visited[currY - 2][currX + 1] = 'T'
        else:
            if board[currY - 1][currX] != '@' and board[currY - 1][currX + 1] != '@' and board[currY - 1][currX + 2] != '@':
                visited[currY - 1][currX] = 'T'
                visited[currY - 1][currX + 1] = 'T'
                visited[currY - 1][currX + 2] = 'T'
            else:
                visited[currY + 1][currX] = 'T'
                visited[currY + 1][currX + 1] = 'T'
                visited[currY + 1][currX + 2] = 'T'

        if i != 0:
            ansX = -1
            ansY = -1
            foundUnion = False
            que = []
            que.append([currX, currY])
            prevs = []
            disjointVisited = []
            for i in range(height):
                prevs.append([])
                disjointVisited.append([])
                for j in range(width):
                    prevs[i].append([-1, -1])
                    disjointVisited[i].append('F')
            prevs[currY][currX] = [currX, currY]
            while que and not foundUnion:
                curr = que.pop()
                x = curr[0]
                y = curr[1]
                disjointVisited[y][x] = 'T'
                if board[y - 1][x] != '@' and disjointVisited[y - 1][x] == 'F':
                    if setGroup[y - 1][x] != 0:
                        if prevs[y - 1][x] == [-1, -1]:
                            prevs[y - 1][x] = [x, y]
                        que.append([x, y - 1])
                    else:
                        foundUnion = True
                        ansX = x
                        ansY = y
                if board[y][x - 1] != '@' and disjointVisited[y][x - 1] == 'F':
                    if setGroup[y][x - 1] != 0:
                        if prevs[y][x - 1] == [-1, -1]:
                            prevs[y][x - 1] = [x, y]
                        que.append([x - 1, y])
                    else:
                        foundUnion = True
                        ansX = x
                        ansY = y
                if board[y][x + 1] != '@' and disjointVisited[y][x + 1] == 'F':
                    if setGroup[y][x + 1] != 0:
                        if prevs[y][x + 1] == [-1, -1]:
                            prevs[y][x + 1] = [x, y]
                        que.append([x + 1, y])
                    else:
                        foundUnion = True
                        ansX = x
                        ansY = y
                if board[y + 1][x] != '@' and disjointVisited[y + 1][x] == 'F':
                    if setGroup[y + 1][x] != 0:
                        if prevs[y + 1][x] == [-1, -1]:
                            prevs[y + 1][x] = [x, y]
                        que.append([x, y + 1])
                    else:
                        foundUnion = True
                        ansX = x
                        ansY = y
            while prevs[ansY][ansX] != [ansX, ansY]:
                visited[ansY][ansX] = 'T'
                ansX, ansY = prevs[ansY][ansX][0], prevs[ansY][ansX][1]
            
        que = [[currX, currY]]
        while que:
            c = que.pop()
            x = c[0]
            y = c[1]
            setGroup[y][x] = 0
            if visited[y - 1][x] == 'T' and y != 1 and setGroup[y - 1][x] != 0:
                que.append([x, y - 1])
            if visited[y][x + 1] == 'T' and x != width - 2 and setGroup[y][x + 1] != 0:
                que.append([x + 1, y])
            if visited[y + 1][x] == 'T' and y != height - 2 and setGroup[y + 1][x] != 0:
                que.append([x, y + 1])
            if visited[y][x - 1] == 'T' and x != 1 and setGroup[y][x - 1] != 0:
                que.append([x - 1, y])

        if direction == 0:
            board[currY + 1][currX] = '@'
        elif direction == 1:
            board[currY][currX - 1] = '@'
        elif direction == 2:
            board[currY - 1][currX] = '@'
        else:
            board[currY][currX + 1] = '@'

    print("Generating 70%...")

    # Inner walls generation:
    validChoices = []
    for j in range(1, height - 1):
        for k in range(1, width - 1):
            if visited[j][k] == '.':
                validChoices.append([j, k])
    if len(validChoices) == 0:
        print("Not enough walls, regenerating")
        return [[], [], [], []]
    for validChoice in validChoices:
        board[validChoice[0]][validChoice[1]] = '@'
    # Turning boxes from immovable walls back into a box.
    for boxPath in boxPaths:
        x = boxPath.currX
        y = boxPath.currY
        direction = boxPath.direction
        if direction == 0:
            board[y + 1][x] = 'X'
        elif direction == 1:
            board[y][x - 1] = 'X'
        elif direction == 2:
            board[y - 1][x] = 'X'
        else:
            board[y][x + 1] = 'X'
    print("Generating 85%...")

    # Generating a random player position
    validChoices = []
    for j in range(1, height - 1):
        for k in range(1, width - 1):
            if board[j][k] == '.':
                validChoices.append([j, k])
    r = random.randint(0, len(validChoices) - 1)
    board[validChoices[r][0]][validChoices[r][1]] = 'P'

    print("Generating 100%...")
    print("Generating complete.")
    print("----------------------Vault of Sokoban----------------------")
    print("Hidden deep within the Amazon Forest, the ancient 'Vault of ")
    print("Sokoban' holds the source of the world's harmony. Over the ")
    print("centuries, its mechanisms -- powered by magical, glowing")
    print("crates have become misaligned due to the passing of time and")
    print("the greed of those who died seeking the vault's power.")
    print("")
    print("As the player, your job is to align the crates back to their")
    print("original position. With this newfound power, you can save the")
    print("world from the chickens that have terrorized the world for")
    print("centuries. Good luck, adventurer!")
    print("")
    return board

width = 12
height = 12
boxCount = 3

origBoard = []
gameBoard = []

doneGenerating = False
while not doneGenerating:
    origBoard = generate(height, width, boxCount)
    if origBoard:
        gameBoard = deepcopy(origBoard)
        xCount, oCount, pCount = 0, 0, 0
        for row in gameBoard:
            for cell in row:
                if cell == 'X':
                    xCount += 1
                elif cell == 'O':
                    oCount += 1
                elif cell == 'P':
                    pCount += 1
        if xCount == boxCount and oCount == boxCount and pCount == 1:
            doneGenerating = True

def isWon(gameboard):
    for row in gameboard:
        for cell in row:
            if cell == 'O':
                return False
    return True

playerX = -1
playerY = -1
for i in range(height):
    for j in range(width):
        if origBoard[i][j] == 'P':
            playerX = j
            playerY = i
gameOver = False
while not gameOver:
    for i in range(height):
        for j in range(width):
            print(gameBoard[i][j], end=" ")
        if i == 1:
            print("    Press WASD to move around.", end="")
        elif i == 2:
            print("    Press R to reset the board.", end="")
        elif i == 3:
            print("    Press Q to quit the game.", end="")
        elif i == 4:
            print("    Press N to create a new board.", end="")
        elif i == 6:
            print("    X: Box", end="")
        elif i == 7:
            print("    @: Wall", end="")
        elif i == 8:
            print("    P: Player", end="")
        elif i == 9:
            print("    O: Destination", end="")
        print()
    print("Next Move: ")

    u1 = gameBoard[playerY - 1][playerX]
    r1 = gameBoard[playerY][playerX + 1]
    d1 = gameBoard[playerY + 1][playerX]
    l1 = gameBoard[playerY][playerX - 1]

    i = input()
    if i == 'a':
        if l1 == 'X' and playerX > 1:
            l2 = gameBoard[playerY][playerX - 2]
            if l2 == 'O' or l2 == '.':
                if origBoard[playerY][playerX] == 'O':
                    gameBoard[playerY][playerX] = 'O'
                else:
                    gameBoard[playerY][playerX] = '.'
                gameBoard[playerY][playerX - 1] = 'P'
                gameBoard[playerY][playerX - 2] = 'X'
            else:
                playerX += 1
        elif l1 == '.' or l1 == 'O':
            if origBoard[playerY][playerX] == 'O':
                gameBoard[playerY][playerX] = 'O'
            else:
                gameBoard[playerY][playerX] = '.'
            gameBoard[playerY][playerX - 1] = 'P'
        else:
            playerX += 1
        playerX -= 1
    elif i == 'w':
        if u1 == 'X' and playerY > 1:
            u2 = gameBoard[playerY - 2][playerX]
            if u2 == 'O' or u2 == '.':
                if origBoard[playerY][playerX] == 'O':
                    gameBoard[playerY][playerX] = 'O'
                else:
                    gameBoard[playerY][playerX] = '.'
                gameBoard[playerY - 1][playerX] = 'P'
                gameBoard[playerY - 2][playerX] = 'X'
            else:
                playerY += 1
        elif u1 == '.' or u1 == 'O':
            if origBoard[playerY][playerX] == 'O':
                gameBoard[playerY][playerX] = 'O'
            else:
                gameBoard[playerY][playerX] = '.'
            gameBoard[playerY - 1][playerX] = 'P'
        else:
            playerY += 1
        playerY -= 1

    elif i == 's':
        if d1 == 'X' and playerY < height - 2:
            d2 = gameBoard[playerY + 2][playerX]
            if d2 == 'O' or d2 == '.':
                if origBoard[playerY][playerX] == 'O':
                    gameBoard[playerY][playerX] = 'O'
                else:
                    gameBoard[playerY][playerX] = '.'
                gameBoard[playerY + 1][playerX] = 'P'
                gameBoard[playerY + 2][playerX] = 'X'
            else:
                playerY -= 1
        elif d1 == '.' or d1 == 'O':
            if origBoard[playerY][playerX] == 'O':
                gameBoard[playerY][playerX] = 'O'
            else:
                gameBoard[playerY][playerX] = '.'
            gameBoard[playerY + 1][playerX] = 'P'
        else:
            playerY -= 1
        playerY += 1
    elif i == 'd':
        if r1 == 'X' and playerX < width - 2:
            r2 = gameBoard[playerY][playerX + 2]
            if r2 == 'O' or r2 == '.':
                if origBoard[playerY][playerX] == 'O':
                    gameBoard[playerY][playerX] = 'O'
                else:
                    gameBoard[playerY][playerX] = '.'
                gameBoard[playerY][playerX + 1] = 'P'
                gameBoard[playerY][playerX + 2] = 'X'
            else:
                playerX -= 1
        elif r1 == '.' or r1 == 'O':
            if origBoard[playerY][playerX] == 'O':
                gameBoard[playerY][playerX] = 'O'
            else:
                gameBoard[playerY][playerX] = '.'
            gameBoard[playerY][playerX + 1] = 'P'
        else:
            playerX -= 1
        playerX += 1
    elif i == 'r':
        gameBoard = deepcopy(origBoard)
    elif i == 'n':
        doneGenerating = False
        if origBoard:
            while not doneGenerating:
                origBoard = generate(height, width, boxCount)
                gameBoard = deepcopy(origBoard)
                xCount, oCount, pCount = 0, 0, 0
                for row in gameBoard:
                    for cell in row:
                        if cell == 'X':
                            xCount += 1
                        elif cell == 'O':
                            oCount += 1
                        elif cell == 'P':
                            pCount += 1
                if xCount == boxCount and oCount == boxCount and pCount == 1:
                    doneGenerating = True
    elif i == 'q':
        gameOver = True
    if isWon(gameBoard):
        for row in gameBoard:
            for c in row:
                print(c, end=" ")
            print()
        print("You won!")
        gameOver = True



