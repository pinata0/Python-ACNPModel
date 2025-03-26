---
생성자: Pinata
생성 일시: Invalid date
상위 문서:
  - "[[Reinforce Algorithm]]"
---
```JavaScript
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gym

# 환경 생성
env = gym.make("CartPole-v1")

# 신경망 정의 (정책 네트워크)
class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)  # 확률 값 출력
        )
    
    def forward(self, state):
        return self.fc(state)

# 환경 정보
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
policy = PolicyNetwork(state_dim, action_dim)
optimizer = optim.Adam(policy.parameters(), lr=0.01)

# Reinforce 알고리즘
def reinforce(num_episodes=1000, gamma=0.99):
    for episode in range(num_episodes):
        state = env.reset()
        log_probs = []
        rewards = []

        # 1. 환경과 상호작용하여 데이터 수집
        done = False
        while not done:
            state = torch.tensor(state, dtype=torch.float32)
            action_probs = policy(state)
            action = torch.distributions.Categorical(action_probs).sample()
            
            log_probs.append(torch.log(action_probs[action]))  # 로그 확률 저장
            state, reward, done, _ = env.step(action.item())
            rewards.append(reward)
        
        # 2. 보상 계산 (Return)
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)  # 정규화

        # 3. 정책 업데이트
        loss = -torch.sum(torch.stack(log_probs) * returns)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Episode {episode + 1}: Total Reward = {sum(rewards)}")

reinforce()
```