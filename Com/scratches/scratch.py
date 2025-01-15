%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%这是第二次作业的框架代码，在此作业中你将构建一个
2
D - FDTD
代码来模拟天线阵列的波束成形。
%%%代码的大部分已经完成。需要你完成的部分已被标记出来。
%%%没有必要完全遵循这个框架。请注意，构建
2
D - FDTD
代码有很多种方法。如果你决定使用你自己的代码结构，你不会因此丢分。
%%%请在代码中添加详细的注释。
%%%如果对第二次作业和此代码有任何问题，请发送电子邮件至
l.guo3 @ uq.edu.au。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc
clear

beamforming_angle = pi / 6; %这是波束成形角度。请注意角度是以弧度为单位。该角度的范围可以从 - pi / 3
到
pi / 3。
show_wave = 1; %这是一个显示
FDTD
仿真结果的标志。show_wave = 1
表示代码将在
FDTD
仿真期间显示波传播；show_wave = 0
表示代码不会显示波传播。请注意，在
FDTD
仿真过程中显示波传播会使代码运行时间更长。

dx = 1e-3; %x
方向上的网格大小
dy = 1e-3; %y
方向上的网格大小

%%%初始化电磁常数
freq = 20e9; %信号的频率
w = 2 * pi * freq; %信号的角频率
eps_o = 8.854187817e-12; %真空中的介电常数
u_o = 4 * pi * 1e-7; %真空中的磁导率
eps_r_b = 1; %真空中的相对介电常数
sigma_b = 0; %真空中的导电率
eps_b = eps_r_b * eps_o; %背景介质的介电常数（在我们的作业中，背景介质是自由空间）
c = 1 / sqrt(u_o * eps_o); %光速
lambda = c / freq; %自由空间中波的波长
       ant_Tx_N = 25; %发送天线元件的数量
       ant_Rx_N = 55; %接收天线元件的数量

       Lx = 500e-3; %这是整个 FDTD 计算区域的尺寸
       Ly = 500e-3; %这是整个 FDTD 计算区域的尺寸

       x_dash =[-250e-3 + dx: dx: 250e-3]; %定义
x
方向上的网格坐标
y_dash = [-250e-3 + dx: dy: 250e-3]; %定义
y
方向上的网格坐标
[Axis_x, Axis_y] = ndgrid(x_dash, y_dash); %定义包含
x
和
y
方向网格坐标的矩阵

Nx = Ly / dy; %磁场在整个
FDTD
区域的网格数量
Ny = Lx / dx; %磁场在整个
FDTD
区域的网格数量
Nx1 = Ly / dy + 1; %电场在整个
FDTD
区域的网格数量（电场因为半网格位移多了一个网格）
Ny1 = Lx / dx + 1; %电场在整个
FDTD
区域的网格数量
dt = dx / (c * sqrt(2)); %选择正确的时间步长（参考方程(4.60
a)，但这是用于
3
D
情况）
FS = 1 / dt; %傅里叶变换的采样频率
Nt = 5000; %FDTD
中计算的时间步数

t_array = [0: dt: (Nt - 1) * dt]; %定义一个数组，用于存放不同的时间实例

%%%------------------ 初始化整个
FDTD
计算区域内的电气特性（介电常数和导电率，不包括
PML） --------------------- %%%

eps_z = eps_r_b. * eps_o. * ones(Nx1, Ny1); %为仿真域分配介电常数

sigma_ez = zeros(Nx1, Ny1) + sigma_b; %为仿真域中的
Ez
分量分配导电率
sigma_mx = zeros(Nx1, Ny); %为仿真域中的
Hx
分量分配导电率
sigma_my = zeros(Nx, Ny1); %为仿真域中的
Hy
分量分配导电率

