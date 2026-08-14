#define main g75_embedded_main
#include "/mnt/data/g7_5_brink_analysis.cpp"
#undef main

struct Counts { uint64_t all=0, full=0; };

static vector<uint8_t> loadMask(const string& p, uint64_t n){
  vector<uint8_t> v(n); ifstream f(p, ios::binary); if(!f){cerr<<"missing "<<p<<"\n"; exit(3);} f.read((char*)v.data(), v.size()); return v;
}
static Counts cntMask(Arena& a,const vector<uint8_t>&v){ Counts z; for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&v[c]){z.all++; if(a.sigOf(a.dec(c))==15)z.full++;} return z; }

// Strict White attractor to arbitrary target, bounded to an already-certified White-winning upper attractor.
static vector<uint8_t> attrBound(Arena& a,const vector<uint8_t>&T,const vector<uint8_t>&upper){
  vector<uint8_t>A(a.RAW,0); vector<uint16_t> rem(a.RAW,0); deque<uint64_t>q; vector<uint64_t>ss;
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&upper[c]&&T[c]){A[c]=1;q.push_back(c);}  
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&upper[c]&&!A[c]){
    S s=a.dec(c); if(s.turn!=1) continue; Arena::MoveStats ms; a.successors(s,ss,&ms);
    uint32_t n=ss.size()+(ms.promo?1:0)+((ss.empty()&&!ms.promo)?1:0);
    rem[c]=uint16_t(min<uint32_t>(65535,n));
  }
  while(!q.empty()){
    uint64_t z=q.front();q.pop_front();
    a.predecessors(z,[&](uint64_t p){ if(!upper[p]||A[p])return; S ps=a.dec(p); if(ps.turn==0){A[p]=1;q.push_back(p);} else if(rem[p]>0 && --rem[p]==0){A[p]=1;q.push_back(p);} });
  }
  return A;
}

static vector<uint8_t> checkAttrBound(Arena& a,const vector<uint8_t>&T,const vector<uint8_t>&upper){
  vector<uint8_t>C(a.RAW,0); vector<uint16_t>rem(a.RAW,0); deque<uint64_t>q; vector<uint64_t>ss;
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&upper[c]&&T[c]){C[c]=1;q.push_back(c);}  
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&upper[c]&&!C[c]){ S s=a.dec(c); if(s.turn!=1)continue; Arena::MoveStats ms;a.successors(s,ss,&ms); uint32_t n=ss.size()+(ms.promo?1:0)+((ss.empty()&&!ms.promo)?1:0); rem[c]=uint16_t(min<uint32_t>(65535,n)); }
  while(!q.empty()){
    uint64_t z=q.front();q.pop_front(); bool zCheck=a.inCheck(a.dec(z));
    a.predecessors(z,[&](uint64_t p){ if(!upper[p]||C[p])return; S ps=a.dec(p); if(ps.turn==0){ if(T[z]||zCheck){C[p]=1;q.push_back(p);} } else if(rem[p]>0 && --rem[p]==0){C[p]=1;q.push_back(p);} });
  }
  return C;
}

struct PivotResult { vector<uint8_t>K,R; Counts diff,kern,closure; uint64_t missing=0,extra=0; };
static PivotResult pivotFactor(Arena& a,const vector<uint8_t>&T,const vector<uint8_t>&A,const vector<uint8_t>&C){
  PivotResult pr; pr.K.assign(a.RAW,0); pr.R.assign(a.RAW,0); vector<uint16_t>rem(a.RAW,0); deque<uint64_t>q; vector<uint64_t>ss;
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&A[c]&&!C[c]){
    pr.diff.all++; S s=a.dec(c); if(a.sigOf(s)==15)pr.diff.full++; if(s.turn!=0)continue; Arena::MoveStats ms;a.successors(s,ss,&ms); bool piv=false;
    for(auto z:ss) if(C[z]&&!T[z]&&!a.inCheck(a.dec(z))){piv=true;break;}
    if(piv){pr.K[c]=pr.R[c]=1;q.push_back(c);pr.kern.all++;if(a.sigOf(s)==15)pr.kern.full++;}
  }
  for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&A[c]&&!C[c]&&!pr.R[c]){S s=a.dec(c);if(s.turn!=1)continue;Arena::MoveStats ms;a.successors(s,ss,&ms);uint32_t n=0;for(auto z:ss)if(!C[z])n++;uint32_t blocker=ms.promo||(ss.empty()&&!ms.promo);rem[c]=uint16_t(min<uint32_t>(65535,n+blocker));}
  while(!q.empty()){uint64_t z=q.front();q.pop_front();a.predecessors(z,[&](uint64_t p){if(!A[p]||C[p]||pr.R[p])return;S ps=a.dec(p);if(ps.turn==0){pr.R[p]=1;q.push_back(p);}else if(rem[p]>0&&--rem[p]==0){pr.R[p]=1;q.push_back(p);}});}  
  for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]){if(pr.R[c]){pr.closure.all++;if(a.sigOf(a.dec(c))==15)pr.closure.full++;if(!(A[c]&&!C[c]))pr.extra++;}if(A[c]&&!C[c]&&!pr.R[c])pr.missing++;}
  return pr;
}

