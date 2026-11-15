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
