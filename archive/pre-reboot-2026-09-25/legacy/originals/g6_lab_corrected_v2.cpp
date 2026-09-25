#include <bits/stdc++.h>
using namespace std;

static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;}
static inline int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
vector<int> kingMoves[64], knightMoves[64];

void initMoves(){
 for(int s=0;s<64;s++){
  for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int ff=F(s)+df, rr=R(s)+dr; if(ff>=0&&ff<8&&rr>=0&&rr<8) kingMoves[s].push_back(rr*8+ff);} 
  const int D[8][2]={{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};
  for(auto &d:D){int ff=F(s)+d[0],rr=R(s)+d[1]; if(ff>=0&&ff<8&&rr>=0&&rr<8) knightMoves[s].push_back(rr*8+ff);} 
 }
}
static inline bool pawnAttacks(int p,int t){int dr=R(t)-R(p), df=abs(F(t)-F(p)); return dr==1 && df==1;}

bool bishopAttacks(int b,int t,int wk,int p,int bk){
 int df=F(t)-F(b),dr=R(t)-R(b); if(df==0||abs(df)!=abs(dr)) return false; int sf=df>0?1:-1,sr=dr>0?1:-1;
 int ff=F(b)+sf,rr=R(b)+sr; while(ff!=F(t)||rr!=R(t)){int s=rr*8+ff; if(s==wk||s==p||s==bk) return false; ff+=sf;rr+=sr;} return true;
}
bool bishopAttacksAfterBlackMove(int b,int t,int wk,int p){
 // target is black king square; occupancies before target are wk,p only (bishop excluded at origin)
 int df=F(t)-F(b),dr=R(t)-R(b); if(df==0||abs(df)!=abs(dr)) return false; int sf=df>0?1:-1,sr=dr>0?1:-1;
 int ff=F(b)+sf,rr=R(b)+sr; while(ff!=F(t)||rr!=R(t)){int s=rr*8+ff; if(s==wk||s==p) return false; ff+=sf;rr+=sr;} return true;
}

// ---------- KPK d-file full ranks 2..7 ----------
static inline int kcode(int pri,int wk,int bk,int turn){return (((pri*64+wk)*64+bk)*2+turn);} 
static inline void kdecode(int c,int &pri,int &wk,int &bk,int &turn){turn=c&1;int x=c>>1;bk=x%64;x/=64;wk=x%64;pri=x/64;}
struct KPK { vector<uint8_t> valid,win; vector<int16_t> dist; int W=0,D=0,maxr=0; };

KPK solveKPK(int file=3){
 const int SZ=6*64*64*2; KPK K; K.valid.assign(SZ,0); K.win.assign(SZ,0); K.dist.assign(SZ,-1);
 for(int pri=0;pri<6;pri++){int rank=pri+2,p=(rank-1)*8+file; for(int wk=0;wk<64;wk++) if(wk!=p) for(int bk=0;bk<64;bk++) if(bk!=p&&bk!=wk&&cheb(wk,bk)>1){K.valid[kcode(pri,wk,bk,1)]=1; if(!pawnAttacks(p,bk))K.valid[kcode(pri,wk,bk,0)]=1;}}
 auto succ=[&](int c, vector<int>& ss,int &tw,int &td){ss.clear();tw=td=0;int pri,wk,bk,turn;kdecode(c,pri,wk,bk,turn);int rank=pri+2,p=(rank-1)*8+file; if(!turn){
   for(int nw:kingMoves[wk]) if(nw!=p&&nw!=bk&&cheb(nw,bk)>1){int nc=kcode(pri,nw,bk,1); if(K.valid[nc])ss.push_back(nc);} 
   int q=p+8; if(q<64&&q!=wk&&q!=bk){ if(rank==7)tw++; else {int nc=kcode(pri+1,wk,bk,1);if(K.valid[nc])ss.push_back(nc);} if(rank==2){int q2=p+16;if(q2!=wk&&q2!=bk){int nc=kcode(pri+2,wk,bk,1);if(K.valid[nc])ss.push_back(nc);}} }
  } else {
   for(int nb:kingMoves[bk]){ if(nb==wk)continue; if(nb==p){if(cheb(nb,wk)>1)td++; continue;} if(cheb(nb,wk)<=1||pawnAttacks(p,nb))continue; int nc=kcode(pri,wk,nb,0); if(K.valid[nc])ss.push_back(nc);} }
 };
 vector<int> codes;codes.reserve(42000);for(int c=0;c<SZ;c++)if(K.valid[c])codes.push_back(c); vector<int> ss;int tw,td;
 for(int c:codes){int pri,wk,bk,turn;kdecode(c,pri,wk,bk,turn);if(turn){succ(c,ss,tw,td);if(ss.empty()&&!tw&&!td){int p=(pri+1)*8+file; if(pawnAttacks(p,bk)){K.win[c]=1;K.dist[c]=0;}}}}
 bool ch=true;int pass=0;while(ch&&pass<100){ch=false;pass++;for(int c:codes)if(!K.win[c]){succ(c,ss,tw,td);int pri,wk,bk,turn;kdecode(c,pri,wk,bk,turn);if(!turn){int best=1e9;if(tw)best=0;for(int s:ss)if(K.win[s])best=min(best,(int)K.dist[s]);if(best<1e9){K.win[c]=1;K.dist[c]=best+1;ch=true;}}else{int total=ss.size()+tw+td;if(total&&td==0){bool all=true;int mx=0;for(int s:ss){if(!K.win[s]){all=false;break;}mx=max(mx,(int)K.dist[s]);}if(all){K.win[c]=1;K.dist[c]=mx+1;ch=true;}}}}}
 for(int c:codes)if(K.win[c]){K.W++;K.maxr=max(K.maxr,(int)K.dist[c]);}K.D=codes.size()-K.W; return K;
}

