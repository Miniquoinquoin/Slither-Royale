import { Application, Graphics } from 'pixi.js';
import { state } from './GameSocket';

(async () => {
  const app = new Application();
  await app.init({ resizeTo: window, background: 0x0b0f1a, antialias: true });

  document.body.appendChild(app.canvas);

  const color = 0x4ade80;
  const g = new Graphics()
  app.stage.addChild(g);

  app.ticker.add(() => {
    if (!state) return;
    g.clear();
    for (const snake of state.snakes) {
      for (let i = snake.pts.length - 2; i >= 0; i -= 2) {
        g.circle(snake.pts[i], snake.pts[i + 1], snake.r).fill(color);
      }
    } 
  });

  const head = new Graphics().circle(0, 0, 20).fill(0x4ade80);
  head.position.set(app.screen.width / 2, app.screen.height / 2);

  app.stage.addChild(head);

  const mouse = { x: head.x, y: head.y };
  window.addEventListener('pointermove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });

  const SPEED = 200;
  app.ticker.add((ticker) => {
    const dt = ticker.deltaMS / 1000;
    const angle = Math.atan2(mouse.y - head.y, mouse.x - head.x);
    head.x += Math.cos(angle) * SPEED * dt;
    head.y += Math.sin(angle) * SPEED * dt;
  });
})();