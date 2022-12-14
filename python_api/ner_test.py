# %%
# from ner_module import ner_predict
from ner_module_kss import ner_predict

sample = '''
여야 원내대표가 16일 오후 김진표 국회의장 주재로 다시 얼굴을 맞대고 내년도 예산안 협상을 이어갔지만 기존 입장만 되풀이하며 진전을 보지 못했다.

이날 회동은 전날 김 의장이 내놓은 중재안을 국민의힘이 받아들이지 않으면서, 예산안 협상이 또 불발된 이후 첫 만남이었다.

양당 원내대표는 이날도 서로에게 '양보'를 요구하며 지루한 대치 국면을 이어갔다.

국민의힘 주호영 원내대표는 "예산안 처리 법정 기한과 정기국회 기간이 도과한 지 꽤 됐는데도 불구하고 내년도 예산안을 합의 처리 못 해 국민께 죄송하다"며 입을 열었다.

이어 "헌법이나 법률에도 예산 편성과 운영에는 정부에 주도권을 주고 있다"며 "정부가 위기의 순간에 빠르게, 계획대로 재정 운용을 집행할 수 있게 협조해 달라고 민주당에 간곡히 부탁드린다"고 말했다.

그러면서 "위기의 순간에 정부가 소신껏 팀을 짜 제때 좀 (일을) 할 수 있게끔 민주당이 조금은 양보하고 도와주시길 바란다"며 "(민주당은) 지난 5년간 하실 만큼 했지 않나"라고 되물었다.

주 원내대표는 "지금은 최대 위기이고 법인세의 경우 해외 직접 투자 유치 때문에 사활을 거는 문제가 돼 있다"며 "국회의장 중재안인 1%포인트 인하만으로는 대만(20%)과 싱가포르(17%)와 경쟁하기 어려워 저희들이 선뜻 (중재안을) 받지 못한 상태"라고 강조했다.

역시 올해 연말까지로 예정된 승용차 개소세 30% 인하 조치는 내년 6월 말까지 6개월간 연장된다.

2018년 7월부터 적용된 승용차 개소세 인하 혜택은 이로써 약 5년 동안 이어지게 됐다.

정부는 이를 통해 경기 침체기 승용차 소비를 촉진하겠다는 방침이다.

승용차를 살 때는 원래 5%의 개소세가 붙는데, 이를 30% 낮춰 3.5%로 적용하면 교육세(개소세액의 30%)는 물론 차량 구매 금액과 연동된 부가세와 취득세까지 함께 줄어들면서 전체 세금 부담을 낮추는 효과가 있다.

개소세 인하 혜택 한도는 100만원이다. 차량 구매시 한도를 모두 채우면 소비자는 개소세 100만원, 교육세 30만원, 부가세 13만원 등 최대 143만원의 세금 인하 혜택을 받을 수 있다.

다만 코로나19 시기 일시적으로 도입된 개소세 인하 조치가 장기간 이어지면서 정책의 '약발'이 떨어졌다는 지적도 만만치 않다.

정부 내부에서도 개소세 인하 연장에 대한 의견이 엇갈리며 내년 세입 예산안에는 인하 조치가 반영되지 않은 것으로 전해졌다.

정부는 "이번 연장 조치는 승용차 구매 시 가격 부담을 완화하고, 기존 인하 기간에 차량 구매 계약을 체결한 소비자가 차량 출고 지연으로 혜택을 받지 못하는 사례를 감안한 것"이라고 설명했다.

LNG·유연탄 등 발전 연료에 대한 개소세 15% 인하 조치도 현재와 같은 수준으로 6개월간 연장한다.

발전 원가 부담에 따른 공공요금 인상 압력을 낮추겠다는 취지다.

관련 시행령은 향후 입법예고와 국무회의를 거쳐 내년 1월 1일부터 시행된다.
'''

sample_res = ner_predict(sample)
print(sample_res)