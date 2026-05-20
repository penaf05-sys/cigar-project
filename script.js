async function getStory(name, origin, strength, year, affiliateUrl, imgFile, flavors, price, cardEl) {
    document.querySelectorAll('.cigar-card').forEach(c => c.classList.remove('active'));
    if (cardEl) cardEl.classList.add('active');

    document.getElementById('story').innerHTML = `
        <img src="images/${imgFile}" alt="${name}" class="story-img">
        <p class="loading">Rolling your story...</p>
    `;
    document.getElementById('story').scrollIntoView({ behavior: 'smooth', block: 'start' });

    const response = await fetch('/story', {
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
        <button class="voiceover-btn" onclick="playVoiceover(this)" data-text="${data.plain_text.replace(/"/g, '&quot;')}">
            🎙️ Hear the Story
        </button>
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


let currentAudio = null;

async function playVoiceover(btn) {
    // If audio is playing, stop it
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
        btn.textContent = '🎙️ Hear the Story';
        btn.disabled = false;
        return;
    }

    const text = btn.getAttribute('data-text');
    btn.textContent = '⏳ Loading voice...';
    btn.disabled = true;

    try {
        const response = await fetch('/voiceover', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text.substring(0, 2500)})
        });

        const data = await response.json();

        if (data.audio) {
            currentAudio = new Audio('data:audio/mpeg;base64,' + data.audio);
            currentAudio.play();
            btn.textContent = '⏹️ Stop';
            btn.disabled = false;
            currentAudio.onended = () => {
                currentAudio = null;
                btn.textContent = '🎙️ Hear the Story';
                btn.disabled = false;
            };
        } else {
            btn.textContent = '❌ Voice failed';
            btn.disabled = false;
        }
    } catch (err) {
        btn.textContent = '❌ Voice failed';
        btn.disabled = false;
    }
}