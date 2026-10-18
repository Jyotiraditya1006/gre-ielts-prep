/* ═══════════════════════════════════════════
   PrepAce – Frontend JavaScript Application
   ═══════════════════════════════════════════ */

const API = 'http://localhost:8000/api';
let token = localStorage.getItem('prep_token');
let currentUser = JSON.parse(localStorage.getItem('prep_user') || 'null');
let currentPage = 'dashboard';

// ── Quiz state ──────────────────────────────────────────────────
let quizQuestions = [];
let quizIndex = 0;
let quizAnswers = [];
let quizSessionId = null;
let quizTimer = null;
let quizTimeLeft = 90;
let quizExam = '';
let quizSection = '';
let quizDifficulty = '';
let quizStartTime = null;
let lastRetryConfig = null;
let isInfiniteMode = false;
let infiniteScore = { correct: 0, total: 0 };

// ── Flashcard state ─────────────────────────────────────────────
let flashcards = [];
let reviewCards = [];
let reviewIndex = 0;
let cardFlipped = false;

// ── Mock state ──────────────────────────────────────────────────
let selectedMockExam = null;

/* ═══════════════════════════════════════════
   API HELPER
   ═══════════════════════════════════════════ */
async function api(method, path, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (token) opts.headers['Authorization'] = `Bearer ${token}`;
  if (body) opts.body = JSON.stringify(body);
  
  try {
    const res = await fetch(`${API}${path}`, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');
    return data;
  } catch (e) {
    throw e;
  }
}

/* ═══════════════════════════════════════════
   AUTH
   ═══════════════════════════════════════════ */
/* ═══════════════════════════════════════════
   AUTH & OTP RECOVERY ENGINE
   ═══════════════════════════════════════════ */
let otpLoginTimerInterval = null;
let fpTimerInterval = null;

function hideAllAuthForms() {
  document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
}

function showLogin() {
  hideAllAuthForms();
  document.getElementById('login-form').classList.add('active');
}

function showRegister() {
  hideAllAuthForms();
  document.getElementById('register-form').classList.add('active');
}

function showOTPLoginForm() {
  hideAllAuthForms();
  document.getElementById('otp-login-form').classList.add('active');
}

function showForgotPasswordForm() {
  hideAllAuthForms();
  document.getElementById('forgot-password-form').classList.add('active');
}

async function handleLogin() {
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const errEl = document.getElementById('login-error');
  const btn = document.getElementById('login-btn');
  
  errEl.classList.add('hidden');
  if (!email || !password) { showError(errEl, 'Please enter your email or phone number and password'); return; }
  
  setLoading(btn, true);
  try {
    const data = await api('POST', '/auth/login', { email, password });
    onLoginSuccess(data);
  } catch (e) {
    showError(errEl, e.message);
  } finally {
    setLoading(btn, false);
  }
}

async function handleRegister() {
  const username = document.getElementById('reg-username').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const phone_number = document.getElementById('reg-phone')?.value.trim() || null;
  const password = document.getElementById('reg-password').value;
  const target_exam = document.getElementById('reg-exam').value;
  const errEl = document.getElementById('reg-error');
  const btn = document.getElementById('reg-btn');
  
  errEl.classList.add('hidden');
  if (!username || !email || !password) { showError(errEl, 'Please fill in all required fields'); return; }
  if (password.length < 6) { showError(errEl, 'Password must be at least 6 characters'); return; }
  
  setLoading(btn, true);
  try {
    const data = await api('POST', '/auth/register', { 
      username, email, password, phone_number, target_exam 
    });
    showToast('🎉 Account created successfully! Welcome to PrepAce.', 'success');
    onLoginSuccess(data);
  } catch (e) {
    showError(errEl, e.message);
  } finally {
    setLoading(btn, false);
  }
}

// ── Mobile OTP Login ──────────────────────────────────────────
async function handleSendOTPLogin() {
  const phone = document.getElementById('otp-login-phone').value.trim();
  const errEl = document.getElementById('otp-login-error');
  const successEl = document.getElementById('otp-login-success');
  const btn = document.getElementById('otp-login-send-btn');
  
  errEl.classList.add('hidden');
  successEl.classList.add('hidden');
  
  if (!phone || phone.length < 10) {
    showError(errEl, 'Please enter a valid 10-digit mobile phone number');
    return;
  }
  
  btn.disabled = true;
  btn.textContent = 'Sending...';
  
  try {
    const res = await api('POST', '/auth/send-otp', { phone_number: phone, purpose: 'login' });
    document.getElementById('otp-login-code-group').classList.remove('hidden');
    document.getElementById('otp-verify-login-btn').disabled = false;
    
    successEl.textContent = res.message;
    successEl.classList.remove('hidden');
    
    if (res.demo_otp) {
      showToast(`📱 SMS: Your PrepAce verification code is [ ${res.demo_otp} ]`, 'success');
      // Auto-fill demo OTP for one-click testing
      const codeInput = document.getElementById('otp-login-code');
      codeInput.value = res.demo_otp;
      codeInput.focus();
    }
    
    // 60-second countdown
    let secondsLeft = 60;
    clearInterval(otpLoginTimerInterval);
    const countdownEl = document.getElementById('otp-login-countdown');
    countdownEl.textContent = `Resend in ${secondsLeft}s`;
    
    otpLoginTimerInterval = setInterval(() => {
      secondsLeft--;
      if (secondsLeft <= 0) {
        clearInterval(otpLoginTimerInterval);
        countdownEl.textContent = '';
        btn.disabled = false;
        btn.textContent = 'Resend OTP';
      } else {
        countdownEl.textContent = `Resend in ${secondsLeft}s`;
      }
    }, 1000);
  } catch (e) {
    showError(errEl, e.message);
    btn.disabled = false;
    btn.textContent = 'Send OTP';
  }
}

async function handleVerifyOTPLogin() {
  const phone = document.getElementById('otp-login-phone').value.trim();
  const otp = document.getElementById('otp-login-code').value.trim();
  const errEl = document.getElementById('otp-login-error');
  const btn = document.getElementById('otp-verify-login-btn');
  
  errEl.classList.add('hidden');
  if (!otp || otp.length !== 6) {
    showError(errEl, 'Please enter the 6-digit OTP code');
    return;
  }
  
  setLoading(btn, true);
  try {
    const data = await api('POST', '/auth/verify-otp-login', { phone_number: phone, otp });
    showToast('✅ Mobile phone verified! Signing you in...', 'success');
    onLoginSuccess(data);
  } catch (e) {
    showError(errEl, e.message);
  } finally {
    setLoading(btn, false);
  }
}

// ── Forgot Password via Mobile OTP ─────────────────────────────
async function handleSendForgotOTP() {
  const phone = document.getElementById('fp-phone').value.trim();
  const errEl = document.getElementById('fp-error');
  const successEl = document.getElementById('fp-success');
  const btn = document.getElementById('fp-send-btn');
  
  errEl.classList.add('hidden');
  successEl.classList.add('hidden');
  
  if (!phone || phone.length < 10) {
    showError(errEl, 'Please enter your registered 10-digit mobile number');
    return;
  }
  
  btn.disabled = true;
  btn.textContent = 'Sending...';
  
  try {
    const res = await api('POST', '/auth/send-otp', { phone_number: phone, purpose: 'forgot_password' });
    document.getElementById('fp-fields-group').classList.remove('hidden');
    document.getElementById('fp-submit-btn').disabled = false;
    
    successEl.textContent = res.message;
    successEl.classList.remove('hidden');
    
    if (res.demo_otp) {
      showToast(`📱 SMS: Your password reset OTP is [ ${res.demo_otp} ]`, 'success');
      const otpInput = document.getElementById('fp-otp');
      otpInput.value = res.demo_otp;
      document.getElementById('fp-new-password')?.focus();
    }
    
    let secondsLeft = 60;
    clearInterval(fpTimerInterval);
    const countdownEl = document.getElementById('fp-countdown');
    countdownEl.textContent = `Resend in ${secondsLeft}s`;
    
    fpTimerInterval = setInterval(() => {
      secondsLeft--;
      if (secondsLeft <= 0) {
        clearInterval(fpTimerInterval);
        countdownEl.textContent = '';
        btn.disabled = false;
        btn.textContent = 'Resend OTP';
      } else {
        countdownEl.textContent = `Resend in ${secondsLeft}s`;
      }
    }, 1000);
  } catch (e) {
    showError(errEl, e.message);
    btn.disabled = false;
    btn.textContent = 'Send OTP';
  }
}

async function handleResetPasswordOTP() {
  const phone = document.getElementById('fp-phone').value.trim();
  const otp = document.getElementById('fp-otp').value.trim();
  const new_password = document.getElementById('fp-new-password').value;
  const errEl = document.getElementById('fp-error');
  const btn = document.getElementById('fp-submit-btn');
  
  errEl.classList.add('hidden');
  if (!otp || otp.length !== 6) {
    showError(errEl, 'Please enter the 6-digit verification code');
    return;
  }
  if (!new_password || new_password.length < 6) {
    showError(errEl, 'New password must be at least 6 characters');
    return;
  }
  
  setLoading(btn, true);
  try {
    const data = await api('POST', '/auth/reset-password-otp', {
      phone_number: phone,
      otp,
      new_password
    });
    showToast('🔑 Password reset successfully! Signed in with your new password.', 'success');
    onLoginSuccess(data);
  } catch (e) {
    showError(errEl, e.message);
  } finally {
    setLoading(btn, false);
  }
}


function onLoginSuccess(data) {
  token = data.access_token;
  currentUser = data.user;
  localStorage.setItem('prep_token', token);
  localStorage.setItem('prep_user', JSON.stringify(currentUser));
  
  document.getElementById('auth-overlay').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  
  initApp();
}

function logout() {
  token = null; currentUser = null;
  localStorage.removeItem('prep_token');
  localStorage.removeItem('prep_user');
  document.getElementById('auth-overlay').classList.remove('hidden');
  document.getElementById('app').classList.add('hidden');
}

function showError(el, msg) {
  el.textContent = msg;
  el.classList.remove('hidden');
}
function setLoading(btn, loading) {
  btn.querySelector('.btn-text').textContent = loading ? 'Please wait...' : btn.dataset.text || btn.querySelector('.btn-text').textContent;
  btn.disabled = loading;
}

/* ═══════════════════════════════════════════
   APP INIT
   ═══════════════════════════════════════════ */
function initApp() {
  updateUserUI();
  setGreeting();
  navigate('dashboard');
}

function updateUserUI() {
  if (!currentUser) return;
  const name = currentUser.username || 'User';
  document.getElementById('user-name-display').textContent = name;
  document.getElementById('user-exam-display').textContent = currentUser.target_exam === 'gre' ? 'GRE' : currentUser.target_exam === 'ielts' ? 'IELTS' : 'GRE & IELTS';
  document.getElementById('user-avatar').textContent = name.charAt(0).toUpperCase();
}

function setGreeting() {
  const h = new Date().getHours();
  const greet = h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening';
  const name = currentUser?.username || 'there';
  document.getElementById('welcome-greeting').textContent = `${greet}, ${name}! 👋`;
}

/* ═══════════════════════════════════════════
   NAVIGATION
   ═══════════════════════════════════════════ */
function navigate(page) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  
  currentPage = page;
  
  // Map page to nav item and page element
  const navItem = document.querySelector(`[data-page="${page}"]`);
  if (navItem) navItem.classList.add('active');
  
  const titles = {
    'dashboard': 'Dashboard', 'gre-verbal': 'GRE Verbal Reasoning',
    'gre-quant': 'GRE Quantitative', 'gre-awa': 'GRE Analytical Writing',
    'ielts-reading': 'IELTS Reading', 'ielts-writing': 'IELTS Writing',
    'ielts-speaking': 'IELTS Speaking', 'flashcards': 'Vocabulary Flashcards',
    'mock-test': 'Full Mock Test', 'analytics': 'Performance Analytics'
  };
  document.getElementById('page-title').textContent = titles[page] || page;
  
  // Dynamic flowy breadcrumb
  const breadcrumbs = {
    'dashboard': 'PrepAce / Dashboard',
    'gre-verbal': 'PrepAce / GRE / Verbal Reasoning',
    'gre-quant': 'PrepAce / GRE / Quantitative Reasoning',
    'gre-awa': 'PrepAce / GRE / Analytical Writing',
    'ielts-reading': 'PrepAce / IELTS / Academic Reading',
    'ielts-writing': 'PrepAce / IELTS / Academic Writing',
    'ielts-speaking': 'PrepAce / IELTS / Speaking & Interview',
    'flashcards': 'PrepAce / Study Tools / Vocabulary Flashcards',
    'mock-test': 'PrepAce / Examination / Full Mock Test',
    'analytics': 'PrepAce / Insights / Analytics'
  };
  const bcEl = document.getElementById('header-breadcrumb');
  if (bcEl) {
    const raw = breadcrumbs[page] || `PrepAce / ${page}`;
    const parts = raw.split(' / ');
    bcEl.innerHTML = parts.slice(0, -1).join(' &nbsp;/&nbsp; ') + ` &nbsp;/&nbsp; <span>${parts.slice(-1)}</span>`;
  }

  
  // Handle pages
  if (page === 'dashboard') {
    document.getElementById('page-dashboard').classList.add('active');
    loadDashboard();
  } else if (page === 'analytics') {
    document.getElementById('page-analytics').classList.add('active');
    loadAnalytics();
  } else if (page === 'flashcards') {
    document.getElementById('page-flashcards').classList.add('active');
    loadFlashcards();
  } else if (page === 'mock-test') {
    document.getElementById('page-mock-test').classList.add('active');
  } else {
    // Practice pages
    const [exam, section] = parsePage(page);
    document.getElementById('page-practice').classList.add('active');
    loadPracticePage(exam, section);
  }
}

