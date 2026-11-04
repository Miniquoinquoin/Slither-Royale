type Snake = {
  id: number;
  name: string;
  skin: number;
  r: number;
  score: number;
  boost: boolean;
  pts: number[];
};

type GameState = {
  t: number;
  you: number;
  snakes: Snake[];
  food: unknown[];
};

export let state: GameState | null = null;

const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => console.log('[ws] connecté');
ws.onclose = () => console.log('[ws] fermé');
ws.onmessage = (event) => {
    state = JSON.parse(event.data);
    // update(state!);
};

// function update(s: GameState) {
//     console.log(s.t, s.snakes.length);
//     console.log(s);
// }
