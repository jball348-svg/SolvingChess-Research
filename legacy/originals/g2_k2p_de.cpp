#include <bits/stdc++.h>
using namespace std;
static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;}
static inline int ch(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
static inline bool patt(int p,int t){return R(t)==R(p)+1 && abs(F(t)-F(p))==1;}

// Generic K+P vs K for fixed pawn file pf, ranks 2..7. stm 0=W,1=B.
struct KPK {
 int pf, N=64*6*64*2; vector<uint8_t> valid,win; vector<int16_t> rank;
 static inline int enc(int w,int pi,int b,int st){return (((w*6+pi)*64+b)*2+st);} 
 static inline void dec(int id,int&w,int&pi,int&b,int&st){st=id%2;id/=2;b=id%64;id/=64;pi=id%6;id/=6;w=id;}
 int psq(int pi) const {return (pi+1)*8+pf;} // rank index 1..6 => chess ranks 2..7
 bool val(int w,int p,int b,int st) const {if(w==p||w==b||p==b)return false;if(ch(w,b)<=1)return false;if(st==0&&patt(p,b))return false;return true;}
 KPK(int file):pf(file),valid(N),win(N),rank(N,-1){solve();}
 void gen(int w,int pi,int b,int st, vector<int>&su,int &tot,bool &prom,bool &cap){
  su.clear();tot=0;prom=cap=false;int p=psq(pi);
  if(st==0){
   for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int nf=F(w)+df,nr=R(w)+dr;if(nf<0||nf>=8||nr<0||nr>=8)continue;int d=nr*8+nf;if(d==p||d==b||ch(d,b)<=1)continue;tot++;if(val(d,p,b,1))su.push_back(enc(d,pi,b,1));}
   int r=R(p); if(r==6){int d=p+8;if(d!=w&&d!=b){tot++;prom=true;}}
   else {int d=p+8;if(d!=w&&d!=b){tot++;if(val(w,d,b,1))su.push_back(enc(w,pi+1,b,1)); if(r==1){int d2=p+16;if(d2!=w&&d2!=b){tot++;if(val(w,d2,b,1))su.push_back(enc(w,pi+2,b,1));}}}}
  } else {
   for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int nf=F(b)+df,nr=R(b)+dr;if(nf<0||nf>=8||nr<0||nr>=8)continue;int d=nr*8+nf;if(d==w||ch(w,d)<=1)continue;bool cp=d==p;if(!cp&&patt(p,d))continue;tot++;if(cp){cap=true;continue;}if(val(w,p,d,0))su.push_back(enc(w,pi,d,0));}
  }
 }
 void solve(){vector<int> ids,su;vector<uint8_t> stm(N),capA(N),promA(N);vector<uint16_t> tot(N),rem;vector<uint32_t> indeg(N);
  for(int w=0;w<64;w++)for(int pi=0;pi<6;pi++){int p=psq(pi);for(int b=0;b<64;b++)for(int st=0;st<2;st++){int id=enc(w,pi,b,st);if(val(w,p,b,st)){valid[id]=1;stm[id]=st;ids.push_back(id);}}}
  long long E=0;for(int id:ids){int w,pi,b,st,t;bool pr,cp;dec(id,w,pi,b,st);gen(w,pi,b,st,su,t,pr,cp);tot[id]=t;promA[id]=pr;capA[id]=cp;for(int d:su){indeg[d]++;E++;}}
  vector<uint32_t> off(N+1),cur;for(int i=0;i<N;i++)off[i+1]=off[i]+indeg[i];cur=off;vector<uint32_t> pred(E);for(int id:ids){int w,pi,b,st,t;bool pr,cp;dec(id,w,pi,b,st);gen(w,pi,b,st,su,t,pr,cp);for(int d:su)pred[cur[d]++]=id;}
  rem=tot;vector<int>L,NX;for(int id:ids)if(stm[id]==0&&promA[id]){win[id]=1;rank[id]=0;L.push_back(id);}int r=0;while(!L.empty()){NX.clear();r++;for(int d:L)for(uint32_t k=off[d];k<off[d+1];k++){int p=pred[k];if(win[p])continue;if(stm[p]==0){win[p]=1;rank[p]=r;NX.push_back(p);}else{if(rem[p])rem[p]--;if(rem[p]==0&&tot[p]>0&&!capA[p]){win[p]=1;rank[p]=r;NX.push_back(p);}}}L.swap(NX);} 
  cerr<<"KPK file "<<char('a'+pf)<<" valid="<<ids.size()<<" wins="<<accumulate(win.begin(),win.end(),0LL)<<" draws="<<ids.size()-accumulate(win.begin(),win.end(),0LL)<<" edges="<<E<<"\n";
 }
};

