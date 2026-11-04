# 등간격 Query의 인과적 Softmax Attention을 위한 준선형 대수 알고리즘과 저랭크 경로 보정

연구 노트 · 2026-11-04 · 개념 증명 및 합성 데이터 검증

> **상태**: 재현 가능한 연구 가설 및 구조적 조건부 정리. 출판·신규성 검증·실제 LLM 실험을 마친 연구 성과는 아니다. 여기서 '정확'은 실수의 대수적 연산 모델에서의 동일성을 뜻하며, FP16/FP32의 비트 단위 일치를 뜻하지 않는다.

## 1. 명제

임의의 Key `k_j ∈ R^d` 및 Value `v_j ∈ R^h`가 있고, 모든 Query가 `q_t=a+t b` (`t=0,...,N-1`)로 주어지면, 다음의 인과적 Softmax Attention을

\[
Y_t=\frac{\sum_{j=0}^{t}\exp(q_t^\top k_j/\sqrt d)\,v_j}{\sum_{j=0}^{t}\exp(q_t^\top k_j/\sqrt d)}
\]

`O(Nd+(h+1)N log^3 N)` 산술 연산으로 계산할 수 있다. 인과 마스크가 없다면 `O(Nd+(h+1)N log^2 N)`으로 계산할 수 있다. 빠른 다항식 곱셈 알고리즘 `M(N)=O(N log N)` 및 실수 연산의 단위 비용을 전제한다. 실제 비트 복잡도와 수치 안정성은 별도 문제다.

## 2. 유리함수로의 환원

각 Key에 대해

\[
w_j=\exp(a^\top k_j/\sqrt d),\qquad
z_j=\exp(b^\top k_j/\sqrt d)
\]

를 정의한다. 그러면 `exp(q_t · k_j / √d)=w_j z_j^t`다.

값이 스칼라인 경우 다음을 정의하자.

\[
F(x)=\sum_{j=0}^{N-1}\frac{w_j}{1-z_jx}
=\frac{P(x)}{D(x)},\qquad
D(x)=\prod_{j=0}^{N-1}(1-z_j x).
\]

형식적 멱급수의 기본 등식 `1/(1-zx)=sum_{t>=0} z^t x^t`에서 즉시

\[
[x^t]F(x)=\sum_{j=0}^{N-1} w_jz_j^t
\]

를 얻는다. 가중치를 `w_j v_{j,c}`로 바꾸면 Value의 `c`번째 좌표에 대한 분자도 동일하게 얻는다. 따라서 모든 Query의 정규화 분모와 분자를 다항식의 계수로 한꺼번에 구할 수 있다.

`P,D`는 양분 트리로 구성한다. 좌우 부분집합에서 얻은 `(P_L,D_L)`, `(P_R,D_R)`을

\[
D=D_LD_R,\qquad P=P_LD_R+P_RD_L
\]

로 합친다. 다항식 곱셈에 FFT/NTT를 사용하면 트리를 `O(N log^2 N)`에 구성한다. 이후 Newton 급수 역산을 이용해 `P/D mod x^N`의 N개 계수를 `O(N log N)`에 추출한다. 필요한 Value 좌표마다 가중치가 다른 분자를 구성한다.

## 3. 인과 마스크를 보존하는 분할정복

인과적 분모는 `Z_t=∑_{j≤t}w_jz_j^t`다. 인덱스 구간 `[L,R)`을 `[L,M)`, `[M,R)`로 양분한다.

* 좌우 내부의 인과적인 쌍은 재귀적으로 처리한다.
* 왼쪽 Key `j∈[L,M)`와 오른쪽 Query `t∈[M,R)`는 모두 허용된 인과적 쌍이다.
* 이 교차 직사각형은 다음 계수 추출과 정확히 같다.

\[
\sum_{j=L}^{M-1}w_jz_j^t
=[x^{t-M}]\sum_{j=L}^{M-1}\frac{w_jz_j^M}{1-z_jx}.
\]

마찬가지로 `w_j v_j`를 넣어 분자를 계산한다. `j=t` 대각선 항은 개별적으로 추가한다. 이 분해에서는 각 허용 쌍 `j≤t`가 정확히 한 번 포함되고, 금지된 `j>t`는 한 번도 포함되지 않는다.

길이 `N` 구간에 대한 합성 비용은

\[
T(N)=2T(N/2)+O((h+1)N\log^2N)
=O((h+1)N\log^3N).
\]

