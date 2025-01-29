function [ u ] = UnicycleToPoseControl( xTrue,xGoal )
%Computes a control to reach a pose for unicycle
%   xTrue is the robot current pose : [ x y theta ]'
%   xGoal is the goal point
%   u is the control : [v omega]'

alpha = atan2(xGoal(2) - xTrue(2), xGoal(1) - xTrue(1)) - xTrue(3);
alpha = AngleWrap(alpha);
rho = sqrt((xGoal(1) - xTrue(1))^2 + (xGoal(2) - xTrue(2))^2);

Krho = 30;
Kalpha = 10;
Kbeta = 10;
alpha_max = pi/3;

v = Krho * rho;

if(rho > 0.05)

  omega = Kalpha * alpha;

  if(abs(alpha) > alpha_max)
    v = 0;
  end

else

  beta = xGoal(3) - xTrue(3);
  omega = Kbeta * beta;
  v = 0;

end

u = [v; omega];

end

