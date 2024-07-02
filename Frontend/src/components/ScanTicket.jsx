import axios from 'axios';
import React, { useState } from 'react'

const ScanTicket = () => {
    const [scannerType, setScannerType] = useState(1);
    const handleTicketScanner = async (scan_type) => {
        try {
          setScannerType(scan_type)
          console.log(scannerType, scan_type)
          const responce = await axios.get(`http://localhost:5000/api/scan/${scan_type}`)
          console.log('scanner opened : ', responce.data)
        } catch (error) {
          console.error('error in scanner : ', error);
        }
      }
  return (
    <div>
      <h1>Scanner</h1>
      <button onClick={() => handleTicketScanner(1)}>Check-In Scanner</button>
      <button onClick={() => handleTicketScanner(0)}>Check-Out Scanner</button>
    </div>
  )
}

export default ScanTicket