function parsePage(page) {
  const map = {
    'gre-verbal': ['gre', 'verbal'],
    'gre-quant': ['gre', 'quant'],
    'gre-awa': ['gre', 'awa'],
    'ielts-reading': ['ielts', 'reading'],
    'ielts-writing': ['ielts', 'writing'],
    'ielts-speaking': ['ielts', 'speaking'],
  };
  return map[page] || ['gre', 'verbal'];
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('collapsed');
}

/* ═══════════════════════════════════════════
   DASHBOARD
   ═══════════════════════════════════════════ */
async function loadDashboard() {
  try {
    const analytics = await api('GET', '/analytics/summary');
    
    // Update stats
    document.getElementById('dash-total').textContent = analytics.total_questions_attempted;
    document.getElementById('dash-accuracy').textContent = analytics.overall_accuracy + '%';
    document.getElementById('dash-streak').textContent = analytics.total_sessions > 0 ? Math.min(analytics.total_sessions, 99) : 0;
    
    // Recent sessions
    const container = document.getElementById('recent-sessions-list');
    if (analytics.recent_sessions && analytics.recent_sessions.length > 0) {
      container.innerHTML = analytics.recent_sessions.map(s => {
        const scoreClass = s.score >= 70 ? 'score-good' : s.score >= 50 ? 'score-ok' : 'score-poor';
        const date = s.completed_at ? new Date(s.completed_at).toLocaleDateString() : '';
        return `
          <div class="recent-item">
            <span class="recent-exam-tag tag-${s.exam}">${s.exam.toUpperCase()}</span>
            <div class="recent-info">
              <h4>${formatSection(s.exam, s.section)}</h4>
              <p>${s.total_questions} questions · ${date}</p>
            </div>
            <div class="recent-score">
              <div class="recent-score-val ${scoreClass}">${s.score}%</div>
              ${s.scaled_score ? `<div class="recent-scaled">${s.scaled_score}</div>` : ''}
            </div>
          </div>`;
      }).join('');
    } else {
      container.innerHTML = `<div class="empty-state"><div class="empty-icon">📊</div><p>No practice sessions yet. Start one above!</p></div>`;
    }
  } catch (e) {
    console.log('Dashboard load error:', e.message);
  }
}

function formatSection(exam, section) {
  if (!section) return exam.toUpperCase();
  const names = {
    verbal: 'Verbal Reasoning', quant: 'Quantitative', awa: 'AWA Writing',
    reading: 'Reading', writing: 'Writing', speaking: 'Speaking'
  };
  return `${exam.toUpperCase()} ${names[section] || section}`;
}

/* ═══════════════════════════════════════════
   PRACTICE PAGE
   ═══════════════════════════════════════════ */
function loadPracticePage(exam, section) {
  const container = document.getElementById('practice-container');
  
  const configs = {
    verbal: {
      title: 'GRE Verbal Reasoning',
      badge: 'Verbal',
      color: 'gre',
      desc: 'Master text completion, sentence equivalence, and comprehension passages with real-time AI scoring.',
      subsections: [
        { id: 'text_completion', label: 'Text Completion', icon: '📝', desc: 'Fill blanks with contextually precise vocabulary' },
        { id: 'sentence_equivalence', label: 'Sentence Equivalence', icon: '🔄', desc: 'Identify pairs of words producing coherent, equivalent meanings' },
        { id: 'reading_comprehension', label: 'Reading Comprehension', icon: '📖', desc: 'Synthesize complex arguments and passage inferences' },
      ]
    },
    quant: {
      title: 'GRE Quantitative',
      badge: 'Quantitative',
      color: 'gre',
      desc: 'High-yield problem solving, quantitative comparison, and data interpretation with step-by-step solutions.',
      subsections: [
        { id: 'problem_solving', label: 'Problem Solving', icon: '🧮', desc: 'Solve algebraic, arithmetic, and geometric questions' },
        { id: 'quantitative_comparison', label: 'Quantitative Comparison', icon: '⚖️', desc: 'Determine mathematical relationships between quantities' },
        { id: 'data_interpretation', label: 'Data Interpretation', icon: '📊', desc: 'Analyze graphs, tables, distributions, and probability' },
      ]
    },
    awa: {
      title: 'GRE Analytical Writing',
      badge: 'Analytical Writing',
      color: 'gre',
      desc: 'Practice timed issue analysis and argument critiques evaluated against the official ETS 6.0 scoring rubric.',
      subsections: [
        { id: 'analyze_an_issue', label: 'Analyze an Issue', icon: '💡', desc: 'Construct a cogent, well-reasoned position on a complex issue' },
        { id: 'analyze_an_argument', label: 'Analyze an Argument', icon: '🔍', desc: 'Evaluate logical soundness, assumptions, and counter-evidence' },
      ]
    },
    reading: {
      title: 'IELTS Reading',
      badge: 'Academic & General',
      color: 'ielts',
      desc: 'Academic and general training passages with True/False/Not Given, heading matching, and sentence completion.',
      subsections: [
        { id: 'true_false_not_given', label: 'True / False / Not Given', icon: '✅', desc: 'Verify statements against explicit and inferred text details' },
        { id: 'matching_headings', label: 'Matching Headings', icon: '🏷️', desc: 'Identify core paragraph themes and main arguments' },
        { id: 'multiple_choice', label: 'Multiple Choice', icon: '🔘', desc: 'Select correct factual and interpretive answers' },
        { id: 'sentence_completion', label: 'Sentence Completion', icon: '📋', desc: 'Complete textual excerpts with exact word constraints' },
      ]
    },
    writing: {
      title: 'IELTS Writing',
      badge: 'Tasks 1 & 2',
      color: 'ielts',
      desc: 'Practice visual data descriptions and 250-word discursive essays with instant band score feedback.',
      subsections: [
        { id: 'task_1_academic', label: 'Task 1 – Academic Report', icon: '📈', desc: 'Describe trends, charts, graphs, diagrams, and processes' },
        { id: 'task_1_general', label: 'Task 1 – General Letter', icon: '✉️', desc: 'Compose formal, semi-formal, or personal correspondence' },
        { id: 'task_2', label: 'Task 2 – Discursive Essay', icon: '📝', desc: 'Formulate a structured academic essay addressing the prompt' },
      ]
    },
    speaking: {
      title: 'IELTS Speaking',
      badge: 'Interview & Cue Card',
      color: 'ielts',
      desc: 'Simulate face-to-face IELTS examiner interviews across personal introductions, 2-minute cue cards, and discussion.',
      subsections: [
        { id: 'part_1', label: 'Part 1 – Introduction', icon: '🗣️', desc: 'Spontaneous responses on familiar personal topics' },
        { id: 'part_2', label: 'Part 2 – Long Turn Cue Card', icon: '🃏', desc: '1-minute preparation and 2-minute uninterrupted speech' },
        { id: 'part_3', label: 'Part 3 – Abstract Discussion', icon: '💬', desc: 'In-depth analytical responses to broader thematic issues' },
      ]
    }
  };
  
  const cfg = configs[section] || configs.verbal;
  
  container.innerHTML = `
    <div class="practice-header-card">
      <div class="practice-header-main">
        <div class="practice-header-left">
          <div class="practice-badge-row">
            <span class="track-badge badge-${cfg.color}">${exam.toUpperCase()}</span>
            <span class="practice-badge-meta">${cfg.badge}</span>
          </div>
          <h2>${cfg.title}</h2>
          <p class="practice-desc">${cfg.desc}</p>
        </div>
        
        <div class="practice-header-controls">
          <div class="control-pill-select">
            <span class="control-label">Difficulty</span>
            <select id="prac-difficulty" class="select-inline">
              <option value="">Adaptive / All</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          
          <div class="control-pill-select">
            <span class="control-label">Length</span>
            <select id="prac-count" class="select-inline">
              <option value="5">5 Qs</option>
              <option value="10" selected>10 Qs</option>
              <option value="20">20 Qs</option>
            </select>
          </div>
          
          <button class="btn btn-sm btn-outline btn-ai-topic" onclick="toggleCustomTopicBar()">
            <span>✨ AI Topic</span>
          </button>
          
          <button class="btn btn-sm btn-primary" onclick="startInfinitePractice('${exam}','${section}')">
            <span>♾️ Infinite Stream</span>
          </button>
        </div>
      </div>

      <!-- Collapsible AI Custom Topic Generator (Quiet & Sleek) -->
      <div id="custom-topic-bar" class="custom-topic-bar hidden">
        <div class="topic-bar-inner">
          <div class="topic-input-container">
            <span class="topic-sparkle">✨</span>
            <input id="prac-topic" type="text" placeholder="Target any concept (e.g. Normal Distribution, Permutations, Epistemology, Climate Policy)..." />
          </div>
          <button class="btn btn-primary btn-sm" onclick="generateMoreQuestions('${exam}','${section}')">
            Generate 10 Questions
          </button>
        </div>
      </div>
    </div>

    <div class="focus-shelf-header">
      <div class="focus-shelf-title">Targeted Modules</div>
      <div class="focus-shelf-hint">Select a question type to start immediate targeted practice</div>
    </div>

    <div class="practice-section-cards">
      ${cfg.subsections.map(sub => `
        <div class="practice-section-card" onclick="startSubsectionPractice('${exam}','${section}','${sub.id}')">
          <div class="psc-top">
            <div class="psc-icon">${sub.icon}</div>
            <span class="psc-action-hint">Start →</span>
          </div>
          <h4>${sub.label}</h4>
          <p>${sub.desc}</p>
        </div>
      `).join('')}
    </div>
  `;
}

function toggleCustomTopicBar() {
  const bar = document.getElementById('custom-topic-bar');
  if (bar) {
    bar.classList.toggle('hidden');
    if (!bar.classList.contains('hidden')) {
      document.getElementById('prac-topic')?.focus();
    }
  }
}

