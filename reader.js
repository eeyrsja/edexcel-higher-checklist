const search = document.querySelector('#text-search');
const results = document.querySelector('#text-results');
const status = document.querySelector('#text-search-status');
const sections = [...document.querySelectorAll('.reading-section')];
const fold = value => value.toLowerCase().replace(/[‘’]/g, "'");
const passages = sections.map(section => {
  const blocks = [...section.querySelectorAll('.reading-copy p, .reading-copy pre')];
  return {
    id: section.id,
    title: section.querySelector('h2').textContent,
    blocks: blocks.map((block, index) => {
      block.id = section.id + '-passage-' + (index + 1);
      const text = block.textContent.replace(/\s+/g, ' ').trim();
      return {id: block.id, text, folded: fold(text)};
    }),
  };
});

search.addEventListener('input', () => {
  const query = fold(search.value.trim().replace(/\s+/g, ' '));
  results.replaceChildren();
  if (!query) {
    status.textContent = '';
    return;
  }

  let count = 0;
  for (const passage of passages) {
    for (const block of passage.blocks) {
      const index = block.folded.indexOf(query);
      if (index < 0) continue;
      count++;
      if (count > 30) continue;
      const entry = document.createElement('li');
      const link = document.createElement('a');
      const excerpt = document.createElement('span');
      const start = Math.max(0, index - 45);
      const end = Math.min(block.text.length, index + query.length + 65);
      link.href = '#' + block.id;
      link.textContent = passage.title;
      excerpt.textContent = (start ? '…' : '') + block.text.slice(start, end)
        + (end < block.text.length ? '…' : '');
      entry.append(link, excerpt);
      results.append(entry);
    }
  }
  status.textContent = count > 30 ? 'Showing the first 30 matching passages out of ' + count + '.'
    : count === 0 ? 'No matching passages.' : count + (count === 1 ? ' matching passage.' : ' matching passages.');
});

const jump = document.querySelector('#text-jump');
jump.addEventListener('change', () => {
  if (jump.value) location.hash = jump.value;
});

const cookieName = 'gcse-reader-' + location.pathname.split('/').pop().replace('-text.html', '');
const annotationStatus = document.querySelector('#annotation-status');
const bookmarkList = document.querySelector('#saved-bookmarks');
const textBlocks = new Map(
  [...document.querySelectorAll('.reading-copy p, .reading-copy pre')]
    .map(block => [block.id, {element: block, text: block.textContent}]),
);
const examYear = new URLSearchParams(location.search).get('exam');
const examMap = JSON.parse(document.querySelector('#exam-ranges').textContent);
const examRanges = Object.hasOwn(examMap, examYear) ? examMap[examYear] : [];
document.querySelector('#exam-highlight-label').hidden = !examRanges.length;

function readAnnotations() {
  const value = document.cookie.split('; ').find(cookie => cookie.startsWith(cookieName + '='));
  try {
    if (value) {
      const saved = JSON.parse(decodeURIComponent(value.slice(cookieName.length + 1)));
      if (Array.isArray(saved.bookmarks) && Array.isArray(saved.highlights)) return saved;
    }
  } catch {
    // An older or malformed cookie can be replaced on the next save.
  }
  return {bookmarks: [], highlights: []};
}

function saveAnnotations(saved, message) {
  const value = cookieName + '=' + encodeURIComponent(JSON.stringify(saved));
  if (value.length > 3800) {
    annotationStatus.textContent = 'Your notes are full. Remove a highlight or bookmark to make room.';
    return;
  }
  const directory = location.pathname.slice(0, location.pathname.lastIndexOf('/') + 1);
  document.cookie = value + '; Max-Age=31536000; Path=' + directory + '; SameSite=Lax';
  if (!document.cookie.split('; ').includes(value)) {
    annotationStatus.textContent = 'Your browser did not save these notes. Check its cookie settings.';
    return;
  }
  redrawAnnotations(saved);
  annotationStatus.textContent = message;
}

function rangesByBlock(ranges) {
  const grouped = new Map();
  for (const [id, start, end] of ranges) {
    const block = textBlocks.get(id);
    if (!block || !Number.isInteger(start) || !Number.isInteger(end)
        || start < 0 || start >= end || end > block.text.length) continue;
    if (!grouped.has(id)) grouped.set(id, []);
    grouped.get(id).push([start, end]);
  }
  return grouped;
}

const examByBlock = rangesByBlock(examRanges);
let painted = new Set();

