---
생성자: Pinata
생성 일시: Invalid date
Resource: https://qcoding.tistory.com/77
상위 문서:
  - "[[Advantage Actor-Critict]]"
---
**A2C (Advantage Actor-Critic)**

  

**과정**

1. 환경에서 샘플 수집
    1. 환경에서 현재 정책 $\pi_\theta(s|a)$로 여러 개의 Agent가 동시에 데이터 수집
    2. $(s_t, a_t, r_t, s_{t+1})$로 샘플링하여 저장
2. Advantage 계산
    1. 가치 함수 $V(s)$를 $Critic(s_t)$로 예측
    2. TD 타깃 계산 $\hat{Q}(s_t, a_t) = r_t + \gamma V(s_{t+1})$
    3. Advantage 계산 $A(s_t, a_t) = \hat{Q}(s_t,a_t)-V(s_t)$
3. Policy Gradient $\nabla J(\theta) = \mathbb{E}[\nabla\log\pi_\theta(s|a)A(s|a)]$ 계산 후
    1. 양수면 해당 행동 확률 증가
    2. 음수면 해당 행동 확률 감소
4. 가치 함수 업데이트 (MSE)
    
    $L_v = (r_t + \gamma V(s_{t+1})-V(s_t))^2$