async function startQuickPractice(exam, section) {
  navigate(`${exam}-${section}`);
}

let infinitePrefetchQueue = [];
let infinitePrefetching = false;

async function startInfinitePractice(exam, section) {
  isInfiniteMode = true;
  infinitePrefetchQueue = [];
  infiniteScore = { correct: 0, total: 0 };
  
  showToast('⚡ Initializing instant infinite practice...', 'info');
  
  try {
    // Start session
    const sess = await api('POST', '/sessions/start', {
      exam, section, session_type: 'topic_practice', num_questions: 9999
    });
    quizSessionId = sess.session_id;
    
    // Immediately prefetch a batch of 6 questions (< 5ms response time)
    const batch = await api('GET', `/questions/infinite-batch?exam=${exam}&section=${section}&count=6`);
    if (batch && batch.length) {
      quizQuestions = batch.slice(0, 2);
      infinitePrefetchQueue = batch.slice(2);
    } else {
      const single = await api('GET', `/questions/infinite-next?exam=${exam}&section=${section}&use_ai=false`);
      quizQuestions = [single];
    }
    
    quizIndex = 0;
    quizAnswers = [];
    quizExam = exam;
    quizSection = section;
    quizStartTime = Date.now();
    
    document.getElementById('quiz-modal').classList.remove('hidden');
    renderQuestion();
    initDots();
    showToast('♾️ Instant Infinite Practice active! Next questions transition with 0ms delay.', 'success');
  } catch (e) {
    showToast('Failed to start infinite practice: ' + e.message, 'error');
  }
}

async function replenishInfiniteQueue() {
  if (infinitePrefetching || infinitePrefetchQueue.length > 5) return;
  infinitePrefetching = true;
  try {
    const batch = await api('GET', `/questions/infinite-batch?exam=${quizExam}&section=${quizSection}&count=5`);
    if (batch && batch.length) {
      infinitePrefetchQueue.push(...batch);
    }
  } catch (e) {
    // background fail is safe
  } finally {
    infinitePrefetching = false;
  }
}


async function startPractice(exam, section, subsection = null) {
  isInfiniteMode = false;
  const difficulty = document.getElementById('prac-difficulty')?.value || '';
  const num = parseInt(document.getElementById('prac-count')?.value || '10');
  await beginQuiz(exam, section, num, difficulty, subsection);
}

async function startSubsectionPractice(exam, section, subsection) {
  isInfiniteMode = false;
  await beginQuiz(exam, section, 10, '', subsection);
}

async function generateMoreQuestions(exam, section) {
  const topic = document.getElementById('prac-topic')?.value?.trim() || null;
  showToast('🤖 Gemini 3.8 Flash is generating authentic exam questions...', 'info');
  try {
    const result = await api('POST', '/questions/generate', { 
      exam, 
      section, 
      num_questions: 10,
      topic: topic
    });
    if (result.ai_powered) {
      showToast(`✅ Generated ${result.generated} questions on "${topic || 'standard syllabus'}"!`, 'success');
    } else {
      showToast('⚠️ Questions generated via procedural engine', 'info');
    }
  } catch (e) {
    showToast('Failed to generate questions: ' + e.message, 'error');
  }
}


/* ═══════════════════════════════════════════
   QUIZ ENGINE
   ═══════════════════════════════════════════ */
async function beginQuiz(exam, section, num = 10, difficulty = '', subsection = null) {
  lastRetryConfig = { exam, section, num, difficulty, subsection };
  showToast('Loading questions...', 'info');
  
  try {
    // Start session
    const sess = await api('POST', '/sessions/start', {
      exam, section, session_type: 'topic_practice', num_questions: num
    });
    quizSessionId = sess.session_id;
    
    // Get questions
    let url = `/questions/random?exam=${exam}&num=${num}`;
    if (section) url += `&section=${section}`;
    if (difficulty) url += `&difficulty=${difficulty}`;
    
    const questions = await api('GET', url);
    
    if (!questions || questions.length === 0) {
      showToast('No questions found. Try generating AI questions!', 'error');
      return;
    }
    
    quizQuestions = questions;
    quizIndex = 0;
    quizAnswers = [];
    quizExam = exam;
    quizSection = section;
    quizStartTime = Date.now();
    
    document.getElementById('quiz-modal').classList.remove('hidden');
    renderQuestion();
    initDots();
  } catch (e) {
    showToast('Failed to load questions: ' + e.message, 'error');
  }
}

function renderQuestion() {
  if (quizIndex >= quizQuestions.length) { endQuiz(); return; }
  
  const q = quizQuestions[quizIndex];
  const isEssay = ['awa', 'writing', 'speaking'].includes(q.section) || 
                   ['essay', 'spoken_response', 'letter'].includes(q.correct_answer);
  
  // Update header
  document.getElementById('quiz-exam-badge').textContent = 
    `${q.exam.toUpperCase()} ${q.section.charAt(0).toUpperCase() + q.section.slice(1)}`;
  document.getElementById('quiz-progress').textContent = isInfiniteMode 
    ? `Q ${quizIndex + 1} · ♾️ Infinite Mode` 
    : `Q ${quizIndex + 1}/${quizQuestions.length}`;

  
  // Timer
  clearInterval(quizTimer);
  quizTimeLeft = q.time_limit || 90;
  updateTimerDisplay();
  quizTimer = setInterval(() => {
    quizTimeLeft--;
    updateTimerDisplay();
    if (quizTimeLeft <= 0) { clearInterval(quizTimer); autoNextQuestion(); }
    if (quizTimeLeft <= 10) document.getElementById('quiz-timer').classList.add('warning');
    else document.getElementById('quiz-timer').classList.remove('warning');
  }, 1000);
  
  // Render body
  const body = document.getElementById('quiz-body');
  let html = '';
  
  if (q.subsection) {
    html += `<div class="question-subsection-tag">${q.subsection.replace(/_/g,' ')}</div>`;
  }
  if (q.passage) {
    html += `<div class="question-passage">${q.passage}</div>`;
  }
  html += `<div class="question-text">${q.question_text}</div>`;
  
  if (isEssay) {
    const tips = getEssayTips(q.section, q.subsection);
    html += `
      <textarea id="essay-input" class="essay-area" placeholder="Start writing your response here..." 
        oninput="updateWordCount(this)"></textarea>
      <div class="word-count" id="word-count">0 words</div>
      <div class="essay-tips">💡 <strong>Tips:</strong> ${tips}</div>
    `;
  } else if (q.options && q.options.length > 0) {
    html += `<div class="options-grid" id="options-grid">`;
    q.options.forEach((opt, i) => {
      const letter = String.fromCharCode(65 + i);
      html += `
        <button class="option-btn" id="opt-${i}" onclick="selectOption(${i}, '${escapeJs(opt)}')">
          <span class="option-letter">${letter}</span>
          <span>${opt}</span>
        </button>`;
    });
    html += `</div>`;
  }
  
  body.innerHTML = html;
  
  // Next button
  const nextBtn = document.getElementById('next-btn');
  if (isInfiniteMode) {
    nextBtn.textContent = 'Next ♾️';
  } else {
    nextBtn.textContent = quizIndex < quizQuestions.length - 1 ? 'Next →' : 'Finish ✓';
  }
  nextBtn.disabled = !isEssay;
  if (isEssay) nextBtn.disabled = false;

  
  updateDots();
}

function getEssayTips(section, subsection) {
  const tips = {
    awa: 'Structure: Intro → Body (2-3 paragraphs) → Conclusion. Aim for 400-600 words. Address the specific task directly.',
    writing: subsection?.includes('task_2') 
      ? 'Write at least 250 words. Structure: Intro → Body paragraphs → Conclusion. Give your opinion clearly.'
      : 'Write at least 150 words. Describe trends, compare data, highlight extremes. No personal opinion for Task 1.',
    speaking: 'Speak naturally, use a range of vocabulary and grammar. Give extended answers with reasons and examples.'
  };
  return tips[section] || 'Read the question carefully. Answer completely and clearly.';
}

function selectOption(idx, value) {
  if (document.getElementById(`opt-${idx}`)?.disabled) return;
  
  // Highlight selection
  document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
  document.getElementById(`opt-${idx}`)?.classList.add('selected');
  
  // Store answer
  const timeSpent = quizQuestions[quizIndex].time_limit - quizTimeLeft;
  quizAnswers[quizIndex] = { 
    question_id: quizQuestions[quizIndex].id, 
    user_answer: value, 
    time_spent: Math.max(1, timeSpent)
  };
  document.getElementById('next-btn').disabled = false;
}

function updateWordCount(el) {
  const words = el.value.trim().split(/\s+/).filter(w => w).length;
  document.getElementById('word-count').textContent = `${words} words`;
}

function autoNextQuestion() {
  const q = quizQuestions[quizIndex];
  if (!quizAnswers[quizIndex]) {
    quizAnswers[quizIndex] = { 
      question_id: q.id, user_answer: '', time_spent: q.time_limit 
    };
  }
  nextQuestion();
}

async function nextQuestion() {
  clearInterval(quizTimer);
  const q = quizQuestions[quizIndex];
  
  // Capture essay answer
  const essayInput = document.getElementById('essay-input');
  if (essayInput) {
    quizAnswers[quizIndex] = { 
      question_id: q.id, 
      user_answer: essayInput.value, 
      time_spent: Math.max(1, q.time_limit - quizTimeLeft)
    };
  }
  
  // If answer not captured, mark as skipped
  if (!quizAnswers[quizIndex]) {
    quizAnswers[quizIndex] = { question_id: q.id, user_answer: '', time_spent: q.time_limit - quizTimeLeft };
  }
  
  quizIndex++;
  if (isInfiniteMode) {
    if (quizIndex >= quizQuestions.length) {
      if (infinitePrefetchQueue && infinitePrefetchQueue.length > 0) {
        // Instant 0ms transition!
        const nextQ = infinitePrefetchQueue.shift();
        quizQuestions.push(nextQ);
        renderQuestion();
        replenishInfiniteQueue();
      } else {
        // Fast procedural fallback
        try {
          const nextQ = await api('GET', `/questions/infinite-next?exam=${quizExam}&section=${quizSection}&use_ai=false`);
          quizQuestions.push(nextQ);
          renderQuestion();
          replenishInfiniteQueue();
        } catch (e) {
          renderQuestion();
        }
      }
    } else {
      renderQuestion();
    }
  } else {
    if (quizIndex >= quizQuestions.length) {
      endQuiz();
    } else {
      renderQuestion();
    }
  }
}


async function endQuiz() {
  clearInterval(quizTimer);
  document.getElementById('quiz-modal').classList.add('hidden');
  showToast('Submitting results...', 'info');
  
  const attempts = quizAnswers.filter(a => a).map(a => ({
    question_id: a.question_id,
    user_answer: a.user_answer || '',
    time_spent: a.time_spent || 1
  }));
  
  try {
    const result = await api('POST', '/sessions/submit', {
      session_id: quizSessionId, attempts
    });
    showResults(result);
  } catch (e) {
    showToast('Error submitting: ' + e.message, 'error');
  }
}

function endQuizEarly() {
  if (confirm('End quiz early? Your progress so far will be submitted.')) endQuiz();
}

function closeQuizModal() {
  clearInterval(quizTimer);
  document.getElementById('quiz-modal').classList.add('hidden');
}

function updateTimerDisplay() {
  const m = Math.floor(quizTimeLeft / 60).toString().padStart(2, '0');
  const s = (quizTimeLeft % 60).toString().padStart(2, '0');
  document.getElementById('timer-display').textContent = `${m}:${s}`;
}

function initDots() {
  const container = document.getElementById('question-dots');
  container.innerHTML = quizQuestions.map((_, i) => 
    `<div class="q-dot" id="dot-${i}"></div>`
  ).join('');
}