function redrawAnnotations(saved) {
  const personal = rangesByBlock(saved.highlights);
  const marked = new Set([...examByBlock.keys(), ...personal.keys()]);
  for (const id of new Set([...painted, ...marked])) {
    const {element, text} = textBlocks.get(id);
    const exam = examByBlock.get(id) || [];
    const user = personal.get(id) || [];
    const points = [0, text.length, ...exam.flat(), ...user.flat()];
    const bounds = [...new Set(points)].sort((a, b) => a - b);
    const nodes = [];
    for (let i = 0; i < bounds.length - 1; i++) {
      const from = bounds[i], to = bounds[i + 1];
      const inExam = exam.some(([start, end]) => from >= start && to <= end);
      const inUser = user.some(([start, end]) => from >= start && to <= end);
      const value = text.slice(from, to);
      if (inExam || inUser) {
        const mark = document.createElement('mark');
        mark.classList.toggle('exam-match', inExam);
        mark.classList.toggle('personal-highlight', inUser);
        mark.textContent = value;
        nodes.push(mark);
      } else {
        nodes.push(document.createTextNode(value));
      }
    }
    element.replaceChildren(...nodes);
  }
  painted = marked;

  bookmarkList.replaceChildren();
  for (const section of sections) {
    const title = section.querySelector('h2').textContent;
    const button = section.querySelector('.bookmark-toggle');
    const active = saved.bookmarks.includes(section.id);
    button.setAttribute('aria-pressed', active);
    button.textContent = (active ? 'Remove bookmark for ' : 'Bookmark ') + title;
    if (!active) continue;
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = '#' + section.id;
    link.textContent = title;
    item.append(link);
    bookmarkList.append(item);
  }
  if (!bookmarkList.children.length) {
    const item = document.createElement('li');
    item.textContent = 'No bookmarks yet';
    bookmarkList.append(item);
  }
}

for (const section of sections) {
  section.querySelector('.bookmark-toggle').addEventListener('click', () => {
    const saved = readAnnotations();
    const active = saved.bookmarks.includes(section.id);
    saved.bookmarks = active ? saved.bookmarks.filter(id => id !== section.id) : [...saved.bookmarks, section.id];
    saveAnnotations(saved, active ? 'Bookmark removed.' : 'Bookmark saved.');
  });
}

function getSelectedRanges() {
  const selection = window.getSelection();
  if (!selection.rangeCount || selection.isCollapsed) return [];
  const range = selection.getRangeAt(0);
  const selected = [];
  for (const [id, block] of textBlocks) {
    const {element, text} = block;
    if (!range.intersectsNode(element)) continue;
    const prefix = document.createRange();
    prefix.setStart(element, 0);
    const offset = (container, position, fallback) => {
      if (!element.contains(container)) return fallback;
      prefix.setEnd(container, position);
      return prefix.toString().length;
    };
    const start = offset(range.startContainer, range.startOffset, 0);
    const end = offset(range.endContainer, range.endOffset, text.length);
    if (start < end && text.slice(start, end).trim()) selected.push([id, start, end]);
  }
  return selected;
}

let lastSelection = [];
document.addEventListener('selectionchange', () => {
  const selected = getSelectedRanges();
  if (selected.length) lastSelection = selected;
  else if (!document.activeElement?.closest('.reader-tools')) lastSelection = [];
});
for (const [button, remove] of [['save-highlight', false], ['clear-highlight', true]]) {
  document.getElementById(button).addEventListener('pointerdown', event => {
    if (getSelectedRanges().length) event.preventDefault();
  });
  document.getElementById(button).addEventListener('click', () => {
    const selected = getSelectedRanges();
    const ranges = selected.length ? selected : lastSelection;
    if (!ranges.length) {
      annotationStatus.textContent = 'Select words in the text first.';
      return;
    }
    const saved = readAnnotations();
    if (remove) {
      saved.highlights = saved.highlights.flatMap(([id, start, end]) => {
        const overlap = ranges.find(([other, a, b]) => other === id && a < end && b > start);
        if (!overlap) return [[id, start, end]];
        const [, a, b] = overlap;
        return [...(start < a ? [[id, start, a]] : []), ...(b < end ? [[id, b, end]] : [])];
      });
    } else {
      saved.highlights = [...saved.highlights, ...ranges.filter(range => !saved.highlights.some(
        ([id, start, end]) => id === range[0] && start === range[1] && end === range[2],
      ))];
    }
    saveAnnotations(saved, remove ? 'Selected highlight removed.' : 'Highlight saved.');
    window.getSelection().removeAllRanges();
    lastSelection = [];
  });
}

redrawAnnotations(readAnnotations());
window.addEventListener('pageshow', () => redrawAnnotations(readAnnotations()));
if (examRanges.length) {
  requestAnimationFrame(() => {
    document.querySelector('.exam-match')?.scrollIntoView({block: 'center', behavior: 'instant'});
  });
}
