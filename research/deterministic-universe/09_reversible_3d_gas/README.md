# 09. 3차원 가역 우주: 정보 보존과 거시적 시간의 화살

**독립 연구 기록 · 2026-11-16 · 공개 재현 코드 · 학계 최초의 발견 주장 없음**

> **핵심:** 결정론적이고 완전히 되돌릴 수 있는 3차원 입자 우주에서도, 비평형 초기 조건 아래 거시적 혼합 지표는 크게 증가한다. 하지만 매 순간 증가하지는 않는다. 그리고 **정상(불변) 확률분포 아래에서 고정된 관찰자의 최적 미래 예측력은 시간에 따라 변화하지 않는다는 정확한 명제**를 별도로 확인했다.

[수학적 주장/반례 검증대장](CLAIMS.md) · [Python 실험 코드](experiment.py) · [검증 코드](test_experiment.py) · [12개 범위 조건 요약](data/robustness_summary.csv)

## 1. 모델 및 엄밀히 확인한 것

- 공간: 길이 `L`인 **3차원 주기적 정육면체**. 각 격자 칸에 이동 방향 `+x,-x,+y,-y,+z,-z`별 0/1 입자 상태가 있다.
- 한 단계는 **국소 충돌 후 이동** `F=S∘C`.
- 좌표 합이 짝수인 칸은 **고립된 반대방향 x-쌍 ↔ y-쌍**, 홀수인 칸은 **y-쌍 ↔ z-쌍**을 바꾼다. 해당 두 채널 외의 입자가 있으면 변경하지 않는다.
- 따라서 충돌은 자기 역함수 `C²=I`; 이동은 방향별 주기적 순열. 전체 연산 `F`는 정확히 되돌릴 수 있으며 역연산은 `C∘S⁻¹`이다.
- **총 입자 수와 각 축의 총 운동량은 보존**된다. 모든 입자의 속력이 같으므로 운동 에너지도 일정하다.
- 초기 상태는 절반 공간만 무작위(각 채널 독립 베르누이 확률 `p`)로 채운다. **규칙 자체에 난수는 전혀 없다.**
- 같은 초기 상태를 충돌 없는 이동-only `S`와 비교한다.

## 2. 측정값 — 진짜 엔트로피와 구분하기

변 길이 `b`인 공간 블록은 `m=6b³`개의 점유 슬롯을 가진다. 블록별 입자 수가 `n_j`일 때 다음 **거시적 조합론 점수**를 계산한다.

```text
S_B(x) = Σ_j log binomial(m, n_j)
score(x) = S_B(x) / max_{same total particle count} S_B
```

이것은 블록별 밀도만 남겼을 때 가능한 미시배열의 개수를 로그로 나타낸 **Boltzmann형 근사 지표**다. 운동량이나 입자간 상관관계, 실제 기체의 상태밀도를 완전히 세지 않으므로 **실제 열역학 엔트로피와 동일시하지 않는다.**

### 주요 계산 결과

`L=16, b=4, p=0.35`, 64단계, 초기 PRNG 시드 `0..23`, 같은 시드에 대해 두 동역학을 각각 비교.

| 관측 | 충돌 | 충돌 없음 |
|---|---:|---:|
| 초기 평균 점수 | 0.69924 | 0.69924 |
| 8단계 | 0.97976 | 0.97143 |
| 16단계 | 0.95673 | 0.69924 |
| 64단계 | **0.99117** | 0.69924 |
| 처음 대비 최종 평균 변화 | **+0.291933** | 0 |
| 최종 점수 상승 시드 | 24/24 | 0/24 |
| **64단계 정확한 역진 성공** | **24/24** | **24/24** |

시드별 충돌군의 최종 변화 표준편차는 0.003049이며 정규근사 95% 오차반폭은 0.001220이다. 이 숫자는 선택한 초기 준비 분포에서만 통용된다.

**중요한 통제:** L=16에서 순수 이동은 **16단계마다 반드시 원위치**로 돌아오므로 64단계 비교는 충돌군에 유리한 특수한 시점이다. 시간 전체 곡선과 다른 크기의 조건도 함께 확인해야 한다.

- 충돌한 세계에서 24×64=1,536개 연속 전이 중 **610개는 점수가 감소**했다. 예: 시드 0, 9→10단계의 점수 `0.97799051→0.97745521`.
- 12개 조건(`L∈{12,16,20}`, `p∈{0.25,0.35}`, `b∈{2,4}`; 조건당 12개 시드, 48단계)에서는 모두 충돌군의 평균 증가폭이 컸다. 모든 규칙에 보편적으로 적용된다는 뜻은 아니다.
- [본 실험 CSV](data/summary.csv) · [범위 검사 CSV](data/robustness_summary.csv). 원시 궤적은 아래 명령으로 자동 생성된다.