따라서 인과 마스크를 버리지 않고 준선형 복잡도를 얻는다. 이것은 모든 임의 Query에 대한 결과가 아니라 **등간격 affine Query**라는 강한 가정 아래의 구조적 정리다.

## 4. 저랭크 Query 이탈에 대한 보정

실제 Query가 `q_t=(a+t b)+δ_t`라 하자. `δ_t`가 `r`차원 부분공간에 머무른다면

\[
\delta_t=\sum_{\ell=1}^r \alpha_{t\ell}c_\ell.
\]

기준 Query `q_t^0=a+t b`에서 softmax 분포 `p_{tj}^0`, 평균 `μ_v(t)=E[v]`, `μ_k(t)=E[k]`를 정의한다. Softmax 출력의 Query에 대한 미분은

\[
\nabla_qY(q)=\frac{1}{\sqrt d}\operatorname{Cov}_{p(q)}(v,k)
\]

이다. 따라서 방향 `c_ell`에 대한 미분은

\[
g_{t\ell}=\operatorname{Cov}_{p_t^0}\left(v,\frac{c_\ell^\top k}{\sqrt d}\right).
\]

보정 출력은

\[
\widehat Y_t=Y_t(q_t^0)+\sum_{\ell=1}^r\alpha_{t\ell}g_{t\ell}.
\]

여기서 필요한 기댓값은 `v`, `c_ell·k/√d`, `v(c_ell·k/√d)`의 가중 합이고, 모두 2~3절에서 같은 유리함수 계수 알고리즘으로 계산 가능하다. 따라서 `r`과 `h`가 작다면 원래의 준선형 복잡도를 유지한다.

## 5. 보정 오차에 대한 결정적 정리

현재 Query에서 접근 가능한 Key와 Value의 직경을 각각

\[
D_K=\max_{i,j}\|k_i-k_j\|_2,\qquad
D_V=\max_{i,j}\|v_i-v_j\|_2
\]

로 두자. 그러면 위 일차 보정의 오차는

\[
\boxed{\|Y_t(q_t)-\widehat Y_t\|_2\le \frac{D_V D_K^2}{8d}\|\delta_t\|_2^2}
\]

를 만족한다. 이를 위한 증명은 다음과 같다.

1. `s_j=δ_t·k_j/√d`, `p_j(x) ∝ exp(q^0·k_j/√d+x s_j)`를 정의하고 `f(x)=∑p_j(x)v_j`로 둔다.
2. `f'(x)=Cov_{p(x)}(v,s)`이고 `f''(x)=E_{p(x)}[(v-f(x))(s-E_{p(x)}s)^2]`다.
3. `f(x)`는 `v_j`의 볼록 결합이므로 `\|v_j-f(x)\|≤D_V`다. Popoviciu의 분산 상계에 따라 `Var(s)≤(max s-min s)^2/4≤D_K^2\|δ_t\|^2/(4d)`다.
4. 따라서 `\|f''(x)\|≤D_V D_K^2\|δ_t\|^2/(4d)`이고 Taylor 나머지항은 그 절반 이하다.

전체 Key/Value를 한 번 훑으며 임의의 기준점 `c_K,c_V`에 대한 반경 `R_K=max_j ||k_j-c_K||`, `R_V=max_j||v_j-c_V||`을 구하면, `D_K≤2R_K`, `D_V≤2R_V`이므로 더 손쉽게 계산 가능한 상계

\[
\boxed{\|Y_t(q_t)-\widehat Y_t\|_2\le \frac{R_VR_K^2}{d}\|\delta_t\|_2^2}
\]

를 얻는다. 이 수식은 인과 마스크에도 그대로 적용된다. 최적 상계는 아니며 큰 반경을 갖는 모델에서는 느슨할 수 있다.

## 6. 실행 검증

실행 코드: `structured_attention_research.py`, Python 3 + NumPy + mpmath. 난수 시드 고정.

**정확한 유한체 검증:** 큰 소수 `p=998244353` 위에서 다항식 알고리즘을 NTT로 구현했다. 이는 지수함수 자체를 유한체에서 테스트한 것이 아니라, 지수함수에서 환원된 **대수 항등식**을 반올림 없이 검증한 것이다.

| N | 인과적 빠른 알고리즘 | 직접 계산 | 모든 항 일치 |
|---:|---:|---:|:---:|
| 512 | 0.094초 | 0.039초 | 예 |
| 1,024 | 0.260초 | 0.156초 | 예 |
| 2,048 | 0.743초 | 0.701초 | 예 |
| 4,096 | 2.006초 | 2.838초 | 예 |

