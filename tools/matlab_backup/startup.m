%{
������ ���䲥�Ų��Թ��� V1
Andy.wang   
2017/10/13
www.Libratone.com

�����쳣���ࣺ���������ߺ��ء�����
������Դ������ɨƵ 100Hz-10KHz
˼·��ÿ֡fft��Ŀ��Ƶ��壬ͬʱĿ��Ƶ�����Ԥ��
      1,��������ͬƵ��ֵ�ȣ���������Ǻ��ߺ���
      2,Ƶ����ʱ��ʧ�ξ��Ƕ���
      3��Ƶ�ʲ������仯���ǿ���
      4,Ŀ��Ƶ��������Ƶ�������߾�������

������log��txt��
%}
clear all;


currpath = pwd;
cd(currpath);
 %-------------UI���ڴ��ļ�------------
%[file,PathName,FilterIndex] = uigetfile( '*.wav','��ѡ��Ҫ������¼���ļ�'); 
% [xx,fsold]=wavread(strcat(PathName,file));  %Matlab 2012
ffid=fopen('config.txt','r');
PathName = fgetl(ffid);
file = fgetl(ffid);
fclose(ffid);

[xx,fsold]=audioread(strcat(PathName,file));   %Matlab  2016
%----------����ģʽ���ļ�--------
% strPath ='.\¼��_6min\';
% file='16_48K_������_�������ߺ���_6min';
% file='16_48K_������_����__6min';
% file='16_48K_������_����_6min';
% file='16_48K_������_��������_6min';
%filename=strcat(strPath,file,'.wav');
%[xx,fsold]=audioread(filename);
%---------��������--------------
fs=48000;
x=resample(xx,fs,fsold);
Fftlen=2048;
Framelen=floor(length(x)/Fftlen);
frequency_sweep=100:10000;    %������Դ��ɨƵ��Χ
time_wav=10;     %����ɨƵ�ļ�10s
freq_hop_max=ceil(length(frequency_sweep)/time_wav/(fs/Fftlen)/(fs/Fftlen));%����ɨƵ�£�ÿ֡�����2��bin��         
fl=floor(frequency_sweep(1)/fs*Fftlen);
fh=floor(frequency_sweep(end)/fs*Fftlen);
f_4K=floor(4000/fs*Fftlen);   %��4KHz���·�������
peak_ths=35;  %���ֵ�����ֵ��d0dB ����Ŀ��Ƶ��
% noise_ths=10^(30/20); %��Ŀ��Ƶ����ƽ�����ȸ�����ͷ��ȵ�15dB������Ϊ������
noise_ths=40;
noise_time_ths=5;
uneven_time=100;
play_prepare_time=0.3;   %ѭ�����ż�϶ʱ��
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

