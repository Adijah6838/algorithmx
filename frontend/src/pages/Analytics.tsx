import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import api from '../api/axios';

interface Stats {
  total_users: number;
  total_problems: number;
  total_submissions: number;
  total_contests: number;
  submission_statuses: Record<string, number>;
}

const COLORS = ['#10b981', '#ef4444', '#f59e0b', '#6366f1', '#8b5cf6', '#ec4899', '#9ca3af'];

export default function Analytics() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/analytics/')
      .then(res => setStats(res.data))
      .catch(err => setError(err.response?.status === 403 ? 'Access Denied: Admin or Moderator required' : 'Failed to load analytics.'));
  }, []);

  if (error) return <div className="text-center mt-20 text-red-500 font-bold text-xl">{error}</div>;
  if (!stats) return <div className="text-center mt-20 text-xl">Loading analytics...</div>;

  // Format data for the Pie Chart
  const pieData = Object.keys(stats.submission_statuses)
    .map(key => ({ name: key, value: stats.submission_statuses[key] }))
    .filter(item => item.value > 0); // Hide zero-count statuses from the pie

  // Format data for the Bar Chart
  const barData = [
    { name: 'Users', count: stats.total_users },
    { name: 'Problems', count: stats.total_problems },
    { name: 'Submissions', count: stats.total_submissions },
    { name: 'Contests', count: stats.total_contests },
  ];

  return (
    <div className="max-w-6xl mx-auto mt-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Platform Analytics</h1>
      
      {/* Top Row: Summary Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
          <p className="text-gray-500 text-sm font-medium">Total Users</p>
          <p className="text-3xl font-bold text-blue-600">{stats.total_users}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
          <p className="text-gray-500 text-sm font-medium">Total Problems</p>
          <p className="text-3xl font-bold text-green-600">{stats.total_problems}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
          <p className="text-gray-500 text-sm font-medium">Total Submissions</p>
          <p className="text-3xl font-bold text-purple-600">{stats.total_submissions}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
          <p className="text-gray-500 text-sm font-medium">Total Contests</p>
          <p className="text-3xl font-bold text-orange-500">{stats.total_contests}</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-8">
        
        {/* Submission Statuses (Donut Chart) */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-bold text-gray-700 mb-4 text-center">Submission Statuses</h2>
          <div className="h-80">
            {pieData.length === 0 ? (
              <div className="flex items-center justify-center h-full text-gray-400">No submissions yet</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend verticalAlign="bottom" height={36}/>
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Platform Activity (Bar Chart) */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-xl font-bold text-gray-700 mb-4 text-center">Platform Activity</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                <YAxis allowDecimals={false} axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: '#f3f4f6'}} />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={50} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
