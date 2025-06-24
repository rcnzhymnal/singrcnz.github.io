@echo off
rem Define list of Psalm pdfs in the correct order and return in environment variable 'psalms'

set range00=psalm001_*.pdf psalm001b_*.pdf psalm00[2-9]_*.pdf
set range01=psalm01[0-5]_*.pdf psalm016_*.pdf psalm016b_*.pdf psalm01[7-9]_*.pdf psalm019b_*.pdf
set range02=psalm02[0-2]_*.pdf psalm022b_*.pdf psalm022c_*.pdf psalm02[3-5]_*.pdf psalm025b_*.pdf psalm02[6-9]_*.pdf
set range03=psalm03[0-9]_*.pdf
set range04=psalm04[0-2]_*.pdf psalm042b_*.pdf psalm043b_*.pdf psalm04[4-7]_*.pdf psalm047b_*.pdf psalm04[8-9]_*.pdf
set range05=psalm05[0-1]_*.pdf psalm051b*.pdf psalm05[2-9]_*.pdf
set range06=psalm06[0-3]_*.pdf psalm063b_*.pdf psalm06[4-5]_*.pdf psalm065b_*.pdf psalm06[6-8]_*.pdf psalm068?_*.pdf psalm069_*.pdf psalm069b_*.pdf
set range07=psalm07[0-2]*.pdf  psalm073_*.pdf psalm073b_*.pdf psalm07[4-8]_*.pdf psalm078b_*.pdf psalm079_*.pdf
set range08=psalm08[0-1]_*.pdf psalm081b_*.pdf psalm08[2-6]_*.pdf psalm086b_*.pdf psalm087_*.pdf psalm087b_*.pdf psalm08[8-9]*.pdf
set range09=psalm09[0-5]_*.pdf psalm095b_*.pdf psalm09[6-8]_*.pdf psalm098b_*.pdf psalm099_*.pdf
set range10=psalm100_*.pdf psalm100b_*.pdf psalm10[1-3]_*.pdf psalm103b_*.pdf psalm10[4-5]_*.pdf psalm105b_*.pdf psalm10[6-9]_*.pdf
set range11=psalm11[0-6]_*.pdf psalm116b_*.pdf psalm11[7-8]_*.pdf psalm118b_*.pdf psalm119v0[0-2]?_*.pdf psalm119v025b_*.pdf psalm119v0[3-9]?_*.pdf psalm119v1*.pdf
set range12=psalm12[0-9]_*.pdf
set range13=psalm13[0-3]_*.pdf psalm133b_*.pdf psalm13[4-7]_*.pdf psalm137b_*.pdf psalm13[8-9]_*.pdf psalm139b_*.pdf
set range14=psalm14[0-5]_*.pdf psalm145b_*.pdf psalm14[6-9]_*.pdf psalm149b_*.pdf psalm150_*.pdf psalm150b_*.pdf
set psalms=%range00% %range01% %range02% %range03% %range04% %range05% %range06% %range07% %range08% %range09% %range10% %range11% %range12% %range13% %range14% %range15%
