  async function getStory(name, origin, strength, year, affiliateUrl, imgFile, flavors, price, cardEl) {
        document.querySelectorAll('.cigar-card').forEach(c => c.classList.remove('active'));
        if (cardEl) cardEl.classList.add('active');

        document.getElementById('story').innerHTML = `
            <img src="images/${imgFile}" alt="${name}" class="story-img">
            <p class="loading">Rolling your story...</p>
`        ;
         document.getElementById('story').scrollIntoView({ behavior: 'smooth', block: 'start' });

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
            ${data.story}
            <div class="profile-card">
                <div class="profile-card-title">Cigar Profile</div>
                <div class="profile-grid">
                    <div class="profile-item">
                        <div class="profile-label">Origin</div>
                        <div class="profile-value">${origin}</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-label">Strength</div>
                        <div class="profile-value">${strength}</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-label">Est.</div>
                        <div class="profile-value">${year}</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-label">Price Range</div>
                        <div class="profile-value">${price}</div>
                    </div>
                </div>
                <div class="profile-flavors">
                    <div class="profile-label">Tasting Notes</div>
                    <div class="flavor-tags">${flavors.split(' · ').map(f => `<span class="flavor-tag">${f}</span>`).join('')}</div>
                </div>
            </div>
            <a class="affiliate-btn" href="${affiliateUrl}" target="_blank">Shop ${name} &rarr;</a>
        `;
    }