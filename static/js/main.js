/**
 * CareerPilot Core UI Engine
 * Professional Enterprise Workspace Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme Switcher
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', async () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const targetTheme = currentTheme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', targetTheme);
      
      try {
        await fetch('/toggle-theme/', {
          method: 'GET',
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
      } catch (e) {
        console.warn('Theme preference sync offline', e);
      }
    });
  }

  // 2. Global Hotkey for Search (Ctrl+K or /)
  const searchInput = document.getElementById('global-search-input');
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey && e.key.toLowerCase() === 'k') || (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA')) {
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // 3. Mobile Sidebar Toggle
  const mobileToggle = document.getElementById('mobile-sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // 4. Interactive Task & Reminder Toggle Checkboxes
  document.querySelectorAll('.task-toggle-checkbox').forEach(box => {
    box.addEventListener('change', async (e) => {
      const taskId = e.target.dataset.taskId;
      const isCompleted = e.target.checked;
      const row = document.getElementById(`task-row-${taskId}`);
      
      try {
        const res = await fetch(`/planner/tasks/${taskId}/toggle/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ completed: isCompleted })
        });
        const data = await res.json();
        if (data.success && row) {
          if (isCompleted) {
            row.style.opacity = '0.5';
            row.style.textDecoration = 'line-through';
          } else {
            row.style.opacity = '1';
            row.style.textDecoration = 'none';
          }
        }
      } catch (err) {
        console.error('Task toggle failed', err);
        e.target.checked = !isCompleted;
      }
    });
  });

  // 5. Reminder Toggle
  document.querySelectorAll('.reminder-toggle-checkbox').forEach(box => {
    box.addEventListener('change', async (e) => {
      const reminderId = e.target.dataset.reminderId;
      const isCompleted = e.target.checked;
      const row = document.getElementById(`reminder-row-${reminderId}`);

      try {
        const res = await fetch(`/reminders/${reminderId}/toggle/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ completed: isCompleted })
        });
        const data = await res.json();
        if (data.success && row) {
          if (isCompleted) {
            row.style.opacity = '0.5';
          } else {
            row.style.opacity = '1';
          }
        }
      } catch (err) {
        console.error('Reminder toggle failed', err);
        e.target.checked = !isCompleted;
      }
    });
  });

  // 6. Interview Checklist Toggle
  document.querySelectorAll('.checklist-toggle-checkbox').forEach(box => {
    box.addEventListener('change', async (e) => {
      const itemId = e.target.dataset.itemId;
      const isChecked = e.target.checked;
      const label = document.getElementById(`checklist-label-${itemId}`);

      try {
        const res = await fetch(`/interviews/api/checklist/${itemId}/toggle/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ completed: isChecked })
        });
        const data = await res.json();
        if (data.success) {
          if (label) {
            label.style.textDecoration = isChecked ? 'line-through' : 'none';
            label.style.color = isChecked ? 'var(--text-muted)' : 'var(--text-primary)';
          }
          const progressEl = document.getElementById('checklist-progress-text');
          const progressBar = document.getElementById('checklist-progress-bar');
          if (progressEl) {
            progressEl.innerText = `${data.completed_items} of ${data.total_items} completed (${data.percentage}%)`;
          }
          if (progressBar) {
            progressBar.style.width = `${data.percentage}%`;
          }
        }
      } catch (err) {
        console.error('Checklist toggle failed', err);
        e.target.checked = !isChecked;
      }
    });
  });

  // 7. Opportunity Duplicate Checker in Create Form
  const companyInput = document.getElementById('id_company_name');
  const titleInput = document.getElementById('id_opportunity_title');
  const duplicateAlert = document.getElementById('duplicate-warning-banner');

  if (companyInput && titleInput && duplicateAlert) {
    const checkDuplicate = async () => {
      const company = companyInput.value.trim();
      const title = titleInput.value.trim();
      if (company.length > 1 && title.length > 2) {
        try {
          const res = await fetch(`/opportunities/api/check-duplicate/?company=${encodeURIComponent(company)}&title=${encodeURIComponent(title)}`);
          const data = await res.json();
          if (data.duplicate) {
            duplicateAlert.style.display = 'block';
            duplicateAlert.innerHTML = `Note: An opportunity with title "<strong>${data.existing_title}</strong>" at <strong>${data.company}</strong> was already saved on ${data.created_at}. <a href="/opportunities/${data.existing_id}/" style="text-decoration: underline; color: inherit;">View Existing</a>`;
          } else {
            duplicateAlert.style.display = 'none';
          }
        } catch (e) {
          console.warn('Duplicate check error', e);
        }
      }
    };
    companyInput.addEventListener('blur', checkDuplicate);
    titleInput.addEventListener('blur', checkDuplicate);
  }
});

// Helper: Read CSRF cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
