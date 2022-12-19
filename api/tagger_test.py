# %%
from baikal_tagger import nlp_tagger

sample = '''
대통령실이 '이태원 압사 참사' 유가족과 부상자에게 정당한 보상을 하기 위해 특별법을 제정하는 방안도 검토하는 것으로 알려졌다.

조만간 경찰 특별수사본부의 중간수사 결과가 발표되면 당·정 주도로 국가 과실 인정 여부에 따른 배상 또는 보상 논의가 급물살을 탈 것으로 보인다.

대통령실 핵심 관계자는 22일 연합뉴스와 통화에서 "사고 책임이 드러나면 현행법에 따라 조치해야 하고, 부족한 부분에 대해서는 특별법 등 필요한 법령을 만들어 보완할 방침"이라고 밝혔다.

다른 관계자는 통화에서 "법적으로 미비한 부분이 있다면 특별법을 만들 수 있다"며 "현재 내부적으로 검토 중"이라고 전했다.

대통령실 안팎에서 특별법 제정이 거론되는 것은 유가족과 부상자가 국가를 상대로 제기하는 손해배상 청구소송에서 승소할 가능성이 큰 경우를 염두에 두기 때문으로 보인다.

특별법이 효력을 얻으면 개별 소송 없이 심의위원회 등을 통한 일괄 배상이 이뤄질 수 있다.

다만, 대통령실이 미리 국가배상책임을 인정하며 '수사 가이드라인'을 제시한 것으로 비칠 수 있어 조심스러워 하는 기류도 읽힌다.

이와 관련, 윤석열 대통령은 전날 한덕수 국무총리와의 주례회동에서 "유가족에게 정당한 보상을 받을 수 있는 권리를 드리기 위해서라도 실체적 진실 파악이 중요하다"고 언급했다.

여기서 '실체적 진실'이란 정확한 사고 발생 경위를 뜻하며, 경찰의 강제·과학수사를 통해 밝혀질 내용이라는 게 대통령실 관계자들의 설명이다.

최근 국회에서 여야가 논의 중인 국정조사에 선을 긋고 수사를 통한 진상규명에 거듭 힘을 실은 것으로 해석될 여지가 있는 대목이다.

윤 대통령은 이날 국무회의 모두발언에서도 유가족과 부상자에 대한 충분한 지원을 강조하며 "경찰 특수본은 철저한 진상 규명에 총력을 다해 주시기 바란다"고 당부했다.

특수본은 이르면 이번 주 내로 피의자 신병 처리 여부를 확정할 전망이다. 이후 특별법 제정이 실제 논의될 경우 대통령실보다 당정이 나설 가능성이 커 보인다.

대통령실 관계자는 통화에서 "현재는 가장 빠르고 정확하고 엄정한 진상규명에 집중하는 상황"이라며 "과실이 명확하게 드러날 경우 국가배상도 신속하게 논의될 수 있다"고 강조했다.

'''
sample_res = nlp_tagger(sample)
print(sample_res)