int main(int argc,char**argv){
  ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();
  string nm=argc>1?argv[1]:"BB_same_c7_f2";
  vector<Fam> fams={mk("BB_opp_d7_e2","B","B",0,1,"d7","e2"),mk("BB_same_c7_f2","B","B",0,0,"c7","f2")};
  for(auto f:fams) if(f.name==nm){
    Arena a(f); a.valid=loadMask("/mnt/data/"+nm+"_valid.bin",a.RAW); a.out=loadMask("/mnt/data/"+nm+"_out.bin",a.RAW);
    auto A71=loadMask("/mnt/data/"+nm+"_A7_11.bin",a.RAW), A74=loadMask("/mnt/data/"+nm+"_A7_14.bin",a.RAW), A114=loadMask("/mnt/data/"+nm+"_A11_14.bin",a.RAW), Aall=loadMask("/mnt/data/"+nm+"_A7_11_14.bin",a.RAW);
    vector<uint8_t>B(a.RAW,0),P(a.RAW,0),K(a.RAW,0); vector<uint64_t>ss;
    for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]){B[c]=A71[c]||A74[c]||A114[c]; if(Aall[c]&&!B[c])P[c]=1;}
    // Reconstruct hyperkernel exactly for diagnostics.
    for(uint64_t c=0;c<a.RAW;c++) if(a.valid[c]&&P[c]){S s=a.dec(c);if(s.turn!=1)continue;Arena::MoveStats ms;a.successors(s,ss,&ms);if(ms.promo||ss.empty())continue;bool allB=true,all71=true,all74=true,all114=true;for(auto x:ss){if(!B[x])allB=false;if(!A71[x])all71=false;if(!A74[x])all74=false;if(!A114[x])all114=false;}if(allB&&!all71&&!all74&&!all114)K[c]=1;}
    auto pc=cntMask(a,P),kc=cntMask(a,K),allc=cntMask(a,Aall);
    cerr<<"derived target P built: "<<pc.all<<" kernel="<<kc.all<<"\n";
    auto AP=attrBound(a,P,Aall); auto apc=cntMask(a,AP); cerr<<"Attr(P)="<<apc.all<<"\n";
    auto CP=checkAttrBound(a,P,AP); auto cpc=cntMask(a,CP); cerr<<"CheckAttr(P)="<<cpc.all<<"\n";
    auto piv=pivotFactor(a,P,AP,CP);
    // Cross classification: whether AP states are already in proper-subunion base B, original CHECK corridor, or original hyper-pure P.
    vector<uint8_t>Corig=loadMask("/mnt/data/"+nm+"_CHECKCORRIDOR.bin",a.RAW);
    uint64_t ap_in_B=0,ap_in_P=0,ap_in_Corig=0,ap_out_Corig=0,cp_in_P=0;
    for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&AP[c]){ap_in_B+=B[c];ap_in_P+=P[c];ap_in_Corig+=Corig[c];ap_out_Corig+=!Corig[c];if(CP[c]&&P[c])cp_in_P++;}
    cout<<setprecision(10)
      <<"MULTILEVEL "<<nm
      <<" Aall="<<allc.all<<" Aall_full="<<allc.full
      <<" hyperkernel="<<kc.all<<" hyperkernel_full="<<kc.full
      <<" hyperpure="<<pc.all<<" hyperpure_full="<<pc.full
      <<" hyper_amp="<<(kc.all?double(pc.all)/kc.all:0)
      <<" AttrPure="<<apc.all<<" AttrPure_full="<<apc.full
      <<" second_amp_over_pure="<<(pc.all?double(apc.all)/pc.all:0)
      <<" second_amp_over_kernel="<<(kc.all?double(apc.all)/kc.all:0)
      <<" CheckToPure="<<cpc.all<<" CheckToPure_full="<<cpc.full
      <<" check_retention="<<(apc.all?100.0*cpc.all/apc.all:0)
      <<" quiet_required="<<piv.diff.all<<" pivots="<<piv.kern.all
      <<" pivot_amp="<<(piv.kern.all?double(piv.diff.all)/piv.kern.all:0)
      <<" pivot_missing="<<piv.missing<<" pivot_extra="<<piv.extra
      <<" ap_in_properB="<<ap_in_B<<" ap_in_hyperpure="<<ap_in_P
      <<" ap_in_original_check="<<ap_in_Corig<<" ap_out_original_check="<<ap_out_Corig
      <<"\n";
    // Save derived target/attractor masks for downstream proof-DAG audits.
    ofstream fp("/mnt/data/G7_8_"+nm+"_HYPERPURE.bin",ios::binary);fp.write((char*)P.data(),P.size());
    ofstream fk("/mnt/data/G7_8_"+nm+"_HYPERKERNEL.bin",ios::binary);fk.write((char*)K.data(),K.size());
    ofstream fa("/mnt/data/G7_8_"+nm+"_ATTR_HYPERPURE.bin",ios::binary);fa.write((char*)AP.data(),AP.size());
    ofstream fc("/mnt/data/G7_8_"+nm+"_CHECK_HYPERPURE.bin",ios::binary);fc.write((char*)CP.data(),CP.size());
    return 0;
  }
  return 2;
}
