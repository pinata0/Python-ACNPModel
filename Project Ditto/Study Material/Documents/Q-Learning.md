---
생성자: Pinata
생성 일시: Invalid date
Resource: http://hanyang.dcollection.net/common/orgView/200000486149
상위 문서:
  - "[[TD]]"
하위 문서:
  - "[[DQN]]"
---
**Q 함수 : 주어진 상태에서 행동 효율의 기댓값 예측 함수**

- 상태와 행동 쌍에 대한 가치를 나타내는 함수

$Q(s,a)=\mathbb{E}[\displaystyle\sum_{t=0}^∞ γ^t R_t ∣ s_0=s,a_0=a]$

- $Q(s,a)$ : 상태 s에서 행동 a를 했을 때 얻을 수 있는 기대 보상
- $\gamma$ : 할인율(0 ≤ $\gamma$ ≤ 1), 미래 보상의 중요도를 결정
- $R_t$ : t 시점에서 얻은 보상
- $\mathbb{E}$ : 기대값을 의미

  

**벨만 방정식**

$Q(s,a) ← Q(s,a) + \alpha [R + \gamma max_{a’} Q(s’, a’) - Q(s, a)]$

- $\alpha$ : 학습률 (Learning Rate)
- ${R}$ : 현재 상태 s에서 행동 a를 했을 때의 보상
- s' : 행동 a를 수행한 후 도달한 새로운 상태
- $max_{a’} ~Q(s,a)$ : 다음 상태 s’에서 가능한 행동들 중 최대 Q 값