시점 및 머신 상태에 따른 변동이 있으므로 속도는 정밀 벤치마크가 아닌 예시다. 실제 GPU의 부동소수점 softmax 속도 향상을 의미하지 않는다.

**실수 지수함수 검증:** `n=24,d=4,h=3`, 90자리 고정밀 연산에서 실제 `exp`를 이용한 직접 Softmax와 유리함수 계수 방법의 최대 절댓값 차이가 약 `1.79×10^-76`이었다.

**인과적 비선형 Query 검증 (합성 입력):** `n=120,d=12,h=4`, affine Query에 한 방향의 사인파 형태 잔차를 추가했다. 원래 affine 출력으로 근사하면 최대 출력 오차 `0.005790745`; 일차 모멘트 보정 후 `0.000112888`이었다(약 51.30배 감소). 모든 시점에서 위의 결정적 이차 오차 상계를 만족했다. 보정 예제에서는 도출한 모멘트 값을 직접 합으로 산출하여 **보정 수식 자체만**을 검증했으며, 고정밀·안정적인 실제 fast kernel에 통합한 결과는 아니다.

## 7. 결정적인 한계와 반증 실험

1. **구조 조건**: Query가 진짜로 affine 또는 affine + 저랭크 잔차일 필요가 있다. 실제 사전학습 언어모델의 Query가 이 조건을 만족한다는 증거는 아직 없다. 이 조건을 강제로 학습시키면 모델의 표현력이 감소할 수 있다.
2. **수치 안정성**: Vandermonde 구조는 알려진 수치적 불안정성을 갖는다. 특히 `z_j≈1`이면 `D(x)=∏(1-z_jx)`의 계수 상쇄가 심해져 일반 부동소수점 계수 전개가 깨질 수 있다. 유한체 검증은 이 문제를 해결하지 않는다.
3. **계산량 상수**: 출력 차원과 잔차 방향 수에 따라 모멘트 수가 증가한다. 실제 GPU에서 안정적인 고성능 커널이 필요하다.
4. **신규성**: 빠른 Vandermonde 곱셈 및 분할정복은 이미 널리 알려진 기술이다. 구조적 Attention과 결정적 잔차 보정의 결합에 대한 신규성은 별도의 체계적 문헌조사가 필요하다.
5. **검증 계획**: 여러 실제 LLM의 개별 Head Query를 수집하여 길이별 최적 affine/저차원 경로 적합 잔차와 네트워크 출력 오차를 계량하고, FP32/BF16에서 안정적으로 작동하는 기법을 찾으며, FlashAttention의 실제 wall-clock time과 비교해야 한다. 본문 속 이론적 우위만으로 기존 구현의 속도 향상을 단언해서는 안 된다.

## 8. 관련 선행 연구

- I. Gohberg, V. Olshevsky, *Fast Algorithms with Preprocessing for Matrix-Vector Multiplication Problems* (1994). Vandermonde 및 전치행렬의 준선형 곱셈. https://www.sciencedirect.com/science/article/pii/S0885064X84710211
- M. Aliakbarpour et al., *Support Basis: Fast Attention Beyond Bounded Entries* (AISTATS 2026). https://proceedings.mlr.press/v300/aliakbarpour26a.html
- C. Hooper et al., *Multipole Attention for Efficient Long Context Reasoning* (NeurIPS 2025). https://proceedings.nips.cc/paper_files/paper/2025/hash/359f442022ef31bcd9e41959576107ef-Abstract-Conference.html
- D. Le et al., *Don't Read Everything: A Curvature-Conditioned Query for Linear Attention* (EMNLP 2026). https://aclanthology.org/2026.emnlp-main.1153/
- S. Mausberg, *An I/O Lower Bound for Exact Attention* (2026 preprint). https://sammausberg.com/research/papers/exact-attention-io-lower-bound
- M. Ataei, *Conic Certification of Transformer Attention* (2026 preprint). https://arxiv.org/abs/2611.00585

## 9. 다음 목표

가장 값진 결과는 현재 정리 자체가 아니라, **실제 모델에서 Query 구조를 찾아내는 방법**, 그리고 **다항식 곱셈의 빠른 이점을 유지하며 부동소수점 수치 안정성을 증명하는 새로운 알고리즘**이다. 둘 중 하나만 해결해도 후속 연구 가치가 높지만, 둘 다 해결되어야 범용 Transformer 계산 비용에 실제 영향을 줄 수 있다.