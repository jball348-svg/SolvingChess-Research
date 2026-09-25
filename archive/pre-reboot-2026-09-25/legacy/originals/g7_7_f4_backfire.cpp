#define main g74_embedded_main
#include "/mnt/data/g7_fortress_ascent_v8.cpp"
#undef main
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();initB();initPairs();auto K=solveKPK();F4 f(K);f.solve();
 const int SZ=F4::SZ; vector<uint8_t>A(SZ,0),C(SZ,0),T(SZ,0);vector<int>rem(SZ,0);deque<int>q;
 auto target=[&](int c){auto s=f.dec(c);return s.pri>=4&&cheb(s.wk,63)<=4&&cheb(s.bk,63)>=5;};
 long long direct=0;for(int c=0;c<SZ;c++)if(f.valid[c]&&target(c)){T[c]=A[c]=1;q.push_back(c);direct++;}
 for(int c=0;c<SZ;c++)if(f.valid[c]&&!A[c]){auto s=f.dec(c);if(s.t==1){auto m=f.succ(s);rem[c]=m.in.size()+m.ew+m.ed;}}
 while(!q.empty()){int z=q.front();q.pop_front();f.preds(z,[&](int p){if(A[p])return;auto s=f.dec(p);if(s.t==0){A[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){A[p]=1;q.push_back(p);}});}long long an=0;for(int c=0;c<SZ;c++)if(f.valid[c]&&A[c])an++;
 q.clear();fill(rem.begin(),rem.end(),0);for(int c=0;c<SZ;c++)if(T[c]){C[c]=1;q.push_back(c);}for(int c=0;c<SZ;c++)if(f.valid[c]&&A[c]&&!C[c]){auto s=f.dec(c);if(s.t==1){auto m=f.succ(s);rem[c]=m.in.size()+m.ew+m.ed;}}
 while(!q.empty()){int z=q.front();q.pop_front();bool zcheck=f.check(f.dec(z));f.preds(z,[&](int p){if(!A[p]||C[p])return;auto s=f.dec(p);if(s.t==0){if(T[z]||zcheck){C[p]=1;q.push_back(p);}}else if(rem[p]>0&&--rem[p]==0){C[p]=1;q.push_back(p);}});}long long cn=0;for(int c=0;c<SZ;c++)if(C[c])cn++;
 vector<uint8_t>P(SZ,0),Rset(SZ,0);long long pn=0;map<string,long long>cats;for(int c=0;c<SZ;c++)if(f.valid[c]&&A[c]&&!C[c]){auto s=f.dec(c);if(s.t!=0)continue;auto m=f.succ(s);bool kg=0,pg=0,bg=0,any=0;for(int z:m.in)if(C[z]&&!T[z]&&!f.check(f.dec(z))){any=1;auto zz=f.dec(z);if(zz.wk!=s.wk)kg=1;else if(zz.pri!=s.pri)pg=1;else if(zz.b!=s.b)bg=1;}if(any){P[c]=Rset[c]=1;pn++;string key=string(kg?"K":"")+(pg?"P":"")+(bg?"B":"");cats[key]++;}}
 fill(rem.begin(),rem.end(),0);for(int c=0;c<SZ;c++)if(f.valid[c]&&A[c]&&!C[c]&&!Rset[c]){auto s=f.dec(c);if(s.t==1){auto m=f.succ(s);int n=m.ew+m.ed;for(int z:m.in)if(!C[z])n++;rem[c]=n;}}
 q.clear();for(int c=0;c<SZ;c++)if(Rset[c])q.push_back(c);while(!q.empty()){int z=q.front();q.pop_front();f.preds(z,[&](int p){if(!A[p]||C[p]||Rset[p])return;auto s=f.dec(p);if(s.t==0){Rset[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){Rset[p]=1;q.push_back(p);}});}long long qn=0,mis=0,extra=0,badC=0;for(int c=0;c<SZ;c++)if(f.valid[c]){bool qq=A[c]&&!C[c];qn+=qq;if(qq&&!Rset[c])mis++;if(Rset[c]&&!qq)extra++;if(C[c]&&!f.win[c])badC++;}
 cout<<"G6_F4_BACKFIRE direct="<<direct<<" attr="<<an<<" check="<<cn<<" retained_pct="<<fixed<<setprecision(6)<<100.0*cn/an<<" quiet_required="<<qn<<" pivots="<<pn<<" amp="<<(pn?double(qn)/pn:0)<<" missing="<<mis<<" extra="<<extra<<" check_nonwins="<<badC<<" cats=";for(auto&kv:cats)cout<<kv.first<<":"<<kv.second<<",";cout<<"\n";
}
