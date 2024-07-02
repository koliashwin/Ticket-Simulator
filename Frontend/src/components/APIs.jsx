import axios from "axios";

const baseURL = 'http://localhost:5000/api'

export const fetchStationList = async () => {
    try {
        const responce = await axios.get(`${baseURL}/stations`);
        return responce.data;
    } catch (error) {
        console.error('error station fetching API : ', error);
        throw error;
    }
};

export const generateTicket = async (selectedStation) => {
    try {
        const responce = await axios.post(`${baseURL}/generate`, selectedStation);
        return responce.data
        // console.log('tickt generated succesfully: ', responce.data)
        // console.log(selectedStation)
    } catch (error) {
        console.error('error in Ticket Generation API : ', error);
        throw error;
    }
};

export const generatePass = async (passData) => {
    try {
        const response = await axios.post(`${baseURL}/generate_pass`, passData);
        return response.data;
    } catch (error) {
        console.error('error in Pass generation API : ', error);
        throw error;
    }
}