%%%----------------------------------------- 定义
Tx（发送天线）和
Rx（接收天线）的位置 - ---------------------------------------------- %%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%定义
Tx %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Probes_Tx = zeros(ant_Tx_N, 2); %数组存储
Tx
天线的坐标
source_X_Tx = zeros(ant_Tx_N, 1); %数组存储
Tx
天线的网格索引（x
方向）
source_Y_Tx = zeros(ant_Tx_N, 1); %数组存储
Tx
天线的网格索引（y
方向）
for nn = 1: ant_Tx_N
Probes_Tx(nn, 1) = -90e-3 + (nn - 1) * (lambda / 2);
Probes_Tx(nn, 2) = 180e-3;

dis_source_x = abs(Probes_Tx(nn, 1) - x_dash);
[~, source_X_Tx(nn)] = min(dis_source_x);
dis_source_y = abs(Probes_Tx(nn, 2) - y_dash);
[~, source_Y_Tx(nn)] = min(dis_source_y);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%定义
Rx %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Probes_Rx = zeros(ant_Rx_N, 2); %数组存储
Rx
天线的坐标
source_X_Rx = zeros(ant_Rx_N, 1); %数组存储
Rx
天线的网格索引（x
方向）
source_Y_Rx = zeros(ant_Rx_N, 1); %数组存储
Rx
天线的网格索引（y
方向）
for nn = 1: ant_Rx_N
Probes_Rx(nn, 1) = -200e-3 + (nn - 1) * (lambda / 2);
Probes_Rx(nn, 2) = -180e-3;

dis_source_x = abs(Probes_Rx(nn, 1) - x_dash);
[~, source_X_Rx(nn)] = min(dis_source_x);
dis_source_y = abs(Probes_Rx(nn, 2) - y_dash);
[~, source_Y_Rx(nn)] = min(dis_source_y);
end

%%%----------------------------------------------------------------------------------------------------------------------- %%%

%%%真空中的磁导率为
uo
ux = ones(Nx1, Ny);
ux = ux. * u_o;
uy = ones(Nx, Ny1);
uy = uy. * u_o;

%%%----------------------------------- 初始化整个
FDTD
计算区域内的系数（不考虑
PML） --------------------------------- %%%
%%%初始化用于更新
Ez
的
FDTD
系数
Ceze = (2 * eps_z - dt * sigma_ez). / (2 * eps_z + dt * sigma_ez);
Cezhy = (2 * dt). / ((2 * eps_z + dt * sigma_ez) * dx);
Cezhx = -1 * (2 * dt). / ((2 * eps_z + dt * sigma_ez) * dy);
Cezj = -1 * (2 * dt). / (2 * eps_z + dt * sigma_ez);

%%%初始化用于更新
Hx
的
FDTD
系数
Chxh = (2 * ux - dt * sigma_mx). / (2 * ux + dt * sigma_mx);
Chxez = -1 * (2 * dt). / ((2 * ux + dt * sigma_mx) * dy);

%%%初始化用于更新
Hy
的
FDTD
系数
Chyh = (2 * uy - dt * sigma_my). / (2 * uy + dt * sigma_my);
Chyez = (2 * dt). / ((2 * uy + dt * sigma_my) * dx);

%%%----------------------------------------- 定义
PML
区域 - ---------------------------------------------- %%%
PML_Ro = 1e-8; %PML
区域在法向入射时的反射系数。
n_PML = 2; %PML
的阶数

n_pml_xn = 10; %xn
区域的
PML
厚度为
10
个网格
n_pml_xp = 10; %xp
区域的
PML
厚度为
10
个网格
n_pml_yn = 10; %yn
区域的
PML
厚度为
10
个网格
n_pml_yp = 10; %yp
区域的
PML
厚度为
10
个网格

%%%初始化PML区域中的导电率
sigma_pex_xn = zeros(n_pml_xn, Ny1 - 2);
sigma_pex_xp = zeros(n_pml_xp, Ny1 - 2);
sigma_pex_yn = zeros(Nx1 - n_pml_xn - n_pml_xp - 2, n_pml_yn);
sigma_pex_yp = zeros(Nx1 - n_pml_xn - n_pml_xp - 2, n_pml_yp);

