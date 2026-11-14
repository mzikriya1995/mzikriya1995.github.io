from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Rectangle
out=Path('/mnt/data/RNN_LSTM_4_Hour_Quarto_Project/slides/rnn-lstm/assets');out.mkdir(parents=True,exist_ok=True)
BURG='#982D42'; BLUE='#2865A2'; GOLD='#C68B3D'; INK='#28303D'; GREEN='#23846B'; BG='#F8F7F4'
def fig_start(title, xlabel=None, ylabel=None, size=(10,4.1)):
  fig,ax=plt.subplots(figsize=size,layout='constrained',dpi=160)
  fig.patch.set_facecolor(BG);ax.set_facecolor('white')
  ax.set_title(title,size=17,color=INK,weight='bold',pad=15)
  ax.tick_params(colors=INK,labelsize=11)
  for side in ['top','right']:ax.spines[side].set_visible(False)
  for side in ['bottom','left']:ax.spines[side].set_color('#BCC2C6')
  ax.grid(alpha=.18,zorder=0)
  if xlabel:ax.set_xlabel(xlabel,fontsize=12,color=INK)
  if ylabel:ax.set_ylabel(ylabel,fontsize=12,color=INK)
  return fig,ax
def save(fig,name):fig.savefig(out/name,bbox_inches='tight',facecolor=fig.get_facecolor());plt.close(fig)
x=np.linspace(-5,5,420);t=np.tanh(x);sig=1/(1+np.exp(-x))
fig,ax=fig_start('Activation and derivative: tanh','Input z','Value / slope');ax.plot(x,t,color=BLUE,lw=2.6,label='tanh(z)');ax.plot(x,1-t**2,color=BURG,lw=2.6,label="tanh'(z) = 1−tanh²(z)");ax.axhline(0,color='#AAB1BB',lw=1);ax.legend(frameon=False,loc='upper left',fontsize=12);save(fig,'activation_derivative.png')
fig,ax=fig_start('Repeated gradient-factor products (illustrative)','Number of recurrent steps','Product magnitude');k=np.arange(0,31);ax.plot(k,.75**k,lw=3,color=BLUE,marker='o',markevery=5,label='Factor 0.75: decay');ax.plot(k,1.15**k,lw=3,color=BURG,marker='s',markevery=5,label='Factor 1.15: growth');ax.set_yscale('log');ax.legend(frameon=False,fontsize=11);save(fig,'gradient_product_log.png')
fig,ax=fig_start('Sigmoid gates can saturate','Preactivation z','Gate value');ax.plot(x,sig,color=BURG,lw=3,label='sigmoid(z)');ax.plot(x,sig*(1-sig),color=BLUE,lw=2.6,label="sigmoid'(z)");ax.axhline(.5,color='#BCC2C6',lw=1,ls='--');ax.legend(frameon=False,fontsize=11);save(fig,'gate_saturation.png')
fig,ax=fig_start('Forget-gate retention: c(t)=f·c(t−1)','Timesteps without new input','Fraction of initial cell memory');k=np.arange(0,31);[(ax.plot(k,f**k,lw=3,label=f'f={f:.2f}',color=c)) for f,c in [(.5,BURG),(.9,BLUE),(.99,GREEN)]];ax.legend(frameon=False,fontsize=12);ax.set_ylim(0,1.03);save(fig,'memory_retention.png')
fig,ax=fig_start('Global-norm gradient clipping: scale direction, not angle','Gradient component 1','Gradient component 2');ax.axhline(0,color='#B0B6BD');ax.axvline(0,color='#B0B6BD');theta=np.linspace(0,2*np.pi,250);ax.plot(np.cos(theta),np.sin(theta),color=GREEN,ls='--',lw=2,label='Clip norm = 1');ax.arrow(0,0,2.8,1.8,color=BURG,width=.035,head_width=.15,head_length=.17,length_includes_head=True,label='Before clipping');norm=np.sqrt(2.8**2+1.8**2);ax.arrow(0,0,2.8/norm,1.8/norm,color=BLUE,width=.025,head_width=.12,head_length=.14,length_includes_head=True,label='After clipping');ax.set_xlim(-1.5,3.4);ax.set_ylim(-1.6,2.5);ax.set_aspect('equal');ax.legend(frameon=False,fontsize=11,loc='upper left');save(fig,'clipping_geometry.png')
fig,ax=fig_start('Forecasting windows: historical inputs, future target','Sequence index','Value');t=np.arange(80);y=np.sin(t/6)+.25*np.cos(t/3);ax.plot(t,y,color='#9AA6B3',lw=2.3);lo,lookback=35,15;ax.plot(t[lo:lo+lookback],y[lo:lo+lookback],color=BLUE,lw=4,label='Input history');ax.scatter([t[lo+lookback]],[y[lo+lookback]],s=135,color=BURG,zorder=4,label='Target (t+1)');ax.legend(frameon=False);save(fig,'sliding_window_target.png')
fig,ax=fig_start('Rolling-origin evaluation: train only on the past','Observation index','Data partitions');rows=[(1,50,60),(2,60,70),(3,70,80),(4,80,90)];
for j,(fold,tr,v) in enumerate(rows):
 y=4-j;ax.barh(y,tr,height=.58,left=0,color=BLUE,label='Available training history' if j==0 else None);ax.barh(y,v-tr,height=.58,left=tr,color=GOLD,label='Validation block' if j==0 else None);ax.barh(y,100-v,height=.58,left=v,color='#E8ECF1',label='Future not used' if j==0 else None)
