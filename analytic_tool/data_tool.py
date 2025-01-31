import numpy as np
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')  # Initialize 3D axes

    def plot_movement(self, player1spacetime, player2spacetime, stored_data1=None, stored_data2=None):
        if stored_data1 is None:
            stored_data1 = []
        if stored_data2 is None:
            stored_data2 = []
        x1, y1, z1 = player1spacetime[0], player1spacetime[1], player1spacetime[2]

        self.ax.scatter(x1, y1, z1, c='b', marker='o', label='Player 1')

        x2, y2, z2 = player2spacetime[0], player2spacetime[1], player2spacetime[2]

        self.ax.scatter(x2, y2, z2, c='r', marker='o', label='Player 2')

        self.ax.set_xlabel('Position X')
        self.ax.set_ylabel('Position Y')
        self.ax.set_zlabel('Time')

        self.ax.legend()

        return stored_data1, stored_data2

    def draw(self):
        plt.show()


if __name__ == "__main__":
    data1 = [1, 4, 12]  # Player 1's spacetime data (x, y, time)
    data2 = [1, 7, 16]  # Player 2's spacetime data (x, y, time)

    # Create an instance of the Plotter class
    plot = Plotter()

    # Plot the movement
    plot.plot_movement(player1spacetime=data1, player2spacetime=data2)

    # Display the plot
    plot.draw()