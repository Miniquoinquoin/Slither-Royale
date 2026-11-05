import { Application, Graphics } from 'pixi.js';
// import { state } from './GameSocket';
import { previous, state, receivedAt } from './GameSocket';

(async () => {
  const app = new Application();
  await app.init({ resizeTo: window, background: 0x0b0f1a, antialias: true });

  document.body.appendChild(app.canvas);

  const color = 0x4ade80;
  const g = new Graphics()
  const DURATION = 50;
  app.stage.addChild(g);

  app.ticker.add(() => {
    if (!state) return;
    const alpha = Math.min(1, (performance.now() - receivedAt) / DURATION);
    console.log(alpha);
    g.clear();
    // for (const snake of state.snakes) {
    //   for (let i = snake.pts.length - 2; i >= 0; i -= 2) {
    //     g.circle(snake.pts[i], snake.pts[i + 1], snake.r).fill(color);
    //   }
    // } 

    for (const snake of state.snakes) {
      const prev = previous?.snakes.find((s) => s.id === snake.id);
      for (let i = snake.pts.length - 2; i >= 0; i -= 2) {
        let x = snake.pts[i];
        let y = snake.pts[i + 1];

        if (prev && i + 1 < prev.pts.length) {
          x = prev.pts[i] + (x - prev.pts[i]) * alpha;
          y = prev.pts[i + 1] + (y - prev.pts[i + 1]) * alpha;
        }
        g.circle(x, y, snake.r).fill(color);
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