import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import { logout } from "./securityActions";

export const fetchDashboardDataSuccess = (dashboardData) => {
  return {
    type: actionTypes.FETCH_DASHBOARD_DATA_SUCCESS,
    data: dashboardData,
  };
};

export const fetchDashboardDataFail = (error) => {
  return {
    type: actionTypes.FETCH_DASHBOARD_DATA_FAIL,
    error: error,
  };
};

export const fetchDashboardDataStart = () => {
  return {
    type: actionTypes.FETCH_DASHBOARD_DATA_START,
  };
};

export const fetchDashboardData = () => {
  return (dispatch) => {
    dispatch(fetchDashboardDataStart());

    axios
      .get("/reports/")
      .then((res) => {
        let data = res.data;

        if (data.hasOwnProperty("suspects_by_region")) {
          data.suspects_by_region = JSON.parse(data.suspects_by_region);
        }

        if (data.hasOwnProperty("suspects_by_age")) {
          data.suspects_by_age = JSON.parse(data.suspects_by_age);
        }

        if (data.hasOwnProperty("suspects_by_sex")) {
          data.suspects_by_sex = JSON.parse(data.suspects_by_sex);
        }

        dispatch(fetchDashboardDataSuccess(data));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchDashboardDataFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchDashboardDataFail(err.response.data.message));
          }
        }
      });
  };
};
