import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { CheckCircle, Clock, ArrowLeft, Play, ExternalLink, Award } from 'lucide-react';

export default function AssetViewer({ user }) {
    const { state } = useLocation();
    const navigate = useNavigate();
    const asset = state?.asset;

    const [startTime] = useState(Date.now());
    const [completed, setCompleted] = useState(false);
    const [score, setScore] = useState(100);
    const [submitting, setSubmitting] = useState(false);

    if (!asset) {
        navigate('/');
        return null;
    }

    const [resultData, setResultData] = useState(null);

    const handleComplete = async (finalScore) => {
        setSubmitting(true);
        const timeSpent = Math.floor((Date.now() - startTime) / 1000);
        // Use passed score (from Quiz) or state score (from Slider)
        const submittedScore = typeof finalScore === 'number' ? finalScore : score;

        try {
            const res = await axios.post('/learning/interact', {
                user_id: user.id,
                asset_id: asset.id,
                status: 'completed',
                score: submittedScore,
                time_spent_seconds: timeSpent,
                attempts: 1
            });

            setResultData(res.data);
            setCompleted(true);
            // Removed auto-navigation to allow user to see adaptive results
        } catch (e) {
            console.error(e);
            alert("Failed to submit progress");
            setSubmitting(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto animate-fade-in">
            <button onClick={() => navigate('/')} className="mb-6 flex items-center gap-2 text-indigo-300 hover:text-white transition-colors">
                <ArrowLeft size={20} /> Back to Dashboard
            </button>

            <div className="glass-card rounded-2xl overflow-hidden shadow-2xl">
                {/* Header */}
                <div className="bg-black/40 backdrop-blur-md p-8 border-b border-white/10 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-12 opacity-5 pointer-events-none">
                        <Play size={200} className="text-white transform rotate-12" />
                    </div>
                    <div className="flex justify-between items-start relative z-10">
                        <div>
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-200 border border-indigo-500/30 text-xs font-bold uppercase tracking-wider mb-4 shadow-lg shadow-indigo-500/10">
                                {asset.content_type === 'video' ? <Play size={10} fill="currentColor" /> : <ExternalLink size={10} />}
                                {asset.content_type} Module
                            </span>
                            <h1 className="text-4xl font-extrabold text-white tracking-tight leading-tight">{asset.title}</h1>
                        </div>
                        <div className="text-right">
                            <div className="flex items-center gap-2 text-gray-400 bg-black/30 px-3 py-1.5 rounded-lg border border-white/5">
                                <Clock size={16} className="text-indigo-400" />
                                <span className="font-mono">{asset.estimated_duration_minutes} min</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Content Area */}
                <div className="p-8 bg-black/20 min-h-[400px] flex flex-col items-center justify-center border-b border-white/10 relative">
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/20 pointer-events-none"></div>
                    {asset.content_type === 'video' ? (
                        <div className="w-full aspect-video bg-black rounded-xl overflow-hidden shadow-2xl border border-white/10 relative group">
                            <div className="absolute inset-0 bg-indigo-500/5 animate-pulse pointer-events-none"></div>
                            <iframe
                                className="w-full h-full rounded-xl relative z-10"
                                src={asset.content_url || asset.url}
                                title={asset.title}
                                frameBorder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            ></iframe>
                        </div>
                    ) : (
                        <div className="text-center relative z-10 p-8 glass rounded-xl border border-white/10 max-w-2xl">
                            <div className="mx-auto w-16 h-16 bg-indigo-500/20 rounded-full flex items-center justify-center mb-6">
                                <ExternalLink size={32} className="text-indigo-300" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-4">External Resource</h3>
                            <p className="mb-8 text-gray-300 leading-relaxed">
                                This learning module is hosted on an external platform. Please review the material at the source, then return here to complete your assessment.
                            </p>
                            <a
                                href={asset.content_url || asset.url}
                                target="_blank"
                                rel="noreferrer"
                                className="inline-flex items-center gap-2 px-8 py-3 rounded-full shadow-lg shadow-indigo-500/20 text-white bg-indigo-600 hover:bg-indigo-500 hover:scale-105 transition-all font-bold"
                            >
                                Open Resource <ExternalLink size={16} />
                            </a>
                        </div>
                    )}
                </div>

                {/* Assessment / Completion */}
                <div className="p-10 bg-black/10">
                    {!completed ? (
                        <div className="max-w-2xl mx-auto">
                            {asset.quiz_data ? (
                                <QuizInterface
                                    quizData={asset.quiz_data}
                                    onComplete={(score) => {
                                        setScore(score);
                                        // Trigger submission immediately after quiz
                                        setTimeout(() => handleComplete(score), 500);
                                    }}
                                />
                            ) : (
                                <>
                                    <div className="text-center mb-8">
                                        <h3 className="text-xl font-bold text-white">Assessment</h3>
                                        <p className="text-gray-400 text-sm">Rate your understanding to update your skill profile</p>
                                    </div>

                                    <div className="bg-black/20 p-6 rounded-xl border border-white/5 mb-8">
                                        <label className="flex justify-between text-sm font-medium text-gray-300 mb-4">
                                            <span>Comprehension Score</span>
                                            <span className="text-indigo-300 font-bold">{score}%</span>
                                        </label>
                                        <input
                                            type="range"
                                            min="0"
                                            max="100"
                                            value={score}
                                            onChange={(e) => setScore(Number(e.target.value))}
                                            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-500 hover:accent-indigo-400 transition-all"
                                        />
                                        <div className="flex justify-between text-xs text-gray-500 mt-2 font-mono">
                                            <span>Need Review</span>
                                            <span>Mastered</span>
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => handleComplete(score)}
                                        disabled={submitting}
                                        className="w-full flex justify-center items-center gap-2 py-4 px-6 rounded-xl shadow-xl shadow-green-900/20 text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-bold text-lg"
                                    >
                                        {submitting ? <span className="animate-pulse">Processing...</span> : <><CheckCircle size={20} /> Complete Module</>}
                                    </button>
                                </>
                            )}
                        </div>
                    ) : (
                        <div className="text-center py-12 animate-slide-up max-w-2xl mx-auto">
                            {/* Result Display */}
                            <div className="mb-8">
                                <div className={`mx-auto h-24 w-24 rounded-full flex items-center justify-center mb-6 border shadow-[0_0_30px_rgba(0,0,0,0.3)] ${resultData?.remedial
                                    ? 'bg-yellow-500/20 border-yellow-500/30 text-yellow-400'
                                    : 'bg-green-500/20 border-green-500/30 text-green-400'
                                    }`}>
                                    <Award className="h-12 w-12" />
                                </div>
                                <h3 className="text-3xl font-extrabold text-white mb-2">
                                    {resultData?.remedial ? "Review Needed" : "Module Mastered!"}
                                </h3>
                                <p className="text-lg text-indigo-200 mb-6">{resultData?.message}</p>
                            </div>

                            {/* Adaptive Actions */}
                            <div className="grid gap-6">
                                {/* Case A: High Score -> Next Recommendation */}
                                {resultData?.next_recommendation && (
                                    <div className="glass-card p-6 rounded-xl border border-indigo-500/30 bg-indigo-500/10">
                                        <h4 className="text-sm font-bold text-indigo-300 uppercase mb-3">🚀 Recommended Next Step</h4>
                                        <div className="flex items-center gap-4 bg-black/40 p-4 rounded-lg">
                                            <div className="h-10 w-10 bg-indigo-600 rounded-full flex items-center justify-center flex-shrink-0">
                                                <Play size={20} className="text-white" />
                                            </div>
                                            <div className="text-left flex-1">
                                                <div className="text-white font-bold">{resultData.next_recommendation.title}</div>
                                                <div className="text-xs text-gray-400">Level {resultData.next_recommendation.difficulty_level} • Fastest Path</div>
                                            </div>
                                            <button
                                                onClick={() => navigate('/learn', { state: { asset: resultData.next_recommendation }, replace: true })}
                                                className="px-4 py-2 bg-white text-indigo-900 rounded-lg text-sm font-bold hover:bg-gray-100"
                                            >
                                                Start Now
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {/* Case B: Low Score -> Cheatsheet */}
                                {resultData?.remedial && resultData?.cheatsheet && (
                                    <div className="glass-card p-8 rounded-xl text-left border border-yellow-500/20 bg-yellow-500/5">
                                        <h4 className="text-lg font-bold text-yellow-300 mb-4 flex items-center gap-2">
                                            <span className="text-2xl">📝</span> Quick Review Cheatsheet
                                        </h4>
                                        <div className="prose prose-invert prose-sm max-w-none text-gray-300 whitespace-pre-wrap font-mono bg-black/30 p-6 rounded-lg border border-white/5">
                                            {resultData.cheatsheet}
                                        </div>
                                        <div className="mt-6 text-center">
                                            <button
                                                onClick={() => setCompleted(false)}
                                                className="text-sm text-gray-400 hover:text-white underline"
                                            >
                                                Retake Quiz
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <button
                                onClick={() => navigate('/')}
                                className="mt-12 px-8 py-3 rounded-full bg-white/10 hover:bg-white/20 text-white font-bold transition-all"
                            >
                                Return to Dashboard
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function QuizInterface({ quizData, onComplete }) {
    const [currentQ, setCurrentQ] = useState(0);
    const [answers, setAnswers] = useState({});

    const handleOptionSelect = (qId, optionIdx) => {
        setAnswers({ ...answers, [qId]: optionIdx });
    };

    const handleNext = () => {
        if (currentQ < quizData.length - 1) {
            setCurrentQ(currentQ + 1);
        } else {
            // Calculate Score
            let correct = 0;
            quizData.forEach(q => {
                if (answers[q.id] === q.correct_index) correct++;
            });
            const finalScore = Math.round((correct / quizData.length) * 100);
            onComplete(finalScore);
        }
    };

    const question = quizData[currentQ];
    const isLast = currentQ === quizData.length - 1;
    const answered = answers[question.id] !== undefined;

    return (
        <div className="glass-card p-8 rounded-2xl border border-indigo-500/20 bg-indigo-900/10">
            <div className="flex justify-between items-center mb-6">
                <span className="text-xs font-bold text-indigo-300 uppercase tracking-widest">Question {currentQ + 1} of {quizData.length}</span>
                <span className="text-xs text-gray-500">{Math.round(((currentQ) / quizData.length) * 100)}% Complete</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-8 leading-relaxed">
                {question.question}
            </h3>

            <div className="space-y-3 mb-8">
                {question.options.map((opt, idx) => (
                    <button
                        key={idx}
                        onClick={() => handleOptionSelect(question.id, idx)}
                        className={`w-full text-left p-4 rounded-xl border transition-all flex items-center gap-3 ${answers[question.id] === idx
                            ? 'bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-900/50'
                            : 'bg-black/20 border-white/5 text-gray-300 hover:bg-white/5 hover:border-white/10'
                            }`}
                    >
                        <div className={`h-6 w-6 rounded-full border flex items-center justify-center text-xs font-bold ${answers[question.id] === idx ? 'bg-white text-indigo-600 border-white' : 'border-gray-500 text-gray-500'
                            }`}>
                            {String.fromCharCode(65 + idx)}
                        </div>
                        {opt}
                    </button>
                ))}
            </div>

            <div className="flex justify-end">
                <button
                    onClick={handleNext}
                    disabled={!answered}
                    className="px-8 py-3 bg-white text-indigo-900 rounded-lg font-bold hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {isLast ? "Submit Quiz" : "Next Question →"}
                </button>
            </div>
        </div>
    );
}


