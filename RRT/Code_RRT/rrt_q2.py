"""
RRT_2D
@author: huiming zhou

Modified by David Filliat
"""

import os
import sys
import math
import numpy as np
import plotting, utils
import env
import time

# parameters
showAnimation = False

class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None


class Rrt:
    def __init__(self, environment, s_start, s_goal, step_len, goal_sample_rate, iter_max):
        self.s_start = Node(s_start)
        self.s_goal = Node(s_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.iter_max = iter_max
        self.vertex = [self.s_start]

        self.env = environment
        if showAnimation:
            self.plotting = plotting.Plotting(self.env, s_start, s_goal)
        self.utils = utils.Utils(self.env)

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def planning(self):
        iter_goal = None
        collisions = 0
        for i in range(self.iter_max):
            node_rand = self.generate_random_node(self.goal_sample_rate)
            node_near = self.nearest_neighbor(self.vertex, node_rand)
            node_new = self.new_state(node_near, node_rand)

            if self.utils.is_collision(node_near, node_new):
                collisions += 1

            if node_new and not self.utils.is_collision(node_near, node_new):
                self.vertex.append(node_new)
                dist, _ = self.get_distance_and_angle(node_new, self.s_goal)

                if dist <= self.step_len and iter_goal == None and not self.utils.is_collision(node_new, self.s_goal):
                    node_new = self.new_state(node_new, self.s_goal)
                    node_goal = node_new
                    iter_goal = i

        if iter_goal == None:
            return None, self.iter_max
        else:
            return self.extract_path(node_goal), iter_goal, collisions

    def generate_random_node(self, goal_sample_rate):
        if np.random.random() < goal_sample_rate:
            return self.s_goal

        delta = self.utils.delta

        return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                    np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))


    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)

        dist = min(self.step_len, dist)
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))
        node_new.parent = node_start

        return node_new

    def extract_path(self, node_end):
        path = [(self.s_goal.x, self.s_goal.y)]
        node_now = node_end

        while node_now.parent is not None:
            node_now = node_now.parent
            path.append((node_now.x, node_now.y))

        return path

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)


def get_path_length(path):
    """
    Compute path length
    """
    length = 0
    for i,k in zip(path[0::], path[1::]):
        length += np.linalg.norm(np.array(i) - np.array(k)) # math.dist(i,k)
    return length


def main():

    list_collisions = []
    needed_iters = []

    steps = [1, 2, 5, 10, 20, 30, 50]

    times_per_stepsize = 10
    
    for step in steps:
        avg_collisions = 0
        avg_needed_iters = 0
        
        for i in range(times_per_stepsize):
            print("Iteration: ", step, " - ", i)

            x_start=(2, 2)  # Starting node
            x_goal=(49, 24)  # Goal node
            environment = env.Env()

            rrt = Rrt(environment, x_start, x_goal, step, 0.10, 2000)

            path, nb_iter, collisions = rrt.planning()

            if path:
                avg_collisions += collisions/times_per_stepsize
                avg_needed_iters += nb_iter/times_per_stepsize
                if showAnimation:
                    rrt.plotting.animation(rrt.vertex, path, "RRT", True)
                    plotting.plt.show()
        list_collisions.append(avg_collisions)
        needed_iters.append(avg_needed_iters)
        
    plotting.plt.plot(steps, list_collisions, color='red')
    plotting.plt.xlabel('Step Size')
    plotting.plt.ylabel('Collisions')
    plotting.plt.title('Collisions vs Step Size (RRT)')
    plotting.plt.xlim(xmin=0)
    plotting.plt.ylim(ymin=0)

    plotting.plt.figure()
    plotting.plt.plot(steps, needed_iters, color='blue')
    plotting.plt.xlabel('Step Size')
    plotting.plt.ylabel('Iterations to find path')
    plotting.plt.title('Step Size vs Iterations to find path (RRT)')
    plotting.plt.xlim(xmin=0)
    plotting.plt.ylim(ymin=0)

    plotting.plt.show()



if __name__ == '__main__':
    main()
