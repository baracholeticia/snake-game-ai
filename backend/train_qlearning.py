from agents.qlearning_agent import QLearningAgent, ACTIONS
from core.environment import SnakeEnvironment

EPISODES = 5000
LOG_EVERY = 100


def train():
    env = SnakeEnvironment()
    agent = QLearningAgent(training=True)

    scores = []

    for episode in range(1, EPISODES + 1):
        env.reset()
        state = env.get_agent_observation()
        done = False

        while not done:
            action_idx = agent._choose_action(state)
            action = ACTIONS[action_idx]

            _, reward, done = env.step(action)
            next_state = env.get_agent_observation()

            agent.update(state, action_idx, reward, next_state, done)
            state = next_state

        agent.decay_epsilon()
        scores.append(env.score)

        if episode % LOG_EVERY == 0:
            avg = sum(scores[-LOG_EVERY:]) / LOG_EVERY
            print(
                f"Episódio {episode:5d} | "
                f"score médio (últimos {LOG_EVERY}): {avg:6.1f} | "
                f"epsilon: {agent.epsilon:.3f} | "
                f"estados aprendidos: {len(agent.q_table)}"
            )

    agent.save()
    print(f"\ntabela Q salva em {agent.table_path}")


if __name__ == "__main__":
    train()