// K + c-pawn + d-pawn vs K; pawn indices are ranks 2..7. promotion is White win.
struct K2P {
 int f1=3,f2=4; int N=64*6*6*64*2; KPK &k1,&k2; vector<uint8_t> valid,win,stm,capWinExit; vector<int16_t> rank; vector<uint16_t> tot;
 static inline int enc(int w,int p1i,int p2i,int b,int st){return (((((w*6+p1i)*6+p2i)*64+b)*2+st));}
 static inline void dec(int id,int&w,int&p1i,int&p2i,int&b,int&st){st=id%2;id/=2;b=id%64;id/=64;p2i=id%6;id/=6;p1i=id%6;id/=6;w=id;}
 int psq(int f,int pi)const{return (pi+1)*8+f;}
 bool val(int w,int p1,int p2,int b,int st)const{if(w==p1||w==p2||w==b||p1==p2||p1==b||p2==b)return false;if(ch(w,b)<=1)return false;if(st==0&&(patt(p1,b)||patt(p2,b)))return false;return true;}
 K2P(KPK&a,KPK&d):k1(a),k2(d),valid(N),win(N),stm(N),capWinExit(N),rank(N,-1),tot(N){solve();}
 // capWinExit: at Black node, whether a legal capture goes to a White-winning KPK (so still winning for White). capDrawExit separately returned.
 void gen(int w,int i1,int i2,int b,int st,vector<int>&su,int &T,bool &prom,bool &capDraw){
   su.clear();T=0;prom=false;capDraw=false;int p1=psq(f1,i1),p2=psq(f2,i2);
   if(st==0){
    for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int nf=F(w)+df,nr=R(w)+dr;if(nf<0||nf>=8||nr<0||nr>=8)continue;int d=nr*8+nf;if(d==p1||d==p2||d==b||ch(d,b)<=1)continue;T++;if(val(d,p1,p2,b,1))su.push_back(enc(d,i1,i2,b,1));}
    // pawn1 c-file
    for(int which=1;which<=2;which++){int p=which==1?p1:p2, pi=which==1?i1:i2;int r=R(p); if(r==6){int d=p+8;if(d!=w&&d!=b&&d!=(which==1?p2:p1)){T++;prom=true;}} else {int d=p+8;if(d!=w&&d!=b&&d!=(which==1?p2:p1)){T++;int ni=pi+1;if(which==1){if(val(w,d,p2,b,1))su.push_back(enc(w,ni,i2,b,1));}else{if(val(w,p1,d,b,1))su.push_back(enc(w,i1,ni,b,1));} if(r==1){int d2=p+16;if(d2!=w&&d2!=b&&d2!=(which==1?p2:p1)){T++;ni=pi+2;if(which==1){if(val(w,d2,p2,b,1))su.push_back(enc(w,ni,i2,b,1));}else{if(val(w,p1,d2,b,1))su.push_back(enc(w,i1,ni,b,1));}}}}}}
   } else {
    for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int nf=F(b)+df,nr=R(b)+dr;if(nf<0||nf>=8||nr<0||nr>=8)continue;int d=nr*8+nf;if(d==w||ch(w,d)<=1)continue;bool c1=d==p1,c2=d==p2;if(!c1&&!c2&&(patt(p1,d)||patt(p2,d)))continue; // attacked by surviving pawns
      if(c1 && patt(p2,d)) continue; if(c2 && patt(p1,d)) continue; // captured square protected by other pawn
      T++;
      if(c1||c2){int remp=c1?p2:p1; int remi=c1?i2:i1; KPK &K=c1?k2:k1; int kid=KPK::enc(w,remi,d,0); if(!K.win[kid]) capDraw=true; else su.push_back(-1-kid); continue;}
      if(val(w,p1,p2,d,0))su.push_back(enc(w,i1,i2,d,0));
    }
   }
 }
 void solve(){vector<int>ids,su;vector<uint8_t>promA(N),capDrawA(N);vector<uint16_t>rem;vector<uint32_t>indeg(N);long long validCount=0;
   for(int w=0;w<64;w++)for(int i1=0;i1<6;i1++){int p1=psq(f1,i1);for(int i2=0;i2<6;i2++){int p2=psq(f2,i2);for(int b=0;b<64;b++)for(int st=0;st<2;st++){int id=enc(w,i1,i2,b,st);if(val(w,p1,p2,b,st)){valid[id]=1;stm[id]=st;ids.push_back(id);validCount++;}}}}
   // Only internal K2P edges contribute predecessor graph. KPK-winning capture exits are treated as already winning terminals for universal Black-node condition.
   long long E=0;vector<uint16_t> kpkWinExits(N,0);
   for(int id:ids){int w,i1,i2,b,st,T;bool pr,cd;dec(id,w,i1,i2,b,st);gen(w,i1,i2,b,st,su,T,pr,cd);tot[id]=T;promA[id]=pr;capDrawA[id]=cd;for(int d:su){if(d>=0){indeg[d]++;E++;}else{kpkWinExits[id]++;}}}
   vector<uint32_t>off(N+1),cur;for(int i=0;i<N;i++)off[i+1]=off[i]+indeg[i];cur=off;vector<uint32_t>pred(E);for(int id:ids){int w,i1,i2,b,st,T;bool pr,cd;dec(id,w,i1,i2,b,st);gen(w,i1,i2,b,st,su,T,pr,cd);for(int d:su)if(d>=0)pred[cur[d]++]=id;}
   // rem counts non-winning obligations at Black nodes: internal successors + draw captures. Winning KPK capture exits need no proof.
   rem.assign(N,0);for(int id:ids){if(stm[id]==1){uint16_t internal=0;int w,i1,i2,b,st,T;bool pr,cd;dec(id,w,i1,i2,b,st);gen(w,i1,i2,b,st,su,T,pr,cd);for(int d:su)if(d>=0)internal++; rem[id]=internal + (cd?1:0);}}
   vector<int>L,NX;for(int id:ids){if(stm[id]==0&&promA[id]){win[id]=1;rank[id]=0;L.push_back(id);} else if(stm[id]==1 && tot[id]>0 && rem[id]==0){win[id]=1;rank[id]=0;L.push_back(id);}}
   long long cum=L.size();cout<<"rank 0 "<<L.size()<<" cumulative "<<cum<<"\n";int r=0;while(!L.empty()){NX.clear();r++;for(int d:L)for(uint32_t k=off[d];k<off[d+1];k++){int p=pred[k];if(win[p])continue;if(stm[p]==0){win[p]=1;rank[p]=r;NX.push_back(p);}else{if(rem[p])rem[p]--;if(rem[p]==0&&tot[p]>0){win[p]=1;rank[p]=r;NX.push_back(p);}}}if(NX.empty())break;cum+=NX.size();cout<<"rank "<<r<<" "<<NX.size()<<" cumulative "<<cum<<"\n";L.swap(NX);}long long W=accumulate(win.begin(),win.end(),0LL);cout<<"VALID "<<validCount<<" WINS "<<W<<" DRAWS "<<validCount-W<<" MAXRANK "<<r-1<<" EDGES "<<E<<"\n";
   FILE*f=fopen("/mnt/data/g2_k2p_rank.bin","wb");fwrite(rank.data(),sizeof(int16_t),rank.size(),f);fclose(f);
 }
};
int main(){KPK kc(3),kd(4);K2P x(kc,kd);}
