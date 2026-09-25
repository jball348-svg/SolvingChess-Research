#include <bits/stdc++.h>
using namespace std;

static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;}
static inline int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
vector<int> bsqs; int bindex_[64];
static inline int enc(int wk,int wb,int wpidx,int bk,int stm){return ((((wk*32+bindex_[wb])*6+wpidx)*64+bk)*2+stm);} 
static inline void dec(int id,int &wk,int &wb,int &wpidx,int &bk,int &stm){
 stm=id%2; id/=2; bk=id%64; id/=64; wpidx=id%6; id/=6; int bi=id%32; id/=32; wk=id; wb=bsqs[bi];
}
static inline bool pawn_att(int wp,int t){int f=F(wp),r=R(wp),tf=F(t),tr=R(t);return tr==r+1 && abs(tf-f)==1;}
static inline bool bishop_att(int wb,int t,int wk,int wp){
 int df=F(t)-F(wb),dr=R(t)-R(wb); if(df==0||abs(df)!=abs(dr)) return false; int sf=df>0?1:-1,sr=dr>0?1:-1; int f=F(wb)+sf,r=R(wb)+sr;
 while(f!=F(t)||r!=R(t)){int s=r*8+f; if(s==wk||s==wp) return false; f+=sf;r+=sr;} return true;
}
static inline bool valid4(int wk,int wb,int wp,int bk,int stm){
 if(wk==wb||wk==wp||wk==bk||wb==wp||wb==bk||wp==bk) return false; if(cheb(wk,bk)<=1) return false;
 if(stm==0){ if(pawn_att(wp,bk)) return false; if(bishop_att(wb,bk,wk,wp)) return false; }
 return true;
}

// Generate legal successors in original conservative model. Internal valid successors pushed; exits increase total.
static inline void gen(int wk,int wb,int wpidx,int bk,int stm, vector<int>& succ, int &total){
 succ.clear(); total=0; int wp=15+8*wpidx;
 if(stm==0){ // white
   // king
   for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++) if(df||dr){int nf=F(wk)+df,nr=R(wk)+dr; if(nf<0||nf>=8||nr<0||nr>=8)continue; int d=nr*8+nf; if(d==wb||d==wp||d==bk)continue; if(cheb(d,bk)<=1)continue; total++; if(valid4(d,wb,wp,bk,1)) succ.push_back(enc(d,wb,wpidx,bk,1));}
   // bishop slides
   const int D[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}};
   for(auto &q:D){int f=F(wb)+q[0],r=R(wb)+q[1]; while(f>=0&&f<8&&r>=0&&r<8){int d=r*8+f; if(d==wk||d==wp||d==bk) break; total++; if(valid4(wk,d,wp,bk,1)) succ.push_back(enc(wk,d,wpidx,bk,1)); f+=q[0];r+=q[1];}}
   // pawn pushes
   int r=R(wp);
   if(r==6){ // h7-h8 promotion exit, if h8 vacant
      int d=63; if(d!=wk&&d!=wb&&d!=bk) total++;
   } else {
      int d=wp+8; if(d!=wk&&d!=wb&&d!=bk){ total++; if(valid4(wk,wb,d,bk,1)) succ.push_back(enc(wk,wb,wpidx+1,bk,1));
        if(r==1){int d2=wp+16; if(d2!=wk&&d2!=wb&&d2!=bk){ total++; if(valid4(wk,wb,d2,bk,1)) succ.push_back(enc(wk,wb,wpidx+2,bk,1)); }}
      }
   }
 } else { // black king
   for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++) if(df||dr){int nf=F(bk)+df,nr=R(bk)+dr; if(nf<0||nf>=8||nr<0||nr>=8)continue; int d=nr*8+nf; if(d==wk)continue; if(cheb(wk,d)<=1)continue;
      bool capB=(d==wb), capP=(d==wp); // after capture, test attacks from remaining white units
      if(!capP && pawn_att(wp,d)) continue;
      if(!capB){int p2=capP?-1:wp; // bishop line blockers include wk and pawn if present
        int df2=F(d)-F(wb),dr2=R(d)-R(wb); bool batt=false;
        if(df2!=0&&abs(df2)==abs(dr2)){int sf=df2>0?1:-1,sr=dr2>0?1:-1;int f=F(wb)+sf,r=R(wb)+sr;batt=true;while(f!=F(d)||r!=R(d)){int s=r*8+f;if(s==wk||(p2>=0&&s==p2)){batt=false;break;}f+=sf;r+=sr;}}
        if(batt) continue;
      }
      total++;
      if(capB||capP) continue; // conservative unsafe exit
      if(valid4(wk,wb,wp,d,0)) succ.push_back(enc(wk,wb,wpidx,d,0));
   }
 }
}

