# 우주가 이미 정해져 있다면, 우리는 미래를 알 수 있을까?

> **결정론적 우주 안에 사는 관찰자는 자기 세계를 어디까지 이해할 수 있을까?**
>
> 결정론 · 카오스 · 자기참조 · 정보이론 · 안전한 실험 · AI의 학습을 잇는 공개 탐구

**[상세 연구 보고서](RESEARCH_COMPENDIUM.md) · [실험 코드와 데이터](#연구-기록과-재현-자료) · [선행연구 및 한계](RESEARCH_COMPENDIUM.md#6-학술적-위치와-선행연구)**

## 먼저, 쉬운 이야기부터

어떤 우주의 모든 일이 정확한 법칙에 따라 일어난다고 가정해 보자. 그렇다면 그 안에 사는 사람은 내일 무슨 일이 일어날지 모두 알 수 있을까?

꼭 그렇지는 않다. **미래가 정해져 있는 것**과 **그 미래를 알아낼 수 있는 것**은 다르기 때문이다.

- 일기예보가 정확한 물리 법칙을 사용하더라도, 현재 날씨를 충분히 자세히 측정하지 못하면 먼 미래를 놓칠 수 있다.
- 누군가의 행동을 예측해 알려주면, 그 사람은 그 예측을 듣고 행동을 바꿀 수 있다. 예측 발표도 세상의 사건이 된다.
- 의사가 치료를 선택하면 환자를 도울 수 있지만, 똑같은 환자를 *치료하지 않았을 때* 어떻게 됐을지는 직접 볼 수 없다.
- 인공지능이 안전한 환경에서만 학습하면 위험을 줄일 수 있다. 그러나 잘못 선택한 실험은 나중에 꼭 필요한 것을 알아낼 기회를 막을 수도 있다.

이 프로젝트는 이런 질문들을 **실제로 실행 가능한 작은 가상 우주**를 만들어 살펴본 기록이다. 철학적 생각만 나열하지 않고, 코드를 실행해 예외와 한계까지 확인하려고 했다.

## 지금까지 얻은 네 가지 결론

**1. 결정되어 있다고 해서 예측할 수 있는 것은 아니다.**  
완전히 결정론적인 우주도 관찰자에게는 무작위처럼 보일 수 있다. 관찰할 수 있는 정보가 부족하거나, 법칙을 표현하는 방식이 맞지 않을 수 있다.

**2. 관찰과 개입은 다르다.**  
아무리 오래 지켜봐도 구별되지 않는 두 우주가, 작은 실험 하나로 구별될 수도 있다. 반대로 어떤 차이는 허용된 어떤 실험으로도 알아낼 수 없다.

**3. 안전한 행동이 반드시 좋은 학습은 아니다.**  
당장 위험하지 않고 정보를 많이 주는 선택도, 이후의 실험 기회를 영구히 없앨 수 있다. *지금 아는 것*뿐 아니라 *앞으로 알아낼 수 있는 것*이 중요하다.

**4. 미래를 알리고 사용하는 행위도 미래의 일부다.**  
예언을 들은 사람이 반대로 움직이도록 설계된 경우, 정확한 공개 예언은 논리적으로 성립하지 않는다. 그렇다고 우주의 결정론이 깨진 것은 아니다.

### 그렇다면 시뮬레이션 우주는?

실제 세계와 시뮬레이션된 세계가 **우리가 수행할 수 있는 모든 관측과 실험에서 같은 결과**를 낸다면, 내부 관찰자는 그 둘을 구분하지 못할 수 있다. 하지만 이것은 **우리가 시뮬레이션 속에 있다는 증거가 아니다.** 지금까지의 실험은 실제 우주가 결정론적인지조차 판정하지 않는다.

## 왜 이런 연구를 하는가?

처음 질문은 철학적이었다. *'우주의 미래가 이미 정해져 있다면 자유의지와 지식은 무엇인가?'*

연구가 진행되자 질문이 바뀌었다.

> **지능은 자기 세계를 안전하게 이해하면서, 앞으로도 더 알아낼 수 있는 능력을 어떻게 지킬 수 있을까?**

이 질문은 현실에도 닿아 있다.

- **AI 안전성과 자율학습:** 위험한 행동을 제한하면서도, 자신이 잘못 알고 있는 것을 수정할 실험 경로를 보존할 수 있는가?
- **의료와 정책:** 개입이 성공했을 때 관측되지 않는 '개입하지 않았을 경우'를 어떻게 신중하게 추론할 것인가?
- **과학철학:** 실험 결과가 설명하는 구조와, 세계가 실제로 구현된 방식은 언제 구분 가능할까?

우리의 장기 목표는 **'미래 학습 가능성을 보존하는 안전한 행동'을 판정하는 알고리즘**을 탐구하는 것이다. 아직 실용성이 검증된 기술이나 독창적인 학술 정리는 아니다.

## 연구 기록과 재현 자료

| 단계 | 누구나 이해하는 질문 | 자료 |
|---|---|---|
| 01~02 | 미래가 정해졌어도 왜 예언은 틀릴 수 있나? | [실험](deterministic_universe_experiment.py) · [노트](deterministic_universe_research_note.md) |
| 03 | 사람들이 예측에 반응하면 사회 전체가 출렁일까? | [집단 예측 연구](reflexive_universe/research_note.md) |
| 04 | 결정론적인 세계가 진짜 난수처럼 보일 수 있을까? | [실험](deterministic_observer_lab/experiment.py) · [노트](deterministic_observer_lab/research_note.md) |
| 05 | 관찰만으로 모르는 법칙을 실험으로 밝혀낼 수 있을까? | [실험](active_observer_universe/experiment.py) · [노트](active_observer_universe/research_note.md) |
| 06 | 안전하게 살아남으면서도 진실을 알아낼 수 있을까? | [실험](safe_observer_universe/experiment.py) · [노트](safe_observer_universe/research_note.md) |
| 07 | 세상을 안정시키는 행동이 오히려 법칙을 감출까? | [실험](epistemic_closure_lab/experiment.py) · [노트](epistemic_closure_lab/research_note.md) |
| 08 | 지금 많이 아는 선택이 미래의 배움을 망칠 수 있을까? | [실험](epistemic_viability_lab/experiment.py) · [노트](epistemic_viability_lab/research_note.md) |

전체 수학적 정의, 실험 조건, 검증 범위, 반례와 참고문헌은 **[통합 연구 보고서](RESEARCH_COMPENDIUM.md)**에 정리했다.

모든 숫자는 해당 **작은 인공 모형**에서 계산한 결과다. 실제 인류 사회나 물리 우주에 그 수치가 그대로 적용된다는 주장이 아니다.

### 직접 실행하기

대부분 Python 3 표준 라이브러리만 사용한다. 예를 들어 최신의 유한상태 지식 탐색 실험은 다음과 같이 실행할 수 있다.

```bash
python epistemic_viability_lab/experiment.py
```

세부적인 실행 방법과 생성 데이터는 각 하위 폴더의 문서를 참고한다. 수학적 주장의 옳고 그름은 출력 로그만이 아니라 보고서의 가정과 증명을 함께 확인해야 한다.

## 결론: 지금의 지식보다 중요한 것

어떤 진실은 관측할 수 없다. 어떤 진실은 실험을 해야 보인다. 그리고 어떤 실험은 우리를 위험에 빠뜨리거나, 훗날 더 중요한 사실을 알아낼 기회를 없앨 수도 있다.

따라서 지능을 평가하는 질문은 '지금 얼마나 많이 알고 있는가?'에서 끝나지 않는다.

**'어떤 행동을 선택해야, 안전하게 살아남으면서 앞으로도 더 깊이 알아낼 수 있는가?'**

이것이 여덟 차례의 가상 우주 실험을 관통하는 가장 중요한 질문이자, 우리가 다음에 탐구할 문제다.

---

## Research status / English summary

**Exploratory, reproducible research — 4 November 2026.** Eight small-model studies connect deterministic dynamics, observability, self-referential forecasts, active system identification, robust safety, and future learning capacity. A deterministic world need not be predictable to an embedded observer; interventions can reveal hidden laws but may also destroy future opportunities to learn.

**No evidence for a simulated universe, proof of physical determinism, discovery of free will, or established academic novelty is claimed.** The mathematics relies substantially on existing work in inference limits, performative prediction, control, and partially observable planning. Developed with AI assistance, with toy models and explicit assumptions. For details, see the [research compendium](RESEARCH_COMPENDIUM.md).

**Repository context:** This folder is an independent research archive hosted in the public `agent-house` repository; it is **not** part of the Agent House web app.
