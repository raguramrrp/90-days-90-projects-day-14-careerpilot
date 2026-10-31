/**
 * CareerPilot Interactive Kanban Pipeline Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.kanban-card');
  const columns = document.querySelectorAll('.kanban-items');

  let draggedCard = null;

  cards.forEach(card => {
    card.setAttribute('draggable', 'true');

    card.addEventListener('dragstart', (e) => {
      draggedCard = card;
      card.style.opacity = '0.5';
      e.dataTransfer.setData('text/plain', card.dataset.appId);
      e.dataTransfer.effectAllowed = 'move';
    });

    card.addEventListener('dragend', () => {
      if (draggedCard) {
        draggedCard.style.opacity = '1';
        draggedCard = null;
      }
    });

    // Quick status select fallback
    const statusSelect = card.querySelector('.quick-status-select');
    if (statusSelect) {
      statusSelect.addEventListener('change', async (e) => {
        const newStatus = e.target.value;
        const appId = card.dataset.appId;
        await updateApplicationStatus(appId, newStatus, card);
      });
    }
  });

  columns.forEach(column => {
    column.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      column.style.backgroundColor = 'var(--accent-bg)';
    });

    column.addEventListener('dragleave', () => {
      column.style.backgroundColor = '';
    });

    column.addEventListener('drop', async (e) => {
      e.preventDefault();
      column.style.backgroundColor = '';
      if (!draggedCard) return;

      const newStatus = column.dataset.stageKey;
      const appId = draggedCard.dataset.appId;
      const prevStatus = draggedCard.dataset.currentStatus;

      if (newStatus !== prevStatus) {
        column.appendChild(draggedCard);
        draggedCard.dataset.currentStatus = newStatus;
        const select = draggedCard.querySelector('.quick-status-select');
        if (select) select.value = newStatus;
        
        await updateApplicationStatus(appId, newStatus, draggedCard);
      }
    });
  });

  async function updateApplicationStatus(appId, newStatus, cardEl) {
    try {
      const response = await fetch(`/applications/${appId}/update-status/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          status: newStatus,
          notes: `Moved to ${newStatus} via Kanban board.`
        })
      });
      const data = await response.json();
      if (!data.success) {
        alert('Failed to update stage: ' + (data.error || 'Server error'));
        window.location.reload();
      } else {
        // Find target column and ensure card is placed there
        const targetCol = document.querySelector(`.kanban-items[data-stage-key="${newStatus}"]`);
        if (targetCol && cardEl.parentElement !== targetCol) {
          targetCol.appendChild(cardEl);
          cardEl.dataset.currentStatus = newStatus;
        }
        updateColumnCounts();
      }
    } catch (err) {
      console.error('Status update failed', err);
      alert('Network or server error updating application status.');
    }
  }

  function updateColumnCounts() {
    document.querySelectorAll('.kanban-column').forEach(col => {
      const stageKey = col.querySelector('.kanban-items')?.dataset.stageKey;
      const count = col.querySelectorAll('.kanban-card').length;
      const countEl = col.querySelector('.kanban-count');
      if (countEl) countEl.innerText = count;
    });
  }
});
