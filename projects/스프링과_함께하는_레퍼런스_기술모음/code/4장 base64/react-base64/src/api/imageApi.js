import axios from 'axios';

const BASE_URL = 'http://localhost:8080';

const axiosJson = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const imageApi = {
  upload(fileName, fileData) {
    const payload = { fileName, fileData };
    return axiosJson.post('/upload', payload);
  },

  list() {
    return axios.get(`${BASE_URL}/list`);
  },

  detail(id) {
    return axios.get(`${BASE_URL}/${id}`);
  },
};