p0_num=0;   %�հ�֡������
p_last=0;   %��һ��Ŀ��Ƶ��
noise_num=0; %����֡����
maybe_int=0; %ǰһ֡���ƿ��٣����迴��һ֡
%------debug��--------
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
    %---------------�ҷ�---------------
    pp=[];
    maxp=0;
    for ii=fl:fh
        if xfft(ii)>xfft(ii-1) && xfft(ii)>xfft(ii+1)  %�����в���
            pp=[pp ;[ii  xfft(ii)]];
            if xfft(ii)>maxp
                maxp=xfft(ii);
            end
        end
    end
    pp=sortrows(pp,2);    %��������
    pp=flipud(pp);
    for ii=1:length(pp(:,1))    %�ҳ��ϴ�Ĳ��壬ȥ��С����
        if pp(ii,2)<pp(1,2)-6;
            pp(ii,:)=0;
        end
    end
    pp(find(pp(:,2)==0),:)=[];
    ind_predict_start=indu_old;  %Ԥ�Ȿ֡Ƶ��
    ind_predict_end=indu_old+freq_hop_max+1;  %һ֡��Ŀ��Ƶ�������
    yu=0;indu=0;
    xffttmp=xfft;
    for ii=1:length(pp(:,1))     %��Ŀ��Ƶ��
        xffttmp(pp(ii,1)-3:pp(ii,1)+3)=0;
        if pp(ii,1)>=ind_predict_start && pp(ii,1)<=ind_predict_end
            indu=pp(ii,1);
            yu=pp(ii,2);
            break;
        end
    end
    if indu==0      %�Ҳ���������߷�
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
    yl=mean(xffttmp(tmpbin)); %����ƽ����ֵ
    yl_all(frame)=yl;
    %% ��������
    if yu>30 || (yu>-20 && yu>(yl+peak_ths))  %��ΪĿ��Ƶ��
        %------------�ж�����-----------
        if sum((yu-xfft(tmpbin_4K)<noise_ths).*(xfft(tmpbin_4K)>-40))>=20  || sum(xfft(tmpbin_4K)>-10)>=30
            noise_all(frame)=1;  %��֡Ϊ����
        end
        %-----------�жϸߵͱ仯------------
        if bintable(indu,2)==0  %����Ƶ����ǰû���ֹ�����Ǽ�һ��
            bintable(indu,2:3)=[yu 1];
        else                                     %����Ƶ����ֹ�������㱾�η�ֵ���ϴη�ֵ��
            if indu~=indu_intable_old                    %�����ظ�Ƶ�㲻�ظ���
                bintable(indu,2:3)=[yu , yu-bintable(indu,2)];
                indu_intable_old=indu;
            end
        end
        
        indu_all(frame)=indu;
        indu_old=indu;
    else
        indu_all(frame)=0;
    end
    %% indu_all����������/���٣�noise_all������������bintable�������ߺ���
    if indu_all(frame)~=0
        p_now=indu_all(frame);
        %-----------��������------------
        if p_last>fh-5 && p_now<fl+5 && p0_num>0   %һ�ν��紦�пհ�֡ʱ
            if p0_num>play_pre_binnum
                if  frame>2 && sum(indu_all(1:frame-1))~=0
                    log=[log;[frame-1 2 (frame-1)*Fftlen/fs 0]];  %����log
                end
            end
        elseif p0_num>2    %���Ź������пհ�֡ʱ
            if  frame>2 && sum(indu_all(1:frame-1))~=0
                log=[log;[frame-1 2 (frame-1)*Fftlen/fs 0]];  %����log
            end
        end
        p0_num=0;
        %---------- ���ߺ��ط���------------
        if p_last>fh-5 && p_now<fl+5
            if sum(bintable(:,3)>6)+sum(bintable(:,3)<-6) >uneven_time  %ǰ���ͬƵ���ֵ��>2 || <0.5 �ĵ㳬��5���ͺ��ߺ���
                log=[log;[frame 1 frame*Fftlen/fs 0]];  %���ߺ���log
            end
        end
        %----------���ٷ���----------------
        if abs(p_now-p_last)<=freq_hop_max+1 &&  abs(p_now-p_last)>=0  %����Ŀ��Ƶ�ʹ�������
            pok_all(frame)=1;
        else
            pok_all(frame)=0;
        end
        if frame>10
            if (indu_all(frame-3)-indu_all(frame-4)>10) ||  ( indu_all(frame-4)-indu_all(frame-3)>10 && indu_all(frame-4)<fh-5 && indu_all(frame-3)>fl+5 ) %һ֡��Ŀ��Ƶ��ͻ����
                if sum(pok_all(frame-7:frame-5))==3 && sum(pok_all(frame-2:frame))==3
                    log=[log;[frame-3 3 (frame-3)*Fftlen/fs 0]];  %����
                end
            end
        end
        %-------------��������------------
        num_for_pure=3;   %������֡������������Ϊ����ֹͣ
        if frame>num_for_pure 
            if sum(noise_all(frame-num_for_pure+1:frame))==0  
                if noise_num>=noise_time_ths
                    log=[log;[frame 4 noise_start*Fftlen/fs  (frame-num_for_pure)*Fftlen/fs ]];%����log
                end
                noise_num=0;
            elseif frame==Framelen
                if noise_num>=noise_time_ths
                    log=[log;[frame 4 noise_start*Fftlen/fs  frame*Fftlen/fs ]];%����log
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
%-----------debug ͼ�����-----------
% figure;
% subplot(211);
% plot(indu_all);
% subplot(212);
% plot(noise_all)
%---------���logdao txt�ĵ�-----------
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
            issue='high_low:';%�ߵ�
            time=strcat(second2time(log(ii,3)),'before;');
        elseif log(ii,2)==2
            issue='intermittent:';%����
            time=strcat(second2time(log(ii,3)),'before;');
        elseif log(ii,2)==3
            issue='unsmooth:';%����
            time=strcat(second2time(log(ii,3)),';');
        elseif log(ii,2)==4
            issue='noise:';%����
            time=strcat(second2time(log(ii,3)),'-',second2time(log(ii,4)),';');
        else
            issur='other:';%δ֪����
        end
        outword=strcat(issue,time);
        fprintf(fid,outword);
        fprintf(fid,'\r\n');
    end
    fclose(fid);
end

