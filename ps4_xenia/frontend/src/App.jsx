import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import AssetViewer from './components/AssetViewer'
import AnalyticsDashboard from './components/AnalyticsDashboard'
import UserProfile from './components/UserProfile'
import Quizzes from './components/Quizzes'
import axios from 'axios'
import bgImage from './assets/background.png'

// Configure Axios - Backend is on port 8000
axios.defaults.baseURL = 'http://localhost:8000/api/v1'

function App() {
    const [currentUser, setCurrentUser] = useState(null)
    const [profileOpen, setProfileOpen] = useState(false)

    return (
        <Router>
            <div className="min-h-screen font-sans text-gray-100 relative overflow-hidden transition-colors duration-500">
                {/* Background Layer */}
                <div
                    className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat transform scale-105"
                    style={{ backgroundImage: `url(${bgImage})` }}
                >
                    <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px]"></div>
                    <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/40 to-transparent"></div>
                </div>

                {/* Content Layer */}
                <div className="relative z-10 flex flex-col min-h-screen">
                    <header className="sticky top-0 z-50 glass border-b border-white/10">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
                            <h1 className="text-2xl font-bold flex items-center gap-3 animate-fade-in">
                                <span className="text-3xl filter drop-shadow-lg">⚡</span>
                                <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200 drop-shadow-sm tracking-tight">
                                    Adaptive<span className="font-light">Learning</span>
                                </span>
                            </h1>

                            {/* Public Nav Removed - Login Only */}

                            {currentUser && (
                                <div className="flex items-center gap-6 animate-fade-in delay-100">
                                    <nav className="hidden md:flex gap-6 mr-4">
                                        <Link to="/" className="text-sm font-medium text-gray-300 hover:text-white transition-colors relative group">
                                            Dashboard
                                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-indigo-400 transition-all group-hover:w-full"></span>
                                        </Link>
                                        <Link to="/quizzes" className="text-sm font-medium text-gray-300 hover:text-white transition-colors relative group">
                                            Quizzes
                                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-indigo-400 transition-all group-hover:w-full"></span>
                                        </Link>
                                        <Link to="/analytics" className="text-sm font-medium text-gray-300 hover:text-white transition-colors relative group">
                                            Analytics
                                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-indigo-400 transition-all group-hover:w-full"></span>
                                        </Link>
                                    </nav>

                                    <div className="relative">
                                        <button
                                            onClick={() => setProfileOpen(!profileOpen)}
                                            className="flex items-center gap-3 hover:bg-white/5 p-1.5 pr-3 rounded-lg transition-colors border border-transparent hover:border-white/10"
                                        >
                                            <div className="h-9 w-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold shadow-lg">
                                                {currentUser.full_name.charAt(0)}
                                            </div>
                                            <div className="text-right hidden sm:block">
                                                <div className="text-sm font-bold text-white tracking-wide leading-tight">
                                                    {currentUser.full_name}
                                                </div>
                                                <div className="text-[10px] text-indigo-300 uppercase tracking-wider font-semibold">
                                                    {currentUser.role}
                                                </div>
                                            </div>
                                        </button>

                                        {profileOpen && (
                                            <div className="absolute right-0 mt-2 w-56 glass-card rounded-xl border border-white/10 shadow-2xl overflow-hidden py-1 z-50 animate-fade-in-up origin-top-right backdrop-blur-xl bg-gray-900/90">
                                                <div className="px-4 py-3 border-b border-white/5 bg-white/5">
                                                    <p className="text-xs text-indigo-300 font-bold uppercase mb-1">Signed in as</p>
                                                    <p className="text-sm text-white truncate font-medium">{currentUser.email}</p>
                                                </div>

                                                <div className="py-1">
                                                    <Link
                                                        to="/profile"
                                                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-indigo-500/20 hover:text-white transition-colors"
                                                        onClick={() => setProfileOpen(false)}
                                                    >
                                                        <span>👤</span> My Profile
                                                    </Link>
                                                    <Link
                                                        to="/"
                                                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-indigo-500/20 hover:text-white transition-colors"
                                                        onClick={() => setProfileOpen(false)}
                                                    >
                                                        <span>📊</span> Dashboard
                                                    </Link>
                                                </div>

                                                <div className="border-t border-white/5 my-1"></div>

                                                <button
                                                    onClick={() => { setCurrentUser(null); setProfileOpen(false); }}
                                                    className="w-full text-left flex items-center gap-3 px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors"
                                                >
                                                    <span>🚪</span> Logout
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    </header>

                    <main className="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
                        {!currentUser ? (
                            <Routes>
                                <Route path="/" element={<LoginScreen onLogin={setCurrentUser} />} />
                                <Route path="/quizzes" element={<Quizzes user={null} />} />
                                <Route path="/learn" element={<AssetViewer user={{ id: 'guest', full_name: 'Guest' }} />} />
                                <Route path="*" element={<Navigate to="/" />} />
                            </Routes>
                        ) : (
                            <Routes>
                                <Route path="/" element={<Dashboard user={currentUser} />} />
                                <Route path="/profile" element={<UserProfile user={currentUser} />} />
                                <Route path="/learn" element={<AssetViewer user={currentUser} />} />
                                <Route path="/quizzes" element={<Quizzes user={currentUser} />} />
                                <Route path="/analytics" element={<AnalyticsDashboard user={currentUser} />} />
                                <Route path="*" element={<Navigate to="/" />} />
                            </Routes>
                        )}
                    </main>

                    <footer className="py-6 text-center text-gray-500 text-sm relative z-10">
                        <p>&copy; 2026 Adaptive Learning Platform. All rights reserved.</p>
                    </footer>
                </div>
            </div>
        </Router>
    )
}

function LoginScreen({ onLogin }) {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const payload = {
                email: email,
                password: 'password123'
            };

            const res = await axios.post('/auth/login', payload);
            const token = res.data.access_token;

            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            const profileRes = await axios.get('/auth/me');
            onLogin(profileRes.data);

        } catch (err) {
            console.error(err);
            const msg = err.response?.data?.detail || 'Login failed. Ensure backend is running.';
            setError(msg);
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
            <div className="glass-card p-10 rounded-2xl w-full max-w-md text-center border-t border-white/20">
                <div className="mb-8">
                    <div className="h-16 w-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4 backdrop-blur-xl border border-white/20 shadow-inner">
                        <span className="text-3xl">🔐</span>
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Access Portal</h2>
                    <p className="text-indigo-200 text-sm">Sign in to continue your learning journey</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 text-left">
                    <div>
                        <label className="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Email Address</label>
                        <input
                            type="email"
                            placeholder="user@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-3 rounded-lg bg-black/20 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:bg-black/40 transition-all font-medium"
                            required
                        />
                    </div>

                    {error && (
                        <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-300 text-sm flex items-center gap-2">
                            <span>⚠️</span> {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-4 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold shadow-lg shadow-indigo-900/50 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Authenticating...' : 'Enter Learning Space'}
                    </button>
                </form>

                <div className="mt-10 pt-6 border-t border-white/5 text-sm text-gray-400">
                    <p className="mb-3 font-semibold text-gray-500 uppercase text-xs">Quick Access (Demo)</p>
                    <div className="flex flex-wrap justify-center gap-2">
                        <button
                            type="button"
                            className="px-3 py-1.5 bg-white/5 rounded-md hover:bg-white/10 hover:text-white transition-colors border border-white/5 text-xs font-mono"
                            onClick={() => setEmail('admin@example.com')}
                        >
                            admin@example.com
                        </button>
                        <button
                            type="button"
                            className="px-3 py-1.5 bg-white/5 rounded-md hover:bg-white/10 hover:text-white transition-colors border border-white/5 text-xs font-mono"
                            onClick={() => setEmail('newbie@example.com')}
                        >
                            newbie@example.com
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App