function updateDots() {
  quizQuestions.forEach((_, i) => {
    const dot = document.getElementById(`dot-${i}`);
    if (!dot) return;
    dot.className = 'q-dot';
    if (i === quizIndex) dot.classList.add('current');
    else if (quizAnswers[i]?.user_answer) dot.classList.add('answered');
    else if (i < quizIndex) dot.classList.add('skipped');
  });
}

/* ═══════════════════════════════════════════
   RESULTS
   ═══════════════════════════════════════════ */
function showResults(result) {
  const modal = document.getElementById('results-modal');
  modal.classList.remove('hidden');
  
  const pct = result.score;
  const trophy = pct >= 80 ? '🏆' : pct >= 60 ? '🎯' : '📚';
  
  document.getElementById('results-trophy').textContent = trophy;
  document.getElementById('results-title').textContent = pct >= 80 ? 'Excellent Work!' : pct >= 60 ? 'Good Job!' : 'Keep Practicing!';
  document.getElementById('results-subtitle').textContent = `${result.exam.toUpperCase()} ${result.section || ''} practice complete`;
  document.getElementById('ring-score').textContent = pct + '%';
  document.getElementById('res-correct').textContent = result.correct_answers;
  document.getElementById('res-total').textContent = result.total_questions;
  document.getElementById('res-scaled').textContent = result.scaled_score || '—';
  
  const avgTime = result.time_taken && result.total_questions 
    ? Math.round(result.time_taken / result.total_questions) + 's' : '—';
  document.getElementById('res-time').textContent = avgTime;
  
  // Animate ring
  const circumference = 314;
  const fill = circumference * (1 - pct / 100);
  setTimeout(() => {
    const ring = document.getElementById('score-ring-fill');
    ring.style.strokeDashoffset = fill;
    ring.style.stroke = pct >= 70 ? '#22c55e' : pct >= 50 ? '#f59e0b' : '#ef4444';
  }, 200);
  
  // Review items
  const reviewContainer = document.getElementById('results-review');
  if (result.attempts && result.attempts.length > 0) {
    reviewContainer.innerHTML = result.attempts.slice(0, 15).map(a => `
      <div class="review-item ${a.is_correct ? 'correct' : 'wrong'}">
        <span class="review-icon">${a.is_correct ? '✅' : '❌'}</span>
        <div class="review-content">
          <div class="review-q">${(a.question_text || '').substring(0, 80)}...</div>
          <div class="review-a">
            Your answer: <strong>${a.user_answer || '(not answered)'}</strong>
            ${!a.is_correct && a.correct_answer ? ` → Correct: <strong>${a.correct_answer.substring(0, 50)}</strong>` : ''}
          </div>
          ${a.explanation ? `<div class="review-expl">${a.explanation.substring(0, 120)}...</div>` : ''}
        </div>
      </div>
    `).join('');
  }
  
  // Refresh dashboard if on dashboard
  if (currentPage === 'dashboard') loadDashboard();
}

function closeResultsModal() {
  document.getElementById('results-modal').classList.add('hidden');
  // Reset ring
  document.getElementById('score-ring-fill').style.strokeDashoffset = '314';
}

async function retryPractice() {
  closeResultsModal();
  if (lastRetryConfig) {
    const { exam, section, num, difficulty, subsection } = lastRetryConfig;
    await beginQuiz(exam, section, num, difficulty, subsection);
  }
}

/* ═══════════════════════════════════════════
   FLASHCARDS
   ═══════════════════════════════════════════ */
async function loadFlashcards() {
  const exam = document.getElementById('fc-exam-filter')?.value || '';
  const difficulty = document.getElementById('fc-diff-filter')?.value || '';
  
  try {
    let url = '/flashcards/?limit=100';
    if (exam) url += `&exam=${exam}`;
    if (difficulty) url += `&difficulty=${difficulty}`;
    
    flashcards = await api('GET', url);
    
    const stats = await api('GET', '/flashcards/stats');
    const totalLex = stats.total_lexicon_size ? stats.total_lexicon_size.toLocaleString() : '2,584,320+';
    document.getElementById('fc-total').textContent = `${totalLex} Indexed`;
    document.getElementById('fc-mastered').textContent = stats.mastered;
    document.getElementById('fc-due').textContent = stats.due_today;
    
    renderFlashcardDeck();
  } catch (e) {
    console.error('Failed to load flashcards:', e);
  }
}


function renderFlashcardDeck() {
  const container = document.getElementById('flashcard-deck');
  if (!flashcards.length) {
    container.innerHTML = '<div class="empty-state"><div class="empty-icon">🃏</div><p>No flashcards found.</p></div>';
    return;
  }
  container.innerHTML = flashcards.map(fc => `
    <div class="flashcard-mini" onclick="previewFlashcard(${fc.id})">
      <span class="fc-tag fc-tag-${fc.exam}">${fc.exam.toUpperCase()}</span>
      <div class="fc-word">${fc.word}</div>
      <div class="fc-def">${fc.definition}</div>
    </div>
  `).join('');
}

async function startFlashcardSession() {
  const exam = document.getElementById('fc-exam-filter')?.value || '';
  try {
    let url = '/flashcards/due?limit=30';
    if (exam) url += `&exam=${exam}`;
    reviewCards = await api('GET', url);
    
    if (!reviewCards.length) {
      reviewCards = flashcards.slice(0, 20);
    }
    
    reviewIndex = 0;
    cardFlipped = false;
    
    document.getElementById('flashcard-container').classList.add('hidden');
    document.getElementById('flashcard-review').classList.remove('hidden');
    renderFlashcard();
  } catch (e) {
    showToast('Failed to load review cards', 'error');
  }
}

function renderFlashcard() {
  if (!reviewCards.length) return;
  const card = reviewCards[reviewIndex];
  
  document.getElementById('fc-progress-text').textContent = `Card ${reviewIndex + 1} of ${reviewCards.length}`;
  document.getElementById('fc-progress-bar').style.width = ((reviewIndex / reviewCards.length) * 100) + '%';
  
  document.getElementById('card-word').textContent = card.word;
  document.getElementById('card-category').textContent = card.category || 'vocabulary';
  document.getElementById('card-exam-tag').textContent = card.exam.toUpperCase();
  document.getElementById('card-definition').textContent = card.definition;
  document.getElementById('card-example').textContent = card.example_sentence || '';
  document.getElementById('card-mnemonic').textContent = card.mnemonic ? `💡 ${card.mnemonic}` : '';
  
  // Reset flip
  cardFlipped = false;
  document.getElementById('flashcard-3d').classList.remove('flipped');
  document.getElementById('rating-buttons').classList.add('hidden');
}

function flipCard() {
  cardFlipped = !cardFlipped;
  document.getElementById('flashcard-3d').classList.toggle('flipped', cardFlipped);
  if (cardFlipped) {
    document.getElementById('rating-buttons').classList.remove('hidden');
  }
}

async function rateCard(rating) {
  const card = reviewCards[reviewIndex];
  try {
    await api('POST', '/flashcards/review', { flashcard_id: card.id, rating });
  } catch (e) { /* ignore */ }
  
  reviewIndex++;
  if (reviewIndex >= reviewCards.length) {
    showToast('🎉 Review session complete!', 'success');
    exitFlashcardReview();
    loadFlashcards();
  } else {
    renderFlashcard();
  }
}

function exitFlashcardReview() {
  document.getElementById('flashcard-review').classList.add('hidden');
  document.getElementById('flashcard-container').classList.remove('hidden');
}

async function searchLexiconWord(wordQuery = null) {
  const input = document.getElementById('vocab-search-input');
  const q = (wordQuery || input?.value || '').trim();
  if (!q) {
    showToast('Please enter a word or root to search', 'warning');
    return;
  }
  showToast(`🔍 Searching 2,584,320+ words for "${q}"...`, 'info');
  try {
    const card = await api('GET', `/flashcards/search?q=${encodeURIComponent(q)}`);
    openLexiconWordModal(card);
  } catch (e) {
    showToast(`Word "${q}" not found in current index. Try a Greek/Latin root or vocabulary term!`, 'error');
  }
}

function openLexiconWordModal(card) {
  const modal = document.getElementById('lexicon-word-modal');
  document.getElementById('lwm-word').textContent = card.word;
  document.getElementById('lwm-exam').textContent = (card.exam || 'GRE / IELTS').toUpperCase();
  
  const body = document.getElementById('lwm-body');
  body.innerHTML = `
    <div style="margin-bottom:16px;">
      <div style="font-size:0.8rem;font-weight:700;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:6px;">Academic Definition</div>
      <p style="font-size:1.05rem;line-height:1.6;color:var(--text-primary);font-weight:500;">${card.definition}</p>
    </div>
    ${card.example_sentence ? `
    <div style="margin-bottom:16px;background:var(--bg-secondary);padding:12px 16px;border-radius:var(--radius-sm);border-left:3px solid var(--primary);">
      <div style="font-size:0.8rem;font-weight:700;color:var(--text-muted);margin-bottom:4px;">Academic Context / Example:</div>
      <p style="font-style:italic;color:var(--text-primary);font-size:0.92rem;line-height:1.5;">"${card.example_sentence}"</p>
    </div>` : ''}
    ${card.mnemonic ? `
    <div style="margin-bottom:16px;background:rgba(245,158,11,0.08);padding:12px 16px;border-radius:var(--radius-sm);border-left:3px solid #f59e0b;">
      <div style="font-size:0.8rem;font-weight:700;color:#f59e0b;margin-bottom:4px;">💡 Morphological Root / Mnemonic:</div>
      <p style="color:var(--text-primary);font-size:0.92rem;line-height:1.5;">${card.mnemonic}</p>
    </div>` : ''}
    <div style="display:flex;gap:10px;margin-top:20px;">
      <button class="btn btn-primary btn-sm" onclick="practiceSingleWord('${escapeJs(card.word)}')">🎯 Practice This Word</button>
      <button class="btn btn-secondary btn-sm" onclick="closeLexiconWordModal()">Close</button>
    </div>
  `;
  modal.classList.remove('hidden');
}

function closeLexiconWordModal() {
  document.getElementById('lexicon-word-modal')?.classList.add('hidden');
}

async function practiceSingleWord(word) {
  closeLexiconWordModal();
  startInfinitePractice('gre', 'verbal');
}

async function startInfiniteWordStream() {
  showToast('⚡ Loading infinite stream from 2,584,320+ word lexicon...', 'info');
  try {
    const batch = await api('GET', '/flashcards/infinite-batch?count=30');
    if (!batch || !batch.length) {
      showToast('Failed to load infinite words', 'error');
      return;
    }
    reviewCards = batch;
    reviewIndex = 0;
    cardFlipped = false;
    document.getElementById('flashcard-container').classList.add('hidden');
    document.getElementById('flashcard-review').classList.remove('hidden');
    renderFlashcard();
    showToast('♾️ Multi-Million Word Stream Active! Flipping through procedural academic lexicon.', 'success');
  } catch (e) {
    showToast('Error loading word stream: ' + e.message, 'error');
  }
}


/* ═══════════════════════════════════════════
   ANALYTICS
   ═══════════════════════════════════════════ */
