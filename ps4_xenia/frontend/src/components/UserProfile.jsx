import { useState, useEffect } from 'react';
import axios from 'axios';
import { User, Mail, Briefcase, Award, Save, Clock, BookOpen, Target } from 'lucide-react';

export default function UserProfile({ user }) {
    const [profile, setProfile] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({});
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        fetchProfile();
    }, [user.id]);

    const fetchProfile = async () => {
        try {
            const res = await axios.get(`/profile`);
            setProfile(res.data);
            setFormData({
                full_name: res.data.full_name,
                department: res.data.department || '',
                preferred_learning_style: res.data.preferred_learning_style,
                learning_pace: res.data.learning_pace
            });
        } catch (e) {
            console.error("Failed to fetch profile", e);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            const res = await axios.patch('/profile', formData);
            setProfile(res.data);
            setIsEditing(false);
            setMessage({ type: 'success', text: 'Profile updated successfully!' });
            setTimeout(() => setMessage(null), 3000);
        } catch (e) {
            console.error(e);
            setMessage({ type: 'error', text: 'Failed to update profile.' });
        }
    };

    if (loading) return <div className="p-10 text-center text-white">Loading profile...</div>;

    // Calculate "Progress" (Mock or real if available)
    // Using current_skills count as a proxy for progress for now, or just a static visual
    const skillCount = profile.current_skills?.length || 0;
    const targetCount = profile.target_skills?.length || 0;
    const progressPercent = targetCount > 0 ? Math.min(100, Math.round((skillCount / targetCount) * 100)) : 15; // fallback

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header Card */}
            <div className="glass-card p-8 rounded-2xl flex items-center gap-6 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-6 opacity-5">
                    <User size={120} className="text-white bg-white/10 rounded-full" />
                </div>

                <div className="relative z-10 h-24 w-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-3xl font-bold text-white shadow-xl ring-4 ring-white/10">
                    {profile.full_name.charAt(0)}
                </div>

                <div className="relative z-10 flex-1">
                    <h1 className="text-3xl font-bold text-white mb-2">{profile.full_name}</h1>
                    <div className="flex items-center gap-4 text-indigo-200">
                        <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm">
                            <Briefcase size={14} /> {profile.role}
                        </span>
                        <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm">
                            <Mail size={14} /> {profile.email}
                        </span>
                    </div>
                </div>

                <div className="relative z-10">
                    <button
                        onClick={() => isEditing ? handleSave() : setIsEditing(true)}
                        className={`px-6 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all ${isEditing
                                ? 'bg-green-500 hover:bg-green-600 text-white shadow-lg shadow-green-500/20'
                                : 'bg-white/10 hover:bg-white/20 text-white border border-white/10'
                            }`}
                    >
                        {isEditing ? <><Save size={18} /> Save Changes</> : 'Edit Profile'}
                    </button>
                    {isEditing && (
                        <button
                            onClick={() => setIsEditing(false)}
                            className="mt-2 text-xs text-center w-full text-gray-400 hover:text-white"
                        >
                            Cancel
                        </button>
                    )}
                </div>
            </div>

            {message && (
                <div className={`p-4 rounded-xl flex items-center gap-2 ${message.type === 'success' ? 'bg-green-500/20 text-green-300 border border-green-500/30' : 'bg-red-500/20 text-red-300 border border-red-500/30'}`}>
                    {message.text}
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Column: Details */}
                <div className="md:col-span-2 space-y-6">
                    <div className="glass-card p-6 rounded-2xl">
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <BookOpen size={20} className="text-indigo-400" />
                            Personal Details
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase font-bold text-gray-500">Full Name</label>
                                {isEditing ? (
                                    <input
                                        type="text"
                                        value={formData.full_name}
                                        onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-indigo-500 outline-none"
                                    />
                                ) : (
                                    <div className="text-white font-medium text-lg">{profile.full_name}</div>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase font-bold text-gray-500">Department</label>
                                {isEditing ? (
                                    <input
                                        type="text"
                                        value={formData.department}
                                        onChange={e => setFormData({ ...formData, department: e.target.value })}
                                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-indigo-500 outline-none"
                                    />
                                ) : (
                                    <div className="text-white font-medium text-lg">{profile.department || 'Not Assigned'}</div>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase font-bold text-gray-500">Learning Style</label>
                                {isEditing ? (
                                    <select
                                        value={formData.preferred_learning_style}
                                        onChange={e => setFormData({ ...formData, preferred_learning_style: e.target.value })}
                                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-indigo-500 outline-none"
                                    >
                                        <option value="Visual">Visual</option>
                                        <option value="Auditory">Auditory</option>
                                        <option value="Reading/Writing">Text-Based</option>
                                        <option value="Kinesthetic">Kinesthetic</option>
                                    </select>
                                ) : (
                                    <div className="text-white font-medium text-lg flex items-center gap-2">
                                        {profile.preferred_learning_style}
                                    </div>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase font-bold text-gray-500">Pace</label>
                                {isEditing ? (
                                    <select
                                        value={formData.learning_pace}
                                        onChange={e => setFormData({ ...formData, learning_pace: e.target.value })}
                                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-indigo-500 outline-none"
                                    >
                                        <option value="slow">Slow</option>
                                        <option value="medium">Medium</option>
                                        <option value="fast">Fast</option>
                                    </select>
                                ) : (
                                    <div className="text-white font-medium text-lg capitalize">{profile.learning_pace}</div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Mastery Progress */}
                    <div className="glass-card p-6 rounded-2xl">
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <Target size={20} className="text-green-400" />
                            Path Mastery
                        </h3>

                        <div className="mb-2 flex justify-between text-sm text-gray-300">
                            <span>Overall Progress</span>
                            <span className="font-bold text-green-400">{progressPercent}%</span>
                        </div>
                        <div className="h-4 w-full bg-black/40 rounded-full overflow-hidden mb-6">
                            <div
                                className="h-full bg-gradient-to-r from-green-500 to-emerald-400 relative"
                                style={{ width: `${progressPercent}%` }}
                            >
                                <div className="absolute inset-0 bg-white/20 animate-pulse-slow"></div>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                                <div className="text-2xl font-bold text-white mb-1">{profile.target_skills.length}</div>
                                <div className="text-xs text-gray-400 uppercase">Target Skills</div>
                            </div>
                            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                                <div className="text-2xl font-bold text-white mb-1">{profile.current_skills.length}</div>
                                <div className="text-xs text-gray-400 uppercase">Skills Mastered</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Skills */}
                <div className="space-y-6">
                    <div className="glass-card p-6 rounded-2xl h-full">
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <Award size={20} className="text-purple-400" />
                            Skills Registry
                        </h3>

                        <div className="space-y-6">
                            <div>
                                <h4 className="text-xs font-bold text-gray-500 uppercase mb-3">Current Skills</h4>
                                <div className="flex flex-wrap gap-2">
                                    {profile.current_skills.map(skill => (
                                        <span key={skill} className="px-3 py-1.5 rounded-lg bg-indigo-500/20 text-indigo-200 border border-indigo-500/30 text-sm font-medium">
                                            {skill}
                                        </span>
                                    ))}
                                    {profile.current_skills.length === 0 && <span className="text-gray-500 text-sm italic">No skills recorded</span>}
                                </div>
                            </div>

                            <div>
                                <h4 className="text-xs font-bold text-gray-500 uppercase mb-3">Goal Skills</h4>
                                <div className="flex flex-wrap gap-2">
                                    {profile.target_skills.map(skill => (
                                        <span key={skill} className="px-3 py-1.5 rounded-lg bg-purple-500/20 text-purple-200 border border-purple-500/30 text-sm font-medium dashed-border">
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
