import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';

interface Problem {
  id: number;
  title: string;
  difficulty: string;
  category: string;
}

export default function Problems() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/problems/').then(res => setProblems(res.data)).catch(err => console.error(err)).finally(() => setLoading(false));
  }, []);

  const getDifficultyColor = (diff: string) => {
    if (diff === 'Easy') return 'bg-green-100 text-green-800';
    if (diff === 'Medium') return 'bg-yellow-100 text-yellow-800';
    if (diff === 'Hard') return 'bg-red-100 text-red-800';
    return 'bg-purple-100 text-purple-800';
  };

  if (loading) return <div className="text-center mt-20 text-xl">Loading...</div>;

  return (
    <div className="max-w-5xl mx-auto mt-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Problem Set</h1>
      <div className="space-y-4">
        {problems.map((problem) => (
          <Link to={`/problems/${problem.id}`} key={problem.id} className="block bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold text-blue-600 mb-1">{problem.title}</h2>
                <p className="text-sm text-gray-500">Category: {problem.category}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${getDifficultyColor(problem.difficulty)}`}>
                {problem.difficulty}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