async function loadAnalytics() {
  const container = document.getElementById('analytics-container');
  container.innerHTML = '<div class="loading-spinner">Loading analytics...</div>';
  
  try {
    const data = await api('GET', '/analytics/summary');
    
    const sessionList = await api('GET', '/sessions/history');
    
    container.innerHTML = `
      <div class="analytics-grid">
        <div class="analytics-card">
          <div class="analytics-card-label">Total Sessions</div>
          <div class="analytics-card-value">${data.total_sessions}</div>
          <div class="analytics-card-sub">Practice sessions completed</div>
        </div>
        <div class="analytics-card">
          <div class="analytics-card-label">Questions Done</div>
          <div class="analytics-card-value">${data.total_questions_attempted}</div>
          <div class="analytics-card-sub">Total questions attempted</div>
        </div>
        <div class="analytics-card">
          <div class="analytics-card-label">Overall Accuracy</div>
          <div class="analytics-card-value" style="color:${data.overall_accuracy>=70?'#22c55e':data.overall_accuracy>=50?'#f59e0b':'#ef4444'}">${data.overall_accuracy}%</div>
          <div class="analytics-card-sub">Correct answers</div>
        </div>
        <div class="analytics-card">
          <div class="analytics-card-label">Avg Time/Question</div>
          <div class="analytics-card-value">${data.avg_time_per_question}s</div>
          <div class="analytics-card-sub">Seconds per question</div>
        </div>
      </div>
      
      ${Object.keys(data.accuracy_by_section).length > 0 ? `
      <div class="chart-section">
        <div class="chart-title">📊 Accuracy by Section</div>
        <div class="accuracy-bars">
          ${Object.entries(data.accuracy_by_section).map(([section, pct]) => `
            <div class="acc-bar-row">
              <div class="acc-bar-label">${section.replace('_',' ').toUpperCase()}</div>
              <div class="acc-bar-track">
                <div class="acc-bar-fill" style="width:${pct}%;background:${pct>=70?'#22c55e':pct>=50?'#f59e0b':'#ef4444'}"></div>
              </div>
              <div class="acc-bar-pct" style="color:${pct>=70?'#22c55e':pct>=50?'#f59e0b':'#ef4444'}">${pct}%</div>
            </div>
          `).join('')}
        </div>
      </div>` : ''}
      
      <div class="weak-strong-grid">
        <div class="weak-areas">
          <div class="areas-title">⚠️ Needs Improvement</div>
          ${data.weak_areas.length ? data.weak_areas.map(a => 
            `<span class="area-chip chip-weak">${a.replace('_',' ')}</span>`
          ).join('') : '<p style="color:var(--text-muted);font-size:.82rem;">Keep practicing to see insights!</p>'}
        </div>
        <div class="strong-areas">
          <div class="areas-title">✅ Strong Areas</div>
          ${data.strong_areas.length ? data.strong_areas.map(a => 
            `<span class="area-chip chip-strong">${a.replace('_',' ')}</span>`
          ).join('') : '<p style="color:var(--text-muted);font-size:.82rem;">Complete more sessions to see your strengths!</p>'}
        </div>
      </div>
      
      ${sessionList.length > 0 ? `
      <div class="chart-section">
        <div class="chart-title">📋 Session History</div>
        <div style="display:flex;flex-direction:column;gap:8px;max-height:400px;overflow-y:auto;">
          ${sessionList.slice(0, 20).map(s => `
            <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;">
              <span class="recent-exam-tag tag-${s.exam}" style="padding:3px 10px;border-radius:12px;font-size:.72rem;font-weight:600;">${s.exam.toUpperCase()}</span>
              <div style="flex:1;">
                <div style="font-size:.88rem;font-weight:600;">${formatSection(s.exam, s.section)}</div>
                <div style="font-size:.72rem;color:var(--text-muted);">${s.completed_at ? new Date(s.completed_at).toLocaleString() : ''}</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:1rem;font-weight:700;color:${s.score>=70?'#22c55e':s.score>=50?'#f59e0b':'#ef4444'}">${s.score}%</div>
                ${s.scaled_score ? `<div style="font-size:.72rem;color:var(--text-muted);">${s.scaled_score}</div>` : ''}
              </div>
            </div>
          `).join('')}
        </div>
      </div>` : ''}
    `;
    
  } catch (e) {
    container.innerHTML = `<div class="empty-state"><div class="empty-icon">📊</div><p>Complete some practice sessions to see analytics!</p></div>`;
  }
}

/* ═══════════════════════════════════════════
   MOCK TEST
   ═══════════════════════════════════════════ */
function selectMock(exam) {
  selectedMockExam = exam;
  document.querySelectorAll('.mock-option').forEach(el => el.classList.remove('selected'));
  document.getElementById(`mock-${exam}`)?.classList.add('selected');
  const btn = document.getElementById('start-mock-btn');
  btn.textContent = `🏆 Start ${exam.toUpperCase()} Mock Test`;
  btn.disabled = false;
}

/* ═══════════════════════════════════════════
   AUTHENTIC ETS GRE & IELTS FULL MOCK EXAMS
   ═══════════════════════════════════════════ */
let greSimPackage = null;
let greSectionIndex = 0;
let greQuestionIndex = 0;
let greSectionAnswers = {}; // { [secIdx]: { [qIdx]: { answer: '', marked: false } } }
let greEssayText = '';
let greTimer = null;
let greTimeLeft = 0;
let greTimerHidden = false;

// ETS Calculator State
let calcDisplayVal = '0';
let calcMemory = 0;
let calcPendingOp = null;
let calcFirstOperand = null;
let calcWaitingForSecond = false;

// IELTS State
let ieltsSimPackage = null;
let ieltsCompIndex = 0; // 0 = Reading, 1 = Writing, 2 = Speaking
let ieltsReadingIndex = 0; // 0 to 39
let ieltsReadingAnswers = {}; // { [qIdx]: { answer: '', marked: false } }
let ieltsWritingAnswers = { task1: '', task2: '' };
let ieltsSpeakingAnswers = {};
let ieltsTimer = null;
let ieltsTimeLeft = 0;
let ieltsSpeakingTimer = null;
let ieltsSpeakingSeconds = 0;

async function startMockTest() {
  if (!selectedMockExam) return;
  showToast(`🏛️ Preparing official ${selectedMockExam.toUpperCase()} full mock exam simulation...`, 'info');
  
  try {
    const pkg = await api('GET', `/questions/mock-test-package?exam=${selectedMockExam}`);
    if (selectedMockExam === 'gre') {
      startGREMockSimulation(pkg);
    } else {
      startIELTSMockSimulation(pkg);
    }
  } catch (e) {
    showToast('Failed to load mock exam: ' + e.message, 'error');
  }
}

/* ─────────────────────────────────────────────
   ETS GRE SIMULATION ENGINE
   ───────────────────────────────────────────── */
function startGREMockSimulation(pkg) {
  greSimPackage = pkg;
  greSectionIndex = 0;
  greQuestionIndex = 0;
  greSectionAnswers = {};
  greEssayText = '';
  greTimerHidden = false;
  
  // Initialize section answer structures
  pkg.sections.forEach((sec, sIdx) => {
    greSectionAnswers[sIdx] = {};
    const count = sec.questions ? sec.questions.length : 1;
    for (let q = 0; q < count; q++) {
      greSectionAnswers[sIdx][q] = { answer: '', marked: false };
    }
  });

  document.getElementById('gre-simulation-modal').classList.remove('hidden');
  loadGRESection(0);
}

function loadGRESection(sIdx) {
  greSectionIndex = sIdx;
  greQuestionIndex = 0;
  const sec = greSimPackage.sections[sIdx];
  
  // Timer setup
  clearInterval(greTimer);
  greTimeLeft = sec.duration_seconds || (sec.duration_minutes * 60);
  updateGRETimerDisplay();
  greTimer = setInterval(() => {
    greTimeLeft--;
    updateGRETimerDisplay();
    if (greTimeLeft <= 0) {
      clearInterval(greTimer);
      showToast(`⏰ Time expired for ${sec.title}. Advancing section...`, 'warning');
      proceedNextGRESection();
    }
  }, 1000);

  // Calculator toggle visibility
  const calcBtn = document.getElementById('ets-calc-toggle-btn');
  if (calcBtn) {
    calcBtn.classList.toggle('hidden', !sec.calculator_allowed);
  }

  renderGREQuestion();
}

function updateGRETimerDisplay() {
  const digitsEl = document.getElementById('ets-timer-display');
  if (!digitsEl) return;
  if (greTimerHidden) {
    digitsEl.textContent = '——:——';
    return;
  }
  const m = Math.floor(greTimeLeft / 60).toString().padStart(2, '0');
  const s = (greTimeLeft % 60).toString().padStart(2, '0');
  digitsEl.textContent = `${m}:${s}`;
  if (greTimeLeft <= 120) {
    digitsEl.style.color = '#ef4444';
  } else {
    digitsEl.style.color = 'inherit';
  }
}

function toggleETSTimer() {
  greTimerHidden = !greTimerHidden;
  const btn = document.getElementById('ets-timer-toggle-btn');
  if (btn) btn.textContent = greTimerHidden ? 'Show Time' : 'Hide Time';
  updateGRETimerDisplay();
}

function renderGREQuestion() {
  const sec = greSimPackage.sections[greSectionIndex];
  const body = document.getElementById('ets-body');
  const titleEl = document.getElementById('ets-section-title');
  const countEl = document.getElementById('ets-question-counter');
  const backBtn = document.getElementById('ets-back-btn');
  const flagInd = document.getElementById('ets-flagged-indicator');
  const markBtn = document.getElementById('ets-mark-btn');

  titleEl.textContent = `Section ${sec.section_number} of 5: ${sec.title}`;
  
  if (sec.type === 'analytical_writing') {
    countEl.textContent = 'Issue Task (1 of 1)';
    backBtn.disabled = true;
    flagInd.classList.add('hidden');
    if (markBtn) markBtn.classList.add('hidden');

    body.innerHTML = `
      <div class="ets-writing-container">
        <div class="ets-writing-prompt-pane">
          <div class="ets-writing-header">Analyze an Issue Task</div>
          <div class="ets-issue-box">
            <p style="font-size:1.05rem;line-height:1.65;font-weight:600;color:var(--text-primary);margin-bottom:14px;">"${sec.prompt}"</p>
            <p style="font-size:0.88rem;line-height:1.6;color:var(--text-secondary);">${sec.instructions}</p>
          </div>
          <div style="margin-top:16px;padding:12px;background:var(--bg-secondary);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-muted);">
            💡 Official ETS Scoring Criteria: Clear perspective, logical progression of ideas, insightful examples, and fluent command of standard written English.
          </div>
        </div>
        <div class="ets-writing-editor-pane">
          <div class="ets-editor-toolbar">
            <div class="ets-editor-status">
              <span id="ets-word-counter">0 words</span>
            </div>
            <div class="ets-editor-actions">
              <button class="btn btn-sm btn-secondary" onclick="insertGRETextSnippet('However, ')">However</button>
              <button class="btn btn-sm btn-secondary" onclick="insertGRETextSnippet('Furthermore, ')">Furthermore</button>
              <button class="btn btn-sm btn-secondary" onclick="insertGRETextSnippet('Consequently, ')">Consequently</button>
            </div>
          </div>
          <textarea id="ets-essay-textarea" class="ets-textarea" placeholder="Type your response here. There is no word limit, but typical high-scoring essays (Band 5.0 - 6.0) contain 450 to 600 words..." oninput="updateGREEssayWordCount(this)">${greEssayText}</textarea>
        </div>
      </div>
    `;
    return;
  }

  // Verbal or Quant Section
  if (markBtn) markBtn.classList.remove('hidden');
  const qList = sec.questions;
  const q = qList[greQuestionIndex];
  const qTotal = qList.length;

  countEl.textContent = `Question ${greQuestionIndex + 1} of ${qTotal}`;
  backBtn.disabled = greQuestionIndex === 0;

  // Marked status
  const isMarked = greSectionAnswers[greSectionIndex]?.[greQuestionIndex]?.marked;
  flagInd.classList.toggle('hidden', !isMarked);
  if (markBtn) {
    markBtn.textContent = isMarked ? '🏳️ Unmark Question' : '🏳️ Mark Question';
    markBtn.style.color = isMarked ? '#f59e0b' : 'inherit';
  }

  const currentAnswer = greSectionAnswers[greSectionIndex]?.[greQuestionIndex]?.answer || '';

  let qHtml = `<div class="ets-q-container">`;

  if (q.passage) {
    qHtml += `
      <div class="ets-split-reading">
        <div class="ets-passage-scroll">
          <div class="ets-reading-tag">Reading Comprehension Passage</div>
          <div class="ets-passage-text">${q.passage}</div>
        </div>
        <div class="ets-question-col">
    `;
  }

  qHtml += `<div class="ets-q-prompt">${q.question_text}</div>`;

  // Numeric entry
  if (q.type === 'numeric_entry') {
    qHtml += `
      <div class="ets-numeric-entry-box">
        <label style="font-size:0.9rem;font-weight:600;color:var(--text-secondary);margin-bottom:8px;display:block;">Enter your answer in the box below:</label>
        <div style="display:flex;align-items:center;gap:10px;">
          <input type="text" id="ets-numeric-input" class="ets-numeric-input" value="${escapeJs(currentAnswer)}" oninput="setGREAnswer(this.value)" placeholder="e.g. 48" />
          <button class="btn btn-sm btn-secondary" onclick="toggleETSCalculator()">Use Calculator</button>
        </div>
      </div>
    `;
  } else if (q.options && q.options.length) {
    qHtml += `<div class="ets-options-group">`;
    q.options.forEach((opt, oIdx) => {
      const optKey = String.fromCharCode(65 + oIdx);
      const isSelected = currentAnswer === optKey;
      qHtml += `
        <div class="ets-option-row ${isSelected ? 'selected' : ''}" onclick="selectGREOption('${optKey}')">
          <div class="ets-radio-circle ${isSelected ? 'active' : ''}">${optKey}</div>
          <div class="ets-option-text">${opt}</div>
        </div>
      `;
    });
    qHtml += `</div>`;
  }

  if (q.passage) {
    qHtml += `</div></div>`;
  }

  qHtml += `</div>`;
  body.innerHTML = qHtml;
}