// ---------- G5-style K+minor+d-pawn vs K, pawn rank band ----------
enum PType{KNIGHT=0,BISHOP=1,ROOK=2};
static inline int gcode(int pri,int wk,int m,int bk,int turn){return ((((pri*64+wk)*64+m)*64+bk)*2+turn);} 
static inline void gdecode(int c,int &pri,int &wk,int &m,int &bk,int &turn){turn=c&1;int x=c>>1;bk=x%64;x/=64;m=x%64;x/=64;wk=x%64;pri=x/64;}

bool rookAttacksAfterBlackMove(int ro,int t,int wk,int p){
 if(F(ro)!=F(t)&&R(ro)!=R(t))return false;int sf=(F(t)>F(ro))-(F(t)<F(ro)),sr=(R(t)>R(ro))-(R(t)<R(ro));int ff=F(ro)+sf,rr=R(ro)+sr;while(ff!=F(t)||rr!=R(t)){int s=rr*8+ff;if(s==wk||s==p)return false;ff+=sf;rr+=sr;}return true;
}
bool rookAttacks(int ro,int t,int wk,int p,int bk){
 if(F(ro)!=F(t)&&R(ro)!=R(t))return false;int sf=(F(t)>F(ro))-(F(t)<F(ro)),sr=(R(t)>R(ro))-(R(t)<R(ro));int ff=F(ro)+sf,rr=R(ro)+sr;while(ff!=F(t)||rr!=R(t)){int s=rr*8+ff;if(s==wk||s==p||s==bk)return false;ff+=sf;rr+=sr;}return true;
}

struct ArenaResult{long long valid=0,W=0,D=0;int maxr=0;long long target=0,targetBad=0,targetAttr=0;long long restorationAnte=0,restFail=0,restStalemate=0; vector<uint8_t> validMask,winMask; vector<int16_t> dist;};

struct G5Arena{
 PType pt; vector<int> ranks; int file=3; int SZ; const KPK* K;
 vector<uint8_t> valid;
 G5Arena(PType t, vector<int> rr,const KPK* kk,int ff=3):pt(t),ranks(rr),file(ff),K(kk){SZ=ranks.size()*64*64*64*2;valid.assign(SZ,0);buildValid();}
 bool minorAttacksBK(int m,int bk,int wk,int p) const {if(pt==KNIGHT)return find(knightMoves[m].begin(),knightMoves[m].end(),bk)!=knightMoves[m].end(); if(pt==BISHOP)return bishopAttacks(m,bk,wk,p,bk); return rookAttacks(m,bk,wk,p,bk);} 
 bool minorAttacksSquareAfter(int m,int t,int wk,int p) const {if(pt==KNIGHT)return find(knightMoves[m].begin(),knightMoves[m].end(),t)!=knightMoves[m].end(); if(pt==BISHOP)return bishopAttacksAfterBlackMove(m,t,wk,p); return rookAttacksAfterBlackMove(m,t,wk,p);} 
 void buildValid(){for(int pri=0;pri<(int)ranks.size();pri++){int p=(ranks[pri]-1)*8+file;for(int wk=0;wk<64;wk++)if(wk!=p)for(int bk=0;bk<64;bk++)if(bk!=p&&bk!=wk&&cheb(wk,bk)>1)for(int m=0;m<64;m++)if(m!=p&&m!=wk&&m!=bk){int cb=gcode(pri,wk,m,bk,1);valid[cb]=1;bool chk=pawnAttacks(p,bk)||minorAttacksBK(m,bk,wk,p);if(!chk)valid[gcode(pri,wk,m,bk,0)]=1;}}}
 bool blackInCheck(int pri,int wk,int m,int bk) const {int p=(ranks[pri]-1)*8+file;return pawnAttacks(p,bk)||minorAttacksBK(m,bk,wk,p);} 
 // KPK lookup after minor capture; assumes d-file and ranks 2..7 K table
 bool kpkWinAfterMinorCapture(int pri,int wk,int nbk) const {int rank=ranks[pri];int kpri=rank-2;int c=kcode(kpri,wk,nbk,0);return c>=0&&c<(int)K->valid.size()&&K->valid[c]&&K->win[c];}
 int kpkDistAfterMinorCapture(int pri,int wk,int nbk) const {int rank=ranks[pri];int c=kcode(rank-2,wk,nbk,0);return (c>=0&&c<(int)K->dist.size())?K->dist[c]:-1;}

