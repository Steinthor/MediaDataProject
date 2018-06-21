%% SIFT 

clear all;
load('f1_sift_02.csv')
load('p_sift_02.csv')

Tr = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7];
Tc = [1,2,3,6,7,8,9,10,11,12,13,14,15,16];
[m,i] = max(f1_sift_02);
[mm,ii]=max(m);
[n,j] = max(p_sift_02);
[nn,jj]=max(n);
subplot(1,2,1)
surf(Tc,Tr,f1_sift_02)
title('SIFT F1')
xlabel('Tc')
ylabel('Tr')
zlabel('F1')
hold on
plot3(Tc(ii),Tr(i(ii)),mm,'r.','MarkerSize', 20);
hold off
subplot(1,2,2)
surf(Tc,Tr,p_sift_02)
title('SIFT precision')
xlabel('Tc')
ylabel('Tr')
zlabel('p')
hold on
plot3(Tc(jj),Tr(j(jj)),nn,'r.','MarkerSize', 20);
hold off


%% SURF
clear all;
load('f1_surf_02.csv')
load('p_surf_02.csv')

Tr = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7];
Tc = [1,2,3,6,7,8,9,10,11,12,13,14,15,16];
[m,i] = max(f1_surf_02);
[mm,ii]=max(m);
[n,j] = max(p_surf_02);
[nn,jj]=max(n);
subplot(1,2,1)
surf(Tc,Tr,f1_surf_02)
title('SURF F1')
xlabel('Tc')
ylabel('Tr')
zlabel('F1')
hold on
plot3(Tc(ii),Tr(i(ii)),mm,'r.','MarkerSize', 20);
hold off
subplot(1,2,2)
surf(Tc,Tr,p_surf_02)
title('SURF precision')
xlabel('Tc')
ylabel('Tr')
zlabel('p')
hold on
plot3(Tc(jj),Tr(j(jj)),nn,'r.','MarkerSize', 20);
hold off

%% BRISK
clear all;
load('f1_brisk_02.csv')
load('p_brisk_02.csv')

Tr = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7];
Tc = [1,2,3,6,7,8,9,10,11,12,13,14,15,16];
[m,i] = max(f1_brisk_02);
[mm,ii]=max(m);
[n,j] = max(p_brisk_02);
[nn,jj]=max(n);
subplot(1,2,1)
surf(Tc,Tr,f1_brisk_02)
title('BRISK F1')
xlabel('Tc')
ylabel('Tr')
zlabel('F1')
hold on
plot3(Tc(ii),Tr(i(ii)),mm,'r.','MarkerSize', 20);
hold off
subplot(1,2,2)
surf(Tc,Tr,p_brisk_02)
title('BRISK precision')
xlabel('Tc')
ylabel('Tr')
zlabel('p')
hold on
plot3(Tc(jj),Tr(j(jj)),nn,'r.','MarkerSize', 20);
hold off

%% ORB
clear all;
load('f1_orb_02.csv')
load('p_orb_02.csv')

Tr = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7];
Tc = [1,2,3,6,7,8,9,10,11,12,13,14,15,16];
[m,i] = max(f1_orb_02);
[mm,ii]=max(m);
[n,j] = max(p_orb_02);
[nn,jj]=max(n);
subplot(1,2,1)
surf(Tc,Tr,f1_orb_02)
title('ORB F1')
xlabel('Tc')
ylabel('Tr')
zlabel('F1')
hold on
plot3(Tc(ii),Tr(i(ii)),mm,'r.','MarkerSize', 20);
hold off
subplot(1,2,2)
surf(Tc,Tr,p_orb_02)
title('ORB precision')
xlabel('Tc')
ylabel('Tr')
zlabel('p')
hold on
plot3(Tc(jj),Tr(j(jj)),nn,'r.','MarkerSize', 20);
hold off