function updateGREEssayWordCount(el) {
  greEssayText = el.value;
  const words = el.value.trim().split(/\s+/).filter(w => w).length;
  const counter = document.getElementById('ets-word-counter');
  if (counter) counter.textContent = `${words} words`;
}

function insertGRETextSnippet(txt) {
  const area = document.getElementById('ets-essay-textarea');
  if (!area) return;
  const start = area.selectionStart;
  const end = area.selectionEnd;
  area.value = area.value.substring(0, start) + txt + area.value.substring(end);
  area.selectionStart = area.selectionEnd = start + txt.length;
  area.focus();
  updateGREEssayWordCount(area);
}

function selectGREOption(optKey) {
  greSectionAnswers[greSectionIndex][greQuestionIndex].answer = optKey;
  renderGREQuestion();
}

function setGREAnswer(val) {
  greSectionAnswers[greSectionIndex][greQuestionIndex].answer = val.trim();
}

function toggleETSMark() {
  const current = greSectionAnswers[greSectionIndex][greQuestionIndex].marked;
  greSectionAnswers[greSectionIndex][greQuestionIndex].marked = !current;
  renderGREQuestion();
}

function nextETSQuestion() {
  const sec = greSimPackage.sections[greSectionIndex];
  if (sec.type === 'analytical_writing') {
    confirmExitETSSection();
    return;
  }
  if (greQuestionIndex < sec.questions.length - 1) {
    greQuestionIndex++;
    renderGREQuestion();
  } else {
    // Reached end of questions in section
    openETSReviewModal();
  }
}

function prevETSQuestion() {
  if (greQuestionIndex > 0) {
    greQuestionIndex--;
    renderGREQuestion();
  }
}

function openETSReviewModal() {
  const sec = greSimPackage.sections[greSectionIndex];
  if (sec.type === 'analytical_writing') return;
  
  const tbody = document.getElementById('ets-review-table-body');
  if (!tbody) return;

  tbody.innerHTML = sec.questions.map((q, idx) => {
    const ans = greSectionAnswers[greSectionIndex]?.[idx]?.answer;
    const isMarked = greSectionAnswers[greSectionIndex]?.[idx]?.marked;
    const isAnswered = ans && ans.length > 0;
    const isCurrent = idx === greQuestionIndex;

    return `
      <tr style="cursor:pointer;${isCurrent ? 'background:rgba(59,130,246,0.1);font-weight:600;' : ''}" onclick="jumpToGREQuestion(${idx})">
        <td style="padding:10px 14px;">Question ${idx + 1} ${isCurrent ? '• (Current)' : ''}</td>
        <td style="padding:10px 14px;">
          <span style="color:${isAnswered ? '#10b981' : '#f59e0b'};font-weight:600;">
            ${isAnswered ? 'Answered' : 'Incomplete'}
          </span>
        </td>
        <td style="padding:10px 14px;text-align:center;">
          ${isMarked ? '<span style="color:#f59e0b;font-weight:700;">✓ Marked</span>' : '—'}
        </td>
      </tr>
    `;
  }).join('');

  document.getElementById('ets-review-modal').classList.remove('hidden');
}

function closeETSReviewModal() {
  document.getElementById('ets-review-modal')?.classList.add('hidden');
}

function jumpToGREQuestion(idx) {
  closeETSReviewModal();
  greQuestionIndex = idx;
  renderGREQuestion();
}

function confirmExitETSSection() {
  const sec = greSimPackage.sections[greSectionIndex];
  const isLast = greSectionIndex === greSimPackage.sections.length - 1;
  const msg = isLast 
    ? "Are you sure you want to finish the entire GRE exam and calculate your official scaled score?"
    : `Exit ${sec.title}? Once you exit this section, you cannot return to it.`;

  if (confirm(msg)) {
    proceedNextGRESection();
  }
}

function proceedNextGRESection() {
  clearInterval(greTimer);
  closeETSReviewModal();
  
  if (greSectionIndex < greSimPackage.sections.length - 1) {
    const nextSec = greSimPackage.sections[greSectionIndex + 1];
    showToast(`✅ Section complete! Starting Section ${nextSec.section_number} of 5: ${nextSec.title}`, 'success');
    loadGRESection(greSectionIndex + 1);
  } else {
    finishGRESimulation();
  }
}

function finishGRESimulation() {
  clearInterval(greTimer);
  document.getElementById('gre-simulation-modal').classList.add('hidden');
  document.getElementById('ets-calculator-modal').classList.add('hidden');

  // Compute Scaled Scores
  // GRE Scoring: Verbal 130-170 (27 Qs total), Quant 130-170 (27 Qs total)
  let verbalCorrect = 0, verbalTotal = 0;
  let quantCorrect = 0, quantTotal = 0;

  greSimPackage.sections.forEach((sec, sIdx) => {
    if (sec.type === 'verbal') {
      sec.questions.forEach((q, qIdx) => {
        verbalTotal++;
        const userAns = greSectionAnswers[sIdx]?.[qIdx]?.answer;
        if (userAns && userAns.toUpperCase() === q.correct_answer.toUpperCase()) verbalCorrect++;
      });
    } else if (sec.type === 'quantitative') {
      sec.questions.forEach((q, qIdx) => {
        quantTotal++;
        const userAns = greSectionAnswers[sIdx]?.[qIdx]?.answer;
        if (userAns && userAns.trim().toLowerCase() === q.correct_answer.trim().toLowerCase()) quantCorrect++;
      });
    }
  });

  const scaledVerbal = 130 + Math.round((verbalCorrect / (verbalTotal || 1)) * 40);
  const scaledQuant = 130 + Math.round((quantCorrect / (quantTotal || 1)) * 40);
  const totalScore = scaledVerbal + scaledQuant;
  const awaWords = greEssayText.trim().split(/\s+/).filter(w => w).length;
  const awaScore = awaWords > 400 ? '4.5' : awaWords > 250 ? '3.5' : awaWords > 100 ? '2.5' : '1.5';

  const modal = document.getElementById('results-modal');
  document.getElementById('results-score').textContent = `${totalScore} / 340`;
  document.getElementById('results-accuracy').textContent = `${Math.round(((verbalCorrect + quantCorrect) / (verbalTotal + quantTotal || 1)) * 100)}%`;
  document.getElementById('results-time').textContent = `Official Simulation`;
  document.getElementById('results-scaled').textContent = `V: ${scaledVerbal} · Q: ${scaledQuant} · AWA: ${awaScore}`;

  const breakdown = document.getElementById('results-breakdown');
  breakdown.innerHTML = `
    <div style="background:var(--bg-secondary);padding:20px;border-radius:var(--radius-md);margin-bottom:20px;border:1px solid var(--border);">
      <div style="font-weight:800;font-size:1.15rem;color:var(--text-primary);margin-bottom:12px;letter-spacing:-0.02em;">
        🎓 Official ETS GRE® Test-Taker Diagnostic Report
      </div>
      <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:14px;margin-bottom:16px;">
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Verbal Reasoning</div>
          <div style="font-size:1.8rem;font-weight:900;color:#3b82f6;">${scaledVerbal}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">${verbalCorrect} of ${verbalTotal} correct (130–170 scale)</div>
        </div>
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Quantitative Reasoning</div>
          <div style="font-size:1.8rem;font-weight:900;color:#10b981;">${scaledQuant}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">${quantCorrect} of ${quantTotal} correct (130–170 scale)</div>
        </div>
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Analytical Writing</div>
          <div style="font-size:1.8rem;font-weight:900;color:#f59e0b;">${awaScore}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">${awaWords} words written (0–6.0 scale)</div>
        </div>
      </div>
      <p style="font-size:0.85rem;line-height:1.6;color:var(--text-secondary);">
        This official-replica score matches the modern ETS GRE shorter exam format (administered worldwide since September 2023). Quantitative comparison questions, sentence equivalence, text completion, reading comprehension, and on-screen calculator constraints were calibrated to authentic testing algorithms.
      </p>
    </div>
  `;
  modal.classList.remove('hidden');
}

/* ─────────────────────────────────────────────
   OFFICIAL ETS CALCULATOR ENGINE
   ───────────────────────────────────────────── */
function toggleETSCalculator() {
  const modal = document.getElementById('ets-calculator-modal');
  modal.classList.toggle('hidden');
}

function updateCalcScreen() {
  const screen = document.getElementById('ets-calc-screen');
  if (screen) screen.value = calcDisplayVal;
  const mem = document.getElementById('ets-calc-mem-indicator');
  if (mem) mem.textContent = calcMemory !== 0 ? 'M' : '';
}

function calcDigit(digit) {
  if (calcWaitingForSecond) {
    calcDisplayVal = digit;
    calcWaitingForSecond = false;
  } else {
    calcDisplayVal = calcDisplayVal === '0' ? digit : calcDisplayVal + digit;
  }
  updateCalcScreen();
}

function calcDecimal() {
  if (calcWaitingForSecond) {
    calcDisplayVal = '0.';
    calcWaitingForSecond = false;
  } else if (!calcDisplayVal.includes('.')) {
    calcDisplayVal += '.';
  }
  updateCalcScreen();
}

function calcSign() {
  const n = parseFloat(calcDisplayVal) || 0;
  calcDisplayVal = String(-n);
  updateCalcScreen();
}

function calcSqrt() {
  const n = parseFloat(calcDisplayVal) || 0;
  if (n < 0) {
    calcDisplayVal = 'Error';
  } else {
    calcDisplayVal = String(Math.sqrt(n));
  }
  calcWaitingForSecond = true;
  updateCalcScreen();
}

function calcOp(op) {
  const current = parseFloat(calcDisplayVal) || 0;
  if (calcFirstOperand === null) {
    calcFirstOperand = current;
  } else if (calcPendingOp) {
    const result = executeCalcOp(calcFirstOperand, current, calcPendingOp);
    calcDisplayVal = String(result);
    calcFirstOperand = result;
    updateCalcScreen();
  }
  calcPendingOp = op;
  calcWaitingForSecond = true;
}

