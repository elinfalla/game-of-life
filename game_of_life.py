import Tkinter
import random
import time

#NUM_RUNS = 10
CANVAS_DIMENSION = 400 #pixels
GRID_DIMENSION = 100
scalingFactor = CANVAS_DIMENSION / GRID_DIMENSION #how many pixels across/down each square of the grid is (ie each cell)


#FUNCTION TO CREATE INITIAL RANDOM GRID OF CELLS AND DRAW THEM ON CANVAS
def initialiseCanvas(canvas):
    print("into initcanvas")

    #CREATE CELL GRID - 2D ARRAY OF ALL ZERO VALUES
    cellGrid = []
    for _ in range(GRID_DIMENSION):
        row = []
        for _ in range(GRID_DIMENSION):
            row.append(0)
        cellGrid.append(row)

    #CREATE RANDOM STARTER GRID
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):
            cellGrid[row][col] = random.randint(0, 1)

            #FILL INITIAL ALIVE (=1) CELLS WITH OVAL ON CANVAS
            if cellGrid[row][col] == 1:
                cellRender = canvas.create_oval(
                col * scalingFactor, #x0 - bottom left coord
                row * scalingFactor, #y0 - bottom left coord
                (col+1) * scalingFactor, #x1 - top right coord
                (row+1) * scalingFactor, #y1 - top right coord
                fill='black',
                outline='black')

    return cellGrid


#FUNCTION TO CREATE GRID CONTAINING THE NUMBER OF NEIGHBOURS EACH CELL HAS
def scanNeighbours(cellGrid):

    #CREATE GRID TO HOLD THE NUMBER OF LIVE NEIGHBOURS EACH CELL IN GRID HAS, INITIALISE WITH ZEROS
    numNeighboursGrid = []
    for _ in range(GRID_DIMENSION):
        row = []
        for _ in range(GRID_DIMENSION):
            row.append(0)
        numNeighboursGrid.append(row)

    #ITERATE THROUGH CELL GRID
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):

            #FOR EACH CELL, FIND COORDINATES OF ALL 8 NEIGHBOURS
            for xoffset in range(-1, 2): #doesn't include 2
                for yoffset in range(-1, 2):
                    neighbourX = row + xoffset
                    neighbourY = col + yoffset

                    #ENSURE THAT NEIGHBOUR COORDINATE IS VALID
                    in_bounds = neighbourX in range(GRID_DIMENSION) and neighbourY in range(GRID_DIMENSION)
                    not_center = not (xoffset == yoffset == 0) #ie. 0 offset means current cell, not a neighbour

                    #IF NEIGHBOUR IS ALIVE, ADD 1 TO THE TOTAL NEIGHBOURS FOR THE CELL
                    if in_bounds and not_center:
                        if cellGrid[neighbourX][neighbourY] == 1: #1 means live cell
                            numNeighboursGrid[row][col] += 1

    return numNeighboursGrid


#FUNCTION TO UPDATE GRID BASED ON CONWAY'S RULES
def runIteration(cellGrid):

    #CREATE GRID OF NEIGHBOURS
    numNeighboursGrid = scanNeighbours(cellGrid)

    #ITERATE THROUGH GRID
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):

            #IF CELL IS ALIVE AND HAS MORE OR LESS THAN 2 OR 3 NEIGHBOURS, IT DIES
            if cellGrid[row][col] == 1:
                if numNeighboursGrid[row][col] != 2 and \
                numNeighboursGrid[row][col] != 3:
                    cellGrid[row][col] = 0

            #IF CELL IS DEAD AND HAS 3 NEIGHBOURS, IT BECOMES ALIVE
            elif cellGrid[row][col] == 0:
                if numNeighboursGrid[row][col] == 3:
                    cellGrid[row][col] = 1

    return cellGrid


#FUNCTION TO UPDATE CANVAS TO MATCH CELL GRID
def renderCanvas(cellGrid, canvas):

    #ITERATE THROUGH CELL GRID
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):

            #IF CELL IS ALIVE, DRAW BLACK CIRCLE AT THAT POSITION
            if cellGrid[row][col] == 1:
                celRender = canvas.create_oval(
                col * scalingFactor, #x0 - bottom left coord
                row * scalingFactor, #y0 - bottom left coord
                (col+1) * scalingFactor, #x1 - top right coord
                (row+1) * scalingFactor, #y1 - top right coord
                fill='black',
                outline='black')

            #IF CELL IS DEAD, DRAW WHITE CIRCLE AT THAT POSITION
            else:
                celllRender = canvas.create_oval(
                col * scalingFactor, #x0 - bottom left coord
                row * scalingFactor, #y0 - bottom left coord
                (col+1) * scalingFactor, #x1 - top right coord
                (row+1) * scalingFactor, #y1 - top right coord
                fill='white',
                outline='white')


#FUNCTION TO RUN SIMULATION - CONTINUALLY UPDATING CELL GRID AND CANVAS
def runSimulation(cellGrid, canvas):

    #UPDATE CELL GRID AND CANVAS
    cellGrid = runIteration(cellGrid)
    renderCanvas(cellGrid, canvas)

    #WAIT, THEN REPEAT
    master.after(2000, runSimulation, cellGrid, canvas)


#MAIN PROGRAMME
if __name__ == '__main__': #only runs if explicitly told to

    #CREATE GUI APPLICATION MAIN WINDOW
    master = Tkinter.Tk()

    #CREATE CANVAS
    canvas = Tkinter.Canvas(master, height=CANVAS_DIMENSION, width=CANVAS_DIMENSION, bg='white')
    canvas.pack()

    #INITIALISE CELL GRID AND DRAW ON CANVAS
    cellGrid = initialiseCanvas(canvas)

    #ENTER MAIN EVENT LOOP, AND AFTER DELAY START RUNNING SIMULATION
    master.after(2000, runSimulation, cellGrid, canvas)
    master.mainloop()
