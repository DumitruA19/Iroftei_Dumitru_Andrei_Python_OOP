import axios from './axios';

export const calculatePower = async (input, token) => {
  const res = await axios.post("/pow", input, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

export const calculateFactorial = async (input, token) => {
  const res = await axios.post("/factorial", input, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

export const calculateFibonacci = async (input, token) => {
  const res = await axios.post("/fibonacci", input, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};