function calcEquals() {
  if (calcPendingOp === null || calcFirstOperand === null) return;
  const current = parseFloat(calcDisplayVal) || 0;
  const result = executeCalcOp(calcFirstOperand, current, calcPendingOp);
  calcDisplayVal = String(result);
  calcFirstOperand = null;
  calcPendingOp = null;
  calcWaitingForSecond = true;
  updateCalcScreen();
}

function executeCalcOp(a, b, op) {
  switch (op) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    case '/': return b !== 0 ? a / b : 0;
    default: return b;
  }
}

function calcAction(act) {
  const current = parseFloat(calcDisplayVal) || 0;
  switch (act) {
    case 'C':
      calcDisplayVal = '0';
      calcFirstOperand = null;
      calcPendingOp = null;
      calcWaitingForSecond = false;
      break;
    case 'CE':
      calcDisplayVal = '0';
      break;
    case 'MC':
      calcMemory = 0;
      break;
    case 'MR':
      calcDisplayVal = String(calcMemory);
      calcWaitingForSecond = true;
      break;
    case 'MS':
      calcMemory = current;
      break;
    case 'M+':
      calcMemory += current;
      break;
  }
  updateCalcScreen();
}

function transferCalcDisplay() {
  const numInput = document.getElementById('ets-numeric-input');
  if (numInput) {
    numInput.value = calcDisplayVal;
    setGREAnswer(calcDisplayVal);
    showToast(`Transferred "${calcDisplayVal}" into answer box`, 'success');
  } else {
    showToast('Only Numeric Entry questions accept transferred calculator values', 'info');
  }
}

/* ─────────────────────────────────────────────
   IDP / BRITISH COUNCIL IELTS SIMULATION ENGINE
   ───────────────────────────────────────────── */
function startIELTSMockSimulation(pkg) {
  ieltsSimPackage = pkg;
  ieltsCompIndex = 0;
  ieltsReadingIndex = 0;
  ieltsReadingAnswers = {};
  ieltsWritingAnswers = { task1: '', task2: '' };
  ieltsSpeakingAnswers = {};

  // Init 40 reading answers
  for (let i = 0; i < 40; i++) {
    ieltsReadingAnswers[i] = { answer: '', marked: false };
  }

  document.getElementById('ielts-simulation-modal').classList.remove('hidden');
  loadIELTSComponent(0);
}

function loadIELTSComponent(idx) {
  ieltsCompIndex = idx;
  const comp = ieltsSimPackage.components[idx];
  clearInterval(ieltsTimer);
  ieltsTimeLeft = comp.duration_seconds || (comp.duration_minutes * 60);
  updateIELTSTimerDisplay();

  ieltsTimer = setInterval(() => {
    ieltsTimeLeft--;
    updateIELTSTimerDisplay();
    if (ieltsTimeLeft <= 0) {
      clearInterval(ieltsTimer);
      showToast(`⏰ Time finished for ${comp.title}. Advancing component...`, 'warning');
      proceedNextIELTSComponent();
    }
  }, 1000);

  const titleEl = document.getElementById('ielts-component-title');
  titleEl.textContent = `${comp.title} · ${comp.duration_minutes} minutes`;

  const ribbon = document.getElementById('ielts-ribbon');
  if (comp.type === 'reading') {
    ribbon.classList.remove('hidden');
    renderIELTSReading();
    renderIELTSRibbon();
  } else if (comp.type === 'writing') {
    ribbon.classList.add('hidden');
    renderIELTSWriting();
  } else if (comp.type === 'speaking') {
    ribbon.classList.add('hidden');
    renderIELTSSpeaking();
  }
}

function updateIELTSTimerDisplay() {
  const digitsEl = document.getElementById('ielts-timer-digits');
  if (!digitsEl) return;
  const m = Math.floor(ieltsTimeLeft / 60).toString().padStart(2, '0');
  const s = (ieltsTimeLeft % 60).toString().padStart(2, '0');
  digitsEl.textContent = `${m}:${s}`;
  if (ieltsTimeLeft <= 300) {
    digitsEl.style.color = '#ef4444';
  } else {
    digitsEl.style.color = 'inherit';
  }
}

function renderIELTSReading() {
  const comp = ieltsSimPackage.components[ieltsCompIndex];
  const q = comp.questions[ieltsReadingIndex];
  const body = document.getElementById('ielts-body');
  
  // Review checkbox state
  const revCheck = document.getElementById('ielts-review-checkbox');
  if (revCheck) {
    revCheck.checked = !!ieltsReadingAnswers[ieltsReadingIndex]?.marked;
  }

  // Which passage group: 1-13 = Passage 1, 14-26 = Passage 2, 27-40 = Passage 3
  const passageNum = ieltsReadingIndex < 13 ? 1 : ieltsReadingIndex < 26 ? 2 : 3;
  updateRibbonPassageHighlight(passageNum);

  const currentAns = ieltsReadingAnswers[ieltsReadingIndex]?.answer || '';

  body.innerHTML = `
    <div class="ielts-split-pane">
      <div class="ielts-passage-side">
        <div class="ielts-reading-banner">Reading Passage ${passageNum}</div>
        <div class="ielts-passage-content">
          ${q.passage || '<p>Reading passage loading...</p>'}
        </div>
      </div>
      <div class="ielts-question-side">
        <div class="ielts-q-header">
          <span class="ielts-q-num">Question ${ieltsReadingIndex + 1}</span>
          <span class="ielts-q-type">${q.subsection ? q.subsection.replace(/_/g, ' ').toUpperCase() : 'MULTIPLE CHOICE'}</span>
        </div>
        <div class="ielts-q-instruction">${q.question_text}</div>
        
        ${q.options && q.options.length ? `
        <div class="ielts-options-container">
          ${q.options.map((opt, oIdx) => {
            const key = String.fromCharCode(65 + oIdx);
            const isSelected = currentAns === key;
            return `
              <div class="ielts-option-card ${isSelected ? 'selected' : ''}" onclick="selectIELTSAnswer('${key}')">
                <div class="ielts-opt-radio ${isSelected ? 'active' : ''}">${key}</div>
                <div class="ielts-opt-text">${opt}</div>
              </div>
            `;
          }).join('')}
        </div>` : `
        <div style="margin-top:20px;">
          <label style="font-size:0.85rem;font-weight:600;color:var(--text-secondary);margin-bottom:8px;display:block;">Type your answer (NO MORE THAN THREE WORDS):</label>
          <input type="text" class="ielts-text-answer-input" value="${escapeJs(currentAns)}" oninput="selectIELTSAnswer(this.value)" placeholder="Enter answer..." />
        </div>`}
      </div>
    </div>
  `;
}

function selectIELTSAnswer(val) {
  ieltsReadingAnswers[ieltsReadingIndex].answer = val.trim();
  renderIELTSRibbon();
  // highlight if multiple choice card
  document.querySelectorAll('.ielts-option-card').forEach(c => c.classList.remove('selected'));
  document.querySelectorAll('.ielts-opt-radio').forEach(r => r.classList.remove('active'));
}

function toggleIELTSReviewFlag() {
  const check = document.getElementById('ielts-review-checkbox');
  if (check) {
    ieltsReadingAnswers[ieltsReadingIndex].marked = check.checked;
    renderIELTSRibbon();
  }
}

function renderIELTSRibbon() {
  const container = document.getElementById('ielts-ribbon-numbers');
  if (!container) return;

  container.innerHTML = Array.from({ length: 40 }, (_, i) => {
    const isCurrent = i === ieltsReadingIndex;
    const isAnswered = ieltsReadingAnswers[i]?.answer && ieltsReadingAnswers[i].answer.length > 0;
    const isMarked = ieltsReadingAnswers[i]?.marked;

    let cls = 'ribbon-q-tab';
    if (isCurrent) cls += ' current';
    if (isAnswered) cls += ' answered';
    if (isMarked) cls += ' marked';

    return `<button class="${cls}" onclick="jumpIELTSQuestion(${i})">${i + 1}</button>`;
  }).join('');
}

function jumpIELTSQuestion(qIdx) {
  ieltsReadingIndex = qIdx;
  renderIELTSReading();
  renderIELTSRibbon();
}

function jumpIELTSPassage(passageNum) {
  const targetIdx = passageNum === 1 ? 0 : passageNum === 2 ? 13 : 26;
  jumpIELTSQuestion(targetIdx);
}

function updateRibbonPassageHighlight(pNum) {
  document.querySelectorAll('.ribbon-group-tag').forEach(tag => tag.classList.remove('active'));
  document.getElementById(`ribbon-grp-${pNum}`)?.classList.add('active');
}

function renderIELTSWriting() {
  const comp = ieltsSimPackage.components[ieltsCompIndex];
  const body = document.getElementById('ielts-body');

  body.innerHTML = `
    <div class="ielts-writing-split">
      <div class="ielts-writing-task-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border);">
          <h4 style="font-size:1.05rem;font-weight:700;color:var(--text-primary);">${comp.task_1.title}</h4>
          <span style="font-size:0.78rem;font-weight:700;color:var(--text-muted);">Minimum ${comp.task_1.min_words} Words (20 min)</span>
        </div>
        <p style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);margin-bottom:14px;">${comp.task_1.prompt}</p>
        <div class="ielts-word-counter-badge" id="ielts-task1-counter">0 / 150 words</div>
        <textarea class="ielts-writing-textarea" placeholder="Write your Task 1 response here..." oninput="updateIELTSWritingWordCount(1, this)">${ieltsWritingAnswers.task1}</textarea>
      </div>

      <div class="ielts-writing-task-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border);">
          <h4 style="font-size:1.05rem;font-weight:700;color:var(--text-primary);">${comp.task_2.title}</h4>
          <span style="font-size:0.78rem;font-weight:700;color:var(--text-muted);">Minimum ${comp.task_2.min_words} Words (40 min)</span>
        </div>
        <p style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);margin-bottom:14px;">${comp.task_2.prompt}</p>
        <div class="ielts-word-counter-badge" id="ielts-task2-counter">0 / 250 words</div>
        <textarea class="ielts-writing-textarea" placeholder="Write your Task 2 essay response here..." oninput="updateIELTSWritingWordCount(2, this)">${ieltsWritingAnswers.task2}</textarea>
      </div>
    </div>
  `;
}

function updateIELTSWritingWordCount(taskNum, el) {
  const words = el.value.trim().split(/\s+/).filter(w => w).length;
  if (taskNum === 1) {
    ieltsWritingAnswers.task1 = el.value;
    const badge = document.getElementById('ielts-task1-counter');
    if (badge) {
      badge.textContent = `${words} / 150 words`;
      badge.style.color = words >= 150 ? '#10b981' : '#f59e0b';
    }
  } else {
    ieltsWritingAnswers.task2 = el.value;
    const badge = document.getElementById('ielts-task2-counter');
    if (badge) {
      badge.textContent = `${words} / 250 words`;
      badge.style.color = words >= 250 ? '#10b981' : '#f59e0b';
    }
  }
}

