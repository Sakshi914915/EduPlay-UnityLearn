/**
 * EduPlay - UnityLearn: Gamified Learning Experience Platform
 * Centralized API Client & Mock Fallbacks
 */

const API_BASE = 'http://127.0.0.1:8000/api';

// Demo fallback state store (persisted in localStorage for demo interactions)
const DEMO_STORE = {
  profile: {
    id: 1,
    username: 'alex_hunter',
    first_name: 'Alex',
    last_name: 'Hunter',
    email: 'alex.hunter@unitylearn.edu',
    level: 12,
    xp: 2450,
    next_level_xp: 3000,
    streak_days: 7,
    badges_count: 18,
    courses_enrolled: 6,
    avatar: 'AH',
    bio: 'Aspiring Full Stack Engineer & Quantum Simulation Enthusiast',
  },
  quizzes: [
    {
      id: 1,
      title: 'Python Data Structures & Algorithms',
      subject: 'Programming',
      difficulty: 'Medium',
      xp_reward: 200,
      time_limit_mins: 5,
      questions_count: 5,
      description: 'Test your understanding of Big-O complexity, binary search trees, and hash tables.',
      badge_reward: 'Algorithm Ace 🏆',
      questions: [
        {
          id: 101,
          text: 'What is the average time complexity of searching an element in a Balanced Binary Search Tree (AVL/Red-Black)?',
          options: ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
          correct_index: 1,
          explanation: 'Searching a balanced BST divides the search space in half at each step, yielding O(log n).'
        },
        {
          id: 102,
          text: 'Which python data structure is implemented under the hood as a dynamic array with amortized O(1) append?',
          options: ['list', 'dict', 'set', 'tuple'],
          correct_index: 0,
          explanation: 'Python lists are variable-length arrays backed by continuous memory blocks with geometric resizing.'
        },
        {
          id: 103,
          text: 'In graph theory, which algorithm is optimal for finding the shortest path in a graph with non-negative edge weights?',
          options: ['Bellman-Ford', 'Depth-First Search', "Dijkstra's Algorithm", "Floyd-Warshall"],
          correct_index: 2,
          explanation: "Dijkstra's algorithm greedily expands the minimum known distance node using a priority queue in O((V + E) log V)."
        },
        {
          id: 104,
          text: 'What happens when two distinct keys produce the same hash code in a hash table?',
          options: ['Memory leak error', 'Hash Collision', 'Stack overflow', 'Tuple mutation'],
          correct_index: 1,
          explanation: 'Hash collisions occur when distinct keys map to the same bucket and are resolved via chaining or open addressing.'
        },
        {
          id: 105,
          text: 'Which sorting algorithm has a worst-case time complexity of O(n log n) and is stable?',
          options: ['Quick Sort', 'Merge Sort', 'Heap Sort', 'Selection Sort'],
          correct_index: 1,
          explanation: 'Merge sort always guarantees O(n log n) worst-case time complexity and preserves the relative order of identical keys.'
        }
      ]
    },
    {
      id: 2,
      title: 'Quantum Physics: Wave-Particle Duality',
      subject: 'Science',
      difficulty: 'Hard',
      xp_reward: 350,
      time_limit_mins: 6,
      questions_count: 4,
      description: 'Explore the de Broglie wavelength, photon momentum, and the double-slit experiment.',
      badge_reward: 'Quantum Pioneer ⚛️',
      questions: [
        {
          id: 201,
          text: 'According to the de Broglie hypothesis, what is the wavelength λ of a particle with momentum p?',
          options: ['λ = h * p', 'λ = h / p', 'λ = p / h', 'λ = h * c / p'],
          correct_index: 1,
          explanation: 'de Broglie wavelength is Planck constant h divided by momentum p (λ = h/p).'
        },
        {
          id: 202,
          text: 'In the photoelectric effect, increasing the light intensity increases which property of emitted electrons?',
          options: ['Maximum kinetic energy', 'Number of photoelectrons emitted per second', 'Threshold frequency', 'Work function'],
          correct_index: 1,
          explanation: 'Intensity increases the photon flux per unit time, ejecting more electrons, while frequency determines their kinetic energy.'
        },
        {
          id: 203,
          text: 'The Heisenberg Uncertainty Principle states that one cannot simultaneously measure precisely which pair of variables?',
          options: ['Position and Linear Momentum', 'Energy and Charge', 'Mass and Velocity', 'Spin and Magnetic Field'],
          correct_index: 0,
          explanation: 'Δx * Δp >= ħ/2 specifies the fundamental quantum limit between position and momentum.'
        },
        {
          id: 204,
          text: 'What was the revolutionary conclusion of the Young Double-Slit experiment when performed with single electrons?',
          options: ['Electrons behave only as bullets', 'Electrons self-interfere as probability waves', 'Electrons disappear into antimatter', 'Energy is not conserved'],
          correct_index: 1,
          explanation: 'Even single electrons build up an interference pattern over time, proving their wave-like wavepacket nature.'
        }
      ]
    },
    {
      id: 3,
      title: 'Discrete Mathematics & Boolean Logic',
      subject: 'Mathematics',
      difficulty: 'Easy',
      xp_reward: 120,
      time_limit_mins: 4,
      questions_count: 3,
      description: 'Master propositional logic, truth tables, and De Morgan laws.',
      badge_reward: 'Logic Master 🧠',
      questions: [
        {
          id: 301,
          text: 'According to De Morgan laws, what is the negation of (A AND B)?',
          options: ['(NOT A) AND (NOT B)', '(NOT A) OR (NOT B)', 'NOT (A OR B)', 'A OR (NOT B)'],
          correct_index: 1,
          explanation: '¬(A ∧ B) is equivalent to (¬A ∨ ¬B).'
        },
        {
          id: 302,
          text: 'What is the boolean evaluation of: TRUE XOR TRUE?',
          options: ['TRUE', 'FALSE', 'NULL', 'UNDEFINED'],
          correct_index: 1,
          explanation: 'Exclusive OR (XOR) returns TRUE strictly when inputs differ; for identical inputs it evaluates to FALSE.'
        },
        {
          id: 303,
          text: 'A conditional statement "P implies Q" is false only when:',
          options: ['P is true and Q is false', 'P is false and Q is true', 'Both P and Q are false', 'Both P and Q are true'],
          correct_index: 0,
          explanation: 'A promise P → Q is broken only if hypothesis P holds true but conclusion Q fails.'
        }
      ]
    }
  ],
  leaderboard: [
    { rank: 1, username: 'Elena_Valkyrie', name: 'Elena Rostova', xp: 5420, level: 24, badge: 'Grandmaster 🥇', avatar: 'ER' },
    { rank: 2, username: 'DevKai', name: 'Kai Takahashi', xp: 4890, level: 21, badge: 'Code Samurai 🥈', avatar: 'KT' },
    { rank: 3, username: 'QuantumSarah', name: 'Sarah Jenkins', xp: 4210, level: 19, badge: 'Physicist 🥉', avatar: 'SJ' },
    { rank: 4, username: 'alex_hunter', name: 'Alex Hunter', xp: 2450, level: 12, badge: 'Rising Star 🌟', avatar: 'AH', is_current_user: true },
    { rank: 5, username: 'NeuralNeo', name: 'Neo Anderson', xp: 2100, level: 11, badge: 'AI Apprentice 🤖', avatar: 'NA' },
    { rank: 6, username: 'MayaMatrix', name: 'Maya Lin', xp: 1980, level: 10, badge: 'Data Explorer', avatar: 'ML' },
    { rank: 7, username: 'VikramChandra', name: 'Vikram Chandra', xp: 1850, level: 9, badge: 'Lab Guru', avatar: 'VC' },
    { rank: 8, username: 'ZaraNebula', name: 'Zara Smith', xp: 1720, level: 9, badge: 'Quest Hunter', avatar: 'ZS' }
  ],
  courses: [
    {
      id: 1,
      title: 'Full-Stack Gamified Systems Engineering',
      instructor: 'Dr. Marcus Vance',
      subject: 'Computer Science',
      difficulty: 'Intermediate',
      duration: '6 Weeks',
      lessons_count: 24,
      enrolled_count: 1420,
      progress: 65,
      is_enrolled: true,
      thumbnail_gradient: 'linear-gradient(135deg, #6C63FF, #38B6FF)',
      icon: 'fa-code',
      description: 'Learn modern decoupled architectures, state machines, WebSockets, and real-time gamification feedback loops.',
      modules: [
        { title: 'Foundations of Gamified Architectures', lessons: ['Core reward loops & dopamine timing', 'Event-driven state management', 'Token-based auth with SimpleJWT'] },
        { title: 'Interactive Frontend Engines', lessons: ['Canvas 2D physics integration', 'CSS Glassmorphism rendering techniques', 'Real-time WebSocket telemetry'] },
        { title: 'Scalable Backend & Leaderboard Systems', lessons: ['Redis Sorted Sets for sub-millisecond ranks', 'PostgreSQL transaction isolation', 'Distributed anti-cheat validation'] }
      ]
    },
    {
      id: 2,
      title: 'Quantum Mechanics & Computational Chemistry',
      instructor: 'Prof. Alistair Thorne',
      subject: 'Physics',
      difficulty: 'Advanced',
      duration: '8 Weeks',
      lessons_count: 32,
      enrolled_count: 890,
      progress: 40,
      is_enrolled: true,
      thumbnail_gradient: 'linear-gradient(135deg, #FF6584, #FFA07A)',
      icon: 'fa-atom',
      description: 'From Schrödinger equation derivations to molecular orbital 3D simulations and Hamiltonian matrix solvers.',
      modules: [
        { title: 'Wave Mechanics & Hilbert Spaces', lessons: ['Wavepackets and superposition', 'Operators and Eigenvalues', 'Harmonic oscillator quantization'] },
        { title: 'Virtual Laboratory Simulations', lessons: ['Potential step tunneling', 'Hydrogen atom radial probability', 'Spin precession in magnetic fields'] }
      ]
    },
    {
      id: 3,
      title: 'Neural Networks & Deep Reinforcement Learning',
      instructor: 'Dr. Sophia Zhang',
      subject: 'Artificial Intelligence',
      difficulty: 'Advanced',
      duration: '10 Weeks',
      lessons_count: 40,
      enrolled_count: 2150,
      progress: 0,
      is_enrolled: false,
      thumbnail_gradient: 'linear-gradient(135deg, #43E97B, #38EF7D)',
      icon: 'fa-brain',
      description: 'Master Q-learning, Policy Gradients, Actor-Critic models and train autonomous agents to play Unity games.',
      modules: [
        { title: 'Deep Learning Foundations', lessons: ['Backpropagation & Automatic Differentiation', 'Convolutional Architectures', 'Transformers & Self-Attention'] },
        { title: 'Reinforcement Learning in Action', lessons: ['Markov Decision Processes', 'Deep Q-Networks (DQN)', 'PPO & Environment Vectorization'] }
      ]
    },
    {
      id: 4,
      title: 'Interactive 3D Game Math & Physics',
      instructor: 'Kenji Sato',
      subject: 'Mathematics',
      difficulty: 'Intermediate',
      duration: '5 Weeks',
      lessons_count: 18,
      enrolled_count: 1100,
      progress: 10,
      is_enrolled: true,
      thumbnail_gradient: 'linear-gradient(135deg, #FFA07A, #FFD700)',
      icon: 'fa-cubes',
      description: 'Vectors, Quaternions, Ray-marching, Verlet integration, and collision manifolds built from scratch.',
      modules: [
        { title: 'Vector Algebra for Graphics', lessons: ['Dot & Cross Products', 'Transformation Matrices', 'Euler angles vs Quaternions'] },
        { title: 'Physics Engines & Collision', lessons: ['Separating Axis Theorem (SAT)', 'Verlet Integration vs Euler', 'Constraint Solvers'] }
      ]
    }
  ],
  forumPosts: [
    {
      id: 1,
      title: 'How do you optimize 60 FPS canvas rendering with 1,000 active particles?',
      author: 'Kai Takahashi',
      author_avatar: 'KT',
      author_badge: 'Samurai',
      category: 'Programming',
      created_at: '2 hours ago',
      likes: 34,
      is_liked: false,
      replies_count: 7,
      content: 'I noticed frame drops when repainting thousands of particles individually. Switching to Path2D batching and OffscreenCanvas gave a 4x boost! Has anyone experimented with WebGL shaders for the simulation module?',
      comments: [
        { id: 11, author: 'Alex Hunter', author_avatar: 'AH', created_at: '1 hour ago', text: 'OffscreenCanvas with requestAnimationFrame web workers works wonders. WebGL compute shaders are even faster if you use instanced mesh rendering!' },
        { id: 12, author: 'Elena Rostova', author_avatar: 'ER', created_at: '30 mins ago', text: 'Great tip! Also remember to avoid creating objects in the tick loop to prevent GC pauses.' }
      ]
    },
    {
      id: 2,
      title: 'Intuitive breakdown of Double-Slit wave interference pattern',
      author: 'Sarah Jenkins',
      author_avatar: 'SJ',
      author_badge: 'Physicist',
      category: 'Science',
      created_at: '5 hours ago',
      likes: 52,
      is_liked: true,
      replies_count: 4,
      content: 'Here is an easy mental model: imagine each slit acts as a source of circular ripples in water. The bright bands are peaks aligning with peaks (constructive interference), while dark bands are peaks canceling troughs (destructive).',
      comments: [
        { id: 21, author: 'Alex Hunter', author_avatar: 'AH', created_at: '3 hours ago', text: 'This clicked for me! The simulation slider on Module 2 made it so obvious.' }
      ]
    },
    {
      id: 3,
      title: 'Study Group formation: Preparing for Algorithm Ace Championship',
      author: 'Elena Rostova',
      author_avatar: 'ER',
      author_badge: 'Grandmaster',
      category: 'Study Groups',
      created_at: '1 day ago',
      likes: 28,
      is_liked: false,
      replies_count: 12,
      content: 'Hosting daily 45-minute sprint sessions solving dynamic programming and graph quest challenges. Everyone is welcome to join our voice channel!',
      comments: []
    }
  ],
  studyGroups: [
    { id: 1, name: 'Python Algorithms Guild', subject: 'Computer Science', members: 48, max_members: 60, is_joined: true, description: 'Daily competitive coding sprints, leetcode discussions, and peer mock interviews.' },
    { id: 2, name: 'Quantum Simulation Lab Circle', subject: 'Physics', members: 29, max_members: 40, is_joined: false, description: 'Collaborative analysis of quantum mechanics simulations and lab reports.' },
    { id: 3, name: 'Neural Network Guild', subject: 'Artificial Intelligence', members: 35, max_members: 50, is_joined: true, description: 'Paper reading group and reinforcement learning hackathons.' }
  ],
  authorDrafts: [
    { id: 1, title: 'Calculus III: Vector Surface Integrals', type: 'Quiz', status: 'Published', questions: 8, views: 340, updated_at: 'Yesterday' },
    { id: 2, title: 'Thermodynamics Carnot Cycle Engine', type: 'Simulation', status: 'Draft', questions: 0, views: 12, updated_at: '3 days ago' },
    { id: 3, title: 'Rust Memory Safety & Lifetimes', type: 'Course', status: 'Review', questions: 15, views: 185, updated_at: '5 days ago' }
  ]
};