## 3. 두 개의 정확한 수학적 명제 (기존 이론)

**A. 미시적 정보 보존.** 유한 상태 공간에서 `F`가 일대일 대응이면 `H(X_t)=H(X_0)`: 미시상태 확률질량이 단지 재배열되므로 **전체 Shannon 엔트로피는 변하지 않는다**. 블록 점수 `S_B(x)`는 다른 양이므로 변할 수 있다. 모든 궤적이 주기적이므로 한 궤적에 증가가 있다면 같은 완전 주기에 감소도 있어야 한다.

**B. 정상분포의 예측력 불변.** `μ`가 시간진화 `F`에 대해 불변인 확률분포, `A`가 관측함수, `B`가 미래 이진 목표함수, `k`가 고정된 미래 간격이면,

```text
P*(t,k)=max_g Pr_μ[g(A(X_t)) = B(X_(t+k))]
```

는 `t`에 의존하지 않는다. 이유: 정상성으로 `(A(X_t),B(F^k(X_t)))`의 결합분포가 모든 시점에 동일하기 때문이다. **이 정리는 가역성조차 필수조건이 아니라 정상성이 핵심**이다.

[8비트 완전 전수 실험](stationary_predictability.py): 가역 시프트를 이용해 256개 초기상태를 전수조사하면 균등 정상분포에서 시점 0~7 예측 정확도는 `[.5,.5,.5,.5,.5,.5,.5,.5]`. 절반만 무작위 준비한 비정상 분포에서는 `[1,1,1,.5,.5,.5,.5,1]`. 즉, **초기 분포를 어떻게 준비했는지**가 핵심 변수다.

## 4. 직접 재현하기

Python 3.10+ 권장. 필수 패키지 NumPy 하나.

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_experiment.py
python stationary_predictability.py
python experiment.py --L 16 --block 4 --steps 64 --seeds 24 --probability 0.35 --out data
python robustness.py
```

실행 시 `data/trajectories.csv`, `data/summary.csv`, `data/robustness_summary.csv` 등이 생성된다. 테스트는 국소 충돌 규칙의 **모든 64개 이진 상태 × 짝·홀 격자**, 3종 우주 크기의 순방향/역방향 비트 단위 동등성, 운동량·입자수 보존 및 정상분포 예측력 검증을 포함한다.

## 5. 학계와의 관계

이 연구는 **새로운 시간의 법칙을 발견했다는 발표가 아니다.** 격자 기체, 가역 미시역학, Loschmidt 역설, Poincaré 회귀, 정상확률과 통계역학은 오래된 연구 주제다. 충돌 규칙도 간단한 교육·탐색용 규칙일 뿐 실제 3차원 유체에 대한 정밀 모델로 검증되지 않았다.

- Rivet & Boon, *Lattice Gas Hydrodynamics*, Cambridge, ch.3 (HPP and 3D precursors): https://doi.org/10.1017/CBO9780511524707.004
- *Microscopic reversibility and macroscopic irreversibility: A lattice gas model*, Physica A (2016): https://doi.org/10.1016/j.physa.2016.03.037
- Stanford Encyclopedia of Philosophy, *Philosophy of Statistical Mechanics*: https://plato.stanford.edu/entries/statphys-statmech/
- *Boltzmann–Loschmidt Dispute Reloaded: Quantum 150 Years Later*, Entropy (2026): https://doi.org/10.3390/e28060594

### 다음으로 실제 발견을 시도할 문제

**비정상 초기분포에서 미래 예측력이 얼마나 빨리 변할 수 있는지, 거시적 비평형의 크기와 제한된 관찰범위를 이용해 정확한 상계를 찾을 수 있는가?** 우선 여러 비선형 규칙에서 계산한 반례로 가설을 공격한 뒤, 제한된 시스템 클래스에서만이라도 증명을 시도할 계획이다. 아직 이 상계의 존재나 학문적 신규성을 주장하지 않는다.

---

## English summary

This reproducible study implements a finite 3D six-velocity reversible lattice gas, with an involutive local collision map and periodic streaming. The full microstate is recovered exactly after reversing 64 updates for all 48 tested trajectories. A coarse block-multiplicity score usually grows from a half-filled nonequilibrium preparation, yet **610 of 1,536 individual forward updates decreased it**; there is no pathwise H-theorem. Independently, for any stationary ensemble and fixed observation/target functions, Bayes-optimal finite-horizon prediction accuracy is time-independent, which we verify by exact enumeration of an 8-bit reversible shift. **These results illustrate established mathematical principles, not an original physical discovery or evidence for a deterministic universe.**
