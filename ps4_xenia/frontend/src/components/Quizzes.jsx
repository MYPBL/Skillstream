import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, Clock, Award, Filter } from 'lucide-react';

export default function Quizzes({ user }) {
    const navigate = useNavigate();
    const [assets, setAssets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all'); // all, easy, moderate, hard

    useEffect(() => {
        fetchQuizzes();
    }, []);

    const fetchQuizzes = async () => {
        try {
            const res = await axios.get('/assets');
            // Filter only assets with quiz data
            const quizAssets = res.data.filter(asset => asset.quiz_data && asset.quiz_data.length > 0);
            setAssets(quizAssets);
        } catch (error) {
            console.error('Failed to fetch quizzes:', error);
        } finally {
            setLoading(false);
        }
    };

    const getDifficultyLabel = (level) => {
        if (level <= 2) return 'Easy';
        if (level <= 4) return 'Moderate';
        return 'Hard';
    };

    const getDifficultyColor = (level) => {
        if (level <= 2) return 'bg-green-500/20 text-green-300 border-green-500/30';
        if (level <= 4) return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
        return 'bg-red-500/20 text-red-300 border-red-500/30';
    };

    const filteredAssets = assets.filter(asset => {
        if (filter === 'all') return true;
        const difficulty = getDifficultyLabel(asset.difficulty_level).toLowerCase();
        return difficulty === filter;
    });

    if (loading) {
        return (
            <div className="flex items-center justify-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto animate-fade-in">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-4">
                    <div className="h-12 w-12 bg-indigo-500/20 rounded-full flex items-center justify-center">
                        <BookOpen className="text-indigo-300" size={24} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-extrabold text-white tracking-tight">Quiz Library</h1>
                        <p className="text-gray-400 text-sm mt-1">Test your knowledge and track your progress</p>
                    </div>
                </div>

                {/* Filter Buttons */}
                <div className="flex gap-3 flex-wrap">
                    <button
                        onClick={() => setFilter('all')}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${filter === 'all'
                                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-900/50'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        All Quizzes ({assets.length})
                    </button>
                    <button
                        onClick={() => setFilter('easy')}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${filter === 'easy'
                                ? 'bg-green-600 text-white shadow-lg shadow-green-900/50'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        Easy ({assets.filter(a => a.difficulty_level <= 2).length})
                    </button>
                    <button
                        onClick={() => setFilter('moderate')}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${filter === 'moderate'
                                ? 'bg-yellow-600 text-white shadow-lg shadow-yellow-900/50'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        Moderate ({assets.filter(a => a.difficulty_level > 2 && a.difficulty_level <= 4).length})
                    </button>
                    <button
                        onClick={() => setFilter('hard')}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${filter === 'hard'
                                ? 'bg-red-600 text-white shadow-lg shadow-red-900/50'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        Hard ({assets.filter(a => a.difficulty_level > 4).length})
                    </button>
                </div>
            </div>

            {/* Quiz Grid */}
            {filteredAssets.length === 0 ? (
                <div className="text-center py-20">
                    <Filter className="mx-auto text-gray-600 mb-4" size={48} />
                    <p className="text-gray-400">No quizzes found for this difficulty level.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAssets.map((asset) => (
                        <div
                            key={asset.id}
                            className="glass-card rounded-xl overflow-hidden hover:shadow-2xl hover:shadow-indigo-900/20 transition-all transform hover:scale-[1.02] cursor-pointer border border-white/10"
                            onClick={() => navigate('/learn', { state: { asset } })}
                        >
                            {/* Card Header */}
                            <div className="bg-black/40 p-4 border-b border-white/10">
                                <div className="flex items-start justify-between mb-2">
                                    <h3 className="text-lg font-bold text-white leading-tight flex-1">
                                        {asset.title}
                                    </h3>
                                    <Award className="text-indigo-400 flex-shrink-0 ml-2" size={20} />
                                </div>
                                <p className="text-sm text-gray-400 line-clamp-2">{asset.description}</p>
                            </div>

                            {/* Card Body */}
                            <div className="p-4 space-y-3">
                                {/* Difficulty Badge */}
                                <div className="flex items-center gap-2">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getDifficultyColor(asset.difficulty_level)}`}>
                                        {getDifficultyLabel(asset.difficulty_level)}
                                    </span>
                                    <span className="text-xs text-gray-500">Level {asset.difficulty_level}</span>
                                </div>

                                {/* Quiz Info */}
                                <div className="flex items-center justify-between text-sm">
                                    <div className="flex items-center gap-2 text-gray-400">
                                        <BookOpen size={16} className="text-indigo-400" />
                                        <span>{asset.quiz_data?.length || 0} Questions</span>
                                    </div>
                                    <div className="flex items-center gap-2 text-gray-400">
                                        <Clock size={16} className="text-indigo-400" />
                                        <span>{asset.estimated_duration_minutes || 10} min</span>
                                    </div>
                                </div>

                                {/* Skill Tag */}
                                <div className="pt-2">
                                    <span className="inline-block px-2 py-1 bg-indigo-500/10 text-indigo-300 text-xs rounded border border-indigo-500/20">
                                        {asset.skill_tag || 'General'}
                                    </span>
                                </div>
                            </div>

                            {/* Card Footer */}
                            <div className="p-4 pt-0">
                                <button className="w-full py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold rounded-lg transition-all shadow-lg shadow-indigo-900/30">
                                    Start Quiz
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Info Banner */}
            {!user && filteredAssets.length > 0 && (
                <div className="mt-12 glass-card p-6 rounded-xl border border-yellow-500/20 bg-yellow-500/5">
                    <div className="flex items-start gap-4">
                        <div className="text-3xl">💡</div>
                        <div>
                            <h4 className="text-lg font-bold text-yellow-300 mb-2">Sign in for Full Experience</h4>
                            <p className="text-gray-300 text-sm">
                                You can take quizzes without signing in, but you'll miss out on:
                            </p>
                            <ul className="mt-2 space-y-1 text-sm text-gray-400">
                                <li>• Personalized adaptive recommendations</li>
                                <li>• Progress tracking and analytics</li>
                                <li>• Skill-based learning paths</li>
                                <li>• Performance history</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
