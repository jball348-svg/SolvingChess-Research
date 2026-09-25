#define main g77_same_main
#include "/mnt/data/g7_7_same_side_backfire.cpp"
#undef main

static inline int kcode77(int pri,int wk,int bk,int t){return (((pri*64+wk)*64+bk)*2+t);} 
static inline void kdec77(int c,int &pri,int &wk,int &bk,int &t){t=c&1;int x=c>>1;bk=x%64;x/=64;wk=x%64;pri=x/64;}
struct K77{vector<uint8_t> valid,win;};
K77 solveK77(int file=3){
 int SZ=6*64*64*2;K77 K;K.valid.assign(SZ,0);K.win.assign(SZ,0);
 for(int pri=0;pri<6;pri++){int p=(pri+1)*8+file;for(int wk=0;wk<64;wk++)if(wk!=p)for(int bk=0;bk<64;bk++)if(bk!=p&&bk!=wk&&cheb(wk,bk)>1){K.valid[kcode77(pri,wk,bk,1)]=1;if(!pawnAttacks(p,bk))K.valid[kcode77(pri,wk,bk,0)]=1;}}
 auto succ=[&](int c,vector<int>&ss,int&tw,int&td){ss.clear();tw=td=0;int pri,wk,bk,t;kdec77(c,pri,wk,bk,t);int rank=pri+2,p=(rank-1)*8+file;if(t==0){for(int nw:kingMoves[wk])if(nw!=p&&nw!=bk&&cheb(nw,bk)>1){int z=kcode77(pri,nw,bk,1);if(K.valid[z])ss.push_back(z);}int q=p+8;if(q<64&&q!=wk&&q!=bk){if(rank==7)tw++;else{int z=kcode77(pri+1,wk,bk,1);if(K.valid[z])ss.push_back(z);}if(rank==2){int q2=p+16;if(q2!=wk&&q2!=bk){int z=kcode77(pri+2,wk,bk,1);if(K.valid[z])ss.push_back(z);}}}}else{for(int nb:kingMoves[bk]){if(nb==wk)continue;if(nb==p){if(cheb(nb,wk)>1)td++;continue;}if(cheb(nb,wk)<=1||pawnAttacks(p,nb))continue;int z=kcode77(pri,wk,nb,0);if(K.valid[z])ss.push_back(z);}}};
 vector<int> ss;int tw,td;vector<uint16_t> rem(SZ,0);deque<int>q;
 for(int c=0;c<SZ;c++)if(K.valid[c]){int pri,wk,bk,t;kdec77(c,pri,wk,bk,t);succ(c,ss,tw,td);if(t==0){if(tw){K.win[c]=1;q.push_back(c);}}else{if(ss.empty()&&tw==0&&td==0){int p=(pri+1)*8+file;if(pawnAttacks(p,bk)){K.win[c]=1;q.push_back(c);}}else{rem[c]=ss.size()+td;if(rem[c]==0){K.win[c]=1;q.push_back(c);}}}}
 auto preds=[&](int c,auto fn){int pri,wk,bk,t;kdec77(c,pri,wk,bk,t);int p=(pri+1)*8+file;if(t==1){for(int pw:kingMoves[wk])if(pw!=p&&pw!=bk){int z=kcode77(pri,pw,bk,0);if(K.valid[z])fn(z);}if(pri>0){int z=kcode77(pri-1,wk,bk,0);if(K.valid[z])fn(z);}if(pri==2){int mid=2*8+file;if(mid!=wk&&mid!=bk){int z=kcode77(0,wk,bk,0);if(K.valid[z])fn(z);}}}else{for(int pb:kingMoves[bk])if(pb!=wk&&pb!=p){int z=kcode77(pri,wk,pb,1);if(K.valid[z])fn(z);}}};
 while(!q.empty()){int z=q.front();q.pop_front();preds(z,[&](int p){if(K.win[p])return;int pri,wk,bk,t;kdec77(p,pri,wk,bk,t);if(t==0){K.win[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){K.win[p]=1;q.push_back(p);}});}return K;
}

struct TruthStats{long long W=0,D=0;vector<uint8_t> win;};
TruthStats solveTruth(const Arena&A,const K77&K){TruthStats T;T.win.assign(A.SZ,0);vector<uint16_t>rem(A.SZ,0);deque<int>q;
 auto classifyBlack=[&](int c,int &ew,int &ed){ew=ed=0;int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);int p=A.pawn(pri);for(int nb:kingMoves[bk]){if(nb==wk)continue;if(nb==p){if(cheb(nb,wk)<=1||A.mattAfterPawnGone(m,nb,wk))continue;if(A.pt==ROOK)ew++; else ed++;continue;}if(nb==m){if(cheb(nb,wk)<=1||pawnAttacks(p,nb))continue;int kp=A.ranks[pri]-2;int kc=kcode77(kp,wk,nb,0);if(kc>=0&&kc<(int)K.valid.size()&&K.valid[kc]&&K.win[kc])ew++;else ed++;continue;}}};
 for(int c=0;c<A.SZ;c++)if(A.valid[c]){int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);auto s=A.succ(c);if(t==0){if(s.ext){T.win[c]=1;q.push_back(c);}}else{int ew,ed;classifyBlack(c,ew,ed);if(s.in.empty()&&ew==0&&ed==0){if(A.incheck(pri,wk,m,bk)){T.win[c]=1;q.push_back(c);}}else{rem[c]=s.in.size()+ed;if(rem[c]==0){T.win[c]=1;q.push_back(c);}}}}
 while(!q.empty()){int z=q.front();q.pop_front();A.preds(z,[&](int p){if(T.win[p])return;int pri,wk,m,bk,t;dec4(p,pri,wk,m,bk,t);if(t==0){T.win[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){T.win[p]=1;q.push_back(p);}});}for(int c=0;c<A.SZ;c++)if(A.valid[c]){if(T.win[c])T.W++;else T.D++;}return T;}

int main(){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();auto K=solveK77(3);long long kv=count(K.valid.begin(),K.valid.end(),1),kw=count(K.win.begin(),K.win.end(),1);cerr<<"KPK static="<<kv<<" W="<<kw<<" D="<<(kv-kw)<<"\n";
 for(auto cfg:vector<pair<string,PType>>{{"N",KNIGHT},{"B",BISHOP}}){Arena A(cfg.second,{5,6,7},3);auto T=solveTruth(A,K);long long ante=0,fail=0,gante=0,gfail=0,removed=0,removedFail=0;int promo=59;for(int c=0;c<A.SZ;c++)if(A.valid[c]){int pri,wk,m,bk,t;dec4(c,pri,wk,m,bk,t);int kc=kcode77(A.ranks[pri]-2,wk,bk,t);if(!(kc>=0&&kc<(int)K.valid.size()&&K.valid[kc]&&K.win[kc]))continue;ante++;bool bad=!T.win[c];fail+=bad;bool guard=m!=promo;if(guard){gante++;gfail+=bad;}else{removed++;removedFail+=bad;}}
 cout<<cfg.first<<"-d5_7 static="<<T.W+T.D<<" W="<<T.W<<" D="<<T.D<<" rawAnte="<<ante<<" rawFail="<<fail<<" guardAnte="<<gante<<" guardFail="<<gfail<<" removedByPromoSquare="<<removed<<" removedFailures="<<removedFail<<"\n";
 }
 return 0;}
