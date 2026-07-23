import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from agents.heuristic_agent import HeuristicAgent
from agents.qlearning_agent import QLearningAgent
from core.game_loop import GameLoop

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ManualController:
    name = "manual"

    def __init__(self):
        self.next_action = "straight"

    def decide(self, env) -> str:
        action = self.next_action
        self.next_action = "straight"
        return action

AGENT_REGISTRY = {
    "manual": ManualController,
    "heuristic": HeuristicAgent,
    "qlearning": QLearningAgent,
}
DEFAULT_AGENT = "manual"


@app.websocket("/ws")
async def game_socket(websocket: WebSocket):
    requested_agent = websocket.query_params.get("agent", DEFAULT_AGENT)
    agent_factory = AGENT_REGISTRY.get(requested_agent, AGENT_REGISTRY[DEFAULT_AGENT])

    await websocket.accept()

    async def send_state(state: dict):
        await websocket.send_text(json.dumps(state))

    controller = agent_factory()
    is_manual = isinstance(controller, ManualController)

    game_loop = GameLoop(controller, send_state)
    await game_loop.start()

    try:
        while True:
            raw_message = await websocket.receive_text()
            message = json.loads(raw_message)
            message_type = message.get("type")

            if message_type == "action" and is_manual:
                controller.next_action = message.get("action", "straight")

            elif message_type == "reset":
                game_loop.reset()

    except WebSocketDisconnect:
        await game_loop.stop()