"""
RRT_2D
@author: huiming zhou

Modified by David Filliat
"""
import os
import sys
import math
import numpy as np
import plotting, utils, queue
import env
import time

# parameters
showAnimation = False

class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None


class RrtStar:
    def __init__(self, env, x_start, x_goal, step_len,
                 goal_sample_rate, search_radius, iter_max):
        self.s_start = Node(x_start)
        self.s_goal = Node(x_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.search_radius = search_radius
        self.iter_max = iter_max
        self.vertex = [self.s_start]
        self.path = []

        self.env = env
        if showAnimation:
            self.plotting = plotting.Plotting(self.env, x_start, x_goal)
        self.utils = utils.Utils(self.env)

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def planning(self):
        iter_goal = None
        for k in range(self.iter_max):
            node_rand = self.generate_random_node(self.goal_sample_rate)
            node_near = self.nearest_neighbor(self.vertex, node_rand)
            node_new = self.new_state(node_near, node_rand)

            # index = self.search_goal_parent()
            # if index != (len(self.vertex) - 1) and iter_goal == None:
            #     iter_goal = k

            if showAnimation and k % 50 == 0:
                if index != (len(self.vertex) - 1):
                    self.path = self.extract_path(self.vertex[index])
                else:
                    self.path = []
                self.plotting.animation(self.vertex, self.path, "rrt*, N = " + str(k),False)

            if node_new and not self.utils.is_collision(node_near, node_new):
                neighbor_index = self.find_near_neighbor(node_new)
                self.vertex.append(node_new)

                if neighbor_index:
                    self.choose_parent(node_new, neighbor_index)
                    self.rewire(node_new, neighbor_index)

        index = self.search_goal_parent()

        if index != (len(self.vertex) - 1):
            self.path = self.extract_path(self.vertex[index])
        else:
            self.path = []
            iter_goal = self.iter_max

        return self.path, iter_goal

    def new_state(self, node_start, node_goal):
        dist, theta = self.get_distance_and_angle(node_start, node_goal)

        dist = min(self.step_len, dist)
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))

        node_new.parent = node_start

        return node_new

    def choose_parent(self, node_new, neighbor_index):
        cost = [self.get_new_cost(self.vertex[i], node_new) for i in neighbor_index]

        cost_min_index = neighbor_index[int(np.argmin(cost))]
        node_new.parent = self.vertex[cost_min_index]

    def rewire(self, node_new, neighbor_index):
        for i in neighbor_index:
            node_neighbor = self.vertex[i]

            if self.cost(node_neighbor) > self.get_new_cost(node_new, node_neighbor):
                node_neighbor.parent = node_new

    def search_goal_parent(self):
        dist_list = [math.hypot(n.x - self.s_goal.x, n.y - self.s_goal.y) for n in self.vertex]
        node_index = [i for i in range(len(dist_list)) if dist_list[i] <= self.step_len]
        if len(node_index) > 0:
            cost_list = [dist_list[i] + self.cost(self.vertex[i]) for i in node_index
                         if not self.utils.is_collision(self.vertex[i], self.s_goal)]
            id_list = [i for i in node_index
                         if not self.utils.is_collision(self.vertex[i], self.s_goal)]

            if len(cost_list)> 0:
                id = id_list[int(np.argmin(cost_list))]
                #print('Found path, length : ' + str(min(cost_list)))
                return id

        return len(self.vertex) - 1

    def get_new_cost(self, node_start, node_end):
        dist, _ = self.get_distance_and_angle(node_start, node_end)

        return self.cost(node_start) + dist

    def generate_random_node(self, goal_sample_rate):
        delta = self.utils.delta

        if np.random.random() > goal_sample_rate:
            return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))

        return self.s_goal

    def find_near_neighbor(self, node_new):
        n = len(self.vertex) + 1
        r = min(self.search_radius * math.sqrt((math.log(n) / n)), self.step_len)

        dist_table = [math.hypot(nd.x - node_new.x, nd.y - node_new.y) for nd in self.vertex]
        dist_table_index = [ind for ind in range(len(dist_table)) if dist_table[ind] <= r and
                            not self.utils.is_collision(node_new, self.vertex[ind])]

        return dist_table_index

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    @staticmethod
    def cost(node_p):
        node = node_p
        cost = 0.0

        while node.parent:
            cost += math.hypot(node.x - node.parent.x, node.y - node.parent.y)
            node = node.parent

        return cost

    def update_cost(self, parent_node):
        OPEN = queue.QueueFIFO()
        OPEN.put(parent_node)

        while not OPEN.empty():
            node = OPEN.get()

            if len(node.child) == 0:
                continue

            for node_c in node.child:
                node_c.Cost = self.get_new_cost(node, node_c)
                OPEN.put(node_c)

    def extract_path(self, node_end):
        path = [[self.s_goal.x, self.s_goal.y]]
        node = node_end

        while node.parent is not None:
            path.append([node.x, node.y])
            node = node.parent
        path.append([node.x, node.y])

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
        length += np.linalg.norm(np.array(i) - np.array(k)) #math.dist(i,k)
    return length


def main():

    n_iters = 3000
    step_iter = 250
    lenghts = []
    times = []

    times_per_max_iteration = 3

    for iter in range(0, n_iters, step_iter):
        avg_length = 0
        n_success = 0
        avg_time = 0

        for i in range(times_per_max_iteration):
            print("Iteration: ", iter, " - ", i)

            x_start = (2, 2)  # Starting node
            x_goal = (49, 24)  # Goal node
            environment = env.Env()

            rrt_star = RrtStar(environment, x_start, x_goal, 2, 0.10, 20, iter)

            start_time = time.time()
            path, nb_iter = rrt_star.planning()
            end_time = time.time()

            avg_time += (end_time - start_time) / times_per_max_iteration

            if path:
               avg_length += get_path_length(path)
               n_success += 1

        if n_success:   lenghts.append(avg_length / n_success)
        else:    lenghts.append(None)

        times.append(avg_time)
        print(n_success)


    plotting.plt.plot(range(0, n_iters, step_iter), lenghts, color='red')
    plotting.plt.xlabel('Iterations')
    plotting.plt.ylabel('Path Length')
    plotting.plt.title('Path Length vs Iterations (RRT)')
    plotting.plt.xlim(xmin=0)
    plotting.plt.ylim(ymin=0)


    plotting.plt.figure()
    plotting.plt.plot(range(0, n_iters, step_iter), times, color='blue')
    plotting.plt.xlabel('Iterations')
    plotting.plt.ylabel('Time (s)')
    plotting.plt.title('Time vs Iterations (RRT)')
    plotting.plt.xlim(xmin=0)
    plotting.plt.ylim(ymin=0)


    plotting.plt.show()


if __name__ == '__main__':
    main()
