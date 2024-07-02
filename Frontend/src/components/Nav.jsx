import React from 'react';
import { Link } from 'react-router-dom';

const Nav = () => {
  return (
    <nav style={{position: 'fixed' , top:0, left:'20vw', right:'20vw'}}>
        <ul>
            <button style={{width:"180px"}}>
                <Link to="/generate-ticket">Generate Ticket</Link>
            </button>
            <button style={{width:"180px"}}>
                <Link to="/scan-ticket">Scan Ticket</Link>
            </button>
            <button style={{width:"180px"}}>
                <Link to="/generate-pass">Generate Pass</Link>
            </button>
            <button style={{width:"180px"}}>
                <Link to="/ticket-template">Ticket Sample</Link>
            </button>
        </ul>
    </nav>
  )
}

export default Nav
