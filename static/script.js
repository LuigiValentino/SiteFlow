let currentPage = 1;
        const itemsPerPage = 9;
        let sitemapLinks = [];

        function renderSitemap(page) {
            const startIndex = (page - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            const sitemapList = document.getElementById("sitemap-list");
            sitemapList.innerHTML = '';

            sitemapLinks.slice(startIndex, endIndex).forEach(link => {
                const li = document.createElement('li');
                li.className = "sitemap-item";
                li.innerHTML = `<a href="${link}" class="text-1xl">${link}</a>`;
                sitemapList.appendChild(li);
            });

            renderPagination(page);
        }

        function renderPagination(page) {
            const pagination = document.getElementById("pagination");
            pagination.innerHTML = '';
            const totalPages = Math.ceil(sitemapLinks.length / itemsPerPage);

            const prevButton = document.createElement('button');
            prevButton.innerText = '⬅';
            prevButton.disabled = page === 1;
            prevButton.onclick = () => {
                if (page > 1) {
                    currentPage--;
                    renderSitemap(currentPage);
                }
            };
            pagination.appendChild(prevButton);

            const nextButton = document.createElement('button');
            nextButton.innerText = '⮕';
            nextButton.disabled = page === totalPages;
            nextButton.onclick = () => {
                if (page < totalPages) {
                    currentPage++;
                    renderSitemap(currentPage);
                }
            };
            pagination.appendChild(nextButton);
        }

        document.getElementById('sitemap-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            let url = document.querySelector('input[name="url"]').value;
            document.getElementById('txt-url').value = url;
            document.getElementById('xml-url').value = url;

            let response = await fetch('/generate_sitemap', {
                method: 'POST',
                body: new FormData(e.target)
            });

            let sitemap = await response.json();
            sitemapLinks = sitemap.nodes;

            renderSitemap(currentPage);
        });