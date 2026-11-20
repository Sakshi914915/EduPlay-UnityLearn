/**
 * EduPlay - UnityLearn: Dashboard Controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Check auth guard
  const user = checkAuth(true);
  if (!user) return;

  // Initialize UI navigation and user pill indicators
  initNavUser();

  // Load dashboard data
  await loadDashboardData();

  // Setup notification bell toggle
  setupNotifications();

  // Setup search filter in quick actions
  setupSearch();
});

async function loadDashboardData() {
  try {
    const stats = await EduPlayAPI.getDashboardStats();
    const activities = await EduPlayAPI.getActivityLog();
    const leaderboard = await EduPlayAPI.getLeaderboard();
    const user = getUserData();

    // Populate Welcome Header
    const welcomeName = document.getElementById('welcome-user-name');
    if (welcomeName) {
      welcomeName.textContent = user.first_name || user.username || 'Scholar';
    }

    const levelBadge = document.getElementById('hero-level-badge');
    if (levelBadge) {
      levelBadge.textContent = `Level ${user.level || 12}`;
    }

    // Populate XP Progress
    const currentXp = user.xp || stats.xp || 2450;
    const targetXp = stats.next_level_xp || 3000;
    const pct = Math.min(100, Math.round((currentXp / targetXp) * 100));

    const xpCurrentEl = document.getElementById('xp-current-display');
    if (xpCurrentEl) xpCurrentEl.textContent = `${currentXp.toLocaleString()} XP`;

    const xpTargetEl = document.getElementById('xp-target-display');
    if (xpTargetEl) xpTargetEl.textContent = `${targetXp.toLocaleString()} XP`;

    const xpBar = document.getElementById('hero-xp-bar');
    if (xpBar) {
      setTimeout(() => {
        xpBar.style.width = `${pct}%`;
      }, 200);
    }

    // Populate 4 Metric Cards with animated counters
    animateValue('stat-total-xp', 0, currentXp, 1200);
    animateValue('stat-courses', 0, stats.courses_enrolled || 6, 800);
    animateValue('stat-badges', 0, stats.badges_count || 18, 900);
    animateValue('stat-streak', 0, stats.streak_days || 7, 700);

    // Render Recent Activities
    renderActivities(activities);

    // Render Mini Leaderboard
    renderLeaderboard(leaderboard);

  } catch (err) {
    console.error('Error loading dashboard:', err);
  }
}

function animateValue(id, start, end, duration) {
  const obj = document.getElementById(id);
  if (!obj) return;
  
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const value = Math.floor(progress * (end - start) + start);
    obj.innerHTML = value.toLocaleString();
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

function renderActivities(activities) {
  const container = document.getElementById('activity-feed-container');
  if (!container) return;

  if (!activities || activities.length === 0) {
    container.innerHTML = '<div style="color: var(--text-muted); padding: 1.5rem; text-align: center;">No recent activities yet.</div>';
    return;
  }

  container.innerHTML = activities.slice(0, 5).map(act => `
    <div style="display: flex; align-items: center; gap: 1rem; padding: 0.95rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
      <div style="width: 40px; height: 40px; border-radius: var(--radius-sm); background: rgba(255, 255, 255, 0.05); display: flex; align-items: center; justify-content: center; color: var(--${act.color || 'primary'}); font-size: 1.1rem; flex-shrink: 0;">
        <i class="fa-solid ${act.icon || 'fa-bolt'}"></i>
      </div>
      <div style="flex: 1; min-width: 0;">
        <div style="font-weight: 600; font-size: 0.9rem; color: #FFFFFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${act.title}</div>
        <div style="font-size: 0.78rem; color: var(--text-muted);">${act.time}</div>
      </div>
      <span class="badge badge-accent" style="font-size: 0.75rem;">+${act.xp} XP</span>
    </div>
  `).join('');
}

function renderLeaderboard(leaderboard) {
  const container = document.getElementById('mini-leaderboard-container');
  if (!container) return;

  if (!leaderboard || leaderboard.length === 0) {
    container.innerHTML = '<div style="color: var(--text-muted); text-align: center; padding: 1.5rem;">Leaderboard currently loading...</div>';
    return;
  }

  const topFive = leaderboard.slice(0, 5);
  container.innerHTML = topFive.map(item => {
    let rankBadge = `#${item.rank}`;
    if (item.rank === 1) rankBadge = '🥇';
    if (item.rank === 2) rankBadge = '🥈';
    if (item.rank === 3) rankBadge = '🥉';

    const isUser = item.is_current_user || item.username === 'alex_hunter';
    const bgStyle = isUser ? 'background: rgba(108, 99, 255, 0.12); border: 1px solid var(--border-glow);' : '';

    return `
      <div style="display: flex; align-items: center; gap: 0.9rem; padding: 0.75rem 0.85rem; border-radius: var(--radius-sm); ${bgStyle} margin-bottom: 0.4rem;">
        <span style="font-size: 1.1rem; font-weight: 800; width: 26px; text-align: center;">${rankBadge}</span>
        <div class="user-avatar" style="width: 34px; height: 34px; font-size: 0.8rem;">${item.avatar || 'US'}</div>
        <div style="flex: 1; min-width: 0;">
          <div style="font-weight: 600; font-size: 0.88rem; color: #FFFFFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${item.name || item.username} ${isUser ? '<span style="font-size: 0.7rem; color: var(--accent);">(You)</span>' : ''}
          </div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">Lvl ${item.level} • ${item.badge || 'Scholar'}</div>
        </div>
        <span style="font-weight: 700; font-size: 0.88rem; color: var(--gold);">${item.xp.toLocaleString()} XP</span>
      </div>
    `;
  }).join('');
}

function setupNotifications() {
  const bellBtn = document.getElementById('notif-bell-btn');
  const popup = document.getElementById('notif-dropdown-popup');
  if (bellBtn && popup) {
    bellBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', (e) => {
      if (!popup.contains(e.target) && !bellBtn.contains(e.target)) {
        popup.style.display = 'none';
      }
    });
  }
}

function setupSearch() {
  const searchInput = document.getElementById('dashboard-search-input');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    document.querySelectorAll('.quick-module-card').forEach(card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      const desc = card.querySelector('p').textContent.toLowerCase();
      if (title.includes(query) || desc.includes(query)) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  });
}
