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

# parameters
showAnimation = False

class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None


class Rrt:
    def __init__(self, environment, s_start, s_goal, step_len, obs_corner_sample_rate, iter_max):
        self.s_start = Node(s_start)
        self.s_goal = Node(s_goal)
        self.step_len = step_len
        self.obs_corner_sample_rate = obs_corner_sample_rate
        self.goal_sample_rate = np.min((0.1, 1 - obs_corner_sample_rate))
        self.max_corner_dist = 3
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

        self.random_nodes = []

    def planning(self):
        iter_goal = None
        for i in range(self.iter_max):
            node_rand = self.generate_random_node(self.obs_corner_sample_rate)
            node_near = self.nearest_neighbor(self.vertex, node_rand)
            node_new = self.new_state(node_near, node_rand)

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
            return self.extract_path(node_goal), iter_goal

    def generate_random_node(self, obs_corner_sample_rate):

        rd_nb = np.random.random()

        if rd_nb < obs_corner_sample_rate:
            random_node = self.generate_random_node_from_obs_corner(self.max_corner_dist)

        elif rd_nb < obs_corner_sample_rate + self.goal_sample_rate:
            random_node = self.s_goal

        else:
            delta = self.utils.delta
            random_node = Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                    np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))
        
        if(not self.utils.is_inside_obs(random_node)):
            self.random_nodes.append(random_node)

        return random_node

    def generate_random_node_from_obs_corner(self, max_dist):

        delta = self.utils.delta
        x = None
        y = None

        # Select a random obstacle
        obs = self.env.obs_rectangle[np.random.randint(0, len(self.env.obs_rectangle))]

        # Define the range for x and y coordinates
        x_min = np.max((obs[0] - max_dist, self.x_range[0] + delta))
        x_max = np.min((obs[0] + obs[2] + max_dist, self.x_range[1] - delta))
        y_min = np.max((obs[1] - max_dist, self.y_range[0] + delta))
        y_max = np.min((obs[1] + obs[3] + max_dist, self.y_range[1] - delta))

        # Generate random coordinates within the defined range
        while x is None or self.utils.is_inside_obs(Node((x, y))):
            x = np.random.uniform(x_min, x_max)

            if x < obs[0] or x > obs[0] + obs[2]:
                y = np.random.uniform(y_min, y_max)
            else:
                y_top = np.random.uniform(obs[1] + obs[3], y_max)
                y_bottom = np.random.uniform(y_min, obs[1])
                y = np.random.choice([y_top, y_bottom])

        return Node((x, y))

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

    corner_rate_step = 0.10
    times_for_rate = 20

    success = [0 for i in np.arange(0.0, 1.00 + corner_rate_step, corner_rate_step)]

    for obs_corner_sample_rate in np.arange(0.0, 1.0, corner_rate_step):
        print('Rate : ' + str(obs_corner_sample_rate))
        for i in range(times_for_rate):

            x_start=(2, 2)  # Starting node
            x_goal=(49, 24)  # Goal node
            environment = env.Env2()

            rrt = Rrt(environment, x_start, x_goal, 2, obs_corner_sample_rate, 1500)
            path, nb_iter = rrt.planning()

            if path:
                # print('Found path in ' + str(nb_iter) + ' iterations, length : ' + str(get_path_length(path)))
                success[int(obs_corner_sample_rate/corner_rate_step)] += 1
                print(success[int(obs_corner_sample_rate/corner_rate_step)])
                if showAnimation:
                    rrt.plotting.animation(rrt.vertex, path, "RRT", True, rrt.random_nodes)
                    plotting.plt.show()
            else:
                # print("No Path Found in " + str(nb_iter) + " iterations!")
                if showAnimation:
                    rrt.plotting.animation(rrt.vertex, [], "RRT", True, rrt.random_nodes)
                    plotting.plt.show()

    plotting.plt.plot(np.arange(0.0, 1.0 + corner_rate_step, corner_rate_step), np.array(success)/20, color='red')
    plotting.plt.title("Success by new algorithm rate")
    plotting.plt.xlabel("Rate")
    plotting.plt.ylabel("Success")
    plotting.plt.show()


if __name__ == '__main__':
    main()
