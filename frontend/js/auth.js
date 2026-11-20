/**
 * EduPlay - UnityLearn: Gamified Learning Experience Platform
 * Authentication Helpers & Navigation State Manager
 */

// Determine base path for redirects (whether in root or /pages/)
function getBasePath() {
  const path = window.location.pathname;
  if (path.includes('/pages/')) {
    return '../';
  }
  return './';
}

/**
 * Check if the user is authenticated.
 * If not authenticated, redirects to login.html.
 */
function checkAuth(redirectIfUnauth = true) {
  const token = localStorage.getItem('access_token');
  const userStr = localStorage.getItem('user_data');

  if (!token || !userStr) {
    // Check if demo query param is set
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === 'true') {
      // Initialize automatic demo session
      const demoUser = {
        id: 1,
        username: 'alex_hunter',
        first_name: 'Alex',
        last_name: 'Hunter',
        email: 'alex.hunter@unitylearn.edu',
        level: 12,
        xp: 2450,
        streak_days: 7,
        avatar: 'AH'
      };
      localStorage.setItem('access_token', 'demo_auto_token');
      localStorage.setItem('user_data', JSON.stringify(demoUser));
      return demoUser;
    }

    if (redirectIfUnauth) {
      const basePath = getBasePath();
      window.location.href = `${basePath}login.html`;
      return null;
    }
    return null;
  }

  try {
    return JSON.parse(userStr);
  } catch (e) {
    return null;
  }
}

/**
 * Returns currently authenticated user data or default demo fallback.
 */
function getUserData() {
  const userStr = localStorage.getItem('user_data');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {}
  }
  return {
    username: 'alex_hunter',
    first_name: 'Alex',
    last_name: 'Hunter',
    email: 'alex.hunter@unitylearn.edu',
    level: 12,
    xp: 2450,
    streak_days: 7,
    avatar: 'AH'
  };
}

/**
 * Update user data in localStorage
 */
function setUserData(userData) {
  localStorage.setItem('user_data', JSON.stringify(userData));
  initNavUser();
}

/**
 * Clear authentication credentials and redirect to login page.
 */
function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_data');
  const basePath = getBasePath();
  window.location.href = `${basePath}login.html`;
}

/**
 * Populates top navbar and sidebar user details throughout the platform.
 */
function initNavUser() {
  const user = getUserData();
  
  // Format avatar initials
  const initials = user.avatar || 
    ((user.first_name?.[0] || 'A') + (user.last_name?.[0] || 'H')).toUpperCase();
  const fullName = user.first_name ? `${user.first_name} ${user.last_name}` : user.username;

  // Sidebar user info
  document.querySelectorAll('.user-avatar-initials').forEach(el => {
    el.textContent = initials;
  });
  document.querySelectorAll('.user-name-display').forEach(el => {
    el.textContent = fullName;
  });
  document.querySelectorAll('.user-level-display').forEach(el => {
    el.textContent = `Level ${user.level || 12} Explorer`;
  });

  // Topbar gamification badges
  document.querySelectorAll('.user-xp-badge').forEach(el => {
    el.innerHTML = `<i class="fa-solid fa-bolt text-gold"></i> <span>${(user.xp || 2450).toLocaleString()} XP</span>`;
  });
  document.querySelectorAll('.user-streak-badge').forEach(el => {
    el.innerHTML = `<i class="fa-solid fa-fire text-secondary"></i> <span>${user.streak_days || 7} Days</span>`;
  });

  // Setup mobile sidebar toggle if present
  const toggleBtn = document.querySelector('.mobile-toggle');
  const sidebar = document.querySelector('.app-sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }
}

/**
 * Reusable sleek Toast notification system.
 */
function showToast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  let icon = 'fa-info-circle';
  if (type === 'success') icon = 'fa-circle-check';
  if (type === 'error') icon = 'fa-circle-exclamation';

  toast.innerHTML = `
    <i class="fa-solid ${icon}"></i>
    <span style="flex:1;">${message}</span>
    <i class="fa-solid fa-xmark toast-close"></i>
  `;

  const closeBtn = toast.querySelector('.toast-close');
  closeBtn.addEventListener('click', () => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(50px)';
    setTimeout(() => toast.remove(), 300);
  });

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentElement) {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(50px)';
      setTimeout(() => toast.remove(), 300);
    }
  }, duration);
}

// Global exposure
window.checkAuth = checkAuth;
window.getUserData = getUserData;
window.setUserData = setUserData;
window.logout = logout;
window.initNavUser = initNavUser;
window.showToast = showToast;
