/**
 * CareerPilot Calendar Engine
 * Supports Month, Week, and Day views with real database career events.
 */

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('calendar-container');
  if (!container) return;

  let currentDate = new Date();
  let currentView = 'month'; // 'month', 'week', 'day'
  let allEvents = [];

  const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const titleEl = document.getElementById('calendar-title');
  const prevBtn = document.getElementById('cal-prev-btn');
  const nextBtn = document.getElementById('cal-next-btn');
  const todayBtn = document.getElementById('cal-today-btn');
  const viewBtns = document.querySelectorAll('.cal-view-btn');

  // Load events from backend
  async function loadEvents() {
    try {
      const res = await fetch('/api/calendar-events/');
      allEvents = await res.json();
      render();
    } catch (e) {
      console.error('Failed to load calendar events', e);
    }
  }

  function render() {
    if (currentView === 'month') {
      renderMonthView();
    } else if (currentView === 'week') {
      renderWeekView();
    } else {
      renderDayView();
    }
  }

  function renderMonthView() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    if (titleEl) {
      titleEl.innerText = `${monthNames[month]} ${year}`;
    }

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();

    let html = `
      <div style="display: grid; grid-template-columns: repeat(7, 1fr); background: var(--bg-muted); border-bottom: 1px solid var(--border); font-weight: 600; font-size: 11.5px; text-align: center; padding: 6px 0;">
        ${dayNames.map(d => `<div>${d}</div>`).join('')}
      </div>
      <div class="calendar-grid">
    `;

    const todayStr = new Date().toISOString().split('T')[0];

    // Previous month filler days
    for (let i = firstDay - 1; i >= 0; i--) {
      const dayNum = daysInPrevMonth - i;
      html += `<div class="calendar-cell other-month"><div class="calendar-date-number">${dayNum}</div></div>`;
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const isToday = dateStr === todayStr;
      const dayEvents = allEvents.filter(ev => ev.date === dateStr);

      html += `
        <div class="calendar-cell ${isToday ? 'today' : ''}" data-date="${dateStr}">
          <div class="calendar-date-number" style="${isToday ? 'color: var(--primary-accent); font-weight: 700;' : ''}">${day}</div>
          <div style="display: flex; flex-direction: column; gap: 2px; overflow-y: auto; max-height: 80px;">
            ${dayEvents.map(ev => `
              <a href="${ev.url}" class="calendar-event-pill" style="background-color: ${ev.color};" title="${ev.title}">
                ${escapeHtml(ev.title)}
              </a>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Next month filler
    const totalCells = firstDay + daysInMonth;
    const remaining = (7 - (totalCells % 7)) % 7;
    for (let i = 1; i <= remaining; i++) {
      html += `<div class="calendar-cell other-month"><div class="calendar-date-number">${i}</div></div>`;
    }

    html += `</div>`;
    container.innerHTML = html;
  }

  function renderWeekView() {
    const startOfWeek = new Date(currentDate);
    startOfWeek.setDate(currentDate.getDate() - currentDate.getDay());

    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);

    if (titleEl) {
      titleEl.innerText = `${startOfWeek.toLocaleDateString(undefined, {month:'short', day:'numeric'})} – ${endOfWeek.toLocaleDateString(undefined, {month:'short', day:'numeric', year:'numeric'})}`;
    }

    let html = `
      <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px;">
    `;

    for (let i = 0; i < 7; i++) {
      const dayDate = new Date(startOfWeek);
      dayDate.setDate(startOfWeek.getDate() + i);
      const dateStr = dayDate.toISOString().split('T')[0];
      const isToday = dateStr === new Date().toISOString().split('T')[0];
      const dayEvents = allEvents.filter(ev => ev.date === dateStr);

      html += `
        <div class="card" style="min-height: 380px; display: flex; flex-direction: column; ${isToday ? 'border-color: var(--primary-accent);' : ''}">
          <div style="border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-bottom: 8px;">
            <div style="font-size: 11px; text-transform: uppercase; color: var(--text-secondary);">${dayNames[i]}</div>
            <div style="font-size: 18px; font-weight: 700; color: ${isToday ? 'var(--primary-accent)' : 'var(--text-primary)'};">${dayDate.getDate()}</div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; flex: 1; overflow-y: auto;">
            ${dayEvents.map(ev => `
              <div style="padding: 6px; border-radius: 4px; border-left: 3px solid ${ev.color}; background: var(--bg-muted); font-size: 11.5px;">
                <div style="font-weight: 600;"><a href="${ev.url}" style="color: inherit; text-decoration: none;">${escapeHtml(ev.title)}</a></div>
                <div style="font-size: 10px; color: var(--text-muted);">${ev.badge}</div>
              </div>
            `).join('')}
            ${dayEvents.length === 0 ? '<div style="font-size: 11px; color: var(--text-muted); text-align: center; margin-top: 20px;">No events</div>' : ''}
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  }

  function renderDayView() {
    const dateStr = currentDate.toISOString().split('T')[0];
    const isToday = dateStr === new Date().toISOString().split('T')[0];
    const dayEvents = allEvents.filter(ev => ev.date === dateStr);

    if (titleEl) {
      titleEl.innerText = currentDate.toLocaleDateString(undefined, {weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'});
    }

    let html = `
      <div class="card" style="max-width: 680px; margin: 0 auto; ${isToday ? 'border-color: var(--primary-accent);' : ''}">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 14px;">
          <div>
            <div style="font-size: 16px; font-weight: 600;">Agenda for ${currentDate.toLocaleDateString(undefined, {month: 'short', day: 'numeric'})}</div>
            <div style="font-size: 12px; color: var(--text-secondary);">${dayEvents.length} scheduled event(s)</div>
          </div>
          ${isToday ? '<span class="badge badge-blue">Today</span>' : ''}
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          ${dayEvents.map(ev => `
            <div style="padding: 12px; border-radius: var(--radius-sm); border-left: 4px solid ${ev.color}; background: var(--bg-muted); display: flex; align-items: center; justify-content: space-between;">
              <div>
                <div style="font-weight: 600; font-size: 13px;">${escapeHtml(ev.title)}</div>
                <div style="font-size: 11.5px; color: var(--text-secondary);">Type: ${ev.badge}</div>
              </div>
              <a href="${ev.url}" class="btn btn-secondary btn-sm">View Record</a>
            </div>
          `).join('')}
          ${dayEvents.length === 0 ? '<div style="text-align: center; padding: 30px; color: var(--text-muted);">No scheduled deadlines, interviews, or tasks for this day.</div>' : ''}
        </div>
      </div>
    `;
    container.innerHTML = html;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
  }

  // Event Listeners
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentView === 'month') currentDate.setMonth(currentDate.getMonth() - 1);
      else if (currentView === 'week') currentDate.setDate(currentDate.getDate() - 7);
      else currentDate.setDate(currentDate.getDate() - 1);
      render();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentView === 'month') currentDate.setMonth(currentDate.getMonth() + 1);
      else if (currentView === 'week') currentDate.setDate(currentDate.getDate() + 7);
      else currentDate.setDate(currentDate.getDate() + 1);
      render();
    });
  }

  if (todayBtn) {
    todayBtn.addEventListener('click', () => {
      currentDate = new Date();
      render();
    });
  }

  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('btn-primary'));
      viewBtns.forEach(b => b.classList.add('btn-secondary'));
      btn.classList.remove('btn-secondary');
      btn.classList.add('btn-primary');

      currentView = btn.dataset.view;
      render();
    });
  });

  loadEvents();
});
