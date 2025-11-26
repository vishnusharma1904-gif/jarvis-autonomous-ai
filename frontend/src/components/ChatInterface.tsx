import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Mic, FileText, Image as ImageIcon, Sparkles, Settings, Trash2, Plus, Zap, Code, Brain, Globe } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';

const API_BASE = '/api';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
    audio_url?: string;
}

interface Session {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    messages: Message[];
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessions, setSessions] = useState<Session[]>([]);
    const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [mode, setMode] = useState<string>('normal');
    const [useAgent, setUseAgent] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [isPlayingAudio, setIsPlayingAudio] = useState(false);

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        loadSessions();
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const loadSessions = async () => {
        try {
            const response = await axios.get(`${API_BASE}/sessions`);
            setSessions(response.data);
        } catch (error) {
            console.error('Error loading sessions:', error);
        }
    };

    const createNewSession = async () => {
        try {
            const response = await axios.post(`${API_BASE}/sessions`,
                { title: 'New Chat' },
                { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
            );
            const sessionId = response.data.id;
            setCurrentSessionId(sessionId);
            setMessages([]);
            loadSessions();
        } catch (error) {
            console.error('Error creating session:', error);
        }
    };

    const loadSession = async (sessionId: string) => {
        try {
            const response = await axios.get(`${API_BASE}/sessions/${sessionId}`);
            setCurrentSessionId(sessionId);
            setMessages(response.data.messages || []);
        } catch (error) {
            console.error('Error loading session:', error);
        }
    };

    const deleteSession = async (sessionId: string) => {
        try {
            await axios.delete(`${API_BASE}/sessions/${sessionId}`);
            if (currentSessionId === sessionId) {
                setCurrentSessionId(null);
                setMessages([]);
            }
            loadSessions();
        } catch (error) {
            console.error('Error deleting session:', error);
        }
    };

    const sendMessage = async () => {
        if (!input.trim() && !uploadedFile) return;

        const userMessage: Message = {
            role: 'user',
            content: input,
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const formData = new FormData();
            formData.append('message', input);
            formData.append('mode', mode);
            formData.append('use_agent', useAgent.toString());

            if (currentSessionId) {
                formData.append('session_id', currentSessionId);
            }

            if (uploadedFile) {
                formData.append('file', uploadedFile);
                setUploadedFile(null);
            }

            const response = await axios.post(`${API_BASE}/chat`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const assistantMessage: Message = {
                role: 'assistant',
                content: response.data.response,
                audio_url: response.data.audio_url,
            };

            setMessages(prev => [...prev, assistantMessage]);

            if (!currentSessionId) {
                setCurrentSessionId(response.data.session_id);
                loadSessions();
            }
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, I encountered an error processing your request. Please ensure the backend server is running.',
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setUploadedFile(e.target.files[0]);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const playAudio = (url: string) => {
        const audio = new Audio(`${API_BASE}${url}`);
        audio.play();
        setIsPlayingAudio(true);
        audio.onended = () => setIsPlayingAudio(false);
    };

    const getModeIcon = () => {
        switch (mode) {
            case 'coding': return <Code className="w-4 h-4" />;
            case 'quiz': return <Brain className="w-4 h-4" />;
            case 'eli5': return <Sparkles className="w-4 h-4" />;
            default: return <Zap className="w-4 h-4" />;
        }
    };

    return (
        <div className="flex h-screen bg-black relative overflow-hidden">
            {/* Sidebar */}
            <div className="w-80 glass border-r border-white/10 flex flex-col relative z-10">
                {/* Header */}
                <div className="p-4 border-b border-white/10">
                    <div className="flex items-center justify-between mb-4">
                        <h1 className="text-2xl font-bold cyber-text flex items-center gap-2 animate-float">
                            <Sparkles className="w-7 h-7" />
                            Jarvis
                        </h1>
                        <button
                            onClick={() => setShowSettings(!showSettings)}
                            className="p-2 glass rounded-lg hover:bg-white/10 transition-all"
                        >
                            <Settings className="w-5 h-5" />
                        </button>
                    </div>

                    <button
                        onClick={createNewSession}
                        className="w-full bg-gradient-to-r from-[#00f0ff] via-[#b24bf3] to-[#00f0ff] bg-[length:200%_auto] text-black px-4 py-3 rounded-xl font-semibold flex items-center justify-center gap-2 hover:bg-right transition-all duration-500 shadow-lg"
                        style={{ animation: 'gradient-shift 3s ease infinite' }}
                    >
                        <Plus className="w-5 h-5" />
                        New Chat
                    </button>
                </div>

                {/* Settings Panel */}
                {showSettings && (
                    <div className="p-4 border-b border-white/10 holographic">
                        <h3 className="text-sm font-bold mb-3 text-[#00f0ff] flex items-center gap-2">
                            {getModeIcon()}
                            AI Mode
                        </h3>
                        <select
                            value={mode}
                            onChange={(e) => setMode(e.target.value)}
                            className="w-full glass border border-[#00f0ff]/30 rounded-lg px-3 py-2 mb-3 focus:border-[#00f0ff] focus:ring-2 focus:ring-[#00f0ff]/30 transition-all"
                        >
                            <option value="normal" className="bg-gray-900">💬 Normal Chat</option>
                            <option value="coding" className="bg-gray-900">💻 Coding Assistant</option>
                            <option value="quiz" className="bg-gray-900">🎯 Quiz Generator</option>
                            <option value="eli5" className="bg-gray-900">🌟 ELI5 Mode</option>
                            <option value="flashcard" className="bg-gray-900">📚 Flashcards</option>
                        </select>

                        <label className="flex items-center justify-between cursor-pointer glass p-3 rounded-lg hover:bg-white/5 transition-all">
                            <span className="text-sm flex items-center gap-2">
                                <Brain className="w-4 h-4 text-[#b24bf3]" />
                                Autonomous Agent
                            </span>
                            <input
                                type="checkbox"
                                checked={useAgent}
                                onChange={(e) => setUseAgent(e.target.checked)}
                                className="w-5 h-5 accent-[#00f0ff]"
                            />
                        </label>
                    </div>
                )}

                {/* Sessions List */}
                <div className="flex-1 overflow-y-auto p-2">
                    {sessions.map((session) => (
                        <div
                            key={session.id}
                            className={`p-3 rounded-xl cursor-pointer mb-2 group card-hover ${currentSessionId === session.id
                                ? 'glass border-2 border-[#00f0ff] glow'
                                : 'glass hover:bg-white/5'
                                }`}
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1" onClick={() => loadSession(session.id)}>
                                    <div className="text-sm font-medium line-clamp-2">{session.title}</div>
                                    <div className="text-xs text-gray-400 mt-1 flex items-center gap-1">
                                        <Globe className="w-3 h-3" />
                                        {new Date(session.updated_at).toLocaleDateString()}
                                    </div>
                                </div>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        deleteSession(session.id);
                                    }}
                                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded transition-all"
                                >
                                    <Trash2 className="w-4 h-4 text-red-400" />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Status Bar */}
                <div className="p-4 border-t border-white/10 glass">
                    <div className="flex items-center justify-between text-xs">
                        <span className="flex items-center gap-2">
                            {useAgent ? (
                                <>
                                    <div className="w-2 h-2 rounded-full bg-[#00ff88] animate-pulse" />
                                    <span className="text-[#00ff88]">Agent Active</span>
                                </>
                            ) : (
                                <>
                                    <div className="w-2 h-2 rounded-full bg-gray-500" />
                                    <span className="text-gray-400">Chat Mode</span>
                                </>
                            )}
                        </span>
                        <span className="text-gray-500 font-mono">{mode.toUpperCase()}</span>
                    </div>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative z-10">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {messages.length === 0 && (
                        <div className="text-center mt-20">
                            <div className="inline-block animate-float">
                                <Sparkles className="w-20 h-20 text-[#00f0ff] mx-auto mb-6" style={{ filter: 'drop-shadow(0 0 20px rgba(0,240,255,0.7))' }} />
                            </div>
                            <h2 className="text-4xl font-bold cyber-text mb-4">Welcome to Jarvis AI</h2>
                            <p className="text-gray-400 text-lg mb-12">
                                poweredByVishnuSharma
                            </p>
                            <div className="grid grid-cols-2 gap-6 max-w-3xl mx-auto">
                                {[
                                    {
                                        icon: <Brain className="w-8 h-8" />,
                                        title: '🤖 Autonomous Agent',
                                        desc: 'Execute complex multi-step tasks',
                                        action: () => { setUseAgent(true); setInput("I need you to perform a complex task: "); textareaRef.current?.focus(); }
                                    },
                                    {
                                        icon: <Globe className="w-8 h-8" />,
                                        title: '🌐 Web Access',
                                        desc: 'Real-time search & information',
                                        action: () => { setInput("Search for "); textareaRef.current?.focus(); }
                                    },
                                    {
                                        icon: <Code className="w-8 h-8" />,
                                        title: '💻 Code Execution',
                                        desc: 'Run Python code safely',
                                        action: () => { setMode("coding"); setInput("Write a python script to "); textareaRef.current?.focus(); }
                                    },
                                    {
                                        icon: <Sparkles className="w-8 h-8" />,
                                        title: '📚 RAG System',
                                        desc: 'Upload & query documents',
                                        action: () => fileInputRef.current?.click()
                                    }
                                ].map((feature, idx) => (
                                    <div
                                        key={idx}
                                        onClick={feature.action}
                                        className="glass p-6 rounded-2xl card-hover holographic cursor-pointer hover:border-[#00f0ff] transition-all"
                                    >
                                        <div className="text-[#00f0ff] mb-3">{feature.icon}</div>
                                        <h3 className="font-bold text-white mb-2">{feature.title}</h3>
                                        <p className="text-sm text-gray-400">{feature.desc}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-4 duration-500`}
                        >
                            <div
                                className={`max-w-3xl ${message.role === 'user'
                                    ? 'bg-gradient-to-r from-[#00f0ff] via-[#b24bf3] to-[#00f0ff] bg-[length:200%_auto] text-black'
                                    : 'glass glow'
                                    } rounded-2xl px-6 py-4 shadow-2xl`}
                                style={message.role === 'user' ? { animation: 'gradient-shift 3s ease infinite' } : {}}
                            >
                                <div className="markdown-content">
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            code({ node, className, children, ...props }: any) {
                                                const match = /language-(\w+)/.exec(className || '');
                                                const inline = !className;
                                                return !inline && match ? (
                                                    <SyntaxHighlighter
                                                        style={vscDarkPlus as any}
                                                        language={match[1]}
                                                        PreTag="div"
                                                        {...props}
                                                    >
                                                        {String(children).replace(/\n$/, '')}
                                                    </SyntaxHighlighter>
                                                ) : (
                                                    <code className="bg-black/40 px-2 py-0.5 rounded border border-[#00f0ff]/30" {...props}>
                                                        {children}
                                                    </code>
                                                );
                                            },
                                        }}
                                    >
                                        {message.content}
                                    </ReactMarkdown>
                                </div>

                                {message.audio_url && (
                                    <button
                                        onClick={() => playAudio(message.audio_url!)}
                                        className="mt-3 text-xs text-[#00ff88] hover:text-[#00f0ff] flex items-center gap-1 transition-all"
                                        disabled={isPlayingAudio}
                                    >
                                        <Mic className="w-4 h-4" />
                                        {isPlayingAudio ? 'Playing...' : 'Play Audio'}
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex justify-start animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="glass rounded-2xl px-6 py-4 glow">
                                <div className="flex items-center gap-3">
                                    <div className="loading-spinner w-6 h-6"></div>
                                    <div className="flex gap-1">
                                        {[0, 1, 2].map((i) => (
                                            <div
                                                key={i}
                                                className="w-2 h-2 bg-[#00f0ff] rounded-full animate-pulse-slow"
                                                style={{ animationDelay: `${i * 0.2}s` }}
                                            />
                                        ))}
                                    </div>
                                    <span className="text-sm text-gray-300">
                                        {useAgent ? '🤖 Agent analyzing...' : '💭 Jarvis thinking...'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-6 border-t border-white/10 glass">
                    {uploadedFile && (
                        <div className="mb-3 flex items-center gap-2 glass rounded-lg p-3 border border-[#00f0ff]/30">
                            <FileText className="w-5 h-5 text-[#00f0ff]" />
                            <span className="text-sm text-[#00ff88] flex-1">{uploadedFile.name}</span>
                            <button
                                onClick={() => setUploadedFile(null)}
                                className="text-red-400 hover:text-red-300 font-bold"
                            >
                                ×
                            </button>
                        </div>
                    )}

                    <div className="flex items-end gap-3">
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileSelect}
                            className="hidden"
                            accept=".pdf,.docx,.png,.jpg,.jpeg"
                        />

                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="p-3 glass rounded-xl hover:bg-[#00f0ff]/10 hover:border-[#00f0ff] border border-white/10 transition-all"
                            title="Upload file"
                        >
                            {uploadedFile ? (
                                <ImageIcon className="w-5 h-5 text-[#00ff88]" />
                            ) : (
                                <FileText className="w-5 h-5 text-[#00f0ff]" />
                            )}
                        </button>

                        <textarea
                            ref={textareaRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyPress}
                            placeholder="Message Jarvis..."
                            className="flex-1 glass rounded-xl px-4 py-3 resize-none border border-white/10 focus:border-[#00f0ff] focus:ring-2 focus:ring-[#00f0ff]/30 transition-all"
                            rows={1}
                            style={{ minHeight: '48px', maxHeight: '200px' }}
                        />

                        <button
                            onClick={sendMessage}
                            disabled={isLoading || (!input.trim() && !uploadedFile)}
                            className="p-3 bg-gradient-to-r from-[#00f0ff] to-[#b24bf3] text-black rounded-xl hover:shadow-[0_0_30px_rgba(0,240,255,0.5)] transition-all disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:shadow-none"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>

                    <div className="mt-3 text-xs text-center text-gray-500 font-mono flex items-center justify-center gap-2">
                        {useAgent && <Brain className="w-3 h-3 text-[#00ff88]" />}
                        {useAgent ? '🤖 Autonomous Agent Active' : '💬 Chat Mode'} • Press Enter to send, Shift+Enter for new line
                    </div>
                </div>
            </div>
        </div>
    );
}