int main(){
 memset(bindex_,-1,sizeof(bindex_)); for(int s=0;s<64;s++) if(((F(s)+R(s))&1)==1){bindex_[s]=bsqs.size();bsqs.push_back(s);} 
 const int N=64*32*6*64*2; vector<uint8_t> valid(N,0), stmarr(N,0); vector<int> valid_ids; valid_ids.reserve(1200000);
 long long raw=N, vc=0, seedc=0;
 for(int wk=0;wk<64;wk++)for(int bi=0;bi<32;bi++){int wb=bsqs[bi];for(int pi=0;pi<6;pi++){int wp=15+8*pi;for(int bk=0;bk<64;bk++)for(int stm=0;stm<2;stm++){int id=((((wk*32+bi)*6+pi)*64+bk)*2+stm); if(valid4(wk,wb,wp,bk,stm)){valid[id]=1;stmarr[id]=stm;valid_ids.push_back(id);vc++;if(bk==63)seedc++;}}}}
 cerr<<"raw "<<raw<<" valid "<<vc<<" seed "<<seedc<<"\n";
 // Build CSR predecessor graph, and total legal move count.
 vector<uint32_t> indeg(N,0); vector<uint16_t> total(N,0); vector<int> succ; succ.reserve(32);
 long long edges=0;
 for(int id:valid_ids){int wk,wb,pi,bk,stm;dec(id,wk,wb,pi,bk,stm);int t;gen(wk,wb,pi,bk,stm,succ,t);total[id]=t; for(int d:succ){indeg[d]++;edges++;}}
 cerr<<"internal edges "<<edges<<"\n";
 vector<uint32_t> off(N+1,0); for(int i=0;i<N;i++) off[i+1]=off[i]+indeg[i]; vector<uint32_t> cur=off; vector<uint32_t> preds(edges);
 for(int id:valid_ids){int wk,wb,pi,bk,stm;dec(id,wk,wb,pi,bk,stm);int t;gen(wk,wb,pi,bk,stm,succ,t);for(int d:succ)preds[cur[d]++]=id;}
 vector<int16_t> rank(N,-1); vector<uint16_t> rem=total; vector<int> layer, next; layer.reserve(seedc);
 for(int id:valid_ids){int wk,wb,pi,bk,stm;dec(id,wk,wb,pi,bk,stm); if(bk==63){rank[id]=0;layer.push_back(id);}}
 cout<<"rank 0 "<<layer.size()<<" cumulative "<<layer.size()<<"\n"; long long cum=layer.size(); int r=0;
 // To ensure white remaining excludes unsafe exits: rem starts total; decrement only internal successors that enter attractor. if reaches 0 all legal moves are attr and no exits.
 while(!layer.empty()){
   next.clear(); r++;
   for(int d:layer){for(uint32_t k=off[d];k<off[d+1];k++){int p=preds[k]; if(rank[p]>=0)continue; if(stmarr[p]==1){rank[p]=r;next.push_back(p);} else {if(rem[p]>0) rem[p]--; if(rem[p]==0 && total[p]>0){rank[p]=r;next.push_back(p);}}}}
   if(next.empty()){cout<<"rank "<<r<<" 0 cumulative "<<cum<<"\n";break;} cum+=next.size(); cout<<"rank "<<r<<" "<<next.size()<<" cumulative "<<cum<<"\n"; layer.swap(next);
 }
 return 0;
}
