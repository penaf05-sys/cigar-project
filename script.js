  async function getStory(name, origin, strength, year, affiliateUrl, imgFile, cardEl) {
        document.querySelectorAll('.cigar-card').forEach(c => c.classList.remove('active'));
        if (cardEl) cardEl.classList.add('active');
        document.getElementById('story').innerHTML = `
            <img src="images/${imgFile}" alt="${name}" class="story-img">
            <p class="loading">Rolling your story...</p>
`        ;
        const response = await fetch('http://localhost:8080/story', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, origin, strength, year})
        });
        const data = await response.json();
       document.getElementById('story').innerHTML = `
            <img src="images/${imgFile}" alt="${name}" class="story-img">
             <div class="story-title-block">
                <div class="story-cigar-name">${name}</div>
                <div class="story-cigar-meta">${origin} &nbsp;·&nbsp; Est. ${year}</div>
            </div>
            <p>${data.story}</p>
            <a class="affiliate-btn" href="${affiliateUrl}" target="_blank">Shop ${name} &rarr;</a>
        `;
    }