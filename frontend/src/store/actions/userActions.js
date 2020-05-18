import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import { logout } from "./securityActions";

export const fetchUserSuccess = (data) => {
  return {
    type: actionTypes.FETCH_USER_SUCCESS,
    data: data,
  };
};

export const fetchUserFail = (error) => {
  return {
    type: actionTypes.FETCH_USER_FAIL,
    error: error,
  };
};

export const fetchUserStart = () => {
  return {
    type: actionTypes.FETCH_USER_START,
  };
};

export const fetchUser = () => {
  return (dispatch) => {
    dispatch(fetchUserStart());

    axios
      .get("/auth/user")
      .then((res) => {
        dispatch(fetchUserSuccess(res.data));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchUserFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchUserFail(err.response.data.message));
          }
        }
      });
  };
};
