
tm = 1.0000e-04;
bw = 900e4;
fs = 1e9;

waveform = phased.FMCWWaveform(...
    'SweepTime',tm,...
    'SweepBandwidth',bw,...
    'SampleRate',fs,...
    'SweepDirection', 'Up');

sig = waveform();
subplot(211); 
plot(real(sig))
% plot(0:1/fs:tm-1/fs,real(sig));

xlabel('Time (s)'); ylabel('Amplitude (v)');
title('FMCW signal'); axis tight;
subplot(212); 
spectrogram(sig);
title('FMCW signal spectrogram');