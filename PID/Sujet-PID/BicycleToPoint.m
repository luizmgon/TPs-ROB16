function BicycleToPoint
% Display Bicycle Control Behavior from random position to [0;0]

% Goal and random starting position
xGoal = [0;0;0];
a=rand()*2*pi;
xTrue = [cos(a);sin(a);rand()*2*pi];

%Storage for position and errors
XStore = NaN*zeros(3,2000);
XErrStore = NaN*zeros(5,2000);
k=1;

% loop until goal reached or max time
while max(abs(dist(xTrue(1:2,1),xGoal(1:2,1))))>.005 && k<10000

    % Compute Control
    u=BicycleToPointControl(xTrue,xGoal);

    % Simulate Vehicle motion
    [xTrue,u] = SimulateBicycle(xTrue,u);

    k=k+1;
    %store results:
    XErrStore(:,k) = [dist(xTrue,xGoal);u(1);u(2)];
    XStore(:,k) = xTrue;

    % plot every 100 updates
    if(mod(k-2,100)==0)
        DoBicycleGraphics(xTrue,XStore,XErrStore);
        drawnow;
    end;

end;

% Draw final position and error curves
DoBicycleGraphics(xTrue,XStore,XErrStore);
drawnow;
figure(2);
subplot(4,1,1);plot(XErrStore(1,:));
title('Error');ylabel('x');
subplot(4,1,2);plot(XErrStore(2,:));
ylabel('y');
subplot(4,1,3);plot(XErrStore(4,:));
title('Controls');ylabel('v');
subplot(4,1,4);plot(XErrStore(5,:)*180/pi);
ylabel('\phi');xlabel('time');




