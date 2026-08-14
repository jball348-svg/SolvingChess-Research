#include <bits/stdc++.h>
using namespace std;
static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;} static inline int C(int s){return (F(s)+R(s))&1;}
static inline int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
vector<int> kingMv[64], knightMv[64];
void initMoves(){for(int s=0;s<64;s++){for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int f=F(s)+df,r=R(s)+dr;if(f>=0&&f<8&&r>=0&&r<8)kingMv[s].push_back(r*8+f);}int D[8][2]={{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};for(auto &d:D){int f=F(s)+d[0],r=R(s)+d[1];if(f>=0&&f<8&&r>=0&&r<8)knightMv[s].push_back(r*8+f);}}}
enum PT{BISHOP,KNIGHT,ROOK,QUEEN};
string ptn(PT p){return p==BISHOP?"B":p==KNIGHT?"N":p==ROOK?"R":"Q";} string sqn(int s){if(s<0)return "-";string z;z+=char('a'+F(s));z+=char('1'+R(s));return z;}
struct Fam{string name;PT wp,bp;int wcolor,bcolor;int wpsq,bpsq;};
struct S{int wk,bk,wpiece,bpiece;bool wpawn,bpawn;int turn;}; // turn 0 W, 1 B; piece square -1 absent
struct Arena{
 Fam f; vector<int> wSquares,bSquares; vector<int> wIndex,bIndex; int nw,nb; uint64_t RAW;
 vector<uint8_t> valid,out,rem; // out:0 unknown/draw,1 side-to-move win,2 side-to-move loss,3 explicit draw/stalemate
 Arena(Fam ff):f(ff){wIndex.assign(64,-1);bIndex.assign(64,-1);buildSquares(f.wp,f.wcolor,wSquares,wIndex);buildSquares(f.bp,f.bcolor,bSquares,bIndex);nw=wSquares.size()+1;nb=bSquares.size()+1;RAW=uint64_t(64)*64*nw*nb*2*2*2;}
 void buildSquares(PT p,int col,vector<int>&v,vector<int>&idx){for(int s=0;s<64;s++){if(p==BISHOP && C(s)!=col)continue;idx[s]=v.size();v.push_back(s);}}
 inline uint64_t code(const S&s)const{int wi=s.wpiece<0?nw-1:wIndex[s.wpiece], bi=s.bpiece<0?nb-1:bIndex[s.bpiece];uint64_t x=s.wk;x=x*64+s.bk;x=x*nw+wi;x=x*nb+bi;x=x*2+s.wpawn;x=x*2+s.bpawn;x=x*2+s.turn;return x;}
 inline S dec(uint64_t x)const{S s; s.turn=x%2;x/=2;s.bpawn=x%2;x/=2;s.wpawn=x%2;x/=2;int bi=x%nb;x/=nb;int wi=x%nw;x/=nw;s.bk=x%64;x/=64;s.wk=x%64;s.wpiece=(wi==nw-1?-1:wSquares[wi]);s.bpiece=(bi==nb-1?-1:bSquares[bi]);return s;}
 bool occ(const S&s,int sq)const{return s.wk==sq||s.bk==sq||s.wpiece==sq||s.bpiece==sq||(s.wpawn&&f.wpsq==sq)||(s.bpawn&&f.bpsq==sq);}
 bool pieceAtt(PT p,int from,int to,const S&s,int ignore=-2,int extraBlock=-1)const{
   if(from<0)return false;if(p==KNIGHT){for(int q:knightMv[from])if(q==to)return true;return false;}
   int df=F(to)-F(from),dr=R(to)-R(from),sf=0,sr=0;
   if(p==BISHOP){if(df==0||abs(df)!=abs(dr))return false;sf=df>0?1:-1;sr=dr>0?1:-1;}
   else if(p==ROOK){if(df!=0&&dr!=0)return false;sf=(df>0)-(df<0);sr=(dr>0)-(dr<0);}
   else {if(df==0||dr==0){sf=(df>0)-(df<0);sr=(dr>0)-(dr<0);}else if(abs(df)==abs(dr)){sf=df>0?1:-1;sr=dr>0?1:-1;}else return false;}
   int ff=F(from)+sf,rr=R(from)+sr;while(ff!=F(to)||rr!=R(to)){int q=rr*8+ff;if(q!=ignore && (q==extraBlock||occ(s,q)))return false;ff+=sf;rr+=sr;}return true;
 }
 bool pawnAtt(bool white,int from,int to)const{int dr=R(to)-R(from),df=abs(F(to)-F(from));return df==1&&dr==(white?1:-1);}
 bool attackedByWhite(const S&s,int sq,int ignore=-2,int extraBlock=-1)const{
   if(cheb(s.wk,sq)<=1)return true;
   if(s.wpawn&&f.wpsq!=ignore&&pawnAtt(true,f.wpsq,sq))return true;
   if(s.wpiece>=0&&s.wpiece!=ignore&&pieceAtt(f.wp,s.wpiece,sq,s,ignore,extraBlock))return true;return false;
 }
 bool attackedByBlack(const S&s,int sq,int ignore=-2,int extraBlock=-1)const{
   if(cheb(s.bk,sq)<=1)return true;
   if(s.bpawn&&f.bpsq!=ignore&&pawnAtt(false,f.bpsq,sq))return true;
   if(s.bpiece>=0&&s.bpiece!=ignore&&pieceAtt(f.bp,s.bpiece,sq,s,ignore,extraBlock))return true;return false;
 }
 bool staticValid(const S&s)const{
   if(s.wk==s.bk||cheb(s.wk,s.bk)<=1)return false;
   vector<int> q={s.wk,s.bk};if(s.wpiece>=0)q.push_back(s.wpiece);if(s.bpiece>=0)q.push_back(s.bpiece);if(s.wpawn)q.push_back(f.wpsq);if(s.bpawn)q.push_back(f.bpsq);
   sort(q.begin(),q.end());for(int i=1;i<(int)q.size();i++)if(q[i]==q[i-1])return false;
   if(s.wpiece>=0&&wIndex[s.wpiece]<0)return false;if(s.bpiece>=0&&bIndex[s.bpiece]<0)return false;
   // Side not to move cannot already be in check under the frozen static-valid convention.
   if(s.turn==0 && attackedByWhite(s,s.bk))return false; // Black just moved.
   if(s.turn==1 && attackedByBlack(s,s.wk))return false; // White just moved.
   return true;
 }
 bool inCheck(const S&s)const{return s.turn==0?attackedByBlack(s,s.wk):attackedByWhite(s,s.bk);}
 void pieceDests(PT p,int from,const S&s,vector<int>&d)const{d.clear();if(from<0)return;if(p==KNIGHT){for(int q:knightMv[from])d.push_back(q);return;}int dirs[8][2]={{1,1},{1,-1},{-1,1},{-1,-1},{1,0},{-1,0},{0,1},{0,-1}};int a=0,b=8;if(p==BISHOP){a=0;b=4;}else if(p==ROOK){a=4;b=8;}for(int k=a;k<b;k++){int ff=F(from)+dirs[k][0],rr=R(from)+dirs[k][1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int q=rr*8+ff;d.push_back(q);if(occ(s,q))break;ff+=dirs[k][0];rr+=dirs[k][1];}}}
 struct MoveStats{int legal=0,captures=0,checks=0;bool promo=false;};
 bool promoLegal(const S&s,bool white)const{
   int p=white?f.wpsq:f.bpsq;if(white?!s.wpawn:!s.bpawn)return false;int dir=white?8:-8;int forward=p+dir;
   auto test=[&](int dest,int captured)->bool{S z=s;if(white)z.wpawn=false;else z.bpawn=false;if(captured==1){if(white)z.bpiece=-1;else z.wpiece=-1;} // only opposing piece can be on capture promotion square here
     // promoted piece occupies dest as a neutral blocker for king-safety ray tests.
     int king=white?z.wk:z.bk; bool atk=white?attackedByBlack(z,king,-2,dest):attackedByWhite(z,king,-2,dest);return !atk;};
   if(forward>=0&&forward<64&&!occ(s,forward)&&test(forward,0))return true;
   for(int df:{-1,1}){int ff=F(p)+df,rr=R(p)+(white?1:-1);if(ff<0||ff>=8||rr<0||rr>=8)continue;int d=rr*8+ff; if(white){if(d==s.bpiece&&test(d,1))return true;}else{if(d==s.wpiece&&test(d,1))return true;}}
   return false;
 }
 void successors(const S&s,vector<uint64_t>&ss,MoveStats*ms=nullptr)const{
   ss.clear();MoveStats loc;bool white=s.turn==0;int k=white?s.wk:s.bk;for(int nk:kingMv[k]){
     // own occupancy
     if(white){if(nk==s.wpiece||(s.wpawn&&nk==f.wpsq))continue;if(nk==s.bk)continue;}else{if(nk==s.bpiece||(s.bpawn&&nk==f.bpsq))continue;if(nk==s.wk)continue;}
     S z=s;if(white)z.wk=nk;else z.bk=nk;
     bool cap=false;if(white){if(nk==z.bpiece){z.bpiece=-1;cap=true;}if(z.bpawn&&nk==f.bpsq){z.bpawn=false;cap=true;}}else{if(nk==z.wpiece){z.wpiece=-1;cap=true;}if(z.wpawn&&nk==f.wpsq){z.wpawn=false;cap=true;}}
     z.turn^=1;if(!staticValid(z))continue;ss.push_back(code(z));loc.legal++;loc.captures+=cap;loc.checks+=inCheck(z);
   }
   int pc=white?s.wpiece:s.bpiece;PT pt=white?f.wp:f.bp;if(pc>=0){vector<int>d;pieceDests(pt,pc,s,d);for(int np:d){
     if(white){if(np==s.wk||(s.wpawn&&np==f.wpsq)||np==s.bk)continue;}else{if(np==s.bk||(s.bpawn&&np==f.bpsq)||np==s.wk)continue;}
     S z=s;bool cap=false;if(white){z.wpiece=np;if(np==z.bpiece){z.bpiece=-1;cap=true;}if(z.bpawn&&np==f.bpsq){z.bpawn=false;cap=true;}}else{z.bpiece=np;if(np==z.wpiece){z.wpiece=-1;cap=true;}if(z.wpawn&&np==f.wpsq){z.wpawn=false;cap=true;}}
     z.turn^=1;if(!staticValid(z))continue;ss.push_back(code(z));loc.legal++;loc.captures+=cap;loc.checks+=inCheck(z);
   }}
   if(promoLegal(s,white)){loc.promo=true;loc.legal++;}
   if(ms)*ms=loc;
 }
 void buildValid(){valid.assign(RAW,0);uint64_t n=0;for(uint64_t c=0;c<RAW;c++){S s=dec(c);if(staticValid(s)){valid[c]=1;n++;}}cerr<<f.name<<" raw="<<RAW<<" static="<<n<<"\\n";}
 int sigOf(const S&s)const{return (s.wpiece>=0?8:0)|(s.bpiece>=0?4:0)|(s.wpawn?2:0)|(s.bpawn?1:0);}
 int whiteTruth(uint64_t c)const{S s=dec(c);uint8_t o=out[c];if(o==0||o==3)return 0;return ((s.turn==0&&o==1)||(s.turn==1&&o==2))?1:-1;}
 vector<uint8_t> strictWhiteAttr(const vector<uint8_t>&target)const{
   vector<uint8_t> att(RAW,0), rr(RAW,0);deque<uint64_t>q;vector<uint64_t>ss;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]&&target[c]){att[c]=1;q.push_back(c);}
   for(uint64_t c=0;c<RAW;c++)if(valid[c]&&!att[c]){S s=dec(c);if(s.turn!=1)continue;MoveStats ms;successors(s,ss,&ms);int ext=ms.promo?1:0;if(ss.empty()&&!ms.promo)ext=1;int n=int(ss.size())+ext;rr[c]=uint8_t(min(255,n));}
   while(!q.empty()){uint64_t z=q.front();q.pop_front();predecessors(z,[&](uint64_t p){if(att[p])return;S ps=dec(p);if(ps.turn==0){att[p]=1;q.push_back(p);}else if(rr[p]>0){--rr[p];if(rr[p]==0){att[p]=1;q.push_back(p);}}});}
   return att;
 }
 void analyzeG7(bool doAttrs=true){
   if(out.empty())return;cout<<"ANALYSIS_BEGIN "<<f.name<<"\\n";
   // exact direct full-material transition edges and destination signatures
   array<uint64_t,16> red{};uint64_t promoW=0,promoB=0,full=0,fullMoves=0,fullCaps=0;vector<uint64_t>ss;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);if(sigOf(s)!=15)continue;full++;MoveStats ms;successors(s,ss,&ms);fullMoves+=ms.legal;fullCaps+=ms.captures;if(ms.promo){if(s.turn==0)promoW++;else promoB++;}for(auto x:ss){S z=dec(x);int sg=sigOf(z);if(sg!=15)red[sg]++;}}
   cout<<"FULL_TRANSITIONS states="<<full<<" legal_moves="<<fullMoves<<" captures="<<fullCaps<<" Wpromo_states="<<promoW<<" Bpromo_states="<<promoB<<"\\n";
   for(int sg=0;sg<16;sg++)if(red[sg])cout<<"CAPTURE_EDGE to_SIG="<<sg<<" edges="<<red[sg]<<"\\n";
   // raw projection/restoration information from exact lower signatures
   struct PStat{uint64_t pvalid=0,anteW=0,stayW=0,toD=0,toB=0;};array<PStat,4> ps{};const char* nm[4]={"del_Wpiece","del_Bpiece","del_Wpawn","del_Bpawn"};
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);if(sigOf(s)!=15)continue;int fw=whiteTruth(c);for(int k=0;k<4;k++){S z=s;if(k==0)z.wpiece=-1;if(k==1)z.bpiece=-1;if(k==2)z.wpawn=false;if(k==3)z.bpawn=false;uint64_t d=code(z);if(!valid[d])continue;ps[k].pvalid++;if(whiteTruth(d)==1){ps[k].anteW++;if(fw==1)ps[k].stayW++;else if(fw==0)ps[k].toD++;else ps[k].toB++;}}}
   for(int k=0;k<4;k++)cout<<"PROJECT "<<nm[k]<<" valid="<<ps[k].pvalid<<" lowerW_ante="<<ps[k].anteW<<" restoreW="<<ps[k].stayW<<" restoreD="<<ps[k].toD<<" restoreB="<<ps[k].toB<<"\\n";
   // Fire frozen G6 double-brink race-path target unchanged as far as its published atoms determine.
   int wpPromo=f.wpsq+8,bpPromo=f.bpsq-8;uint64_t targ=0,targW=0,targD=0,targB=0;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);if(sigOf(s)!=15)continue;bool core=cheb(s.wk,wpPromo)<=4&&cheb(s.bk,wpPromo)>=5;int TW=2-(s.turn==0), TB=2-(s.turn==1);bool race=TB>TW;bool path=s.wk!=wpPromo&&s.wpiece!=wpPromo;bool t=core&&race&&path;if(!t)continue;targ++;int w=whiteTruth(c);if(w==1)targW++;else if(w==0)targD++;else targB++;}
   cout<<"G6_TARGET_RACE_PATH_FIRE direct="<<targ<<" W="<<targW<<" D="<<targD<<" B="<<targB<<" false_nonW="<<(targD+targB)<<"\\n";
   // Exact lower-material endpoints as trusted transition targets: black-piece-absent SIG11 and black-pawn-absent SIG14.
   vector<uint8_t>T11(RAW,0),T14(RAW,0),TU(RAW,0);uint64_t n11=0,n14=0;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]&&whiteTruth(c)==1){int sg=sigOf(dec(c));if(sg==11){T11[c]=TU[c]=1;n11++;}if(sg==14){T14[c]=TU[c]=1;n14++;}}
   cout<<"TRANSITION_TARGETS SIG11_W="<<n11<<" SIG14_W="<<n14<<"\\n";
   if(!doAttrs){cout<<"ANALYSIS_END "<<f.name<<"\\n";return;}
   auto A11=strictWhiteAttr(T11);cerr<<f.name<<" attr11 done\\n";auto A14=strictWhiteAttr(T14);cerr<<f.name<<" attr14 done\\n";auto AU=strictWhiteAttr(TU);cerr<<f.name<<" attrUnion done\\n";
   uint64_t a11f=0,a14f=0,auf=0,puref=0,kernf=0,pureAll=0,kernAll=0;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);bool fulls=sigOf(s)==15;if(fulls){a11f+=A11[c];a14f+=A14[c];auf+=AU[c];if(AU[c]&&!A11[c]&&!A14[c])puref++;}if(AU[c]&&!A11[c]&&!A14[c])pureAll++;if(s.turn!=1||A11[c]||A14[c])continue;MoveStats ms;successors(s,ss,&ms);if(ms.promo||ss.empty())continue;bool allB=true,all1=true,all2=true;for(auto x:ss){if(!(A11[x]||A14[x])){allB=false;break;}if(!A11[x])all1=false;if(!A14[x])all2=false;}if(allB&&!all1&&!all2){kernAll++;if(fulls)kernf++;}}
   cout<<"STRICT_ATTR SIG11 full="<<a11f<<" SIG14 full="<<a14f<<" UNION full="<<auf<<" PURE_BRIDGE full="<<puref<<" KERNEL full="<<kernf<<" amplification="<<(kernf?double(puref)/kernf:0.0)<<"\\n";
   cout<<"STRICT_ATTR_ALL pure="<<pureAll<<" kernel="<<kernAll<<" amplification="<<(kernAll?double(pureAll)/kernAll:0.0)<<"\\n";
   cout<<"ANALYSIS_END "<<f.name<<"\\n";
 }
 template<class Fn> void originsForPiece(PT p,int dest,const S&cur,bool white,Fn fn)const{
   if(p==KNIGHT){for(int o:knightMv[dest])fn(o);return;}int dirs[8][2]={{1,1},{1,-1},{-1,1},{-1,-1},{1,0},{-1,0},{0,1},{0,-1}};int a=0,b=8;if(p==BISHOP){a=0;b=4;}else if(p==ROOK){a=4;b=8;}for(int k=a;k<b;k++){int ff=F(dest)+dirs[k][0],rr=R(dest)+dirs[k][1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int o=rr*8+ff;fn(o); // blockers are checked by predecessor validity + forward path logic below via pieceAtt
     // Current occupancy between origin and dest can block further origins. The mover currently sits at dest, so ignore dest.
     if(o==cur.wk||o==cur.bk||o==cur.wpiece||o==cur.bpiece||(cur.wpawn&&o==f.wpsq)||(cur.bpawn&&o==f.bpsq))break;ff+=dirs[k][0];rr+=dirs[k][1];}}
 }
 template<class Fn> void predecessors(uint64_t cc,Fn emit)const{
   S s=dec(cc);bool prevWhite=s.turn==1; // current Black => White moved
   auto tryP=[&](S p){p.turn=prevWhite?0:1;uint64_t pc=code(p);if(valid[pc])emit(pc);};
   // reverse king move, with no capture or restoring exactly one captured enemy unit at destination
   int dest=prevWhite?s.wk:s.bk;for(int o:kingMv[dest]){S p=s;if(prevWhite)p.wk=o;else p.bk=o;tryP(p);
     if(prevWhite){if(s.bpiece<0 && bIndex[dest]>=0){p=s;p.wk=o;p.bpiece=dest;tryP(p);}if(!s.bpawn&&dest==f.bpsq){p=s;p.wk=o;p.bpawn=true;tryP(p);}}
     else {if(s.wpiece<0 && wIndex[dest]>=0){p=s;p.bk=o;p.wpiece=dest;tryP(p);}if(!s.wpawn&&dest==f.wpsq){p=s;p.bk=o;p.wpawn=true;tryP(p);}}
   }
   // reverse piece move
   int pdest=prevWhite?s.wpiece:s.bpiece;PT pt=prevWhite?f.wp:f.bp;if(pdest>=0){originsForPiece(pt,pdest,s,prevWhite,[&](int o){S p=s;if(prevWhite)p.wpiece=o;else p.bpiece=o;tryP(p);
       if(prevWhite){if(s.bpiece<0&&bIndex[pdest]>=0){p=s;p.wpiece=o;p.bpiece=pdest;tryP(p);}if(!s.bpawn&&pdest==f.bpsq){p=s;p.wpiece=o;p.bpawn=true;tryP(p);}}
       else {if(s.wpiece<0&&wIndex[pdest]>=0){p=s;p.bpiece=o;p.wpiece=pdest;tryP(p);}if(!s.wpawn&&pdest==f.wpsq){p=s;p.bpiece=o;p.wpawn=true;tryP(p);}}
   });}
 }
 struct Res{uint64_t st=0,W=0,B=0,D=0;int maxq=0;double sec=0;};
 Res solve(){auto t0=chrono::steady_clock::now();buildValid();out.assign(RAW,0);rem.assign(RAW,0);deque<uint64_t>q;vector<uint64_t>ss;uint64_t seedsW=0,seedsL=0,stal=0;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);MoveStats ms;successors(s,ss,&ms);if(ms.promo){out[c]=1;q.push_back(c);seedsW++;continue;}rem[c]=min<int>(255,ss.size());if(ss.empty()){if(inCheck(s)){out[c]=2;q.push_back(c);seedsL++;}else{out[c]=3;stal++;}}}
   cerr<<"seeds win="<<seedsW<<" loss="<<seedsL<<" stal="<<stal<<" queue="<<q.size()<<"\n";
   uint64_t pops=0;while(!q.empty()){uint64_t s=q.front();q.pop_front();uint8_t os=out[s];predecessors(s,[&](uint64_t p){if(out[p])return;if(os==2){out[p]=1;q.push_back(p);}else if(os==1){if(rem[p]>0)--rem[p];if(rem[p]==0){out[p]=2;q.push_back(p);}}});if((++pops%1000000)==0)cerr<<"pops="<<pops<<" q="<<q.size()<<"\n";}
   // Deterministic cross-signature Bellman audit sample (membership solver itself is exact retrograde).
   uint64_t bellBad=0,bellChecked=0;for(uint64_t c=0;c<RAW;c++)if(valid[c] && c%257==0){bellChecked++;S s=dec(c);vector<uint64_t> vv;MoveStats ms;successors(s,vv,&ms);uint8_t exp=0;if(ms.promo)exp=1;else if(vv.empty()){exp=inCheck(s)?2:3;}else{bool anyLoss=false,allWin=true;for(auto x:vv){uint8_t o=out[x];if(o==2)anyLoss=true;if(o!=1)allWin=false;}if(anyLoss)exp=1;else if(allWin)exp=2;else exp=3;}uint8_t got=(out[c]==0?3:out[c]);if(exp!=got)bellBad++;}
   cerr<<"bellman_sample_checked="<<bellChecked<<" mismatches="<<bellBad<<"\n";
   {ofstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);fv.write((char*)valid.data(),valid.size());ofstream fo("/mnt/data/"+f.name+"_out.bin",ios::binary);fo.write((char*)out.data(),out.size());cerr<<"saved masks "<<f.name<<"\n";}
   // Material-signature ledger: bit3 WPc, bit2 BPc, bit1 WPawn, bit0 BPawn.
   struct Cnt{uint64_t st=0,W=0,B=0,D=0;};array<Cnt,16> sg{};Res r;for(uint64_t c=0;c<RAW;c++)if(valid[c]){r.st++;S s=dec(c);int sig=(s.wpiece>=0?8:0)|(s.bpiece>=0?4:0)|(s.wpawn?2:0)|(s.bpawn?1:0);uint8_t o=out[c];auto add=[&](Cnt&z){z.st++;if(o==0||o==3)z.D++;else if((s.turn==0&&o==1)||(s.turn==1&&o==2))z.W++;else z.B++;};add(sg[sig]);if(o==0||o==3)r.D++;else if((s.turn==0&&o==1)||(s.turn==1&&o==2))r.W++;else r.B++;}
   for(int sig=0;sig<16;sig++)if(sg[sig].st)cout<<"SIG "<<sig<<" static="<<sg[sig].st<<" W="<<sg[sig].W<<" B="<<sg[sig].B<<" D="<<sg[sig].D<<"\n";
   cout<<"TRANSITION_MODEL direct_capture_endpoint_signatures=4 promotions=2 lower_material_closure=internal\n";
   cout<<"AUDIT bellman_sample_checked="<<bellChecked<<" mismatches="<<bellBad<<"\n";r.sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();return r;
 }
};

