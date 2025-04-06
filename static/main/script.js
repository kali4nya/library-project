//search
const searchInput = document.getElementById('search');
const resultsEl = document.getElementById('results');
const spinner = document.getElementById('spinner');

let debounceTimeout = null;
let activeIndex = -1;
let currentResults = [];

searchInput.addEventListener('input', function () {
    const query = this.value;

    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(() => {
        if (query.length === 0) {
            resultsEl.innerHTML = '';
            spinner.classList.add('hidden');
            return;
        }

        spinner.classList.remove('hidden');

        fetch(`/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                spinner.classList.add('hidden');
                currentResults = data;
                renderResults(data, query);
                activeIndex = -1;
            });
    }, 300);
});

searchInput.addEventListener('keydown', function (e) {
    if (!currentResults.length) return;

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % currentResults.length;
        updateActive();
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + currentResults.length) % currentResults.length;
        updateActive();
    } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && currentResults[activeIndex]) {
            alert(`Selected: ${currentResults[activeIndex].title}`);
        }
    }
});

function updateActive() {
    const items = resultsEl.querySelectorAll('li');
    items.forEach((item, i) => {
        item.classList.toggle('active', i === activeIndex);
    });
}

function highlightMatch(text, query) {
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
}

function renderResults(results, query) {
    resultsEl.innerHTML = '';

    if (results.length === 0) {
        resultsEl.innerHTML = '<li>No results found</li>';
        return;
    }

    results.forEach((book, index) => {
        const li = document.createElement('li');

        const title = highlightMatch(book.title, query);
        const author = highlightMatch(book.author, query);
        const year = book.year;

        li.innerHTML = `${title} by ${author} (${year})`;

        if (book.available) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/borrow_book';
            form.style.display = 'inline';
            
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'title';
            input.value = book.title;

            const button = document.createElement('button');
            button.type = 'submit';
            button.textContent = 'Borrow';

            form.appendChild(input);
            form.appendChild(button);
            li.appendChild(document.createTextNode(' ')); // space before form
            li.appendChild(form);
        }

        resultsEl.appendChild(li);
    });
}

// ai overview
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[action="/book_overview"]').forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const title = form.querySelector('input[name="title"]').value;

            let overviewContainer = form.parentElement.querySelector('.ai-overview');
            if (!overviewContainer) {
                overviewContainer = document.createElement('div');
                overviewContainer.className = 'ai-overview';
                overviewContainer.textContent = 'Fetching overview...';
                form.parentElement.appendChild(overviewContainer);
            } else {
                overviewContainer.textContent = 'Fetching overview...';
            }

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ title })
                });

                const data = await response.json();
                if (data.overview) {
                    overviewContainer.textContent = data.overview;
                } else {
                    overviewContainer.textContent = 'No overview found.';
                }
            } catch (err) {
                console.error('Failed to fetch overview:', err);
                overviewContainer.textContent = 'Error fetching overview.';
            }
        });
    });
});