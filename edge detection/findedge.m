I=imread('testimage.jpg');
I=rgb2gray(I);


% Find x & y coordinates of the image
the_edge = edge(I);
[y, x] = find(the_edge);

% Get the total size of the image
[height, width] = size(I);

% Getting the change in y-coordinates:
y_min = y(1);
y_max = y(length(y));
y_delta = y_max - y_min;
% Getting the change in x-coordinates:
x_min = x(1)
x_max = x(length(x))
x_delta = x_max - x_min;

%Getting the angle value, because the displacement should be dependent on
%radius * angle (I think, double check me on this!)
radius = 1;

%In this case, we know x is the one that's changing. We're ignoring y for
%now

%I'm not sure if this is right. Basically I'm assuming 360 deg is enough
%for this stepper motor's change to cover the cake area thing.
encompassingangle = 360; 
fraction_to_multiply_angle_with = x_delta / width;

