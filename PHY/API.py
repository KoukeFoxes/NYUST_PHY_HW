import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

plt.switch_backend('agg')

class API():
    
    def __init__(self, 
                 drag_coefficient : float,
                 projectile_radius : float,
                 mass : float,
                 air_density : float,
                 gravity_acceleration : float,
                 initial_speed : float,
                 launch_angle : float,
                 clear_rander = False):
        
        if clear_rander:
            plt.close()
        
        # Drag coefficient, projectile radius (m), area (m2) and mass (kg).
        c = drag_coefficient
        r = projectile_radius
        A = np.pi * r**2
        m = mass
        # Air density (kg.m-3), acceleration due to gravity (m.s-2).
        rho_air = air_density
        g = gravity_acceleration
        # For convenience, define  this constant.
        k = 0.5 * c * rho_air * A

        # Initial speed and launch angle (from the horizontal).
        v0 = initial_speed
        phi0 = np.radians(launch_angle)

        def deriv(t, u):
            x, xdot, z, zdot = u
            speed = np.hypot(xdot, zdot)
            xdotdot = -k/m * speed * xdot
            zdotdot = -k/m * speed * zdot - g
            return xdot, xdotdot, zdot, zdotdot

        # Initial conditions: x0, v0_x, z0, v0_z.
        u0 = 0, v0 * np.cos(phi0), 0., v0 * np.sin(phi0)
        # Integrate up to tf unless we hit the target sooner.
        t0, tf = 0, 50

        def hit_target(t, u):
            # We've hit the target if the z-coordinate is 0.
            return u[2]
        # Stop the integration when we hit the target.
        hit_target.terminal = True
        # We must be moving downwards (don't stop before we begin moving upwards!)
        hit_target.direction = -1

        def max_height(t, u):
            # The maximum height is obtained when the z-velocity is zero.
            return u[3]

        self.soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True,
                        events=(hit_target, max_height))
        # print(soln)
        # print('Time to target = {:.2f} s'.format(soln.t_events[0][0]))
        # print('Time to highest point = {:.2f} s'.format(soln.t_events[1][0]))

        # A fine grid of time points from 0 until impact time.
        t = np.linspace(0, self.soln.t_events[0][0], 100)

        # Retrieve the solution for the time grid and plot the trajectory.
        self.sol = self.soln.sol(t)
        x, z = self.sol[0], self.sol[2]
        # print('Range to target, xmax = {:.2f} m'.format(x[-1]))
        # print('Maximum height, zmax = {:.2f} m'.format(max(z)))
        plt.plot(x, z)
        plt.xlabel('x /m')
        plt.ylabel('z /m')
        # plt.show()
        
        
    def get_solution(self):
        return self.sol

    def get_MaxHeight(self):
        return max(self.sol[2])
    
    def get_length(self):
        return self.sol[0][-1]
    
    def getTime2HeightPoints(self):
        return self.soln.t_events[1][0]
    
    def getTime2Ground(self):
        return self.soln.t_events[0][0]
      
    def getFig(self):
        return plt   
    
if __name__ == '__main__':
    a = API()
    print('Maximum height, zmax = {:.2f} m'.format(a.get_MaxHeight()))
    print('Range to target, xmax = {:.2f} m'.format(a.get_length()))
    print('Time to target = {:.2f} s'.format(a.getTime2Ground()))
    print('Time to highest point = {:.2f} s'.format(a.getTime2HeightPoints()))
    