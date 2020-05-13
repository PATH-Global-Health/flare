import axios from "./axiosFlare";

const setToken = (token) => {
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Token ${token}`;
    //axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
  } else {
    delete axios.defaults.headers.common["Authorization"];
  }
};

export default setToken;
