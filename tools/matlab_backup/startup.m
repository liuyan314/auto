%{
测试组 音箱播放测试工具 V1
Andy.wang   
2017/10/13
www.Libratone.com

测试异常种类：断续、忽高忽地、杂音
测试音源：线性扫频 100Hz-10KHz
思路：每帧fft找目标频点峰，同时目标频点跟踪预估
      1,相连两段同频峰值比，波动大就是忽高忽地
      2,频点有时消失段就是断续
      3，频率不正常变化就是卡顿
      4,目标频点外其他频点能量高就是杂音

最后输出log到txt。
%}
clear all;


currpath = pwd;
cd(currpath);
 %-------------UI窗口打开文件------------
%[file,PathName,FilterIndex] = uigetfile( '*.wav','请选择要分析的录音文件'); 
% [xx,fsold]=wavread(strcat(PathName,file));  %Matlab 2012
ffid=fopen('config.txt','r');
PathName = fgetl(ffid);
file = fgetl(ffid);
fclose(ffid);

[xx,fsold]=audioread(strcat(PathName,file));   %Matlab  2016
%----------调试模式打开文件--------
% strPath ='.\录音_6min\';
% file='16_48K_单声道_声音忽高忽低_6min';
% file='16_48K_单声道_重音__6min';
% file='16_48K_单声道_正常_6min';
% file='16_48K_单声道_断续卡顿_6min';
%filename=strcat(strPath,file,'.wav');
%[xx,fsold]=audioread(filename);
%---------参数设置--------------
fs=48000;
x=resample(xx,fs,fsold);
Fftlen=2048;
Framelen=floor(length(x)/Fftlen);
frequency_sweep=100:10000;    %测试音源的扫频范围
time_wav=10;     %测试扫频文件10s
freq_hop_max=ceil(length(frequency_sweep)/time_wav/(fs/Fftlen)/(fs/Fftlen));%线性扫频下，每帧最大跨度2个bin点         
fl=floor(frequency_sweep(1)/fs*Fftlen);
fh=floor(frequency_sweep(end)/fs*Fftlen);
f_4K=floor(4000/fs*Fftlen);   %在4KHz以下分析重音
peak_ths=35;  %最高值比最低值高d0dB 算是目标频点
% noise_ths=10^(30/20); %若目标频点外平均幅度高于最低幅度的15dB，则认为有杂音
noise_ths=40;
noise_time_ths=5;
uneven_time=100;
play_prepare_time=0.3;   %循环播放间隙时间
play_pre_binnum=round(play_prepare_time/Fftlen*fs);

bintable=zeros(Fftlen/2,3);  %[freqbin peak rate]
bintable(:,1)=[1:Fftlen/2];
bintable(:,3)=1;
noise_all=zeros(Framelen,1);
indu_all=zeros(Framelen,1);
log=[];

indu_intable_old=0;
indu_old=fl;
ind_noise_start=0;
ind_noise_end=0;

p0_num=0;   %空白帧连续数
p_last=0;   %上一阵目标频点
noise_num=0; %杂音帧计数
maybe_int=0; %前一帧疑似卡顿，还需看后一帧
%------debug用--------
% fig1=figure();
% show=0;
for frame=1:Framelen
    
    y=x((frame-1)*Fftlen+1 : frame*Fftlen);
    xfft=20*log10(abs(fft(y.*hanning(Fftlen))));
    xfft_all(:,frame)=xfft(1:Fftlen/2);
    
    %---------------plot debug--------------
