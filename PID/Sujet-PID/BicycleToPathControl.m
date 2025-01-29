function [ u ] = BicycleToPathControl( xTrue, Path )
%Computes a control to follow a path for bicycle
%   xTrue is the robot current pose : [ x y theta ]'
%   Path is set of points defining the path : [ x1 x2 ... ;
%                                               y1 y2 ...]
%   u is the control : [v phi]'


% Store the current goal and step along the path
persistent current_goal;
persistent current_step;

% Initialize the current goal and step
if isempty(current_goal)
  current_goal = Path(:,1);
  current_step = 2;
end

% Distance from the current robot position to the current goal
distance = sqrt((current_goal(1) - xTrue(1))^2 + (current_goal(2) - xTrue(2))^2);

% If the robot is close enough to the current goal update the goal
if(distance < 0.3)
  [current_goal, current_step] = UpdateGoal(xTrue, current_goal, current_step, Path);
end

% Compute the control inputs to reach the current goal
u = BicycleToPointControl(xTrue, current_goal);

end


function [goal, step] = UpdateGoal( xTrue, current_goal, current_step, Path )

% Calculate the direction vector of the current path segment
current_line_start = Path(:, current_step - 1);
current_line_end = Path(:, current_step);
line_length = sqrt((current_line_start(1) - current_line_end(1))^2 + (current_line_start(2) - current_line_end(2))^2);
current_dir = (current_line_end - current_line_start) / line_length;

% New goal point along the current path segment
step_size = 0.3;
goal = current_goal + step_size * current_dir;

% If the robot is close enough to the current segment's end, update the goal
distance_to_line_end = sqrt((current_line_end(1) - goal(1))^2 + (current_line_end(2) - goal(2))^2);
if(distance_to_line_end < 0.3 && current_step ~= size(Path, 2))
  goal = current_line_end;  % Set the goal to the segment's end
  current_step = current_step + 1;  % Move to the next path segment
end

step = current_step;

end


