import React from 'react'
import './templet_styles.css'
const TicketTemplate = ({name, source, destination, cost}) => {
  return (
    <div className='ticket'>
      <div className='ticket-header'>
        <h2>Ticket</h2>
      </div>
      <div className='ticket-details'>
        <p><strong>Name : </strong>{name}</p>
        <p><strong>From : </strong>{source}</p>
        <p><strong>To : </strong>{destination}</p>
        <p><strong>Cost : </strong>Rs. {cost}/-</p>
      </div>
      <div className='ticket-qrcode'>
        <img src="" alt="QR Code" className='qrcode-img' />
      </div>
    </div>
  )
}

export default TicketTemplate