Fam mk(string n,string W,string B,int wc,int bc,string wp,string bp){auto pt=[](string x){return x=="B"?BISHOP:x=="N"?KNIGHT:x=="R"?ROOK:QUEEN;};auto sq=[](string x){return (x[1]-'1')*8+(x[0]-'a');};return {n,pt(W),pt(B),wc,bc,sq(wp),sq(bp)};}

int main(int argc,char**argv){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();
 vector<Fam> fams={
   mk("BB_opp_d7_e2","B","B",0,1,"d7","e2"),
   mk("BB_same_c7_f2","B","B",0,0,"c7","f2"),
   mk("BN_opp_d7_e2","B","N",0,0,"d7","e2"),
   mk("RB_c7_f2","R","B",0,1,"c7","f2"),
   mk("NB_b7_g2","N","B",0,0,"b7","g2"),
   mk("QB_d7_e2","Q","B",0,1,"d7","e2")};
 string mode=argc>1?argv[1]:"scan";
 if(mode.rfind("edge:",0)==0){auto f=fams[0];Arena a(f);uint64_t pc=stoull(mode.substr(5));S sp=a.dec(pc);cerr<<"p valid="<<a.staticValid(sp)<<"\n";vector<uint64_t>vv;Arena::MoveStats ms;a.successors(sp,vv,&ms);cout<<"succ_n="<<vv.size()<<" promo="<<ms.promo<<"\n";for(auto x:vv){S z=a.dec(x);cout<<x<<" wk="<<z.wk<<" bk="<<z.bk<<" wp="<<z.wpiece<<" bp="<<z.bpiece<<" Wp="<<z.wpawn<<" Bp="<<z.bpawn<<" t="<<z.turn<<"\n";}return 0;}
 if(mode=="scan"){
   mt19937_64 rng(0x677ULL);
   const int N=120000;
   for(auto f:fams){Arena a(f);uint64_t validn=0,totalMoves=0,caps=0,checks=0,promos=0;set<string>endcats;
     for(int i=0;i<N;i++){S st;st.wk=rng()%64;st.bk=rng()%64;int wi=rng()%a.nw,bi=rng()%a.nb;st.wpiece=wi==a.nw-1?-1:a.wSquares[wi];st.bpiece=bi==a.nb-1?-1:a.bSquares[bi];st.wpawn=rng()&1;st.bpawn=rng()&1;st.turn=rng()&1;if(!a.staticValid(st))continue;validn++;vector<uint64_t> ss;Arena::MoveStats ms;a.successors(st,ss,&ms);totalMoves+=ms.legal;caps+=ms.captures;checks+=ms.checks;promos+=ms.promo;
     }
     double vf=double(validn)/N;double est=vf*a.RAW;double br=validn?double(totalMoves)/validn:0;double capd=totalMoves?double(caps)/totalMoves:0;double chkd=totalMoves?double(checks)/totalMoves:0;double prod=validn?double(promos)/validn:0;
     cout<<f.name<<" raw="<<a.RAW<<" est_static="<<(uint64_t)llround(est)<<" valid_frac="<<fixed<<setprecision(4)<<vf<<" mean_branch="<<setprecision(3)<<br<<" capture_density="<<100*capd<<" check_density="<<100*chkd<<" promo_state_pct="<<100*prod<<"\n";
   }
 }
 if(mode.rfind("predcomplete:",0)==0){string nm=mode.substr(13);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());mt19937_64 rng(0xC0FFEEULL);uint64_t checked=0,edges=0,miss=0;while(checked<300000){uint64_t c=rng()%a.RAW;if(!a.valid[c])continue;checked++;S st=a.dec(c);vector<uint64_t>vv;a.successors(st,vv,nullptr);for(auto z:vv){edges++;bool ok=false;a.predecessors(z,[&](uint64_t p){if(p==c)ok=true;});if(!ok){miss++;if(miss<=10)cerr<<"MISSING p="<<c<<" z="<<z<<"\n";}}}cout<<"PREDCOMPLETE "<<f.name<<" checked="<<checked<<" edges="<<edges<<" missing="<<miss<<"\n";return 0;}return 2;}
 if(mode.rfind("predsound:",0)==0){string nm=mode.substr(10);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());mt19937_64 rng(0x50A0DULL);uint64_t checked=0,edges=0,bad=0;while(checked<500000){uint64_t c=rng()%a.RAW;if(!a.valid[c])continue;checked++;a.predecessors(c,[&](uint64_t p){edges++;S ps=a.dec(p);vector<uint64_t>vv;a.successors(ps,vv,nullptr);if(find(vv.begin(),vv.end(),c)==vv.end()){bad++;if(bad<=10)cerr<<"UNSOUND c="<<c<<" p="<<p<<"\n";}});}cout<<"PREDSOUND "<<f.name<<" checked="<<checked<<" edges="<<edges<<" bad="<<bad<<"\n";return 0;}return 2;}
 if(mode.rfind("predups:",0)==0){string nm=mode.substr(8);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());mt19937_64 rng(0xD00DULL);uint64_t checked=0,emitN=0,dupN=0,statesDup=0,maxmult=0;while(checked<250000){uint64_t c=rng()%a.RAW;if(!a.valid[c])continue;checked++;vector<uint64_t>ps;a.predecessors(c,[&](uint64_t p){ps.push_back(p);});emitN+=ps.size();sort(ps.begin(),ps.end());uint64_t d=0,mm=1,cur=1;for(size_t i=1;i<ps.size();i++){if(ps[i]==ps[i-1]){d++;cur++;mm=max(mm,cur);}else cur=1;}if(d){dupN+=d;statesDup++;maxmult=max(maxmult,mm);if(statesDup<=5)cerr<<"dup current="<<c<<" emissions="<<ps.size()<<" duplicate_extra="<<d<<"\n";}}cout<<"PREDUPS "<<f.name<<" checked="<<checked<<" emissions="<<emitN<<" duplicate_extra="<<dupN<<" states_with_dups="<<statesDup<<" max_mult="<<maxmult<<"\n";return 0;}return 2;}
 if(mode.rfind("predaudit:",0)==0){string nm=mode.substr(10);for(auto f:fams)if(f.name==nm){Arena a(f);a.buildValid();mt19937_64 rng(0x677123ULL);uint64_t sound=0,sbad=0,comp=0,cmiss=0;int got=0;while(got<12000){uint64_t c=rng()%a.RAW;if(!a.valid[c])continue;got++;vector<uint64_t> ps;a.predecessors(c,[&](uint64_t p){ps.push_back(p);});for(auto p:ps){sound++;S sp=a.dec(p);vector<uint64_t> vv;a.successors(sp,vv,nullptr);if(find(vv.begin(),vv.end(),c)==vv.end()){sbad++;if(sbad<6)cerr<<"BADP s="<<c<<" p="<<p<<"\n";}}S sp=a.dec(c);vector<uint64_t> vv;a.successors(sp,vv,nullptr);for(auto x:vv){comp++;bool ok=false;a.predecessors(x,[&](uint64_t p){if(p==c)ok=true;});if(!ok){cmiss++;if(cmiss<6)cerr<<"MISSP p="<<c<<" s="<<x<<"\n";}}}cout<<"PREDAUDIT "<<f.name<<" sound_edges="<<sound<<" bad="<<sbad<<" successor_edges="<<comp<<" missing="<<cmiss<<"\n";return 0;}return 2;}
 if(mode.rfind("attr:",0)==0){string z=mode.substr(5);auto k=z.rfind(':');if(k==string::npos)return 2;string nm=z.substr(0,k),which=z.substr(k+1);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary),fo("/mnt/data/"+f.name+"_out.bin",ios::binary);if(!fv||!fo)return 3;fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());set<int>want;{stringstream ss(which);string tok;while(getline(ss,tok,'_'))if(!tok.empty())want.insert(stoi(tok));}vector<uint8_t>T(a.RAW,0);uint64_t tn=0;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&a.whiteTruth(c)==1){int sg=a.sigOf(a.dec(c));if(want.count(sg)){T[c]=1;tn++;}}cerr<<"target "<<which<<" n="<<tn<<"\n";auto A=a.strictWhiteAttr(T);uint64_t all=0,full=0;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&A[c]){all++;if(a.sigOf(a.dec(c))==15)full++;}string path="/mnt/data/"+f.name+"_A"+which+".bin";ofstream ff(path,ios::binary);ff.write((char*)A.data(),A.size());cout<<"ATTR "<<f.name<<" which="<<which<<" target="<<tn<<" all="<<all<<" full="<<full<<"\n";return 0;}return 2;}
 if(mode.rfind("combine:",0)==0){string nm=mode.substr(8);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());vector<uint8_t>A1(a.RAW),A2(a.RAW),AU(a.RAW);ifstream f1("/mnt/data/"+f.name+"_A11.bin",ios::binary),f2("/mnt/data/"+f.name+"_A14.bin",ios::binary),fu("/mnt/data/"+f.name+"_AU.bin",ios::binary);if(!f1||!f2||!fu)return 4;f1.read((char*)A1.data(),A1.size());f2.read((char*)A2.data(),A2.size());fu.read((char*)AU.data(),AU.size());uint64_t pure=0,puref=0,kern=0,kernf=0;vector<uint64_t>ss;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&AU[c]&&!A1[c]&&!A2[c]){pure++;S s=a.dec(c);bool full=a.sigOf(s)==15;if(full)puref++;if(s.turn!=1)continue;Arena::MoveStats ms;a.successors(s,ss,&ms);if(ms.promo||ss.empty())continue;bool allB=true,all1=true,all2=true;for(auto x:ss){if(!(A1[x]||A2[x])){allB=false;break;}if(!A1[x])all1=false;if(!A2[x])all2=false;}if(allB&&!all1&&!all2){kern++;if(full)kernf++;}}cout<<"COMBINE "<<f.name<<" pure_all="<<pure<<" kernel_all="<<kern<<" amp_all="<<(kern?double(pure)/kern:0)<<" pure_full="<<puref<<" kernel_full="<<kernf<<" amp_full="<<(kernf?double(puref)/kernf:0)<<"\n";return 0;}return 2;}

 if(mode.rfind("rank3:",0)==0){string nm=mode.substr(6);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary),fo("/mnt/data/"+f.name+"_out.bin",ios::binary);if(!fv||!fo)return 3;fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());auto load=[&](string tag){vector<uint8_t>v(a.RAW);ifstream fi("/mnt/data/"+f.name+"_A"+tag+".bin",ios::binary);if(!fi)exit(4);fi.read((char*)v.data(),v.size());return v;};auto A71=load("7_11"),A74=load("7_14"),A114=load("11_14");vector<uint8_t>B(a.RAW),att(a.RAW),rr(a.RAW),mx(a.RAW);vector<uint16_t>rk(a.RAW,65535);deque<uint64_t>q;vector<uint64_t>ss;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]){B[c]=A71[c]||A74[c]||A114[c];if(a.whiteTruth(c)==1){int sg=a.sigOf(a.dec(c));if(sg==7||sg==11||sg==14){att[c]=1;rk[c]=0;q.push_back(c);}}}for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&!att[c]){S st=a.dec(c);if(st.turn!=1)continue;Arena::MoveStats ms;a.successors(st,ss,&ms);int ext=ms.promo?1:0;if(ss.empty()&&!ms.promo)ext=1;rr[c]=uint8_t(min(255,int(ss.size())+ext));}while(!q.empty()){uint64_t z=q.front();q.pop_front();a.predecessors(z,[&](uint64_t p){if(att[p])return;S ps=a.dec(p);if(ps.turn==0){att[p]=1;rk[p]=uint16_t(min<int>(65534,rk[z]+1));q.push_back(p);}else if(rr[p]>0){mx[p]=max<uint8_t>(mx[p],uint8_t(min<int>(254,rk[z])));--rr[p];if(rr[p]==0){att[p]=1;rk[p]=uint16_t(mx[p]+1);q.push_back(p);}}});}uint16_t minr=65535;uint64_t mins=0,pure=0;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&att[c]&&!B[c]){pure++;if(rk[c]<minr){minr=rk[c];mins=c;}}cout<<"RANK3 "<<f.name<<" pure="<<pure<<" min_rank="<<minr<<" state="<<mins<<"\n";if(pure){S st=a.dec(mins);Arena::MoveStats ms;a.successors(st,ss,&ms);cout<<"MIN turn="<<st.turn<<" sig="<<a.sigOf(st)<<" promo="<<ms.promo<<" succ="<<ss.size()<<"\n";for(auto x:ss)cout<<"  SUCC "<<x<<" B="<<int(B[x])<<" A="<<int(att[x])<<" rank="<<rk[x]<<" A71="<<int(A71[x])<<" A74="<<int(A74[x])<<" A114="<<int(A114[x])<<"\n";}return 0;}return 2;}
 if(mode.rfind("pairx:",0)==0){string z=mode.substr(6);vector<string>v;stringstream zs(z);string tok;while(getline(zs,tok,':'))v.push_back(tok);if(v.size()!=3)return 2;string nm=v[0],i=v[1],j=v[2];for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());auto load=[&](string tag){vector<uint8_t>x(a.RAW);ifstream fi("/mnt/data/"+f.name+"_A"+tag+".bin",ios::binary);if(!fi){cerr<<"missing "<<tag<<"\n";exit(4);}fi.read((char*)x.data(),x.size());return x;};auto A1=load(i),A2=load(j),AU=load(i+"_"+j);uint64_t pure=0,puref=0,kern=0,kernf=0;vector<uint64_t>ss;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&AU[c]&&!A1[c]&&!A2[c]){pure++;S st=a.dec(c);bool full=a.sigOf(st)==15;if(full)puref++;if(st.turn!=1)continue;Arena::MoveStats ms;a.successors(st,ss,&ms);if(ms.promo||ss.empty())continue;bool allB=true,all1=true,all2=true;for(auto x:ss){if(!(A1[x]||A2[x]))allB=false;if(!A1[x])all1=false;if(!A2[x])all2=false;}if(allB&&!all1&&!all2){kern++;if(full)kernf++;}}cout<<"PAIRX "<<f.name<<" "<<i<<"+"<<j<<" pure_all="<<pure<<" kernel_all="<<kern<<" amp_all="<<(kern?double(pure)/kern:0)<<" pure_full="<<puref<<" kernel_full="<<kernf<<" amp_full="<<(kernf?double(puref)/kernf:0)<<"\n";return 0;}return 2;}
 if(mode.rfind("hyper3:",0)==0){string nm=mode.substr(7);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);if(!fv)return 3;fv.read((char*)a.valid.data(),a.valid.size());auto load=[&](string tag){vector<uint8_t>v(a.RAW);ifstream fi("/mnt/data/"+f.name+"_A"+tag+".bin",ios::binary);if(!fi){cerr<<"missing A"<<tag<<"\n";exit(4);}fi.read((char*)v.data(),v.size());return v;};auto A71=load("7_11"),A74=load("7_14"),A114=load("11_14"),Aall=load("7_11_14");vector<uint8_t>B(a.RAW,0),K(a.RAW,0),cl(a.RAW,0);for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c])B[c]=A71[c]||A74[c]||A114[c];uint64_t pure=0,puref=0,kern=0,kernf=0,pureW=0,pureB=0,blackAllB=0,blackPromo=0,blackEmpty=0,blackAll71=0,blackAll74=0,blackAll114=0;vector<uint64_t>ss;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&Aall[c]&&!B[c]){pure++;S st=a.dec(c);bool full=a.sigOf(st)==15;if(full)puref++;if(st.turn==0){pureW++;continue;}pureB++;Arena::MoveStats ms;a.successors(st,ss,&ms);if(ms.promo){blackPromo++;continue;}if(ss.empty()){blackEmpty++;continue;}bool allB=true,all71=true,all74=true,all114=true;for(auto x:ss){if(!B[x])allB=false;if(!A71[x])all71=false;if(!A74[x])all74=false;if(!A114[x])all114=false;}if(allB)blackAllB++;if(all71)blackAll71++;if(all74)blackAll74++;if(all114)blackAll114++;if(allB&&!all71&&!all74&&!all114){K[c]=1;kern++;if(full)kernf++;}}
   // Independently reconstruct irreducible region from K by queue-based residual backward closure outside B.
   cl=K;deque<uint64_t>cq;vector<uint16_t>rrem(a.RAW,0);for(uint64_t c=0;c<a.RAW;c++)if(K[c])cq.push_back(c);
   for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&!B[c]&&!cl[c]){S st=a.dec(c);if(st.turn!=1)continue;Arena::MoveStats ms;a.successors(st,ss,&ms);uint32_t nout=0;for(auto x:ss)if(!B[x])nout++;uint32_t blocker=(ms.promo||(ss.empty()&&!ms.promo))?1:0;rrem[c]=uint16_t(min<uint32_t>(65535,nout+blocker));}
   while(!cq.empty()){uint64_t z=cq.front();cq.pop_front();a.predecessors(z,[&](uint64_t p){if(!a.valid[p]||B[p]||cl[p])return;S ps=a.dec(p);if(ps.turn==0){cl[p]=1;cq.push_back(p);}else if(rrem[p]>0){--rrem[p];if(rrem[p]==0){cl[p]=1;cq.push_back(p);}}});}
   uint64_t cla=0,clf=0,miss=0,extra=0;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]){if(cl[c]){cla++;if(a.sigOf(a.dec(c))==15)clf++;if(!(Aall[c]&&!B[c]))extra++;}if(Aall[c]&&!B[c]&&!cl[c])miss++;}
   cout<<"HYPER3 "<<f.name<<" pure_all="<<pure<<" pure_Wturn="<<pureW<<" pure_Bturn="<<pureB<<" black_allB="<<blackAllB<<" black_promo="<<blackPromo<<" black_empty="<<blackEmpty<<" black_all71="<<blackAll71<<" black_all74="<<blackAll74<<" black_all114="<<blackAll114<<" kernel_all="<<kern<<" amp_all="<<(kern?double(pure)/kern:0)<<" pure_full="<<puref<<" kernel_full="<<kernf<<" amp_full="<<(kernf?double(puref)/kernf:0)<<" closure_all="<<cla<<" closure_full="<<clf<<" closure_missing="<<miss<<" closure_extra="<<extra<<"\n";return 0;}return 2;}
 if(mode.rfind("group3:",0)==0){string nm=mode.substr(7);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary),fo("/mnt/data/"+f.name+"_out.bin",ios::binary),fa("/mnt/data/"+f.name+"_A7_11_14.bin",ios::binary);if(!fv||!fo||!fa)return 3;fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());vector<uint8_t>A(a.RAW);fa.read((char*)A.data(),A.size());struct G{uint8_t mask=0;uint64_t n=0,w=0,b=0,d=0;};unordered_map<uint64_t,G>g;g.reserve(600000);uint64_t rs=0,rw=0,rb=0,rd=0;for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]){S st=a.dec(c);if(a.sigOf(st)!=15||A[c])continue;rs++;int wt=a.whiteTruth(c);if(wt>0)rw++;else if(wt<0)rb++;else rd++;S k=st;k.wk=0;uint64_t key=a.code(k);auto &z=g[key];z.n++;if(wt>0){z.mask|=1;z.w++;}else if(wt<0){z.mask|=2;z.b++;}else{z.mask|=4;z.d++;}}
   uint64_t mixed=0,mw=0,mb=0,md=0;for(auto &kv:g){auto &z=kv.second;if((z.mask&(z.mask-1))!=0){mixed++;mw+=z.w;mb+=z.b;md+=z.d;}}
   // Frozen G6 double-brink promotion-race slab: both fixed pawns are one move from promotion; tempo-adjusted times differ by exactly one ply for either side to move, hence |TW-TB|<=3 universally.
   double mixedPct=mixed?100.0:0.0,allPct=g.size()?100.0:0.0;cout<<"GROUP3 "<<f.name<<" residual_states="<<rs<<" residual_W="<<rw<<" residual_B="<<rb<<" residual_D="<<rd<<" residual_geometries="<<g.size()<<" mixed_geometries="<<mixed<<" mixed_Wplacements="<<mw<<" mixed_Bplacements="<<mb<<" mixed_Dplacements="<<md<<" race_slab_mixed_pct="<<mixedPct<<" race_slab_all_pct="<<allPct<<" localization_lift_pp="<<(mixedPct-allPct)<<"\n";return 0;}return 2;}
 if(mode.rfind("direct:",0)==0){string nm=mode.substr(7);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary),fo("/mnt/data/"+f.name+"_out.bin",ios::binary);if(!fv||!fo)return 3;fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());a.analyzeG7(false);return 0;}return 2;}
 if(mode.rfind("analyze:",0)==0){string nm=mode.substr(8);for(auto f:fams)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);ifstream fo("/mnt/data/"+f.name+"_out.bin",ios::binary);if(!fv||!fo){cerr<<"missing masks\n";return 3;}fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());a.analyzeG7();return 0;}return 2;}
 if(mode.rfind("solve:",0)==0){string nm=mode.substr(6);for(auto f:fams)if(f.name==nm){Arena a(f);auto r=a.solve();cout<<"RESULT "<<f.name<<" static="<<r.st<<" W="<<r.W<<" B="<<r.B<<" D="<<r.D<<" sec="<<fixed<<setprecision(3)<<r.sec<<"\n";return 0;}cerr<<"unknown family\n";return 2;}
 return 0;
}
