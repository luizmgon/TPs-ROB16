function [ u ] = BicycleToPointControl( xTrue,xGoal )
%Computes a control to reach a pose for bicycle
%   xTrue is the robot current pose : [ x y theta ]'
%   xGoal is the goal point
%   u is the control : [v phi]'


alpha = atan2(xGoal(2) - xTrue(2), xGoal(1) - xTrue(1)) - xTrue(3);
alpha = AngleWrap(alpha);
rho = sqrt((xGoal(1) - xTrue(1))^2 + (xGoal(2) - xTrue(2))^2);

Krho = 30;
Kalpha = 5;

v = Krho * rho;
phi = Kalpha * alpha;

u = [v; phi];

end

