%\Two class 
X=randn(100,2);
Y=randn(100,2);
C1=[2 1;1 2];
C2=[1 0;0 1];
A=chol(C1);
B=chol(C2);
X1=X*A;
Y1=Y*B;
m1=[0 3];m2=[2 1];
N=100;
X2=X1+kron(ones(N,1),m1);
Y2=Y1+kron(ones(N,1),m2);
X=[X2;Y2];
y=[ones(N,1);-ones(N,1)];
figure(1)
plot(X2(:,1),X2(:,2),'c.',Y2(:,1),Y2(:,2),'mx');
hold on
net = feedforwardnet(20);%one hidden layer with 20 neurons and an output layer
net = train(net, X', y');
[output] = net(X');
figure(2)
title('Evaluate the network output','FontSize',18);
bar(output);
hold on;

%Evaluate the network output on a regular grid, and plot the decision contour. How well does
% it compare with the Bayes' optimal boundary? Compare the approximation at two different
% sizes of the network.???

%draw the contour
% % numGrid = 50;
% % xRange = linspace(-4.0, 6.0, numGrid);
% % yRange = linspace(-4.0, 6.0, numGrid);
% % P1 = zeros(numGrid, numGrid);
% % P2 = P1;
% % for i=1:numGrid
% % for j=1:numGrid;
% % x = [xRange(i) yRange(j)]';
% % P(i,j) = net(x);
% % end
% % end
% % figure(1)
% % contour(xRange, yRange, P, [0 0], 'LineWidth', 2);
% % hold on

%Bayes contour
% % numGrid = 50;
% % xRange = linspace(-4.0, 6.0, numGrid);
% % yRange = linspace(-4.0, 6.0, numGrid);
% % P1 = zeros(numGrid, numGrid);
% % P2 = P1;
% % for i=1:numGrid
% % for j=1:numGrid;
% % x = [xRange(i) yRange(j)];
% % P(i,j) = mvnpdf(x,m1,C1)-mvnpdf(x,m2,C2);
% % end
% % end
% % figure(1)
% % contour(xRange, yRange, P, [0 0], 'LineWidth', 2);
% % hold on

%Compare the approximation
%approximation of feedforwardnet
    nCorrect=0;
for i=1:200;
    if(output(1,i)*y(i,1)>0)
        nCorrect=nCorrect+1;
    end
end
pCorrect=nCorrect/200;
disp(['feedforward neronet accuracy: ' num2str(pCorrect)]);

%approximation of Bayes' optimal boundary
outputBayes=ones(N,1);
for i=1:200;
    if(mvnpdf([X(i,1),X(i,2)],m1,C1)>mvnpdf([X(i,1),X(i,2)],m2,C2));
        outputBayes(i,1)=1;
    else
        outputBayes(i,1)=-1;
    end
end

   nCorrect=0;
for i=1:200;
    if(outputBayes(i,1)*y(i,1)>0)
        nCorrect=nCorrect+1;
    end
end
pCorrect=nCorrect/200;
disp(['Bayes optimal boundary accuracy: ' num2str(pCorrect)]);

        