sigma_pey_xn = zeros(n_pml_xn, Ny1 - n_pml_yp - n_pml_yn - 2);
sigma_pey_xp = zeros(n_pml_xp, Ny1 - n_pml_yp - n_pml_yn - 2);
sigma_pey_yn = zeros(Nx1 - 2, n_pml_yn);
sigma_pey_yp = zeros(Nx1 - 2, n_pml_yp);

sigma_pmx_xn = zeros(n_pml_xn, Ny - 1);
sigma_pmx_xp = zeros(n_pml_xp, Ny - 1);

sigma_pmy_yn = zeros(Nx - 1, n_pml_yn);
sigma_pmy_yp = zeros(Nx - 1, n_pml_yp);

%%%设置xn区域
sigma_max_xn = -1 * ((n_PML + 1) * eps_b * c * log(PML_Ro)) / (2 * dx * n_pml_xn);
pho_e_xn = [n_pml_xn: -1: 1] - 3 / 4;
pho_m_xn = [n_pml_xn: -1: 1] - 1 / 4;

for xn_num = 1: n_pml_xn
sigma_pex_xn(xn_num,:) = sigma_max_xn * (pho_e_xn(xn_num) / n_pml_xn) ^ n_PML;
sigma_pmx_xn(xn_num,:) = (u_o / eps_b) * (sigma_max_xn * (pho_m_xn(xn_num) / n_pml_xn) ^ n_PML);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%设置xp区域
%%%在此处计算sigma_pex_xp和sigma_pmx_xp
sigma_max_xp = sigma_max;
pho_e_xp = [1: n_pml_xp];
pho_m_xp = [1: n_pml_xp] - 0.5;
for xp_num = 1: n_pml_xp
sigma_pex_xp(xp_num,:) = sigma_max_xp * (pho_e_xp(xp_num) / n_pml_xp) ^ n_PML;
sigma_pmx_xp(xp_num,:) = (u_o / eps_b) * (sigma_max_xp * (pho_m_xp(xp_num) / n_pml_xp) ^ n_PML);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%设置yn区域
%%%在此处计算sigma_pey_yn和sigma_pmy_yn
sigma_max_yn = sigma_max;
pho_e_yn = [n_pml_yn: -1: 1];
pho_m_yn = [n_pml_yn: -1: 1] - 0.5;
for yn_num = 1: n_pml_yn
sigma_pey_yn(:, yn_num) = sigma_max_yn * (pho_e_yn(yn_num) / n_pml_yn) ^ n_PML;
sigma_pmy_yn(:, yn_num) = (u_o / eps_b) * (sigma_max_yn * (pho_m_yn(yn_num) / n_pml_yn) ^ n_PML);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%设置yp区域
%%%在此处计算sigma_pey_yp和sigma_pmy_yp
sigma_max_yp = sigma_max;
pho_e_yp = [1: n_pml_yp];
pho_m_yp = [1: n_pml_yp] - 0.5;
for yp_num = 1: n_pml_yp
sigma_pey_yp(:, yp_num) = sigma_max_yp * (pho_e_yp(yp_num) / n_pml_yp) ^ n_PML;
sigma_pmy_yp(:, yp_num) = (u_o / eps_b) * (sigma_max_yp * (pho_m_yp(yp_num) / n_pml_yp) ^ n_PML);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%--------------------------------------------- 定义PML的FDTD系数 - ---------------------------------------------- %%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Cezxe_xn =
%%% Cezxe_xp =
%%% Cezxe_yn =
%%% Cezxe_yp =

%%% Cezxhy_xn =
%%% Cezxhy_xp =
%%% Cezxhy_yn =
%%% Cezxhy_yp =

%%% Cezye_xn =
%%% Cezye_xp =
%%% Cezye_yn =
%%% Cezye_yp =

%%% Cezyhx_xn =
%%% Cezyhx_xp =
%%% Cezyhx_yn =
%%% Cezyhx_yp =

%%% Chxh_yn =
%%% Chxh_yp =
%%% Chxez_yn =
%%% Chxez_yp =

