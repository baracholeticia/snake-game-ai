"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AgentType, Direction, GameState } from "@/types/game";

const WS_URL = "ws://localhost:8000/ws";

const DIRECTION_ORDER: Direction[] = ["UP", "RIGHT", "DOWN", "LEFT"];

function buildEmptyState(): GameState {
  return {
    snake: [],
    apple: { x: 0, y: 0 },
    direction: "RIGHT",
    score: 0,
    gameOver: false,
  };
}

function relativeAction(current: Direction, desired: Direction): string | null {
  const currentIdx = DIRECTION_ORDER.indexOf(current);
  const desiredIdx = DIRECTION_ORDER.indexOf(desired);
  const diff = (desiredIdx - currentIdx + 4) % 4;

  if (diff === 0) return "straight";
  if (diff === 1) return "right";
  if (diff === 3) return "left";
  return null;
}

export function useGameWebSocket(agent: AgentType | null) {
  const [state, setState] = useState<GameState>(buildEmptyState);
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);
  const currentDirectionRef = useRef<Direction>("RIGHT");

  useEffect(() => {
    if (!agent) {
      setState(buildEmptyState());
      setConnected(false);
      return;
    }

    const socket = new WebSocket(`${WS_URL}?agent=${agent}`);
    socketRef.current = socket;

    socket.onopen = () => {
      setConnected(true);
      currentDirectionRef.current = "RIGHT";
    };

    socket.onclose = () => setConnected(false);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.error) return;
      currentDirectionRef.current = data.direction as Direction;
      setState(data as GameState);
    };

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [agent]);

  const sendDirection = useCallback((desired: Direction) => {
    const action = relativeAction(currentDirectionRef.current, desired);
    if (!action) return;
    socketRef.current?.send(JSON.stringify({ type: "action", action }));
  }, []);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowUp") sendDirection("UP");
      if (e.key === "ArrowDown") sendDirection("DOWN");
      if (e.key === "ArrowLeft") sendDirection("LEFT");
      if (e.key === "ArrowRight") sendDirection("RIGHT");
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [sendDirection]);

  const reset = useCallback(() => {
    currentDirectionRef.current = "RIGHT";
    socketRef.current?.send(JSON.stringify({ type: "reset" }));
  }, []);

  return { state, connected, reset };
}