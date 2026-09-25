#define main g75_embedded_main
#include "/mnt/data/g7_5_brink_analysis.cpp"
#undef main
static vector<uint8_t> ld(const string&p,uint64_t n){vector<uint8_t>v(n);ifstream f(p,ios::binary);if(!f){cerr<<"missing "<<p<<"\n";exit(3);}f.read((char*)v.data(),v.size());return v;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);initMoves();auto f=mk("BB_same_c7_f2","B","B",0,0,"c7","f2");Arena a(f);a.valid=ld("/mnt/data/BB_same_c7_f2_valid.bin",a.RAW);a.out=ld("/mnt/data/BB_same_c7_f2_out.bin",a.RAW);auto Aall=ld("/mnt/data/BB_same_c7_f2_A7_11_14.bin",a.RAW);auto P=ld("/mnt/data/G7_8_BB_same_c7_f2_HYPERPURE.bin",a.RAW);auto AP=ld("/mnt/data/G7_8_BB_same_c7_f2_ATTR_HYPERPURE.bin",a.RAW);auto CP=ld("/mnt/data/G7_8_BB_same_c7_f2_CHECK_HYPERPURE.bin",a.RAW);vector<uint64_t>ss;uint64_t ap_inbad=0,ap_outqual=0,cp_inbad=0,cp_outqual=0,checked=0;
for(uint64_t c=0;c<a.RAW;c++)if(a.valid[c]&&Aall[c]&&a.sigOf(a.dec(c))==15){checked++;S s=a.dec(c);Arena::MoveStats ms;a.successors(s,ss,&ms);
  auto qualA=[&](){if(P[c])return true;if(s.turn==0){for(auto z:ss)if(AP[z])return true;return false;}bool blocker=ms.promo||(ss.empty()&&!ms.promo);if(blocker||ss.empty())return false;for(auto z:ss)if(!AP[z])return false;return true;};
  bool qa=qualA();if(AP[c]&&!qa)ap_inbad++;if(!AP[c]&&qa)ap_outqual++;
  auto qualC=[&](){if(P[c])return true;if(s.turn==0){for(auto z:ss)if(CP[z]&&(P[z]||a.inCheck(a.dec(z))))return true;return false;}bool blocker=ms.promo||(ss.empty()&&!ms.promo);if(blocker||ss.empty())return false;for(auto z:ss)if(!CP[z])return false;return true;};
  bool qc=qualC();if(CP[c]&&!qc)cp_inbad++;if(!CP[c]&&qc)cp_outqual++;
}
cout<<"MULTILEVEL_AUDIT checked_full_Aall="<<checked<<" AP_member_violations="<<ap_inbad<<" AP_outside_qualifiers="<<ap_outqual<<" CP_member_violations="<<cp_inbad<<" CP_outside_qualifiers="<<cp_outqual<<"\n";
}
