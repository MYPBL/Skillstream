import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Play, TrendingUp, Clock, Award, Zap } from 'lucide-react';

export default function Dashboard({ user }) {
    const [stats, setStats] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, recRes] = await Promise.allSettled([
                    axios.get(`/learning/dashboard/${user.id}`),
                    axios.get(`/learning/${user.id}/recommendations`)
                ]);

                if (statsRes.status === 'fulfilled') setStats(statsRes.value.data);
                if (recRes.status === 'fulfilled') setRecommendations(recRes.value.data);

            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [user.id]);

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="animate-spin h-8 w-8 border-4 border-indigo-400 rounded-full border-t-transparent"></div>
        </div>
    );

    return (
        <div className="space-y-8">
            {/* Welcome Section */}
            <div className="bg-black/40 backdrop-blur-md border border-white/10 shadow-lg rounded-2xl p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                    <Zap size={100} className="text-white" />
                </div>
                <div className="relative z-10">
                    <h2 className="text-3xl font-bold text-white mb-2">
                        Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">{user.full_name.split(' ')[0]}</span>
                    </h2>
                    <p className="text-indigo-200 text-lg">
                        Your learning path is optimized for <span className="font-semibold text-white bg-white/10 px-2 py-0.5 rounded">{user.preferred_learning_style}</span> mastery.
                    </p>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard icon={Award} title="Modules Completed" value={stats?.completed_modules || 0} color="from-blue-500/20 to-cyan-500/20 text-blue-300" delay={0} />
                <StatCard icon={TrendingUp} title="Avg. Performance" value={`${stats?.average_score || 0}%`} color="from-green-500/20 to-emerald-500/20 text-green-300" delay={100} />
                <StatCard icon={Clock} title="Current Level" value={stats?.current_level || 'N/A'} color="from-purple-500/20 to-pink-500/20 text-purple-300" delay={200} />
            </div>

            {/* Recommended for You Grid */}
            <div className="mt-8">
                <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                    <span className="text-indigo-400">Recommended</span> for You
                </h3>

                {recommendations.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {recommendations.map((rec, i) => (
                            <div
                                key={rec.id}
                                className="glass-card rounded-xl overflow-hidden group animate-slide-up"
                                style={{ animationDelay: `${(i + 3) * 100}ms`, animationFillMode: 'forwards', opacity: 0 }}
                            >
                                <div className="h-40 bg-gray-900/50 relative flex items-center justify-center overflow-hidden">
                                    {/* Abstract Background for card */}
                                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 group-hover:scale-110 transition-transform duration-500"></div>

                                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 backdrop-blur-sm z-10">
                                        <button
                                            onClick={() => navigate('/learn', { state: { asset: rec } })}
                                            className="bg-white text-indigo-900 rounded-full p-3 px-6 font-bold flex items-center gap-2 hover:scale-105 transition-transform"
                                        >
                                            <Play size={18} fill="currentColor" /> Start
                                        </button>
                                    </div>

                                    <div className="relative z-0 opacity-60 group-hover:opacity-40 transition-opacity">
                                        <Play size={40} className="text-white" />
                                    </div>

                                    <span className="absolute top-3 right-3 px-2 py-1 bg-black/60 backdrop-blur-md text-white text-xs rounded uppercase font-bold border border-white/10">
                                        {rec.content_type}
                                    </span>
                                </div>
                                <div className="p-6">
                                    <div className="flex justify-between items-start mb-3">
                                        <span className={`text-xs font-bold px-2 py-1 rounded border ${rec.difficulty_level <= 2 ? 'bg-green-500/20 text-green-300 border-green-500/30' : rec.difficulty_level <= 4 ? 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30' : 'bg-red-500/20 text-red-300 border-red-500/30'}`}>
                                            Level {rec.difficulty_level}
                                        </span>
                                        <span className="text-gray-400 text-xs flex items-center gap-1">
                                            <Clock size={12} /> {rec.estimated_duration_minutes}m
                                        </span>
                                    </div>
                                    <h4 className="text-lg font-bold text-white mb-2 line-clamp-2 group-hover:text-indigo-300 transition-colors">{rec.title}</h4>
                                    <p className="text-gray-400 text-sm line-clamp-2 mb-4">{rec.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="glass-card p-12 rounded-xl border-dashed border-white/20 text-center text-gray-400">
                        <p className="text-lg">You're all caught up! Check back later for more content.</p>
                    </div>
                )}
            </div>

            {/* Notifications / Alerts Section */}
            <NotificationSection userId={user.id} />
        </div>
    );
}

function NotificationSection({ userId }) {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const res = await axios.get(`/notifications/${userId}`);
                setNotifications(res.data);
            } catch (e) {
                console.error("Failed to fetch notifications", e);
            }
        };
        fetchNotes();
        // Poll every 10 seconds for real-time feel
        const interval = setInterval(fetchNotes, 10000);
        return () => clearInterval(interval);
    }, [userId]);

    if (notifications.length === 0) return null;

    return (
        <div className="glass-card rounded-2xl p-6 border-t border-indigo-500/30 animate-fade-in-up">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="p-1.5 bg-indigo-500/20 rounded-lg"><Zap size={18} className="text-indigo-300" /></span>
                Recent Updates
            </h3>
            <div className="space-y-3">
                {notifications.slice(0, 3).map(note => (
                    <div key={note.id} className={`p-4 rounded-xl border flex items-start gap-3 backdrop-blur-sm ${note.type === 'success' ? 'bg-green-500/10 border-green-500/20' : 'bg-blue-500/10 border-blue-500/20'}`}>
                        <div className={`mt-1 h-2 w-2 rounded-full shadow-[0_0_8px] ${note.type === 'success' ? 'bg-green-400 shadow-green-400' : 'bg-blue-400 shadow-blue-400'}`}></div>
                        <div>
                            <p className="text-gray-200 text-sm font-medium">{note.message}</p>
                            <p className="text-gray-500 text-xs mt-1 opacity-70">{new Date(note.created_at).toLocaleTimeString()}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

function StatCard({ icon: Icon, title, value, color, delay }) {
    return (
        <div
            className="glass-card p-6 rounded-xl flex items-center gap-4 animate-slide-up"
            style={{ animationDelay: `${delay}ms`, animationFillMode: 'forwards', opacity: 0 }}
        >
            <div className={`p-4 rounded-lg bg-gradient-to-br ${color} shadow-inner`}>
                <Icon size={24} className="text-current" />
            </div>
            <div>
                <p className="text-sm text-gray-400 font-medium">{title}</p>
                <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
            </div>
        </div>
    )
}