// ==========================================================================
// Core Fetch Wrapper
// ==========================================================================

async function apiRequest(endpoint, method = 'GET', data = null, requiresAuth = true) {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
  
  const headers = {
    'Content-Type': 'application/json',
  };

  if (requiresAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const options = {
    method,
    headers,
  };

  if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);

    // If 401 Unauthorized and we had auth, try token refresh once
    if (response.status === 401 && requiresAuth) {
      const refreshed = await refreshToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
        const retryResponse = await fetch(url, options);
        if (!retryResponse.ok) throw new Error(`HTTP ${retryResponse.status}`);
        return await retryResponse.json();
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login.html';
        return null;
      }
    }

    if (!response.ok) {
      const errorJson = await response.json().catch(() => ({}));
      const err = new Error(errorJson.detail || errorJson.error || `HTTP ${response.status}`);
      err.status = response.status;
      err.data = errorJson;
      throw err;
    }

    return await response.json();
  } catch (error) {
    console.warn(`[EduPlay API] Network/Endpoint error for ${method} ${endpoint}:`, error.message);
    // Throw error so caller can utilize demo fallback seamlessly
    throw error;
  }
}

// ==========================================================================
// Authentication APIs
// ==========================================================================

async function login(credentials) {
  try {
    // Attempt standard Django SimpleJWT or custom account login endpoint
    const res = await apiRequest('/token/', 'POST', {
      username: credentials.username || credentials.email,
      password: credentials.password
    }, false).catch(async () => {
      return await apiRequest('/accounts/login/', 'POST', credentials, false);
    });

    if (res && res.access) {
      localStorage.setItem('access_token', res.access);
      if (res.refresh) localStorage.setItem('refresh_token', res.refresh);
      const user = res.user || {
        username: credentials.username || credentials.email.split('@')[0],
        email: credentials.email || `${credentials.username}@unitylearn.edu`,
        first_name: 'Alex',
        last_name: 'Hunter',
        level: 12,
        xp: 2450
      };
      localStorage.setItem('user_data', JSON.stringify(user));
      return { success: true, user, token: res.access };
    }
  } catch (err) {
    console.warn('[EduPlay] Backend unavailable, activating seamless Demo Mode login.');
  }

  // Demo Fallback Login
  const demoUser = {
    ...DEMO_STORE.profile,
    username: credentials.username || credentials.email.split('@')[0] || 'alex_hunter',
  };
  localStorage.setItem('access_token', 'demo_jwt_access_token_eduplay_2024');
  localStorage.setItem('refresh_token', 'demo_jwt_refresh_token_eduplay_2024');
  localStorage.setItem('user_data', JSON.stringify(demoUser));
  return { success: true, user: demoUser, isDemo: true };
}

