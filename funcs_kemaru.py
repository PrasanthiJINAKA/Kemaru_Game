import random
import numpy as np

def isNotInList(l, arr):
    # Checks if an array is present in an iterable of arrays
    flag = True
    for r in l:
        if r.shape==arr.shape:
            if (r==arr).all():
                return False
    return flag

def rotate_matrix( m ):
    # For getting different shape transformations. For example a grid of 2 size can be a horizontal line or vertical line
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def fit_in(grid, ch):
    # Returns a list of row,column indices where a shape can fit on our whole board
    available_options = list()
    x,y = ch.shape
    for i in range(10-x):
        for j in range(10-y):
            grid_ch = grid[i:i+x,j:j+y].copy()
            if (ch+grid_ch).max()==1:
                available_options.append([i,j])
    return available_options

def get_all_shapes():
    # Returns all possible shapes of grid groups that can be used on the board
    all_regions = list()

    region1 = [np.array([[1]])]
    for r in region1:
        all_regions.append(r)

    region2 = [np.array([[1,1]])]
    for r in region2:
        all_regions.append(r)

    region3 = [np.array([[1,1,1]]),np.array([[1,1],[1,0]])]
    for r in region3:
        if isNotInList(all_regions, r):
            all_regions.append(r)
        if isNotInList(all_regions, r.T):
            all_regions.append(r.T)
        rr = r.copy()
        for _ in range(3):
            rr = np.array(rotate_matrix(rr))
            if isNotInList(all_regions, rr):
                all_regions.append(rr)
            if isNotInList(all_regions, rr.T):
                all_regions.append(rr.T)

    region4 = [np.array([[1,1,1,1]]),np.array([[1,1],[1,1]]),
               np.array([[1,1,1],[0,1,0]]), np.array([[1,1,1],[1,0,0]]),
               np.array([[1,1,0],[0,1,1]])]
    for r in region4:
        if isNotInList(all_regions, r):
            all_regions.append(r)
        if isNotInList(all_regions, r.T):
            all_regions.append(r.T)
        rr = r.copy()
        for _ in range(3):
            rr = np.array(rotate_matrix(rr))
            if isNotInList(all_regions, rr):
                all_regions.append(rr)
            if isNotInList(all_regions, rr.T):
                all_regions.append(rr.T)

    region5 = [np.array([[1,1,1,1,1]]),np.array([[0,1,1],[1,1,0],[0,1,0]]),
               np.array([[1,1,1,1],[1,0,0,0]]), np.array([[1,1],[1,1],[1,0]]),
               np.array([[1,1,0,0],[0,1,1,1]]), np.array([[1,1,1],[1,0,1]]),
               np.array([[1,1,1],[0,1,0],[0,1,0]]), np.array([[1,1,1],[1,0,0],[1,0,0]]),
               np.array([[0,0,1],[0,1,1],[1,1,0]]), np.array([[1,1,1,1],[0,1,0,0]]),
               np.array([[0,1,0],[1,1,1],[0,1,0]]), np.array([[1,1,0],[0,1,0],[0,1,1]])]
    for r in region5:
        if isNotInList(all_regions, r):
            all_regions.append(r)
        if isNotInList(all_regions, r.T):
            all_regions.append(r.T)
        rr = r.copy()
        for _ in range(3):
            rr = np.array(rotate_matrix(rr))
            if isNotInList(all_regions, rr):
                all_regions.append(rr)
            if isNotInList(all_regions, rr.T):
                all_regions.append(rr.T)
    return all_regions

def random_grid(level):
    # Generates a random question with multiple regions. Returns question, answer and the regions map
    all_regions = get_all_shapes()
    missings = [25,40,60]
    p = missings[level]/81
    grid = np.zeros((9,9)).astype(int)
    regions_map = np.zeros((9,9)).astype(int)
    region_no = 1
    while(grid.sum()<81):
        ch = np.random.choice(all_regions).copy()
        x,y=ch.shape
        available_options = fit_in(grid, ch)
        if len(available_options)==0:
            continue
        r,c = available_options[np.random.randint(0, len(available_options))]
        grid[r:r+x,c:c+y] = np.maximum(grid[r:r+x,c:c+y], ch)
        regions_map[r:r+x,c:c+y] = regions_map[r:r+x,c:c+y]+ (ch*region_no)
        region_no+=1

    num_regions = int(regions_map.max())
    for region_num in range(1, num_regions+1):
        region_boxes = list(zip(*np.where(regions_map==region_num)))
        np.random.shuffle(region_boxes)
        for idx,(i,j) in enumerate(region_boxes):
            grid[i,j]=idx+1

    qn = np.random.choice([0,1],(9,9),p=[p,1-p])
    qn = (grid*qn).astype(int)
    return qn, grid, regions_map

def get_v_borders(regions_map):
    # Returns the horizontal borders to be drawn on the board
    borders_h = np.ones((9,10)).astype(int)
    borders_h[:,[0,-1]]=5
    for row_num in range(9):
        for col_num in range(1,9):
            if regions_map[row_num,col_num]!=regions_map[row_num,col_num-1]:
                borders_h[row_num,col_num]=5
    return borders_h

def get_h_borders(regions_map):
    # Returns the vertical borders to be drawn on the board
    borders_v = np.ones((10,9)).astype(int)
    borders_v[[0,-1],:]=5
    for row_num in range(1,9):
        for col_num in range(9):
            if regions_map[row_num,col_num]!=regions_map[row_num-1,col_num]:
                borders_v[row_num,col_num]=5
    return borders_v

def evaluate(sol, regions_map):
    # Checks if the board is filled with valid values
    sol = np.array(sol)
    regions_map = np.array(regions_map)
    num_regions = int(regions_map.max())
    for region_num in range(1, num_regions+1):
        region_boxes = list(zip(*np.where(regions_map==region_num)))
        sol_region = sorted([sol[i,j] for i,j in region_boxes])
        exp_soln = list(range(1,len(region_boxes)+1))
        if exp_soln!=sol_region:
            print(exp_soln, sol_region)
            return False
    return True
