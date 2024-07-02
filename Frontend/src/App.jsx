import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import GenerateTicket from './components/GenerateTicket'
import ScanTicket from './components/ScanTicket'
import GeneratePass from './components/GeneratePass'
import TicketTemplate from './templets/TicketTemplate'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <GeneratePass />
      <GenerateTicket />
      <ScanTicket />
      <TicketTemplate name={'TKT-2578'} cost={20} source={'Versova'} destination={'Andheri'} />
    </>
  )
}

export default App
