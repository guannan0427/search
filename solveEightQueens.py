import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        #global r_global
        #r_global = 0
        newBoard = board
        i = 0
        #r_list = []
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            #r_global += 1
            if newNumberOfAttacks == 0:
                #if r_global < 8:
                    #r_global += 1
                #else :
                    break

                   
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        
        # check the costboard to find the minimum value
        # if there are more than one minimum value, then choose it randomly
        lowest_r = -1
        lowest_c = -1

        costboard = self.getCostBoard()
        board = copy.deepcopy(self)
        lowest_cost = 9999
        lowest_costset = []

        for r in range(8):
            for c in range(8):
                if costboard.squareArray[r][c] != 'q':
                    if costboard.squareArray[r][c] <= lowest_cost:
                        lowest_cost = costboard.squareArray[r][c]#to find the first lowest one

        for r in range(8):
            for c in range(8):
                if costboard.squareArray[r][c] == lowest_cost:
                   lowest_costset.append((r,c))

       
        index = random.randint(0,len(lowest_costset)-1)
        lowest_r = lowest_costset[index][0]
        lowest_c = lowest_costset[index][1]

        for r in range(8):
            if board.squareArray[r][lowest_c] == 1:
                board.squareArray[r][lowest_c] = 0
                board.squareArray[lowest_r][lowest_c] = 1
        

        return (board,board.getNumberOfAttacks(),lowest_r,lowest_c)
                      
                

        # First, want to change each column to find the minimum number of attack
        # but is unuseful
        '''
        for c in range(8):
            for r in range(8):
                if self.squareArray[r][c]==1:
                    temp2_r = r
                    temp_r = r
                    #print('up',temp_r)
                    # to find the least up
                    while (temp_r > 1):
                        temp_r = temp_r-1
                        temp_board = copy.deepcopy(self)
                        temp_board.squareArray[temp_r][c] = 1
                        temp_board.squareArray[r][c] = 0
                        temp_numberOfAttack = temp_board.getNumberOfAttacks()
                        numberOfAttack = self.getNumberOfAttacks()
                        #print(temp_r,r,c,temp_numberOfAttack,numberOfAttack)
                        if temp_numberOfAttack < numberOfAttack:
                            row = temp_r
                            newCol = c
                            self = copy.deepcopy(temp_board)
                            r = temp_r
                            
                        else:
                            temp_r = temp_r
                    # to find the least down which compares with the least up

                    while (temp2_r < 7):
                        temp2_r = temp2_r + 1
                        #print('down',temp2_r)
                        temp2_board = copy.deepcopy(self)
                        temp2_board.squareArray[temp2_r][c] = 1
                        temp2_board.squareArray[r][c] = 0
                        temp2_numberOfAttack = temp2_board.getNumberOfAttacks()                         
                        numberOfAttack = self.getNumberOfAttacks()
                        if temp2_numberOfAttack < numberOfAttack:
                            row = temp2_r
                            newCol = c
                            self = copy.deepcopy(temp2_board)
                            r = temp2_r
                        else:
                            temp2_r = temp2_r
        
        minNumOfAttack = self.getNumberOfAttacks()
        newBoard = copy.deepcopy(self)
        return (newBoard, minNumOfAttack, row, newCol)
        '''
        
 
        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """

        
        numberOfAttack = 0
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        #check the same column
                        if rr != r:
                            if self.squareArray[rr][c]==1:
                                numberOfAttack = numberOfAttack + 1
                    for cc in range(8):
                        #check the same row
                        if cc != c:
                            if self.squareArray[r][cc]==1:
                                numberOfAttack = numberOfAttack + 1
                    for rrr in range(8):
                        for ccc in range(8):
                            #check the diagonal
                            if rrr != r and ccc != c:
                                if self.squareArray[rrr][ccc]==1:
                                    if rrr-ccc==r-c and rrr>=ccc:
                                        numberOfAttack +=1
                                    if ccc-rrr==c-r and ccc>rrr:
                                        numberOfAttack +=1
                                    if ccc+rrr==c+r:
                                        numberOfAttack +=1

        # the number of pairs
        numberOfAttack = int(numberOfAttack/2)
        return numberOfAttack
        
                            
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