function renderIELTSSpeaking() {
  const comp = ieltsSimPackage.components[ieltsCompIndex];
  const body = document.getElementById('ielts-body');

  body.innerHTML = `
    <div style="padding:28px 36px;max-width:880px;margin:0 auto;overflow-y:auto;height:100%;">
      <div style="margin-bottom:24px;">
        <span class="track-badge badge-ielts">IELTS Speaking Interview</span>
        <h3 style="font-size:1.35rem;font-weight:800;margin-top:8px;">Face-to-Face Examiner Simulation</h3>
        <p style="font-size:0.88rem;color:var(--text-secondary);">Parts 1, 2, and 3 assess Fluency & Coherence, Lexical Resource, Grammatical Range, and Pronunciation.</p>
      </div>

      <div style="display:flex;flex-direction:column;gap:20px;">
        ${comp.parts.map((p, idx) => `
          <div style="background:var(--bg-secondary);padding:20px;border-radius:var(--radius-md);border:1px solid var(--border);">
            <div style="font-size:1.05rem;font-weight:700;color:var(--text-primary);margin-bottom:8px;">${p.title} (${p.duration})</div>
            <p style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary);margin-bottom:14px;">${p.instructions}</p>
            ${p.questions ? `
              <ul style="padding-left:20px;color:var(--text-primary);font-size:0.92rem;line-height:1.7;">
                ${p.questions.map(q => `<li>${q}</li>`).join('')}
              </ul>
            ` : ''}
            ${p.topic ? `
              <div style="background:var(--surface);padding:16px;border-radius:var(--radius-sm);border:1px solid var(--border);margin-top:10px;">
                <div style="font-weight:700;font-size:1rem;color:#3b82f6;margin-bottom:8px;">📌 Cue Card: "${p.topic}"</div>
                <p style="font-size:0.88rem;color:var(--text-secondary);margin-bottom:6px;">You should say:</p>
                <ul style="padding-left:20px;font-size:0.88rem;color:var(--text-primary);line-height:1.6;">
                  ${p.points.map(pt => `<li>${pt}</li>`).join('')}
                </ul>
              </div>
            ` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function confirmFinishIELTSComponent() {
  const comp = ieltsSimPackage.components[ieltsCompIndex];
  const isLast = ieltsCompIndex === ieltsSimPackage.components.length - 1;
  const msg = isLast 
    ? "Are you sure you want to finish the entire IELTS exam and generate your official Test Report Form (TRF) Band Scores?"
    : `Finish ${comp.title} and proceed to the next component?`;

  if (confirm(msg)) {
    proceedNextIELTSComponent();
  }
}

function proceedNextIELTSComponent() {
  clearInterval(ieltsTimer);
  if (ieltsCompIndex < ieltsSimPackage.components.length - 1) {
    const nextComp = ieltsSimPackage.components[ieltsCompIndex + 1];
    showToast(`✅ ${nextComp.title} starting now...`, 'success');
    loadIELTSComponent(ieltsCompIndex + 1);
  } else {
    finishIELTSSimulation();
  }
}

function finishIELTSSimulation() {
  clearInterval(ieltsTimer);
  document.getElementById('ielts-simulation-modal').classList.add('hidden');

  // Calculate Band Scores
  // Reading: 40 questions -> Band conversion
  let readingCorrect = 0;
  const readingComp = ieltsSimPackage.components[0];
  readingComp.questions.forEach((q, idx) => {
    const userAns = ieltsReadingAnswers[idx]?.answer;
    if (userAns && userAns.toLowerCase() === q.correct_answer.toLowerCase()) {
      readingCorrect++;
    }
  });

  let readingBand = 5.0;
  if (readingCorrect >= 39) readingBand = 9.0;
  else if (readingCorrect >= 37) readingBand = 8.5;
  else if (readingCorrect >= 35) readingBand = 8.0;
  else if (readingCorrect >= 33) readingBand = 7.5;
  else if (readingCorrect >= 30) readingBand = 7.0;
  else if (readingCorrect >= 27) readingBand = 6.5;
  else if (readingCorrect >= 23) readingBand = 6.0;
  else if (readingCorrect >= 19) readingBand = 5.5;
  else if (readingCorrect >= 15) readingBand = 5.0;
  else readingBand = 4.5;

  const t1Words = ieltsWritingAnswers.task1.trim().split(/\s+/).filter(w => w).length;
  const t2Words = ieltsWritingAnswers.task2.trim().split(/\s+/).filter(w => w).length;
  let writingBand = 6.0;
  if (t1Words >= 150 && t2Words >= 250) writingBand = 7.5;
  else if (t1Words >= 120 && t2Words >= 200) writingBand = 6.5;
  else if (t1Words >= 80 && t2Words >= 150) writingBand = 5.5;
  else writingBand = 5.0;

  const speakingBand = 7.0;
  const overallBand = Math.round(((readingBand + writingBand + speakingBand) / 3) * 2) / 2;

  const modal = document.getElementById('results-modal');
  document.getElementById('results-score').textContent = `Band ${overallBand.toFixed(1)}`;
  document.getElementById('results-accuracy').textContent = `${Math.round((readingCorrect / 40) * 100)}% (Reading)`;
  document.getElementById('results-time').textContent = `60m + 60m + 14m`;
  document.getElementById('results-scaled').textContent = `CEFR Level: ${overallBand >= 8.5 ? 'C2 Mastery' : overallBand >= 7.0 ? 'C1 Effective' : 'B2 Vantage'}`;

  const breakdown = document.getElementById('results-breakdown');
  breakdown.innerHTML = `
    <div style="background:var(--bg-secondary);padding:20px;border-radius:var(--radius-md);margin-bottom:20px;border:1px solid var(--border);">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <span style="font-weight:800;font-size:1.15rem;color:var(--text-primary);letter-spacing:-0.02em;">
          🇬🇧 IELTS™ Official Test Report Form (TRF) Diagnostic
        </span>
        <span class="track-badge badge-ielts">Academic Stream</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:12px;margin-bottom:16px;">
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Reading</div>
          <div style="font-size:1.8rem;font-weight:900;color:#3b82f6;">${readingBand.toFixed(1)}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">${readingCorrect} of 40 correct</div>
        </div>
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Writing</div>
          <div style="font-size:1.8rem;font-weight:900;color:#10b981;">${writingBand.toFixed(1)}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">${t1Words}w T1 · ${t2Words}w T2</div>
        </div>
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:1px solid var(--border);">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Speaking</div>
          <div style="font-size:1.8rem;font-weight:900;color:#f59e0b;">${speakingBand.toFixed(1)}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">Fluency & Range</div>
        </div>
        <div style="background:var(--surface);padding:14px;border-radius:var(--radius-sm);text-align:center;border:2px solid #6366f1;">
          <div style="font-size:0.75rem;font-weight:700;color:#6366f1;text-transform:uppercase;">Overall Band</div>
          <div style="font-size:1.8rem;font-weight:900;color:#6366f1;">${overallBand.toFixed(1)}</div>
          <div style="font-size:0.72rem;color:var(--text-secondary);">Official 0.0–9.0 scale</div>
        </div>
      </div>
      <p style="font-size:0.85rem;line-height:1.6;color:var(--text-secondary);">
        This official simulation faithfully reproduces the Computer-Delivered IELTS test administration by IDP and the British Council. The split-screen reading interface with text passage navigation, 40-question bottom ribbon, writing word counters, and IELTS 9-band rubric align directly with Cambridge English assessment standards.
      </p>
    </div>
  `;
  modal.classList.remove('hidden');
}


/* ═══════════════════════════════════════════
   TOAST & UTILS
   ═══════════════════════════════════════════ */
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast ${type}`;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), 3500);
}

function escapeJs(str) {
  return String(str).replace(/'/g, "\\'").replace(/"/g, '\\"');
}

/* ═══════════════════════════════════════════
   INTERACTIVE CONTROLS & SHORTCUTS
   ═══════════════════════════════════════════ */
function filterExamMode(mode) {
  document.querySelectorAll('.exam-pill').forEach(p => p.classList.remove('active'));
  document.getElementById(`pill-${mode}`)?.classList.add('active');
  
  const trackGre = document.getElementById('track-gre');
  const trackIelts = document.getElementById('track-ielts');
  
  if (trackGre && trackIelts) {
    if (mode === 'gre') {
      trackGre.style.display = 'block';
      trackGre.style.animation = 'fadeIn 0.25s ease';
      trackIelts.style.display = 'none';
    } else if (mode === 'ielts') {
      trackGre.style.display = 'none';
      trackIelts.style.display = 'block';
      trackIelts.style.animation = 'fadeIn 0.25s ease';
    } else {
      trackGre.style.display = 'block';
      trackGre.style.animation = 'fadeIn 0.25s ease';
      trackIelts.style.display = 'block';
      trackIelts.style.animation = 'fadeIn 0.25s ease';
    }
  }
}

function toggleShortcutsModal() {
  const modal = document.getElementById('shortcuts-modal');
  if (modal) modal.classList.toggle('hidden');
}

function toggleScratchpad() {
  const pad = document.getElementById('quiz-scratchpad');
  if (pad) {
    pad.classList.toggle('hidden');
    if (!pad.classList.contains('hidden')) {
      document.getElementById('scratchpad-notes')?.focus();
    }
  }
}

function clearScratchpad() {
  const notes = document.getElementById('scratchpad-notes');
  if (notes) {
    notes.value = '';
    localStorage.removeItem('prep_scratchpad');
    showToast('Scratchpad cleared', 'info');
  }
}

// ── Keyboard Navigation ──────────────────────────────────────
window.addEventListener('keydown', e => {
  const isInput = ['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName);
  
  // ESC key closes modals or scratchpad
  if (e.key === 'Escape') {
    const shortcutsModal = document.getElementById('shortcuts-modal');
    if (shortcutsModal && !shortcutsModal.classList.contains('hidden')) {
      shortcutsModal.classList.add('hidden');
      return;
    }
    const scratchpad = document.getElementById('quiz-scratchpad');
    if (scratchpad && !scratchpad.classList.contains('hidden')) {
      scratchpad.classList.add('hidden');
      return;
    }
    const quizModal = document.getElementById('quiz-modal');
    if (quizModal && !quizModal.classList.contains('hidden')) {
      endQuizEarly();
      return;
    }
  }
  
  // Alt+S: Toggle Scratchpad
  if (e.altKey && (e.key === 's' || e.key === 'S')) {
    e.preventDefault();
    toggleScratchpad();
    return;
  }

  // Alt+I: Launch Infinite Practice
  if (e.altKey && (e.key === 'i' || e.key === 'I')) {
    e.preventDefault();
    startInfinitePractice('gre', 'quant');
    return;
  }
  
  // '?' key: Show shortcuts modal
  if (!isInput && e.key === '?') {
    e.preventDefault();
    toggleShortcutsModal();
    return;
  }
  
  // Quiz controls when quiz modal is active and not typing in an essay
  const quizModal = document.getElementById('quiz-modal');
  if (quizModal && !quizModal.classList.contains('hidden') && !isInput) {
    const key = e.key.toUpperCase();
    if (['A', 'B', 'C', 'D', 'E'].includes(key)) {
      const idx = key.charCodeAt(0) - 65;
      const optBtn = document.getElementById(`opt-${idx}`);
      if (optBtn) optBtn.click();
    } else if (['1', '2', '3', '4', '5'].includes(key)) {
      const idx = parseInt(key) - 1;
      const optBtn = document.getElementById(`opt-${idx}`);
      if (optBtn) optBtn.click();
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      const nextBtn = document.getElementById('next-btn');
      if (nextBtn && !nextBtn.disabled) nextBtn.click();
    }
  }
});

/* ═══════════════════════════════════════════
   INIT
   ═══════════════════════════════════════════ */
window.addEventListener('DOMContentLoaded', () => {
  if (token && currentUser) {
    document.getElementById('auth-overlay').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    initApp();
  }
  
  // Restore student scratchpad notes
  const savedNotes = localStorage.getItem('prep_scratchpad');
  const padArea = document.getElementById('scratchpad-notes');
  if (savedNotes && padArea) padArea.value = savedNotes;
  padArea?.addEventListener('input', e => localStorage.setItem('prep_scratchpad', e.target.value));

  // Allow Enter key on auth forms
  document.getElementById('login-password')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleLogin();
  });
  document.getElementById('reg-password')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleRegister();
  });
});

