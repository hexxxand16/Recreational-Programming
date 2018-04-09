clc;clear
X = csvread('sevens.csv');
X(X(:,end)==0,end) = -1;
X = X(randperm(length(X)),:); %ramdomises data
Y = X(:,end);
P = X(901:1000, 1:52);
P_y = Y(901:1000);
X = X(1:900,1:52);
w = zeros(1, 52);
for i = 1:1000
    sum = 0;
    for j = 1:length(X)
        if Y(j) * (w * X(j,:)') <= 0
            sum = sum + Y(j) * X(j,:);
        end
    end
    w = w + 0.01 * sum;
end

test = sign(P * w');
clear sum
error = sum(P_y ~= test)/length(P); %finds error