%%% Chyh_xn =
%%% Chyh_xp =
%%% Chyez_xn =
%%% Chyez_xp =

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%-------------------------------------- 定义中间区域的边界（针对不同的场） ------------------------------------------- %%%

%%%Hy场只在x方向有中间区域
xn_Hy_IM = n_pml_xn + 1;
xp_Hy_IM = Nx - n_pml_xp;
%%%Hx场只在y方向有中间区域
yn_Hx_IM = n_pml_yn + 1;
yp_Hx_IM = Ny - n_pml_yp;
%%%Ez场在x和y方向都有中间区域
yn_Ez_IM = n_pml_yn + 2;
yp_Ez_IM = Ny - n_pml_yp;
xn_Ez_IM = n_pml_xn + 2;
xp_Ez_IM = Nx - n_pml_xp;

%%%------------------------------------- 初始化源信号 - ----------------------------------------- %%%

%%%定义用于调制正弦波的高斯脉冲参数
tao = sqrt(2.3) / (pi * freq); %Tao决定了高斯脉冲的宽度
t_o = sqrt(20) * tao; %时间移位，以便使高斯脉冲在时间为0时为零
gauss_dev = 5e-10; %高斯脉冲的偏差

%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%在此处定义傅里叶变换核
%%% FT_kernal =

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%初始化用于存储整个模拟域中每个时间实例下电场分布的时域电场
TD_Ez = zeros(Nx1, Ny1, Nt - 1);

%%%初始化频域电场和磁场分布的矩阵
FD_Ez = zeros(Nx1, Ny1);
FD_Hx = zeros(Nx1, Ny);
FD_Hy = zeros(Nx, Ny1);

%%%初始化接收天线上的频域电场和磁场分布矩阵
S_Ez = zeros(ant_Rx_N, 1);
S_Hx = zeros(ant_Rx_N, 1);
S_Hy = zeros(ant_Rx_N, 1);

%%%初始化FDTD时间推进中的电场和磁场
Hx = zeros(Nx1, Ny); %初始化用于更新Hx场的数组
Hy = zeros(Nx, Ny1); %初始化用于更新Hy场的数组
Ez = zeros(Nx1, Ny1); %初始化用于更新Ez场的数组

%%%初始化PML区域中的E和H场（我们处理的是TMz波，因此考虑图7
.6
中的设置）
Ezx_pml_xn = zeros(Nx1, Ny1); %初始化xn区域中的Ezx
Ezx_pml_xp = zeros(Nx1, Ny1); %初始化xp区域中的Ezx
Ezx_pml_yn = zeros(Nx1, Ny1); %初始化yn区域中的Ezx
Ezx_pml_yp = zeros(Nx1, Ny1); %初始化yp区域中的Ezx

Ezy_pml_yn = zeros(Nx1, Ny1); %初始化yn区域中的Ezy
Ezy_pml_yp = zeros(Nx1, Ny1); %初始化yp区域中的Ezy
Ezy_pml_xn = zeros(Nx1, Ny1); %初始化xn区域中的Ezy
Ezy_pml_xp = zeros(Nx1, Ny1); %初始化xp区域中的Ezy

%%%-------------------------------------- 为发射天线定义波形 - ------------------------------------------ %%%

t_array_source = -1 * t_array(end) / 2: dt: t_array(end) / 2; %为源波形定义时间数组

Jiz = zeros(Nx, Ny, Nt); %初始化源波形

for nn = 1: ant_Tx_N
time_delay = ((lambda / 2) * (nn - 1) * sin(beamforming_angle)) / c; %定义激励信号的时间延迟
phi = 2 * pi * freq * time_delay; %将时间延迟转换为相移

Jiz(source_Y_Tx(nn), source_X_Tx(nn),:) =  exp(-1 * ((t_array_source - t_o). ^ 2). / (2 * gauss_dev ^ 2)). * cos(
    2. * pi. * freq. * (t_array_source - t_o) + phi); %定义由高斯脉冲调制的正弦波的电流密度
