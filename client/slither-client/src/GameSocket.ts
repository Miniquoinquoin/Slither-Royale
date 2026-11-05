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

// export let state: GameState | null = null;

export let previous: GameState | null = null;
export let state: GameState | null = null;
export let receivedAt = 0;

const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => console.log('[ws] connecté');
ws.onclose = () => console.log('[ws] fermé');
ws.onmessage = (event) => {
    // update(state!);
    previous = state;
    state = JSON.parse(event.data);
    receivedAt = performance.now(); 
};

// function update(s: GameState) {
//     console.log(s.t, s.snakes.length);
//     console.log(s);
// }
