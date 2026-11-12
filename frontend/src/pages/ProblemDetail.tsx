import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/axios';

interface Problem {
  title: string;
  description: string;
  input_spec: string;
  output_spec: string;
  constraints: string;
  difficulty: string;
  test_cases: { input_data: string; expected_output: string; is_sample: boolean }[];
}

export default function ProblemDetail() {
  const { id } = useParams();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('Python');
  const [status, setStatus] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    api.get(`/problems/${id}`).then(res => setProblem(res.data)).catch(err => console.error(err));
  }, [id]);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setStatus('Submitting...');
    try {
      const response = await api.post('/submissions/', {
        problem_id: parseInt(id as string),
        language: language,
        code: code
      });
      
      const subId = response.data.id;
      setStatus('Evaluating...');
      
      const interval = setInterval(async () => {
        try {
          const check = await api.get(`/submissions/${subId}`);
          if (check.data.status !== 'Pending') {
            setStatus(check.data.status);
            clearInterval(interval);
            setIsSubmitting(false);
          }
        } catch (e) { clearInterval(interval); }
      }, 2000);
      
    } catch (err: any) {
      setStatus(err.response?.data?.detail || 'Submission failed');
      setIsSubmitting(false);
    }
  };

  if (!problem) return <div className="text-center mt-20 text-xl">Loading problem...</div>;

  return (
    <div className="max-w-7xl mx-auto mt-6 flex gap-6">
      <div className="w-1/2 bg-white p-6 rounded-lg shadow overflow-y-auto h-[80vh]">
        <Link to="/problems" className="text-blue-500 text-sm mb-4 inline-block">&larr; Back to Problems</Link>
        <h1 className="text-3xl font-bold mb-2">{problem.title}</h1>
        <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-sm">{problem.difficulty}</span>
        
        <div className="mt-6 space-y-4 text-gray-700">
          <p>{problem.description}</p>
          
          <h3 className="font-bold text-lg mt-4">Input Specification</h3>
          <p>{problem.input_spec}</p>
          
          <h3 className="font-bold text-lg mt-4">Output Specification</h3>
          <p>{problem.output_spec}</p>
          
          <h3 className="font-bold text-lg mt-4">Constraints</h3>
          <p>{problem.constraints}</p>

          <h3 className="font-bold text-lg mt-4">Sample Tests</h3>
          {problem.test_cases.filter(tc => tc.is_sample).map((tc, idx) => (
            <div key={idx} className="bg-gray-50 p-4 rounded border font-mono text-sm">
              <div className="mb-2"><strong>Input:</strong><br/>{tc.input_data}</div>
              <div><strong>Output:</strong><br/>{tc.expected_output}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="w-1/2 flex flex-col h-[80vh]">
        <div className="bg-white rounded-lg shadow flex flex-col flex-grow">
          <div className="flex justify-between items-center p-3 border-b bg-gray-50 rounded-t-lg">
            <select value={language} onChange={(e) => setLanguage(e.target.value)} className="border rounded p-2 bg-white text-sm font-medium">
              <option value="Python">Python 3</option>
              <option value="C++">C++</option>
              <option value="Java">Java</option>
            </select>
            <button 
              onClick={handleSubmit} 
              disabled={isSubmitting}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-6 py-2 rounded font-bold transition-colors"
            >
              {isSubmitting ? 'Running...' : 'Submit Code'}
            </button>
          </div>
          
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder={`Write your ${language} code here...`}
            className="w-full flex-grow p-4 font-mono text-sm focus:outline-none resize-none rounded-b-lg"
            spellCheck="false"
          />
        </div>

        {status && (
          <div className={`mt-4 p-4 rounded-lg font-bold text-center border ${
            status === 'Accepted' ? 'bg-green-100 text-green-800 border-green-300' : 
            status === 'Pending' || status === 'Evaluating...' || status === 'Submitting...' ? 'bg-blue-100 text-blue-800 border-blue-300' :
            'bg-red-100 text-red-800 border-red-300'
          }`}>
            Status: {status}
          </div>
        )}
      </div>
    </div>
  );
}
