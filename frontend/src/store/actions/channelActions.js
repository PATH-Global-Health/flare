import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import { logout } from "./securityActions";

export const fetchChannelsLookupSuccess = (lookup) => {
  return {
    type: actionTypes.FETCH_CHANNELS_LOOKUP_SUCCESS,
    lookup,
  };
};

export const fetchChannelsLookupFail = (error) => {
  return {
    type: actionTypes.FETCH_CHANNELS_LOOKUP_FAIL,
    error: error,
  };
};

export const fetchChannelsLookupStart = () => {
  return {
    type: actionTypes.FETCH_CHANNELS_LOOKUP_START,
  };
};

export const fetchChannelsLookup = () => {
  return (dispatch) => {
    dispatch(fetchChannelsLookupStart());

    axios
      .get("/channels/?limit=1000")
      .then((res) => {
        const lookup = [];

        res.data.results.forEach((channel, index) =>
          lookup.push({ value: channel.id, label: channel.name })
        );

        dispatch(fetchChannelsLookupSuccess(lookup));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchChannelsLookupFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchChannelsLookupFail(err.response.data.message));
          }
        }
      });
  };
};
