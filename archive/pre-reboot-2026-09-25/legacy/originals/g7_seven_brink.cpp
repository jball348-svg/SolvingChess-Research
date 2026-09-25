#include <bits/stdc++.h>
using namespace std;
static inline int F(int s){return s&7;} static inline int R(int s){return s>>3;} static inline int C(int s){return (F(s)+R(s))&1;}
static inline int cheb(int a,int b){return max(abs(F(a)-F(b)),abs(R(a)-R(b)));}
vector<int> kingMv[64];
void initMoves(){for(int s=0;s<64;s++)for(int df=-1;df<=1;df++)for(int dr=-1;dr<=1;dr++)if(df||dr){int f=F(s)+df,r=R(s)+dr;if(f>=0&&f<8&&r>=0&&r<8)kingMv[s].push_back(r*8+f);}}
string sqn(int s){string z;z+=char('a'+F(s));z+=char('1'+R(s));return z;}
struct Fam{string name;int wc,bc;int wa,wcPawn,bp;};
struct S{int wk,bk,wb,bb; bool pa,pc,pb; int turn;}; // turn 0 white,1 black; bishops -1 absent
struct Arena{
 Fam f; vector<int>wSquares,bSquares,wIndex,bIndex; int nw=33,nb=33; uint64_t RAW;
 vector<uint8_t> valid,out,rem;
 Arena(Fam ff):f(ff){wIndex.assign(64,-1);bIndex.assign(64,-1);for(int s=0;s<64;s++){if(C(s)==f.wc){wIndex[s]=wSquares.size();wSquares.push_back(s);}if(C(s)==f.bc){bIndex[s]=bSquares.size();bSquares.push_back(s);}}RAW=uint64_t(64)*64*33*33*8*2;}
 inline uint64_t code(const S&s)const{int wi=s.wb<0?32:wIndex[s.wb],bi=s.bb<0?32:bIndex[s.bb];int bits=(s.pa?4:0)|(s.pc?2:0)|(s.pb?1:0);uint64_t x=s.wk;x=x*64+s.bk;x=x*33+wi;x=x*33+bi;x=x*8+bits;x=x*2+s.turn;return x;}
 inline S dec(uint64_t x)const{S s;s.turn=x&1;x>>=1;int bits=x&7;x>>=3;s.pa=bits&4;s.pc=bits&2;s.pb=bits&1;int bi=x%33;x/=33;int wi=x%33;x/=33;s.bk=x%64;x/=64;s.wk=x%64;s.wb=wi==32?-1:wSquares[wi];s.bb=bi==32?-1:bSquares[bi];return s;}
 bool occ(const S&s,int q)const{return s.wk==q||s.bk==q||s.wb==q||s.bb==q||(s.pa&&q==f.wa)||(s.pc&&q==f.wcPawn)||(s.pb&&q==f.bp);}
 bool bishopAtt(int from,int to,const S&s,int ignore=-2,int extra=-1)const{if(from<0)return false;int df=F(to)-F(from),dr=R(to)-R(from);if(df==0||abs(df)!=abs(dr))return false;int sf=df>0?1:-1,sr=dr>0?1:-1,ff=F(from)+sf,rr=R(from)+sr;while(ff!=F(to)||rr!=R(to)){int q=rr*8+ff;if(q!=ignore&&(q==extra||occ(s,q)))return false;ff+=sf;rr+=sr;}return true;}
 bool pawnAtt(bool white,int p,int q)const{return abs(F(q)-F(p))==1&&R(q)-R(p)==(white?1:-1);}
 bool whiteAtt(const S&s,int q,int ignore=-2,int extra=-1)const{if(cheb(s.wk,q)<=1)return true;if(s.pa&&f.wa!=ignore&&pawnAtt(true,f.wa,q))return true;if(s.pc&&f.wcPawn!=ignore&&pawnAtt(true,f.wcPawn,q))return true;if(s.wb>=0&&s.wb!=ignore&&bishopAtt(s.wb,q,s,ignore,extra))return true;return false;}
 bool blackAtt(const S&s,int q,int ignore=-2,int extra=-1)const{if(cheb(s.bk,q)<=1)return true;if(s.pb&&f.bp!=ignore&&pawnAtt(false,f.bp,q))return true;if(s.bb>=0&&s.bb!=ignore&&bishopAtt(s.bb,q,s,ignore,extra))return true;return false;}
 bool staticValid(const S&s)const{
   if(s.wk==s.bk||cheb(s.wk,s.bk)<=1)return false;vector<int>v={s.wk,s.bk};if(s.wb>=0)v.push_back(s.wb);if(s.bb>=0)v.push_back(s.bb);if(s.pa)v.push_back(f.wa);if(s.pc)v.push_back(f.wcPawn);if(s.pb)v.push_back(f.bp);sort(v.begin(),v.end());for(size_t i=1;i<v.size();i++)if(v[i]==v[i-1])return false;if(s.wb>=0&&wIndex[s.wb]<0)return false;if(s.bb>=0&&bIndex[s.bb]<0)return false;
   // Side not to move cannot be in check: same frozen static-valid convention as G7F01/F02.
   if(s.turn==0&&whiteAtt(s,s.bk))return false;if(s.turn==1&&blackAtt(s,s.wk))return false;return true;
 }
 bool inCheck(const S&s)const{return s.turn==0?blackAtt(s,s.wk):whiteAtt(s,s.bk);}
 void bishopDests(int from,const S&s,vector<int>&d)const{d.clear();int dirs[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}};for(auto &z:dirs){int ff=F(from)+z[0],rr=R(from)+z[1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int q=rr*8+ff;d.push_back(q);if(occ(s,q))break;ff+=z[0];rr+=z[1];}}}
 bool promotionFrom(const S&s,bool white,int p)const{
   int dr=white?1:-1;auto own=[&](int q){if(white)return q==s.wk||q==s.wb||(s.pa&&q==f.wa)||(s.pc&&q==f.wcPawn);return q==s.bk||q==s.bb||(s.pb&&q==f.bp);};
   int rr=R(p)+dr;if(rr<0||rr>7)return false;int fwd=rr*8+F(p);
   auto safe=[&](int dest,bool capBishop){S z=s;if(white){if(p==f.wa)z.pa=false;else z.pc=false;if(capBishop)z.bb=-1;}else{z.pb=false;if(capBishop)z.wb=-1;}int king=white?z.wk:z.bk;return !(white?blackAtt(z,king,-2,dest):whiteAtt(z,king,-2,dest));};
   if(!occ(s,fwd)&&safe(fwd,false))return true;
   for(int df:{-1,1}){int ff=F(p)+df;if(ff<0||ff>7)continue;int d=rr*8+ff;if(white){if(d==s.bb&&safe(d,true))return true;}else{if(d==s.wb&&safe(d,true))return true;}}
   return false;
 }
 bool promoLegal(const S&s,bool white)const{if(white){if(s.pa&&promotionFrom(s,true,f.wa))return true;if(s.pc&&promotionFrom(s,true,f.wcPawn))return true;return false;}return s.pb&&promotionFrom(s,false,f.bp);}
 struct MoveStats{int legal=0,captures=0,checks=0;bool promo=false;};
 void successors(const S&s,vector<uint64_t>&ss,MoveStats*ms=nullptr)const{
   ss.clear();MoveStats zms;bool white=s.turn==0;int k=white?s.wk:s.bk;
   for(int nk:kingMv[k]){if(white){if(nk==s.wb||(s.pa&&nk==f.wa)||(s.pc&&nk==f.wcPawn)||nk==s.bk)continue;}else{if(nk==s.bb||(s.pb&&nk==f.bp)||nk==s.wk)continue;}S z=s;if(white)z.wk=nk;else z.bk=nk;bool cap=false;if(white){if(nk==z.bb){z.bb=-1;cap=true;}if(z.pb&&nk==f.bp){z.pb=false;cap=true;}}else{if(nk==z.wb){z.wb=-1;cap=true;}if(z.pa&&nk==f.wa){z.pa=false;cap=true;}if(z.pc&&nk==f.wcPawn){z.pc=false;cap=true;}}z.turn^=1;if(!staticValid(z))continue;ss.push_back(code(z));zms.legal++;zms.captures+=cap;zms.checks+=inCheck(z);}
   int b=white?s.wb:s.bb;if(b>=0){vector<int>d;bishopDests(b,s,d);for(int nbq:d){if(white){if(nbq==s.wk||(s.pa&&nbq==f.wa)||(s.pc&&nbq==f.wcPawn)||nbq==s.bk)continue;}else{if(nbq==s.bk||(s.pb&&nbq==f.bp)||nbq==s.wk)continue;}S z=s;bool cap=false;if(white){z.wb=nbq;if(nbq==z.bb){z.bb=-1;cap=true;}if(z.pb&&nbq==f.bp){z.pb=false;cap=true;}}else{z.bb=nbq;if(nbq==z.wb){z.wb=-1;cap=true;}if(z.pa&&nbq==f.wa){z.pa=false;cap=true;}if(z.pc&&nbq==f.wcPawn){z.pc=false;cap=true;}}z.turn^=1;if(!staticValid(z))continue;ss.push_back(code(z));zms.legal++;zms.captures+=cap;zms.checks+=inCheck(z);}}
   if(promoLegal(s,white)){zms.promo=true;zms.legal++;}if(ms)*ms=zms;
 }
 void buildValid(){valid.assign(RAW,0);uint64_t n=0;for(uint64_t c=0;c<RAW;c++){S s=dec(c);if(staticValid(s)){valid[c]=1;n++;}}cerr<<f.name<<" raw="<<RAW<<" static="<<n<<"\n";}
 template<class FN> void predecessors(uint64_t cc,FN fn)const{
   S s=dec(cc);bool prevWhite=s.turn==1;auto tryP=[&](S p){p.turn=prevWhite?0:1;if(!staticValid(p))return;uint64_t pc=code(p);if(!valid.empty()&&!valid[pc])return;vector<uint64_t>vv;successors(p,vv,nullptr);for(auto x:vv)if(x==cc){fn(pc);return;}};
   int dest=prevWhite?s.wk:s.bk;for(int o:kingMv[dest]){S p=s;if(prevWhite)p.wk=o;else p.bk=o;tryP(p);if(prevWhite){if(s.bb<0&&bIndex[dest]>=0){p=s;p.wk=o;p.bb=dest;tryP(p);}if(!s.pb&&dest==f.bp){p=s;p.wk=o;p.pb=true;tryP(p);}}else{if(s.wb<0&&wIndex[dest]>=0){p=s;p.bk=o;p.wb=dest;tryP(p);}if(!s.pa&&dest==f.wa){p=s;p.bk=o;p.pa=true;tryP(p);}if(!s.pc&&dest==f.wcPawn){p=s;p.bk=o;p.pc=true;tryP(p);}}}
   int bdest=prevWhite?s.wb:s.bb;if(bdest>=0){int dirs[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}};for(auto &di:dirs){int ff=F(bdest)+di[0],rr=R(bdest)+di[1];while(ff>=0&&ff<8&&rr>=0&&rr<8){int o=rr*8+ff;if(occ(s,o))break;S p=s;if(prevWhite)p.wb=o;else p.bb=o;tryP(p);if(prevWhite){if(s.bb<0&&bIndex[bdest]>=0){p=s;p.wb=o;p.bb=bdest;tryP(p);}if(!s.pb&&bdest==f.bp){p=s;p.wb=o;p.pb=true;tryP(p);}}else{if(s.wb<0&&wIndex[bdest]>=0){p=s;p.bb=o;p.wb=bdest;tryP(p);}if(!s.pa&&bdest==f.wa){p=s;p.bb=o;p.pa=true;tryP(p);}if(!s.pc&&bdest==f.wcPawn){p=s;p.bb=o;p.pc=true;tryP(p);}}ff+=di[0];rr+=di[1];}}}
 }
 int sig(const S&s)const{return (s.wb>=0?16:0)|(s.bb>=0?8:0)|(s.pa?4:0)|(s.pc?2:0)|(s.pb?1:0);}
 int whiteTruth(uint64_t c)const{S s=dec(c);uint8_t o=out[c];if(o==0||o==3)return 0;return ((s.turn==0&&o==1)||(s.turn==1&&o==2))?1:-1;}
 struct Res{uint64_t st=0,W=0,B=0,D=0;double sec=0;};
 Res solve(){auto t0=chrono::steady_clock::now();buildValid();out.assign(RAW,0);rem.assign(RAW,0);deque<uint64_t>q;vector<uint64_t>ss;uint64_t seedW=0,seedL=0,stal=0;
   for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);MoveStats ms;successors(s,ss,&ms);if(ms.promo){out[c]=1;q.push_back(c);seedW++;continue;}rem[c]=uint8_t(min<size_t>(255,ss.size()));if(ss.empty()){if(inCheck(s)){out[c]=2;q.push_back(c);seedL++;}else{out[c]=3;stal++;}}}
   cerr<<"seeds sidewin="<<seedW<<" sideloss="<<seedL<<" stal="<<stal<<" q="<<q.size()<<"\n";uint64_t pops=0;while(!q.empty()){uint64_t c=q.front();q.pop_front();uint8_t oc=out[c];predecessors(c,[&](uint64_t p){if(out[p])return;if(oc==2){out[p]=1;q.push_back(p);}else if(oc==1){if(rem[p]>0)--rem[p];if(rem[p]==0){out[p]=2;q.push_back(p);}}});if((++pops%2000000)==0)cerr<<"pops="<<pops<<" q="<<q.size()<<"\n";}
   uint64_t bc=0,bad=0;for(uint64_t c=0;c<RAW;c++)if(valid[c]&&c%509==0){bc++;S s=dec(c);MoveStats ms;successors(s,ss,&ms);uint8_t exp;if(ms.promo)exp=1;else if(ss.empty())exp=inCheck(s)?2:3;else{bool anyLoss=false,allWin=true;for(auto x:ss){uint8_t o=out[x];if(o==2)anyLoss=true;if(o!=1)allWin=false;}exp=anyLoss?1:(allWin?2:3);}uint8_t got=out[c]?out[c]:3;if(exp!=got)bad++;}cerr<<"bellman checked="<<bc<<" bad="<<bad<<"\n";
   {ofstream fv("/mnt/data/"+f.name+"_valid.bin",ios::binary);fv.write((char*)valid.data(),valid.size());ofstream fo("/mnt/data/"+f.name+"_out.bin",ios::binary);fo.write((char*)out.data(),out.size());}
   struct Ct{uint64_t st=0,W=0,B=0,D=0;};array<Ct,32>ct{};Res r;for(uint64_t c=0;c<RAW;c++)if(valid[c]){r.st++;S s=dec(c);auto &x=ct[sig(s)];x.st++;int t=whiteTruth(c);if(t>0){x.W++;r.W++;}else if(t<0){x.B++;r.B++;}else{x.D++;r.D++;}}for(int g=0;g<32;g++)if(ct[g].st)cout<<"SIG "<<g<<" static="<<ct[g].st<<" W="<<ct[g].W<<" B="<<ct[g].B<<" D="<<ct[g].D<<"\n";cout<<"AUDIT bellman_checked="<<bc<<" mismatches="<<bad<<"\n";r.sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();return r;
 }
 void directAnalysis(){uint64_t full=0,moves=0,caps=0,wpromo=0,bpromo=0;array<uint64_t,32>red{};vector<uint64_t>ss;for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);if(sig(s)!=31)continue;full++;MoveStats ms;successors(s,ss,&ms);moves+=ms.legal;caps+=ms.captures;if(ms.promo){if(s.turn==0)wpromo++;else bpromo++;}for(auto x:ss){int sg=sig(dec(x));if(sg!=31)red[sg]++;}}cout<<"FULL states="<<full<<" moves="<<moves<<" captures="<<caps<<" Wpromo="<<wpromo<<" Bpromo="<<bpromo<<"\n";for(int g=0;g<32;g++)if(red[g])cout<<"CAPTURE_EDGE to_SIG="<<g<<" n="<<red[g]<<"\n";
   // Matched G6 double-brink core fire: either white brink pawn gives geometric conversion core, then require black race non-dominant and both white promotion paths clear. No new opponent-bishop access guard is added here.
   uint64_t targ=0,tw=0,td=0,tb=0;for(uint64_t c=0;c<RAW;c++)if(valid[c]){S s=dec(c);if(sig(s)!=31)continue;bool core=cheb(s.wk,56)<=4||cheb(s.wk,58)<=4; // a8 or c8
      bool braced=cheb(s.bk,56)>=5&&cheb(s.bk,58)>=5;bool bRace=true; // black pawn also one move from promotion: unchanged race test cannot call it slower, so deliberately fails unless Black-to-promo square is occupied/blocked.
      // Frozen race constructor requires opponent race slower. In this triple-brink geometry clocks tie at one; hence no typed TARGET_RACE_CLEAR antecedent.
      bool hit=core&&braced&&bRace&&false; if(hit){targ++;int w=whiteTruth(c);if(w>0)tw++;else if(w==0)td++;else tb++;}}
   cout<<"G6_TARGET_UNCHANGED typed_antecedent="<<targ<<" W="<<tw<<" D="<<td<<" B="<<tb<<" note=opponent_race_slower_guard_is_false_everywhere_in_triple_brink_full_stratum\n";
 }
};
Fam mk(string n,int wc,int bc,string a,string c,string b){auto sq=[](string z){return (z[1]-'1')*8+(z[0]-'a');};return {n,wc,bc,sq(a),sq(c),sq(b)};}
int main(int argc,char**argv){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();vector<Fam> fs={mk("BB_opp_a7c7_b2",0,1,"a7","c7","b2"),mk("BB_same_a7c7_b2",0,0,"a7","c7","b2")};string mode=argc>1?argv[1]:"scan";
 if(mode=="scan"){mt19937_64 rng(0x674ULL);int N=160000;for(auto f:fs){Arena a(f);uint64_t vn=0,mv=0,cp=0,ch=0,pr=0;for(int i=0;i<N;i++){uint64_t c=rng()%a.RAW;S s=a.dec(c);if(!a.staticValid(s))continue;vn++;vector<uint64_t>ss;Arena::MoveStats ms;a.successors(s,ss,&ms);mv+=ms.legal;cp+=ms.captures;ch+=ms.checks;pr+=ms.promo;}double q=double(vn)/N;cout<<f.name<<" raw="<<a.RAW<<" est_static="<<uint64_t(llround(q*a.RAW))<<" valid_frac="<<fixed<<setprecision(5)<<q<<" mean_branch="<<setprecision(3)<<(vn?double(mv)/vn:0)<<" capture_density="<<(mv?100.0*cp/mv:0)<<" check_density="<<(mv?100.0*ch/mv:0)<<" promo_state_pct="<<(vn?100.0*pr/vn:0)<<"\n";}return 0;}
 if(mode.rfind("predaudit:",0)==0){string nm=mode.substr(10);for(auto f:fs)if(f.name==nm){Arena a(f);a.buildValid();mt19937_64 rng(0x674123ULL);uint64_t snd=0,bad=0,comp=0,miss=0;int got=0;while(got<10000){uint64_t c=rng()%a.RAW;if(!a.valid[c])continue;got++;vector<uint64_t>ps;a.predecessors(c,[&](uint64_t p){ps.push_back(p);});for(auto p:ps){snd++;S sp=a.dec(p);vector<uint64_t>vv;a.successors(sp,vv,nullptr);if(find(vv.begin(),vv.end(),c)==vv.end())bad++;}S sp=a.dec(c);vector<uint64_t>vv;a.successors(sp,vv,nullptr);for(auto x:vv){comp++;bool ok=false;a.predecessors(x,[&](uint64_t p){if(p==c)ok=true;});if(!ok)miss++;}}cout<<"PREDAUDIT "<<nm<<" sound_edges="<<snd<<" bad="<<bad<<" successor_edges="<<comp<<" missing="<<miss<<"\n";return 0;}return 2;}
 if(mode.rfind("solve:",0)==0){string nm=mode.substr(6);for(auto f:fs)if(f.name==nm){Arena a(f);auto r=a.solve();cout<<"RESULT "<<nm<<" static="<<r.st<<" W="<<r.W<<" B="<<r.B<<" D="<<r.D<<" sec="<<fixed<<setprecision(3)<<r.sec<<"\n";return 0;}return 2;}
 if(mode.rfind("direct:",0)==0){string nm=mode.substr(7);for(auto f:fs)if(f.name==nm){Arena a(f);a.valid.assign(a.RAW,0);a.out.assign(a.RAW,0);ifstream fv("/mnt/data/"+nm+"_valid.bin",ios::binary),fo("/mnt/data/"+nm+"_out.bin",ios::binary);if(!fv||!fo)return 3;fv.read((char*)a.valid.data(),a.valid.size());fo.read((char*)a.out.data(),a.out.size());a.directAnalysis();return 0;}return 2;}
 return 0;
}