ax.set_yticks([1,2,3,4],['Fold 4','Fold 3','Fold 2','Fold 1']);ax.set_xlim(0,100);ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.02),fontsize=10);save(fig,'rolling_origin.png')
fig,ax=fig_start('Parameter counts: input=8, hidden=16, output=1','Model','Trainable recurrent-layer parameters');names=['Simple RNN','GRU','LSTM'];counts=[(8+16+1)*16,3*(8+16+2)*16,4*(8+16+2)*16];bars=ax.bar(names,counts,color=[BLUE,GREEN,BURG],width=.55);ax.bar_label(bars,labels=[f'{n:,}' for n in counts],padding=5,fontsize=12);ax.set_ylim(0,max(counts)*1.25);save(fig,'parameter_cost.png')
fig,ax=fig_start('How the hidden state changes with the recurrent factor','Time step','Hidden-state value');vals=np.zeros((3,21));xs=np.zeros(21);xs[0]=1.0
for r,a in enumerate([.2,.7,1.05]):
 for j in range(21): vals[r,j]=np.tanh(a*(vals[r,j-1] if j>0 else 0)+.7*xs[j])
 ax.plot(np.arange(21),vals[r],lw=2.5,label=f'W_hh={a:.2f}',color=[GREEN,BLUE,BURG][r])
ax.legend(frameon=False);ax.xaxis.set_major_locator(MaxNLocator(integer=True));save(fig,'rnn_state_dynamics.png')
# Real demonstration outputs from prior stored Python run; no fabricated results
pred_file=Path('/mnt/data/_rnn4h_work/COPY_TO_YOUR_EXISTING_WEBSITE/slides/rnn-lstm/outputs/pytorch_predictions.csv')
if pred_file.exists():
 p=pd.read_csv(pred_file)
 fig,ax=fig_start('Illustrative error diagnostics from packaged PyTorch run','Target time index','Forecast residual (prediction − actual)')
 for n,c in [('naive','#596E82'),('rnn',BLUE),('lstm',BURG)]:
  if n in p.columns:ax.plot(p.t,p[n]-p.actual,lw=1.6,label=n.upper(),color=c,alpha=.85)
 ax.axhline(0,color=INK,lw=1);ax.legend(frameon=False,ncol=3);save(fig,'forecast_residuals.png')
fig,ax=fig_start('Threshold choice changes anomaly decisions (illustrative)','Anomaly score','Number of windows');rng=np.random.default_rng(32);normal=rng.gamma(2.5,1,500);abnormal=rng.gamma(5.5,1.15,100);ax.hist(normal,bins=26,alpha=.55,density=True,label='Normal',color=BLUE);ax.hist(abnormal,bins=26,alpha=.48,density=True,label='Abnormal',color=BURG);ax.axvline(5.5,color=INK,lw=2.2,ls='--',label='Example threshold');ax.legend(frameon=False);save(fig,'anomaly_threshold.png')
fig,ax=fig_start('Sequence classification: precision and recall vary with threshold','Decision threshold','Score');thresholds=np.linspace(0.02,.98,150);precision=np.clip(.4+.57*thresholds**.6,0,1);recall=np.clip(.98-(thresholds**1.8)*.92,0,1);f1=2*precision*recall/(precision+recall+1e-10);ax.plot(thresholds,precision,color=GREEN,lw=2.6,label='Precision (illustrative)');ax.plot(thresholds,recall,color=BLUE,lw=2.6,label='Recall (illustrative)');ax.plot(thresholds,f1,color=BURG,lw=3,label='F1');ax.legend(frameon=False);ax.set_ylim(0,1.05);save(fig,'classification_threshold_tradeoff.png')
print('figures:',len(list(out.glob('*.png'))))