async function register(userData) {
  try {
    const res = await apiRequest('/accounts/register/', 'POST', userData, false);
    return res;
  } catch (err) {
    console.warn('[EduPlay] Backend unavailable, simulating local registration.');
    const demoUser = {
      username: userData.username,
      email: userData.email,
      first_name: userData.first_name || 'Scholar',
      last_name: userData.last_name || 'Adventurer',
      level: 1,
      xp: 100,
      streak_days: 1,
      badges_count: 1,
      avatar: (userData.first_name?.[0] || 'S') + (userData.last_name?.[0] || 'A')
    };
    localStorage.setItem('access_token', 'demo_jwt_token_' + Date.now());
    localStorage.setItem('user_data', JSON.stringify(demoUser));
    return { success: true, user: demoUser, isDemo: true };
  }
}

async function refreshToken() {
  const refresh = localStorage.getItem('refresh_token');
  if (!refresh || refresh.startsWith('demo_')) return false;

  try {
    const response = await fetch(`${API_BASE}/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    if (!response.ok) return false;
    const data = await response.json();
    if (data.access) {
      localStorage.setItem('access_token', data.access);
      return true;
    }
  } catch (e) {
    return false;
  }
  return false;
}

// ==========================================================================
// Profile & Dashboard Stats
// ==========================================================================

async function getProfile() {
  try {
    const res = await apiRequest('/accounts/profile/');
    return res;
  } catch (e) {
    // Return stored user or fallback demo profile
    const stored = localStorage.getItem('user_data');
    if (stored) {
      try { return JSON.parse(stored); } catch (err) {}
    }
    return DEMO_STORE.profile;
  }
}

async function getDashboardStats() {
  try {
    const res = await apiRequest('/analytics/dashboard/');
    return res;
  } catch (e) {
    return {
      xp: 2450,
      xp_this_week: 320,
      level: 12,
      next_level_xp: 3000,
      courses_enrolled: 6,
      courses_completed: 4,
      badges_count: 18,
      streak_days: 7,
      study_hours: 46.5,
      accuracy_rate: 88.4
    };
  }
}

async function getActivityLog() {
  try {
    const res = await apiRequest('/analytics/activity/');
    return res;
  } catch (e) {
    return [
      { id: 1, type: 'quiz', title: 'Completed Python DSA Quiz', xp: 200, time: '35 minutes ago', icon: 'fa-trophy', color: 'primary' },
      { id: 2, type: 'simulation', title: 'Explored Newton Laws Friction Lab', xp: 150, time: '3 hours ago', icon: 'fa-flask', color: 'accent' },
      { id: 3, type: 'course', title: 'Progressed in Full-Stack Engineering', xp: 80, time: 'Yesterday', icon: 'fa-book-open', color: 'info' },
      { id: 4, type: 'forum', title: 'Received 12 likes on Canvas Optimization', xp: 50, time: '2 days ago', icon: 'fa-comments', color: 'secondary' },
      { id: 5, type: 'badge', title: 'Unlocked Badge: Quantum Pioneer ⚛️', xp: 300, time: '3 days ago', icon: 'fa-medal', color: 'warning' }
    ];
  }
}

// ==========================================================================
// Game-Based Learning APIs (Quizzes & Leaderboards)
// ==========================================================================

async function getLeaderboard() {
  try {
    const res = await apiRequest('/gamebased/leaderboard/');
    return res;
  } catch (e) {
    return DEMO_STORE.leaderboard;
  }
}

async function getQuizList(filters = {}) {
  try {
    const query = new URLSearchParams(filters).toString();
    const res = await apiRequest(`/gamebased/quizzes/${query ? '?' + query : ''}`);
    return res;
  } catch (e) {
    return DEMO_STORE.quizzes;
  }
}

async function getQuizDetail(id) {
  try {
    const res = await apiRequest(`/gamebased/quizzes/${id}/`);
    return res;
  } catch (e) {
    return DEMO_STORE.quizzes.find(q => q.id === Number(id)) || DEMO_STORE.quizzes[0];
  }
}

async function submitQuiz(id, answers) {
  try {
    const res = await apiRequest(`/gamebased/quizzes/${id}/submit/`, 'POST', { answers });
    return res;
  } catch (e) {
    // Local calculation for demo mode
    const quiz = DEMO_STORE.quizzes.find(q => q.id === Number(id)) || DEMO_STORE.quizzes[0];
    let correctCount = 0;
    quiz.questions.forEach((q, idx) => {
      if (answers[idx] === q.correct_index) correctCount++;
    });
    const scorePct = Math.round((correctCount / quiz.questions.length) * 100);
    const xpEarned = Math.round((scorePct / 100) * quiz.xp_reward);
    
    // Update local profile XP
    const user = JSON.parse(localStorage.getItem('user_data') || '{}');
    if (user.xp !== undefined) {
      user.xp += xpEarned;
      localStorage.setItem('user_data', JSON.stringify(user));
    }

    return {
      success: true,
      quiz_id: id,
      total_questions: quiz.questions.length,
      correct_answers: correctCount,
      score_percentage: scorePct,
      xp_earned: xpEarned,
      badge_unlocked: scorePct >= 75 ? quiz.badge_reward : null
    };
  }
}

// ==========================================================================
// Course & Learning Paths APIs
// ==========================================================================

async function getCourseList(filters = {}) {
  try {
    const query = new URLSearchParams(filters).toString();
    const res = await apiRequest(`/learningpaths/courses/${query ? '?' + query : ''}`);
    return res;
  } catch (e) {
    return DEMO_STORE.courses;
  }
}

async function enrollCourse(id) {
  try {
    const res = await apiRequest(`/learningpaths/courses/${id}/enroll/`, 'POST');
    return res;
  } catch (e) {
    const course = DEMO_STORE.courses.find(c => c.id === Number(id));
    if (course) {
      course.is_enrolled = true;
      course.enrolled_count += 1;
    }
    return { success: true, message: 'Successfully enrolled!', course_id: id };
  }
}

// ==========================================================================
// Collaborative Learning APIs (Forums & Study Groups)
// ==========================================================================

async function getForumPosts(category = 'all') {
  try {
    const res = await apiRequest(`/collaborative/posts/${category !== 'all' ? '?category=' + category : ''}`);
    return res;
  } catch (e) {
    if (category === 'all') return DEMO_STORE.forumPosts;
    return DEMO_STORE.forumPosts.filter(p => p.category.toLowerCase() === category.toLowerCase());
  }
}

async function createPost(data) {
  try {
    const res = await apiRequest('/collaborative/posts/', 'POST', data);
    return res;
  } catch (e) {
    const user = JSON.parse(localStorage.getItem('user_data') || '{}');
    const newPost = {
      id: Date.now(),
      title: data.title,
      author: user.first_name ? `${user.first_name} ${user.last_name}` : 'Alex Hunter',
      author_avatar: user.avatar || 'AH',
      author_badge: 'Scholar',
      category: data.category || 'General',
      created_at: 'Just now',
      likes: 1,
      is_liked: true,
      replies_count: 0,
      content: data.content,
      comments: []
    };
    DEMO_STORE.forumPosts.unshift(newPost);
    return newPost;
  }
}

async function likePost(postId) {
  const post = DEMO_STORE.forumPosts.find(p => p.id === Number(postId));
  if (post) {
    post.is_liked = !post.is_liked;
    post.likes += post.is_liked ? 1 : -1;
    return { likes: post.likes, is_liked: post.is_liked };
  }
  return { likes: 10, is_liked: true };
}

async function addComment(postId, text) {
  const user = JSON.parse(localStorage.getItem('user_data') || '{}');
  const post = DEMO_STORE.forumPosts.find(p => p.id === Number(postId));
  const newComment = {
    id: Date.now(),
    author: user.first_name ? `${user.first_name} ${user.last_name}` : 'Alex Hunter',
    author_avatar: user.avatar || 'AH',
    created_at: 'Just now',
    text
  };
  if (post) {
    post.comments.push(newComment);
    post.replies_count = post.comments.length;
  }
  return newComment;
}

async function getStudyGroups() {
  try {
    const res = await apiRequest('/collaborative/groups/');
    return res;
  } catch (e) {
    return DEMO_STORE.studyGroups;
  }
}

async function joinGroup(groupId) {
  const group = DEMO_STORE.studyGroups.find(g => g.id === Number(groupId));
  if (group) {
    group.is_joined = !group.is_joined;
    group.members += group.is_joined ? 1 : -1;
    return { is_joined: group.is_joined, members: group.members };
  }
  return { is_joined: true };
}

// ==========================================================================
// Authoring APIs (Quiz & Content Builder)
// ==========================================================================

async function getAuthorContent() {
  try {
    const res = await apiRequest('/authoring/content/');
    return res;
  } catch (e) {
    return DEMO_STORE.authorDrafts;
  }
}

async function saveAuthorContent(contentData) {
  try {
    const res = await apiRequest('/authoring/content/', 'POST', contentData);
    return res;
  } catch (e) {
    const newDraft = {
      id: Date.now(),
      title: contentData.title || 'Untitled Assessment',
      type: contentData.type || 'Quiz',
      status: contentData.status || 'Published',
      questions: contentData.questions ? contentData.questions.length : 5,
      views: 0,
      updated_at: 'Just now'
    };
    DEMO_STORE.authorDrafts.unshift(newDraft);
    return newDraft;
  }
}

// Export functions to window scope for easy vanilla JS modularity
window.EduPlayAPI = {
  API_BASE,
  DEMO_STORE,
  apiRequest,
  login,
  register,
  refreshToken,
  getProfile,
  getDashboardStats,
  getActivityLog,
  getLeaderboard,
  getQuizList,
  getQuizDetail,
  submitQuiz,
  getCourseList,
  enrollCourse,
  getForumPosts,
  createPost,
  likePost,
  addComment,
  getStudyGroups,
  joinGroup,
  getAuthorContent,
  saveAuthorContent
};
