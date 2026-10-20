"""NSL-KDD: CV apenas no treino; teste retido, semente 42."""
import argparse, hashlib, json, platform, time
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn, xgboost
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args()
d=pd.read_csv(a.data,header=None); X=d.iloc[:,:41];X.columns=X.columns.astype(str);y=(d[41]!='normal').astype(int)
# A coluna 42 (dificuldade) e o rótulo nunca entram nos atributos.
Xt,Xs,yt,ys=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
cv=StratifiedKFold(3,shuffle=True,random_state=42)
specs=[('Árvore de Decisão',DecisionTreeClassifier(random_state=42),{'model__max_depth':[6,12],'model__min_samples_leaf':[5]}),('Random Forest',RandomForestClassifier(n_estimators=80,n_jobs=1,random_state=42),{'model__max_depth':[12,None],'model__min_samples_leaf':[2]}),('XGBoost',XGBClassifier(n_estimators=100,n_jobs=1,random_state=42,tree_method='hist',eval_metric='logloss',reg_lambda=1),{'model__max_depth':[3,6],'model__learning_rate':[.1]})]
out={'dataset':'NSL-KDD KDDTrain+','sha256':hashlib.sha256(Path(a.data).read_bytes()).hexdigest(),'train':len(Xt),'test':len(Xs),'attacks_test':int(ys.sum()),'seed':42,'environment':{'python':platform.python_version(),'sklearn':sklearn.__version__,'xgboost':xgboost.__version__,'pandas':pd.__version__,'numpy':np.__version__,'platform':platform.platform()},'models':[]}
for name,model,grid in specs:
 pre=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['1','2','3'])],remainder='passthrough')
 pipe=Pipeline([('pre',pre),('model',model)])
 search=GridSearchCV(pipe,grid,scoring='f1',cv=cv,n_jobs=1,refit=True)
 start=time.perf_counter();search.fit(Xt,yt);search_time=time.perf_counter()-start
 best=search.best_estimator_; start=time.perf_counter();best.fit(Xt,yt);fit_time=time.perf_counter()-start
 pred=best.predict(Xs);best.predict(Xs.iloc[:1]);single=[];batch=[]
 for _ in range(30):
  t=time.perf_counter();best.predict(Xs.iloc[:1]);single.append((time.perf_counter()-t)*1000)
 for _ in range(5):
  t=time.perf_counter();best.predict(Xs);batch.append((time.perf_counter()-t)*1000/len(Xs))
 r=dict(name=name,accuracy=accuracy_score(ys,pred),precision=precision_score(ys,pred),recall=recall_score(ys,pred),f1=f1_score(ys,pred),matrix=confusion_matrix(ys,pred).tolist(),fit_s=fit_time,search_s=search_time,single_ms=float(np.median(single)),p95_ms=float(np.percentile(single,95)),batch_ms=float(np.median(batch)),cv_f1=search.best_score_,params=search.best_params_)
 names=best.named_steps['pre'].get_feature_names_out(); imp=best.named_steps['model'].feature_importances_; order=np.argsort(imp)[-8:][::-1]; r['importance']=[{'feature':str(names[i]),'value':float(imp[i])} for i in order]
 out['models'].append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
Path('dist/results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
