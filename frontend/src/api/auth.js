import axios from "./axios";

export const login = async (identifier, password) => {
  const params = new URLSearchParams();
  params.append("username", identifier); // works for both username or email
  params.append("password", password);

  const response = await axios.post("/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return response.data;
};
