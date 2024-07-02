import React, { useEffect, useState } from 'react'
import { fetchStationList, generatePass } from './APIs';

const GeneratePass = () => {
    const [stations, setStations] = useState([]);
    const [passData, setPassData] = useState({
        pass_type: 'trip',
        user_name: '',
        user_contact: '',
        source_station: '',
        destination: '',
        trips: '',
        balance: '',
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

    const handlePassGeneration = async () => {
        console.log(passData)
        try {
            const response = await generatePass(passData);
            console.log('Pass generated successfully : ', response)
        } catch (error) {
            console.error('Error in Pass generation : ', error)
        }
    }

    return (
        <div>
            <h2>Pass Generator</h2>
            <label >Pass Type : </label>
            <input
                type="radio"
                name="pass_type" id='trip'
                value='trip'
                onChange={(e) => setPassData({
                    ...passData,
                    pass_type: e.target.value
                })}
            />
            <label htmlFor="trip">Trip</label>
            <input type="radio"
                name="pass_type" id='balance'
                value='balance'
                onChange={(e) => setPassData({
                    ...passData,
                    pass_type: e.target.value
                })}
            />
            <label htmlFor="balance">Balance</label>
            <br />

            <label htmlFor="user_name">User Name : </label>
            <input
                type="text"
                id='user_name'
                value={passData.user_name}
                onChange={(e) => setPassData({
                    ...passData,
                    user_name: e.target.value
                })}
            />
            <br />
            <label htmlFor="user_contact">User Contact : </label>
            <input
                type="tel"
                id='user_contact'
                value={passData.user_contact}
                onChange={(e) => setPassData({
                    ...passData,
                    user_contact: e.target.value
                })}
            />
            <br />
            {passData.pass_type == 'trip' ? (
                <>
                    <label htmlFor="source_station">Source Station :</label>
                    <select
                        id="source_station"
                        value={passData.source_station}
                        onChange={(e) => setPassData({
                            ...passData,
                            source_station: e.target.value
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
                        value={passData.destination}
                        onChange={(e) => setPassData({
                            ...passData,
                            destination: e.target.value
                        })}
                    >
                        <option value="">select station</option>
                        {stations.map(station => (
                            <option key={station.id} value={station.id}>{station.name}</option>
                        ))}
                    </select>
                    <br />
                    <label htmlFor="trips">No of Trips : </label>
                    <select id="trips"
                    value={passData.trips}
                    onChange={(e) => setPassData({
                        ...passData,
                        trips: e.target.value
                    })}>
                        <option value="">select</option>
                        <option value="45">45</option>
                    </select>
                    <br />
                </>
            ) : (
                <>
                    <label htmlFor="balance">Amount: </label>
                    <input
                        type="number"
                        id='balance'
                        value={passData.balance}
                        onChange={(e) => setPassData({
                            ...passData,
                            balance: e.target.value
                        })}
                    />
                    <br />
                </>
            )}
            <button onClick={handlePassGeneration}>Generate Pass</button>
        </div>
    )
}

export default GeneratePass