Jiz(source_Y_Tx(nn), source_X_Tx(nn),:) = circshift(Jiz(source_Y_Tx(nn), source_X_Tx(nn),:), -1500); %将波形移位以使其从0
ns开始
end

if show_wave
    figure(1);
    set(gcf, 'Position', [50 50 1300 950]);
end

%%%--------------------------- 从这里进入
FDTD
主循环进行时间步进计算 - -------------------------- %%%

for time_step = 1: Nt - 1
if time_step == round(Nt / 4)
    fprintf('25%% 时间域转换计算已完成...\n');
end

if time_step == round(Nt / 2)
    fprintf('50%% 时间域转换计算已完成...\n');
end

if time_step == round(3 * Nt / 4)
    fprintf('75%% 时间域转换计算已完成...\n');
end
%%%------------------------------------- 更新中间区域的
Hx
和
Hy
场 - ---------------------------------------

Hx(2: Nx, yn_Hx_IM: yp_Hx_IM) = Chxh(2: Nx, yn_Hx_IM: yp_Hx_IM).*Hx(2: Nx, yn_Hx_IM: yp_Hx_IM) + Chxez(
    2: Nx, yn_Hx_IM: yp_Hx_IM) ...
.*(Ez(2 : Nx, yn_Hx_IM + 1: yp_Hx_IM + 1) - Ez(2: Nx, yn_Hx_IM: yp_Hx_IM));
Hy(xn_Hy_IM: xp_Hy_IM, 2: Ny) = Chyh(xn_Hy_IM: xp_Hy_IM, 2: Ny).*Hy(xn_Hy_IM: xp_Hy_IM, 2: Ny) + Chyez(
    xn_Hy_IM: xp_Hy_IM, 2: Ny) ...
.*(Ez(xn_Hy_IM + 1 : xp_Hy_IM + 1, 2: Ny) - Ez(xn_Hy_IM: xp_Hy_IM, 2: Ny));

%%%--------------------------------------- 更新
PML
区域中的
Hx
和
Hy
场 - ---------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%更新
PML
区域中的
Hx
和
Hy
场

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%--------------------------------------- 更新中间区域的
Ez
场 - ---------------------------------------------

Ez(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM) = Ceze(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM).*Ez(
    xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM) ...
+ Cezhy(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM).*(Hy(xn_Ez_IM : xp_Ez_IM, yn_Ez_IM: yp_Ez_IM) - Hy(
    xn_Ez_IM - 1: xp_Ez_IM - 1, yn_Ez_IM: yp_Ez_IM)) ...
+ Cezhx(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM).*(Hx(xn_Ez_IM : xp_Ez_IM, yn_Ez_IM: yp_Ez_IM) - Hx(
    xn_Ez_IM: xp_Ez_IM, yn_Ez_IM - 1: yp_Ez_IM - 1)) ...
+ Cezj(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM).*Jiz(xn_Ez_IM: xp_Ez_IM, yn_Ez_IM: yp_Ez_IM, time_step);

%%%--------------------------------------- 更新
PML
区域的
Ez
场 - ---------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%更新
PML
区域的
Ez
场

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

TD_Ez(:,:, time_step) = Ez; %将当前时间实例下更新的电场存入此矩阵

%%%显示模拟的电场
if show_wave
    imagesc(abs(Ez));
    axis
    image;
    caxis([0 2e-2]);
    colormap('hot')
    pause(0.001)
end

%%%%%%%%%%%%%%%%%%%%%%%%%你需要完成这一部分（如果你选择在
FDTD
时间步进循环中执行傅里叶变换） %%%%%%%%%%%%%%%%%%%%%%%%%

%%%计算每个网格（整个计算域）上的频域
Ez
场
%%%你将计算结果放入在第
249
行定义的
"FD_Ez"
矩阵中

%%%计算接收天线位置的频域
Ez
场
%%%你将计算结果放入在第
254
行定义的
"S_Ez"
矩阵中

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end
