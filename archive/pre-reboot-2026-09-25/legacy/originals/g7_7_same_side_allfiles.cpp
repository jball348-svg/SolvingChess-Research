#include <bits/stdc++.h>
using namespace std;
static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;}
static inline int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
vector<int> kingMoves[64], knightMoves[64];
void initMoves(){for(int s=0;s<64;s++){for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int f=F(s)+df,r=R(s)+dr;if(f>=0&&f<8&&r>=0&&r<8)kingMoves[s].push_back(r*8+f);}const int D[8][2]={{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};for(auto &d:D){int f=F(s)+d[0],r=R(s)+d[1];if(f>=0&&f<8&&r>=0&&r<8)knightMoves[s].push_back(r*8+f);}}}
static inline bool pawnAttacks(int p,int t){return R(t)-R(p)==1 && abs(F(t)-F(p))==1;}
bool sliderAtt(char typ,int a,int t,const vector<int>&block){int df=F(t)-F(a),dr=R(t)-R(a);int sf=0,sr=0;if(typ=='B'){if(df==0||abs(df)!=abs(dr))return false;sf=df>0?1:-1;sr=dr>0?1:-1;}else{if(df!=0&&dr!=0)return false;sf=(df>0)-(df<0);sr=(dr>0)-(dr<0);}int f=F(a)+sf,r=R(a)+sr;while(f!=F(t)||r!=R(t)){int q=r*8+f;for(int b:block)if(q==b)return false;f+=sf;r+=sr;}return true;}
enum PType{KNIGHT=0,BISHOP=1,ROOK=2};
static inline int code4(int pri,int wk,int m,int bk,int t){return ((((pri*64+wk)*64+m)*64+bk)*2+t);} 
static inline void dec4(int c,int &pri,int &wk,int &m,int &bk,int &t){t=c&1;int x=c>>1;bk=x%64;x/=64;m=x%64;x/=64;wk=x%64;pri=x/64;}
struct Arena{
 PType pt; vector<int> ranks; int file; int SZ; vector<uint8_t> valid;
 Arena(PType p, vector<int> rr,int f=3):pt(p),ranks(rr),file(f){SZ=ranks.size()*64*64*64*2;valid.assign(SZ,0);build();}
 int pawn(int pri)const{return (ranks[pri]-1)*8+file;}
 bool matt(int m,int q,int wk,int p)const{if(pt==KNIGHT)return find(knightMoves[m].begin(),knightMoves[m].end(),q)!=knightMoves[m].end();vector<int>b={wk,p};return sliderAtt(pt==BISHOP?'B':'R',m,q,b);}
 bool mattAfterPawnGone(int m,int q,int wk)const{if(pt==KNIGHT)return find(knightMoves[m].begin(),knightMoves[m].end(),q)!=knightMoves[m].end();vector<int>b={wk};return sliderAtt(pt==BISHOP?'B':'R',m,q,b);}
 bool incheck(int pri,int wk,int m,int bk)const{return pawnAttacks(pawn(pri),bk)||matt(m,bk,wk,pawn(pri));}
 bool validS(int pri,int wk,int m,int bk,int t)const{int p=pawn(pri);if(wk==p||m==p||bk==p||wk==m||wk==bk||m==bk||cheb(wk,bk)<=1)return false;if(t==0&&incheck(pri,wk,m,bk))return false;return true;}
 void build(){for(int pri=0;pri<(int)ranks.size();pri++)for(int wk=0;wk<64;wk++)for(int m=0;m<64;m++)for(int bk=0;bk<64;bk++)for(int t=0;t<2;t++)if(validS(pri,wk,m,bk,t))valid[code4(pri,wk,m,bk,t)]=1;}
 struct Succ{vector<int> in;int ext=0;};
 Succ succ(int c)const{int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);int p=pawn(pri);Succ o;if(t==0){
   for(int nw:kingMoves[wk])if(nw!=p&&nw!=m&&nw!=bk&&cheb(nw,bk)>1){int z=code4(pri,nw,m,bk,1);if(valid[z])o.in.push_back(z);} 
   int q=p+8;if(q<64&&q!=wk&&q!=m&&q!=bk){if(ranks[pri]==7)o.ext++;else if(pri+1<(int)ranks.size()&&ranks[pri+1]==ranks[pri]+1){int z=code4(pri+1,wk,m,bk,1);if(valid[z])o.in.push_back(z);}if(ranks[pri]==2){int q2=p+16;if(q2!=wk&&q2!=m&&q2!=bk){auto it=find(ranks.begin(),ranks.end(),4);if(it!=ranks.end()){int np=it-ranks.begin(),z=code4(np,wk,m,bk,1);if(valid[z])o.in.push_back(z);}}}}
   if(pt==KNIGHT){for(int nm:knightMoves[m])if(nm!=wk&&nm!=p&&nm!=bk){int z=code4(pri,wk,nm,bk,1);if(valid[z])o.in.push_back(z);}}
   else {int bd[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}},rd[4][2]={{1,0},{-1,0},{0,1},{0,-1}};auto ds=(pt==BISHOP?bd:rd);for(int i=0;i<4;i++){int f=F(m)+ds[i][0],r=R(m)+ds[i][1];while(f>=0&&f<8&&r>=0&&r<8){int nm=r*8+f;if(nm==wk||nm==p||nm==bk)break;int z=code4(pri,wk,nm,bk,1);if(valid[z])o.in.push_back(z);f+=ds[i][0];r+=ds[i][1];}}}
 } else {
   for(int nb:kingMoves[bk]){if(nb==wk)continue;if(nb==p){if(cheb(nb,wk)>1&&!mattAfterPawnGone(m,nb,wk))o.ext++;continue;}if(nb==m){if(cheb(nb,wk)>1&&!pawnAttacks(p,nb))o.ext++;continue;}if(cheb(nb,wk)<=1||pawnAttacks(p,nb)||matt(m,nb,wk,p))continue;int z=code4(pri,wk,m,nb,0);if(valid[z])o.in.push_back(z);} }
 return o;}
 template<class FN> void preds(int c,FN fn)const{int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);int p=pawn(pri);if(t==1){
   for(int pw:kingMoves[wk])if(pw!=p&&pw!=m&&pw!=bk){int z=code4(pri,pw,m,bk,0);if(valid[z])fn(z);} 
   if(pri>0&&ranks[pri-1]==ranks[pri]-1){int z=code4(pri-1,wk,m,bk,0);if(valid[z])fn(z);}if(ranks[pri]==4){auto it=find(ranks.begin(),ranks.end(),2);if(it!=ranks.end()){int pp=it-ranks.begin(),mid=2*8+file;if(mid!=wk&&mid!=m&&mid!=bk){int z=code4(pp,wk,m,bk,0);if(valid[z])fn(z);}}}
   if(pt==KNIGHT){for(int pm:knightMoves[m])if(pm!=wk&&pm!=p&&pm!=bk){int z=code4(pri,wk,pm,bk,0);if(valid[z])fn(z);}}
   else {int bd[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}},rd[4][2]={{1,0},{-1,0},{0,1},{0,-1}};auto ds=(pt==BISHOP?bd:rd);for(int i=0;i<4;i++){int f=F(m)+ds[i][0],r=R(m)+ds[i][1];while(f>=0&&f<8&&r>=0&&r<8){int pm=r*8+f;if(pm==wk||pm==p||pm==bk)break;int z=code4(pri,wk,pm,bk,0);if(valid[z])fn(z);f+=ds[i][0];r+=ds[i][1];}}}
 } else {for(int pb:kingMoves[bk])if(pb!=wk&&pb!=p&&pb!=m){int z=code4(pri,wk,m,pb,1);if(valid[z])fn(z);}}
 }
 bool commonTarget(int c)const{int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);int promo=56+file;return ranks[pri]>=6&&cheb(wk,promo)<=4&&cheb(bk,promo)>=5;}
 bool immediateStalemate(int c)const{int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);if(t!=1)return false;auto s=succ(c);return s.in.empty()&&s.ext==0&&!incheck(pri,wk,m,bk);}
 bool target(int c)const{return commonTarget(c)&&!immediateStalemate(c);}
 vector<uint8_t> attr(bool filtered)const{vector<uint8_t>A(SZ,0);vector<int>rem(SZ,0);deque<int>q;for(int c=0;c<SZ;c++)if(valid[c]&&target(c)){A[c]=1;q.push_back(c);}for(int c=0;c<SZ;c++)if(valid[c]&&!A[c]){int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);if(t==1){auto s=succ(c);rem[c]=s.in.size()+s.ext;}}
   while(!q.empty()){int z=q.front();q.pop_front();bool zTarget=target(z);int pri,wk,m,bk,t;dec4(z,pri,wk,m,bk,t);bool zCheck=(t==1&&incheck(pri,wk,m,bk));preds(z,[&](int p){if(A[p])return;int ppri,pwk,pm,pbk,ptm;dec4(p,ppri,pwk,pm,pbk,ptm);if(ptm==0){if(!filtered||zTarget||zCheck){A[p]=1;q.push_back(p);}}else if(rem[p]>0&&--rem[p]==0){A[p]=1;q.push_back(p);}});}return A;}
 void run(const string&name)const{auto A=attr(false),C=attr(true);long long tg=0,na=0,nc=0;for(int c=0;c<SZ;c++)if(valid[c]){tg+=target(c);na+=A[c];nc+=C[c];}
   vector<uint8_t>K(SZ,0),Rset(SZ,0);long long kp=0;map<string,long long> cats;for(int c=0;c<SZ;c++)if(valid[c]&&A[c]&&!C[c]){int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);if(t!=0)continue;auto s=succ(c);bool any=false,kg=false,pg=false,mg=false;for(int z:s.in)if(C[z]&&!target(z)){int zpri,zwk,zm,zbk,zt;dec4(z,zpri,zwk,zm,zbk,zt);if(!(zt==1&&incheck(zpri,zwk,zm,zbk))){any=true;if(zwk!=wk)kg=true;else if(zpri!=pri)pg=true;else if(zm!=m)mg=true;}}if(any){K[c]=Rset[c]=1;kp++;string key=string(kg?"K":"")+(pg?"P":"")+(mg?"M":"");cats[key]++;}}
   vector<int>rem(SZ,0);for(int c=0;c<SZ;c++)if(valid[c]&&A[c]&&!C[c]&&!Rset[c]){int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);if(t==1){auto s=succ(c);int n=s.ext;for(int z:s.in)if(!C[z])n++;rem[c]=n;}}
   deque<int>q;for(int c=0;c<SZ;c++)if(Rset[c])q.push_back(c);while(!q.empty()){int z=q.front();q.pop_front();preds(z,[&](int p){if(!A[p]||C[p]||Rset[p])return;int pri,wk,m,bk,t;dec4(p,pri,wk,m,bk,t);if(t==0){Rset[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){Rset[p]=1;q.push_back(p);}});}long long qn=0,missing=0,extra=0;for(int c=0;c<SZ;c++)if(valid[c]){bool qv=A[c]&&!C[c];qn+=qv;if(qv&&!Rset[c])missing++;if(Rset[c]&&!qv)extra++;}
   cout<<name<<" static="<<count(valid.begin(),valid.end(),1)<<" target="<<tg<<" attr="<<na<<" check="<<nc<<" retained_pct="<<fixed<<setprecision(6)<<(na?100.0*nc/na:0)<<" quiet_required="<<qn<<" pivots="<<kp<<" amp="<<(kp?double(qn)/kp:0)<<" missing="<<missing<<" extra="<<extra<<" cats=";for(auto &kv:cats)cout<<kv.first<<":"<<kv.second<<",";cout<<"\n";
 }
};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();for(int ff=0;ff<8;ff++){for(auto x:vector<pair<string,PType>>{{"N",KNIGHT},{"B",BISHOP},{"R",ROOK}}){Arena a(x.second,{5,6,7},ff);string nm=x.first+string("-")+char('a'+ff)+"5_7";a.run(nm);}}return 0;}
