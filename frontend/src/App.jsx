import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, 
  Search, 
  BarChart3, 
  Trees, 
  History, 
  ChevronRight,
  TrendingUp,
  Users,
  AlertCircle
} from 'lucide-react';
import { 
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';

const API_BASE = "http://localhost:8000";

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { id: 'predict', label: 'Analisis Baru', icon: <Search size={20} /> },
    { id: 'visualize', label: 'Struktur Model', icon: <Trees size={20} /> },
    { id: 'history', label: 'Statistik Data', icon: <History size={20} /> },
  ];

  return (
    <div className="sidebar glass-panel">
      <div style={{ marginBottom: '3rem', paddingLeft: '1rem' }}>
        <h2 style={{ color: '#10b981', fontSize: '1.5rem' }}>BPMA <span style={{ color: '#fff' }}>STAKE</span></h2>
        <p style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Monitoring System v2.0</p>
      </div>
      {menuItems.map(item => (
        <div 
          key={item.id}
          className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
          onClick={() => setActiveTab(item.id)}
        >
          {item.icon}
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
};

const Dashboard = ({ stats }) => {
  if (!stats) return <div className="animate-fade-in">Loading Statistics...</div>;

  const pieData = Object.entries(stats.label_distribution).map(([name, value]) => ({ name, value }));
  const COLORS = ['#10b981', '#ef4444'];

  const scoreData = [
    { name: 'Komunikasi', value: stats.average_scores.Komunikasi },
    { name: 'Laporan', value: stats.average_scores.Laporan },
    { name: 'Rapat', value: stats.average_scores.Rapat },
    { name: 'Partisipasi', value: stats.average_scores.Partisipasi },
  ];

  return (
    <div className="animate-fade-in">
      <h1 style={{ marginBottom: '2rem' }}>Overview Monitor</h1>
      
      <div className="grid-2">
        <div className="glass-panel card">
          <h3>Distribusi Hubungan</h3>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel card">
          <h3>Rata-rata Skor Interaksi</h3>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis domain={[0, 3]} stroke="#94a3b8" />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: '1.5rem' }}>
         <div className="glass-panel card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '1rem', borderRadius: '12px' }}>
              <Users color="#10b981" />
            </div>
            <div>
              <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Total Stakeholder</p>
              <h2 style={{ fontSize: '1.8rem' }}>{stats.total_kkks}</h2>
            </div>
         </div>
         <div className="glass-panel card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '1rem', borderRadius: '12px' }}>
              <BarChart3 color="#3b82f6" />
            </div>
            <div>
              <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Total Record Data</p>
              <h2 style={{ fontSize: '1.8rem' }}>{stats.total_records}</h2>
            </div>
         </div>
      </div>
    </div>
  );
};

const PredictForm = () => {
  const [formData, setFormData] = useState({
    nama_kkks: '',
    skor_komunikasi: 2.0,
    skor_laporan: 2.0,
    skor_rapat: 2.0,
    skor_partisipasi: 2.0
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/predict`, formData);
      setResult(res.data);
    } catch (err) {
      alert("Error predicting status. Make sure API is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <h1>Analisis Hubungan Baru</h1>
      <div className="grid-2">
        <div className="glass-panel card">
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label>Nama KKKS</label>
              <input 
                type="text" 
                placeholder="Masukkan nama stakeholder..." 
                value={formData.nama_kkks}
                onChange={e => setFormData({...formData, nama_kkks: e.target.value})}
                required
              />
            </div>
            {['komunikasi', 'laporan', 'rapat', 'partisipasi'].map(field => (
              <div className="input-group" key={field}>
                <label style={{ textTransform: 'capitalize' }}>Skor {field} (1.0 - 3.0)</label>
                <input 
                  type="number" 
                  step="0.5" 
                  min="1" 
                  max="3" 
                  value={formData[`skor_${field}`]}
                  onChange={e => setFormData({...formData, [`skor_${field}`]: parseFloat(e.target.value)})}
                />
              </div>
            ))}
            <button className="btn-primary" style={{ width: '100%' }} disabled={loading}>
              {loading ? 'Menganalisis...' : 'Mulai Analisis CART'}
            </button>
          </form>
        </div>

        <div>
          {result ? (
            <div className="glass-panel card prediction-result animate-fade-in">
              <p style={{ color: '#94a3b8', marginBottom: '1rem' }}>Hasil Prediksi Model:</p>
              <h2 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>{result.nama_kkks}</h2>
              <div className={`status-badge ${result.label === 'Harmonis' ? 'status-harmonis' : 'status-kurang'}`}>
                {result.label}
              </div>
              <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '2rem' }}>
                <div>
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Confidence</p>
                  <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{(result.confidence * 100).toFixed(0)}%</p>
                </div>
                <div>
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Algorithm</p>
                  <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>CART</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="glass-panel card" style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', color: '#94a3b8' }}>
              <AlertCircle size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
              <p>Belum ada data analisis.<br/>Silakan isi form untuk memulai prediksi.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const TreeVisualizer = () => {
  return (
    <div className="animate-fade-in">
      <h1>Struktur Keputusan CART</h1>
      <div className="glass-panel card">
        <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>Visualisasi pohon keputusan (Decision Tree) yang digunakan sistem untuk mengklasifikasi hubungan stakeholder.</p>
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1rem', overflow: 'hidden' }}>
          <img 
            src={`${API_BASE}/visualize-tree`} 
            alt="Decision Tree CART" 
            style={{ width: '100%', height: 'auto', display: 'block' }} 
          />
        </div>
      </div>
    </div>
  );
};

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get(`${API_BASE}/stats`);
        setStats(res.data);
      } catch (err) {
        console.error("Failed to fetch stats", err);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="main-content">
        {activeTab === 'dashboard' && <Dashboard stats={stats} />}
        {activeTab === 'predict' && <PredictForm />}
        {activeTab === 'visualize' && <TreeVisualizer />}
        {activeTab === 'history' && (
          <div className="animate-fade-in">
            <h1>Statistik Data</h1>
            <div className="glass-panel card">
              <pre style={{ fontSize: '0.8rem', color: '#10b981' }}>{JSON.stringify(stats, null, 2)}</pre>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