 void whiteSucc(int c, vector<int>& ss,int &termW) const {ss.clear();termW=0;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int p=(ranks[pri]-1)*8+file;
   for(int nw:kingMoves[wk]) if(nw!=p&&nw!=m&&nw!=bk&&cheb(nw,bk)>1){int nc=gcode(pri,nw,m,bk,1);if(valid[nc])ss.push_back(nc);} 
   int q=p+8;if(q<64&&q!=wk&&q!=m&&q!=bk){if(ranks[pri]==7)termW++;else if(pri+1<(int)ranks.size()&&ranks[pri+1]==ranks[pri]+1){int nc=gcode(pri+1,wk,m,bk,1);if(valid[nc])ss.push_back(nc);} if(ranks[pri]==2){int q2=p+16;if(q2!=wk&&q2!=m&&q2!=bk){auto it=find(ranks.begin(),ranks.end(),4);if(it!=ranks.end()){int npri=int(it-ranks.begin());int nc=gcode(npri,wk,m,bk,1);if(valid[nc])ss.push_back(nc);}}} }
   if(pt==KNIGHT){for(int nm:knightMoves[m])if(nm!=wk&&nm!=p&&nm!=bk){int nc=gcode(pri,wk,nm,bk,1);if(valid[nc])ss.push_back(nc);}}
   else { const int dirs[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}}; const int rdirs[4][2]={{1,0},{-1,0},{0,1},{0,-1}}; auto &dirs2=(pt==BISHOP?dirs:rdirs); for(int di=0;di<4;di++){int ff=F(m)+dirs2[di][0],rr=R(m)+dirs2[di][1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int nm=rr*8+ff;if(nm==wk||nm==p||nm==bk)break;int nc=gcode(pri,wk,nm,bk,1);if(valid[nc])ss.push_back(nc);ff+=dirs2[di][0];rr+=dirs2[di][1];}} }
 }
 void blackSucc(int c, vector<int>& ss,int &extW,int &extWmax,int &extDraw) const {ss.clear();extW=extDraw=0;extWmax=0;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int p=(ranks[pri]-1)*8+file;
   for(int nb:kingMoves[bk]){if(nb==wk)continue; if(nb==p){ // capture pawn -> K+minor vs K draw; ensure safe from wk and minor after pawn gone
       if(cheb(nb,wk)<=1)continue; bool matt=false;if(pt==KNIGHT)matt=find(knightMoves[m].begin(),knightMoves[m].end(),nb)!=knightMoves[m].end();else if(pt==BISHOP){int df=F(nb)-F(m),dr=R(nb)-R(m);if(df&&abs(df)==abs(dr)){int sf=df>0?1:-1,sr=dr>0?1:-1,ff=F(m)+sf,rr=R(m)+sr;matt=true;while(ff!=F(nb)||rr!=R(nb)){int s=rr*8+ff;if(s==wk){matt=false;break;}ff+=sf;rr+=sr;}}}else{if(F(nb)==F(m)||R(nb)==R(m)){int sf=(F(nb)>F(m))-(F(nb)<F(m)),sr=(R(nb)>R(m))-(R(nb)<R(m)),ff=F(m)+sf,rr=R(m)+sr;matt=true;while(ff!=F(nb)||rr!=R(nb)){int s=rr*8+ff;if(s==wk){matt=false;break;}ff+=sf;rr+=sr;}}} if(!matt){ if(pt==ROOK){extW++;extWmax=max(extWmax,0);} else extDraw++; } continue; }
     if(nb==m){ // capture minor -> KPK
       if(cheb(nb,wk)<=1||pawnAttacks(p,nb))continue; if(kpkWinAfterMinorCapture(pri,wk,nb)){extW++;extWmax=max(extWmax,kpkDistAfterMinorCapture(pri,wk,nb));}else extDraw++; continue; }
     if(cheb(nb,wk)<=1||pawnAttacks(p,nb)||minorAttacksSquareAfter(m,nb,wk,p))continue; int nc=gcode(pri,wk,m,nb,0);if(valid[nc])ss.push_back(nc);
   }
 }

 template<class FPred> void forPred(int c,FPred fn) const {int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int p=(ranks[pri]-1)*8+file; if(t==1){ // current black, previous white
    for(int pw:kingMoves[wk]) if(pw!=p&&pw!=m&&pw!=bk){int pc=gcode(pri,pw,m,bk,0);if(valid[pc])fn(pc);} 
    if(pri>0&&ranks[pri-1]==ranks[pri]-1){int pc=gcode(pri-1,wk,m,bk,0);if(valid[pc])fn(pc);} 
    // Reverse the legal initial two-square pawn push (rank 2 -> rank 4).
    if(ranks[pri]==4){auto it=find(ranks.begin(),ranks.end(),2);if(it!=ranks.end()){int p2=int(it-ranks.begin());int mid=2*8+file; // rank-3 square
      if(mid!=wk&&mid!=m&&mid!=bk){int pc=gcode(p2,wk,m,bk,0);if(valid[pc])fn(pc);}}}
    if(pt==KNIGHT){for(int pm:knightMoves[m])if(pm!=wk&&pm!=p&&pm!=bk){int pc=gcode(pri,wk,pm,bk,0);if(valid[pc])fn(pc);}}
    else {const int bdirs[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}};const int rdirs[4][2]={{1,0},{-1,0},{0,1},{0,-1}};auto &ds=(pt==BISHOP?bdirs:rdirs);for(int di=0;di<4;di++){int ff=F(m)+ds[di][0],rr=R(m)+ds[di][1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int pm=rr*8+ff;if(pm==wk||pm==p||pm==bk)break;int pc=gcode(pri,wk,pm,bk,0);if(valid[pc])fn(pc);ff+=ds[di][0];rr+=ds[di][1];}}}
  } else { // current white, previous black
    for(int pb:kingMoves[bk]) if(pb!=wk&&pb!=p&&pb!=m){int pc=gcode(pri,wk,m,pb,1);if(valid[pc])fn(pc);} }
 }

 ArenaResult solveGame(bool keepMasks=true) const {ArenaResult A;A.valid=count(valid.begin(),valid.end(),1);vector<uint8_t> win(SZ,0);vector<int16_t> dist(SZ,-1);vector<uint8_t> rem(SZ,0);deque<int> q;vector<int> ss;int tw,ew,ewm,ed;
   // initialize outdegrees and terminal wins
   for(int c=0;c<SZ;c++)if(valid[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(!t){whiteSucc(c,ss,tw);if(tw){win[c]=1;dist[c]=1;q.push_back(c);}}
    else {blackSucc(c,ss,ew,ewm,ed);int non=ss.size()+ed; // external wins excluded
      if(ss.empty()&&ew==0&&ed==0){if(blackInCheck(pri,wk,m,bk)){win[c]=1;dist[c]=0;q.push_back(c);} }
      else {rem[c]=(uint8_t)min(255,non); if(non==0){win[c]=1;dist[c]=ewm+1;q.push_back(c);} }
    }}
   while(!q.empty()){int s=q.front();q.pop_front();forPred(s,[&](int p){if(win[p])return;int pri,wk,m,bk,t;gdecode(p,pri,wk,m,bk,t);if(!t){win[p]=1;dist[p]=dist[s]+1;q.push_back(p);}else{if(rem[p]>0)rem[p]--;if(rem[p]==0){ // need max distance for black later; placeholder
          win[p]=1;dist[p]=dist[s]+1;q.push_back(p);}}});}
   // recompute minimax distances on frozen winning set to stable exact ranks
   fill(dist.begin(),dist.end(),-1);bool ch=true;int passes=0;while(ch&&passes<100){ch=false;passes++;for(int c=0;c<SZ;c++)if(valid[c]&&win[c]&&dist[c]<0){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(!t){whiteSucc(c,ss,tw);int best=1e9;if(tw)best=0;for(int s:ss)if(win[s]&&dist[s]>=0)best=min(best,(int)dist[s]);if(best<1e9){dist[c]=best+1;ch=true;}}
      else {blackSucc(c,ss,ew,ewm,ed);if(ss.empty()&&ew==0&&ed==0&&blackInCheck(pri,wk,m,bk)){dist[c]=0;ch=true;continue;} if(ed)continue;bool all=true;int mx=ew?ewm:-1;for(int s:ss){if(!win[s]||dist[s]<0){all=false;break;}mx=max(mx,(int)dist[s]);}if(all&&mx>=0){dist[c]=mx+1;ch=true;}} }}
   for(int c=0;c<SZ;c++)if(valid[c]){if(win[c]){A.W++;A.maxr=max(A.maxr,(int)dist[c]);}else A.D++;}if(keepMasks){A.validMask=valid;A.winMask=move(win);A.dist=move(dist);}return A;
 }

 bool commonTarget(int c) const {int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int rank=ranks[pri];int promo=7*8+file;return rank>=6 && cheb(wk,promo)<=4 && cheb(bk,promo)>=5;}
 bool immediateStalemate(int c) const {int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(!t)return false;vector<int> ss;int ew,ewm,ed;blackSucc(c,ss,ew,ewm,ed);return ss.empty()&&ew==0&&ed==0&&!blackInCheck(pri,wk,m,bk);}
 bool safeTarget(int c) const {return commonTarget(c)&&!immediateStalemate(c);}
 bool projectedKpkWin(int c) const {int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int rank=ranks[pri];int kc=kcode(rank-2,wk,bk,t);return kc>=0&&kc<(int)K->valid.size()&&K->valid[kc]&&K->win[kc];}
 bool safeInheritRook(int c) const {return pt==ROOK&&projectedKpkWin(c)&&!immediateStalemate(c);}
 long long countTarget(const vector<uint8_t>& truth,long long &bad) const {long long n=0;bad=0;for(int c=0;c<SZ;c++)if(valid[c]&&commonTarget(c)){n++;if(!truth[c])bad++;}return n;}
 vector<uint8_t> strictAttractor(function<bool(int)> target) const {vector<uint8_t> att(SZ,0);vector<uint8_t> rem(SZ,0);deque<int> q;vector<int> ss;int tw,ew,ewm,ed;
   for(int c=0;c<SZ;c++)if(valid[c]&&target(c)){att[c]=1;q.push_back(c);} 
   // for black states, all legal moves must stay internal and eventually hit target; all shortcut exits are failures, so include them in remaining forever
   for(int c=0;c<SZ;c++)if(valid[c]&&!att[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(t){blackSucc(c,ss,ew,ewm,ed);int total=ss.size()+ew+ed;rem[c]=(uint8_t)min(total,255);} }
   while(!q.empty()){int s=q.front();q.pop_front();forPred(s,[&](int p){if(att[p])return;int pri,wk,m,bk,t;gdecode(p,pri,wk,m,bk,t);if(!t){att[p]=1;q.push_back(p);}else if(rem[p]>0){rem[p]--;if(rem[p]==0){att[p]=1;q.push_back(p);}}});}
   return att;
 }
 void restorationStats(const vector<uint8_t>& truth,long long &ante,long long &fail,long long &stale) const {ante=fail=stale=0;vector<int> ss;int tw,ew,ewm,ed;for(int c=0;c<SZ;c++)if(valid[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int rank=ranks[pri];int kc=kcode(rank-2,wk,bk,t);if(kc>=0&&kc<(int)K->valid.size()&&K->valid[kc]&&K->win[kc]){ante++;if(!truth[c]){fail++; // immediate stalemate in full state = side to move black, no legal and not in check
      if(t==1){blackSucc(c,ss,ew,ewm,ed);if(ss.empty()&&ew==0&&ed==0&&!blackInCheck(pri,wk,m,bk))stale++;}
    }}}
 }
};

int main(int argc,char**argv){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();auto K=solveKPK(3);cout<<"KPK valid="<<K.W+K.D<<" W="<<K.W<<" D="<<K.D<<" maxr="<<K.maxr<<"\n";
 vector<pair<string,PType>> tests={{"N",KNIGHT},{"B",BISHOP}};if(argc>1&&string(argv[1])=="rook")tests={{"R",ROOK}};
 if(argc>1&&string(argv[1])=="restoreFarHeldout"){ for(int ff:vector<int>{0,1,2,4}){auto Kf=solveKPK(ff);for(auto [nm,typ]:vector<pair<string,PType>>{{"N",KNIGHT},{"B",BISHOP},{"R",ROOK}}){G5Arena A(typ,{2,3,4,5,6,7},&Kf,ff);auto T=A.solveGame(true);long long ante=0,bad=0,stale=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.projectedKpkWin(c)){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int p=(A.ranks[pri]-1)*8+ff;if(cheb(bk,p)<5||A.immediateStalemate(c))continue;ante++;if(!T.winMask[c])bad++;}cout<<nm<<"-file"<<ff<<" farSafeAnte="<<ante<<" violations="<<bad<<"\n";} } return 0;}
 if(argc>1&&string(argv[1])=="restoreDistanceSweep"){ for(auto [nm,typ]:vector<pair<string,PType>>{{"N",KNIGHT},{"B",BISHOP}}){G5Arena A(typ,{2,3,4,5,6,7},&K,3);auto T=A.solveGame(true);cout<<nm<<" d2_7 BK-distance guard\n";for(int th=1;th<=7;th++){long long ante=0,fail=0,stale=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.projectedKpkWin(c)){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);int p=(A.ranks[pri]-1)*8+3;if(cheb(bk,p)<th)continue;ante++;if(!T.winMask[c]){fail++;if(A.immediateStalemate(c))stale++;}}cout<<" BKdist>="<<th<<" ante="<<ante<<" fail="<<fail<<" nonstale="<<(fail-stale)<<" stale="<<stale<<"\n";} } return 0;}
 if(argc>1&&string(argv[1])=="rank2Profile"){ for(auto [nm,typ]:vector<pair<string,PType>>{{"N",KNIGHT},{"B",BISHOP},{"R",ROOK}}){G5Arena A(typ,{2,3,4,5,6,7},&K,3);auto T=A.solveGame(true);long long fail=0,stale=0,mD3=0,mD4=0,mFile=0,mAdjP=0,mAdjWK=0,wkFront=0,bkNearP=0,checking=0,btm=0;map<int,long long> mdistP,mdistPromo;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.projectedKpkWin(c)&&!T.winMask[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(A.ranks[pri]!=2)continue;fail++;int p=11; if(A.immediateStalemate(c))stale++;if(m==19)mD3++;if(m==27)mD4++;if(F(m)==3)mFile++;if(cheb(m,p)<=1)mAdjP++;if(cheb(m,wk)<=1)mAdjWK++;if(wk==19||wk==27)wkFront++;if(cheb(bk,p)<=2)bkNearP++;if(A.minorAttacksBK(m,bk,wk,p))checking++;if(t)btm++;mdistP[cheb(m,p)]++;mdistPromo[cheb(m,59)]++;}cout<<nm<<" rank2 fail="<<fail<<" stale="<<stale<<" Btm="<<btm<<" mD3="<<mD3<<" mD4="<<mD4<<" mOnPawnFile="<<mFile<<" mAdjPawn="<<mAdjP<<" mAdjWK="<<mAdjWK<<" wkOnD3orD4="<<wkFront<<" bkDistPawn<=2="<<bkNearP<<" minorCheckingBK="<<checking<<"\n";cout<<"  minorDistPawn:";for(auto &x:mdistP)cout<<x.first<<":"<<x.second<<",";cout<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="restByRank"){ vector<pair<string,PType>> cfg={{"N",KNIGHT},{"B",BISHOP},{"R",ROOK}}; for(auto [nm,typ]:cfg){G5Arena A(typ,{2,3,4,5,6,7},&K,3);auto T=A.solveGame(true);cout<<nm<<"-d2_7 restoration-by-rank\n";for(int rr=2;rr<=7;rr++){long long ante=0,fail=0,stale=0,fw=0,fb=0;vector<int> ss;int ew,ewm,ed;for(int c=0;c<A.SZ;c++)if(A.valid[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(A.ranks[pri]!=rr||!A.projectedKpkWin(c))continue;ante++;if(!T.winMask[c]){fail++;if(t)fb++;else fw++;if(A.immediateStalemate(c))stale++;}}cout<<" rank="<<rr<<" ante="<<ante<<" fail="<<fail<<" stale="<<stale<<" nonstale="<<(fail-stale)<<" WtmFail="<<fw<<" BtmFail="<<fb<<"\n";} } return 0;}
 if(argc>1&&string(argv[1])=="scaleD"){ vector<tuple<string,PType,vector<int>>> cfg={ {"N-d5_7",KNIGHT,{5,6,7}}, {"N-d4_7",KNIGHT,{4,5,6,7}}, {"N-d2_7",KNIGHT,{2,3,4,5,6,7}}, {"B-d5_7",BISHOP,{5,6,7}}, {"B-d4_7",BISHOP,{4,5,6,7}}, {"B-d2_7",BISHOP,{2,3,4,5,6,7}} }; for(auto &z:cfg){string nm;PType typ;vector<int> rr;tie(nm,typ,rr)=z;G5Arena A(typ,rr,&K,3);auto Rr=A.solveGame(true);long long safeN=0,safeBad=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.safeTarget(c)){safeN++;if(!Rr.winMask[c])safeBad++;}auto att=A.strictAttractor([&](int c){return A.safeTarget(c);});long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);cout<<nm<<" static="<<Rr.valid<<" W="<<Rr.W<<" D="<<Rr.D<<" safeTarget="<<safeN<<" safeBad="<<safeBad<<" safeAttr="<<count(att.begin(),att.end(),1)<<" restAnte="<<ante<<" restFail="<<fail<<" restStale="<<stale<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="bridgeSplitWK"){ vector<tuple<string,PType,int,vector<int>>> cfg={ {"N-d",KNIGHT,3,{5,6,7}}, {"B-d",BISHOP,3,{5,6,7}}, {"R-d",ROOK,3,{5,6,7}}, {"N-b",KNIGHT,1,{5,6,7}}, {"B-b",BISHOP,1,{5,6,7}}, {"R-b",ROOK,1,{5,6,7}} }; for(auto &z:cfg){string nm;PType typ;int ff;vector<int> rr;tie(nm,typ,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(typ,rr,&Kf,ff);auto L=[&](int c){if(!A.safeTarget(c))return false;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);return F(wk)<=ff;};auto U=[&](int c){if(!A.safeTarget(c))return false;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);return F(wk)>=ff;};auto AL=A.strictAttractor(L);auto AR=A.strictAttractor(U);auto AU=A.strictAttractor([&](int c){return A.safeTarget(c);});long long nl=0,nr=0,al=0,ar=0,au=0,pure=0,both=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]){nl+=L(c);nr+=U(c);al+=AL[c];ar+=AR[c];au+=AU[c];if(AU[c]&&!AL[c]&&!AR[c])pure++;if(AL[c]&&AR[c])both++;}cout<<nm<<" TL="<<nl<<" TR="<<nr<<" AL="<<al<<" AR="<<ar<<" AU="<<au<<" pureBridge="<<pure<<" basinOverlap="<<both<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="bridgeSplit"){ vector<tuple<string,PType,int,vector<int>>> cfg={ {"N-d",KNIGHT,3,{5,6,7}}, {"B-d",BISHOP,3,{5,6,7}}, {"R-d",ROOK,3,{5,6,7}}, {"N-b",KNIGHT,1,{5,6,7}}, {"B-b",BISHOP,1,{5,6,7}}, {"R-b",ROOK,1,{5,6,7}} }; for(auto &z:cfg){string nm;PType typ;int ff;vector<int> rr;tie(nm,typ,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(typ,rr,&Kf,ff);auto L=[&](int c){if(!A.safeTarget(c))return false;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);return F(bk)<=ff;};auto U=[&](int c){if(!A.safeTarget(c))return false;int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);return F(bk)>=ff;};auto AL=A.strictAttractor(L);auto AR=A.strictAttractor(U);auto AU=A.strictAttractor([&](int c){return A.safeTarget(c);});long long nl=0,nr=0,al=0,ar=0,au=0,pure=0,both=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]){nl+=L(c);nr+=U(c);al+=AL[c];ar+=AR[c];au+=AU[c];if(AU[c]&&!AL[c]&&!AR[c])pure++;if(AL[c]&&AR[c])both++;}cout<<nm<<" TL="<<nl<<" TR="<<nr<<" AL="<<al<<" AR="<<ar<<" AU="<<au<<" pureBridge="<<pure<<" basinOverlap="<<both<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="bridgeR"){ vector<tuple<string,int,vector<int>>> cfg={ {"R-a5_7",0,{5,6,7}}, {"R-b5_7",1,{5,6,7}}, {"R-c5_7",2,{5,6,7}}, {"R-d5_7",3,{5,6,7}}, {"R-d2_7",3,{2,3,4,5,6,7}} }; for(auto &z:cfg){string nm;int ff;vector<int> rr;tie(nm,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(ROOK,rr,&Kf,ff);auto truth=A.solveGame(true);auto AP=A.strictAttractor([&](int c){return A.safeInheritRook(c);});auto AT=A.strictAttractor([&](int c){return A.safeTarget(c);});auto AU=A.strictAttractor([&](int c){return A.safeInheritRook(c)||A.safeTarget(c);});long long p=0,t=0,ap=0,at=0,au=0,pureSep=0,pureG4=0,nonwin=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]){bool pp=A.safeInheritRook(c),tt=A.safeTarget(c);p+=pp;t+=tt;ap+=AP[c];at+=AT[c];au+=AU[c];if(AU[c]&&!AP[c]&&!AT[c])pureSep++;if(AU[c]&&!pp&&!AT[c])pureG4++;if(AU[c]&&!truth.winMask[c])nonwin++;}cout<<nm<<" P="<<p<<" T="<<t<<" AP="<<ap<<" AT="<<at<<" AU="<<au<<" pureSeparate="<<pureSep<<" pureG4style="<<pureG4<<" nonwin="<<nonwin<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="waveR2"){ vector<tuple<string,int,vector<int>>> cfg={ {"R-a4_7",0,{4,5,6,7}}, {"R-c4_7",2,{4,5,6,7}}, {"R-d4_7",3,{4,5,6,7}}, {"R-d2_7",3,{2,3,4,5,6,7}} }; for(auto &z:cfg){string nm;int ff;vector<int> rr;tie(nm,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(ROOK,rr,&Kf,ff);auto Rr=A.solveGame(true);long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);long long safeViol=fail-stale;long long safeN=0,safeBad=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.safeTarget(c)){safeN++;if(!Rr.winMask[c])safeBad++;}auto att=A.strictAttractor([&](int c){return A.safeTarget(c);});cout<<nm<<" static="<<Rr.valid<<" W="<<Rr.W<<" D="<<Rr.D<<" restAnte="<<ante<<" restFail="<<fail<<" stale="<<stale<<" safeInheritViol="<<safeViol<<" safeTarget="<<safeN<<" safeTargetBad="<<safeBad<<" safeAttr="<<count(att.begin(),att.end(),1)<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="waveR"){ vector<tuple<string,int,vector<int>>> cfg={ {"R-a5_7",0,{5,6,7}}, {"R-b5_7",1,{5,6,7}}, {"R-c5_7",2,{5,6,7}}, {"R-d5_7",3,{5,6,7}} }; for(auto &z:cfg){string nm;int ff;vector<int> rr;tie(nm,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(ROOK,rr,&Kf,ff);auto Rr=A.solveGame(true);long long bad=0,targ=A.countTarget(Rr.winMask,bad);long long safeN=0,safeBad=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.safeTarget(c)){safeN++;if(!Rr.winMask[c])safeBad++;}auto att=A.strictAttractor([&](int c){return A.safeTarget(c);});long long ac=count(att.begin(),att.end(),1);long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);cout<<nm<<" static="<<Rr.valid<<" W="<<Rr.W<<" D="<<Rr.D<<" geomTarget="<<targ<<" geomBad="<<bad<<" safeTarget="<<safeN<<" safeBad="<<safeBad<<" safeAttr="<<ac<<" restAnte="<<ante<<" restFail="<<fail<<" restStale="<<stale<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="wave2"){ vector<tuple<string,PType,int,vector<int>>> cfg={ {"N-b5_7",KNIGHT,1,{5,6,7}}, {"B-b5_7",BISHOP,1,{5,6,7}}, {"N-e5_7",KNIGHT,4,{5,6,7}}, {"B-e5_7",BISHOP,4,{5,6,7}} }; for(auto &z:cfg){string nm;PType typ;int ff;vector<int> rr;tie(nm,typ,ff,rr)=z;auto Kf=solveKPK(ff);G5Arena A(typ,rr,&Kf,ff);auto Rr=A.solveGame(true);long long bad=0,targ=A.countTarget(Rr.winMask,bad);long long safeN=0,safeBad=0;for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.safeTarget(c)){safeN++;if(!Rr.winMask[c])safeBad++;}auto att=A.strictAttractor([&](int c){return A.safeTarget(c);});long long ac=count(att.begin(),att.end(),1);long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);cout<<nm<<" static="<<Rr.valid<<" W="<<Rr.W<<" D="<<Rr.D<<" geomTarget="<<targ<<" geomBad="<<bad<<" safeTarget="<<safeN<<" safeBad="<<safeBad<<" safeAttr="<<ac<<" restFail="<<fail<<" restStale="<<stale<<"\n";} return 0;}
 if(argc>1&&string(argv[1])=="wave1"){ vector<tuple<string,PType,int,vector<int>>> cfg={ {"N-a5_7",KNIGHT,0,{5,6,7}}, {"B-a5_7",BISHOP,0,{5,6,7}}, {"N-c5_7",KNIGHT,2,{5,6,7}}, {"B-c5_7",BISHOP,2,{5,6,7}}, {"N-d4_7",KNIGHT,3,{4,5,6,7}}, {"B-d4_7",BISHOP,3,{4,5,6,7}} }; for(auto &z:cfg){string nm;PType typ;int ff;vector<int> rr;tie(nm,typ,ff,rr)=z;auto Kf=solveKPK(ff);auto t0=chrono::steady_clock::now();G5Arena A(typ,rr,&Kf,ff);auto Rr=A.solveGame(true);long long bad=0,targ=A.countTarget(Rr.winMask,bad);auto att=A.strictAttractor([&](int c){return A.commonTarget(c);});long long ac=count(att.begin(),att.end(),1);long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);cout<<nm<<" static="<<Rr.valid<<" W="<<Rr.W<<" D="<<Rr.D<<" maxr="<<Rr.maxr<<" target="<<targ<<" bad="<<bad<<" attr="<<ac<<" restAnte="<<ante<<" restFail="<<fail<<" restStale="<<stale<<" sec="<<chrono::duration<double>(chrono::steady_clock::now()-t0).count()<<"\n"; if(bad){ long long bt=0,wt=0,st=0,pr6=0,pr7=0,mPromo=0,mAdjWK=0; map<int,int> bkHist,mHist; vector<int> ss;int tw,ew,ewm,ed; for(int c=0;c<A.SZ;c++)if(A.valid[c]&&A.commonTarget(c)&&!Rr.winMask[c]){int pri,wk,m,bk,t;gdecode(c,pri,wk,m,bk,t);if(t)bt++;else wt++;if(rr[pri]==6)pr6++;else if(rr[pri]==7)pr7++;if(m==7*8+ff)mPromo++;if(cheb(m,wk)<=1)mAdjWK++;bkHist[bk]++;mHist[m]++;if(t){A.blackSucc(c,ss,ew,ewm,ed);if(ss.empty()&&ew==0&&ed==0&&!A.blackInCheck(pri,wk,m,bk))st++;}} cout<<"  badstats Btm="<<bt<<" Wtm="<<wt<<" stalemate="<<st<<" p6="<<pr6<<" p7="<<pr7<<" minorPromo="<<mPromo<<" minorAdjWK="<<mAdjWK<<" BKs=";for(auto &x:bkHist)cout<<x.first<<":"<<x.second<<",";cout<<"\n"; } } return 0;}
 for(auto [name,pt]:tests){auto t0=chrono::steady_clock::now();G5Arena A(pt,{5,6,7},&K,3);cout<<name<<" static="<<count(A.valid.begin(),A.valid.end(),1)<<"\n";auto Rr=A.solveGame(true);auto t1=chrono::steady_clock::now();long long bad=0;long long targ=A.countTarget(Rr.winMask,bad);auto att=A.strictAttractor([&](int c){return A.commonTarget(c);});long long ac=count(att.begin(),att.end(),1);long long ante,fail,stale;A.restorationStats(Rr.winMask,ante,fail,stale);cout<<name<<" W="<<Rr.W<<" D="<<Rr.D<<" maxr="<<Rr.maxr<<" target="<<targ<<" bad="<<bad<<" attr="<<ac<<" restAnte="<<ante<<" restFail="<<fail<<" restStale="<<stale<<" sec="<<chrono::duration<double>(chrono::steady_clock::now()-t0).count()<<"\n";
 }
}
