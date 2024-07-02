import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { fetchStationList, generateTicket } from './APIs';
import TicketTemplate from '../templets/TicketTemplate';

const GenerateTicket = () => {
  const [renderedTicket, setRenderedTicket] = useState(null);
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState({
    source: '',
    destination: ''
  })

  useEffect(() => {
    loadStations();
  }, []);

  const loadStations = async () => {
    try {
      const stationData = await fetchStationList();
      setStations(stationData);
    } catch (error) {
      console.error('Error fetching stations : ', error)
    }
  }

  const handleTicketGeneration = async () => {
    try {
      const responce = await generateTicket(selectedStation);
      console.log('tickt generated succesfully: ', responce[1]);
      const ticketData = responce[1][0]
      
      setRenderedTicket(
        <TicketTemplate 
          name={ticketData[0]}
          cost={ticketData[4]}
          source={ticketData[2]}
          destination={ticketData[3]}
        />
      )
    } catch (error) {
      console.error('error generating ticket : ', error);
    }
  }

  return (
    <div>
      <h2>Ticket Generator</h2>
      <label htmlFor="source_station">Source Station :</label>
      <select 
        id="source_station"
        value={selectedStation.source}
        onChange={(e) => setSelectedStation({
          ...selectedStation,
          source: e.target.value
        })}
      >
        <option value="">select station</option>
        {stations.map(station => (
          <option key={station.id} value={station.id}>{station.name}</option>
        ))}
      </select>
      <br />
      <label htmlFor="destination">Destination :</label>
      <select 
        id="destination"
        value={selectedStation.destination}
        onChange={(e) => setSelectedStation({
          ...selectedStation,
          destination: e.target.value
        })}
      >
        <option value="">select station</option>
        {stations.map(station => (
          <option key={station.id} value={station.id}>{station.name}</option>
        ))}
      </select>
      <br />
      <button onClick={handleTicketGeneration}>Generate Ticket</button>
      {renderedTicket && renderedTicket}
    </div>
  )
}

export default GenerateTicket
