% Make the plots for problem #3
% CSE 6140 homework #3
% Dylan Crocker 20150920

close all; clear all; clc;

%% Read in the files

dat0406 = dlmread('results/rmat0406_output.txt');
dat0507 = dlmread('results/rmat0507_output.txt');
dat0608 = dlmread('results/rmat0608_output.txt');
dat0709 = dlmread('results/rmat0709_output.txt');
dat0810 = dlmread('results/rmat0810_output.txt');
dat0911 = dlmread('results/rmat0911_output.txt');
dat1012 = dlmread('results/rmat1012_output.txt');
dat1113 = dlmread('results/rmat1113_output.txt');
dat1214 = dlmread('results/rmat1214_output.txt');
dat1315 = dlmread('results/rmat1315_output.txt');
dat1416 = dlmread('results/rmat1416_output.txt');
dat1517 = dlmread('results/rmat1517_output.txt');
% dat1618 = dlmread('results/rmat1618_output.txt');

% dat0406x = dlmread('results_networkx/rmat0406_output.txt');
% dat0507x = dlmread('results_networkx/rmat0507_output.txt');
% dat0608x = dlmread('results_networkx/rmat0608_output.txt');
% dat0709x = dlmread('results_networkx/rmat0709_output.txt');
% dat0810x = dlmread('results_networkx/rmat0810_output.txt');
% dat0911x = dlmread('results_networkx/rmat0911_output.txt');
% dat1012x = dlmread('results_networkx/rmat1012_output.txt');
% dat1113x = dlmread('results_networkx/rmat1113_output.txt');
% dat1214x = dlmread('results_networkx/rmat1214_output.txt');
% dat1315x = dlmread('results_networkx/rmat1315_output.txt');
% dat1416x = dlmread('results_networkx/rmat1416_output.txt');
% dat1517x = dlmread('results_networkx/rmat1517_output.txt');
% dat1618x = dlmread('results_networkx/rmat1618_output.txt');

%% Process Data

% Static computation times
static_times = [dat0406(1,2) dat0507(1,2) dat0608(1,2) dat0709(1,2) ...
                dat0810(1,2) dat0911(1,2) dat1012(1,2) dat1113(1,2) ...
                dat1214(1,2) dat1315(1,2) dat1416(1,2) dat1517(1,2) ...
%                 dat1618(1,2)];
];

% Dynamic computation times
dynamic_times = [sum(dat0406(:,2)) sum(dat0507(:,2)) sum(dat0608(:,2)) ...
                 sum(dat0709(:,2)) sum(dat0810(:,2)) sum(dat0911(:,2)) ...
                 sum(dat1012(:,2)) sum(dat1113(:,2)) sum(dat1214(:,2)) ...
                 sum(dat1315(:,2)) sum(dat1416(:,2)) sum(dat1517(:,2)) ...
%                  sum(dat1618(:,2))];
];

graph_edges = [64 128 259 530 1054 2183 4411 9875 29779 106361 372670 1770677]; % 7926934];
graph_nodes = [16 32 64 128 256 512 1024 2048 4096 8192 16384 32768];

%% Plot results

c = .001;

figure()
set(gcf,'defaultlinelinewidth',3)
loglog(graph_edges, static_times)
hold all
loglog(graph_edges, c*graph_edges.*log(graph_nodes))
title('Static MST Computation Times','FontSize',14)
xlabel('Graph size (Number of Edges)','FontSize',14)
ylabel('Computation Time (ms)','FontSize',14)
legend('Measured','O(m*log(n))','Location','SouthEast')
grid on

c = 4;

figure()
set(gcf,'defaultlinelinewidth',3)
loglog(graph_edges, dynamic_times)
hold all
loglog(graph_edges, c*graph_edges)
title('Dynamic MST Computation Times','FontSize',14)
xlabel('Graph size (Number of Edges)','FontSize',14)
ylabel('Computation Time (ms)','FontSize',14)
legend('Measured','O(m)','Location','SouthEast')
grid on

% Comparison Plots
