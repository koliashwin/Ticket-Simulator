import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Test = () => {
  const [data, setData] = useState([]);
  const [formData, setFormData] = useState({});
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data: ', error)
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedId){
        await axios.put(`http://localhost:5000/api/data/${selectedId}`, formData);
      }
      else{
        await axios.post('http://localhost:5000/api/data', formData);
      }
      fetchData();
      setFormData({});
      setSelectedId(null);
    } catch (error) {
      console.error('Error adding/editing data : ', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/data/${id}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting data : ', error)
    }
  };

  const handleEdit = (id) => {
    const selectedItem = data.find(item => item.id === id);
    setFormData({...selectedItem});
    setSelectedId(id);
  }

  return (
    <div>
      <h1>CRUD Operations</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Enter name" value={formData.name || ''} onChange={handleInputChange} />
        <button type="submit">{selectedId ? 'Update':'Add'}</button>
      </form>
      <ul>
        {data.map(item => (
          <li key={item.id}>
            {item.name}
            <button onClick={() => handleEdit(item.id)}>Edit</button>
            <button onClick={() => handleDelete(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Test;
