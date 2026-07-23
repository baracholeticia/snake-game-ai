export type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT";

export type AgentType = "heuristic" | "qlearning" | "genetic";

export interface Position {
  x: number;
  y: number;
}

export interface GameState {
  snake: Position[];
  apple: Position;
  direction: Direction;
  score: number;
  gameOver: boolean;
}

export const GRID_SIZE = 15;