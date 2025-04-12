import numpy as np
import matplotlib.pyplot as plt

L = 80
grid = np.zeros((L,L))
delta = 0.1
T = 0.2


# init grid
for i in range(L):
    for j in range(L):
        grid[i,j] = np.random.rand() * np.pi

# utils 
def display_grid():
    for i in range(L):
        for j in range(L):
            print(f"{grid[i,j]:.2f}", end=' ')
        print('')

# physics 
def computeEij(i,j):
    Eij = 0
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = (i + di ) % L, (j + dj ) % L 
        Eij += - (1.5 * np.cos( grid[i,j] - grid[ni, nj])**2 - 0.5)
    return Eij

def computeS():
    c = np.cos(2*grid)
    s = np.sin(2*grid)
    return np.sqrt( np.mean(c)**2 + np.mean(s)**2)


cycles = 200
S = 0
for cycle in range(cycles):
    print('cycle : ', cycle )
    for sweep in range(L**2):
        i,j = np.random.rand(2) * L
        i,j = int(i), int(j)

        x = grid[i,j]
        Ex = computeEij(i,j)
        grid[i,j] = (grid[i,j] + np.random.uniform(-delta, delta)) % np.pi
        ExPrime = computeEij(i,j)

        Paccept = np.exp(- (ExPrime - Ex)/T)
        if np.random.rand() > Paccept:
            grid[i,j] = x
        
        S += computeS()
Savg = S / ( L**2*cycles - int(0.2 * cycles * L**2) ) # 20% of cycles are used to equilibriate the system.
print(f"{Savg = :.3f}")

step = 2  # space between arrows
X, Y = np.meshgrid(np.arange(0, L, step), np.arange(0, L, step))
angles = grid[::step, ::step]
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        x0, y0 = X[i, j], Y[i, j]
        dx = 0.5 * np.cos(angles[i, j])
        dy = 0.5 * np.sin(angles[i, j])
        plt.plot([x0 - dx, x0 + dx], [y0 - dy, y0 + dy], color='black', lw=1)

plt.title(f"Finale configuration { Savg = :.2f}")
plt.axis('equal')
plt.axis('off')
plt.show()

plt.figure(figsize=(6, 6))
plt.imshow(grid, cmap='gray', origin='lower', extent=(0, L, 0, L))
plt.colorbar(label='Angle (rad)')
plt.title(f"Finale configuration { Savg = :.2f}")
plt.axis('equal')
plt.axis('off')
plt.show()