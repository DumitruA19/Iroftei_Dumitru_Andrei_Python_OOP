import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Change if needed
});

export default instance;
