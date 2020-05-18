import axios from "axios";
import hostURL from "./hostURL";

const instance = axios.create({
  baseURL: hostURL() + "/api/",
  // baseURL: "http://localhost:8000/api/",
});

export default instance;
