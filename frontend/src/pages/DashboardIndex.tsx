import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function DashboardIndex() {
  const auth = useContext(AuthContext);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold text-green-600 mb-2">Welcome to AlgorithmX!</h2>
      <p className="text-gray-600">Navigate to the <strong>Problems</strong> tab to start solving challenges.</p>
    </div>
  );
}
