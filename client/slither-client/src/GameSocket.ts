const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => console.log('[ws] connecté');
ws.onclose = () => console.log('[ws] fermé');
ws.onmessage = (event) => {
  const gamestate = JSON.parse(event.data);
  console.log(gamestate);
};