#include <bits/stdc++.h>
using namespace std;
int F(int s){return s&7;} int R(int s){return s>>3;} int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
bool rookAtk(int ro,int sq,int wk,int bk){
 if(F(ro)==F(sq)){int step=(sq>ro?8:-8); for(int x=ro+step;x!=sq;x+=step) if(x==wk||x==bk) return false; return true;}
 if(R(ro)==R(sq)){int step=(sq>ro?1:-1); for(int x=ro+step;x!=sq;x+=step) if(x==wk||x==bk) return false; return true;}
 return false;
}
int enc(int wk,int ro,int bk,int t){return (((wk*64+ro)*64+bk)<<1)|t;}
void dec(int c,int&wk,int&ro,int&bk,int&t){t=c&1;c>>=1;bk=c%64;c/=64;ro=c%64;c/=64;wk=c;}
bool validState(int wk,int ro,int bk,int t){
 if(wk==ro||wk==bk||ro==bk||cheb(wk,bk)<=1) return false;
 // Static-valid convention: side not to move cannot already be in check.
 if(t==0 && rookAtk(ro,bk,wk,bk)) return false; // White to move => Black (not-to-move) not in check.
 return true;
}
void succ(int wk,int ro,int bk,int t, vector<int>&out, bool &externalDraw){
 out.clear(); externalDraw=false;
 if(t==0){
   // WK moves.
   for(int dr=-1;dr<=1;dr++)for(int df=-1;df<=1;df++)if(dr||df){int nr=R(wk)+dr,nf=F(wk)+df;if(nr<0||nr>7||nf<0||nf>7)continue;int nw=nr*8+nf;if(nw==ro||nw==bk||cheb(nw,bk)<=1)continue;int c=enc(nw,ro,bk,1);if(validState(nw,ro,bk,1))out.push_back(c);}
   // Rook moves, cannot capture king.
   const int dirs[4]={1,-1,8,-8};
   for(int d:dirs){int x=ro;while(true){int y=x+d;if(y<0||y>=64)break;if((d==1||d==-1)&&R(y)!=R(x))break;x=y;if(x==wk||x==bk)break;int c=enc(wk,x,bk,1);if(validState(wk,x,bk,1))out.push_back(c);} }
 } else {
   // BK moves; capture rook is external K vs K draw if legal.
   for(int dr=-1;dr<=1;dr++)for(int df=-1;df<=1;df++)if(dr||df){int nr=R(bk)+dr,nf=F(bk)+df;if(nr<0||nr>7||nf<0||nf>7)continue;int nb=nr*8+nf;if(nb==wk||cheb(nb,wk)<=1)continue;
      if(nb==ro){externalDraw=true; continue;}
      if(rookAtk(ro,nb,wk,nb)) continue;
      int c=enc(wk,ro,nb,0);if(validState(wk,ro,nb,0))out.push_back(c);
   }
 }
}
int main(){
 const int SZ=64*64*64*2; vector<unsigned char> valid(SZ),win(SZ); vector<int16_t> dist(SZ,-1); long long nv=0,vw=0,vb=0; vector<int> out;
 for(int wk=0;wk<64;wk++)for(int ro=0;ro<64;ro++)for(int bk=0;bk<64;bk++)for(int t=0;t<2;t++){int c=enc(wk,ro,bk,t);if(validState(wk,ro,bk,t)){valid[c]=1;nv++;if(t==0)vw++;else vb++;}}
 // Seed Black-to-move checkmates.
 long long mates=0,stales=0;
 for(int c=0;c<SZ;c++)if(valid[c]){int wk,ro,bk,t;dec(c,wk,ro,bk,t);if(t!=1)continue;bool ed=false;succ(wk,ro,bk,t,out,ed);if(out.empty()&&!ed){if(rookAtk(ro,bk,wk,bk)){win[c]=1;dist[c]=0;mates++;}else stales++;}}
 int rounds=0; bool ch=true;
 while(ch){ch=false;rounds++; for(int c=0;c<SZ;c++)if(valid[c]&&!win[c]){int wk,ro,bk,t;dec(c,wk,ro,bk,t);bool ed=false;succ(wk,ro,bk,t,out,ed);if(t==0){int best=1e9;for(int s:out)if(win[s])best=min(best,(int)dist[s]);if(best<1e9){win[c]=1;dist[c]=best+1;ch=true;}}
 else {if(ed||out.empty())continue;bool all=true;int mx=-1;for(int s:out){if(!win[s]){all=false;break;}mx=max(mx,(int)dist[s]);}if(all){win[c]=1;dist[c]=mx+1;ch=true;}}
 } }
 long long W=0,D=0,wtm=0,wtmW=0,btm=0,btmW=0;int maxd=0;vector<tuple<int,int,int>> wtmDraws;
 for(int c=0;c<SZ;c++)if(valid[c]){int wk,ro,bk,t;dec(c,wk,ro,bk,t);if(win[c]){W++;maxd=max(maxd,(int)dist[c]);}else D++;if(t==0){wtm++;if(win[c])wtmW++;else if(wtmDraws.size()<20)wtmDraws.push_back({wk,ro,bk});}else{btm++;if(win[c])btmW++;}}
 cout<<"KRK valid="<<nv<<" W="<<W<<" D="<<D<<" mates="<<mates<<" stalemates="<<stales<<" maxdist="<<maxd<<" rounds="<<rounds<<"\n";
 cout<<"WTM valid="<<wtm<<" W="<<wtmW<<" D="<<(wtm-wtmW)<<"; BTM valid="<<btm<<" W="<<btmW<<" D="<<(btm-btmW)<<"\n";
 if(!wtmDraws.empty()){cout<<"WTM draw samples:";for(auto [wk,ro,bk]:wtmDraws)cout<<" ("<<wk<<","<<ro<<","<<bk<<")";cout<<"\n";}
}
