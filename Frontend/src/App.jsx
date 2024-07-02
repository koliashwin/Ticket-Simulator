import { useState } from 'react'
import './App.css'
import MyRouter from './Router'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='App'>
      <MyRouter />
    </div>
  )
}

export default App
