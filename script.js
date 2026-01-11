async function loadProjects() {
    try {
        const response = await fetch('projects.json');
        const projects = await response.json();
        renderProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

function renderProjects(projects) {
    const grid = document.getElementById('projects-grid');

    projects.forEach(project => {
        const card = document.createElement('article');
        card.className = 'project-card';

        const imageHTML = project.image
            ? `<img src="${project.image}" alt="${project.title}" class="project-image">`
            : `<div class="project-image-placeholder">No image</div>`;

        card.innerHTML = `
            ${imageHTML}
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-date">${formatDate(project.date)}</p>
                <p class="project-description">${project.description}</p>
            </div>
        `;

        grid.appendChild(card);
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long'
    });
}

document.addEventListener('DOMContentLoaded', loadProjects);
