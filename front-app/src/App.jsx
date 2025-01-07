import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import EmailSender from "./EmailSender"; 
import Job from './job';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
    <header className="App-header">
      <h1 className="text-center mt-4"> Aubay Job Applications Analysis</h1>
    </header>
    <main className="container">
      {/* Inclure le composant EmailSender */}
      <EmailSender />
    </main>
  </div>
  )
}

export default App
