import { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);
  const [dashboardMsg, setDashboardMsg] = useState('');
  const [paymentAmount, setPaymentAmount] = useState(0);

  const handleRegister = async () => {
    await axios.post('http://localhost:8000/register', { username, password });
    alert('Registered Successfully ✅');
  };

  const handleLogin = async () => {
    const res = await axios.post('http://localhost:8000/login', { username, password });
    setToken(res.data.access_token);
    alert('Logged In ✅');
  };

  const accessDashboard = async () => {
    const res = await axios.get('http://localhost:8000/dashboard', {
      headers: { Authorization: `Bearer ${token}` },
    });
    setDashboardMsg(res.data.message);
  };

  const handlePayment = async () => {
    const res = await axios.post('http://localhost:8000/create-payment', { amount: paymentAmount });
    alert(`Payment Link Created ✅\nSecret: ${res.data.client_secret}`);
  };

  return (
    <div className="flex flex-col items-center p-8 space-y-6">
      <h1 className="text-3xl font-bold">AI SaaS Product 🚀</h1>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="p-2 border rounded-md w-1/2"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="p-2 border rounded-md w-1/2"
      />

      <div className="space-x-4">
        <button onClick={handleRegister} className="bg-blue-500 text-white p-2 rounded-md">Register ✅</button>
        <button onClick={handleLogin} className="bg-green-500 text-white p-2 rounded-md">Login 🔥</button>
      </div>

      <button onClick={accessDashboard} className="bg-purple-500 text-white p-2 rounded-md">Access Dashboard 🚀</button>
      {dashboardMsg && <p>{dashboardMsg}</p>}

      <input
        type="number"
        placeholder="Payment Amount"
        value={paymentAmount}
        onChange={(e) => setPaymentAmount(e.target.value)}
        className="p-2 border rounded-md w-1/2"
      />
      <button onClick={handlePayment} className="bg-yellow-500 text-white p-2 rounded-md">Stripe Payment 💳</button>
    </div>
  );
};

export default App;
