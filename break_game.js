const button = document.querySelector('#game-button');
const track = button.querySelector('.game-track');
const action = document.querySelector('#game-action');
const scoreLabel = document.querySelector('#score');
const bestLabel = document.querySelector('#best');
const status = document.querySelector('#game-status');

const cookieName = 'gcse-hit-the-gap-best';
let best = readBest();
let playing = false;
let score = 0;
let position = 0;
let gapStart = 0.4;
let gapWidth = 0.2;
let startedAt = 0;
let frame = 0;
bestLabel.textContent = best;

function readBest() {
  const cookie = document.cookie.split('; ').find(part => part.startsWith(cookieName + '='));
  const value = Number(cookie?.slice(cookieName.length + 1));
  return Number.isSafeInteger(value) && value >= 0 ? value : 0;
}

function saveBest() {
  best = Math.max(best, score, readBest());
  bestLabel.textContent = best;
  document.cookie = cookieName + '=' + best + '; Max-Age=31536000; SameSite=Lax';
}

function startGap() {
  gapWidth = Math.max(0.085, 0.23 - score * 0.012);
  gapStart = 0.16 + Math.random() * (0.68 - gapWidth);
  track.style.setProperty('--gap-left', gapStart * 100 + '%');
  track.style.setProperty('--gap-width', gapWidth * 100 + '%');
  position = 0;
  track.style.setProperty('--position', '0%');
  startedAt = performance.now();
}

function animate(now) {
  const duration = Math.max(480, 1350 - score * 65);
  const phase = Math.max(0, now - startedAt) / duration % 2;
  position = 1 - Math.abs(1 - phase);
  track.style.setProperty('--position', position * 100 + '%');
  frame = requestAnimationFrame(animate);
}

button.addEventListener('click', () => {
  if (!playing) {
    score = 0;
    scoreLabel.textContent = score;
    status.textContent = '';
    action.textContent = 'Tap';
    playing = true;
    startGap();
    frame = requestAnimationFrame(animate);
    return;
  }

  if (position >= gapStart && position <= gapStart + gapWidth) {
    score++;
    scoreLabel.textContent = score;
    saveBest();
    status.textContent = 'Nice! Score ' + score + '.';
    startGap();
    return;
  }

  playing = false;
  cancelAnimationFrame(frame);
  action.textContent = 'Play again';
  status.textContent = 'Missed the gap. You scored ' + score + '.';
});