%     if show==1
%         figure(fig1);
%         cla;
%         plot(xfft(1:Fftlen/2));
%         title(strcat('frame=',num2str(frame)));
%     end
    %---------------找峰---------------
    pp=[];
    maxp=0;
    for ii=fl:fh
        if xfft(ii)>xfft(ii-1) && xfft(ii)>xfft(ii+1)  %找所有波峰
            pp=[pp ;[ii  xfft(ii)]];
            if xfft(ii)>maxp
                maxp=xfft(ii);
            end
        end
    end
    pp=sortrows(pp,2);    %波峰排序
    pp=flipud(pp);
    for ii=1:length(pp(:,1))    %找出较大的波峰，去掉小波峰
        if pp(ii,2)<pp(1,2)-6;
            pp(ii,:)=0;
        end
    end
    pp(find(pp(:,2)==0),:)=[];
    ind_predict_start=indu_old;  %预测本帧频点
    ind_predict_end=indu_old+freq_hop_max+1;  %一帧后目标频点最大跨度
    yu=0;indu=0;
    xffttmp=xfft;
    for ii=1:length(pp(:,1))     %找目标频点
        xffttmp(pp(ii,1)-3:pp(ii,1)+3)=0;
        if pp(ii,1)>=ind_predict_start && pp(ii,1)<=ind_predict_end
            indu=pp(ii,1);
            yu=pp(ii,2);
            break;
        end
    end
    if indu==0      %找不到就用最高峰
        indu=pp(1,1);
        yu=pp(1,2);
    end
    
    
    if indu-100<fl
        tmpbin=[fl : indu+100];
    elseif indu+100>Fftlen/2
        tmpbin=[indu-100:iFftlen/2];
    else
        tmpbin=[indu-100:indu+100];
    end
    if indu<fl+5
        tmpbin_4K=[fl+5 : f_4K];
    elseif indu>f_4K-5
        tmpbin_4K=[fl:f_4K-5];
    else
        tmpbin_4K=[[fl:indu-5],[indu+5:f_4K]];
    end
    yl=mean(xffttmp(tmpbin)); %噪声平均峰值
    yl_all(frame)=yl;
    %% 分析波峰
    if yu>30 || (yu>-20 && yu>(yl+peak_ths))  %若为目标频点
        %------------判断杂音-----------
        if sum((yu-xfft(tmpbin_4K)<noise_ths).*(xfft(tmpbin_4K)>-40))>=20  || sum(xfft(tmpbin_4K)>-10)>=30
            noise_all(frame)=1;  %此帧为杂音
        end
        %-----------判断高低变化------------
        if bintable(indu,2)==0  %若此频点以前没出现过，则登记一下
            bintable(indu,2:3)=[yu 1];
        else                                     %若此频点出现过，则计算本次峰值与上次峰值比
            if indu~=indu_intable_old                    %连续重复频点不重复计
                bintable(indu,2:3)=[yu , yu-bintable(indu,2)];
                indu_intable_old=indu;
            end
        end
        
        indu_all(frame)=indu;
        indu_old=indu;
    else
        indu_all(frame)=0;
    end
    %% indu_all来分析断续/卡顿；noise_all来分析杂音；bintable分析忽高忽地
    if indu_all(frame)~=0
        p_now=indu_all(frame);
        %-----------断续分析------------
        if p_last>fh-5 && p_now<fl+5 && p0_num>0   %一段交界处有空白帧时
            if p0_num>play_pre_binnum
                if  frame>2 && sum(indu_all(1:frame-1))~=0
                    log=[log;[frame-1 2 (frame-1)*Fftlen/fs 0]];  %断续log
                end
            end
        elseif p0_num>2    %播放过程中有空白帧时
            if  frame>2 && sum(indu_all(1:frame-1))~=0
                log=[log;[frame-1 2 (frame-1)*Fftlen/fs 0]];  %断续log
            end
        end
        p0_num=0;
        %---------- 忽高忽地分析------------
        if p_last>fh-5 && p_now<fl+5
            if sum(bintable(:,3)>6)+sum(bintable(:,3)<-6) >uneven_time  %前后段同频点峰值比>2 || <0.5 的点超过5个就忽高忽地
                log=[log;[frame 1 frame*Fftlen/fs 0]];  %忽高忽地log
            end
        end
        %----------卡顿分析----------------
        if abs(p_now-p_last)<=freq_hop_max+1 &&  abs(p_now-p_last)>=0  %相连目标频率过度正常
            pok_all(frame)=1;
        else
            pok_all(frame)=0;
        end
        if frame>10
            if (indu_all(frame-3)-indu_all(frame-4)>10) ||  ( indu_all(frame-4)-indu_all(frame-3)>10 && indu_all(frame-4)<fh-5 && indu_all(frame-3)>fl+5 ) %一帧后，目标频率突变了
                if sum(pok_all(frame-7:frame-5))==3 && sum(pok_all(frame-2:frame))==3
                    log=[log;[frame-3 3 (frame-3)*Fftlen/fs 0]];  %卡顿
                end
            end
        end
        %-------------重音分析------------
        num_for_pure=3;   %连续几帧不是杂音，认为杂音停止
        if frame>num_for_pure 
            if sum(noise_all(frame-num_for_pure+1:frame))==0  
                if noise_num>=noise_time_ths
                    log=[log;[frame 4 noise_start*Fftlen/fs  (frame-num_for_pure)*Fftlen/fs ]];%杂音log
                end
                noise_num=0;
            elseif frame==Framelen
                if noise_num>=noise_time_ths
                    log=[log;[frame 4 noise_start*Fftlen/fs  frame*Fftlen/fs ]];%杂音log
                end
                noise_num=0;
            else
                if noise_num==0  
                    noise_start=frame;
                end
                noise_num=noise_num+1;
            end
        end
        %-------------------over-----------------
        p_last=p_now;
    else
        p0_num=p0_num+1;
    end
%     if ismember(frame,fx);
%         frame
%     end
%     
end
%-----------debug 图形输出-----------
% figure;
% subplot(211);
% plot(indu_all);
% subplot(212);
% plot(noise_all)
%---------输出logdao txt文档-----------
fid=fopen(strcat(PathName,file,'.txt'),'w+');
if sum(indu_all)/Framelen<0.1
    fprintf(fid,'no sound');
elseif isempty(log)==1
    fprintf(fid,'pass');
    fclose(fid);
else
    fprintf(fid,'issue:%d;',size(log,1));
    fprintf(fid,'\r\n');
    for ii=1:size(log,1)    
        if log(ii,2)==1
            issue='high_low:';%高低
            time=strcat(second2time(log(ii,3)),'before;');
        elseif log(ii,2)==2
            issue='intermittent:';%断续
            time=strcat(second2time(log(ii,3)),'before;');
        elseif log(ii,2)==3
            issue='unsmooth:';%卡顿
            time=strcat(second2time(log(ii,3)),';');
        elseif log(ii,2)==4
            issue='noise:';%杂音
            time=strcat(second2time(log(ii,3)),'-',second2time(log(ii,4)),';');
        else
            issur='other:';%未知问题
        end
        outword=strcat(issue,time);
        fprintf(fid,outword);
        fprintf(fid,'\r\n');
    end
    fclose(fid);
end

