import React, { useEffect, useState } from 'react'
import { fetchStationList } from './APIs';

const Stations = (Label) => {
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
  
  const handleDataGeneration = async () => {
    try {
      const responce = await generateTicket(selectedStation);
      console.log(Label+' generated succesfully: ', responce);
    } catch (error) {
      console.error(`error generating ${Label} : `, error);
    }
  }

  return (
    <div>
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
      {/* <button onClick={handleDataGeneration}>Generate {Label}</button> */}
    </div>
  )
}

export default Stations
