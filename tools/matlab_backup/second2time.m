%ÃëÖÓ×ª hh-mm-ss
function time=second2time(second)
hour=floor(second/3600);
if hour>0
    second=second-hour*3600;
end
min=floor(second/60);
if min>0
    second=second-min*60;
end
if second*10/10-floor(second*10/10)==0
    time='000';
    time=strcat( num2str(second) ,'.',time);
else
    time=floor(mod(second*1000,1000));
    time=num2str(time);
    time=strcat( num2str(floor(second)),'.', time);
end
if min>0
    time=strcat(num2str(min),'.',time);
end
if hour>0
    time=strcat(num2str(hour),'.',time);
end
end