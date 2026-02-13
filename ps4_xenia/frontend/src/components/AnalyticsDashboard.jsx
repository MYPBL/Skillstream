import { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';
import { Timer, Zap, Trophy, Activity, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function AnalyticsDashboard({ user }) {
    const navigate = useNavigate();
    const [overview, setOverview] = useState(null);
    const [skillData, setSkillData] = useState([]);
    const [activityData, setActivityData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const [overviewRes, skillRes, activityRes] = await Promise.allSettled([
                    axios.get(`/analytics/${user.id}/overview`),
                    axios.get(`/analytics/${user.id}/skills`),
                    axios.get(`/analytics/${user.id}/activity`)
                ]);

                if (overviewRes.status === 'fulfilled') setOverview(overviewRes.value.data);
                if (skillRes.status === 'fulfilled') setSkillData(skillRes.value.data);
                if (activityRes.status === 'fulfilled') setActivityData(activityRes.value.data);

            } catch (e) {
                console.error("Analytics fetch failed", e);
            } finally {
                setLoading(false);
            }
        };

        fetchAnalytics();
    }, [user.id]);

    if (loading) return (
        <div className="flex justify-center items-center h-screen">
            <div className="animate-spin h-12 w-12 border-4 border-indigo-500 rounded-full border-t-transparent"></div>
        </div>
    );

    return (
        <div className="space-y-8 animate-fade-in pb-12">
            <div className="flex justify-between items-center mb-4">
                <button onClick={() => navigate('/')} className="flex items-center gap-2 text-indigo-300 hover:text-white transition-colors">
                    <ArrowLeft size={20} /> Back to Dashboard
                </button>
                <div className="px-3 py-1 bg-indigo-900/40 rounded-full border border-indigo-500/30 text-xs text-indigo-200 uppercase tracking-wider font-bold">
                    Quantified Self
                </div>
            </div>

            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <StatBox icon={Timer} title="Total Learning Hours" value={overview?.total_learning_hours || 0} color="text-blue-400" />
                <StatBox icon={Zap} title="Efficiency Score" value={overview?.efficiency_score || 0} suffix="/100" color="text-yellow-400" />
                <StatBox icon={Trophy} title="Modules Completed" value={overview?.modules_completed || 0} color="text-green-400" />
                <StatBox icon={Activity} title="Current Streak" value={overview?.current_streak_days || 0} suffix=" Days" color="text-pink-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Skill Radar Chart */}
                <div className="glass-card p-8 rounded-2xl">
                    <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <span className="p-2 rounded-lg bg-indigo-500/20"><Zap size={20} className="text-indigo-400" /></span>
                        Skill Proficiency Radar
                    </h3>
                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={skillData}>
                                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a5b4fc', fontSize: 12 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                <Radar
                                    name="Proficiency"
                                    dataKey="A"
                                    stroke="#818cf8"
                                    strokeWidth={3}
                                    fill="#6366f1"
                                    fillOpacity={0.4}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                                    itemStyle={{ color: '#818cf8' }}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                    <p className="text-center text-xs text-gray-500 mt-4">Complete modules with high scores to expand your radar.</p>
                </div>

                {/* Activity Bar Chart */}
                <div className="glass-card p-8 rounded-2xl">
                    <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <span className="p-2 rounded-lg bg-green-500/20"><Activity size={20} className="text-green-400" /></span>
                        Learning Velocity (Last 7 Days)
                    </h3>
                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={activityData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                                />
                                <Bar dataKey="minutes" fill="#10b981" radius={[4, 4, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <p className="text-center text-xs text-gray-500 mt-4">Consistency is key to mastering new technologies.</p>
                </div>
            </div>
        </div>
    );
}

function StatBox({ icon: Icon, title, value, suffix = '', color }) {
    return (
        <div className="glass-card p-6 rounded-xl border-t border-white/10 relative overflow-hidden group">
            <div className={`absolute top-0 right-0 p-4 opacity-10 transform translate-x-2 -translate-y-2 group-hover:scale-110 transition-transform`}>
                <Icon size={64} />
            </div>
            <div className="relative z-10">
                <div className="flex items-center gap-3 mb-2">
                    <Icon size={20} className={color} />
                    <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">{title}</span>
                </div>
                <div className="text-3xl font-bold text-white">
                    {value}<span className="text-lg text-gray-500 font-normal ml-1">{suffix}</span>
                </div>
            </div>
        </div>
    )
}
