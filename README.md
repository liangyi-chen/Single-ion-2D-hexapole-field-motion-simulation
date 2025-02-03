# Single Ion 2D Hexapole Field Motion Simulation

This is a simple Python program with Tkinter UI that simulates the motion of a charged particle in a hexapole RF field. With the input parameters, the program can output the trajectory in the 2D plane of the particle's motion. The calculation is done in 2nd-order Runge-Kutta method.

The parameters include:

- V0: The peak voltage of the RF field.
- omega: The angular frequency of the RF field.
- x0: The starting x position of the particle.
- y0: The starting y position of the particle.
- q: The charge of the particle.
- m: The mass of the particle.
- h: The step size.
- vx0: The x component of the initial velocity of the particle.
- vy0: The y component of the initial velocity of the particle.
- Endtime: The length of the simulation.

The amounts are unitless, so the simulation results are qualitative, not quantitative.
