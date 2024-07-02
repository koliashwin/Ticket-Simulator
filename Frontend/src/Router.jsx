import React from 'react';
import {Route, BrowserRouter as Router, Routes} from 'react-router-dom';
import Nav from './components/Nav';
import GenerateTicket from './components/GenerateTicket';
import ScanTicket from './components/ScanTicket';
import GeneratePass from './components/GeneratePass';
import TicketTemplate from './templets/TicketTemplate';

const MyRouter = () => {
  return (
    <Router>
        <Nav />
        <Routes>
            <Route path='/generate-ticket' element={<GenerateTicket/>} />
            <Route path='/scan-ticket' element={<ScanTicket/>} />
            <Route path='/generate-pass' element={<GeneratePass/>} />
            <Route path='/ticket-template' element={<TicketTemplate name={'TKT-5893'} cost={20} source={'Versova'} destination={'Andheri'} qr_code={'D:/Git-hub repo/Metro QR/Backend/qr_codes/TKT-5893.png'} />} />
        </Routes>
    </Router>
  )
}

export default MyRouter
