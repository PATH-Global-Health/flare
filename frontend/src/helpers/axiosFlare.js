import axios from "axios";
import hostURL from "./hostURL";

const instance = axios.create({
  baseURL: hostURL() + "/api/",
});

export default instance;
